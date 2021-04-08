# was Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/MackieC4.py
# Compiled at: 2011-01-22 04:38:37
# Decompiled by https://python-decompiler.com
"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
# MS: not sure this applies anymore ;-)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Nathan Ramella <nar@remix.net> or visit http://www.remix.net

This script is based off the Ableton Live supplied MIDI Remote Scripts.

This is the second file that is loaded, by way of being instantiated through
__init__.py

from _Framework.ControlSurface import ControlSurface
import logging, time, LiveUtils
from consts import *
from Encoder import Encoder
from EncoderController import EncoderController
import MidiRemoteScript
import Live

"""
from __future__ import absolute_import, print_function, unicode_literals
import sys
import Live
if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object
    import logging
    import time
    from .consts import *
    from .Encoders import Encoders
    from .EncoderController import EncoderController
else:  # Live 10
    import logging, time
    from .consts import *
    from .Encoders import Encoders
    from .EncoderController import EncoderController
    import MidiRemoteScript

logger = logging.getLogger(__name__)


class MackieC4(object):
    """  Main class that establishes the MackieC4 Component
         --- although technically, the Mackie Control C4Pro is an "extension" of the
             Mackie Control itself (like the MackieControlXT), this script stands alone.
             It doesn't work 'with' those Midi Remote Scripts which is why is_extension()
             returns False from here
    """
    __module__ = __name__
    prlisten = {}
    '''prlisten is "Parameter Range" Listener?'''

    plisten = {}
    '''plisten is "Parameter" Listener?"'''

    dlisten = {}
    '''dlisten is "Device Listener'''

    # clisten = {}
    # '''clisten is "Clip" Listener'''

    slisten = {}
    '''slisten is "Slot Listener'''

    sslisten = {}

    pplisten = {}
    '''pplisten is "Playing Position" Listener'''

    # cnlisten = {}
    # '''cnlisten is "Clip Listener'''
    #
    # cclisten = {}
    # '''cclisten is "Clip Color" Listener'''

    mlisten = {'solo': {}, 'mute': {}, 'arm': {}, 'current_monitoring_state': {}, 'panning': {}, 'volume': {}, 'sends': {}, 'name': {}, 'oml': {}, 'omr': {}, 'color': {}, 'available_input_routing_channels': {}, 'available_input_routing_types': {}, 'available_output_routing_channels': {}, 'available_output_routing_types': {}, 'input_routing_type': {}, 'input_routing_channel': {}, 'output_routing_channel': {}, 'output_routing_type': {}}
    '''oml is "output_meter_left, omr is output_meter_right'''

    rlisten = {'solo': {}, 'mute': {}, 'panning': {}, 'volume': {}, 'sends': {}, 'name': {}, 'color': {}, 'available_output_routing_channels': {}, 'available_output_routing_types': {}, 'output_routing_channel': {}, 'output_routing_type': {}}
    '''rlisten is "Returns" Listener '''

    masterlisten = {'panning': {}, 'volume': {}, 'crossfader': {}}
    scenelisten = {}
    scene = 0
    track = 0
    track_count = 0
    surface_is_locked = 0
    rebuild_my_database = 0
    return_resetter = 0

    def __init__(self, c_instance):
        self.__c_instance = c_instance

        # initialize the 32 encoders, their EncoderController and
        # add them as __components here
        self.__components = []
        self.__encoders = [Encoders(self, i) for i in encoder_range]
        for s in self.__encoders:
            self.__components.append(s)

        self.__encoder_controller = EncoderController(self, self.__encoders)
        self.__components.append(self.__encoder_controller)

        # turn off FUNCTION and ASSIGNMENT button LEDs except the default
        for cc in range(C4SID_SPLIT, C4SID_FUNCTION + 1):
            if cc == C4SID_CHANNEL_STRIP:
                self.send_midi((NOTE_ON_STATUS, cc, BUTTON_STATE_ON))
            else:
                self.send_midi((NOTE_ON_STATUS, cc, BUTTON_STATE_OFF))

        tracks = self.song().visible_tracks + self.song().return_tracks
        index = 0

        # if the selected Live track is in view (on computer screen?)
        # assign track to the local index of the matching selected track in Live
        for track in tracks:
            if track == self.song().view.selected_track:
                self.track = index
            index = index + 1

        self.track_count = len(tracks)

        # if refresh_state is not already listening for visible tracks view changes
        if self.song().visible_tracks_has_listener(self.refresh_state) != 1:
            self.song().add_visible_tracks_listener(self.refresh_state)

    def connect_script_instances(self, instanciated_scripts):
        """
        Called by the Application as soon as all scripts are initialized.
        You can connect yourself to other running scripts here, as we do it
        connect the extension modules
        """
        pass

    def is_extension(self):
        return False

    def request_rebuild_midi_map(self):
        """
        To be called from any components, as soon as their internal state changed in a
        way, that we do need to remap the mappings that are processed directly by the
        Live engine.
        Don't assume that the request will immediately result in a call to
        your build_midi_map function. For performance reasons this is only
        called once per GUI frame.
        """
    # MS: _Framework.ControlSurface does the following codeblock
    # def request_rebuild_midi_map(self):
    #     if self._suppress_requests_counter > 0:
    #         self._rebuild_requests_during_suppression += 1
    #     else:
    #         self._c_instance.request_rebuild_midi_map()
        self.__c_instance.request_rebuild_midi_map()

    def update_display(self):
        """
        This function is run every 100ms, so we use it to initiate our Song.current_song_time
        listener to allow us to process incoming OSC commands as quickly as possible under
        the current listener scheme.
        """
        for c in self.__components:
            c.on_update_display_timer()

    def send_midi(self, midi_event_bytes):
        """
        Use this function to send MIDI events through Live to the _real_ MIDI devices
        that this script is assigned to.
        """
        self.__c_instance.send_midi(midi_event_bytes)

    def receive_midi(self, midi_bytes):

        # coming from C4 midi_bytes[0] is always 0x91 or 0xB1 (NOTE_ON or CC) [C4 sends note on with velocity 0 for note off]
        # velocity of note on messages is always 7F, velocity of note off messages is always 00
        # C4 always sends and receives on channel 1
        is_note_on_msg = midi_bytes[0] & 0xF0 == NOTE_ON_STATUS  # (& F0 strips off any channel related bits)
        is_note_off_msg = midi_bytes[0] & 0xF0 == NOTE_OFF_STATUS
        is_cc_msg = midi_bytes[0] & 0xF0 == CC_STATUS

        # self.log_message("noteON<{}> noteOFF<{}> cc<{}> received".format(is_note_on_msg, is_note_off_msg, is_cc_msg))
        if is_note_on_msg or is_note_off_msg:  # it will never be a note off message
            channel = midi_bytes[0] & 0x0F  # (& 0F preserves only channel related bits)
            note = midi_bytes[1]  # data1
            velocity = midi_bytes[2]  # data2

            # self.log_message("note<{}> velo<{}> received".format(note, velocity))
            ignore_note_offs = velocity == BUTTON_STATE_ON
            """   Any button on the C4 falls into this range
                             G#-1   up to Eb 4  [00 - 3F]          """
            if note in range(C4SID_FIRST, C4SID_LAST + 1) and ignore_note_offs:
                if note in track_nav_switch_ids:
                    self.track_inc_dec(note)
                elif note in bank_switch_ids:
                    self.__encoder_controller.handle_bank_switch_ids(note)
                elif note in slot_nav_switch_ids:
                    self.__encoder_controller.handle_slot_nav_switch_ids(note)
                elif note == C4SID_LOCK:
                    self.lock_surface()
                elif note in assignment_mode_switch_ids:
                    self.__encoder_controller.handle_assignment_switch_ids(note)
                elif note in encoder_switch_ids:  # this is just the 'encoder switches'
                    self.__encoder_controller.handle_pressed_v_pot(note)
        if is_cc_msg:  # 240 == CC_STATUS:

            # channel = midi_bytes[0] & 0x0F  # (& 0F preserves only channel related bits)
            cc_nbr = midi_bytes[1]  # data1
            cc_value = midi_bytes[2]  # data2

            # self.log_message("cc_nbr<{}> cc_value<{}> received".format(cc_nbr, cc_value))
            if cc_nbr in encoder_cc_ids:  # 0x20 - 0x3F
                vpot_index = cc_nbr & 0x0F  # & 0F preserves only vpot_index related bits)
                self.__encoder_controller.handle_vpot_rotation(vpot_index, cc_value)

    def can_lock_to_devices(self):
        return False

    def suggest_input_port(self):
        return ''

    def suggest_output_port(self):
        return ''

    def application(self):
        """returns a reference to the application that we are running in"""
        return Live.Application.get_application()

    def song(self):
        """returns a reference to the Live Song that we do interact with"""
        return self.__c_instance.song()

    def handle(self):
        """returns a handle to the c_interface that is needed when forwarding MIDI events via the MIDI map"""
        return self.__c_instance.handle()

    # def getslots(self):
    #     tracks = self.song().visible_tracks
    #     clipSlots = []
    #     for track in tracks:
    #         clipSlots.append(track.clip_slots)
    #
    #     return clipSlots

    def trBlock(self, trackOffset, blocksize):
        block = []
        tracks = self.song().visible_tracks
        for track_index in range(0, blocksize):
            if len(tracks) > trackOffset + track_index:
                trk_nme = tracks[(trackOffset + track_index)].name
                # not just adding the track name, adding a list with one element that is the track name
                block.extend([str(trk_nme)])
            else:
                block.extend(['fake Track NAME'])  # MS lets try

    def disconnect(self):
        # self.rem_clip_listeners()
        self.rem_mixer_listeners()
        self.rem_scene_listeners()
        self.rem_tempo_listener()
        self.rem_overdub_listener()
        self.rem_tracks_listener()
        self.rem_device_listeners()
        self.rem_transport_listener()
        self.song().remove_visible_tracks_listener(self.refresh_state)
        for c in self.__components:
            c.destroy()

    def build_midi_map(self, midi_map_handle):

        # build the relationships between info in Live and each __encoder
        for s in self.__encoders:
            s.build_midi_map(midi_map_handle)

        # ask Live to forward all midi note messages here
        # cc's come automatically?
        for i in range(C4SID_FIRST, C4SID_LAST + 1):
            Live.MidiMap.forward_midi_note(self.handle(), midi_map_handle, 0, i)
            Live.MidiMap.forward_midi_cc(self.handle(), midi_map_handle, 0, i)

        self.rebuild_my_database = 1
        if self.return_resetter == 1:
            time.sleep(0.5)
            self.__encoder_controller.handle_assignment_switch_ids(C4SID_CHANNEL_STRIP)  # default mode
            self.return_resetter = 0

    def suggest_map_mode(self, cc_no, channel=0):  # MS identical to what MackieControlXT does
        result = Live.MidiMap.MapMode.absolute

        # if cc_no in range(FID_PANNING_BASE, FID_PANNING_BASE + NUM_ENCODERS):
        if cc_no in encoder_range:
            result = Live.MidiMap.MapMode.relative_signed_bit
        return result

    def refresh_state(self):
        # self.add_clip_listeners()
        self.add_mixer_listeners()
        self.add_tempo_listener()
        self.add_overdub_listener()
        self.add_tracks_listener()
        self.add_device_listeners()
        self.add_transport_listener()
        self.add_scene_listeners()
        if self.rebuild_my_database == 0:
            self.__encoder_controller.build_setup_database()
        self.trBlock(0, len(self.song().visible_tracks))

    def add_scene_listeners(self):
        self.rem_scene_listeners()
        if self.song().view.selected_scene_has_listener(self.scene_change) != 1:
            self.song().view.add_selected_scene_listener(self.scene_change)
        if self.song().view.selected_track_has_listener(self.track_change) != 1:
            self.song().view.add_selected_track_listener(self.track_change)

    def rem_scene_listeners(self):
        if self.song().view.selected_scene_has_listener(self.scene_change) == 1:
            self.song().view.remove_selected_scene_listener(self.scene_change)
        if self.song().view.selected_track_has_listener(self.track_change) == 1:
            self.song().view.remove_selected_track_listener(self.track_change)

    def track_change(self):
        selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks
        index = 0
        found = 0
        selected_index = 0
        for track in tracks:
            index = index + 1
            if track == selected_track:
                selected_index = index
                found = 1

        if found == 0:

            # I think this 128 might mean use the master track index as a fallback
            # but index 128 is out-of-bounds by one
            # (valid track indexes inside EncoderController are 00 - 127)
            selected_index = 127  # MS ok lets then try and change that to 127

        if selected_index != self.track:
            self.track = selected_index

        if self.track_count > len(tracks) + 1:
            self.__encoder_controller.track_deleted(selected_index - 1)
        elif self.track_count < len(tracks) + 1:
            self.__encoder_controller.track_added(selected_index - 1)  # MS this get called when moving clip to another existing track, why?
            self.return_resetter = 1
        else:
            self.__encoder_controller.track_changed(selected_index - 1)
        self.track_count = len(tracks) + 1

    def scene_change(self):
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

    def add_tempo_listener(self):
        self.rem_tempo_listener()
        # print ('add tempo listener')
        if self.song().tempo_has_listener(self.tempo_change) != 1:
            self.song().add_tempo_listener(self.tempo_change)

    def rem_tempo_listener(self):
        if self.song().tempo_has_listener(self.tempo_change) == 1:
            self.song().remove_tempo_listener(self.tempo_change)

    def tempo_change(self):  # MS was broken and referring to LiveUtils, fixed and requirement for LiveUtils removed
        return Live.Application.get_application().get_document().tempo

    def add_transport_listener(self):
        if self.song().is_playing_has_listener(self.transport_change) != 1:
            self.song().add_is_playing_listener(self.transport_change)

    def rem_transport_listener(self):
        if self.song().is_playing_has_listener(self.transport_change) == 1:
            self.song().remove_is_playing_listener(self.transport_change)

    def transport_change(self):
        pass

    def add_overdub_listener(self):
        self.rem_overdub_listener()
        if self.song().overdub_has_listener(self.overdub_change) != 1:
            self.song().add_overdub_listener(self.overdub_change)

    def rem_overdub_listener(self):
        if self.song().overdub_has_listener(self.overdub_change) == 1:
            self.song().remove_overdub_listener(self.overdub_change)

    def overdub_change(self):  # MS: removed dependency to LiveUtils
        return Live.Song.Song.overdub

    def add_tracks_listener(self):
        self.rem_tracks_listener()
        if self.song().tracks_has_listener(self.tracks_change) != 1:
            self.song().add_tracks_listener(self.tracks_change)

    def rem_tracks_listener(self):
        if self.song().tracks_has_listener(self.tracks_change) == 1:
            self.song().remove_tracks_listener(self.tracks_change)

    def tracks_change(self):
        self.request_rebuild_midi_map()

    # def rem_clip_listeners(self):
    #     self.log_message("** Remove Listeners **")
    #
    #     for slot in self.slisten:
    #         if slot is not None:
    #             if slot.has_clip_has_listener(self.slisten[slot]) == 1:  # MS HAD a KeyError when deleting a track, referring to ClipSlot.ClipSlot, fixed in LiveUtils
    #                 slot.remove_has_clip_listener(self.slisten[slot])
    #
    #     self.slisten = {}
    #
    #     for slot in self.sslisten:
    #         if slot is not None:
    #             if slot.has_stop_button_has_listener(self.sslisten[slot]) == 1:
    #                 slot.remove_has_stop_button_listener(self.sslisten[slot])
    #
    #     self.sslisten = {}
    #
    #     for clip in self.clisten:
    #         if clip is not None:
    #             if clip.playing_status_has_listener(self.clisten[clip]) == 1:  # MS KeyError when clip move across tracks, was 6 lines above, now here
    #                 clip.remove_playing_status_listener(self.clisten[clip])
    #
    #     self.clisten = {}
    #     for clip in self.pplisten:
    #         if clip is not None:
    #             if clip.playing_position_has_listener(self.pplisten[clip]) == 1:
    #                 clip.remove_playing_position_listener(self.pplisten[clip])
    #
    #     self.pplisten = {}
    #     for clip in self.cnlisten:
    #         if clip is not None:
    #             if clip.name_has_listener(self.cnlisten[clip]) == 1:
    #                 clip.remove_name_listener(self.cnlisten[clip])
    #
    #     self.cnlisten = {}
    #     for clip in self.cclisten:
    #         if clip is not None:
    #             if clip.color_has_listener(self.cclisten[clip]) == 1:
    #                 clip.remove_color_listener(self.cclisten[clip])
    #
    #     self.cclisten = {}
    #     return
    #
    # def add_clip_listeners(self):
    #     self.rem_clip_listeners()
    #     tracks = self.getslots()
    #     for track in range(len(tracks)):
    #         for clip in range(len(tracks[track])):
    #             c = tracks[track][clip]
    #             if c.clip is not None:
    #                 self.add_cliplistener(c.clip, track, clip)
    #             self.add_slotlistener(c, track, clip)
    #
    #     return
    #
    # def add_cliplistener(self, clip, tid, cid):
    #     cb = lambda: self.clip_changestate(clip, tid, cid)
    #     if (clip in self.clisten) != 1:
    #         clip.add_playing_status_listener(cb)
    #         self.clisten[clip] = cb
    #     cb2 = lambda: self.clip_position(clip, tid, cid)
    #     if (clip in self.pplisten) != 1:
    #         clip.add_playing_position_listener(cb2)
    #         self.pplisten[clip] = cb2
    #     cb3 = lambda: self.clip_name(clip, tid, cid)
    #     if (clip in self.cnlisten) != 1:
    #         clip.add_name_listener(cb3)
    #         self.cnlisten[clip] = cb3
    #     if (clip in self.cclisten) != 1:
    #         clip.add_color_listener(cb3)
    #         self.cclisten[clip] = cb3
    #
    # def add_slotlistener(self, slot, tid, cid):
    #     cb = lambda : self.slot_changestate(slot, tid, cid)
    #     if (slot in self.slisten) != 1:
    #         slot.add_has_clip_listener(cb)
    #         self.slisten[slot] = cb

    def rem_mixer_listeners(self):
        # Master Track
        for type in ('volume', 'panning', 'crossfader'):
            for tr in self.masterlisten[type]:
                if tr is not None:
                    cb = self.masterlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        # Normal Tracks
        for type in ('arm', 'solo', 'mute', 'current_monitoring_state', 'available_input_routing_channels',
                     'available_input_routing_types', 'available_output_routing_channels',
                     'available_output_routing_types', 'input_routing_channel', 'input_routing_type',
                     'output_routing_channel', 'output_routing_type'):
            for tr in self.mlisten[type]:
                if tr is not None:
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
                if tr is not None:
                    cb = self.mlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        for tr in self.mlisten['sends']:
            if tr is not None:
                for send in self.mlisten['sends'][tr]:
                    if send is not None:
                        cb = self.mlisten['sends'][tr][send]
                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)

        for tr in self.mlisten['name']:
            if tr is not None:
                cb = self.mlisten['name'][tr]
                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)

        for tr in self.mlisten['color']:
            if tr is not None:
                cb = self.mlisten['color'][tr]

                try:
                    if tr.color_has_listener(cb) == 1:
                        tr.remove_color_listener(cb)
                except:
                    pass

        for tr in self.mlisten['oml']:
            if tr is not None:
                cb = self.mlisten['oml'][tr]

                if tr.output_meter_left_has_listener(cb) == 1:
                    tr.remove_output_meter_left_listener(cb)

        for tr in self.mlisten['omr']:
            if tr is not None:
                cb = self.mlisten['omr'][tr]
                if tr.output_meter_right_has_listener(cb) == 1:
                    tr.remove_output_meter_right_listener(cb)

        # Return Tracks
        for type in ('solo', 'mute', 'available_output_routing_channels', 'available_output_routing_types', 'output_routing_channel', 'output_routing_type'):
            for tr in self.rlisten[type]:
                if tr is not None:
                    cb = self.rlisten[type][tr]
                    test = eval('tr.' + type + '_has_listener(cb)')
                    if test == 1:
                        eval('tr.remove_' + type + '_listener(cb)')

        for type in ('volume', 'panning'):
            for tr in self.rlisten[type]:
                if tr is not None:
                    cb = self.rlisten[type][tr]
                    test = eval('tr.mixer_device.' + type + '.value_has_listener(cb)')
                    if test == 1:
                        eval('tr.mixer_device.' + type + '.remove_value_listener(cb)')

        for tr in self.rlisten['sends']:
            if tr is not None:
                for send in self.rlisten['sends'][tr]:
                    if send is not None:
                        cb = self.rlisten['sends'][tr][send]
                        if send.value_has_listener(cb) == 1:
                            send.remove_value_listener(cb)

        for tr in self.rlisten['name']:
            if tr is not None:
                cb = self.rlisten['name'][tr]
                if tr.name_has_listener(cb) == 1:
                    tr.remove_name_listener(cb)

        for tr in self.rlisten['color']:
            if tr is not None:
                cb = self.rlisten["color"][tr]
                try:
                    if tr.color_has_listener(cb) == 1:
                        tr.remove_color_listener(cb)
                except:
                    pass
        self.mlisten = {'solo': {}, 'mute': {}, 'arm': {}, 'current_monitoring_state': {}, 'panning': {}, 'volume': {},
                        'sends': {}, 'name': {}, 'oml': {}, 'omr': {}, 'color': {},
                        'available_input_routing_channels': {}, 'available_input_routing_types': {},
                        'available_output_routing_channels': {}, 'available_output_routing_types': {},
                        'input_routing_type': {}, 'input_routing_channel': {}, 'output_routing_channel': {},
                        'output_routing_type': {}}
        self.rlisten = {'solo': {}, 'mute': {}, 'panning': {}, 'volume': {}, 'sends': {}, 'name': {}, 'color': {},
                        'available_output_routing_channels': {}, 'available_output_routing_types': {},
                        'output_routing_channel': {}, 'output_routing_type': {}}
        self.masterlisten = {'panning': {}, 'volume': {}, 'crossfader': {}}
        return

    def add_mixer_listeners(self):
        self.rem_mixer_listeners()
        tr = self.song().master_track
        for type in ('volume', 'panning', 'crossfader'):
            self.add_master_listener(0, type, tr)

        self.add_meter_listener(0, tr, 2)
        tracks = self.song().visible_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 0)
            if tr.has_audio_output:
                self.add_meter_listener(track, tr)
            for type in ('arm', 'solo', 'mute'):
                if type == 'arm':
                    if tr.can_be_armed == 1:
                        self.add_mixert_listener(track, type, tr)
                else:
                    self.add_mixert_listener(track, type, tr)

            for type in ('volume', 'panning'):
                self.add_mixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_send_listener(track, tr, sid, tr.mixer_device.sends[sid])

        tracks = self.song().return_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 1)
            self.add_meter_listener(track, tr, 1)
            for type in ('solo', 'mute'):
                self.add_retmixert_listener(track, type, tr)

            for type in ('volume', 'panning'):
                self.add_retmixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_retsend_listener(track, tr, sid, tr.mixer_device.sends[sid])

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

    def add_meter_listener(self, tid, track, r=0):
        cb = lambda: self.meter_changestate(tid, track, 0, r)
        if (track in self.mlisten['oml']) != 1:
            self.mlisten['oml'][track] = cb
        track.add_output_meter_left_listener(cb)
        cb = lambda: self.meter_changestate(tid, track, 1, r)
        if (track in self.mlisten['omr']) != 1:
            self.mlisten['omr'][track] = cb
        track.add_output_meter_right_listener(cb)

    # def clip_name(self, clip, tid, cid):
    #     pass
    #
    # def clip_position(self, clip, tid, cid):
    #     if self.check_md(1):
    #         if clip.is_playing:
    #             pass
    #
    # def slot_changestate(self, slot, tid, cid):
    #     # tmptrack = Live.getTrack(tid)
    #     # armed = tmptrack.arm and 1 or 0
    #     if slot.clip is not None:
    #         self.add_cliplistener(slot.clip, tid, cid)
    #         playing = 1
    #         if slot.clip.is_playing == 1:
    #             playing = 2
    #         if slot.clip.is_triggered == 1:
    #             playing = 3
    #         length = slot.clip.loop_end - slot.clip.loop_start
    #     elif (slot.clip in self.clisten) == 1:
    #         slot.clip.remove_playing_status_listener(self.clisten[slot.clip])
    #     else:
    #         if (slot.clip in self.pplisten) == 1:
    #             slot.clip.remove_playing_position_listener(self.pplisten[slot.clip])  # MS something's wrong here, according to LOM only clip.clip has pplisten,but not slot.clip
    #         if (slot.clip in self.cnlisten) == 1:
    #             slot.clip.remove_name_listener(self.cnlisten[slot.clip])
    #         if (slot.clip in self.cclisten) == 1:
    #             slot.clip.remove_color_listener(self.cclisten[slot.clip])
    #
    #     return
    #
    # def clip_changestate(self, clip, x, y):
    #     playing = 0
    #
    #     if clip.is_playing == 1:
    #         playing = 1
    #         if clip.is_recording == 1:
    #             playing = 3
    #         if self.song().tracks[x].arm == 1 and clip.is_audio_clip == 0:
    #             if self.song().overdub == 1:
    #                 playing = 3
    #             else:
    #                 playing = 1
    #     else:
    #         pass
    #     if clip.is_triggered == 1:
    #         playing = 2
    #     else:
    #         pass

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

    def meter_changestate(self, tid, track, lr, r=0):
        if r == 2:
            if self.check_md(2):
                if lr == 0:
                    pass
        elif r == 1:
            if self.check_md(3):
                if lr == 0:
                    pass
        elif self.check_md(4):
            if lr == 0:
                pass

    def check_md(self, param):
        devices = self.song().master_track.devices
        if len(devices) > 0:
            if devices[0].parameters[param].value > 0:  # MS IndexError (out of range) referring to "if self.check_md(2)" and "cb = lambda: self.meter_changestate(tid, track, 0, r)"
                return 1
            else:
                return 0
        else:
            return 0

    def add_device_listeners(self):
        self.rem_device_listeners()
        self.do_add_device_listeners(self.song().tracks, 0)
        self.do_add_device_listeners(self.song().return_tracks, 1)
        self.do_add_device_listeners([self.song().master_track], 2)

    def do_add_device_listeners(self, tracks, type):
        for i in range(len(tracks)):
            self.add_devicelistener(tracks[i], i, type)
            if len(tracks[i].devices) >= 1:
                for j in range(len(tracks[i].devices)):
                    self.add_devpmlistener(tracks[i].devices[j])
                    if len(tracks[i].devices[j].parameters) >= 1:
                        for k in range(len(tracks[i].devices[j].parameters)):
                            par = tracks[i].devices[j].parameters[k]
                            self.add_paramlistener(par, i, j, k, type)

    def rem_device_listeners(self):
        for pr in self.prlisten:
            try:
                ocb = self.prlisten[pr]  # KeyError when exchanging M4L device, KeyError when closing Live after deleting last device, ref to disconnect
            except KeyError:
                pr = None

            if pr is not None:
                if pr.value_has_listener(ocb) == 1:
                    pr.remove_value_listener(ocb)

        self.prlisten = {}
        for tr in self.dlisten:
            ocb = self.dlisten[tr]
            if tr is not None:
                if tr.view.selected_device_has_listener(ocb) == 1:
                    tr.view.remove_selected_device_listener(ocb)

        self.dlisten = {}
        for de in self.plisten:
            ocb = self.plisten[de]
            if de is not None:
                if de.parameters_has_listener(ocb) == 1:
                    de.remove_parameters_listener(ocb)

        self.plisten = {}  # MS this produces a KeyError when closing Live with:
        # RemoteScriptError:   File "C:\ProgramData\Ableton\Live 11 Beta\Resources\MIDI Remote Scripts\MackieC4\MackieC4.py", line 240, in disconnect
        # RemoteScriptError: self.rem_device_listeners()
        # RemoteScriptError:   File "C:\ProgramData\Ableton\Live 11 Beta\Resources\MIDI Remote Scripts\MackieC4\MackieC4.py", line 776, in rem_device_listeners
        # RemoteScriptError: ocb = self.prlisten[pr]
        # RemoteScriptError: KeyError
        # RemoteScriptError: <DeviceParameter.DeviceParameter object at 0x0000000073D58850>

        return

    def add_devpmlistener(self, device):
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

    def add_devicelistener(self, track, tid, type):
        cb = lambda: self.device_changestate(track, tid, type)
        if (track in self.dlisten) != 1:
            track.view.add_selected_device_listener(cb)
            self.dlisten[track] = cb

    def device_changestate(self, track, tid, type):  # MS THIS is the origin of shit, is it?
        # did = self.tuple_idx(track.devices, track.view.selected_device)
        self.__encoder_controller.device_added_deleted_or_changed()
        # if type == 2:
        #     pass
        # elif type == 1:
        #     pass

    # def tuple_idx(self, tuple, obj):
    #     for i in range(0, len(tuple)):
    #         if tuple[i] == obj:
    #             return i

    def track_inc_dec(self, note):
        # self.log_message("handling note <{}> for track inc dec".format(note))
        selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks
        index = 0
        selected_index = 0
        if selected_track == self.song().master_track:
            if note == C4SID_TRACK_LEFT:  # 19: left of master track is return tracks then regular tracks
                selected_index = len(tracks) - 1
                self.song().view.selected_track = tracks[selected_index]
                self.track = selected_index
            # can't move right of master track
        else:
            for track in tracks:
                index = index + 1
                if track == selected_track:
                    self.log_message("current selected_track <{}>".format(track.name))
                    if note == C4SID_TRACK_LEFT:
                        if index > 1:  # can't move selection left of track 0
                            selected_index = index - 2
                            self.song().view.selected_track = tracks[selected_index]
                            self.log_message("new selected_track <{}>".format(tracks[selected_index].name))
                    elif note == C4SID_TRACK_RIGHT:
                        if index < len(tracks):  # right of last return track goes to master track
                            selected_index = index
                            self.song().view.selected_track = tracks[index]
                            self.log_message("new selected_track <{}>".format(tracks[selected_index].name))
                        else:
                            selected_index = self.__encoder_controller.master_track_index()
                            self.song().view.selected_track = self.song().master_track
                            self.log_message("new selected_track <{}>".format(self.song().master_track.name))

            self.track = selected_index

    def lock_surface(self):
        if self.surface_is_locked == 0:
            self.log_message("locking surface, led state ON")
            self.surface_is_locked = 1
            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_ON))
        else:
            self.log_message("unlocking surface, led state OFF")
            self.surface_is_locked = 0
            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, BUTTON_STATE_OFF))

    def log_message(self, *message):
        """ Overrides standard to use logger instead of c_instance. """
        try:
            message = '(%s) %s' % (self.__class__.__name__,
             (' ').join(map(str, message)))
            logger.info(message)
        except:
            logger.info('Logging encountered illegal character(s)!')

    @staticmethod
    def get_logger():
        """ Returns this script's logger object. """
        return logger
