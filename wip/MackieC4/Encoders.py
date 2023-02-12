# was Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/Encoders.py
# Compiled at: 2011-01-13 21:07:51

from __future__ import absolute_import, print_function, unicode_literals  # MS
from . MackieC4Component import *

import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

from itertools import chain
from ableton.v2.base import liveobj_valid


class Encoders(MackieC4Component):
    """ Represents one encoder of the Mackie C4 """
    __module__ = __name__

    def __init__(self, main_script, vpot_index):
        MackieC4Component.__init__(self, main_script)
        self.within_destroy = False
        self.__encoder_controller = None
        self.__vpot_index = vpot_index
        self.__vpot_cc_nbr = vpot_index + C4SID_VPOT_CC_ADDRESS_BASE
        self.__v_pot_parameter = None
        self._Encoders__assigned_track = None

        self.__v_pot_display_memory = {VPOT_CURRENT_CC_VALUE: [], VPOT_NEXT_CC_VALUE: []}
        self.__update_led_ring_display_mode(VPOT_DISPLAY_SINGLE_DOT)

        self.v_pot_display_frame_count = 0
        self.v_pot_display_memory_len = len(self.__v_pot_display_memory[VPOT_CURRENT_CC_VALUE])
        return

    # function provided by MackieC4Component super
    def destroy(self):
        # self.destroy()
        self.within_destroy = True
        self.unlight_vpot_leds()
        self.refresh_state()
        MackieC4Component.destroy(self)
        self.within_destroy = False

    def set_encoder_controller(self, encoder_controller):
        self.__encoder_controller = encoder_controller

    def vpot_index(self):
        return self.__vpot_index

    def v_pot_parameter(self):
        return self.__v_pot_parameter

    def animate_v_pot_led_ring(self, frame, reverse=False):
        remainder = frame % self.v_pot_display_memory_len
        if reverse:
            update_value = self.__v_pot_display_memory[VPOT_NEXT_CC_VALUE][remainder]
        else:
            update_value = self.__v_pot_display_memory[VPOT_CURRENT_CC_VALUE][remainder]

        self.update_led_ring(update_value)

    def set_v_pot_parameter(self, parameter, display_mode=VPOT_DISPLAY_BOOLEAN):
        if not display_mode == None:
            self.__update_led_ring_display_mode(display_mode)
        self.__v_pot_parameter = parameter
        if not parameter:
            self.unlight_vpot_leds()

    def __update_led_ring_display_mode(self, display_mode=VPOT_DISPLAY_BOOLEAN):

        self.__v_pot_display_mode = display_mode

        # when mode is boost-cut VPOT_DISPLAY_BOOST_CUT: (0x11, 0x1B), the C4 allows both 0x11 and 0x1B as valid "Boost Cut" values
        # the list: self.__v_pot_display_memory[VPOT_CURRENT_CC_VALUE] should contain element 0x1B == eleven elements
        # 0x11, 0x12, 0x13...0x1B
        display_mode_cc_base = encoder_ring_led_mode_cc_values[self.__v_pot_display_mode][0]
        # for "Boost Cut": self.__v_pot_display_mode][1] - display_mode_cc_base == 0x1B - 0x11 == 0x0A == ten elements
        # that's why +1 here
        range_len = encoder_ring_led_mode_cc_values[self.__v_pot_display_mode][1] - display_mode_cc_base + 1
        self.__v_pot_display_memory[VPOT_CURRENT_CC_VALUE] = [display_mode_cc_base + x for x in range(range_len)]

        #  [:] is the default "slicing operator" operation. a list copy assignment operation here
        self.__v_pot_display_memory[VPOT_NEXT_CC_VALUE] = self.__v_pot_display_memory[VPOT_CURRENT_CC_VALUE][:]
        self.__v_pot_display_memory[VPOT_NEXT_CC_VALUE].reverse()

        self.v_pot_display_memory_len = len(self.__v_pot_display_memory[VPOT_CURRENT_CC_VALUE])

    def update_led_ring(self, update_value):
        self.send_midi((CC_STATUS, self.__vpot_cc_nbr, update_value))

    def unlight_vpot_leds(self):
        data2 = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_BOOLEAN][0]
        # midi CC messages (0xB0, 0x20, data) (CC_STATUS, C4SID_VPOT_CC_ADDRESS_1, data)
        self.update_led_ring(RING_LED_ALL_OFF)

    def show_full_enlighted_poti(self):
        data2 = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_BOOLEAN][1]
        # midi CC messages (0xB0, 0x20, data) (CC_STATUS, C4SID_VPOT_CC_ADDRESS_1, data)
        self.update_led_ring(data2)

    # to be deleted!?
    def show_vpot_ring_spread(self):
        data1 = 0x31
        data2 = 0x36 - 0x31
        # data3 = a tuple of (0x31, 0x32, 0x33, 0x34, 0x35) when data2 = 0x36 - 0x31 == 0x05
        # since VPOT_DISPLAY_SPREAD: (0x31, 0x36)
        data2 = data2 + 1  # to include the last valid "spread" value
        data3 = tuple(data1 + x for x in range(data2))
        # midi CC messages (0xB0, 0x20, data) (CC_STATUS, C4SID_VPOT_CC_ADDRESS_1, data)
        self.send_midi((CC_STATUS, self.__vpot_cc_nbr, data3))

    def build_midi_map(self, midi_map_handle):  # why do we have an additional build_midi_map here in Encoders?? Already in MackieC4
        """Live -> Script
        Build DeviceParameter Mappings, that are processed in Audio time, or forward MIDI messages explicitly to our receive_midi_functions.
        Which means that when you are not forwarding MIDI, nor mapping parameters, you will never get any MIDI messages at all.
        """
        needs_takeover = False
        encoder = self.__vpot_index
        param = self.__v_pot_parameter
        if liveobj_valid(param):

            feedback_rule = Live.MidiMap.CCFeedbackRule()
            feedback_rule.channel = 0
            feedback_rule.cc_no = self.__vpot_cc_nbr
            display_mode_cc_base = encoder_ring_led_mode_cc_values[self.__v_pot_display_mode][0]
            feedback_val_range_len = encoder_ring_led_mode_cc_values[self.__v_pot_display_mode][1]
            feedback_val_range_len = feedback_val_range_len - display_mode_cc_base + 1
            feedback_rule.cc_value_map = tuple([display_mode_cc_base + x for x in range(feedback_val_range_len)])
            feedback_rule.delay_in_ms = -1.0
            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, param, 0, encoder, Live.MidiMap.MapMode.relative_signed_bit, feedback_rule, needs_takeover, sensitivity=1.0)  # MS "sensitivity" added
            # self.main_script().log_message("potIndex<{}> feedback<{}> MAPPED, coming from build_midi_map in __encoders".format(encoder, param))

            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, param)

        else:
            if not liveobj_valid(param):
                if param is None:
                    channel = 0
                    cc_no = self.__vpot_cc_nbr
                    Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, channel, cc_no)
                    # self.main_script().log_message("potIndex<{0}> mapping encoder to FORWARD CC <{1}> MS: coming from build_midi_map in __encoders".format(encoder, cc_no))
                else:
                    self.main_script().log_message("potIndex<{0}> nothing mapped param is lost weakref".format(encoder))
            else:
                self.main_script().log_message("potIndex<{0}> nothing mapped param <{1}>".format(encoder, param))

    def assigned_track(self):
        return self._Encoders__assigned_track

    def handle_vpot_rotation(self, vpot_index, cc_value):
        if vpot_index is self.__vpot_index and self.__encoder_controller is not None:
            self.__encoder_controller.handle_vpot_rotation(self.__vpot_index, cc_value)

    def __assigned_track_index(self):  # MS new from Mackie Control.ChannelStrip
        index = 0
        for t in chain(self.song().visible_tracks, self.song().return_tracks):
            if t == self._Encoders__assigned_track:
                return index
            index += 1

        if self._Encoders__assigned_track:
            pass

    def __select_track(self):
        if self._Encoders__assigned_track:
            all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)  # MS tuple is new and from Mackie script
            if self.song().view.selected_track != all_tracks[self.__assigned_track_index()]:  # MS new but seems to work
                self.song().view.selected_track = all_tracks[self.__assigned_track_index()]
            elif self.application().view.is_view_visible('Arranger'):
                if self._Encoders__assigned_track:
                    self._Encoders__assigned_track.view.is_collapsed = not self._Encoders__assigned_track.view.is_collapsed

    def refresh_state(self):
        return ' '

    def on_update_display_timer(self):
        pass
