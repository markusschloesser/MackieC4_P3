# was Python bytecode 2.5 (62131)
# Compiled at: 2011-01-22 04:38:37

"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
# MS: not sure this applies anymore ;-)
#
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

This script is based off the Ableton Live supplied MIDI Remote Scripts.

This is the second file that is loaded, by way of being instantiated through __init__.py
"""

from __future__ import absolute_import, print_function, unicode_literals
import sys
import Live
from ableton.v2.base import liveobj_valid, clamp
from .TimeDisplay import TimeDisplay
from . import song_util
import logging
import time
from .consts import *
from .Encoders import Encoders
from .EncoderController import EncoderController

if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object


logger = logging.getLogger(__name__)


class MackieC4(object):
    """  Main class that establishes the MackieC4 Component
         --- although technically, the Mackie Control C4Pro is an "extension" of the Mackie Control itself (like the MackieControlXT), this script stands alone.
             It doesn't work 'with' those Midi Remote Scripts which is why is_extension() returns False from here
       Main class that establishes the Mackie Control <-> Live interaction. It acts as a container/manager for all the
       Mackie C4 subcomponents like Encoders, Displays and so on.
       Further it is glued to Lives MidiRemoteScript C instance, which will forward some notifications to us,
       and lets us forward some requests that are needed beside the general Live API (see 'send_midi' or 'request_rebuild_midi_map').
    """
    __module__ = __name__
    prlisten = {}
    '''prlisten is "Parameter Range" Listener?'''

    plisten = {}
    '''plisten is "Parameter" Listener?"'''

    dlisten = {}
    '''dlisten is "Device Listener'''

    mlisten = {'solo': {}, 'mute': {}, 'arm': {}, 'current_monitoring_state': {}, 'panning': {}, 'volume': {}, 'sends': {}, 'name': {}, 'available_input_routing_channels': {}, 'available_input_routing_types': {}, 'available_output_routing_channels': {}, 'available_output_routing_types': {}, 'input_routing_type': {}, 'input_routing_channel': {}, 'output_routing_channel': {}, 'output_routing_type': {}}
    '''mlisten is Mixer Listener'''

    rlisten = {'solo': {}, 'mute': {}, 'panning': {}, 'volume': {}, 'sends': {}, 'name': {}, 'available_output_routing_channels': {}, 'available_output_routing_types': {}, 'output_routing_channel': {}, 'output_routing_type': {}}
    '''rlisten is "Returns" Listener '''

    masterlisten = {'panning': {}, 'volume': {}, 'crossfader': {}}

    scene = 0
    track_index = 0
    track_count = 0
    surface_is_locked = 0
    rebuild_my_database = 0
    return_resetter = 0
    init_ready = False

    def __init__(self, c_instance):

        self.__c_instance = c_instance

        # initialize the 32 encoders, their EncoderController and add them as __components here
        self.__encoders = [Encoders(self, i) for i in encoder_range]
        self.__encoder_controller = EncoderController(self, self.__encoders)
        self.__components = [self.__encoders[i] for i in encoder_range]
        self.__components.append(self.__encoder_controller)


        tracks = self.song().visible_tracks + self.song().return_tracks
        index = 0

        # assign track to the local index of the matching selected track in Live
        for track in tracks:
            if track == self.song().view.selected_track:
                self.track_index = index
            index = index + 1

        self.track_count = len(tracks)

        # if refresh_state is not already listening for visible tracks view changes
        if self.song().visible_tracks_has_listener(self.tracks_change) != 1:
            self.song().add_visible_tracks_listener(self.tracks_change)

        # To display song position pointer or beats on display
        self.__time_display = TimeDisplay(self)
        self.__components.append(self.__time_display)

        self.__shift_is_pressed = False
        self.__option_is_pressed = False
        self.__ctrl_is_pressed = False
        self.__alt_is_pressed = False
        self.__marker_is_pressed = False
        self.__user_mode_exit = False

        self.__note_handling_dict = {C4SID_LOCK: lambda _: self.lock_surface() }
        for note in range(system_switch_ids[0], track_nav_switch_ids[-1] + 1): # range(0, 21) notes 0 - 20
            # self.log_message("MC.__init__: adding note {} to __note_handling_dict".format(note))
            if note in track_nav_switch_ids:
                self.__note_handling_dict.update({note: self.track_inc_dec})
            elif note in bank_switch_ids or note in single_switch_ids:
                self.__note_handling_dict.update({note: self.__encoder_controller.handle_bank_switch_ids})
            elif note in slot_nav_switch_ids:
                self.__note_handling_dict.update({note: self.__encoder_controller.handle_slot_nav_switch_ids})
            elif note in assignment_mode_switch_ids:
                self.__note_handling_dict.update({note: self.__encoder_controller.handle_assignment_switch_ids})
        for note in encoder_switch_ids: # encoder button ids 32 - 63
            self.__note_handling_dict.update({note: self.__encoder_controller.handle_pressed_v_pot})

        self.init_ready = True

        # turn off FUNCTION and ASSIGNMENT button LEDs except the default
        # self.log_message("MC.__init__: self.__init__ firing")
        for cc in range(C4SID_SPLIT, C4SID_FUNCTION + 1):
            if cc == C4SID_CHANNEL_STRIP:
                # self.log_message("MC.__init__: {}".format((NOTE_ON_STATUS, cc, BUTTON_STATE_ON)))
                self.send_midi((NOTE_ON_STATUS, cc, BUTTON_STATE_ON))
            else:
                # self.log_message("MC.__init__: {}".format((NOTE_ON_STATUS, cc, BUTTON_STATE_OFF)))
                self.send_midi((NOTE_ON_STATUS, cc, BUTTON_STATE_OFF))


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
        if self.init_ready:
            # self.log_message("MC.request_rebuild_midi_map: firing")
            self.__c_instance.request_rebuild_midi_map()

    def update_display(self):
        """
        Aka on_timer. Called every 100 ms and should be used to update display relevant parts of the controller.
        """
        # pass
        if self.init_ready and self.__encoder_controller.assignment_mode() != C4M_USER:
            # self.log_message("MC.update_display: firing")  # every 100 ms verbose log message
            for c in self.__components:
                c.on_update_display_timer()

    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices that this script is assigned to.
        """
        if self.init_ready and self.__encoder_controller.assignment_mode() != C4M_USER:
            # self.log_message("MC.send_midi: firing")  # very verbose log message
            self.__c_instance.send_midi(midi_event_bytes)

    def build_midi_map(self, midi_map_handle):
        """Live -> Script        Build DeviceParameter mappings, that are processed in Audio time, or forward MIDI messages
        explicitly to our receive_midi_functions. Which means that when you are not forwarding MIDI, nor mapping parameters, you will
        never get any MIDI messages at all. """
        if self.init_ready:
            # self.log_message("MC.build_midi_map: firing")
            # build the relationships between info in Live and each __encoder, this is the MAPPING part (Parameters handled by Live directly)
            for s in self.__encoders:
                s.build_midi_map(midi_map_handle)

            # ask Live to forward all midi note and CC messages here. This is the FORWARDING part  (Parameters handled by this script, for example for Function mode)
            for i in range(C4SID_FIRST, C4SID_LAST + 1):
                Live.MidiMap.forward_midi_note(self.handle(), midi_map_handle, 0, i)
                Live.MidiMap.forward_midi_cc(self.handle(), midi_map_handle, 0, i)

            # self.rebuild_my_database = 1
            if self.return_resetter == 1:
                time.sleep(0.5)
                self.log_message("MC.build_midi_map: self.return_resetter == 1, forcing channel strip mode assignment after 500 ms sleep")
                self.__encoder_controller.handle_assignment_switch_ids(C4SID_CHANNEL_STRIP)  # default mode
                self.return_resetter = 0

    def receive_midi(self, midi_bytes):
        """MIDI messages are only received through this function, when explicitly forwarded in 'build_midi_map'"""

        is_note_on_msg = midi_bytes[0] & 0xF0 == NOTE_ON_STATUS
        is_note_off_msg = midi_bytes[0] & 0xF0 == NOTE_OFF_STATUS
        if self.__encoder_controller.assignment_mode() == C4M_USER:
            # already in USER mode, check for exit status
            marker_event = midi_bytes[1] == C4SID_MARKER
            lock_event = midi_bytes[1] == C4SID_LOCK
            is_marker_press = is_note_on_msg and marker_event
            is_marker_release = is_note_off_msg or is_marker_press and midi_bytes[2] == BUTTON_STATE_OFF
            previous_mode_switch_id = assignment_mode_switch_ids[self.__encoder_controller.last_assignment_mode()]
            self.__user_mode_exit = False
            if is_marker_press:
                self.set_marker_is_pressed(True)
            elif is_marker_release:
                self.set_marker_is_pressed(False)
            elif lock_event and self.__marker_is_pressed:
                # conditions here do NOT need to guard against processing this button combo when NOT already in user mode
                new_mode = button_id_to_assignment_mode[previous_mode_switch_id]
                new_name = new_mode  # assignment_mode_to_button_id[new_mode]
                if new_name == 1:
                    new_name = "C4M_PLUGINS"
                elif new_name == 2:
                    new_name = "C4M_CHANNEL_STRIP"
                elif new_name == 3:
                    new_name = "C4M_FUNCTION"
                #  before STOP signal events for patch to process
                # self.__c_instance.send_midi(midi_bytes)  # no LOCK Press event to the patch
                self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MARKER, BUTTON_STATE_OFF)) # yes Marker Release event to patch
                # STOP signal for patch to process
                self.log_message("MC.receive_midi: sending 'button 22' signal toggling Max bypass mode, STOP processing START bypassing")
                self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MAX_BYPASS_ID, BUTTON_STATE_OFF)) # for this signal: velocity 0 means STOP processing
                self.log_message("MC.receive_midi: leaving C4M_USER mode (0) for {0} mode ({1})".format(new_name, new_mode))
                self.__encoder_controller.handle_assignment_switch_ids(previous_mode_switch_id)
                self.__user_mode_exit = True # flag needs to stay set until first method re-entry after USER mode only

            if self.init_ready and not self.__user_mode_exit:
                # C4M_USER mode normal forwarding to Max patch for processing
                # (or spurious feedback to C4 if patch is not running or patch processing is manually bypassed?)
                self.__c_instance.send_midi(midi_bytes)   # all midi (Note and CC event messages)
        elif self.__user_mode_exit and self.__encoder_controller.last_assignment_mode() == C4M_USER:
            # logging.info("MC.receive_midi: note message: ({},{})".format(midi_bytes[1], midi_bytes[2]))
            if is_note_on_msg and midi_bytes[2] == BUTTON_STATE_ON and midi_bytes[1] == C4SID_LOCK:
                # if first message after leaving USER mode is a LOCK button event
                force_unlocking = True
                self.lock_surface(force_unlocking)
                logging.info("MC.receive_midi: (first user mode exit) event handled - ignoring first LOCK button pressed event")
            elif is_note_off_msg and midi_bytes[1] == C4SID_LOCK:
                # logging.info("MC.receive_midi: (first user mode exit) event handled - ignoring LOCK Note OFF event")
                pass
                # logging.info("MC.receive_midi: (first user mode exit) event handled - ignoring MARKER Note OFF event")
            else:
                logging.info("MC.receive_midi: (first user mode exit) event unhandled - {} event message dropped".format(midi_bytes))
            self.__user_mode_exit = False
        elif self.init_ready:
            # self.log_message("MC.receive_midi: mode != C4M_USER")
            # in cases when the first midi_msg event after leaving USER mode is NOT a LOCK button event, clear the USER mode exit flag so this script
            # will handle LOCK button events normally. (otherwise "force_unlocking danger" exists (once) as long as last_assignment_mode() == C4M_USER)
            self.__user_mode_exit = False
            is_cc_msg = midi_bytes[0] & 0xF0 == CC_STATUS
            # self.log_message("MC.receive_midi: noteON<{}> noteOFF<{}> cc<{}>".format(is_note_on_msg, is_note_off_msg, is_cc_msg))
            if is_note_on_msg:
                channel = midi_bytes[0] & 0x0F  # (& 0F preserves only channel related bits)
                note = midi_bytes[1]  # data1
                velocity = midi_bytes[2]  # data2
                ignore_note_offs = velocity == BUTTON_STATE_ON  # ignore Note ON events without 127 velocity
                # self.log_message("MC.receive_midi: note<{}> velo<{}>".format(note, velocity))
                """   Any button on the C4 falls into this range G#-1 up to Eb 4 [00 - 3F] """
                if note in set(range(C4SID_FIRST, C4SID_LAST + 1)):
                    if note in modifier_switch_ids:
                        self.__encoder_controller.handle_modifier_switch_ids(note, velocity)
                    elif ignore_note_offs:
                        if note in self.__note_handling_dict:
                            self.__note_handling_dict[note](note)
                        else:
                            if note == 4: # Spot/Erase button is not mapped to any remote script behavior
                                # self.log_message("MC.receive_midi: Spot/Erase button is not mapped to any handling behavior")
                                pass
                            else:
                                self.log_message("MC.receive_midi: unhandled note value: {}".format(note))

                    if note == C4SID_MARKER:
                        # This "note" entered receive_midi() with script NOT already in USER mode, now it is in USER mode, turn off the MARKER LED and pass control
                        # (the patch might turn the LED right back ON after it takes over, but this feedback message will reach the patch before the 'button 22' message below)
                        self.__c_instance.send_midi((NOTE_OFF_STATUS, note, BUTTON_STATE_OFF)) # this script just switched to USER mode, and MARKER LED is now OFF
                        self.__c_instance.send_midi((NOTE_ON_STATUS, C4SID_MAX_BYPASS_ID, BUTTON_STATE_ON)) # for this signal: velocity 127 means START processing

                        self.log_message("MC.receive_midi: sending 'button 22' signal toggling Max bypass mode, START processing STOP bypassing")
            elif is_cc_msg:
                """here one can use vpot_rotation to forward CC data to a function"""
                cc_no = midi_bytes[1]
                cc_value = midi_bytes[2]
                # vpot_range = [32, 33, 34, 35, ..., 63] == [0x20, 0x21, 0x22, ..., 0x3F]
                # so vpot_range[11] == 43 == C4SID_VPOT_CC_ADDRESS_12 == 0x2B
                vpot_range = range(C4SID_VPOT_CC_ADDRESS_BASE, C4SID_VPOT_CC_ADDRESS_32 + 1)

                if self.__encoder_controller.assignment_mode() == C4M_FUNCTION:
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_12:
                        self.handle_jog_wheel_rotation(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_14:  # skip encoder 13 (display space occupied)
                        self.set_loop_length(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_15:
                        self.set_loop_start(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_16:
                        self.zoom_or_scroll(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_19:
                        self.scrub_clip(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_20:
                        self.scroll_clip(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_21:
                        self.zoom_clip(cc_value)
                    if vpot_range[cc_no] == C4SID_VPOT_CC_ADDRESS_22:
                        self.tempo_change(cc_value)

                elif self.__encoder_controller.assignment_mode() == C4M_CHANNEL_STRIP:
                    if 8 <= cc_no <= 15:
                        self.__encoder_controller.toggle_devices(cc_no, cc_value)
            elif is_note_off_msg: # an actual Note Off event: is_note_off_msg = midi_bytes[0] & 0xF0 == NOTE_OFF_STATUS
                # logging.info("MC.receive_midi: unhandled - passing (ignoring) note off event {}".format(midi_bytes))
                # this pass is expected, the C4 sends Note ON with velocity 0 for Note OFF.
                # Live generates Note Offs the script can ignore and the USER Mode patch doesn't need to process
                pass
            elif midi_bytes[0] == 0xF0:
                # this sysex is from the C4, it is the unit serial number in response to a sysex request (from Live?)
                #                                        Z   T   1   0   4   7   3   A   3  ACK
                #                240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 65, 51,   6, 0, 247
                #                                        Z   T   1   0   4   7   3    y DLE ACK
                c4InitWelcome = [240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 121, 16,  6, 0, 247]
                lgth = len(c4InitWelcome)
                if lgth == len(midi_bytes):
                    match = True
                    for i in range(5): # first chunk always the same, middle chunk varies with serial numbers
                        if c4InitWelcome[i] != midi_bytes[i]:
                            match = False
                    for j in range(lgth - 3, lgth):# last chunk always the same
                        if c4InitWelcome[j] != midi_bytes[j]:
                            match = False
                    if match:
                        # the C4 just blanked its displays (except the hello message on the top screen?)
                        self.update_display()
                        if self.__encoder_controller.assignment_mode() == C4M_USER:
                            # forward to Max patch to also handle
                            self.__c_instance.send_midi(midi_bytes)
                    else:
                        logging.info("MC.receive_midi: unhandled matching length - sysex event {} dropped".format(midi_bytes))
                else:
                    logging.info("MC.receive_midi: unhandled non-matching length - sysex event {} dropped".format(midi_bytes))

            else:
                logging.info("MC.receive_midi: unhandled - event {} dropped".format(midi_bytes))

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
        nav = Live.Application.Application.View.NavDirection
        app_view = self.application().view
        view_name = 'Detail/DeviceChain'
        clip = self.song().view.detail_clip

        scroll = cc_value == 1 and 3 or 2  # (because 'and' has higher precedence than 'or' scroll will only be assigned the value True when cc_value == 2)
        log_txt = 'scroll_clip called with cc_value {}'.format(cc_value)
        logging.info(log_txt)

        if cc_value > 64:
            if not self.application().view.is_view_visible(view_name):
                self.application().view.focus_view(view_name)
                # clip.move_playing_pos(- cc_value)
                app_view.scroll_view(nav.left, view_name, False)
        if cc_value <= 64:
            if not self.application().view.is_view_visible(view_name):
                self.application().view.focus_view(view_name)
                app_view.scroll_view(nav.right, view_name, False)

    def zoom_clip(self, cc_value):
        nav = Live.Application.Application.View.NavDirection
        app_view = self.application().view
        view_name = 'Detail/Clip'
        log_txt = 'MC.zoom_clip: called with cc_value {}'.format(cc_value)
        logging.info(log_txt)

        # scroll = cc_value == 65 and 3 or 1
        if cc_value > 64:
            if not app_view.is_view_visible(view_name):
                logging.info('MC.zoom_clip: Focusing Detail/Clip view')
                app_view.focus_view(view_name)
                app_view.zoom_view(nav.left, view_name, False)
                logging.info('MC.zoom_clip: Zooming view to the left')
        if cc_value < 64:
            if not app_view.is_view_visible(view_name):
                logging.info('MC.zoom_clip: Focusing Detail/Clip view')
                app_view.focus_view(view_name)
                app_view.zoom_view(nav.right, view_name, False)
                logging.info('MC.zoom_clip: Zooming view to the right')

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
        return ''

    def suggest_output_port(self):
        """Live -> Script        Live can ask the script for an output port name to find a suitable one.        """
        return ''

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
        self.rem_mixer_listeners()
        self.rem_scene_listeners()
        self.rem_overdub_listener()
        self.rem_tracks_listener()
        self.rem_device_listeners()
        self.rem_transport_listener()
        if self.song().visible_tracks_has_listener(self.tracks_change):
            self.song().remove_visible_tracks_listener(self.tracks_change)
        for c in self.__components:
            c.destroy()

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
        if self.init_ready:
            # self.log_message("MC.refresh_state: firing")
            self.add_mixer_listeners()
            self.add_overdub_listener()
            self.add_tracks_listener()
            self.add_device_listeners()
            self.add_transport_listener()
            self.add_scene_listeners()
            if self.rebuild_my_database == 0:
                self.__encoder_controller.build_setup_database()
                self.rebuild_my_database = 1
            self.trBlock(0, len(self.song().visible_tracks))

    def add_scene_listeners(self):
        # Instead of checking if the listener exists before adding or removing it, I've added try-except blocks to handle the cases when the listener is not present. This reduces the number of function calls
        try:
            self.song().view.add_selected_scene_listener(self.scene_change)
        except RuntimeError:
            pass

        try:
            self.song().view.add_selected_track_listener(self.track_change)
        except RuntimeError:
            pass

    def rem_scene_listeners(self):
        # Instead of checking if the listener exists before adding or removing it, I've added try-except blocks to handle the cases when the listener is not present. This reduces the number of function calls
        try:
            self.song().view.remove_selected_scene_listener(self.scene_change)
        except RuntimeError:
            pass

        try:
            self.song().view.remove_selected_track_listener(self.track_change)
        except RuntimeError:
            pass

    def track_change(self):
        # need to do 2 things: assign the new 'selected Index'
        #     self.track_index = selected_index
        # and
        # figure out if a track was added, deleted, or just changed, then delegate to appropriate encoder controller methods
        selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks
        # track might have been deleted, added, or just changed (always one at a time?)
        if not len(tracks) in range(self.track_count - 1, self.track_count + 2):  # include + 1 in range
            self.log_message("MC.track_change: nbr visible tracks (includes rtn tracks) {0} BUT SAVED VALUE <{1}> OUT OF EXPECTED RANGE".format(len(tracks), self.track_count))
        else:
            assert len(tracks) in range(self.track_count - 1, self.track_count + 2)  # include + 1 in range
            # self.log_message("MC.track_change:  nbr visible tracks in expected range (includes rtn tracks) {0} and saved value <{1}> agree".format(len(tracks), self.track_count))

        index = 0
        selected_index = 0
        found = selected_track in tracks

        for track in tracks:
            if track == selected_track:
                selected_index = index
                found = True
            index += 1

        if not found:
            if selected_track == self.song().master_track:
                # index is now "one past" the last index in
                # tracks = self.song().visible_tracks + self.song().return_tracks
                selected_index = index
            else:
                # signal that something bad happened - selected track
                selected_index = 555

        if selected_index != self.track_index:
            # self.log_message("MC.track_change: setting self.track_index {0} to selected index {1}".format(self.track_index, selected_index))
            self.track_index = selected_index

        if self.track_count > len(tracks):
            self.__encoder_controller.track_deleted(selected_index)
            self.track_count -= 1
        elif self.track_count < len(tracks):
            self.__encoder_controller.track_added(selected_index)
            self.track_count += 1
            self.tracks_change()
        else:
            self.__encoder_controller.track_changed(selected_index)

    def scene_change(self):   # do we need scenes? TESTED, without scene stuff, display on C4 doesn't get updated (WTF??)'
        selected_scene = self.song().view.selected_scene
        scenes = self.song().scenes
        index = 0
        selected_index = 0
        for scene in scenes:
            index = index + 1
            if scene == selected_scene:
                selected_index = index

        if selected_index != self.scene:
            self.scene = selected_index

    def add_transport_listener(self):
        # Instead of checking if the listener exists before adding or removing it, I've added try-except blocks to handle the cases when the listener is not present. This reduces the number of function calls
        try:
            self.song().add_is_playing_listener(self.transport_change)
        except RuntimeError:
            pass

    def rem_transport_listener(self):
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
        self.request_rebuild_midi_map()

    def rem_mixer_listeners(self):
        # Master Track
        for type in ('volume', 'panning', 'crossfader'):
            for tr in self.masterlisten[type]:
                if liveobj_valid(tr):
                    cb = self.masterlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        # Normal Tracks
        for type in ('arm', 'solo', 'mute', 'current_monitoring_state', 'available_input_routing_channels',
                     'available_input_routing_types', 'available_output_routing_channels',
                     'available_output_routing_types', 'input_routing_channel', 'input_routing_type',
                     'output_routing_channel', 'output_routing_type', ):
            for tr in self.mlisten[type]:
                if liveobj_valid(tr):  # and not tr.None:
                    # ("C4/rem_mixer_listeners track <{0}> ltype <{1}>".format(tr.name, type))
                    cb = self.mlisten[type][tr]
                    if type == 'arm':
                        if tr.can_be_armed == 1:
                            if tr.arm_has_listener(cb) == 1:
                                tr.remove_arm_listener(cb)

                    elif type == 'current_monitoring_state':
                        if tr.can_be_armed == 1:
                            if tr.current_monitoring_state_has_listener(cb) == 1:
                                tr.remove_current_monitoring_state_listener(cb)
                    else:
                        test = eval('tr.' + type + '_has_listener(cb)')
                        if test == 1:
                            eval('tr.remove_' + type + '_listener(cb)')

        for type in ('volume', 'panning'):
            for tr in self.mlisten[type]:
                if liveobj_valid(tr):
                    cb = self.mlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        for tr in self.mlisten['sends']:
            if liveobj_valid(tr):
                for send in self.mlisten['sends'][tr]:
                    if liveobj_valid(send):
                        cb = self.mlisten['sends'][tr][send]
                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)

        for tr in self.mlisten['name']:
            if liveobj_valid(tr):
                cb = self.mlisten['name'][tr]
                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)

        # Return Tracks
        for type in ('solo', 'mute', 'available_output_routing_channels', 'available_output_routing_types', 'output_routing_channel', 'output_routing_type'):
            for tr in self.rlisten[type]:
                if liveobj_valid(tr):
                    cb = self.rlisten[type][tr]
                    test = eval('tr.' + type + '_has_listener(cb)')
                    if test == 1:
                        eval('tr.remove_' + type + '_listener(cb)')

        for type in ('volume', 'panning'):
            for tr in self.rlisten[type]:
                if liveobj_valid(tr):
                    cb = self.rlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        for tr in self.rlisten['sends']:
            if liveobj_valid(tr):
                for send in self.rlisten['sends'][tr]:
                    if liveobj_valid(send):
                        cb = self.rlisten['sends'][tr][send]
                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)

        for tr in self.rlisten['name']:
            if liveobj_valid(tr):
                cb = self.rlisten['name'][tr]
                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)

        self.mlisten = {'solo': {}, 'mute': {}, 'arm': {}, 'current_monitoring_state': {}, 'panning': {}, 'volume': {},
                        'sends': {}, 'name': {}, 'available_input_routing_channels': {}, 'available_input_routing_types': {},
                        'available_output_routing_channels': {}, 'available_output_routing_types': {},
                        'input_routing_type': {}, 'input_routing_channel': {}, 'output_routing_channel': {},
                        'output_routing_type': {}, }
        self.rlisten = {'solo': {}, 'mute': {}, 'panning': {}, 'volume': {}, 'sends': {}, 'name': {},
                        'available_output_routing_channels': {}, 'available_output_routing_types': {},
                        'output_routing_channel': {}, 'output_routing_type': {}}
        self.masterlisten = {'panning': {}, 'volume': {}, 'crossfader': {}}
        return

    def add_mixer_listeners(self):
        self.rem_mixer_listeners()
        tr = self.song().master_track
        for type in ('volume', 'panning', 'crossfader'):
            self.add_master_listener(0, type, tr)

        tracks = self.song().visible_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 0)
            for type in ('arm', 'solo', 'mute'):
                if type == 'arm':
                    if tr.can_be_armed == 1:
                        self.add_mixert_listener(track, type, tr)
                else:
                    self.add_mixert_listener(track, type, tr)

            for type in ('volume', 'panning'):
                self.add_mixerv_listener(track, type, tr)

            for type in ('is_frozen'):
                if tr.can_be_frozen == 1:
                    if tr.is_frozen_has_listener(self.on_is_frozen_changed):
                        tr.remove_is_frozen_listener(self.on_is_frozen_changed)
                    tr.add_is_frozen_listener(self.on_is_frozen_changed)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_send_listener(track, tr, sid, tr.mixer_device.sends[sid])

        tracks = self.song().return_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 1)
            for type in ('solo', 'mute'):
                self.add_retmixert_listener(track, type, tr)

            for type in ('volume', 'panning'):
                self.add_retmixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_retsend_listener(track, tr, sid, tr.mixer_device.sends[sid])

    def on_is_frozen_changed(self):
        self.__encoder_controller.handle_assignment_switch_ids(C4SID_CHANNEL_STRIP)

    def add_send_listener(self, tid, track, sid, send):
        if (track in self.mlisten['sends']) != 1:
            self.mlisten['sends'][track] = {}
        if (send in self.mlisten['sends'][track]) != 1:
            cb = lambda: self.send_changestate(tid, track, sid, send)
            self.mlisten['sends'][track][send] = cb
            send.add_value_listener(cb)

    def add_mixert_listener(self, tid, type, track):
        if (track in self.mlisten[type]) != 1:
            cb = lambda: self.mixert_changestate(type, tid, track)
            self.mlisten[type][track] = cb
            eval('track.add_' + type + '_listener(cb)')

    def add_mixerv_listener(self, tid, type, track):
        if (track in self.mlisten[type]) != 1:
            cb = lambda: self.mixerv_changestate(type, tid, track)
            self.mlisten[type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    def add_master_listener(self, tid, type, track):
        if (track in self.masterlisten[type]) != 1:
            cb = lambda: self.mixerv_changestate(type, tid, track, 2)
            self.masterlisten[type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    def add_retsend_listener(self, tid, track, sid, send):
        if (track in self.rlisten['sends']) != 1:
            self.rlisten['sends'][track] = {}
        if (send in self.rlisten['sends'][track]) != 1:
            cb = lambda: self.send_changestate(tid, track, sid, send, 1)
            self.rlisten['sends'][track][send] = cb
            send.add_value_listener(cb)

    def add_retmixert_listener(self, tid, type, track):
        if (track in self.rlisten[type]) != 1:
            cb = lambda: self.mixert_changestate(type, tid, track, 1)
            self.rlisten[type][track] = cb
            eval('track.add_' + type + '_listener(cb)')

    def add_retmixerv_listener(self, tid, type, track):
        if (track in self.rlisten[type]) != 1:
            cb = lambda: self.mixerv_changestate(type, tid, track, 1)
            self.rlisten[type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    # Track name listener
    def add_trname_listener(self, tid, track, ret=0):
        cb = lambda: self.trname_changestate(tid, track, ret)
        if ret == 1:
            if (track in self.rlisten['name']) != 1:
                self.rlisten['name'][track] = cb
        elif (track in self.mlisten['name']) != 1:
            self.mlisten['name'][track] = cb
        track.add_name_listener(cb)

    def mixerv_changestate(self, type, tid, track, r=0):
        val = eval('track.mixer_device.' + type + '.value')
        types = {'panning': 'pan', 'volume': 'volume', 'crossfader': 'crossfader'}
        if r == 2:
            pass
        elif r == 1:
            pass

    def mixert_changestate(self, type, tid, track, r=0):
        val = eval('track.' + type)
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

    def add_device_listeners(self):
        self.rem_device_listeners()
        # self.log_message("MC.add_device_listeners: for tracks")
        self.do_add_device_listeners(self.song().tracks, 0)
        # self.log_message("MC.add_device_listeners: for return tracks")
        self.do_add_device_listeners(self.song().return_tracks, 1)
        # self.log_message("MC.add_device_listeners: for main track")
        self.do_add_device_listeners([self.song().master_track], 2)

    def do_add_device_listeners(self, tracks, type):
        for i in range(len(tracks)):
            self.add_device_listener(tracks[i], i, type)
            # self.log_message("MC.do_add_device_listeners: for track type <{0}>".format(type))
            if len(tracks[i].devices) >= 1:
                for j in range(len(tracks[i].devices)):
                    self.add_devpmlistener(tracks[i].devices[j])
                    param_count = len(tracks[i].devices[j].parameters)
                    # self.log_message("MC.do_add_device_listeners: adding <{0}> device parameter listeners".format(param_count))
                    if param_count >= 1:
                        for k in range(len(tracks[i].devices[j].parameters)):
                            par = tracks[i].devices[j].parameters[k]
                            self.add_paramlistener(par, i, j, k, type)

    def rem_device_listeners(self):
        for pr in self.prlisten:
            if liveobj_valid(pr):
                ocb = self.prlisten[pr]
                # self.log_message("MC.rem_device_listeners: removing track device parameter listeners")
                if pr.value_has_listener(ocb) == 1:
                    pr.remove_value_listener(ocb)

        self.prlisten = {}

        for tr in self.dlisten:
            if liveobj_valid(tr):
                ocb = self.dlisten[tr]
                # self.log_message("MC.rem_device_listeners: removing track listeners")
                if tr.view.selected_device_has_listener(ocb) == 1:  # this is a direct call/check with to a function from Live (def selected_device_has_listener)
                    tr.view.remove_selected_device_listener(ocb)

        self.dlisten = {}

        for de in self.plisten:
            if liveobj_valid(de):
                ocb = self.plisten[de]
                # self.log_message("MC.rem_device_listeners: removing track device listeners")
                if de.parameters_has_listener(ocb) == 1:
                    de.remove_parameters_listener(ocb)

        self.plisten = {}
        return

    def add_device_listener(self, track, tid, type):
        cb = lambda: self.device_changestate(track, tid, type)
        # self.log_message("MC.add_device_listener: track <{0}> tidx <{1}> type <{2}>".format(track.name, tid, type))
        if (track in self.dlisten) != 1:
            track.add_devices_listener(cb)  # this is a direct call/check with/ to a function from Live
            track.view.add_selected_device_listener(cb)   # this is a direct call/check with/ to a function from Live ( def add_selected_device_listener(self, arg1, arg2) )

            # self.log_message("MC.add_device_listener: not already listening, so adding listener callback")
            self.dlisten[track] = cb

    def device_changestate(self, track, tid, type):  # equivalent to __on_selected_device_chain_changed in MCU
        # self.log_message("MC.device_changestate: track <{0}> tidx <{1}> type <{2}>".format(track.name, tid, type))
        # did = self.tuple_idx(track.devices, track.view.selected_device)
        self.__encoder_controller.device_added_deleted_or_changed(track, tid, type)
        # if type == 2:
        #     pass
        # elif type == 1:
        #     pass

    def add_devpmlistener(self, device):  # devpmlistener is device parameter listener
        cb = lambda: self.devpm_change()
        if (device in self.plisten) != 1:
            device.add_parameters_listener(cb)
            self.plisten[device] = cb

    def devpm_change(self):
        self.refresh_state()

    def add_paramlistener(self, param, tid, did, pid, type):
        cb = lambda: self.param_changestate(param, tid, did, pid, type)
        if (param in self.prlisten) != 1:
            param.add_value_listener(cb)
            self.prlisten[param] = cb

    def param_changestate(self, param, tid, did, pid, type):
        if type == 2:
            pass
        elif type == 1:
            pass

    def track_inc_dec(self, note):
        selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks

        if selected_track == self.song().master_track:
            if note == C4SID_TRACK_LEFT:
                selected_index = len(tracks) - 1
                self.song().view.selected_track = tracks[selected_index]
            # can't move right of master track
        else:
            selected_index = tracks.index(selected_track)
            for index, track in enumerate(tracks):
                if track == selected_track:
                    if note == C4SID_TRACK_LEFT and index > 0:
                        selected_index = index - 1
                    elif note == C4SID_TRACK_RIGHT and index < len(tracks) - 1:
                        selected_index = index + 1
                    elif note == C4SID_TRACK_RIGHT and index == len(tracks) - 1:
                        self.song().view.selected_track = self.song().master_track
                        return  # Return early since the master track has been selected

            if 0 <= selected_index < len(tracks):
                self.song().view.selected_track = tracks[selected_index]

    def lock_surface(self, force_unlock=False):
        if force_unlock:
            self.log_message("MC.lock_surface: force unlocking surface, LOCK led state to OFF")
            self.surface_is_locked = 0
            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_OFF))
        elif not self.surface_is_locked:
            self.log_message("MC.lock_surface: toggle locking surface, led state to ON")
            self.surface_is_locked = 1
            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_ON))
        else:
            self.log_message("MC.lock_surface: toggle unlocking surface, led state to OFF")
            self.surface_is_locked = 0
            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_OFF))

    def log_message(self, *message):
        """ Overrides standard to use logger instead of c_instance. """
        try:
            message = '(%s) %s' % (self.__class__.__name__, " ".join(map(str, message)))
            logger.info(message)
        except:
            logger.info('MC.log_message: Logger encountered illegal character(s)!')

    @staticmethod
    def get_logger():
        """ Returns this script's logger object. """
        return logger

    def show_message(self, message):
        """ Displays the given message in Live's status bar """
        self.__c_instance.show_message(message)
