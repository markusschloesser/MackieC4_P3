# coding=utf-8
# was once Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/EncoderController.py
# Compiled at: 2011-01-22 05:02:32
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals  # MS
from __future__ import division

import time
import logging

from ableton.v2.base import liveobj_valid, liveobj_changed, find_if, listens
from ableton.v2.control_surface.elements.display_data_source import adjust_string
from ableton.v2.control_surface.component import Component
from ableton.v3.live.action import toggle_or_cycle_parameter_value
import ableton.v3.live.util as v3_util


import Live

from . import script_utils
# from .script_utils import CoolDown, TooSoon
from .script_utils import EncoderDisplaySegment
from .EncoderControllerDataStore import EncoderControllerDataStore, track_callback_types
from . import mode_utils_track_channel_strip as tcs_mode_util
from . import mode_utils_track_device as td_mode_util
from . import mode_utils_song_function as sf_mode_util
from . import mode_utils_user as usr_mode_util
from .MackieC4Component import *
from _Generic.Devices import *

class ButtonController(object):
    """Tracks the state of all nineteen C4 "control buttons" 7 with associated LEDs (nine LEDs) and 12 without.  For the 12 buttons without an LED, """ \
    """the LED state value depends on the way the button is used.  For the Modifier Group buttons (Shift, Option, Control, Alt), the pressed state determines the  """ \
    """LED state, if the button had an LED, it would be ON when the button "is pressed", OFF otherwise.  For the Assignment Group buttons (Marker, Track, Chan Strip, """ \
    """Function), which do have LEDs, the LEDs in the group act like 'radio buttons', only one can be ON (selected) at a time, and it stays ON until another button in """ \
    """the group is pressed and its LED turns ON instead.  The Single Left and Single Right buttons in the Parameter group also follow the press & hold Modifier group """ \
    """button behavior pattern, but generally all non-Modifier group buttons "react" on_press, 'ignoring' on_release button events. The Split button has three associated """\
    """LEDs labelled 1/3, 2/2, 3/1 respectively, but ignore the 'denominator' and imagine they are just labelled 1, 2, 3.  Each Split button press turns ON one more LED, """\
    """first 1, then 2, then 3 turn ON before the next press turns them all OFF again. """

    def __init__(self, last_assignment_mode=C4M_FUNCTION, init_assignment_mode=C4M_CHANNEL_STRIP):

        self.function_group_buttons = {
            C4SID_SPLIT: {"led_id": {C4SID_SPLIT: {"virtual_press_count": 0, "led_value": [0, 127]},
                                     C4SID_SPLIT + 1: {"virtual_press_count": 0, "led_value": [0, 127]},
                                     C4SID_SPLIT + 2: {"virtual_press_count": 0, "led_value": [0, 127]}},  "press_count": 0},
            C4SID_LOCK: {"led_id": {C4SID_LOCK: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_SPLIT_ERASE: {"led_id": {C4SID_SPLIT_ERASE: {"led_value": [0, 127]}}, "press_count": 0}
        }
        self.assignment_group_buttons = {
            C4SID_MARKER: {"led_id": {C4SID_MARKER: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_TRACK: {"led_id": {C4SID_TRACK: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_CHANNEL_STRIP: {"led_id": {C4SID_CHANNEL_STRIP: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_FUNCTION: {"led_id": {C4SID_FUNCTION: {"led_value": [0, 127]}}, "press_count": 0}
        }
        self.modifier_group_buttons = {
            C4SID_SHIFT: {"led_id": {C4SID_SHIFT: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_OPTION: {"led_id": {C4SID_OPTION: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_CONTROL: {"led_id": {C4SID_CONTROL: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_ALT: {"led_id": {C4SID_ALT: {"led_value": [0, 127]}}, "press_count": 0}
        }
        self.parameter_group_buttons = {
            C4SID_BANK_LEFT: {"led_id": {C4SID_BANK_LEFT: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_BANK_RIGHT: {"led_id": {C4SID_BANK_RIGHT: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_SINGLE_LEFT: {"led_id": {C4SID_SINGLE_LEFT: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_SINGLE_RIGHT: {"led_id": {C4SID_SINGLE_RIGHT: {"led_value": [0, 127]}}, "press_count": 0}
        }
        self.session_group_buttons = {
            C4SID_TRACK_LEFT: {"led_id": {C4SID_TRACK_LEFT: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_TRACK_RIGHT: {"led_id": {C4SID_TRACK_RIGHT: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_SLOT_UP: {"led_id": {C4SID_SLOT_UP: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_SLOT_DOWN: {"led_id": {C4SID_SLOT_DOWN: {"led_value": [0, 127]}}, "press_count": 0}
        }
        self.modifier_group_multi_press_definitions = {
            "none": 0,
            "shift_only": 1,
            "option_only": 2,
            "control_only": 4,
            "alt_only": 8,
            "expand_chains": 12  # Control + Alt == 8 + 4
        }

        self.__split_led_ids = [0, 1, 2, 3]
        self.__split_led_cycle_index = 0

        # these two assignments just declare the two dunder vars
        self.__last_assignment_led_on = assignment_mode_to_button_id[last_assignment_mode]
        self.__current_assignment_led_on = assignment_mode_to_button_id[init_assignment_mode]
        # this update uses "button press" semantics
        self._update_assignment_button_state(assignment_mode_to_button_id[init_assignment_mode]) # init is now current (led is ON) and last remains last (led is OFF)

    @property
    def split_led_cycle_index(self):
        return self.__split_led_cycle_index
    @property
    def nbr_split_leds_on(self):
        return self.split_led_cycle_index
    @property
    def last_assignment_led_on(self):
        return self.__last_assignment_led_on
    @property
    def last_active_script_mode(self):
        return button_id_to_assignment_mode[self.last_assignment_led_on]
    @property
    def current_assignment_led_on(self):
        return self.__current_assignment_led_on
    @property
    def current_active_script_mode(self):
        return button_id_to_assignment_mode[self.current_assignment_led_on]
    @property
    def nbr_modifier_btns_pressed(self):
        rtn = self.modifier_button_bit_field()
        if rtn in [1, 2, 4, 8]:
            rtn = 1
        elif rtn in [3, 5, 6, 9, 10, 12]:
            rtn = 2
        elif rtn in [7, 11, 13, 14]:
            rtn = 3
        elif rtn == 15:
            rtn = 4
        return rtn

    @property
    def is_expand_chains_modifier_press_combo(self):
        return self.modifier_button_bit_field() == self.modifier_group_multi_press_definitions["expand_chains"]

    @property
    def split_led_states(self):
        btn_ref = self.function_group_buttons[C4SID_SPLIT]
        btn_led_ref = btn_ref["led_id"]

        toggle = btn_led_ref[C4SID_SPLIT]["virtual_press_count"] % 2
        out_value_00 = btn_led_ref[C4SID_SPLIT]["led_value"][toggle]
        toggle = btn_led_ref[C4SID_SPLIT + 1]["virtual_press_count"] % 2
        out_value_01 = btn_led_ref[C4SID_SPLIT + 1]["led_value"][toggle]
        toggle = btn_led_ref[C4SID_SPLIT + 2]["virtual_press_count"] % 2
        out_value_02 = btn_led_ref[C4SID_SPLIT + 2]["led_value"][toggle]
        return out_value_00, out_value_01, out_value_02
    @property
    def lock_led_state(self):
        return self.get_function_btn_led_state(C4SID_LOCK)
    @property
    def spot_erase_led_state(self):
        return self.get_function_btn_led_state(C4SID_SPLIT_ERASE)

    @property
    def marker_led_state(self):
        return self.get_assignment_btn_led_state(C4SID_MARKER)
    @property
    def track_led_state(self):
        return self.get_assignment_btn_led_state(C4SID_TRACK)
    @property
    def chan_strip_led_state(self):
        return self.get_assignment_btn_led_state(C4SID_CHANNEL_STRIP)
    @property
    def function_led_state(self):
        return self.get_assignment_btn_led_state(C4SID_FUNCTION)

    @property
    def shift_led_state(self):
        return self.get_modifier_btn_led_state(C4SID_SHIFT)
    @property
    def option_led_state(self):
        return self.get_modifier_btn_led_state(C4SID_OPTION)
    @property
    def control_led_state(self):
        return self.get_modifier_btn_led_state(C4SID_CONTROL)
    @property
    def alt_led_state(self):
        return self.get_modifier_btn_led_state(C4SID_ALT)

    @property
    def shift_pressed_state(self):
        return self.get_modifier_btn_pressed_state(C4SID_SHIFT)
    @property
    def only_shift_is_pressed(self):
        return self.modifier_button_bit_field() == self.modifier_group_multi_press_definitions["shift_only"]
    @property
    def option_pressed_state(self):
        return self.get_modifier_btn_pressed_state(C4SID_OPTION)
    @property
    def only_option_is_pressed(self):
        return self.modifier_button_bit_field() == self.modifier_group_multi_press_definitions["option_only"]
    @property
    def control_pressed_state(self):
        return self.get_modifier_btn_pressed_state(C4SID_CONTROL)
    @property
    def only_control_is_pressed(self):
        return self.modifier_button_bit_field() == self.modifier_group_multi_press_definitions["control_only"]
    @property
    def alt_pressed_state(self):
        return self.get_modifier_btn_pressed_state(C4SID_ALT)
    @property
    def only_alt_is_pressed(self):
        return self.modifier_button_bit_field() == self.modifier_group_multi_press_definitions["alt_only"]

    @property
    def bank_left_led_state(self):
        return self.get_parameter_btn_led_state(C4SID_BANK_LEFT)
    @property
    def bank_right_led_state(self):
        return self.get_parameter_btn_led_state(C4SID_BANK_RIGHT)    
    @property
    def single_left_led_state(self):
        return self.get_parameter_btn_led_state(C4SID_SINGLE_LEFT)
    @property
    def single_right_led_state(self):
        return self.get_parameter_btn_led_state(C4SID_SINGLE_RIGHT)

    @property
    def bank_left_pressed_state(self):
        return self.get_parameter_btn_pressed_state(C4SID_BANK_LEFT)
    @property
    def bank_right_pressed_state(self):
        return self.get_parameter_btn_pressed_state(C4SID_BANK_RIGHT)    
    @property
    def single_left_pressed_state(self):
        return self.get_parameter_btn_pressed_state(C4SID_SINGLE_LEFT)
    @property
    def single_right_pressed_state(self):
        return self.get_parameter_btn_pressed_state(C4SID_SINGLE_RIGHT)

    @property
    def track_left_led_state(self):
        return self.get_session_btn_led_state(C4SID_TRACK_LEFT)
    @property
    def track_right_led_state(self):
        return self.get_session_btn_led_state(C4SID_TRACK_RIGHT)    
    @property
    def slot_up_led_state(self):
        return self.get_session_btn_led_state(C4SID_SLOT_UP)
    @property
    def slot_down_led_state(self):
        return self.get_session_btn_led_state(C4SID_SLOT_DOWN)

    @property
    def track_left_pressed_state(self):
        return self.get_session_btn_pressed_state(C4SID_TRACK_LEFT)
    @property
    def track_right_pressed_state(self):
        return self.get_session_btn_pressed_state(C4SID_TRACK_RIGHT)    
    @property
    def slot_up_pressed_state(self):
        return self.get_session_btn_pressed_state(C4SID_SLOT_UP)
    @property
    def slot_down_pressed_state(self):
        return self.get_session_btn_pressed_state(C4SID_SLOT_DOWN)

    def handle_function_button_press(self, button_id):
        if button_id == C4SID_SPLIT:
            self._split_led_states()
        else:
            self._update_function_button_state(button_id)

    def handle_assignment_button_press(self, button_id):
        self._update_assignment_button_state(button_id)

    def handle_modifier_button_press(self, button_id):
        self._update_modifier_button_state(button_id)

    def handle_parameter_button_press(self, button_id):
        self._update_parameter_button_state(button_id)

    def handle_session_button_press(self, button_id):
        self._update_session_button_state(button_id)

    def get_function_btn_led_state(self, button_id):
        """These buttons have associated physical LEDs. Because this controller only counts function button presses, """ \
        """the LED value returned here latches and returns state is ON or OFF until the button is pressed again. """ \
        """This method does not take multiple LEDs (the Split button) into account."""
        return self._led_state(self.function_group_buttons[button_id], button_id)

    def get_assignment_btn_led_state(self, button_id):
        """These buttons have associated physical LEDs. Because this controller only counts assignment button presses, """ \
        """the LED value returned here latches like a radio button and returns state is ON or OFF until another button in the group is pressed. """ \
        """However, the Marker button behaves differently at the script level.  Because Marker means User mode and User mode could be connected to the Max """ \
        """Sequencer patch and the Sequencer patch takes over control of the entire C4, the special way to exit User mode is to Press & Hold the marker button """ \
        """then Press the Lock button.  The marker LED will turn OFF and the LED for the previous script mode will turn back ON."""
        return self._led_state(self.assignment_group_buttons[button_id], button_id)

    def get_modifier_btn_led_state(self, button_id):
        """These buttons don't have associated physical LEDs. Because this controller counts both modifier button presses and releases, """ \
        """the LED value returned here only returns state is ON while the button is actually pressed (unlike controlled buttons with physical LEDs that latch)"""
        return self._led_state(self.modifier_group_buttons[button_id], button_id)

    def get_modifier_btn_pressed_state(self, button_id):
        """releases count as presses, for even counts 0, 2, 4, etc. the button is released, otherwise the button is pressed"""
        return self._pressed_state(self.modifier_group_buttons[button_id])

    @staticmethod
    def _led_state(btn_ref, btn_id):
        btn_led_ref = btn_ref["led_id"]
        toggle = btn_ref["press_count"] % 2
        return btn_led_ref[btn_id]["led_value"][toggle]

    @staticmethod
    def _pressed_state(btn_ref):
        toggle = btn_ref["press_count"] % 2
        return 0 if not toggle else 127

    def get_parameter_btn_led_state(self, button_id):
        """These buttons do not have associated physical LEDs. Because this controller counts both parameter button presses and releases, """ \
        """the LED value returned here only returns state is ON while the button is actually pressed (unlike controlled buttons with physical LEDs that latch) """ 
        return self._led_state(self.parameter_group_buttons[button_id], button_id)

    def get_parameter_btn_pressed_state(self, button_id):
        """releases count as presses, for even counts 0, 2, 4, etc. the button is released, otherwise the button is pressed"""
        return self._pressed_state(self.parameter_group_buttons[button_id])

    def get_session_btn_led_state(self, button_id):
        """These buttons do not have associated physical LEDs. Because this controller only counts session button presses, """ \
        """the LED value returned here latches and returns state is ON until the button is actually pressed again"""
        return self._led_state(self.session_group_buttons[button_id], button_id)

    def get_session_btn_pressed_state(self, button_id):
        """releases count as presses, for even counts 0, 2, 4, etc. the button is released, otherwise the button is pressed"""
        return self._pressed_state(self.session_group_buttons[button_id])

    def modifier_button_bit_field(self):
        """Shift=2^0, Option=2^1, Control=2^2, Alt=2^3, no modifiers pressed = 0. """ \
        """Returns an int value 0 - 15 depending on which modifiers are currently pressed"""
        rtn = 0
        if self.alt_pressed_state > 0:
            rtn =+ 8
        if self.control_pressed_state > 0:
            rtn += 4
        if self.option_pressed_state > 0:
            rtn += 2
        if self.shift_pressed_state > 0:
            rtn += 1

        return rtn

    def assignment_button_led_bit_field(self):
        """Marker=2^0, Track=2^1, ChanStrip=2^2, Function=2^3, no assignment button leds ON = 0. """ \
        """Returns an int value 0 - 15 depending on which assignment button leds are currently ON (currently, one LED in this group is always exclusively ON, """ \
        """so this method only actually returns one of these four 2^x values corresponding to which assignment button led is currently ON), no 'press combos' allowed """
        # but theoretically, this script could leverage up to all 16 unique four bit values for up to 12 more "assignment modes"
        rtn = 0
        if self.function_led_state > 0:
            rtn = + 8
        if self.chan_strip_led_state > 0:
            rtn += 4
        if self.track_led_state > 0:
            rtn += 2
        if self.marker_led_state > 0:
            rtn += 1

        return rtn

    def split_button_led_bit_field(self):
        """led0=2^0, led1=2^1, led2=2^2, no Split LEDs lit = 0. Returns an int value 0 - 7 depending on which Split LEDs are currently lit. """ \
        """The current split button LED repeat cycle (0, 1, 2, 3) lit in turn means this method only (currently) returns values from the 'bit field' cycle """ \
        """(0, 1, 3, 7), half of the 8 possible three bit combinations, where (the bit field value) 3 specificaly means led0 and led1 are ON while led2 is OFF and """ \
        """(the bit field value) 7 means all three split LEDs are ON. """
        led0, led1, led2 = self.split_led_states
        rtn = 0
        if led0 > 0:
            rtn += 1
        if led1 > 0:
            rtn += 2
        if led2 > 0:
            rtn += 4
        return rtn

    def _flip_split_erase_led_state(self, value=C4SID_SPLIT_ERASE):
        self._update_function_button_state(value)

    def _update_function_button_state(self, btn_id):
        return self._update_button_state(self.function_group_buttons[btn_id])

    def _update_assignment_button_state(self, btn_id):
        """(script mode) assignment group button LED ON states are mutually exclusive, and one assignment LED is always ON. You can only turn OFF a given """ \
        """assignment LED by pressing a different assignment button (turning its LED ON instead). The exception to this 'rule' is User-Sequencer mode, when """ \
        """enabled and connected, which takes control of all midi feedback to C4 LEDs and LCDs. This controller only handles User-Sequencer mode events """ \
        """associated with entering or exiting User mode. If the sequencer is NOT connected, all you can do in User mode is exit. """
        if self.get_assignment_btn_led_state(btn_id) < 1:
            # new assignment mode is NOT already active (LED is OFF)
            last_mode_id = self.__current_assignment_led_on
            button_ref = self._update_button_state(self.assignment_group_buttons[btn_id])# new assignment mode is active (LED is now ON)
            self.__current_assignment_led_on = btn_id
            self.__last_assignment_led_on = last_mode_id
            for key in self.assignment_group_buttons.keys():
                btn = self.assignment_group_buttons[key]
                if not btn["led_id"] == btn_id:
                    state = btn["press_count"] % 2
                    if state > 0:
                        btn["press_count"] += 1 # any other assignment mode is now logically deactivated (LED is now OFF)
            return button_ref
        else: # this assignment mode is already active (LED is already ON)
            return self.assignment_group_buttons[btn_id]

    def _update_modifier_button_state(self, btn_id):
        return self._update_button_state(self.modifier_group_buttons[btn_id])

    def _update_parameter_button_state(self, btn_id):
        return self._update_button_state(self.parameter_group_buttons[btn_id])

    def _update_session_button_state(self, btn_id):
        return self._update_button_state(self.session_group_buttons[btn_id])

    @staticmethod
    def _update_button_state(btn_ref):
        btn_ref["press_count"] += 1
        return btn_ref

    def _split_led_states(self, value=C4SID_SPLIT):
        button_ref = self._update_function_button_state(value)
        btn_led_ref = button_ref["led_id"]

        self.__split_led_cycle_index = button_ref["press_count"] % len(self.__split_led_ids)
        # 4 states repeat == 1, 2, 3 leds ON, and "all leds OFF"
        if self.__split_led_cycle_index > 0:
            inner_offset = self.__split_led_cycle_index - 1
            btn_led_ref[inner_offset]["virtual_press_count"] += 1
        else:
            if btn_led_ref[C4SID_SPLIT]["virtual_press_count"] % 2 > 0:
                btn_led_ref[C4SID_SPLIT]["virtual_press_count"] += 1
            if btn_led_ref[C4SID_SPLIT + 1]["virtual_press_count"] % 2 > 0:
                btn_led_ref[C4SID_SPLIT + 1]["virtual_press_count"] += 1
            if btn_led_ref[C4SID_SPLIT + 2]["virtual_press_count"] % 2 > 0:
                btn_led_ref[C4SID_SPLIT + 2]["virtual_press_count"] += 1

        if self.nbr_split_leds_on == 3:
            # 3 SPLIT leds ON means turn OFF "LCD text scrolling" (displays don't update often enough for scrolling)
            if self.spot_erase_led_state > 0:
                # if the "spot erase" led is ON, turn it OFF by "virtually pressing" the button
                self._flip_split_erase_led_state()
        elif self.nbr_split_leds_on == 0:
            # 0 SPLIT leds ON means turn ON "LCD text scrolling" (scrolling text by default)
            if self.spot_erase_led_state == 0:
                # if the "spot erase" led is OFF, turn it ON by "virtually pressing" the button
                self._flip_split_erase_led_state()


class EncoderController(MackieC4Component, Component):
    """This is the main script "business logic" controller.  With helpers, it controls how all the buttons, encoders, LEDs, and LCDs on the """ \
    """Mackie C4 (and C4 Pro) controller (MCU-extension controller) behave when this script connects Live to the C4. "Mapped" encoders are controlled by Live """ \
    """when mapped and active, for example, encoder 32 in Track Channel Strip mode is mapped to 'Track Volume' in Live.  So turning the encoder on the C4 affects the """ \
    """track volume in Live, and mouse-dragging the Track volume in Live affects the LED ring around encoder 32.  However, the LCD text over encoder 32 is entirely """ \
    """generated and controlled by this script (in coordination with Live). In other words, 'midi mapping' (registering) a script's encoder in Live doesn't extend to """ \
    """the associated LCD text segment over the encoder, all LCD text is handled 'manually' by this script (in coordination with Live). """
    __module__ = __name__

    time_format =  Live.Song.TimeFormat.smpte_25
    nav_directions =  Live.Application.Application.View.NavDirection

    def __init__(self, main_script, encoders, device_provider):
        # MackieC4Component sits between MackieC4 and EncoderController because that's how the original Mackie MCU scripts are designed.
        # MackieC4Component means EncoderController doesn't need to use super-class-shared-method-name method calling semantics (like it would
        # if it directly inherited from MackieC4).  Functions in MackieC4Component all (but one) delegate to functions in MackieC4, which is the self._init__()
        # main_script input object here (which gets passed directly to MackieC4Component.__init__(self, main_script))
        #
        if main_script is None:
            raise ValueError("main_script is None?")
        MackieC4Component.__init__(self, main_script)
        Component.__init__(self, register_component=self.register_component, song=self.song())
        
        self.log_levels = main_script.script_log_levels
        self.current_log_level = main_script.current_script_log_level
        # some EncoderController methods have modal functionality depending on "from where" they are called
        # these modal functions have variable behavior based on "where" method "modal function" calls have come from.
        # For example, if self.xfade() is called from self.on_update_display_timer() it does different work,
        # than if it is called from self.handle_pressed_v_pot().
        self.mode_functions = {
            "handle_pressed_v_pot": self.handle_pressed_v_pot,
            "reassign_encoder_parameters": self.__reassign_encoder_parameters,
            "on_update_display_timer": self.on_update_display_timer
        }
        """defines the only normal class functions allowed to call modal class functions like self.xfade()"""

        self.__parameter_inc_dec_flag = False
        self.__parameter_inc_dec_args = None
        self.btn_ctlr = ButtonController(last_assignment_mode=C4M_FUNCTION, init_assignment_mode=C4M_CHANNEL_STRIP)
        self.btn_ctlr.handle_function_button_press(C4SID_SPLIT_ERASE) # LCD text scrolling ON by default
        # suspect the reason for 'own_encoders' too is because, at runtime, while this self.__init__() is running; the main_script input,
        # (and the caller), MackieC4, is still inside its own __init__ (and thus can't be referenced successfully yet?)
        # The encoders here though, both sets, are fully initialized and are successfully referenced (here inside __init__())
        self.__own_encoders = encoders
        self.__encoders = encoders

        for s in self.__own_encoders:
            s.set_encoder_controller(self)

        self.__ds = EncoderControllerDataStore(main_script, self)
        self.__ds.data.class_logging = self.current_log_level < logging.DEBUG
        self.__time_display = script_utils.TimeDisplay(smpt_format=self.time_format)
        self.__display_update_lag_upper_bounds = [0, 5, 10, 20]
        self.__display_update_lag_upper_bounds_index = 0
        self.__display_update_lag_counter = 0
        self.__view_is_changing = False
        self.add_special_parameter_listeners_pending = False

        self.selected_track = None
        """direct reference to Live's currently selected Track. song.view.selected_track"""
        self.__locked_device_track = None
        """if script is not locked to a device, this property references self.selected_track, otherwise this property references the Track containing the device """ \
        """to which the script is locked which may differ from Live's currently selected Track"""

        self.__ordered_plugin_parameters = []  # Live's DeviceParameters of __chosen_plugin (if exists)
        self.__device_provider = device_provider
        self.__chosen_plugin = None
        self.is_locked_to_device = False
        self._expand_chains = False
        self.__on_device_changed.subject = self.__device_provider
        self.__on_is_locked_to_device_changed.subject = self.__device_provider

        self.__display_parameters = []
        self.__display_parameters = [EncoderDisplaySegment(x) for x in range(NUM_ENCODERS)]


        self.encoder_name_display_state = [
            {
                "toggle": False,
                "last_toggle_time": 0.0,
                "scroll_pos": 0,
                "last_scroll_time": 0.0
            }
            for _ in range(NUM_ENCODERS)
        ]
        """the LCD text over each encoder is limited to 6 or 7 characters.  For Tracks and Devices with longer names, the 'full' name can scroll or toggle within the """ \
        """limited space over an encoder (rather than getting mangled by automated contraction adjustments).  These 'encoder_id' to 'name display state' dicts manage """ \
        """the associated scroll and or toggle details at runtime. """

        self.subordinate_track_is_selected = False
        """False when the master track is selected, True otherwise."""
        self.subordinate_selected_track_allows_audio = False
        """True if the selected track is subordinate and has audio output (master always has audio output). """ \
        """False if the selected track is subordinate and has no audio output (only midi output).  """ \
        """Meaninglessly False if the selected track is master (master is not subordinate).""" \

        self.last_send_messages = {
            LCD_ANGLED_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []},
            LCD_TOP_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []},
            LCD_MDL_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []},
            LCD_BTM_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}
        }
        self.__pending_device_change = False
        self.__chain_expansion_changed = False
        self.__selected_device_changed_flag = False
        self.returns_switch = 0

        self.update_assignment_mode_leds()
        self.update_system_switch_leds()

        self._last_undo_label = ""
        self._last_undo_label_time = 0

        self._last_redo_label = ""
        self._last_redo_label_time = 0

        self.clear_all_lcds()
        return

    def update_undo_info(self, clean):
        self._last_redo_label = clean
        self._last_redo_label_time = time.time()

    def update_redo_info(self, clean):
        self._last_undo_label = clean
        self._last_undo_label_time = time.time()

    def destroy(self):

        if self.main_script() is not None:
            self.send_goodbye_screen()
            self.clear_all_leds()
        MackieC4Component.destroy(self)

    def send_goodbye_screen(self):
        self.display_message_top_lcd('                     Ableton Live                      ', '                   Device is offline                   ')

    def clear_all_lcds(self):
        self.display_message_top_lcd(force=True)

    def clear_all_leds(self):
        for i in range(C4SID_SHIFT):
            self.send_midi((NOTE_ON_STATUS, i, LED_OFF_DATA))

        for j in encoder_range:
            self.send_midi((CC_STATUS, j + NUM_ENCODERS, LED_OFF_DATA))

    def display_message_top_lcd(self, top_line="", bottom_line="", force=False):
        so_many_spaces = "".join([" " for i in range(NUM_TEXT_BYTES_PER_SYSEX_MSG)])
        if len(top_line) < 1:
            top_line = so_many_spaces
        if len(bottom_line) < 1:
            bottom_line = so_many_spaces
        self.send_display_string(LCD_ANGLED_ADDRESS, top_line, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, so_many_spaces, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, so_many_spaces, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, so_many_spaces, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_ANGLED_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, so_many_spaces, LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, so_many_spaces, LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, so_many_spaces, LCD_BOTTOM_ROW_OFFSET, force=force)

    def display_message_all_lcd(self, top_line="", bottom_line="", force=False):
        so_many_spaces = "".join([" " for i in range(NUM_TEXT_BYTES_PER_SYSEX_MSG)])
        if len(top_line) < 1:
            top_line = so_many_spaces
        if len(bottom_line) < 1:
            bottom_line = so_many_spaces
        self.send_display_string(LCD_ANGLED_ADDRESS, top_line, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_ANGLED_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET, force=force)

    def request_rebuild_midi_map(self):
        MackieC4Component.request_rebuild_midi_map(self)

    def get_encoders(self):
        return self.__encoders

    @property
    def current_track_name(self):
        return 'None' if self.selected_track is None else 'Invalid' if not liveobj_valid(self.selected_track) else self.selected_track.name

    @property
    def expand_chains(self):
        return self._expand_chains

    def _set_expand_chains(self, expand=False):
        """only changes chain expansion behavior when you inc/dec tracks and devices using Session Group buttons on the C4 """ \
        """if BOTH Ctrl and Alt Modifier buttons are already pressed, otherwise chain expansion behavior doesn't change"""
        log_id = "EC._set_expand_chains: "
        allowed = self.btn_ctlr.is_expand_chains_modifier_press_combo
        self.main_script().log_message(logging.DEBUG, f"{log_id}{self.expand_chains} currently, input is {expand} and state update is {'' if allowed else 'NOT '}allowed")
        if allowed:
            self._expand_chains = expand
            self.main_script().log_message(logging.DEBUG, f"{log_id}now set to {self.expand_chains}")

    @property
    def chain_expansion_changed(self):
        return self.__chain_expansion_changed
    @chain_expansion_changed.setter
    def chain_expansion_changed(self, assigned_state):
        self.__chain_expansion_changed = assigned_state

    @property
    def selected_device_changed_flag(self):
        return self.__selected_device_changed_flag

    @selected_device_changed_flag.setter
    def selected_device_changed_flag(self, flag_is_flying):
        self.__selected_device_changed_flag = flag_is_flying

    @listens("device")
    def __on_device_changed(self):
        log_id = "EC.__on_device_changed: "
        trace_level = self.log_levels["TRACE"]
        d = self.__device_provider.provided_device
        self.__ds.next_selected_device = d
        if self.__chosen_plugin != d:
            self.__device_provider.clear_last_param_details()
            if liveobj_valid(d):
                track = self.song().view.selected_track
                if track != self.__locked_device_track:
                    msg = f"{log_id}listener popped, {d.name} is valid, but not local selected_track, pending device change flag set"
                    self.main_script().log_message(logging.DEBUG, msg)
                    self.__pending_device_change = True
                    self.__ds.next_selected_device = d
                    return

                msg = f"{log_id}listener popped, {d.name} is valid, and local selected_track, processing device change now"
                self.main_script().log_message(logging.DEBUG, msg)
                self.main_script().log_message(self.log_levels["TRACE"], f"{log_id} and {'' if self.expand_chains else 'NOT '} expanding chains")
                extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
                device_index = self.find_device_index_in_list(extended_device_list, d)
                self.__ds.device_added_deleted_or_changed(extended_device_list, d, device_index)
                self.main_script().log_message(trace_level, f"{log_id} local data updated, updating special param listeners")
                self.add_special_parameter_listeners(track, d)

                if self.__chosen_plugin is None:
                    last_name = "None"
                elif not liveobj_valid(self.__chosen_plugin):
                    last_name = "<device deleted>"
                else:
                    last_name = self.__chosen_plugin.name

                self.main_script().log_message(trace_level, f"{log_id}device changed, updating chosen plugin from {last_name} to {d.name}")
                self.__update_chosen_plugin_device(d)
                self.selected_device_changed_flag = True  #  track's "device list" listener callback will see this flag and flip it back to False
            # else:
            #     # can land here when folding a group track and new selected (group) track doesn't have any devices
            #     self.main_script().log_message(logging.DEBUG, f"{log_id}listener popped, but device not liveobj valid?")
        else:
            # can land here when a track's only device is deleted (because None == not liveobj_valid()) <-- but we need to handle on this "equal difference" event
            provided_name = "None" if d is None else "Invalid" if not liveobj_valid(d) else d.name
            chosen_name = "None" if self.__chosen_plugin is None else "Invalid" if not liveobj_valid(self.__chosen_plugin) else self.__chosen_plugin.name
            if d is None and not liveobj_valid(self.__chosen_plugin):
                # selected track did not change and selected device (the only device) was deleted
                self.main_script().log_message(logging.DEBUG, f"{log_id}device changed to {provided_name}, updating chosen plugin from {chosen_name}")
                self.main_script().log_message(trace_level, f"{log_id}clearing devices for track at song index {self.__ds.last_selected_track_index}")
                self.__ds.data.clear_track_devices(self.__ds.last_selected_track_index)
                self.__update_chosen_plugin_device(d)
            else:
                msg = f"{log_id}listener popped, but provided device {provided_name} is already self.__chosen_plugin {chosen_name}, pass"
                self.main_script().log_message(trace_level, msg)

    def on_selected_device_movement(self, device_obj):
        log_id = "EC.on_selected_device_movement: "
        nm = "Invalid" if not liveobj_valid(device_obj) else device_obj.name
        device_moved = True
        if liveobj_valid(device_obj) and device_obj == self.song().view.selected_track.view.selected_device:
            stored_active_device = self.__ds.data.get_device(self.__ds.last_selected_track_index, self.__ds.last_selected_device_index)
            new_device_list_order = self.main_script().get_device_list(self.selected_track.devices, self.expand_chains)
            new_device_index = self.find_device_index_in_list(new_device_list_order, device_obj)
            if stored_active_device is not None:
                if stored_active_device.device == device_obj:
                    # above should nearly always be true? (can't mouse-move an unselected device)
                    device_moved = self.__inner_device_movement(new_device_list_order, device_obj, new_device_index)
                else:
                    stored_name = "stored-last-Invalid" if not liveobj_valid(stored_active_device) else stored_active_device.name
                    self.main_script().log_message(logging.WARNING, f"{log_id}input selected device {nm} is NOT already stored device {stored_name}?")
                    device_moved = False
            else:
                # a device move was undone, the stored device at the (previously) moved-to index has already been deleted and reinserted (by Live)
                # back at the moved-from index
                self.main_script().log_message(logging.INFO, f"{log_id}conditions for undo/redo of device {nm} movement detected, attempting to recover")
                stored_device_map = self.__ds.data.get_track_device_map(self.__ds.last_selected_track_index)
                full_rebuild = True
                if stored_device_map is not None:
                    if  len(stored_device_map.keys()) > 0:
                        full_rebuild = False

                if full_rebuild: # stored map is None or has no keys
                    lgth = len(new_device_list_order)
                    self.main_script().log_message(logging.INFO, f"{log_id}recovering device {nm} by fully restoring device map")
                    for i in range(lgth):
                        self.__ds.update_device_counts_on_addition(i, new_device_list_order, i, i + 1)
                else: # partial rebuild? stored_device_map has at least one key
                    lgth = len(new_device_list_order)
                    if stored_device_map is not None: # redundant, but None type doesn't have function keys()
                        existing_keys_lgth = len(stored_device_map.keys())
                        assert lgth >= existing_keys_lgth
                        assert existing_keys_lgth <= new_device_index < lgth  # new index is 'right of' all existing indexes
                        self.main_script().log_message(logging.INFO, f"{log_id}VISIBILITY!!! recovering device {nm} by partially restoring device map")
                        short_range = lgth - existing_keys_lgth
                        for i in range(short_range):
                            insert_index = i + existing_keys_lgth
                            if insert_index < lgth:
                                self.__ds.update_device_counts_on_addition(i, new_device_list_order, insert_index, insert_index + 1)
                            else:
                                log_msg = f"{log_id}cannot recover device {nm} as expected, index {insert_index} too large for device list length {lgth}?"
                                self.main_script().log_message(logging.INFO, log_msg)
                stored_active_device = self.__ds.data.get_device(self.__ds.last_selected_track_index, new_device_index)
                log_msg = f"{log_id}recovery attempt completed "
                if stored_active_device is not None and stored_active_device.device == device_obj:
                    self.main_script().log_message(logging.INFO, log_msg + "successfully")
                else:
                    self.main_script().log_message(logging.INFO, log_msg + "unsuccessfully")
        else:
            # landed here moving a Group track containing two "rack tracks" (a rack of DrumGroup devices and a rack of InstrumentGroup devices)
            self.main_script().log_message(logging.DEBUG, f"{log_id}conditions for movement of device {nm} not detected, maybe the track moved?")
            device_moved = False
        if device_moved and self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
            # the track's visible device bank order has changed, update the LCD device bank display order to match (if the device bank is already showing)
            self.__reassign_encoder_parameters()

    def __inner_device_movement(self, new_device_list_order, device_obj, new_device_index, device_name="None"):
        log_id = "EC.__inner_device_movement: "
        device_moved = True
        if new_device_index > -1:
            if self.__ds.last_selected_device_index != new_device_index:
                self.__ds.last_selected_device = device_obj
                self.__ds.track_device_moved(new_device_list_order, device_obj, new_device_index)
            else:
                self.main_script().log_message(logging.ERROR, f"{log_id}new index of selected device {device_name} is not different from stored index as expected?")
                device_moved = False
        else:
            self.main_script().log_message(logging.ERROR, f"{log_id}index of selected device {device_name} not located in selected track device list as expected?")
            device_moved = False
        return device_moved


    def add_special_parameter_listeners(self, selected_track, selected_device):
        log_id = "EC.add_special_parameter_listeners: "
        if liveobj_valid(selected_track):
            # note: these listeners are in addition to the script's normal midi mapping listeners
            # they are associated with the C4.selected_device_change_state() callback method and
            # they specifically support the Parameter Single left and right button behavior (increment/decrement value of last changed device parameter)
            # existing (C4.selected_device_change_state() callback) listeners are automatically removed before adding new ones
            self.main_script().do_add_one_devices_listeners(selected_device, track_name=selected_track.name)
        else:
            track = self.__device_provider.device_track
            if liveobj_valid(track):
                self.main_script().do_add_one_devices_listeners(selected_device, track_name=track.name)
            else:
                self.main_script().log_message(logging.INFO, f"{log_id}selected device {selected_device.name} is valid, but not selected_track, finding track")
                track, index = self.find_devices_track(selected_device)
                if liveobj_valid(track):
                    self.selected_track = track
                    self.main_script().do_add_one_devices_listeners(selected_device, track_name=track.name)
                else:
                    msg = f"{log_id}selected device is {selected_device.name} but can't locate valid track reference. "
                    self.main_script().log_message(logging.ERROR, msg + "no device parameter listeners added, predicting something else will soon derail anyway")

    def find_devices_track(self, device):
        """checks if input device is in device chain of song().view.selected_track. returns the Track (selected_track) and song index where found or None"""
        log_id = "EC.find_devices_track: "
        selected_track = self.song().view.selected_track
        trace_level = self.log_levels["TRACE"]
        if liveobj_valid(selected_track):
            tracks = self.song().visible_tracks + self.song().return_tracks
            selected_index = 0

            if selected_track == self.song().master_track:
                selected_index = len(tracks) # "one index past" the last valid regular + return tracks index
                self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
                devices = self.get_device_list(selected_track.devices, expand_chains=self.expand_chains)
                found = device in devices
                msg = f"{log_id}self.song().view.selected_track is master (i=={selected_index}) and {device.name} device was "
                if found:
                    self.main_script().log_message(trace_level, f"{msg}found")
                    return selected_track, selected_index
                else:
                    self.main_script().log_message(logging.DEBUG, f"{msg}NOT found, None returned")
                    return None, None
            else:
                if selected_track in tracks:
                    for i, track in enumerate(tracks):
                        if track == selected_track:
                            selected_index = i
                            break
                    self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
                    devices  = self.get_device_list(selected_track.devices, expand_chains=self.expand_chains)
                    found = device in devices
                    msg = f"{log_id}self.song().view.selected_track is {selected_track.name} (i=={selected_index}) and {device.name} device was "
                    if found:
                        self.main_script().log_message(trace_level, f"{msg}found")
                        return selected_track, selected_index
                    else:
                        self.main_script().log_message(logging.WARNING, f"{msg}NOT found, None returned")
                        return None, None
                else:
                    self.main_script().log_message(logging.ERROR, f"{log_id}self.song().view.selected_track is not master and not in visible or return tracks?")
                    return None, None
        else:
            self.main_script().log_message(logging.ERROR, f"{log_id}self.song().view.selected_track is not a valid Live object?")
            return selected_track


    def __update_chosen_plugin_device(self, device):
        log_id = "EC.__update_chosen_plugin_device: "
        trace_level = self.log_levels["TRACE"]
        self.__chosen_plugin = device  # in cases like a new midi track selected; device will == None here
        if not liveobj_valid(self.selected_track):
            if liveobj_valid(device):
                self.main_script().log_message(logging.INFO, f"{log_id} device is {device.name} but current selected_track is not valid, finding track")
                # if self.__chosen_plugin is not valid going in here, the found track coming out will never be valid either, something will soon bug out
                track, index = self.find_devices_track(self.__chosen_plugin)
                if liveobj_valid(track):
                    self.selected_track = track
                    msg = f"{log_id}device is {device.name} and selected track is {self.selected_track.name}, rebuilding midi map after special device change"
                    self.main_script().log_message(logging.INFO, msg)
                else:
                    self.main_script().log_message(logging.ERROR, f"{log_id}selected_track is still not valid, __reassign_encoder_parameters() will soon bug out")
            else:
                self.main_script().log_message(logging.INFO, f"{log_id} device is not valid and current selected_track is not valid, not rebuilding midi map")
                return
        else:  # liveobj_valid(self.selected_track)
            if liveobj_valid(device):
                msg = f"{log_id}device is {device.name} and selected track is {self.selected_track.name}, rebuilding midi map after normal device change"
                self.main_script().log_message(trace_level, msg)
            else:
                msg = f"{log_id}selected track is {self.selected_track.name} but device is not valid, rebuilding midi map for NoneType device"
                self.main_script().log_message(trace_level, msg)
        self.__reorder_parameters()
        self.__reassign_encoder_parameters()
        self.request_rebuild_midi_map()
        # nm = "None" if self.__chosen_plugin is None else self.__chosen_plugin.name
        # self.main_script().log_message(logging.DEBUG, f"{log_id}chosen_plugin changed to {nm}")

    @listens("is_locked_to_device")
    def __on_is_locked_to_device_changed(self):
        is_locked = self.__device_provider.surface_is_locked
        # dv = self.__chosen_plugin.name if self.__chosen_plugin is not None else "None"
        # if is_locked:
        #     self.main_script().log_message(logging.DEBUG, f"EC.__on_is_locked_to_device_changed: listener popped, now locked to device {dv}")
        # else:
        #     self.main_script().log_message(logging.DEBUG, f"EC.__on_is_locked_to_device_changed: listener popped, now unlocking from device {dv}")
        self.__locked_device_track = self.selected_track  # can't be locking (or unlocking) a device on an invalid "selected" track
        self.is_locked_to_device = is_locked

    def build_setup_database(self):
        log_id = "EC.build_setup_database"
        # self.main_script().log_message(logging.DEBUG, "EC.build_setup_database: C4.building setup db")
        song = self.song()
        self.__ds.build_setup_database(song)

        # self.main_script().log_message(logging.DEBUG, "EC.build_setup_database: C4.t_count after setup <{0}>".format(self.__eah.t_count))
        # self.main_script().log_message(logging.DEBUG, "EC.build_setup_database: C4.main_script().track_count after setup <{0}>".format(self.main_script().track_count))
        selected_track = song.view.selected_track
        selected_index, selected_callback_type, callback_type_index, nbr_song_tracks = self.find_track_index(selected_track)
        self.__ds.last_selected_track_index = selected_index
        self.track_changed(selected_index, selected_callback_type, callback_type_index)

        self.selected_track = selected_track
        self.__ds.selected_track = self.selected_track
        self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
        devices_on_selected_trk = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
            if len(devices_on_selected_trk) == 0:
                self.__update_chosen_plugin_device(None)
            else:
                d = devices_on_selected_trk[0]
                if not d == song.view.selected_track.view.selected_device:
                    self.song().view.select_device(d)
                else:
                    # make sure to initialize a "last selected device"
                    self.__on_device_changed()
                    if not self.main_script().has_param_value_listener(d.parameters[0]):
                        self.add_special_parameter_listeners(selected_track, d)

        return

    def master_track_index(self):
        return self.__ds.master_track_index


    def on_param_state_change(self, param, callback_track_type_index, device_index, parameter_index, callback_track_type):
        # reordered method inputs
        self.__ds.on_param_state_change(callback_track_type, callback_track_type_index, device_index, parameter_index, param)

    def track_moved(self, callback_track_type, next_song_index):
        self.__ds.track_moved(callback_track_type, next_song_index, self.selected_track)

    def track_changed(self, track_index, selected_track_callback_type, callback_type_index):
        log_id = "EC.track_changed: "
        self.selected_track = self.song().view.selected_track
        trace_level = self.log_levels["TRACE"]

        if self.btn_ctlr.is_expand_chains_modifier_press_combo:
            # chain expansion behavior changes when both Control and Alt are pressed
            self._set_expand_chains(not self.expand_chains)
            self.chain_expansion_changed = True
            self.__ds.data.chain_expansion_changed()
        else:
            self.chain_expansion_changed = False

        if liveobj_valid(self.selected_track):
            self.main_script().log_message(trace_level, f"{log_id}track_index input is {track_index}, selected_track is {self.selected_track.name}")
        else:
            self.main_script().log_message(trace_level, f"{log_id}track_index input is {track_index}, but selected_track is not liveobj valid")

        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track

        next_active_track_ref = self.__ds.data.get_track(track_index)
        self.main_script().log_message(trace_level, f"{log_id}track_index input is {track_index}, stored active_track is {next_active_track_ref.track_name}")
        if liveobj_valid(next_active_track_ref.track) and self.selected_track != next_active_track_ref.track:
            self.main_script().log_message(trace_level, f"{log_id}live obj at index differs from stored ref at same index, track moved")
            # don't worry about chain expansion changes here, "selected track" already changed, it's moved now
            self.track_moved(next_active_track_ref.type, track_index)
        else:
            if not liveobj_valid(next_active_track_ref.track) and liveobj_valid(self.selected_track):
                msg = f"{log_id}VISIBILTY!! stored active_track {next_active_track_ref.track_name} is not valid and selected track is valid {self.selected_track.name} "
                self.main_script().log_message(logging.WARNING, msg + "updating invalid stored reference and re-entering")
                self.__ds.data.remove_track(0 if track_index < 1 else track_index - 1) # pass the "index before" the track to be removed
                self.__ds.data.add_track(self.selected_track, selected_track_callback_type, track_index)
                self.track_changed(track_index, selected_track_callback_type, callback_type_index) # stored track is valid now so we can process track_changed()
                return
            else:
                if next_active_track_ref.device_list_is_dirty:
                    t = next_active_track_ref.track
                    if liveobj_valid(t):
                        changed_device_list = self.get_device_list(t.devices, self.expand_chains)
                        msg = f"{log_id}chain expansion behavior has changed since stored active_track {next_active_track_ref.track_name} was stored with "
                        msg += f"{next_active_track_ref.device_count} devices, "
                        self.main_script().log_message(trace_level, msg)
                        self.main_script().log_message(trace_level, f"rebuilding stored device map with {len(changed_device_list)} devices")
                        atd = self.__ds.data.get_active_track_details_at_song_index(track_index)
                        new_device_count = atd.rebuild_device_map(changed_device_list)
                        if not len(changed_device_list) == new_device_count:
                            compare = f"Live devices {len(changed_device_list)} vs stored devices {new_device_count}"
                            msg = f"{log_id}device count mismatch after rebuilding device map for track {next_active_track_ref.track_name}: {compare}"
                            self.main_script().log_message(logging.DEBUG, msg)
                        # else:
                        #     assert len(changed_device_list) == new_device_count
                        # this should be a moot assignment, next_active_track_ref is already atd.active_track,
                        # but the local next_active_track_ref instance might not already be updated with the new device list references and atd.active_track is updated
                        next_active_track_ref = atd.active_track

                selected_device_index = next_active_track_ref.selected_device_index # next_active_track_ref.device_count
                msg = f"{log_id}stored active_track {next_active_track_ref.track_name} has {next_active_track_ref.device_count} devices and "
                self.main_script().log_message(trace_level, msg + f"selected_device_index {selected_device_index}")
                if self.main_script().processing_track_inc_dec_event:
                    self.main_script().processing_track_inc_dec_event = False
                self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
                extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
                nbr_devices = len(extended_device_list)
                next_device = None
                if selected_device_index is not None and self.__pending_device_change:
                    next_device = self.__ds.next_selected_device
                    last_selected_device_on_track = self.__ds.data.get_device(self.__ds.last_selected_track_index, self.__ds.last_selected_device_index)
                    if last_selected_device_on_track == next_device:
                        selected_device_index = self.__ds.last_selected_device_index
                        self.__pending_device_change = False
                        self.main_script().log_message(logging.ERROR, f"{log_id}pending device change to {next_device.name} cancelled, ")
                    elif nbr_devices > next_active_track_ref.device_count:
                        selected_device_index = nbr_devices - 1
                        next_active_track_ref.device_count = nbr_devices
                        msg = f"{log_id}pending device change, device added, selected index is last device in chain {selected_device_index}"
                    else:
                        msg = f"{log_id}pending device change, device changed because track changed and selected index is {selected_device_index} here too"
                    self.main_script().log_message(trace_level, msg)
                else: # selected_device_index is None or this track change is not a self.__pending_device_change case
                    log_idx = "None" if selected_device_index is None else selected_device_index
                    if nbr_devices > 0 and (selected_device_index is None or not (0 <= selected_device_index < nbr_devices)):
                        msg = f"{log_id}selected device index is {log_idx} but there are {nbr_devices} devices, setting selected device index to {nbr_devices - 1}"
                        self.main_script().log_message(trace_level, msg)
                        next_active_track_ref.selected_device_index = nbr_devices - 1
                        self.__ds.data.set_track(next_active_track_ref)
                        selected_device_index = next_active_track_ref.selected_device_index

                self._track_changed_device_change(track_index, nbr_devices, selected_device_index, next_device, extended_device_list)

        return

    def _track_changed_device_change(self, track_index, nbr_devices, selected_device_index, next_device, track_device_list):
        log_id = "EC._track_changed_device_change: "
        trace_level = self.log_levels["TRACE"]
        if nbr_devices == 0:
            self.main_script().log_message(trace_level, f"{log_id}no devices found on track {self.selected_track.name}")
            self.__ds.track_changed(track_index)
            self.__ds.update_device_counter(track_index, 0)
        else:
            if selected_device_index is not None and selected_device_index > -1:
                if nbr_devices > selected_device_index:
                    if next_device is None:
                        next_device = track_device_list[selected_device_index]
                    if liveobj_valid(next_device):
                        self.main_script().log_message(trace_level, f"{log_id}{next_device.name} found at index {selected_device_index}")
                    self.__ds.track_changed(track_index)
                    self.__ds.update_device_counter(track_index, nbr_devices)
                    self.main_script().log_message(trace_level, f"{log_id}called __eah.update_device_counter({track_index}, {nbr_devices})")
                # else something didn't get updated correctly at startup and/or when devices deleted?
                elif nbr_devices > 0:  # punt if we can
                    next_device = track_device_list[nbr_devices - 1]
                    msg = f"{log_id}Because there are only {nbr_devices} devices in device list for track {self.selected_track.name}, index "
                    if liveobj_valid(next_device):
                        msg += f"{selected_device_index} returned by ECDS is OOB, using fallback selected device {next_device.name} found at index {nbr_devices - 1} "
                        self.main_script().log_message(trace_level, msg + "instead.")
                    else:
                        nbr_devices = 0
                        msg += f"{selected_device_index} returned by ECDS is OOB, and "
                        self.main_script().log_message(logging.ERROR, msg + f"invalid device found at index 0 of track's device list. assumption issue?")
                    self.__ds.track_changed(track_index)
                    self.__ds.update_device_counter(track_index, nbr_devices)
                    self.main_script().log_message(trace_level, f"{log_id}called __eah.update_device_counter(track_index={track_index}, nbr_of_devices={nbr_devices})")
                else:
                    msg = f"{log_id}len(extended_device_list) {nbr_devices} < {selected_device_index} selected_device_index, no update"
                    self.main_script().log_message(logging.DEBUG, msg)
            # else:
            # selected_device_index is None or selected_device_index < 0

        if not self.is_locked_to_device:
            self.main_script().log_message(trace_level, f"{log_id}script data update for new Live selected_track {self.selected_track.name} finished. ")
            msg_prefix = f"{log_id}Now updating script data for new Live selected_device, "
            if liveobj_valid(next_device):
                self.__locked_device_track = self.selected_track
                if not self.is_processing_track_device_state_change():
                    if not self.selected_track.view.selected_device == next_device:
                        self.main_script().log_message(logging.DEBUG, f"{msg_prefix}selecting device {next_device.name} and updating chosen plugin device")
                        # this device selection could cause cascading listener callbacks in Live
                        # so don't update self.__chosen_plugin here now, defer to the ensuing device change listener callback
                        self.song().view.select_device(next_device)
                    else:
                        self.main_script().log_message(trace_level, f"{msg_prefix}but song selected device is already {next_device.name}")
                        if self.__chosen_plugin == next_device:
                            self.main_script().log_message(trace_level, f"{log_id}and script chosen plugin is already {next_device.name}")
                            self.__update_chosen_plugin_device(next_device)
                        else:
                            if self.__pending_device_change:
                                msg_prefix = f"{log_id}and a local device change is pending, "
                                nm = "None" if self.__chosen_plugin is None else "Invalid" if not liveobj_valid(self.__chosen_plugin) else self.__chosen_plugin.name
                                self.main_script().log_message(trace_level, f"{msg_prefix}processing local device change with index {selected_device_index}")
                                self.__ds.device_added_deleted_or_changed(track_device_list, next_device, selected_device_index)
                                self.main_script().log_message(trace_level, f"{log_id} {nm} to {next_device.name}")
                                stored_track_ref = self.__ds.data.get_track(track_index)
                                if stored_track_ref.selected_device_index != selected_device_index:
                                    msg = f"{log_id}updating track ref selected device index {stored_track_ref.selected_device_index} to {selected_device_index}"
                                    self.main_script().log_message(trace_level, msg)
                                    stored_track_ref.selected_device_index = selected_device_index
                                    if stored_track_ref.device_count != nbr_devices:
                                        self.__ds.update_device_counter(stored_track_ref.index, nbr_devices)
                                        msg = f"{log_id}number of devices on stored track reference not already updated?"
                                        self.main_script().log_message(trace_level, msg)
                                if self.__ds.last_selected_device_index != selected_device_index:
                                    msg = f"{log_id}updating last selected device index {self.__ds.last_selected_device_index} to {selected_device_index}"
                                    self.main_script().log_message(trace_level, msg)
                                    self.__ds.last_selected_device_index = selected_device_index
                                self.main_script().log_message(trace_level, f"{msg_prefix}updating script chosen plugin from {nm} to {next_device.name}")
                                self.__update_chosen_plugin_device(next_device)
                                if liveobj_valid(next_device):
                                    self.main_script().log_message(trace_level, f"and updating special parameter listeners for {next_device.name}")
                                    self.add_special_parameter_listeners(self.selected_track, next_device)
                                self.__pending_device_change = False
                            nsd = self.__ds.next_selected_device
                            name = "None" if nsd is None else "Invalid" if not liveobj_valid(nsd) else nsd.name
                            if nsd == next_device:
                                self.main_script().log_message(logging.ERROR, f"{log_id}pending device change to {name} processed successfully")
                                self.__ds.next_selected_device = None
                            else:
                                msg = f"{log_id}pending device change to {name} ignored in favor of change to {next_device.name}?"
                                self.main_script().log_message(logging.ERROR, msg)
                else:
                    self.main_script().log_message(logging.DEBUG, f"{msg_prefix}but device state is already actively changing")
            else:
                if self.__pending_device_change:
                    msg_prefix += "and a local device change is pending, "
                self.main_script().log_message(logging.DEBUG, f"{msg_prefix}but no valid device found, self.__chosen_plugin == None")
                self.__update_chosen_plugin_device(next_device)  # device == None
                if self.__pending_device_change and self.__ds.next_selected_device != next_device:
                    name = self.__ds.next_selected_device.name
                    self.main_script().log_message(logging.DEBUG, f"{log_id}pending device change to {name} ignored?, self.__eah.next_selected_device == None")
                    self.__ds.next_selected_device = None

                self.__pending_device_change = False

    # a Group track expanded and the selected track index is changing (Group expanded 'left of' selected track of this track type)
    def tracks_added(self, track_index, tracks_of_type, callback_track_type_of_selected_index):
        log_id = "EC.tracks_added: "
        if self.btn_ctlr.is_expand_chains_modifier_press_combo:
            # chain expansion behavior changes when both Control and Alt are pressed
            self._set_expand_chains(not self.expand_chains)
            self.chain_expansion_changed = True
            self.__ds.data.chain_expansion_changed()

        self.__ds.tracks_added(track_index, tracks_of_type, callback_track_type_of_selected_index)
        # (using same update selected track code as from self.track_deleted() instead of same update logic in track_added())
        self.__update_selected_track(track_index)
        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[callback_track_type_of_selected_index]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[callback_track_type_of_selected_index])

    # a Group track expanded and the selected track index is NOT changing (Group expanded 'right of' selected track of this type or selected track is return or main type
    # return tracks can not be Grouped
    def unselected_tracks_added(self, found_changed_track_callback_type, callback_type_track_count):
        log_id = "EC.unselected_tracks_added: "
        if self.btn_ctlr.is_expand_chains_modifier_press_combo:
            # chain expansion behavior changes when both Control and Alt are pressed
            self._set_expand_chains(not self.expand_chains)
            self.chain_expansion_changed = True
            self.__ds.data.chain_expansion_changed()

        self.__ds.unselected_tracks_added(found_changed_track_callback_type, callback_type_track_count)
        self.__update_selected_track(self.__ds.last_selected_track_index)
        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[found_changed_track_callback_type]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[found_changed_track_callback_type])

    def track_added(self, track_index, found_changed_track_callback_type):
        log_id = "EC.track_added: "
        self.selected_track = self.song().view.selected_track
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
        self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
        extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
        self.__ds.track_added(track_index, self.selected_track, extended_device_list, found_changed_track_callback_type)

        self.refresh_state()
        device = None
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
            selected_device_index = self.__ds.last_selected_device_index
            if selected_device_index is not None and selected_device_index > -1:
                if len(extended_device_list) > selected_device_index:
                    selected_device = extended_device_list[selected_device_index]
                    device = selected_device
                elif len(extended_device_list) > 0:
                    selected_device = extended_device_list[0]
                    self.__ds.last_selected_device_index = 0
                    device = selected_device

            if  liveobj_valid(device):
                self.song().view.select_device(device)
            else:
                self.__update_chosen_plugin_device(device)  # device == None

        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[found_changed_track_callback_type]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[found_changed_track_callback_type])
        return

    # when stored tracks get deleted (disappear from song().visible_tracks) their stored device lists get deleted too, expanded or collapsed chains.
    # when Group Tracks collapse, the stored collapsing group-track "loses" all stored group-expanded tracks and their devices no longer "visible" regardless of expanded
    # chains status, but changing the script's chain expansion behavior when collapsing a Group still globally impacts all the stored tracks and devices in the set.
    # The script will process the next Track change or Group expand/collapse event using the updated chain expansion setting, unless CTRL+ALT "flips the flag" again.
    # (In fewer words, Group Track collapse is modeled in script storage by following a single code execution path, no logical branching on the expanded chains flag status)
    def tracks_deleted(self, track_index, tracks_of_type, track_type=-1):
        log_id = "EC.tracks_deleted: "
        if self.btn_ctlr.is_expand_chains_modifier_press_combo:
            # chain expansion behavior changes when both Control and Alt are pressed
            self._set_expand_chains(not self.expand_chains)

        self.main_script().log_message(logging.DEBUG, f"{log_id}deleting tracks of type {track_type} from index: {track_index}")
        self.__ds.tracks_deleted(track_index, tracks_of_type, track_type)
        self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}updating selected track info at index: {track_index}")
        self.__update_selected_track(track_index)
        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[track_type]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[track_type])

    def unselected_tracks_deleted(self, found_changed_track_callback_type, callback_type_track_count):
        log_id = "EC.unselected_tracks_deleted: "
        if self.btn_ctlr.is_expand_chains_modifier_press_combo:
            # chain expansion behavior changes when both Control and Alt are pressed
            self._set_expand_chains(not self.expand_chains)

        self.__ds.unselected_tracks_deleted(found_changed_track_callback_type, callback_type_track_count)
        self.__update_selected_track(self.__ds.last_selected_track_index)
        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[found_changed_track_callback_type]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[found_changed_track_callback_type])

    def unselected_tracks_changed(self, found_changed_track_callback_type, callback_type_track_count):
        log_id = "EC.unselected_tracks_changed: "
        if self.btn_ctlr.is_expand_chains_modifier_press_combo:
            # chain expansion behavior changes when tracks change and both Control and Alt are pressed
            self._set_expand_chains(not self.expand_chains)
        self.__ds.unselected_tracks_changed(found_changed_track_callback_type, callback_type_track_count)
        self.__update_selected_track(self.__ds.last_selected_track_index)
        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[found_changed_track_callback_type]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[found_changed_track_callback_type])

    def track_deleted(self, next_selected_track_index, callback_track_type_of_selected_index, callback_type_index):
        log_id = "EC.track_deleted: "
        self.main_script().log_message(logging.DEBUG, f"{log_id}stored ref object at song index {next_selected_track_index} will be deleted")
        if callback_track_type_of_selected_index == 1 and callback_type_index == 0:
            self.__ds.data.remove_track_by_callback_type(track_callback_types[callback_track_type_of_selected_index], callback_type_index)
        else:
            self.__ds.track_deleted(0 if next_selected_track_index < 1 else next_selected_track_index - 1)

        next_ref = self.__ds.data.get_active_track_details_at_song_index(next_selected_track_index)
        msg = f"{log_id}shifted stored ref at song index {next_selected_track_index} is now {next_ref.active_track.track_name}"
        self.main_script().log_message(self.log_levels["TRACE"], msg)
        self.__update_selected_track(next_selected_track_index)
        if self.__ds.data.class_logging:
            self.main_script().log_message(logging.DEBUG, f"{log_id}dump of stored {track_callback_types[callback_track_type_of_selected_index]} tracks:")
        self.__ds.data.log_dump_with_devices_by_callback_track_type_key(track_callback_types[callback_track_type_of_selected_index])

    def __update_selected_track(self, track_index):
        log_id = "EC.__update_selected_track: "
        track_obj = self.song().view.selected_track
        if not liveobj_valid(track_obj):
            self.main_script().log_message(logging.DEBUG, f"{log_id}song().view.selected_track is not valid, neither is index {track_index}")
        self.selected_track = track_obj
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
            track_ref = self.__ds.data.get_active_track_details_at_song_index(track_index)
            msg = f"{log_id}processing track change, song selected track {self.selected_track.name} "
            if track_ref is not None:
                if liveobj_changed(self.selected_track, track_ref.active_track.track):
                    self.main_script().log_message(logging.DEBUG, msg + f"changed versus stored track {track_ref.active_track.track_name}")
                    self.__ds.track_changed(track_index)
                    insert = "is now"
                else:
                    self.main_script().log_message(logging.DEBUG, msg + f"already matches stored track {track_ref.active_track.track_name}")
                    insert = "is unchanged"
            else:
                msg += f"is not stored at song index {track_index}, None atd_ref returned, no stored 'last selected' updates based on None"
                self.main_script().log_message(logging.DEBUG, msg)
                insert = "remains"

            log_list = [self.__ds.last_selected_track_index, self.__ds.last_selected_track_callback_type, self.__ds.last_selected_track_callback_type_index]
            msg = f"{log_id}song index {track_index} {insert} last selected [song index, cb_type, type_index] {log_list}"
            self.main_script().log_message(self.log_levels["TRACE"], msg)

        self.refresh_state()  # class local refresh, resets "modifier is pressed" states to "released"

        self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
        extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
        last_selected_device_index = self.__ds.last_selected_device_index # at track_index
        # self.main_script().log_message(logging.DEBUG, f"{log_id}selected tk device index after: {0}".format(selected_device_index))
        # self.main_script().log_message(logging.DEBUG, "f"{log_id}nbr of devices on selected track after: {0}".format(len(extended_device_list)))
        device_obj = None
        if not self.is_locked_to_device:

            if last_selected_device_index is not None and last_selected_device_index > -1:
                nbr_devices = len(extended_device_list)
                if last_selected_device_index < nbr_devices:
                    selected_device = extended_device_list[last_selected_device_index]
                    device_obj = selected_device
                elif nbr_devices > 0:
                    selected_device = extended_device_list[nbr_devices - 1]
                    self.__ds.last_selected_device_index = nbr_devices - 1
                    device_obj = selected_device

            if liveobj_valid(device_obj):
                self.__locked_device_track = self.selected_track
                if not (self.song().view.selected_track.view.selected_device == device_obj or self.is_processing_track_device_state_change()):
                    self.main_script().log_message(logging.DEBUG, f"{log_id}selecting device {device_obj.name} at new device index {last_selected_device_index}")
                    self.song().view.select_device(device_obj)
                # else:
                #     msg = f"{log_id}device {device_obj.name} at index {last_selected_device_index} is "
                #     if self.song().view.selected_track.view.selected_device == device_obj:
                #         self.main_script().log_message(logging.DEBUG, f"{msg}already selected in song, not selecting again")
                #     else:
                #         self.main_script().log_message(logging.DEBUG, f"{msg}not selected but script is already processing a track device state change")
            else:
                self.__update_chosen_plugin_device(device_obj)  # device == None

        return

    def device_list_changed(self, track, track_type_index, track_type):
        log_id = "EC.device_list_changed: "
        if track == self.selected_track and len(track.devices) == len(self.selected_track.devices):
            # only processing drag&drop movement of the selected device
            type_key = track_callback_types[track_type]
            self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
            extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
            track_dtls_ref = self.__ds.data.get_active_track_details_ref_by_type_key(type_key, track_type_index)
            track_ref = track_dtls_ref.active_track
            stored_selected_device_index = track_ref.selected_device_index
            stored_device_count = track_dtls_ref.device_count
            if stored_device_count == track_ref.device_count:
                if stored_device_count == len(extended_device_list):
                    selected_device_obj = self.selected_track.view.selected_device
                    last_device_ref = track_dtls_ref.selected_device
                    last_device_ref_obj = None if last_device_ref is None else last_device_ref.device
                    if liveobj_valid(last_device_ref_obj) and selected_device_obj == last_device_ref_obj:
                        # once through both collections in one pass to skip rekeying lists that already match
                        if not track_dtls_ref.has_matching_deviceobj_list(extended_device_list):
                            # rekeying the data store is an exponentially growing operation
                            self.__ds.data.rekey_device_list_by_track_callback_type(type_key, track_type_index, extended_device_list, selected_device_obj)
                            track_ref = self.__ds.data.get_track_by_type_key(type_key, track_type_index)
                            dtls = f"changed from {stored_selected_device_index} to {track_ref.selected_device_index}"
                            self.main_script().log_message(logging.DEBUG, f"{log_id}device move event processed successfully selected device index {dtls}")
                        else:
                            self.main_script().log_message(logging.DEBUG, f"{log_id}pass, no device move detected, next device list order already mapped")
                    else:
                        self.main_script().log_message(logging.DEBUG, f"{log_id}pass, no device move detected, selected device is changing")
                else:
                    dtls = ""
                    if self.main_script().current_script_log_level < logging.DEBUG:
                        dtls = f"stored device list length {stored_device_count} not equal to changed device list length {len(extended_device_list)}"
                    self.main_script().log_message(logging.DEBUG, f"{log_id}pass, device list size is changing " + dtls)
            else:
                dtls = f"number of track details ref stored devices {stored_device_count} not equal to number of active track ref stored devices {track_ref.device_count}"
                self.main_script().log_message(logging.WARNING, f"{log_id}pass, logic issue?" + dtls)
                d_map = self.__ds.data.get_track_device_map_by_callback_type(type_key, track_type_index)
                dtls = f"{log_id}{type_key} track ref at {type_key} index {track_type_index} has stored devices {[x.device_name for x in d_map.values()]}"
                self.main_script().log_message(logging.DEBUG, dtls)
        else:
            self.main_script().log_message(logging.WARNING, f"{log_id}pass, assumption issue? Live objects don't agree? not a drag&drop device movement event")


    def device_added_deleted_or_changed(self, track, track_index, track_type, track_type_index):
        log_id = "EC.device_added_deleted_or_changed: "
        updated_idx = -1
        # extended_device_list is the device list with enumerated/flattened rack devices
        # if a device is added to any unselected track, this extended device list is not populated here with the new device on the freshly selected track
        # devices cannot be updated or deleted from an unselected track, they can only be added to an unselected track. (by drag&drop, for example)
        self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
        extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)

        # Use a dictionary to map type to listener_type
        listener_types = {0: "normal", 1: "return", 2: "master"}.get(track_type, "None")

        if liveobj_valid(track):
            # log_msg = f"{log_id}processing device change-state of Track listener type <{listener_type}> on track <{track.name}> at index {track_index}"
            # self.main_script().log_message(logging.DEBUG, log_msg)
            if liveobj_changed(self.selected_track, track):
                sel_trk_nm = self.selected_track.name if liveobj_valid(self.selected_track) else "None"
                log_msg = f"{log_id}because VISIBILTY!! input track <{track.name}> is not self.selected_track, "
                log_msg += f"updating self.selected_track from <{sel_trk_nm}> to <{track.name}> and calling self.track_changed({track_index}) "
                self.main_script().log_message(logging.DEBUG, log_msg + f"to update self.__eah before calling self.__eah.device_added_deleted_or_changed() below")
                self.selected_track = track
                self.track_changed(track_index, track_type, track_type_index)  # <--- ???
                # update the extended (flattened) device list for the changed selected Track
                # extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)

            if liveobj_valid(self.selected_track):
                selected_device = self.selected_track.view.selected_device
                if liveobj_valid(selected_device):
                    log_msg = f"{log_id}track {self.selected_track.name} and device {selected_device.name} are valid"
                    self.main_script().log_message(logging.DEBUG, log_msg)
                    selected_device_index = self.find_device_index_in_list(extended_device_list, selected_device)
                    updated_idx = self.__ds.device_added_deleted_or_changed(extended_device_list, selected_device, selected_device_index)

            device = None
            if not self.is_locked_to_device:
                if updated_idx == -1:
                    device = None
                    # might happen if track with no devices deleted, and the next selected track also has no devices?
                    self.__ds.last_selected_device_index = None
                    # self.main_script().log_message(logging.DEBUG, "{0}__chosen_plugin is now None because no ECDS updated index".format(log_id))
                elif len(extended_device_list) > updated_idx:
                    device = extended_device_list[updated_idx]
                    self.__ds.last_selected_device_index = updated_idx
                    # log_msg = f"{log_id}__chosen_plugin is now {self.__chosen_plugin.name} because updated index is <{updated_idx}>"
                    # self.main_script().log_message(logging.DEBUG, log_msg)
                elif len(extended_device_list) > 0:  # evaluation never reaches here if updated_idx == 0
                    device = extended_device_list[0]
                    self.__ds.last_selected_device_index = 0
                    # self.main_script().log_message(logging.DEBUG, f"{log_id}ONLY device __chosen_plugin is now {self.__chosen_plugin.name} because don't know")
                else:
                    # might happen if track with no devices deleted, and the next selected track also has no devices?
                    self.__ds.last_selected_device_index = None
                    # self.main_script().log_message(logging.DEBUG, f"{log_id}__chosen_plugin is now None because else-fell-through")

                if liveobj_valid(device):
                    self.__locked_device_track = self.selected_track
                    self.song().view.select_device(device) # this should notify device listeners via "device provider"
                else:
                    self.__update_chosen_plugin_device(device) # device == None

        new_device_count_track = len(extended_device_list)
        # self.main_script().log_message(logging.DEBUG, "{0}device count AFTER update <{1}>".format(log_id, new_device_count_track))

        if new_device_count_track > 0:
            for i, device in enumerate(extended_device_list):
                log_msg = f"{log_id}device at extended device list index <{i}> is"
                if liveobj_valid(device):
                    # self.main_script().log_message(logging.DEBUG, f"{log_msg} <{device.name}>"
                    pass
                else:
                    log_msg = f"{log_msg} not liveobj_valid"
                    self.main_script().log_message(logging.ERROR, log_msg)
        # else:
            # self.main_script().log_message(logging.WARNING, f"{log_id}new_device_count_track was NOT > 0, NOT enumerating devices for log")

    @staticmethod
    def find_device_index_in_list(device_list, device):
        current_selected_indexes = (x for x in range(len(device_list)) if device_list[x] == device)
        # if the device list contains more than one selected instance of the selected device, collect all selected indexes
        # and pass the first index collected
        device_index = next(current_selected_indexes, -1)
        if device_index < 0 < len(device_list):
            device_index = len(device_list) - 1
        return device_index

    def toggle_devices(self, cc_no, cc_value):
        """any clockwise turn cc_value activates device represented by cc_no, counterclockwise turns deactivate device."""
        # Track - Channel Strip mode is the only mode that shows banks of devices to toggle on and off like this
        # Track - Devices mode shows the "chosen device" parameters, the first one of which directly toggles the "chosen device" on and off
        log_id = "EC.toggle_devices: "
        if self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
            # some 'device bank' of the track where the device-to-which-the-script-is-locked is located is displayed
            locked_devices_track_is_selected = self.is_locked_to_device and self.__locked_device_track == self.song().view.selected_track
            allow_toggle = True if not self.is_locked_to_device or locked_devices_track_is_selected else False
            if allow_toggle:
                atd = self.__ds.data.get_active_track_details_at_song_index(self.__ds.last_selected_track_index)
                bank_of_selected_device_is_the_device_bank_on_display = atd.device_bank_index_of_selected_device == atd.active_track.track_device_bank_view_index
                # if script is locked to a device, script should probably only allow toggling the locked device ON/OFF, but that whole bank is on display
                # locked or not, only process the devices in the bank on display
                if bank_of_selected_device_is_the_device_bank_on_display or not self.is_locked_to_device:
                    rtn_str = tcs_mode_util.toggle_devices(atd, cc_no, cc_value)
                    if len(rtn_str) > 0:
                        self.main_script().log_message(logging.WARNING, rtn_str)


    def assignment_mode(self):
        return self.btn_ctlr.current_active_script_mode

    def last_assignment_mode(self):
        return self.btn_ctlr.last_active_script_mode

    # This method is never called from USER mode
    #
    # C4SID_SPLIT behavior only affects the "display update" refresh RATE (feedback to lcds, leds, and led rings) when the song IS NOT playing,
    #    display refresh RATE is always full speed when song IS playing (full speed is 10 full display updates per second)
    # C4SID_SPLIT controls the amount of intentional lag applied between "on display update timer" calls and actual C4 display updates which "slows down" the
    #    apparent LCD text scrolling rate (for "long" display strings)
    #    all split button leds OFF means no lag applied (send display update midi messages every time "on display update timer" is called, 1 for 1)
    #      when 0 C4SID_SPLIT leds are ON - ONLY do timer based display updates (ignore callback events, the next timer based update is soon enough)
    #    all split button leds ON means infinite lag amount (never send display update midi messages, ignore "on display update timer" calls)
    #      when 3 C4SID_SPLIT leds are ON - ONLY do callback based display updates (ignore C4SID_SPLIT_ERASE led state - set text scrolling disabled)
    #
    # C4SID_LOCK is mapped to Live's (Python) LOM API "Lock control surface to device" behavior.
    #
    # C4SID_SPLIT_ERASE (semi-dependent on SPLIT state) enables or disables the "LCD screen text scrolling" (when LESS THAN 3 C4SID_SPLIT leds are ON)
    #   dependency is if all 3 C4SID_SPLIT leds are ON - set "LCD screen text scrolling", C4SID_SPLIT_ERASE led state to off, disabled)
    def handle_system_switch_ids(self, switch_id):

        self.btn_ctlr.handle_function_button_press(switch_id)

        if switch_id == C4SID_SPLIT:
            self.__display_update_lag_upper_bounds_index = self.btn_ctlr.split_led_cycle_index
        elif switch_id == C4SID_LOCK:
            if self.btn_ctlr.lock_led_state > 0:
                d = self.__device_provider.provided_device
                if liveobj_valid(d):
                    self.lock_to_device(d)
                else: # turn the LOCK LED OFF again because no valid device to lock to
                    self.btn_ctlr.handle_function_button_press(switch_id)
            else:
                self.unlock_from_device()
            if self.btn_ctlr.nbr_split_leds_on > 0:
                # ONLY do    timer based display updates when zero C4SID_SPLIT leds are ON
                # ONLY do callback based display updates when all  C4SID_SPLIT leds are ON
                # (do both display update styles when 1 or 2 Split leds are on)
                self.one_display_update()
        elif switch_id == C4SID_SPLIT_ERASE:
            pass # self.__spot_erase_state = self.btn_ctlr.split_erase_led_state
        else:
            self.main_script().log_message(logging.ERROR, f"EC.handle_system_switch_ids: unknown system switch id {switch_id}, no change in generated feedback")

        self.update_system_switch_leds()

    def update_system_switch_leds(self):
        if self.btn_ctlr.current_active_script_mode != C4M_USER:
            out_value_00, out_value_01, out_value_02 = self.btn_ctlr.split_led_states
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT, out_value_00))
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT + 1, out_value_01))
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT + 2, out_value_02))

            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, self.btn_ctlr.lock_led_state))
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT_ERASE, self.btn_ctlr.spot_erase_led_state))

    def handle_assignment_switch_ids(self, switch_id, leaving_user_mode=False):
        """the 4 Assignment buttons on the C4, which control script mode switching"""
        self.btn_ctlr.handle_assignment_button_press(switch_id)
        self.update_system_switch_leds()
        self.update_assignment_mode_leds()
        self.__reassign_encoder_parameters()
        self.request_rebuild_midi_map()
        if self.btn_ctlr.nbr_split_leds_on > 0:  # when no split leds are on, only do timer based display updates
            # need to wipe USER mode LCD screen displays when we leave USER mode, but not too soon, wait 20 ms
            self.one_delayed_display_update(.020)

    def handle_bank_switch_ids(self, switch_id):
        """ Parameter Group Buttons: Bank Left, Bank Right, Single Left, Single Right are only mapped to behavior in the two 'track modes', channel-strip and devices """
        # no wrap around: stop moving left at track 0, stop moving right at master track
        log_id = "EC.handle_bank_switch_ids: "
        self.btn_ctlr.handle_parameter_button_press(switch_id)
        update_self = False
        if switch_id == C4SID_BANK_LEFT:
            bank_left_index = 6
            if self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
                update_self = self.handle_track_device_bank_view_update(bank_left_index)
            elif self.btn_ctlr.current_active_script_mode == C4M_PLUGINS:
                update_self = self.handle_selected_device_parameter_bank_view_update(bank_left_index)
        elif switch_id == C4SID_BANK_RIGHT:
            bank_right_index = 7
            if self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
                update_self = self.handle_track_device_bank_view_update(bank_right_index)
            elif self.btn_ctlr.current_active_script_mode == C4M_PLUGINS:
                update_self = self.handle_selected_device_parameter_bank_view_update(bank_right_index)
        elif self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP or self.btn_ctlr.current_active_script_mode == C4M_PLUGINS:
            update_self = self.handle_selected_device_parameter_inc_dec(switch_id)

        if update_self:
            self.__reassign_encoder_parameters()
            self.request_rebuild_midi_map()
            if self.btn_ctlr.nbr_split_leds_on > 0:  # when no split leds are on, only do timer based display updates
                self.one_display_update()

    def handle_slot_nav_switch_ids(self, switch_id):
        """ "slot navigation" (arrow up 🔼/down 🔽) switches between Devices in all modes except User """
        log_id = "EC.handle_slot_nav_switch_ids: "
        if self.btn_ctlr.current_active_script_mode != C4M_USER:  # button_id_to_assignment_mode[C4SID_MARKER]:
            self.btn_ctlr.handle_session_button_press(switch_id)
            trk_device_current_index = self.__ds.last_selected_device_index if self.__ds.last_selected_device_index is not None else 0
            max_trk_device_index = self.__ds.selected_track_nbr_stored_devices - 1 if self.__ds.selected_track_nbr_stored_devices > 1 else 0
            update_self = False
            trk_device_adjusted_index = 0
            if switch_id == C4SID_SLOT_DOWN:
                if trk_device_current_index > 0:
                    trk_device_adjusted_index = trk_device_current_index - 1
                    update_self = True
            elif switch_id == C4SID_SLOT_UP:
                if trk_device_current_index < max_trk_device_index:
                    trk_device_adjusted_index = trk_device_current_index + 1
                    update_self = True

            if not self.is_locked_to_device and update_self:
                song_device = self.song().view.selected_track.view.selected_device
                stored_current_device_ref = self.__ds.data.get_device(self.__ds.last_selected_track_index, self.__ds.last_selected_device_index)
                self.__ds.last_selected_device_index = trk_device_adjusted_index
                # if the stored selected device remains the device we think it is, get the next device reference to select in Live from local storage (if exists)...
                # else get the next device reference to select in Live from Live using self.get_device_list()
                msg_pfx = f"{log_id} getting next device to select from "
                valid_stored_ref_match = liveobj_valid(stored_current_device_ref) and song_device == stored_current_device_ref.device
                if valid_stored_ref_match:
                    self.main_script().log_message(self.log_levels["TRACE"], msg_pfx + f"local storage at index {trk_device_adjusted_index}")
                    stored_next_device_ref = self.__ds.data.get_device(self.__ds.last_selected_track_index, self.__ds.last_selected_device_index)
                    if stored_next_device_ref is not None:
                        current_selected_device = stored_next_device_ref.device
                        if not liveobj_valid(current_selected_device):
                            self.__ds.last_selected_device_index = None
                    else: # else condition should only be necessary here where update_self == True if stored track device data is stale,
                          # so recovery (from stale stored data) might not be possible
                        if valid_stored_ref_match:
                            current_selected_device = stored_current_device_ref.device
                        else:
                            active_track_details = self.__ds.data.get_active_track_details_at_song_index(self.__ds.last_selected_track_index)
                            if active_track_details.device_count > 0:
                                stored_next_device_ref = active_track_details.devices[0]
                                current_selected_device = stored_next_device_ref.device
                                if liveobj_valid(current_selected_device):
                                    self.__ds.last_selected_device_index = 0
                                else:
                                    self.__ds.last_selected_device_index = None
                            else:
                                current_selected_device = None
                                self.__ds.last_selected_device_index = None
                else:
                    self.main_script().log_message(self.log_levels["TRACE"], msg_pfx + f"Live at index {trk_device_adjusted_index}")
                    self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
                    extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
                    if len(extended_device_list) > trk_device_adjusted_index:
                        current_selected_device = extended_device_list[trk_device_adjusted_index]
                    # else conditions should only be necessary here where update_self == True if stored track and device index data is stale
                    elif len(extended_device_list) > 0:
                        current_selected_device = extended_device_list[0]
                        self.__ds.last_selected_device_index = 0
                    else:
                        current_selected_device = None
                        self.__ds.last_selected_device_index = None

                if liveobj_valid(current_selected_device) and liveobj_changed(current_selected_device, song_device):
                    self.song().view.select_device(current_selected_device)
                else:
                    self.__update_chosen_plugin_device(current_selected_device) # current_selected_device == None

    def handle_modifier_switch_ids(self, switch_id, value):
        log_id = "EC.handle_modifier_switch_ids: "
        self.btn_ctlr.handle_modifier_button_press(switch_id)
        pressed = self.btn_ctlr.get_modifier_btn_pressed_state(switch_id)
        assert pressed == value # 0 or 127 'velocity data value'
        if switch_id == C4SID_SHIFT:
            self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}SHIFT is {'' if pressed else 'NOT '}pressed")
        elif switch_id == C4SID_OPTION:
            self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}OPTION is {'' if pressed else 'NOT '}pressed")
        elif switch_id == C4SID_CONTROL:
            self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}CONTROL is {'' if pressed else 'NOT '}pressed")
        elif switch_id == C4SID_ALT:
            self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}ALT is {'' if pressed else 'NOT '}pressed")


    def _show_assignment_mode_change_message(self):
        new_mode = self.btn_ctlr.current_active_script_mode
        old_mode = self.btn_ctlr.last_active_script_mode
        new_name = new_mode
        old_name = old_mode
        if new_name == 0:
            new_name = "USER SEQUENCER"
            if old_mode == 1:
                old_name = "DEVICE CHAIN"
            elif old_mode == 2:
                old_name = "CHANNEL STRIP"
            else:# 3:
                old_name = "SONG FUNCTIONS"
        if new_name == 1:
            new_name = "DEVICE CHAIN"
            if old_mode == 2:
                old_name = "CHANNEL STRIP"
            elif old_mode == 3:
                old_name = "SONG FUNCTIONS"
            else:# 0
                old_name = "USER SEQUENCER"
        elif new_name == 2:
            new_name = "CHANNEL STRIP"
            if old_mode == 3:
                old_name = "SONG FUNCTIONS"
            elif old_mode == 0:
                old_name = "USER SEQUENCER"
            else:# 1
                old_name = "DEVICE CHAIN"
        elif new_name == 3:
            new_name = "SONG FUNCTIONS"
            if old_mode == 0:
                old_name = "USER SEQUENCER"
            elif old_mode == 1:
                old_name = "DEVICE CHAIN"
            else:# 2
                old_name = "CHANNEL STRIP"
        self.main_script().show_message(f"mode change from {old_name} to {new_name}")

    def update_assignment_mode_leds(self):
        """
          turn off button LED of the button associated with the old assignment mode
          turn  on button LED of the button associated with the current/new assignment mode
        """
        delay_assignment_led_update = False

        if self.btn_ctlr.current_active_script_mode == C4M_USER:
            # going INTO USER mode these feedback messages pass through the Max patch before it starts processing messages
            # self.main_script().log_message(logging.DEBUG, "EC.update_assignment_mode_leds: entering USER mode")
            for i in range(C4SID_MARKER, C4SID_FUNCTION + 1) :
                self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_OFF))

        elif self.btn_ctlr.last_active_script_mode == C4M_USER:
            # leaving USER mode, messages from here would be processed by the Max patch
            # which would generate the feedback messages going directly to the C4 (before it receives the "button 22" signal sent below)
            # blindly telling the Max patch to toggle the assignment LED states from here would rarely leave the LEDs
            # accurately depicting the script's new current "assignment mode"
            delay_assignment_led_update = True
            # self.main_script().log_message(logging.DEBUG, "EC.update_assignment_mode_leds: leaving USER mode")
            # self.main_script().show_message(logging.DEBUG, "mode change from {} to {}".format(old_name, new_name))
        else:
            # log_msg = f"EC.update_assignment_mode_leds: changing non USER mode {old_name} ({old_mode}) to {new_name} ({new_mode})"
            # self.main_script().log_message(logging.DEBUG, log_msg)
            # not in USER mode these feedback messages pass through the Max patch
            current_mode_id = assignment_mode_to_button_id[self.btn_ctlr.current_active_script_mode]
            for i in assignment_mode_switch_ids:
                if i == current_mode_id:
                    self.main_script().log_message(logging.DEBUG, f"EC.update_assignment_mode_leds: led id {i} ON")
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_ON))
                else:
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_OFF))

        if delay_assignment_led_update:
            # self.main_script().log_message(logging.DEBUG, "EC.update_assignment_mode_leds: updating assignment LEDs after leaving USER mode")
            current_mode_id = assignment_mode_to_button_id[self.btn_ctlr.current_active_script_mode]
            done = False
            for i in range(C4SID_SPLIT, C4SID_FUNCTION + 1):
                if i < C4SID_MARKER and not done:
                    self.update_system_switch_leds()
                    done = True
                if i == current_mode_id:
                    self.main_script().log_message(logging.DEBUG, f"EC.update_assignment_mode_leds: led id {i} ON")
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_ON))
                else:
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_OFF))

        self._show_assignment_mode_change_message()

    def handle_vpot_rotation(self, vpot_index, cc_value):
        """For any encoder that is not midi mapped to some control in Live, and we want to map the CC messages it sends some other function of Live. """ \
        """For any encoder that is midi mapped to some control in Live, the CC messages are handled by the mapped control and should be ignored here """

        if self.btn_ctlr.current_active_script_mode == C4M_FUNCTION:
            feedback_address = encoder_feedback_cc_ids[vpot_index]
            if feedback_address == C4SID_VPOT_CC_ADDRESS_12:
                self.main_script().handle_jog_wheel_rotation(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_14:  # (display segment over encoder 13 is occupied)
                self.main_script().set_loop_length(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_15:
                self.main_script().set_loop_start(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_16:
                self.main_script().zoom_or_scroll(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_19:
                self.main_script().scrub_clip(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_20:
                self.main_script().scroll_clip(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_21:
                self.main_script().zoom_clip(cc_value)
            elif feedback_address == C4SID_VPOT_CC_ADDRESS_22:
                self.main_script().tempo_change(cc_value)
            # else: address of unused encoder in C4M_FUNCTION mode
        elif self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
            if vpot_index in row_01_encoders:
                self.toggle_devices(vpot_index, cc_value)
            # else: address of midi mapped or unused encoder in C4M_CHANNEL_STRIP mode
        if self.btn_ctlr.nbr_split_leds_on > 0:  # when no split leds are on, only do timer based display updates
            self.one_display_update()

    def unsolo_all_functionality(self, mode_name, vpot_index):
        mode_function = self.mode_functions.get(mode_name)
        if mode_function:
            if mode_name == "handle_pressed_v_pot":
                script_utils.unsolo_all(self.song().tracks)
            # elif mode_name == "reassign_encoder_parameters":
            #     encoders_to_display_text = {vpot_index: ('all', 'unsolo')}
            #     return encoders_to_display_text
            elif mode_name == "on_update_display_timer":
                if script_utils.any_soloed_track(self.song().tracks):
                    self.__encoders[vpot_index].show_full_enlighted_poti()
                else:
                    self.__encoders[vpot_index].unlight_vpot_leds()
        else:
            raise ValueError(f"Invalid mode name: {mode_name}")

    def beat_pointer(self, mode_name, vpot_index):
        """ show beat position pointer or song position pointer at encoder 12 AND encoder 13 position in second row """
        upper_string2 = ''
        lower_string2 = ''
        mode_function = self.mode_functions.get(mode_name)
        if mode_function:
            if mode_name == "handle_pressed_v_pot":
                self.__time_display.toggle_mode()
            elif mode_name == "on_update_display_timer":
                if self.__time_display.show_beat_time:
                    time_string = str(self.song().get_current_beats_song_time()) + ' '
                    upper_string2 += 'Bar:Bt:Sb:Tik '
                    lower_string2 += time_string
                else:
                    time_string = str(self.song().get_current_smpte_song_time(self.__time_display.smpt_format)) + ' '
                    upper_string2 += 'Hrs:Mn:Sc:Fra '
                    lower_string2 += time_string

                # vpot ring light
                display_mode_cc_first = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_WRAP][0]
                display_mode_cc_last = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_WRAP][1]

                scaler = make_interpolater(0, self.song().last_event_time, display_mode_cc_first, display_mode_cc_last)
                play_head = int(self.song().current_song_time)
                led_ring_val = int(scaler(play_head))

                spp_vpot = self.__encoders[vpot_index]
                spp_vpot.update_led_ring(led_ring_val)
        else:
            raise ValueError(f"Invalid mode name: {mode_name}")
        return upper_string2, lower_string2

    def loop_length(self, mode_name, vpot_index):
        upper_string2 = ''
        lower_string2 = ''
        mode_function = self.mode_functions.get(mode_name)
        if mode_function:
            if mode_name == "on_update_display_timer":
                get_loop_length = str(self.song().loop_length / 4)
                upper_string2 += 'LoopLength'
                lower_string2 += adjust_string(get_loop_length, 6) + ' '

                # vpot ring light
                display_mode_cc_first = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_SPREAD][0]
                display_mode_cc_last = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_SPREAD][1]

                scaler = make_interpolater(1, self.song().last_event_time, display_mode_cc_first, display_mode_cc_last)
                loop_length = int(self.song().loop_length)
                led_ring_val = int(scaler(loop_length))

                spp_vpot = self.__encoders[vpot_index + 1]  # because offset due to SPP being 2 slots wide
                spp_vpot.update_led_ring(led_ring_val)
        else:
            raise ValueError(f"Invalid mode name: {mode_name}")
        return upper_string2, lower_string2

    def xfade(self, mode_name, vpot_index, u_alt_text=None, l_alt_text=None):
        # handles all Crossfade functionality for pressed_vpot, reassign and on_update_display_timer
        upper_string4 = ''
        lower_string4 = ''
        mode_function = self.mode_functions.get(mode_name)
        if mode_function:
            if mode_name == "handle_pressed_v_pot":
                if self.selected_track.has_audio_output:
                    if self.subordinate_track_is_selected:
                        state = self.selected_track.mixer_device.crossfade_assign
                        value_to_send = None
                        if state == 0:
                            value_to_send = 'Mixer.Crossfade.A'
                        elif state == 1:
                            value_to_send = 'Mixer.Crossfade.Off'
                        elif state == 2:
                            value_to_send = 'Mixer.Crossfade.B'
                        script_utils.crossfade_toggle_value(self.selected_track, value_to_send)  # vpot push for Crossfade assign A/B/off on Audio or Return tracks
                    else:
                        param = self.__encoders[vpot_index].v_pot_parameter()
                        param.value = param.default_value  # button press == jump to default value for Crossfader on Master track
                    if self.btn_ctlr.nbr_split_leds_on > 0:  # when no split leds are on, only do timer based display updates
                        self.one_display_update(force=True)

            elif mode_name == "reassign_encoder_parameters":
                vpot_display_text = EncoderDisplaySegment(vpot_index)
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                if self.selected_track.has_audio_output:
                    if self.subordinate_track_is_selected != 1:
                        vpot_display_text.set_text(self.selected_track.mixer_device.crossfader,'X-Fade')  # Crossfader on Master track
                        vpot_param = (self.selected_track.mixer_device.crossfader, VPOT_DISPLAY_BOOST_CUT)

                xfade_vpot = self.__encoders[vpot_index]
                xfade_vpot.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

            elif mode_name == "on_update_display_timer":
                if liveobj_valid(self.selected_track):
                    if self.selected_track.has_audio_output:
                        if self.subordinate_track_is_selected:
                            value_to_display = None
                            try:
                                state = self.selected_track.mixer_device.crossfade_assign
                            except RuntimeError:  # Main track has no crossfader assignment! (when no tracks have A or B assigned, like a default Live session)
                                state = 1

                            spp_vpot = self.__encoders[vpot_index]
                            if state == 0:
                                value_to_display = 'XFadeA'
                                spp_vpot.update_led_ring(0x11)
                            elif state == 1:
                                value_to_display = ' Off  '
                                spp_vpot.unlight_vpot_leds()
                            elif state == 2:
                                value_to_display = 'XFadeB'
                                spp_vpot.update_led_ring(0x1B)
                            upper_string4 += 'X-Fade' + ' '
                            lower_string4 += str(value_to_display) + ' '

                        else:
                            upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])
                            lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                    else:
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])
                        lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                else:
                    upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])
                    lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])

        else:
            raise ValueError(f"Invalid mode name: {mode_name}")
        return upper_string4, lower_string4

    def handle_track_device_bank_view_update(self, control_index):
        log_id = "EC.handle_track_device_bank_view_update: "
        current_device_bank_index = self.__ds.last_selected_track_device_bank_view_index
        # max_device_bank_index = self.__ds.selected_device_bank_count - 1
        max_device_bank_index = self.__ds.selected_track_nbr_required_device_banks
        self.main_script().log_message(logging.DEBUG, f"{log_id} stored bank view index {current_device_bank_index} stored nbr banks required {max_device_bank_index}")
        max_device_bank_index -= 1  # index value
        bank_left_index = 6
        bank_right_index = 7
        update_self = False
        if control_index == bank_left_index:
            if current_device_bank_index > 0:
                current_device_bank_index -= 1
                update_self = True
            else:
                self.main_script().log_message(logging.DEBUG, f"{log_id} can't move bank view Left, already displaying bank 0")
        elif control_index == bank_right_index:
            if current_device_bank_index < max_device_bank_index:
                current_device_bank_index += 1
                update_self = True
            else:
                self.main_script().log_message(logging.DEBUG, f"{log_id} can't move bank view Right, already displaying max bank {max_device_bank_index + 1}")

        if update_self:
            self.main_script().log_message(logging.DEBUG, f"{log_id} moving bank view to new index {current_device_bank_index}")
            self.__ds.last_selected_track_device_bank_view_index = current_device_bank_index
        return update_self

    def handle_selected_device_parameter_bank_view_update(self, control_index):
        log_id = "EC.handle_selected_device_parameter_bank_view_update: "
        current_parameter_bank_track = self.__ds.last_selected_device_parameter_bank_view_index
        bank_left_index = 6
        bank_right_index = 7
        update_self = False
        current_track_device_parameter_bank_nbr_changed = False
        if control_index == bank_left_index:
            if current_parameter_bank_track > 0:
                current_parameter_bank_track -= 1
                # self.main_script().log_message(logging.DEBUG, f"{log_id}self.t_d_p_bank_current[self.t_current]: {self.__eah.last_selected_device_index})
                update_self = True
                current_track_device_parameter_bank_nbr_changed = True
        elif control_index == bank_right_index:
            current_track_device_preset_bank = current_parameter_bank_track
            # self.main_script().log_message(logging.DEBUG, f"{log_id}current_track_device_preset_bank: {0}".format(current_track_device_preset_bank))
            track_device_preset_bank_count = self.__ds.max_last_selected_track_device_parameter_bank_nbr
            # self.main_script().log_message(logging.DEBUG, f"{log_id}track_device_preset_bank_count: {0}".format(track_device_preset_bank_count))
            if current_track_device_preset_bank < track_device_preset_bank_count - 1:
                current_parameter_bank_track += 1
                update_self = True
                current_track_device_parameter_bank_nbr_changed = True
        if update_self and current_track_device_parameter_bank_nbr_changed:
            self.__ds.last_selected_device_parameter_bank_view_index = current_parameter_bank_track
            # msg = f"{log_id}device parameter-bank in view {current_parameter_bank_track} after pressed-vpot event handling, "
            # if device_ref.parameter_bank_index_of_selected_parameter == current_parameter_bank_track:
            #     self.main_script().log_message(logging.DEBUG, msg + "contains selected parameter")
            # else:
            #     # execution lands here whenever a device's "selected parameter" (normally, the last parameter that changed)
            #     # is not one of the 24 parameters in the "parameter bank" currently mapped to the 24 associated C4 encoders
            #     # in this self.btn_ctlr.current_active_script_mode == C4M_PLUGINS state. (Track - Devices mode)
            #     idx = device_ref.parameter_bank_index_of_selected_parameter
            #     self.main_script().log_message(logging.DEBUG, msg + f"doesn't match device_ref value {idx}")
        return update_self

    def handle_selected_device_parameter_inc_dec(self, switch_id):
        log_id = "EC.handle_selected_device_parameter_inc_dec: "
        update_self = True
        if liveobj_valid(self.__chosen_plugin):
            last_param_name = self.__device_provider.get_last_param_value_change_name()
            if liveobj_valid(self.__chosen_plugin.parameters):
                self.main_script().log_message(logging.DEBUG, f"{log_id}looking for original param name <{last_param_name}> in device <{self.__chosen_plugin.name}>")
                cp = v3_util.get_parameter_by_name(last_param_name, self.__chosen_plugin)  # checks for match with p.original_name
                if not liveobj_valid(cp):
                    self.main_script().log_message(logging.DEBUG, f"{log_id}looking for param name <{last_param_name}> in device <{self.__chosen_plugin.name}>")
                    chosen_param = script_utils.get_parameter_by_name(last_param_name, self.__chosen_plugin)  # checks for match with p.name
                else:
                    chosen_param = cp

                if liveobj_valid(chosen_param):
                    if isinstance(chosen_param, tuple):
                        self.main_script().log_message(logging.DEBUG, f"{log_id}v3_util.get_parameter_by_name() returned a valid tuple")
                        param = chosen_param[0]
                        if not liveobj_valid(param):
                            self.main_script().log_message(logging.WARNING, f"{log_id}but obj at index 0 was not liveobj_valid?")
                    else:
                        param = chosen_param

                    if liveobj_valid(param):
                        modifier = 1.0
                        if param.value < 1.0 and param.max == 1.0:
                            modifier = 0.01
                        if self.btn_ctlr.only_shift_is_pressed:
                            modifier *= 5
                        elif self.btn_ctlr.only_option_is_pressed:
                            modifier *= 10

                        if switch_id == C4SID_SINGLE_LEFT:
                            inc_amt = -1 * modifier
                        elif switch_id == C4SID_SINGLE_RIGHT:
                            inc_amt = 1 * modifier
                        else:
                            inc_amt = None
                        # self.main_script().log_message(logging.DEBUG, f"{log_id}updating value {param.value} by {inc_amt}")
                        script_utils.update_or_cycle_parameter_value(param, inc_amt, self.btn_ctlr.only_alt_is_pressed)
                        # btn_id, parameter, increment_amount
                        self.__parameter_inc_dec_args = {"btn_id": switch_id, "parameter": param, "increment_amount": inc_amt}
                        self.__parameter_inc_dec_flag = True
                        update_self = False
                        # self.main_script().log_message(logging.DEBUG, f"{log_id}updated value {param.value}")
                    else:
                        self.main_script().log_message(logging.WARNING, f"{log_id}param returned from get_parameter_by_name() was not liveobj_valid?")
                # else:
                #     # after a device change, but before a device parameter value change: when Single Left or Right buttons are pressed
                #     # execution silently passes through here (because the "last param changed" is None until a param changes)
                #     self.main_script().log_message(logging.DEBUG, f"{log_id}unable to get_parameter_by_name() neither returned parameter was liveobj_valid?")
            else:
                self.main_script().log_message(logging.WARNING, f"{log_id}can't get parameters from valid device <{self.__chosen_plugin.name}>?")
        return update_self

    def handle_pressed_v_pot(self, vpot_index):
        """method handles midi messages sent by encoder buttons, v_pot == 'encoder button'"""
        log_id = "EC.handle_pressed_v_pot: "
        if self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
            atd = self.__ds.data.get_active_track_details_at_song_index(self.__ds.last_selected_track_index)
            update_self = tcs_mode_util.handle_pressed_vpot(atd, vpot_index, self.handle_track_device_bank_view_update, self.handle_assignment_switch_ids,
                                                            self.is_locked_to_device, self.__ds, self.song(), self.__update_chosen_plugin_device,
                                                            self.main_script().log_message, self.subordinate_selected_track_allows_audio, self.__encoders,
                                                            self.xfade, self.subordinate_track_is_selected, self.main_script().show_message)
            if update_self:
                self.__reassign_encoder_parameters()

        elif self.btn_ctlr.current_active_script_mode == C4M_PLUGINS:

            last_index = 0 if self.__ds.last_selected_device_index is None else self.__ds.last_selected_device_index
            device_ref = self.__ds.data.get_device(self.__ds.last_selected_track_index, last_index)
            selected_track = self.__ds.data.get_track(self.__ds.last_selected_track_index).track
            update_self = td_mode_util.handle_pressed_vpot(device_ref, self.__display_parameters, vpot_index, selected_track,
                                                           self.handle_selected_device_parameter_bank_view_update, self.__encoders)
            if update_self:
                self.__reassign_encoder_parameters()
                self.request_rebuild_midi_map()

        elif self.btn_ctlr.current_active_script_mode == C4M_FUNCTION:
            sf_mode_util.handle_pressed_v_pot(vpot_index, self.__encoders, self.song(), self.application().view, self.btn_ctlr, self.unsolo_all_functionality,
                                              self.update_undo_info, self.update_redo_info, self.beat_pointer, self.nav_directions)

        # when no split leds are on, only do timer based display updates
        if self.btn_ctlr.nbr_split_leds_on > 0:
            self.one_display_update(force=True)

    def __send_parameter(self, vpot_index):
        """ Returns the send parameter that is assigned to the given encoder as a tuple (param, param.name) """
        if vpot_index < len(self.song().view.selected_track.mixer_device.sends):
            p = self.song().view.selected_track.mixer_device.sends[vpot_index]
            #  self.main_script().log_message(logging.DEBUG, "EC._send_parameter: Param name <{0}>".format(p.name))
            return p, p.name
        else:
            # The Song doesn't have this many sends
            return None, ''.join([" " for i in range(6)])

    def __plugin_parameter(self, vpot_index):
        """ Return the plugin parameter that is assigned to the given encoder as a tuple (param, param.name) """

        parameters = self.__ordered_plugin_parameters
        if vpot_index in encoder_range:
            current_track_device_preset_bank = self.__ds.last_selected_track_device_parameter_bank_nbr
            preset_bank_index = current_track_device_preset_bank * SETUP_DB_PARAM_BANK_SIZE
            current_track_param_count = len(parameters)
            is_param_index = current_track_param_count > vpot_index + preset_bank_index
            if is_param_index:
                p = parameters[vpot_index + preset_bank_index]
                return p

            # The device doesn't have this many parameters
            return None, ''.join([" " for i in range(6)])
        else: # theoretically not possible, vpot_index should never be outside the encoder_range
            return None, 'PPppPP'

    def __reorder_parameters(self):
        log_id = "EC.__reorder_parameters: "
        result = []
        if liveobj_valid(self.__chosen_plugin):
            active_track_ref = self.__ds.data.get_track(self.__ds.last_selected_track_index)
            # AssertionError: assert active_track_ref.selected_device_index is not None
            # (when rebuilding midi map after normal "add device" change - with chains expanding)
            if active_track_ref.selected_device_index is None:
                if self.__ds.last_selected_device_index is not None:
                    active_track_ref.selected_device_index = self.__ds.last_selected_device_index
                    assert active_track_ref.selected_device_index is not None
                    assert self.__ds.last_selected_device_index == active_track_ref.selected_device_index
                    active_device_ref = self.__ds.data.get_device(active_track_ref.index, active_track_ref.selected_device_index)
                    if active_device_ref is not None:
                        selected_device = active_device_ref.device
                    else:
                        msg = f"{log_id}no stored device for track {active_track_ref.track_name} at device index {active_track_ref.selected_device_index}, "
                        self.main_script().log_message(logging.ERROR, msg + "using chosen device params")
                        selected_device = self.__chosen_plugin

                    result = [(p, p.name) if liveobj_valid(p) else (p, "None") for p in selected_device.parameters]
                    device_class_name = selected_device.class_name
                    nbr_params = len(selected_device.parameters)
                    self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}ordered {len(result)} params for {device_class_name} with {nbr_params} params")
                else:
                    assert self.__ds.last_selected_device_index is None
                    assert active_track_ref.selected_device_index is None
                    msg = f"{log_id}no stored device for track ref {active_track_ref.track_name} at selected device indexes None, "
                    self.main_script().log_message(logging.ERROR, msg + "trying track details")
                    active_track_details_ref = self.__ds.data.get_active_track_details_at_song_index(self.__ds.last_selected_track_index)
                    if active_track_details_ref.selected_device_index is not None:
                        if active_track_details_ref.selected_device is not None:
                            # this is a sign that (some?) stored references are only getting updated at the 'track details' level when chain expansion behavior changes
                            self.__ds.last_selected_device_index = active_track_details_ref.selected_device_index
                            active_track_ref.selected_device_index = active_track_details_ref.selected_device_index
                            selected_device = active_track_details_ref.selected_device.device
                            self.main_script().log_message(logging.ERROR, f"{log_id}SUCCESS with track details")
                        else:
                            msg = f"{log_id}no stored device for track details ref {active_track_details_ref.track_name} even though stored device index "
                            msg += f"{active_track_details_ref.selected_device_index} is not None, using chosen device params"
                            self.main_script().log_message(logging.ERROR, msg)
                            selected_device = self.__chosen_plugin
                    else:
                        assert active_track_details_ref.selected_device_index is None
                        assert active_track_details_ref.selected_device is None
                        msg = f"{log_id}no stored device for track details ref {active_track_details_ref.track_name} because stored device index "
                        msg += f"is also None, using chosen device params"
                        self.main_script().log_message(logging.ERROR, msg)
                        selected_device = self.__chosen_plugin
                    result = [(p, p.name) if liveobj_valid(p) else (p, "None") for p in selected_device.parameters]
                    device_class_name = selected_device.class_name
                    nbr_params = len(selected_device.parameters)
                    self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}ordered {len(result)} params for {device_class_name} with {nbr_params} params")
            else:
                assert active_track_ref.selected_device_index is not None
                if self.__ds.last_selected_device_index is None:
                    self.__ds.last_selected_device_index = active_track_ref.selected_device_index

                active_device_ref = self.__ds.data.get_device(active_track_ref.index, active_track_ref.selected_device_index)
                if active_device_ref is not None:
                    selected_device = active_device_ref.device
                else:
                    msg = f"{log_id}no stored device for track {active_track_ref.track_name} at device index {active_track_ref.selected_device_index}, "
                    self.main_script().log_message(logging.ERROR, msg + "using chosen device params")
                    selected_device = self.__chosen_plugin

                result = [(p, p.name) if liveobj_valid(p) else (p, "None") for p in selected_device.parameters]
                device_class_name = selected_device.class_name
                nbr_params = len(selected_device.parameters)
                self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}ordered {len(result)} params for {device_class_name} with {nbr_params} params")
        else:
            self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}ordered {len(result)} params for None device with zero params")
        self.__ordered_plugin_parameters = result


    @staticmethod
    def get_device_on_off_parameter(d=None):
        if liveobj_valid(d):
            return find_if(lambda p: p.original_name.startswith('Device On') and liveobj_valid(p) and p.is_enabled, d.parameters)
        return None

    def get_ordered_on_off_parameter(self, d=None):
        if liveobj_valid(d):
            params = self.__ordered_plugin_parameters
            return find_if(lambda p: p.original_name.startswith('Device On') and liveobj_valid(p) and p.is_enabled, params)
        return None

    def __reassign_encoder_parameters(self):
        """ Reevaluate all v-pot -> parameter assignments """
        log_id = "EC.__reassign_encoder_parameters: "
        self.subordinate_track_is_selected = False
        self.subordinate_selected_track_allows_audio = False
        if not liveobj_valid(self.selected_track):
            self.main_script().log_message(logging.DEBUG, f"{log_id}self.selected track is not valid, blowing up soon")

        stored_track_ref = self.__ds.data.get_track(self.__ds.last_selected_track_index)
        if self.selected_track != stored_track_ref.track:
            msg = f"{log_id}self.selected track {self.selected_track.name} is not stored selected track {stored_track_ref.track_name}, blowing up soon?"
            self.main_script().log_message(logging.DEBUG, msg)
        else:
            assert self.selected_track == stored_track_ref.track

        stored_devices = self.__ds.selected_track_stored_device_list
        extended_device_list = stored_devices
        self.main_script().log_message(logging.DEBUG, f"{log_id}reassigning encoder parameters for track with {len(extended_device_list)} devices")

        if self.selected_track != self.song().master_track:
            self.subordinate_track_is_selected = True
            if self.selected_track.has_audio_output:
                self.subordinate_selected_track_allows_audio = True

        self.__display_parameters = []

        if self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
            self.returns_switch = 0
            is_log_less_than_info = self.current_log_level < self.log_levels["INFO"]
            tcs_mode_util.reassign_encoder_parameters(self.selected_track, extended_device_list, self.main_script().log_message, self.__ds, self.__encoders,
                                                      self.__display_parameters, self._update_vpot_led_device_is_active_status, self.subordinate_track_is_selected,
                                                      self.subordinate_selected_track_allows_audio, self.__send_parameter, is_log_less_than_info, self.xfade)

        elif self.btn_ctlr.current_active_script_mode == C4M_PLUGINS:
            td_mode_util.reassign_encoder_parameters(self.selected_track, self.__ds, self.__encoders, self.__chosen_plugin, self.__plugin_parameter,
                                                     self.__display_parameters)

        elif self.btn_ctlr.current_active_script_mode == C4M_FUNCTION:
            sf_mode_util.reassign_encoder_parameters(self.__encoders, self.song(), self.__display_parameters)

        elif self.btn_ctlr.current_active_script_mode == C4M_USER:
            usr_mode_util.reassign_encoder_parameters(self.__encoders, extended_device_list, self._update_vpot_led_device_is_active_status,
                                                      self.send_user_mode_display_strings)

        if self.btn_ctlr.nbr_split_leds_on > 0:  # when no split leds are on, only do timer based display updates
            self.one_display_update(force=True)
        return

    def send_user_mode_display_strings(self):
        top_line = 'MackieC4Pro remote script User mode'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        bottom_line = 'Switching to Max Sequencer patch control'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        self.send_display_string(LCD_ANGLED_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
        self.send_display_string(LCD_ANGLED_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)
        top_line = 'Press and Hold the Marker button again'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        bottom_line = 'Then Press the Lock button to Exit USER mode and'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)
        top_line = 'Return to the previous remote script mode. All other'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        bottom_line = 'button and pot control functions pass to the Max patch'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)
        top_line = 'Press and Hold Marker then Press Lock'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        bottom_line = 'to exit USER mode'.center(NUM_TEXT_BYTES_PER_SYSEX_MSG)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)

    def _update_vpot_led_device_is_active_status(self):
        log_id = "EC._update_vpot_leds_for_device_toggle: "
        # self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}{'' if self.expand_chains else 'NOT '}expanding chains")
        # extended_device_list = self.get_device_list(self.selected_track.devices, expand_chains=self.expand_chains)
        extended_device_list = self.__ds.selected_track_stored_device_list
        current_device_bank_track = self.__ds.last_selected_track_device_bank_view_index
        current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE) # offset is 0, 8, 16, 24, etc
        assert self.__ds.selected_track_nbr_stored_devices == len(extended_device_list)
        # In C4M_PLUGINS mode encoder 8 "also" controls device ON/OFF status (first device parameter)
        assert self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP or self.btn_ctlr.current_active_script_mode == C4M_PLUGINS

        for s_index in row_01_encoders:
            row_index = s_index - SETUP_DB_DEVICE_BANK_SIZE
            if row_index + current_encoder_bank_offset < self.__ds.selected_track_nbr_stored_devices:
                device_index = row_index + current_encoder_bank_offset
                if device_index < len(extended_device_list):
                    device = extended_device_list[device_index]
                    if device.is_active:
                        self.__encoders[s_index].show_full_enlighted_poti()
                    else:
                        self.__encoders[s_index].unlight_vpot_leds()
                else:
                    self.main_script().log_message(self.log_levels["TRACE"], f"{log_id}index {device_index} too large for stored device list?")
                    self.__encoders[s_index].unlight_vpot_leds()


    def get_alternating_display_text(self, text: str, index: int, width: int = 6) -> str:
        """use this to switch between first 6 and second 6 characters for parameter names etc"""
        # Use raw name as-is if it fits
        if len(text.strip()) <= width:
            return adjust_string(text.strip(), width)

        # Remove all spaces only if the name is longer than 6
        compressed = text.replace(" ", "") if len(text.strip()) > width else text
        padded = compressed.ljust(width * 2)[:width * 2]

        now = time.time()
        state = self.encoder_name_display_state[index]

        if now - state["last_switch_time"] >= 1.5:
            state["toggle"] = not state["toggle"]
            state["last_switch_time"] = now

        part = padded[width:width * 2] if state["toggle"] else padded[:width]

        return adjust_string(part.strip(), width)


    def get_scrolling_display_text(self, text: str, index: int, width: int = 6, max_scroll_len: int = 18) -> str:
        """Scroll 6-char window across cleaned string up to 18 chars.
        - ≤6: static
        - 7–8: adjust_string to 6
        - 9–18: scroll (spaces removed)
        - >18: adjust_string to 18, then scroll
        """

        raw = str(text).strip()
        if len(raw) <= width:
            return adjust_string(raw, width)

        raw_length_ns = len(raw.replace(" ", ""))  # count without spaces

        # Case 1: 7–8 → smart shorten to 6
        if width < raw_length_ns <= width + 2:
            return adjust_string(raw, width)

        # Case 2: >18 → shorten to 18 first, then scroll
        if raw_length_ns > max_scroll_len:
            scroll_text = adjust_string(raw, max_scroll_len)
        else:
            # Case 3: 9–18 → scroll, but with spaces removed
            scroll_text = raw.replace(" ", "")[:max_scroll_len]

        state = self.encoder_name_display_state[index]
        now = time.time()

        max_scroll_pos = max(0, len(scroll_text) - width)

        at_start = state["scroll_pos"] == 0
        at_end = state["scroll_pos"] == max_scroll_pos
        delay = 1.5 if at_start or at_end else 0.5

        if now - state["last_scroll_time"] >= delay:
            state["scroll_pos"] += 1
            state["last_scroll_time"] = now

            if state["scroll_pos"] > max_scroll_pos:
                state["scroll_pos"] = 0

        window = scroll_text[state["scroll_pos"]:state["scroll_pos"] + width]
        return adjust_string(window, width)

    @script_utils.CoolDown(300)
    def repeating_param_inc_dec_moves(self, btn_id, parameter, increment_amount):
        # See self.handle_bank_switch_ids method above for how the repeating cycle gets started when this button is pressed
        # The repeating cycle stops here when this button is released.
        if self.btn_ctlr.get_parameter_btn_pressed_state(btn_id):
            script_utils.update_or_cycle_parameter_value(parameter, increment_amount)
        else:
            self.__parameter_inc_dec_args = None
            self.__parameter_inc_dec_flag = False

    def on_update_display_timer(self):
        """Called by Live every 100 ms. This is the original "real time" device-display update callback method"""
        if self.btn_ctlr.nbr_split_leds_on < 3: # when 3 split leds are ON, don't do any timer based display updates
            if self.song().is_playing:
                self.__do_display_update()
            elif self.__display_lag_timer_bang():
                self.__do_display_update()

        if self.__parameter_inc_dec_flag and self.__parameter_inc_dec_args is not None:
            try:
                self.repeating_param_inc_dec_moves(**self.__parameter_inc_dec_args)
            except script_utils.TooSoon:
                pass


    def one_delayed_display_update(self, delay_secs=.050, force=False): # 50 ms
        time.sleep(delay_secs)
        if self.btn_ctlr.nbr_split_leds_on > 0:  # when no split leds are on, only do timer based display updates
            self.one_display_update(force=force)

    def one_display_update(self, force=False):
        """do a display update passing force as needed"""
        self.__do_display_update(force=force)

    def __display_lag_timer_bang(self):
        # (when song is NOT playing) count to _upper_bounds[bounds_index] before returning True and resetting the count
        max_lag = self.__display_update_lag_upper_bounds[self.__display_update_lag_upper_bounds_index]
        if self.__display_update_lag_upper_bounds_index == len(self.__display_update_lag_upper_bounds) - 1:
            return False  # never bang at last lag setting
        elif self.__display_update_lag_counter < max_lag:
            self.__display_update_lag_counter += 1
            return False  # increment countdown to bang
        else:
            self.__display_update_lag_counter = 0
            return True  # reset count and bang

    def __do_display_update(self, force=False):
        """force means send the generated LCD screen display update messages even if they match the previous update messages sent"""
        log_id = "EC.__do_display_update: "
        upper_string1 = ''
        lower_string1 = ''
        upper_string2 = ''
        lower_string2 = ''
        upper_string3 = ''
        lower_string3 = ''
        upper_string4 = ''
        lower_string4 = ''
        selected_track = self.__locked_device_track  # == self.selected_track when not locked
        if self.btn_ctlr.current_active_script_mode == C4M_USER:
            return  # no display updates in this mode (all updates in this mode, if any, are handled by the Max sequencer patch)
        elif self.btn_ctlr.current_active_script_mode == C4M_CHANNEL_STRIP:
            show_device_banking_text = self.__ds.selected_track_nbr_stored_devices > 1
            lcd1_device_chain_flags = [False for x in row_01_encoders]

            atd = self.__ds.data.get_active_track_details_at_song_index(self.__ds.last_selected_track_index)
            for i in range(SETUP_DB_DEVICE_BANK_SIZE):
                # bank view index 4, with bank start index 32, means check devices 32 - 39 for 'chains' (xxxGroupDevice class_names)
                # {unsupported operand type(s) for *: 'NoneType' and 'int'} if the selected track never had a device bank in view before
                # when two existing tracks are Ctrl-G grouped, the new (Group) Track can fall into this category and cause the bracketed RemoteScriptError
                bank_start = 0 if atd.active_track.track_device_bank_view_index is None else atd.active_track.track_device_bank_view_index * SETUP_DB_DEVICE_BANK_SIZE
                device_index = bank_start + i
                if device_index < atd.device_count:
                    dev_ref = atd.devices[device_index]
                    if dev_ref.device.class_name.endswith("GroupDevice"):
                        lcd1_device_chain_flags[i] = True

            upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4 = (
                tcs_mode_util.do_display_update(
                self.application().view, selected_track, self.__chosen_plugin, self.is_locked_to_device, self.__display_parameters, self.btn_ctlr,
                self.get_scrolling_display_text, self.xfade, self.subordinate_track_is_selected, self.__encoders, show_device_banking_text,
                lcd1_device_chain_flags, self.expand_chains)
            )
        elif self.btn_ctlr.current_active_script_mode == C4M_PLUGINS:
            device_ref = self.__ds.data.get_device(self.__ds.last_selected_track_index, self.__ds.last_selected_device_index)
            upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4 = (
                td_mode_util.do_display_update(
                    self.__ds.last_selected_device_index, selected_track, self.__chosen_plugin, self.is_locked_to_device,
                    self.pad_right_if_less, device_ref, self.__display_parameters, self.btn_ctlr, self.get_scrolling_display_text,
                    self.main_script().log_message)
            )
        elif self.btn_ctlr.current_active_script_mode == C4M_FUNCTION:
            upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4 = (
                sf_mode_util.do_display_update(
                    self.application().view, self.song(), selected_track, self.__encoders, self.__display_parameters, self.unsolo_all_functionality, self.btn_ctlr,
                    self._last_undo_label_time, self._last_undo_label, self.get_scrolling_display_text, self._last_redo_label_time, self._last_redo_label,
                    self.beat_pointer, self.loop_length)
            )
        else:
            self.main_script().log_message(logging.ERROR, f"{log_id}UNKNOWN SCRIPT MODE!!!")


        self.send_display_string(LCD_ANGLED_ADDRESS, self.pad_right_if_less(upper_string1), LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, self.pad_right_if_less(upper_string2), LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, self.pad_right_if_less(upper_string3), LCD_TOP_ROW_OFFSET, force=force)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, self.pad_right_if_less(upper_string4), LCD_TOP_ROW_OFFSET, force=force)

        self.send_display_string(LCD_ANGLED_ADDRESS, self.pad_right_if_less(lower_string1), LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_TOP_FLAT_ADDRESS, self.pad_right_if_less(lower_string2), LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_MDL_FLAT_ADDRESS, self.pad_right_if_less(lower_string3), LCD_BOTTOM_ROW_OFFSET, force=force)
        self.send_display_string(LCD_BTM_FLAT_ADDRESS, self.pad_right_if_less(lower_string4), LCD_BOTTOM_ROW_OFFSET, force=force)

        return

    def pad_right_if_less(self, text, pad_char=" ", max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG, log_success=False):
        """operates like string.ljust(pad_char, max_length), but logs details"""
        log_id = "EC.pad_right_if_less: "
        if len(text) > max_length:
            temp = text[:max_length]
            # input display line string length seems to "always" be 56 instead of 55  (56 is the "bottom line offset", 56th byte of "top line" text is actually
            # the first byte of the "bottom line".  The C4 would accept 110 bytes (or more) in one message and write both top and bottom lines, but
            # this script always writes full single lines, 55 bytes
            # self.main_script().log_message(logging.DEBUG, f"{log_id}input text was too long {len(text)}, truncated to {len(temp)}: {temp}")
            text = temp
        elif len(text) < max_length:
            pad_len = max_length - len(text)
            temp = text
            old_len = len(text)
            text = text + "".join([pad_char for i in range(pad_len)])
            if not len(text) == max_length:
                self.main_script().log_message(logging.ERROR, f"{log_id}oopsie? padded length {len(text)} not equal to max length {max_length}")
                self.main_script().log_message(logging.ERROR, f"{log_id}before ({temp}) from length ({text})")
            elif log_success:
                self.main_script().log_message(logging.ERROR, f"{log_id}successfully padded text to max length {max_length} from length {old_len}")
                self.main_script().log_message(logging.ERROR, f"{log_id}before ({temp}) from length ({text})")

        return text

    def send_display_string(self, display_address, text_for_display, display_row_offset, cursor_offset=0, force=False):
        """
            Sends a midi sysex message to C4
            display_address: LCD_ANGLED_ADDRESS, LCD_TOP_FLAT_ADDRESS, LCD_MDL_FLAT_ADDRESS, LCD_BTM_FLAT_ADDRESS
            display_row_offset: first character index of top line or bottom line
            cursor_offset: offset index into top or bottom row, top line values > 0 will overwrite bottom line unless msg text is truncated to (55 - cursor_offset)
            force: sometimes what is stored as the last message got blanked off the LCD by other factors and needs to be resent anyway
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_for_display, display_row_offset, cursor_offset)
        is_update = self.last_send_messages[display_address][display_row_offset] != ascii_text_sysex_ints

        if force or is_update:
            self.last_send_messages[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def __generate_sysex_body(self, text_for_display, display_row_offset, cursor_offset=0):
        # looks like cursor_offset is supposed to be an index to each cell in an LCD row but the SYSEX message for writing to
        # any display row is always 63 bytes (55 bytes of ASCII text) i.e. the whole row, so cursor_offset can be eliminated
        if display_row_offset == LCD_TOP_ROW_OFFSET:  # 0x00
            offset = cursor_offset
        elif display_row_offset == LCD_BOTTOM_ROW_OFFSET:  # 0x38 (56 == NUM_CHARS_PER_DISPLAY_LINE + 2)
            offset = LCD_BOTTOM_ROW_OFFSET + cursor_offset
        else:
            assert 0  # explode on any invalid display_row_offset value

        # convert Unicode string (list of character values) to list of integer values
        ascii_text_sysex_ints = [ord(c) for c in text_for_display]
        for i in range(len(ascii_text_sysex_ints)):
            # replace any integer values above the ASCII 7-bit (MIDI_DATA) range (0x00 - 0x7F)
            if ascii_text_sysex_ints[i] > MIDI_DATA_LAST_VALID:
                ascii_text_sysex_ints[i] = ASCII_HASH

        return ascii_text_sysex_ints

    def refresh_state(self):
        # overrides MackieC4Component.refresh_state() which defers to C4.refresh_state() which drops and reloads all listeners, and we don't want that
        for s in self.__encoders:
            s.refresh_state()
