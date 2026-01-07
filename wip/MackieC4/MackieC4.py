# was Python bytecode 2.5 (62131)
# Compiled at: 2011-01-22 04:38:37

"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
# Copyright generally applies for the life of the original Copyright owner (in the USA), even open source code remains copyright protected
# The original source code is available as the first commit in this repository
# All changes to the original source are Copyright (C) 201x - 2025 Markus Schloesser (and contributors)
#
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser GPL (General Public License)
# as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser GPL for more details.
#
# You should have received a copy of the GNU Lesser GPL along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

This script is based off the Ableton Live supplied MIDI Remote Scripts.
This is the second file that is loaded, by way of being instantiated through __init__.py
"""

from __future__ import absolute_import, print_function, unicode_literals
import logging
import time

import Live
from ableton.v2.base import liveobj_valid, clamp

from .TimeDisplay import TimeDisplay
from . import song_util
from .consts import *
from .Encoders import Encoders
from .EncoderController import EncoderController
from .c4_device_provider import C4DeviceProvider
from .MackieC4ListenerMixin import MackieC4ListenerMixin

if sys.version_info[0] >= 3:  # Python 3.x+ (Live 11+)
    from builtins import str
    from builtins import range
    from builtins import object


logger = logging.getLogger(__name__)



class MackieC4(MackieC4ListenerMixin, object):
    """  Main class that establishes the MackieC4 Component
         --- although technically, the Mackie Control C4Pro is an "extension" of the Mackie Control itself (like the MackieControlXT), this script stands alone.
             It doesn't work 'with' those Midi Remote Scripts which is why is_extension() returns False from here
       Main class that establishes the Mackie Control <-> Live interaction. It acts as a container/manager for all the
       Mackie C4 subcomponents like Encoders, Displays and so on.
       Further it is glued to Lives MidiRemoteScript C instance, which will forward some notifications to us,
       and lets us forward some requests that are needed beside the general Live API (see 'send_midi' or 'request_rebuild_midi_map').
    """
    __module__ = __name__

    scene_index = 0
    track_index = 0
    track_count = 0
    
    script_log_levels = {"ALWAYS": 0, "DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "NEVER": 99}
    current_script_log_level = script_log_levels["DEBUG"]

    def __init__(self, c_instance):
        self.__c_instance = c_instance

        self.__components = []
        self.__surface_is_locked = False
        self.__device_provider = C4DeviceProvider(self.song())
        self.__handling_assignment_switch = False
        self.__processing_track_device_state_change = False
        self.__processing_track_state_change = False
        self._selected_track_index = 0
        self._selected_track_callback_type = 0

        # Guard needed because self.__encoder_controller doesn't exist yet when self.__encoders are initializing and trying to send_midi()
        self.__init_ready = False
        self.__encoders = [Encoders(self, i) for i in encoder_range]
        self.__encoder_controller = EncoderController(self, self.__encoders, self.__device_provider)        
        for comp in [*self.__encoders, self.__encoder_controller, self.__device_provider]:
            self.register_component(comp)
        self.__init_ready = True

        MackieC4ListenerMixin.__init__(self, encoder_controller=self.__encoder_controller)

        # if the goodbye message is displaying on the C4 after Live shutdown, and Live restarts, clear the display asap
        self.__encoder_controller.clear_all_lcds()
        self.__encoder_controller.clear_all_leds()
        self.send_midi((NOTE_ON_STATUS, C4SID_CHANNEL_STRIP, BUTTON_STATE_ON)) # turn ON default mode LED

        tracks = self.song().visible_tracks + self.song().return_tracks
        index = 0

        # assign track to the local index of the matching selected track in Live
        for track in tracks:
            if track == self.song().view.selected_track:
                self.last_selected_track_index = index
            index = index + 1

        self.track_count = len(tracks)
        self.callback_type_track_counts = {0: int(len(self.song().visible_tracks)), 1: int(len(self.song().return_tracks)), 2: 1}

        # if refresh_state is not already listening for visible tracks view changes
        if self.song().visible_tracks_has_listener(self.tracks_change) != 1:
            self.song().add_visible_tracks_listener(self.tracks_change)

        self.__encoder_controller.build_setup_database() # self.song() reference needed

        # To display song position pointer or beats on display
        self.__time_display = TimeDisplay(self)
        self.register_component(self.__time_display)

        self.__shift_is_pressed = False
        self.__option_is_pressed = False
        self.__ctrl_is_pressed = False
        self.__alt_is_pressed = False
        self.__marker_is_pressed = False
        self.__user_mode_exit = False

        self.c4_note_range = set(range(C4SID_FIRST, C4SID_LAST + 1))

        self.note_handling_dict = {
            **{note: self.track_inc_dec for note in track_nav_switch_ids},
            **{note: self.__encoder_controller.handle_bank_switch_ids for note in bank_switch_ids},
            **{note: self.__encoder_controller.handle_bank_switch_ids for note in single_switch_ids},
            **{note: self.__encoder_controller.handle_slot_nav_switch_ids for note in slot_nav_switch_ids},
            **{note: self.__encoder_controller.handle_system_switch_ids for note in system_switch_ids},
            **{note: self.__encoder_controller.handle_assignment_switch_ids for note in assignment_mode_switch_ids},
            **{note: self.__encoder_controller.handle_pressed_v_pot for note in encoder_switch_ids}
        }


    def connect_script_instances(self, instanciated_scripts):
        """
        Called by the Application as soon as all scripts are initialized. You can connect yourself to other running
        scripts here.
        """
        pass

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        """
        To be called from any components, as soon as their internal state changed in a way, that we do need to remap the
        mappings that are processed directly by the Live engine. Don't assume that the request will immediately result in
        a call to your build_midi_map function. For performance reasons this is only called once per GUI frame.

        When the internal MIDI controller has changed in a way that you need to rebuild the MIDI mappings, request a rebuild
        by calling this function. This is processed as a request, to be sure that it's not too often called, because it's
        time-critical.
        """
        self.__c_instance.request_rebuild_midi_map()

    def update_display(self):
        """
        Aka on_timer. Called every 100 ms and should be used to update display relevant parts of the controller.
        """
        if self.__encoder_controller.assignment_mode() != C4M_USER:
            # self.log_message(logging.DEBUG, "C4.update_display: firing")  # verbose log message
            for c in self.__components:
                c.on_update_display_timer()
        # else:
        #      the script is in USER mode (or not initialized yet)
        #      and should NOT be sending display updates
        #      self.log_message(logging.DEBUG, "C4.update_display: NOT firing")  # also verbose

    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices that this script is assigned to.
        """
        if self.__init_ready and (self.__handling_assignment_switch or self.__encoder_controller.assignment_mode() != C4M_USER):
            # self.__handling_assignment_switch means the script might be switching to USER mode so we still want to send this midi
            # self.log_message(logging.DEBUG, "C4.send_midi: firing")  # very verbose log message
            self.__c_instance.send_midi(midi_event_bytes)
        # else:
        #      the script is completely into USER mode (or not initialized yet)
        #      and should NOT be sending any midi events via this method
        #      self.log_message(logging.DEBUG, "C4.send_midi: NOT firing")  # verbose log message?

    def build_midi_map(self, midi_map_handle):
        """Live -> Script        Build DeviceParameter mappings, that are processed in Audio time, or forward MIDI messages
        explicitly to our receive_midi_functions. Which means that when you are not forwarding MIDI, nor mapping parameters, you will
        never get any MIDI messages at all. """

        # build the relationships between info in Live and each __encoder, this is the MAPPING part (Parameters handled by Live directly)
        for s in self.__encoders:
            # this s.build_midi_map() will ask to forward midi CC messages from any encoder that is currently "mapped to" None (instead of a liveobj_valid(param))
            s.build_midi_map(midi_map_handle)

        # ask Live to forward all midi note messages here. This is the FORWARDING part  (Parameters handled by this script, for example for Function mode)
        # forward every incoming midi Note or CC message with an id value between 0 and 63 to the script for processing, some of these CC forwarding requests
        # will be second requests for encoder ids above that don't get mapped to a valid "live object" at any given time, but you can ask as many times as
        # you want Live doesn't forward the same message twice. Even for encoders mapped above (handled by Live directly), forward the midi messages they emit
        for i in range(C4SID_FIRST, C4SID_LAST + 1):
            Live.MidiMap.forward_midi_note(self.handle(), midi_map_handle, 0, i)
            Live.MidiMap.forward_midi_cc(self.handle(), midi_map_handle, 0, i)


    def receive_midi(self, midi_bytes):
        log_id = "C4.receive_midi: "
        """Live -> Script    MIDI messages are only received through this function, when explicitly forwarded in 'build_midi_map'."""
        # coming from C4 midi_bytes[0] is always 0x91 or 0xB1 (NOTE_ON or CC) [C4 sends note on with velocity 0 for note off]
        # velocity of note on messages is always 7F, velocity of note off messages is always 00
        # C4 always sends and receives on channel 1
        is_note_on_msg = midi_bytes[0] & 0xF0 == NOTE_ON_STATUS  # (& F0 strips off any channel related bits)
        is_note_off_msg = midi_bytes[0] & 0xF0 == NOTE_OFF_STATUS

        if self.__encoder_controller.assignment_mode() == C4M_USER:
            # already in USER mode, check for exit status
            marker_on_event = is_note_on_msg and midi_bytes[1] == C4SID_MARKER
            lock_on_event = is_note_on_msg and midi_bytes[1] == C4SID_LOCK
            is_marker_on_press = marker_on_event and midi_bytes[2] == BUTTON_STATE_ON
            is_lock_on_press = lock_on_event and midi_bytes[2] == BUTTON_STATE_ON
            # a true c4 release never happens, Live always converts Note ON messages with velocity 0 to Note OFF messages
            is_c4_marker_release = marker_on_event and midi_bytes[2] == BUTTON_STATE_OFF
            is_marker_off_release = is_note_off_msg and midi_bytes[1] == C4SID_MARKER and midi_bytes[2] == BUTTON_STATE_OFF
            previous_mode_switch_id = assignment_mode_switch_ids[self.__encoder_controller.last_assignment_mode()]
            self.__user_mode_exit = False  # might be about to exit

            if is_marker_on_press:
                self.set_marker_is_pressed(True)
                # self.log_message(logging.DEBUG, f"{log_id}USER mode MARKER is pressed")
            elif is_c4_marker_release or is_marker_off_release:
                self.set_marker_is_pressed(False)
                # if is_c4_marker_release:
                #    self.log_message(logging.DEBUG, f"{log_id}USER mode MARKER is released, unexpected NOTE ON event")
                # else:
                #     self.log_message(logging.DEBUG, f"{log_id}USER mode MARKER is released")
            elif is_lock_on_press and self.__marker_is_pressed:
                # self.log_message(logging.DEBUG, f"{log_id}USER mode LOCK press event while MARKER is pressed")
                # conditions here do NOT need to guard against processing this button combo when NOT already in user mode
                #  events for patch to process before sending STOP signal
                # no LOCK Press event forwarded to the patch
                # the USER mode patch's MARKER button status is "pressed",
                # send a "release" event to the patch that completes one press/release cycle
                self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_OFF))
                # Now "restore" the USER mode patch's MARKER button LED ON/OFF status
                # One Press+Release event toggles the LED ON/OFF, Two (quick) Press+Release events means the LED ON/OFF state "doesn't change"
                self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_ON))
                self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_OFF))
                # STOP signal for patch to process
                self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MAX_BYPASS_ID, BUTTON_STATE_OFF))  # for this signal: velocity 0 means STOP processing
                # self.log_message(logging.DEBUG, f"{log_id}sending 'button 22' signal toggling Max bypass mode, STOP processing START bypassing")
                self.__user_mode_exit = True  # flag needs to stay set until first method re-entry after USER mode only
                self.__encoder_controller.handle_assignment_switch_ids(previous_mode_switch_id)
                # self.log_message(logging.DEBUG, f"{log_id}USER mode exit!  script is no longer in USER mode")
                self.set_marker_is_pressed(False)  # technically not released yet but don't need the signal any longer

            if not self.__user_mode_exit:
                # C4M_USER mode normal forwarding to Max patch for processing
                # (or spurious feedback to C4 if patch is not running or patch processing is manually bypassed?)
                # when the sequencer patch is not connected AND we're in USER mode but not exiting, for example,
                # a user can only turn ON every "control button" LED (7 total LEDs SPLIT 1/3 through FUNCTION)
                # but every button PRESS and encoder TURN message received that reaches here becomes spurious feedback "forwarded" to the C4
                # whenever the Max Sequencer patch is not in use.  If the script is running solo, it's probably "never" in USER mode anyway.
                # no way to stop forwarding such spurious feedback messages programmatically without "knowing" whether the patch "exists" or not?
                # self.log_message(logging.DEBUG, f"{log_id}normal USER mode forwarding msg <{midi_bytes}>")
                self.__c_instance.send_midi(midi_bytes)  # all midi (Note and CC event messages)
        elif self.__user_mode_exit and self.__encoder_controller.last_assignment_mode() == C4M_USER:
            # self.log_message(logging.DEBUG, f"{log_id}(first user mode exit) note message: ({midi_bytes})")

            if is_note_on_msg and midi_bytes[1] == C4SID_LOCK and midi_bytes[2] == BUTTON_STATE_ON:
                # self.log_message(logging.DEBUG, f"{log_id}(first user mode exit) event passed - investigating LOCK button pressed event")
                pass
            elif is_note_off_msg and midi_bytes[1] == C4SID_LOCK:
                # self.log_message(logging.DEBUG, f"{log_id}(first user mode exit) event passed - eating LOCK Note OFF event")
                pass
            elif is_note_off_msg and midi_bytes[1] == C4SID_MARKER:
                # self.log_message(logging.DEBUG, f"{log_id}(first user mode exit) event handled - setting MARKER is released Note OFF event")
                self.set_marker_is_pressed(False)
            else:
                self.log_message(logging.WARNING, f"{log_id}(first user mode exit) event unhandled - dropping event message {midi_bytes}")
            # these button LEDs should be restored to "remote script" status display
            self.__encoder_controller.update_system_switch_leds()
            self.__user_mode_exit = False
            # self.log_message(logging.DEBUG, f"{log_id}(first user mode exit) Split, Lock, SpotErase LEDs OFF")
        else:
            # self.log_message(logging.DEBUG, f"{log_id}mode != C4M_USER")
            # in cases when the first midi_msg event after leaving USER mode is NOT a LOCK button event, clear the USER mode exit flag so this script
            # will handle LOCK button events normally.
            self.__user_mode_exit = False #
            is_cc_msg = midi_bytes[0] & 0xF0 == CC_STATUS
            # self.log_message(logging.DEBUG, f"{log_id}noteON<{is_note_on_msg}> noteOFF<{is_note_off_msg}> cc<{is_cc_msg}>")
            if is_note_on_msg:
                channel = midi_bytes[0] & 0x0F  # (& 0F preserves only channel related bits)
                note = midi_bytes[1]  # data1
                velocity = midi_bytes[2]  # data2
                # self.log_message(logging.DEBUG, f"{log_id}NOTE ON for note<{note}> velo<{velocity}>")
                # ignore Note ON events without 127 velocity
                handle_this_event = velocity == BUTTON_STATE_ON
                """   Any button on the C4 falls into this range G#-1 up to Eb 4 [00 - 3F] """
                if note in set(range(C4SID_FIRST, C4SID_LAST + 1)):
                    if note in modifier_switch_ids:  # Shift, Option, Alt, Control
                        self.__encoder_controller.handle_modifier_switch_ids(note, velocity)
                    elif handle_this_event:
                        # NOT in USER mode here and velocity == 127
                        if note in self.note_handling_dict:
                            if note in assignment_mode_switch_ids:
                                # True here: NOT in USER mode AND changing modes AND this script is still in control of USER mode display
                                # need to display something when Max sequencer patch is NOT connected and going into USER mode
                                # "this" display will get overwritten after the sequencer patch takes over (if connected)
                                self.__handling_assignment_switch = True
                            self.note_handling_dict[note](note)
                            self.__handling_assignment_switch = False
                        else:
                            if note == 4:  # Spot/Erase buttons is not mapped to any remote script behavior
                                # self.log_message(logging.INFO, f"{log_id}Spot/Erase button is not mapped to any handling behavior")
                                pass
                            else:
                                self.log_message(logging.ERROR, f"{log_id}unhandled note value: {note}")

                    if note == C4SID_MARKER:
                        # This "note ON event" entered receive_midi() while the script was NOT in USER mode, because this line is under else:
                        # now the script IS in USER mode, because self.__note_handling_dict[note](note) and note == C4SID_MARKER:
                        # but the Max patch is still NOT-processing yet, forward this midi event to the C4 display
                        # self.log_message(logging.DEBUG, f"{log_id}before leaving script control, turning MARKER led OFF <{(NOTE_ON_STATUS, note, BUTTON_STATE_OFF)}>")
                        self.__c_instance.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))
                        # (just-before-going-into-user-mode) MARKER LED is now OFF (would normally be ON indicating USER mode)
                        # send START signal for patch to process
                        # self.log_message(logging.DEBUG, f"{log_id}sending 'button 22' signal toggling Max bypass mode, START processing STOP bypassing")
                        self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MAX_BYPASS_ID, BUTTON_STATE_ON))
                        self.set_marker_is_pressed(False)  # in case LOCK button is pressed by itself in USER mode, don't exit USER mode

                        # self.log_message(logging.DEBUG, f"{log_id}script now in USER mode, Max patch is in control")
                        # MARKER Press+Release events created for the patch to "restore" the USER mode patch's MARKER button LED ON/OFF status
                        # One Press+Release event toggles the LED ON/OFF, Two (quick) Press+Release events mean the LED ON/OFF state "doesn't change"
                        self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_ON))
                        self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_OFF))
                        # (when the human physically releases the C4 MARKER button after switching to USER mode, the event is processed by the patch instead of this script)
                        # MARKER Press event created for the patch to prepare for the (spurious) "first MARKER release" event the patch will see and process in USER mode
                        # The "human release" always happens going into user mode, always need to "pre press" here
                        self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_ON))
            elif is_cc_msg:
                """The only CC messages arriving here we care about are from some "unmapped" encoders, which is why this code doesn't check for "C4M_PLUGIN" mode.
                   All "C4M_PLUGIN" (Track-Device) mode encoders could be mapped, so their midi messages are not handled by the remote script, (those messages 
                   are either already handled automatically by Live or from (temporarily) unmapped encoders"""
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]

                if self.__encoder_controller.assignment_mode() == C4M_FUNCTION:
                    self.__encoder_controller.handle_vpot_rotation(cc_no, cc_value)
                elif self.__encoder_controller.assignment_mode() == C4M_CHANNEL_STRIP:
                    self.__encoder_controller.handle_vpot_rotation(cc_no, cc_value)

            elif is_note_off_msg:  # an actual Note Off event: is_note_off_msg = midi_bytes[0] & 0xF0 == NOTE_OFF_STATUS
                # self.log_message(logging.DEBUG, f"{log_id}unhandled - passing (ignoring) note off event {midi_bytes}")
                # this pass is expected, the C4 sends Note ON with velocity 0 for Note OFF.
                # Live generates Note Offs the script can ignore here (not USER mode) because USER Mode has already processed above as needed
                # self.log_message(logging.DEBUG, f"{log_id}NOT in USER mode MARKER is released, passing (NOTE OFF event)")
                self.set_marker_is_pressed(False)
                pass
            elif midi_bytes[0] == 0xF0:
                # this sysex is from the C4, it is the unit serial number in response to a sysex request (reset from Live?)
                #                                          Z   T   1   0   4   7   3   A   3  ACK  <-- (specifically C4Pro serials start with ZT)
                #                  240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 65, 51,   6, 0, 247
                #                                          Z   T   1   0   4   7   3    y DLE ACK
                c4InitWelcome = [240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 121, 16, 6, 0, 247]
                c4WelcomeHeader = [240, 0, 0, 102, 23, 1]
                c4WelcomeTail = [6, 0, 247]
                lgth = len(c4InitWelcome)
                hdr_lgth = len(c4WelcomeHeader)
                trl_lgth = len(c4WelcomeTail)
                if lgth == len(midi_bytes):
                    match = True
                    for i in range(hdr_lgth):  # first chunk always the same, middle chunk varies with serial numbers
                        if c4InitWelcome[i] != midi_bytes[i]:
                            match = False
                    for j in range(lgth - trl_lgth, lgth):  # last chunk always the same
                        if c4InitWelcome[j] != midi_bytes[j]:
                            match = False
                    if match:
                        # the C4 just blanked its displays (except the hello message on the top screen?)
                        # assignment mode is never USER here, msg was passed above in USER mode
                        self.log_message(logging.INFO,f"{log_id}attempting to update display after receiving C4 serial number sysex message {midi_bytes}")
                        self.__encoder_controller.one_delayed_display_update(0.49, force=True)  # how about now?
                        self.__encoder_controller.update_assignment_mode_leds()
                        self.__encoder_controller.update_system_switch_leds()
                    else:
                        self.log_message(logging.WARNING,f"{log_id}unhandled matching length - sysex event dropped {midi_bytes}")
                else:
                    self.log_message(logging.WARNING,f"{log_id}unhandled non-matching length - sysex event dropped {midi_bytes}")
            else:
                self.log_message(logging.WARNING,f"{log_id}unhandled - sysex event dropped {midi_bytes}")

    def handle_jog_wheel_rotation(self, cc_value):  # aka beat_pointer
        """use one vpot encoder to simulate a jog wheel rotation, with acceleration """
        if cc_value >= 64:
            self.song().jump_by(-(cc_value - 64))
        if cc_value < 64:
            self.song().jump_by(cc_value)

    def set_loop_length(self, cc_value):
        """use one vpot encoder to set the loop length in Arrange mode """
        if cc_value >= 64:
            self.song().loop_length = clamp(self.song().loop_length - (4 * (cc_value - 64)), 4, 10000)
        if cc_value <= 64:
            self.song().loop_length = (self.song().loop_length + (clamp(4 * (cc_value), 4, 10000)))

    def set_loop_start(self, cc_value):
        """use one vpot encoder to set the loop start point in Arrange mode """
        if cc_value >= 64:
            self.song().loop_start = clamp(self.song().loop_start - (cc_value - 64), 0, 10000)
        if cc_value <= 64:
            self.song().loop_start = (self.song().loop_start + (clamp((cc_value), 1, 10000)))

    def zoom_or_scroll(self, cc_value):
        """ Scroll in Session view or Zoom in Arrange view with vpot_rotation encoder rotation"""
        nav = Live.Application.Application.View.NavDirection
        if cc_value >= 64:
            self.application().view.zoom_view(nav.left, '', self.alt_is_pressed())
        if cc_value <= 64:
            self.application().view.zoom_view(nav.right, '', self.alt_is_pressed())

    def scrub_clip(self, cc_value):
        clip = self.song().view.detail_clip
        if clip:
            if cc_value >= 64:
                clip.scrub(8*(-(cc_value - 64)))
            if cc_value <= 64:
                clip.scrub(8*(cc_value))

    def scroll_clip(self, cc_value):  # todo WIP
        log_id = "C4.scroll_clip: "
        nav = Live.Application.Application.View.NavDirection
        app_view = self.application().view
        view_name = 'Detail/DeviceChain'
        self.log_message(logging.DEBUG,f'{log_id}called with cc_value: {cc_value}')
        clip = self.song().view.detail_clip

        scroll = cc_value == 1 and 3 or 2
        self.log_message(logging.DEBUG,f'{log_id}called with cc_value: {cc_value}')

        if cc_value > 64:
            if not self.application().view.is_view_visible(view_name):
                self.application().view.focus_view(view_name)
                self.log_message(logging.DEBUG,f'{log_id}Focusing view to {view_name}')
                # clip.move_playing_pos(- cc_value)
                app_view.scroll_view(nav.left, view_name, False)
        if cc_value <= 64:
            if not self.application().view.is_view_visible(view_name):
                self.application().view.focus_view(view_name)
                app_view.scroll_view(nav.right, view_name, False)

    def zoom_clip(self, cc_value):
        log_id = "C4.zoom_clip: "
        nav = Live.Application.Application.View.NavDirection
        app_view = self.application().view
        view_name = 'Detail/Clip'
        self.log_message(logging.DEBUG,f'{log_id}called with cc_value: {cc_value}')

        # scroll = cc_value == 65 and 3 or 1
        if cc_value > 64:
            if not app_view.is_view_visible(view_name):
                self.log_message(logging.DEBUG,f'{log_id}Focusing view {view_name}')
                app_view.focus_view(view_name)
                app_view.zoom_view(nav.left, view_name, False)
                self.log_message(logging.DEBUG,f'{log_id}Zooming view to the left')
        if cc_value < 64:
            if not app_view.is_view_visible(view_name):
                self.log_message(logging.DEBUG,f'{log_id}Focusing view {view_name}')
                app_view.focus_view(view_name)
                app_view.zoom_view(nav.right, view_name, False)
                self.log_message(logging.DEBUG,f'{log_id}Zooming view to the right')

    def tempo_change(self, cc_value):  # BPM
        """Sets the current song tempo"""
        if self.ctrl_is_pressed():
            multiplier = 16
        elif self.shift_is_pressed():
            multiplier = 0.25
        else:
            multiplier = 1

        if cc_value >= 64:
            amount = -((cc_value - 64) / 4 * multiplier)
        else:
            amount = (cc_value / 4 * multiplier)

        tempo = max(20, min(999, self.song().tempo + amount))
        self.song().tempo = tempo

    def can_lock_to_devices(self):  # todo: make use of it, locking itself works
        """Live -> Script
            Should return True, if the ControlSurface can lock a device.
            "SimpleControlSurface" does not support controlling devices, so it will always be False."""
        return True

    def suggest_input_port(self):
        """Live -> Script   Live can ask the script for an input port name to find a suitable one.    """
        return 'Mackie C4'

    def suggest_output_port(self):
        """Live -> Script        Live can ask the script for an output port name to find a suitable one.        """
        return 'Mackie C4'

    def shift_is_pressed(self):
        return self.__shift_is_pressed

    def set_shift_is_pressed(self, pressed):
        self.__shift_is_pressed = pressed

    def option_is_pressed(self):
        return self.__option_is_pressed

    def set_option_is_pressed(self, pressed):
        self.__option_is_pressed = pressed

    def ctrl_is_pressed(self):
        return self.__ctrl_is_pressed

    def set_ctrl_is_pressed(self, pressed):
        self.__ctrl_is_pressed = pressed

    def alt_is_pressed(self):
        return self.__alt_is_pressed

    def set_alt_is_pressed(self, pressed):
        self.__alt_is_pressed = pressed

    def marker_is_pressed(self):
        return self.__marker_is_pressed

    def set_marker_is_pressed(self, pressed):
        self.__marker_is_pressed = pressed

    def application(self):
        """returns a reference to the application that we are running in"""
        return Live.Application.get_application()

    def song(self):
        """returns a reference to the Live Song that we do interact with"""
        return self.__c_instance.song()

    def handle(self):
        """returns a handle to the c_interface that is needed when forwarding MIDI events via the MIDI map"""
        return self.__c_instance.handle()

    def trBlock(self, trackOffset, blocksize):
        tracks = self.song().visible_tracks
        block = [
            str(tracks[trackOffset + track_index].name)
            if len(tracks) > trackOffset + track_index
            else 'fake Track NAME'
            for track_index in range(0, blocksize)
        ]
        return block

    def disconnect(self):
        """Live -> Script        Called right before we get disconnected from Live.
        Is called by Live when the script is unloaded. This happens when the script gets unselected from the preferences,
        automatically when the corresponding MIDI ports are gone or Live is shut down. All listeners to the Live API need
        to be removed. Cyclic dependencies should be broken, so the control surface can be garbage collected."""
        self.destroy_mixer_listeners()  # rem_mixer_listeners()
        self.rem_scene_listeners()
        self.rem_overdub_listener()
        self.rem_tracks_listener()
        self.remove_device_listeners()  # rem_device_listeners()
        self.rem_transport_listener()
        if self.song().visible_tracks_has_listener(self.tracks_change):
            self.song().remove_visible_tracks_listener(self.tracks_change)
        for c in self.__components:
            c.destroy()

    def register_component(self, component):
        self.__components.append(component)
        component.canonical_parent = self

    def suggest_map_mode(self, cc_no, channel=0):
        """  Live -> Script   Live can ask the script for a suitable mapping mode for a given CC.    """

        result = Live.MidiMap.MapMode.absolute

        if cc_no in encoder_range:
            result = Live.MidiMap.MapMode.relative_signed_bit
        return result

    def refresh_state(self):
        """Live -> Script
        Send out MIDI to completely update the attached MIDI controller. Will be called when requested by the user,
        after for example having reconnecting the MIDI cables or when exiting MIDI map mode
        """
        self.set_mixer_listeners()  # add_mixer_listeners()
        self.add_overdub_listener()
        self.add_tracks_listener()
        self.add_device_listeners()
        self.add_transport_listener()
        self.add_scene_listeners()

        self.trBlock(0, len(self.song().visible_tracks))

    def add_scene_listeners(self):
        # try-except blocks handle the cases when the song-view-listener callback method self.scene_change, for example, is already present. This reduces 
        # the number of function calls at the expense of using exception handling semantics for relatively normal program event handling.
        try:
            self.song().view.add_selected_scene_listener(self.scene_change)
        except RuntimeError:
            pass

        try:
            self.song().view.add_selected_track_listener(self.track_change)
        except RuntimeError:
            pass

    def rem_scene_listeners(self):
        # try-except blocks handle the cases when the song-view-listener (callback method self.scene_change, for example) is already not present. 
        try:
            self.song().view.remove_selected_scene_listener(self.scene_change)
        except RuntimeError:
            pass

        try:
            self.song().view.remove_selected_track_listener(self.track_change)
        except RuntimeError:
            pass

    def track_change(self):
        log_id = "C4.track_change: "
        selected_track_index, selected_track_callback_type = self.find_selected_track_index()
        self.log_message(logging.DEBUG, f"{log_id}calling track_changed passing index {selected_track_index} only")
        self.__encoder_controller.track_changed(selected_track_index)
        # self.request_rebuild_midi_map()  <--- called by EC

    def find_changed_track_callback_type(self):
        log_id = "C4.find_changed_track_callback_type: "
        """ depending on the arrangement of tracks you can see on the screen in Live, a 'tracks listener' event's callback_type 'location' might not be the same 'location'
            as the selected track's callback_type location.  For example, an unfolded group track with 2 instruments and 2 audio tracks make 5 plain callback type 0 tracks,
            plus 2 callback type 1 return tracks (and callback type 2 master) result in 7 'song track indexes (plus master). If the first return track is selected
            in this arrangement, it will have selected track index 5.  When a mouse click closes the Group track in this arrangement, the selected return track
            doesn't change, but its index does, the updated first return track index is 3, but that updated index is in the wrong callback_type 'location' and
            the EAH.SongData 'database' gets corrupted.  This method returns the change's correct callback_type 'location' so the 'database' won't get corrupted """
        found_changed_track_callback_type = 2
        callback_type_track_count = 1
        next_type_counts = {0: len(self.song().visible_tracks), 1: len(self.song().return_tracks), 2: 1}
        msg = f"{log_id}"
        # for i in next_type_counts.keys():
        #     msg += f"type {i}: old count {self.callback_type_track_counts[i]} new count {next_type_counts[i]}"
        #     self.log_message(logging.DEBUG, msg)
        #     msg = f"{log_id}"

        if self.callback_type_track_counts[0] < next_type_counts[0] and self.callback_type_track_counts[1] == next_type_counts[1]:
            # less plain type 0 tracks and same return type 1 tracks
            found_changed_track_callback_type = 0
            callback_type_track_count = next_type_counts[0]
        elif self.callback_type_track_counts[0] > next_type_counts[0] and self.callback_type_track_counts[1] == next_type_counts[1]:
            # more plain type 0 tracks and same return type 1 tracks
            found_changed_track_callback_type = 0
            callback_type_track_count = next_type_counts[0]
        elif self.callback_type_track_counts[0] == next_type_counts[0] and self.callback_type_track_counts[1] < next_type_counts[1]:
            # same plain type 0 tracks and less return type 1 tracks
            found_changed_track_callback_type = 1
            callback_type_track_count = next_type_counts[1]
        elif self.callback_type_track_counts[0] == next_type_counts[0] and self.callback_type_track_counts[1] > next_type_counts[1]:
            # same plain type 0 tracks and more return type 1 tracks
            found_changed_track_callback_type = 1
            callback_type_track_count = next_type_counts[1]

        # msg = f"{log_id} returning found values ({found_changed_track_callback_type}, {callback_type_track_count})"
        # self.log_message(logging.DEBUG, msg)
        return found_changed_track_callback_type, callback_type_track_count

    def update_callback_type_track_counts(self):
        self.callback_type_track_counts[0] = int(len(self.song().visible_tracks))
        self.callback_type_track_counts[1] = int(len(self.song().return_tracks))

    def find_selected_track_index(self):
        log_id = "C4.find_selected_track_index: "
        # need to do 3 things:
        # - determine the 'song tracks index' of Live's selected track
        # - assign the last_selected_track_index property the determined 'selected Track Index' value
        # - return the new 'song index' value and the 'callback type' of the (visible_tracks or return_tracks) list containing the selected track
        selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks
        nbr_song_tracks = len(tracks)

        selected_index = 0
        found = selected_track in tracks

        for i, track in enumerate(tracks):
            if track == selected_track:
                selected_index = i
                found = True
                break

        if not found:
            if selected_track == self.song().master_track:
                # tracks = self.song().visible_tracks + self.song().return_tracks
                # this script stores master track info "one past" the tracks above
                selected_index = nbr_song_tracks
            else:
                # signal that something bad happened - selected track
                self.log_message(logging.ERROR,f"{log_id}setting selected index to a bad value {selected_index}")
                selected_index = 555

        if selected_index != self.last_selected_track_index:
            self.log_message(logging.DEBUG,f"{log_id}setting self.last_selected_track_index {self.last_selected_track_index} to found index {selected_index}")
            self.last_selected_track_index = selected_index
            self.last_selected_track_callback_type = 2
            if selected_index < len(self.song().visible_tracks):
                self.last_selected_track_callback_type = 0
            elif selected_index < nbr_song_tracks:
                self.last_selected_track_callback_type = 1
        return self.last_selected_track_index, self.last_selected_track_callback_type

    @property
    def last_selected_track_index(self):
        return self._selected_track_index

    @last_selected_track_index.setter
    def last_selected_track_index(self, next_index):
        self._selected_track_index = next_index

    @property
    def last_selected_track_callback_type(self):
        return self._selected_track_callback_type

    @last_selected_track_callback_type.setter
    def last_selected_track_callback_type(self, cb_type):
        self._selected_track_callback_type = cb_type

    def scene_change(self): 
        selected_scene = self.song().view.selected_scene
        scenes = self.song().scenes
        index = 0
        selected_index = 0
        for scene in scenes:
            index = index + 1
            if scene == selected_scene:
                selected_index = index

        if selected_index != self.scene_index:
            self.scene_index = selected_index

    def add_transport_listener(self):
        # try-except blocks handle the cases when the song.is_playing_listener callback method self.transport_change is already present.
        try:
            self.song().add_is_playing_listener(self.transport_change)
        except RuntimeError:
            pass

    def rem_transport_listener(self):
        # try-except blocks handle the cases when the song.is_playing_listener callback method self.transport_change is already not present.
        try:
            self.song().remove_is_playing_listener(self.transport_change)
        except RuntimeError:
            pass

    def transport_change(self):
        pass

    def add_overdub_listener(self):
        try:
            self.song().add_overdub_listener(self.overdub_change)
        except RuntimeError:
            pass

    def rem_overdub_listener(self):
        try:
            self.song().remove_overdub_listener(self.overdub_change)
        except RuntimeError:
            pass

    def overdub_change(self):
        return Live.Song.Song.overdub

    def add_tracks_listener(self):
        try:
            self.song().add_tracks_listener(self.tracks_change)
        except RuntimeError:
            pass

    def rem_tracks_listener(self):
        try:
            self.song().remove_tracks_listener(self.tracks_change)
        except RuntimeError:
            pass

    def tracks_change(self):
        self.__processing_track_state_change = True
        log_id = "C4.tracks_change: "

        selected_index, callback_track_type_of_selected_index = self.find_selected_track_index()
        found_changed_track_callback_type, found_callback_type_track_count = self.find_changed_track_callback_type()
        dtls = f"(selected_index={selected_index}, callback_track_type_of_selected_index={callback_track_type_of_selected_index}, "
        found_type = '2 (master - always 1 track)'
        if found_changed_track_callback_type == 1:
            found_type = "1 (return)"
        elif found_changed_track_callback_type == 0:
            found_type = "0 (visible)"
        dtls += f"found_cb_type={found_type}, found_cb_type_track_count={found_callback_type_track_count})"
        tracks = self.song().visible_tracks + self.song().return_tracks
        msg = f"{log_id}callback event with {len(self.song().visible_tracks)} + {len(self.song().return_tracks)} = {len(tracks)} visible and return tracks in song "
        self.log_message(logging.DEBUG, msg)
        self.log_message(logging.DEBUG, dtls)
        new_track_count = len(tracks)

        if callback_track_type_of_selected_index == found_changed_track_callback_type:
            if self.track_count > new_track_count:
                if self.track_count - new_track_count > 1:
                    tracks_removed = self.track_count - new_track_count
                    if callback_track_type_of_selected_index == 1:
                        tracks = self.song().return_tracks
                    msg = f"{log_id}calling ec.tracks_deleted(index={selected_index}, cbt_track_count({len(tracks)}), track_type={callback_track_type_of_selected_index}"
                    self.log_message(logging.DEBUG, msg)
                    self.__encoder_controller.tracks_deleted(selected_index, tracks, callback_track_type_of_selected_index)
                else:
                    self.log_message(logging.DEBUG,f"{log_id}calling track_deleted passing index {selected_index} only")
                    self.__encoder_controller.track_deleted(selected_index)
                #self.request_rebuild_midi_map()   <-- called by EC
            elif self.track_count < new_track_count:
                if new_track_count - self.track_count > 1:
                    if callback_track_type_of_selected_index == 1:
                        tracks = self.song().return_tracks
                    msg = f"{log_id}calling ec.tracks_added(index={selected_index}, cbt_tracks=({len(tracks)} tracks), cb_type={callback_track_type_of_selected_index}"
                    self.log_message(logging.DEBUG, msg)
                    self.__encoder_controller.tracks_added(selected_index, tracks, callback_track_type_of_selected_index)
                else:
                    self.log_message(logging.DEBUG,f"{log_id}calling track_added passing index {selected_index} only")
                    self.__encoder_controller.track_added(selected_index)
                #self.request_rebuild_midi_map() <-- called by EC
            else:
                self.log_message(logging.DEBUG,f"{log_id}calling EC.track_changed passing index {selected_index}")
                # since track counts match, something else in the callback_track_type collection of the selected_index's Track changed
                self.__encoder_controller.track_changed(selected_index)
        else:
            # still need to add or remove from correct track collection in EAH.SongData, but the current Song selected index points to the wrong
            # track collection in SongData, so special handling for this situation

            if found_changed_track_callback_type == 0 and found_callback_type_track_count > self.callback_type_track_counts[0]: # old len(self.song().visible_tracks):
                msg = f"{log_id}calling ec.unselected_tracks_added{dtls}"
                self.log_message(logging.DEBUG, msg)
                self.__encoder_controller.unselected_tracks_added(found_changed_track_callback_type, found_callback_type_track_count)
            elif found_changed_track_callback_type == 0 and found_callback_type_track_count < self.callback_type_track_counts[0]: # old len(self.song().visible_tracks):
                msg = f"{log_id}calling ec.unselected_tracks_deleted{dtls}"
                self.log_message(logging.DEBUG, msg)
                self.__encoder_controller.unselected_tracks_deleted(found_changed_track_callback_type, found_callback_type_track_count)
            elif found_changed_track_callback_type == 1 and found_callback_type_track_count > self.callback_type_track_counts[1]: # old len(self.song().return_tracks):
                msg = f"{log_id}calling ec.unselected_tracks_added{dtls}"
                self.log_message(logging.DEBUG, msg)
                self.__encoder_controller.unselected_tracks_added(found_changed_track_callback_type, found_callback_type_track_count)
            elif found_changed_track_callback_type == 1 and found_callback_type_track_count < self.callback_type_track_counts[1]: # old len(self.song().return_tracks):
                msg = f"{log_id}calling ec.unselected_tracks_deleted{dtls}"
                self.log_message(logging.DEBUG, msg)
                self.__encoder_controller.unselected_tracks_deleted(found_changed_track_callback_type, found_callback_type_track_count)
            else: # different 'selected index' and 'event index' callback track types were detected, but no telltale track-type count differences
                # landed here when two tracks were selected at the same time (shift + left-click) then Ctrl-G grouped (Group Track was added, processed above)
                # future new-track(s)-in-group events should be ignored here in tracks_changed()
                # in favor of new-track-added-and-selected event processing by track_changed(index)
                # also landed here when a track was added (Ctrl+Shift+T) "next to" the selected track inside a Group because (I think)
                # the first event was "new track added in visible tracks" (processed above) and the second event was new-track-in-group (landed here)
                # also safe to ignore here in tracks_changed()
                msg = f"{log_id} logic issue? passing on this event {dtls}"  # continuing to log in case of other triggers
                self.log_message(logging.ERROR, msg)
                # self.__encoder_controller.unselected_tracks_changed(found_changed_track_callback_type, found_callback_type_track_count)

        self.update_callback_type_track_counts()
        self.track_count = new_track_count
        self.__processing_track_state_change = False

    def processing_track_state_change(self):
        return self.__processing_track_state_change

    def processing_track_device_state_change(self):
        return self.__processing_track_device_state_change

    def selected_device_change_state(self, track, tid, type):
        # this was the only listener that popped when the index of the selected device changed (order of devices changed in device list)
        log_id = "C4.selected_device_change_state: "
        self.log_message(logging.DEBUG, f"{log_id}passing on selected device change-state listener for {track.name} with callback type {type} at type index {tid} event")
        # self.__processing_track_device_state_change = True
        # self.log_message(logging.DEBUG, f"{log_id}processing device list drag&drop on script's selected track")
        # self.__encoder_controller.device_list_changed(track, tid, type)
        # self.__processing_track_device_state_change = False
        # if self.last_selected_track_index == tid:
        #     self.log_message(logging.DEBUG, f"{log_id}processing device change on script's selected track")
        #     self.__processing_track_device_state_change = True
        #      # whatever track has the selected device
        #     self.__processing_track_device_state_change = False
        # else:
        #     self.log_message(logging.DEBUG, f"{log_id}ignoring device change because {tid} is not the script's selected track index {self.last_selected_track_index}")

    def device_changestate(self, track, tid, type):
        log_id = "C4.device_changestate: "
        self.log_message(logging.DEBUG, f"{log_id}device listener for {track.name} at index {tid} with type {type} popped")
        if self.last_selected_track_index == tid:
            self.log_message(logging.DEBUG, f"{log_id}processing device change on script's selected track")
            self.__processing_track_device_state_change = True
            self.__encoder_controller.device_added_deleted_or_changed(track, tid, type)
            self.__processing_track_device_state_change = False
        else:
            self.log_message(logging.DEBUG, f"{log_id}ignoring device change because {tid} is not the script's selected track index {self.last_selected_track_index}")
        # if type == 2:
        #     pass
        # elif type == 1:
        #     pass

    def param_changestate(self, param, tid, did, pid, type):
        log_id = "C4.param_changestate: "
        self.log_message(logging.DEBUG, f"{log_id}parameter change state listener for {param.name} popped")

        msg = f"{log_id} cb type {type} track index {tid} device at device chain index {did} parameter at parameter list index {pid} "
        self.log_message(logging.DEBUG, msg + f"{param.name} changed state to value {param.value}")
        self.__encoder_controller.on_param_state_change(param, tid, did, pid, type)
        self.__device_provider.set_last_param_value_change_details(param, tid, did, pid)
        # if type == 2:
        #     pass
        # elif type == 1:
        #     pass

    def devpm_change(self, device):
        log_id = "C4.devpm_change: "
        self.log_message(logging.DEBUG, f"{log_id}parameters listener for {device.name} popped, refreshing encoder controller state")
        self.__encoder_controller.refresh_state()

    def mixerv_changestate(self, type, tid, track, r=0):
        cmd = f"track.mixer_device.{type}.value"
        val = eval(cmd)
        types = {'panning': 'pan', 'volume': 'volume', 'crossfader': 'crossfader'}
        if r == 2:
            pass
        elif r == 1:
            pass

    def mixert_changestate(self, type, tid, track, r=0):
        cmd = f"track.{type}"
        val = eval(cmd)
        if r == 1:
            pass

    def send_changestate(self, tid, track, sid, send, r=0):
        val = send.value
        if r == 1:
            pass

    def trname_changestate(self, tid, track, r=0):
        if r == 1:
            pass
        else:
            self.trBlock(0, len(self.song().visible_tracks))

    def on_is_frozen_changed(self):
        if not self.__encoder_controller.assignment_mode() == C4M_USER: # only one way to exit user mode (Marker + Lock buttons)
            # switch script to Track Channel Strip mode if not already
            self.__encoder_controller.handle_assignment_switch_ids(C4SID_CHANNEL_STRIP)


    def track_inc_dec(self, note):
        log_id = "C4.track_inc_dec: "
        old_selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks

        if old_selected_track == self.song().master_track:
            if note == C4SID_TRACK_LEFT:
                new_selected_index = len(tracks) - 1
                self.song().view.selected_track = tracks[new_selected_index]
            else: # can't move right of master track
                new_selected_index = len(tracks) # still master
        else:
            old_selected_index = tracks.index(old_selected_track)
            self.log_message(logging.DEBUG,f"{log_id}before processing, song track {old_selected_track.name} at index {old_selected_index} is selected")
            new_selected_index = old_selected_index
            for index, track in enumerate(tracks):
                if track == old_selected_track:
                    if note == C4SID_TRACK_LEFT and index > 0:
                        new_selected_index = index - 1
                    elif note == C4SID_TRACK_RIGHT and index < len(tracks) - 1:
                        new_selected_index = index + 1
                    elif note == C4SID_TRACK_RIGHT and index == len(tracks) - 1:
                        self.song().view.selected_track = self.song().master_track
                        return  # Return early since the master track has been selected

            if 0 <= new_selected_index < len(tracks):
                self.song().view.selected_track = tracks[new_selected_index]

        self.log_message(logging.DEBUG,f"{log_id}after processing, song track {self.song().view.selected_track.name} at index {new_selected_index} is selected")

    def get_is_locked_to_device(self):
        return self.__surface_is_locked

    def set_is_locked_to_device(self, is_locked):
        self.__surface_is_locked = is_locked


    def lock_surface_to_device(self, device):
        log_id = "C4.lock_surface: "
        if not self.__surface_is_locked:
            self.log_message(logging.INFO,f"{log_id}locking surface to device {device.name}, led state to ON")
            self.__device_provider.lock_to_device(device)
        else:
            dev = "None"
            if self.__device_provider.provided_device is not None:
                dev = self.__device_provider.provided_device.name
            self.log_message(logging.INFO,f"{log_id}surface already locked to {dev}, led state stays ON")

        self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_ON))

    def unlock_surface_from_device(self):
        log_id = "C4.unlock_surface: "
        if self.__surface_is_locked:
            self.log_message(logging.INFO,f"{log_id}unlocking surface from device {self.__device_provider.provided_device.name}, led state to OFF")
            self.__device_provider.unlock_from_device()
        else:
            self.log_message(logging.INFO,f"{log_id}surface already unlocked, led state stays OFF")

        self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_OFF))

    def log_message(self, level=script_log_levels["ERROR"], *message):
        """ Overrides standard to use logger instead of c_instance. """
        if self.current_script_log_level <= level:
            try:
                message = f'{" ".join(map(str, message))}'
                logger.info(message)
            except:
                logger.info('Logging encountered illegal character(s)!')

    @staticmethod
    def get_logger():
        """ Returns this script's logger object. """
        return logger

    def show_message(self, message):
        """ Displays the given message in Live's status bar """
        self.__c_instance.show_message(message)
