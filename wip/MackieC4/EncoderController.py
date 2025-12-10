# coding=utf-8
# was once Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/EncoderController.py
# Compiled at: 2011-01-22 05:02:32
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals  # MS
from __future__ import division

import re
import sys
import time

from ableton.v2.base import liveobj_valid, liveobj_changed, find_if, listens
from ableton.v2.control_surface.elements.display_data_source import adjust_string
from ableton.v2.control_surface.component import Component
from ableton.v3.live.action import toggle_or_cycle_parameter_value
import ableton.v3.live.util as v3_util

if sys.version_info[0] >= 3:  # Python 3.x (Live 11+)
    from builtins import range
    from ableton.v3.live import util


from . import track_util
from . import song_util
from .EncoderAssignmentHistory import EncoderAssignmentHistory
from .EncoderDisplaySegment import EncoderDisplaySegment
from .MackieC4Component import *
from _Generic.Devices import *
from .TimeDisplay import TimeDisplay


class EncoderController(MackieC4Component, Component):
    """
     Controls all (the sum) encoders of the Mackie C4 Pro controller extension
  """
    __module__ = __name__

    def __init__(self, main_script, encoders, device_provider):
        # suspect MackieC4Component exists because MackieC4 and EncoderController share some method_names.
        # MackieC4Component means EncoderController doesn't need to use super-class-shared-method-name
        # method calling semantics. Functions in MackieC4Component all delegate to functions in MackieC4,
        # known as main_script here
        if main_script is None:
            raise ValueError("main_script is None?")
        MackieC4Component.__init__(self, main_script)
        Component.__init__(self, register_component=self.register_component, song=self.song())

        # definition of modes, for refactoring various code to separate functions
        # this HAS TO BE up here. If further down in init, it will produce an error during initialization
        self.mode_functions = {
            "handle_pressed_v_pot": self.handle_pressed_v_pot,
            "reassign_encoder_parameters": self.__reassign_encoder_parameters,
            "on_update_display_timer": self.on_update_display_timer
        }

        # C4SID_SPLIT_ERASE is the only system switch (button) with no associated behavior mapped
        # C4SID_SPLIT behavior only affects "display updates" (feedback to leds and led rings)...
        #    when the song is NOT playing:
        #    C4SID_SPLIT controls the amount of intentional lag applied between "on display update timer" calls and actual C4 display updates
        #    all split button leds OFF means full lag amount (send display update midi messages once every 20 times "on display update timer" is called)
        #    all split button leds ON means no lag applied (send display update midi messages every time "on display update timer" is called, 1 for 1)
        #    Note: comments below about self.__display_repeat_timer impacting C4 "screen saver" sleep also apply here, the LCD backlights
        #    will not turn off because the song is NOT playing for example.  "Full lag" means about 2 seconds of lag, not minutes of inactivity.
        # C4SID_LOCK is mapped to Live's (Python) LOM API "Lock control surface to device" behavior.
        self.system_switch_functions = {
            C4SID_SPLIT: {"led_id": {C4SID_SPLIT: {"virtual_press_count": 0, "led_value": [0, 127]},
                                     C4SID_SPLIT + 1: {"virtual_press_count": 0, "led_value": [0, 127]},
                                     C4SID_SPLIT + 2: {"virtual_press_count": 0, "led_value": [0, 127]}},  "press_count": 0},
            C4SID_LOCK: {"led_id": {C4SID_LOCK: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_SPLIT_ERASE: {"led_id": {C4SID_SPLIT_ERASE: {"led_value": [0, 127]}}, "press_count": 0}
        }
        self.system_switch_assignments = {
            C4SID_MARKER: {"led_id": {C4SID_MARKER: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_TRACK: {"led_id": {C4SID_TRACK: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_CHANNEL_STRIP: {"led_id": {C4SID_CHANNEL_STRIP: {"led_value": [0, 127]}}, "press_count": 0},
            C4SID_FUNCTION: {"led_id": {C4SID_FUNCTION: {"led_value": [0, 127]}}, "press_count": 0}
        }

        self.__own_encoders = encoders  # why separate references? This reference is only used here in __init__
        self.__encoders = encoders  # why these __encoders too? This reference is used everywhere else
        # suspect the reason is because, at runtime, while this __init__ is running; the main_script here,
        # the caller, MackieC4, is still inside its own __init__ (and thus can't be referenced successfully yet?)
        # The encoders here though, are fully initialized and are successfully referenced

        # tell these encoders my self is now your controller
        for s in self.__own_encoders:
            s.set_encoder_controller(self)

        self.__eah = EncoderAssignmentHistory(main_script, self)
        self.__time_display = TimeDisplay(self)
        self.__display_update_lag_upper_bounds = [20, 10, 5, 0]
        self.__display_update_lag_upper_bounds_index = 0
        self.__display_update_lag_counter = 0
        self.__assignment_mode = C4M_CHANNEL_STRIP

        self.__last_assignment_mode = C4M_FUNCTION # don't initialize with C4M_USER
        self.__current_track_name = ''  # Live's Track Name of selected track
        self.selected_track = None  # Live's selected-Track Object
        self.__locked_device_track = None  # if script is not locked to a device, this property holds self.selected_track

        self.__ordered_plugin_parameters = []  # Live's DeviceParameters of __chosen_plugin (if exists)
        self.__device_provider = device_provider
        self.__chosen_plugin = None
        self.is_locked_to_device = False
        # self.__on_selected_track_changed.subject = self.song().view
        self.__device_listener_hit = False
        self.__on_device_changed.subject = self.__device_provider
        self.__on_is_locked_to_device_changed.subject = self.__device_provider

        self.__display_parameters = []

        # initialize to blank screen segments
        self.__display_parameters = [EncoderDisplaySegment(self, x) for x in range(NUM_ENCODERS)]

        self.encoder_name_display_state = [
            {
                "toggle": False,
                "last_toggle_time": 0.0,
                "scroll_pos": 0,
                "last_scroll_time": 0.0
            }
            for _ in range(NUM_ENCODERS)
        ]

        self.__filter_mst_trk = 0
        self.__filter_mst_trk_allow_audio = 0
        self.__last_send_messages = {
            LCD_ANGLED_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []},
            LCD_TOP_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []},
            LCD_MDL_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []},
            LCD_BTM_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}
        }

        song = self.song()
        tracks = song.visible_tracks + song.return_tracks
        selected_track = song.view.selected_track

        self.returns_switch = 0

        found = False
        index = -1
        for i, track in enumerate(tracks):
            if track == selected_track:
                self.track_changed(i)
                found = True
                index = i
                break
        if not found:# this means master track is selected when the song session is initializing
            index = len(tracks)
            self.track_changed(index)

        self.update_assignment_mode_leds()

        self.__shift_state = False
        self.__option_state = False
        self.__ctrl_state = False
        self.__alt_state = False

        self._last_undo_label = ""
        self._last_undo_label_time = 0

        self._last_redo_label = ""
        self._last_redo_label_time = 0

        self.clear_all_lcds()
        return

    def destroy(self):

        if self.main_script() is not None:
            self.sendGoodbyeScreen()
            self.clear_all_leds()
        MackieC4Component.destroy(self)

    def sendGoodbyeScreen(self):
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

    def request_rebuild_midi_map(self):
        MackieC4Component.request_rebuild_midi_map(self)

    def get_encoders(self):
        return self.__encoders


    # @listens("selected_track")
    # def __on_selected_track_changed(self):
    #     self.main_script().log_message("EC.__on_selected_track_changed: listener popped")
    #     # self.main_script().log_message("EC.__on_selected_track_changed: listener popped, calling self.main_script().track_change()")
    #     # self.main_script().track_change()

    @listens("device")
    def __on_device_changed(self):
        log_id = "EC.__on_device_changed: "
        d = self.__device_provider.provided_device
        self.__device_provider.clear_last_param_details()
        if liveobj_valid(d):
            track = self.__locked_device_track
            if liveobj_valid(track):
                # note: these listeners are in addition to the script's normal midi mapping listeners
                # they support the Parameter Single left and right button behavior (increment/decrement value of last changed device parameter)
                self.main_script().do_add_one_devices_listeners(d, track_name=track.name)
            else:
                track = self.__device_provider.device_track
                if liveobj_valid(track):
                    self.main_script().do_add_one_devices_listeners(d, track_name=track.name)
                else:
                    self.main_script().log_message(f"{log_id}listener popped, {d.name} is valid, but not selected_track, finding track")
                    track, index = self.find_devices_track(d)
                    if liveobj_valid(track):
                        self.selected_track = track
                        self.main_script().do_add_one_devices_listeners(d, track_name=track.name)
                    else:
                        msg = f"{log_id}listener popped, device is {d.name} but can't locate valid track reference. "
                        self.main_script().log_message(msg + "no device parameter listeners added, but something else will soon derail anyway")
            # self.main_script().log_message(f"{log_id}: listener popped, device changed to {d.name}")
            self.__device_listener_hit = True
            self.__update_chosen_plugin_device(d)
        else:
            self.main_script().log_message(f"{log_id}listener popped, but device not liveobj valid?")

    def find_devices_track(self, device):
        log_id = "EC.find_devices_track: "
        selected_track = self.song().view.selected_track
        if liveobj_valid(selected_track):
            tracks = self.song().visible_tracks + self.song().return_tracks
            selected_index = 0 # this track index should be the "local EAH database" index associated with the selected_track

            if selected_track == self.song().master_track:
                selected_index = len(tracks) # "one index past" the last valid regular + return tracks index
                devices = self.get_device_list(selected_track.devices)
                found = device in devices
                msg = f"{log_id}self.song().view.selected_track is master (i=={selected_index}) and {device.name} device was "
                if found:
                    self.main_script().log_message(f"{msg}found")
                    return selected_track, selected_index
                else:
                    self.main_script().log_message(f"{msg}NOT found, None returned")
                    return None
            else:
                if selected_track in tracks:
                    for i, track in enumerate(tracks):
                        if track == selected_track:
                            selected_index = i
                            break
                    devices  = self.get_device_list(selected_track.devices)
                    found = device in devices
                    msg = f"{log_id}self.song().view.selected_track is {selected_track.name} (i=={selected_index}) and {device.name} device was "
                    if found:
                        self.main_script().log_message(f"{msg}found")
                        return selected_track, selected_index
                    else:
                        self.main_script().log_message(f"{msg}NOT found, None returned")
                        return None, None
                else:
                    self.main_script().log_message(f"{log_id}self.song().view.selected_track is not master and not in visible or return tracks?")
                    return None, None
        else:
            self.main_script().log_message(f"{log_id}self.song().view.selected_track is not a valid Live object?")
            return selected_track


    def __update_chosen_plugin_device(self, device):
        log_id = "EC.__update_chosen_plugin_device: "
        self.__chosen_plugin = device  # in cases like a new midi track selected; device will == None here
        if not liveobj_valid(self.selected_track):
            self.main_script().log_message(f"{log_id}current selected_track is not valid, finding track")
            # if self.__chosen_plugin is not valid going in here, the found track coming out will never be valid either, something will soon bug out
            track, index = self.find_devices_track(self.__chosen_plugin)
            if liveobj_valid(track):
                self.selected_track = track
            else:
                self.main_script().log_message(f"{log_id}selected_track is still not valid, __reassign_encoder_parameters() will soon bug out")
        # else:
        #     self.main_script().log_message(f"{log_id}selected track is valid, rebuilding midi map normally")
        self.__reorder_parameters()
        self.__reassign_encoder_parameters()
        self.request_rebuild_midi_map()
        # nm = "None" if self.__chosen_plugin is None else self.__chosen_plugin.name
        # self.main_script().log_message(f"EC.__update_chosen_plugin_device: chosen_plugin changed to {nm}")

    @listens("is_locked_to_device")
    def __on_is_locked_to_device_changed(self):
        is_locked = self.__device_provider.surface_is_locked
        # dv = self.__chosen_plugin.name if self.__chosen_plugin is not None else "None"
        # if is_locked:
        #     self.main_script().log_message(f"EC.__on_is_locked_to_device_changed: listener popped, now locked to device {dv}")
        # else:
        #     self.main_script().log_message(f"EC.__on_is_locked_to_device_changed: listener popped, now unlocking from device {dv}")
        self.__locked_device_track = self.selected_track  # can't be locking (or unlocking) a device on an invalid "selected" track
        self.is_locked_to_device = is_locked

    def build_setup_database(self):
        # self.main_script().log_message("EC.build_setup_database: C4/building setup db")
        self.__eah.build_setup_database(self.song())        # self.track_count

        # self.main_script().log_message("EC.build_setup_database: C4.t_count after setup <{0}>".format(self.__eah.t_count))
        # self.main_script().log_message("EC.build_setup_database: C4.main_script().track_count after setup <{0}>".format(self.main_script().track_count))

        self.selected_track = self.song().view.selected_track
        devices_on_selected_trk = self.get_device_list(self.selected_track.devices)
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
            if len(devices_on_selected_trk) == 0:
                self.__update_chosen_plugin_device(None)
            else:
                self.song().view.select_device(devices_on_selected_trk[0])

        return

    def master_track_index(self):
        return self.__eah.master_track_index()

    def track_changed(self, track_index):
        log_id = "EC.track_changed: "
        self.selected_track = self.song().view.selected_track
        tracks = self.song().visible_tracks + self.song().return_tracks + (self.song().master_track,)
        try:
            j = tracks.index(self.selected_track)
        except ValueError:
            j = -1

        if liveobj_valid(self.selected_track):
            self.main_script().log_message(f"{log_id}track_index input is {track_index}, selected_track is {self.selected_track.name} at index {j}")
        else:
            self.main_script().log_message(f"{log_id}track_index input is {track_index}, but selected_track is not liveobj valid at index {j}")

        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track

        selected_device_index = self.__eah.track_changed(track_index)
        extended_device_list = self.get_device_list(self.selected_track.devices)
        device = None
        if len(extended_device_list) == 0:
            self.main_script().log_message(f"{log_id}no devices found on track {self.selected_track.name}")
            self.__eah.update_device_counter(track_index, 0)
        else:
            if selected_device_index > -1:
                if len(extended_device_list) > selected_device_index:
                    device = extended_device_list[selected_device_index]
                    if liveobj_valid(device):
                        self.main_script().log_message(f"{log_id}{device.name} found at index {selected_device_index}")
                    self.__eah.update_device_counter(track_index, len(extended_device_list))
                    self.main_script().log_message(f"{log_id}called __eah.update_device_counter({track_index}, {len(extended_device_list)})")
                # else something didn't get updated correctly at startup and/or when devices deleted?
                elif len(extended_device_list) > 0: # punt if we can
                    device = extended_device_list[0]
                    if liveobj_valid(device):
                        self.main_script().log_message(f"{log_id}{device.name} found at index 0 because {selected_device_index} is too big")
                    self.__eah.update_device_counter(track_index, len(extended_device_list))
                    self.main_script().log_message(f"{log_id}called __eah.update_device_counter({track_index}, {len(extended_device_list)})")
                else:
                    self.main_script().log_message(f"{log_id}len(extended_device_list) {len(extended_device_list)} < {selected_device_index} selected_device_index")
            else:
                # something isn't getting updated correctly at startup and/or when devices are deleted
                self.main_script().log_message("len(self.t_d_current) <= self.t_current")
                self.main_script().log_message("{0} <= {1}".format(len(self.__eah.t_d_current), self.__eah.t_current))

        if not self.is_locked_to_device:
            if liveobj_valid(device):
                self.__locked_device_track = self.selected_track
                self.main_script().log_message(f"{log_id}selected_track is now {self.selected_track.name} selecting device {device.name}")
                self.__device_listener_hit = False
                self.song().view.select_device(device) # this device selection might be redundant to Live
                if not self.__device_listener_hit:  # if this device selection didn't trigger Live listener notifications (yet?), update here now
                    self.main_script().log_message(f"{log_id}device listener hit not detected, manually updating local chosen device {device.name}")
                    self.__update_chosen_plugin_device(device)  # this device selection updates the state of this script
            else:
                self.main_script().log_message(f"{log_id}selected_track is now {self.selected_track.name} but no valid device found, self.__chosen_plugin == None")
                self.__update_chosen_plugin_device(device)  # device == None

        return

    def tracks_added(self, track_index, tracks):
        # does it matter that this code always adds these tracks here without accounting for each track's extended_device_list in the EAH arrays,
        # then only updates the local selected track? (using same update code as from self.track_deleted())
        self.__eah.tracks_added(track_index, tracks)
        self.__update_selected_track(track_index)

    def track_added(self, track_index):
        log_id = "EC.track_added: "
        self.selected_track = self.song().view.selected_track
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
        extended_device_list = self.get_device_list(self.selected_track.devices)
        self.__eah.track_added(track_index, extended_device_list)

        # This is a way to call a super-class method from a subclass with a method of the same name see def refresh_state() below (way, way below)
        MackieC4Component.refresh_state(self)
        device = None
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
            selected_device_index = self.__eah.get_selected_device_index()
            if selected_device_index > -1:
                if len(extended_device_list) > selected_device_index:
                    selected_device = extended_device_list[selected_device_index]
                    device = selected_device
                elif len(extended_device_list) > 0:
                    selected_device = extended_device_list[0]
                    self.__eah.set_selected_device_index(0)
                    device = selected_device

            if  liveobj_valid(device):
                self.__device_listener_hit = False
                self.song().view.select_device(device)
                if not self.__device_listener_hit:  # if this device selection didn't trigger Live listener notifications (yet?), update here now
                    self.main_script().log_message(f"{log_id}device listener hit not detected, manually updating local chosen device {device.name}")
                    self.__update_chosen_plugin_device(device)  # this device selection updates the state of this script
            else:
                self.__update_chosen_plugin_device(device)  # device == None
        return

    def tracks_deleted(self, track_index, tracks):
        self.__eah.tracks_deleted(track_index, tracks)
        self.__update_selected_track(track_index)

    def track_deleted(self, track_index):
        # log_id = "EC.track_deleted: "
        # self.main_script().log_message(f"{log_id}del tk idx before deleted track: {0}".format(track_index))
        self.__eah.track_deleted(track_index)
        self.__update_selected_track(track_index)

    def __update_selected_track(self, track_index):
        log_id = "EC.__update_selected_track: "
        track = self.song().view.selected_track
        if not liveobj_valid(track):
            self.main_script().log_message(f"{log_id}song().view.selected_track is not valid, neither is index {track_index}")
        self.selected_track = track
        if not self.is_locked_to_device:
            self.__locked_device_track = self.selected_track
        # self.main_script().log_message(f"{log_id}selected tk after: {0}".format(self.selected_track.name))
        self.refresh_state()

        extended_device_list = self.get_device_list(self.selected_track.devices)
        selected_device_index = self.__eah.get_selected_device_index()
        # self.main_script().log_message(f"{log_id}selected tk device index after: {0}".format(selected_device_index))
        # self.main_script().log_message("f"{log_id}nbr of devices on selected track after: {0}".format(len(extended_device_list)))
        device = None
        if not self.is_locked_to_device:

            if selected_device_index > -1:
                if len(extended_device_list) > selected_device_index:
                    selected_device = extended_device_list[selected_device_index]
                    device = selected_device
                elif len(extended_device_list) > 0:
                    selected_device = extended_device_list[0]
                    self.__eah.set_selected_device_index(0)
                    device = selected_device

            if liveobj_valid(device):
                self.__locked_device_track = self.selected_track
                self.__device_listener_hit = False
                self.song().view.select_device(device)
                if not self.__device_listener_hit:  # if this device selection didn't trigger Live listener notifications (yet?), update here now
                    self.main_script().log_message(f"{log_id}device listener hit not detected, manually updating local chosen device {device.name}")
                    self.__update_chosen_plugin_device(device)  # this device selection updates the state of this script
            else:
                self.__update_chosen_plugin_device(device)  # device == None

        return

    def device_added_deleted_or_changed(self, track, tid, type):
        log_id = "EC.device_added_deleted_or_changed: "
        updated_idx = -1
        # extended_device_list is the device list with enumerated/flattened rack devices
        # if a device is added to any unselected track, this extended device list is not populated here with the new device on the freshly selected track
        # devices cannot be updated or deleted from an unselected track, they can only be added to an unselected track. (by drag&drop, for example)
        extended_device_list = self.get_device_list(self.selected_track.devices)

        # Use a dictionary to map type to listener_type
        listener_types = {0: "normal", 1: "return", 2: "master"}.get(type, "None")

        if liveobj_valid(track):
            # log_msg = f"{log_id}processing device change-state of Track listener type <{listener_type}> on track <{track.name}> at index {tid}"
            # self.main_script().log_message(log_msg)
            if liveobj_changed(self.selected_track, track):
                sel_trk_nm = self.selected_track.name if liveobj_valid(self.selected_track) else "None"
                log_msg = f"{log_id}because input track <{track.name}> is not self.selected_track, "
                log_msg += f"updating self.selected_track to <{sel_trk_nm}> and calling self.track_changed({tid}) "
                self.main_script().log_message(log_msg + f"to update self.__eah before calling self.__eah.device_added_deleted_or_changed() below")
                self.selected_track = track
                self.track_changed(tid)
                # update the extended (flattened) device list for the changed selected Track
                extended_device_list = self.get_device_list(self.selected_track.devices)

            if liveobj_valid(self.selected_track):
                selected_device = self.selected_track.view.selected_device
                if liveobj_valid(selected_device):
                    log_msg = f"{log_id}track {self.selected_track.name} and device {selected_device.name} are valid"
                    self.main_script().log_message(log_msg)
                    current_selected_indexes = (x for x in range(len(extended_device_list))
                                                if extended_device_list[x] == selected_device)
                    selected_device_idx = next(current_selected_indexes, -1)
                    extended_device_list = self.get_device_list(self.selected_track.devices)
                    if selected_device_idx < 0 < len(extended_device_list):
                        selected_device_idx = len(extended_device_list) - 1
                    updated_idx = self.__eah.device_added_deleted_or_changed(extended_device_list, selected_device, selected_device_idx)

            device = None
            if not self.is_locked_to_device:
                if updated_idx == -1:
                    device = None
                    # might happen if track with no devices deleted, and the next selected track also has no devices?
                    self.__eah.set_selected_device_index(-1)  # danger -1 is OOB for an index
                    # self.main_script().log_message("{0}__chosen_plugin is now None because no EAH updated index".format(log_id))
                elif len(extended_device_list) > updated_idx:
                    device = extended_device_list[updated_idx]
                    self.__eah.set_selected_device_index(updated_idx)
                    # log_msg = f"{log_id}__chosen_plugin is now {self.__chosen_plugin.name} because updated index is <{updated_idx}>"
                    # self.main_script().log_message(log_msg)
                elif len(extended_device_list) > 0:  # evaluation never reaches here if updated_idx == 0
                    device = extended_device_list[0]
                    self.__eah.set_selected_device_index(0)
                    # self.main_script().log_message("{0}ONLY device __chosen_plugin is now {1} because don't know".format(log_id, self.__chosen_plugin.name))
                else:
                    # might happen if track with no devices deleted, and the next selected track also has no devices?
                    self.__eah.set_selected_device_index(-1)  # danger -1 is OOB for an index
                    # self.main_script().log_message("{0}}__chosen_plugin is now None because else-fell-through".format(log_id))

                if liveobj_valid(device):
                    self.__locked_device_track = self.selected_track
                    self.__device_listener_hit = False
                    self.song().view.select_device(device) # this should notify device listeners via "device provider"
                    if not self.__device_listener_hit:  # if this device selection didn't trigger Live listener notifications (yet?), update here now
                        self.main_script().log_message(f"{log_id}device listener hit not detected, manually updating local chosen device {device.name}")
                        self.__update_chosen_plugin_device(device)  # this device selection updates the state of this script
                else:
                    self.__update_chosen_plugin_device(device) # device == None

        new_device_count_track = len(extended_device_list)
        # self.main_script().log_message("{0}device count AFTER update <{1}>".format(log_id, new_device_count_track))

        if new_device_count_track > 0:
            for i, device in enumerate(extended_device_list):
                log_msg = f"{log_id}device at extended device list index <{i}> is"
                if liveobj_valid(device):
                    # self.main_script().log_message(f"{log_msg} <{device.name}>"
                    pass
                else:
                    log_msg = f"{log_msg} not liveobj_valid"
                    self.main_script().log_message(log_msg)
        # else:
            # self.main_script().log_message("{0}new_device_count_track was NOT > 0, NOT enumerating devices for log".format(log_id))

    def toggle_devices(self, cc_no, cc_value):
        """any clockwise turn cc_value activates device represented by cc_no, counterclockwise turns deactivate device."""
        # Track - Channel Strip mode is the only mode that shows banks of devices to toggle on and off like this
        # Track - Devices mode shows the "chosen device" parameters, one of which toggles the "chosen device" on and off like this
        if self.__assignment_mode == C4M_CHANNEL_STRIP:

            device_list = self.song().view.selected_track.devices
            extended_device_list = self.get_device_list(device_list)

            # Calculate the index of the first device in the current device bank
            current_device_bank_track = self.__eah.get_selected_device_bank_index()
            bank_start_index = (current_device_bank_track) * 8

            # Ensure that bank_start_index is non-negative
            if bank_start_index < 0:
                self.main_script().log_message("EC.toggle_devices: negative device bank index protection triggered")
                bank_start_index = 0
            # if not locked to device, always allow
            # if locked to device, only allow if locked device's track is currently selected in Live
            allow_toggle = True if (not self.is_locked_to_device or
                                    (self.is_locked_to_device and self.__locked_device_track == self.song().view.selected_track)) else False
            if allow_toggle:
                bank_end = bank_start_index + 8
                for i, device in enumerate(extended_device_list):
                    # Get the 'bank index' of the encoder mapped to this device
                    encoder_bank_index = i % 8
                    encoder_cc_no = 8 + encoder_bank_index # i.e. row_01_encoders [8,9,10,11,12,13,14,15]

                    # Check if the first parameter (always the device On/Off toggle switch parameter) is enabled and toggle it accordingly
                    parameter = device.parameters[0]
                    if liveobj_valid(parameter) and parameter.is_enabled:
                        ccw_turn = cc_value > 64
                        if ccw_turn and cc_no == encoder_cc_no:
                            if bank_start_index <= i < bank_end:
                                parameter.value = False
                        elif not ccw_turn and cc_no == encoder_cc_no:
                            if bank_start_index <= i < bank_end:
                                parameter.value = True
                    else:
                        if not liveobj_valid(parameter):
                            self.main_script().log_message("EC.toggle_devices: assumption issue: device.parameters[0] was not liveobj_valid")


    def assignment_mode(self):
        return self.__assignment_mode

    def last_assignment_mode(self):
        return self.__last_assignment_mode

    # self.system_switch_functions = {
    #     C4SID_SPLIT: {"led_id": {C4SID_SPLIT: {"virtual_press_count": 0, "led_value": [0, 127]},
    #                              1: {"virtual_press_count": 0, "led_value": [0, 127]},
    #                              2: {"virtual_press_count": 0, "led_value": [0, 127]}},
    #                   "press_count": 0},
    #     C4SID_LOCK: {"led_id": {C4SID_LOCK: {"led_value": [0, 127]}},
    #                  "press_count": 0},
    #     C4SID_SPLIT_ERASE: {"led_id": {C4SID_SPLIT_ERASE: {"led_value": [0, 127]}},
    #                         "press_count": 0}
    # }
    # Currently,
    # C4SID_SPLIT_ERASE is the only system switch (button) with no associated behavior mapped
    # C4SID_SPLIT behavior only affects "display updates" (feedback to leds and led rings)...
    #    when the song is NOT playing:
    #    C4SID_SPLIT controls the amount of intentional lag applied between "on display update timer" calls and actual C4 display updates
    #    all split button leds OFF means full lag amount (send display update midi messages once every 20 times "on display update timer" is called)
    #    all split button leds ON means no lag applied (send display update midi messages every time "on display update timer" is called, 1 for 1)
    # C4SID_LOCK is mapped to Live's (Python) LOM API "Lock control surface to device" behavior.
    def handle_system_switch_ids(self, switch_id):
        switch_dict = self.system_switch_functions[switch_id]
        switch_dict["press_count"] += 1
        led_dict = switch_dict["led_id"]
        out_value = 0
        send_feedback = True
        if switch_id == C4SID_SPLIT:
            offset = switch_dict["press_count"] % len(self.__display_update_lag_upper_bounds)  #  4 states repeat == 1, 2, 3 leds ON, and "all leds OFF"
            if offset > 0: # self.__display_update_lag_upper_bounds_index
                inner_offset = offset - 1
                led_dict[inner_offset]["virtual_press_count"] += 1
            else:
                if led_dict[C4SID_SPLIT]["virtual_press_count"] % 2 > 0:
                    led_dict[C4SID_SPLIT]["virtual_press_count"] += 1
                if led_dict[C4SID_SPLIT + 1]["virtual_press_count"] % 2 > 0:
                    led_dict[C4SID_SPLIT + 1]["virtual_press_count"] += 1
                if led_dict[C4SID_SPLIT + 2]["virtual_press_count"] % 2 > 0:
                    led_dict[C4SID_SPLIT + 2]["virtual_press_count"] += 1
            self.update_system_switch_leds() # also sends Lock and Erase led "updates"
            send_feedback = False
            # else out_value = 0
            # as the press count cycles up here, the amount of lag cycles down
            # all Split leds OFF is max lag, and all 3 Split leds ON is zero lag (full speed of "on display update timer" (every 100 ms))
            self.__display_update_lag_upper_bounds_index = offset

        elif switch_id == C4SID_LOCK:
            out_value = led_dict[C4SID_LOCK]["led_value"][switch_dict["press_count"] % 2]
            if out_value > 0:
                self.lock_to_device(self.__device_provider.provided_device)
            else:
                self.unlock_from_device()
            self.one_display_update()
        elif switch_id == C4SID_SPLIT_ERASE:
            out_value = led_dict[C4SID_SPLIT_ERASE]["led_value"][switch_dict["press_count"] % 2]
        else:
            self.main_script().log_message(f"EC.handle_system_switch_ids: unknown system switch id {switch_id}, no feedback generated")
            send_feedback = False

        if send_feedback:
            self.send_midi((NOTE_ON_STATUS, switch_id, out_value))

    def update_system_switch_leds(self):
        if self.__assignment_mode != C4M_USER:
            switch_dict = self.system_switch_functions[C4SID_SPLIT]
            led_dict = switch_dict["led_id"]

            toggle = led_dict[C4SID_SPLIT]["virtual_press_count"] % 2
            out_value_00 = led_dict[C4SID_SPLIT]["led_value"][toggle]
            toggle = led_dict[C4SID_SPLIT + 1]["virtual_press_count"] % 2
            out_value_01 = led_dict[C4SID_SPLIT + 1]["led_value"][toggle]
            toggle = led_dict[C4SID_SPLIT + 2]["virtual_press_count"] % 2
            out_value_02 = led_dict[C4SID_SPLIT + 2]["led_value"][toggle]
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT, out_value_00))
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT + 1, out_value_01))
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT + 2, out_value_02))

            switch_dict = self.system_switch_functions[C4SID_LOCK]
            led_dict = switch_dict["led_id"]
            toggle = switch_dict["press_count"] % 2
            lock_value = led_dict[C4SID_LOCK]["led_value"][toggle]
            self.send_midi((NOTE_ON_STATUS, C4SID_LOCK, lock_value))

            switch_dict = self.system_switch_functions[C4SID_SPLIT_ERASE]
            led_dict = switch_dict["led_id"]
            toggle = switch_dict["press_count"] % 2
            erase_value = led_dict[C4SID_SPLIT_ERASE]["led_value"][toggle]
            self.send_midi((NOTE_ON_STATUS, C4SID_SPLIT_ERASE, erase_value))

            # for btn_id in self.system_switch_assignments:
            #     switch_dict = self.system_switch_assignments[btn_id]
            #     led_dict = switch_dict["led_id"]
            #     toggle = switch_dict["press_count"] % 2
            #     assignment_value = led_dict[btn_id]["led_value"][toggle]
            #     self.send_midi((NOTE_ON_STATUS, btn_id, assignment_value))

   # no wrap around: stop moving left at track 0, stop moving right at master track
    def handle_bank_switch_ids(self, switch_id):
        """ works in all modes """
        log_id = "EC.handle_bank_switch_ids: "
        # is_assignment_mode = "True" if self.__assignment_mode == C4M_CHANNEL_STRIP else "False"
        # self.main_script().log_message(f"{log_id}the current assignment mode is C4M_CHANNEL_STRIP: <{is_assignment_mode}>")
        current_bank_nbr = self.__eah.get_current_track_device_parameter_bank_nbr()
        update_self = False
        if switch_id == C4SID_BANK_LEFT:
            if current_bank_nbr > 0:
                current_bank_nbr -= 1
                update_self = True
        elif switch_id == C4SID_BANK_RIGHT:
            max_bank_nbr = self.__eah.get_max_current_track_device_parameter_bank_nbr() - 1
            if current_bank_nbr < max_bank_nbr:
                current_bank_nbr += 1
                update_self = True
        elif self.__assignment_mode == C4M_CHANNEL_STRIP or self.__assignment_mode == C4M_PLUGINS:
            if liveobj_valid(self.__chosen_plugin):
                last_param_name = self.__device_provider.get_last_param_value_change_name()
                if liveobj_valid(self.__chosen_plugin.parameters):
                    # self.main_script().log_message(f"{log_id}looking for original param name <{last_param_name}> in device <{self.__chosen_plugin.name}>")
                    cp = v3_util.get_parameter_by_name(last_param_name, self.__chosen_plugin)  # checks for match with p.original_name
                    if not liveobj_valid(cp):
                        # self.main_script().log_message(f"{log_id}looking for param name <{last_param_name}> in device <{self.__chosen_plugin.name}>")
                        chosen_param = song_util.get_parameter_by_name(last_param_name, self.__chosen_plugin) # checks for match with p.name
                    else:
                        chosen_param = cp

                    if liveobj_valid(chosen_param):
                        if isinstance(chosen_param, tuple):
                            self.main_script().log_message(f"{log_id}v3_util.get_parameter_by_name() returned a valid tuple")
                            param = chosen_param[0]
                            if not liveobj_valid(param):
                                self.main_script().log_message(f"{log_id}but obj at index 0 was not liveobj_valid?")
                        else:
                            param = chosen_param

                        if liveobj_valid(param):
                            modifier = 1.0
                            if param.value < 1.0 and param.max == 1.0:
                                modifier = 0.01

                            if switch_id == C4SID_SINGLE_LEFT:
                                inc_amt = -1 * modifier
                            elif switch_id == C4SID_SINGLE_RIGHT:
                                inc_amt = 1 * modifier
                            else:
                                inc_amt = None
                            # self.main_script().log_message(f"{log_id}updating value {param.value} by {inc_amt}")
                            song_util.update_or_cycle_parameter_value(param, inc_amt)
                            update_self = True
                            # self.main_script().log_message(f"{log_id}updated value {param.value}")
                        else:
                            self.main_script().log_message(f"{log_id}param returned from get_parameter_by_name() was not liveobj_valid?")
                    # else:
                    #     # after a device change, but before a device parameter value change, execution passes through here
                    #     self.main_script().log_message(f"{log_id}unable to get_parameter_by_name() neither returned parameter was liveobj_valid?")
                else:
                    self.main_script().log_message(f"{log_id}can't get parameters from valid device <{self.__chosen_plugin.name}>?")

        if update_self:
            self.__eah.set_current_track_device_parameter_bank_nbr(current_bank_nbr)
            self.__reassign_encoder_parameters()
            self.request_rebuild_midi_map()
            self.one_display_update()

    def handle_assignment_switch_ids(self, switch_id):
        """the 4 Assignment buttons on the C4, which handle the mode switching"""
        # C4 assignment.marker button == C4M_USER mode
        update_self = False
        led_dict = self.system_switch_assignments[switch_id]
        if switch_id == C4SID_MARKER:
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_MARKER]:  # C4M_USER:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_MARKER]  # C4M_USER
                update_self = True

        # C4 assignment.track button == C4M_PLUGINS mode
        elif switch_id == C4SID_TRACK:
            # only switch mode and set "last mode" when the mode actually changes
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_TRACK]:  # C4M_PLUGINS:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_TRACK]  # C4M_PLUGINS

                if self.__eah.get_selected_device_index() == 0 and self.__eah.get_max_device_count() > 0:
                    self.song().view.select_device(self.get_device_list(self.selected_track.devices)[0])
                update_self = True

        # C4 assignment.chan_strip button == C4M_CHANNEL_STRIP mode
        elif switch_id == C4SID_CHANNEL_STRIP:
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_CHANNEL_STRIP]:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_CHANNEL_STRIP]
                update_self = True

        # C4 assignment.function button == C4M_FUNCTION mode
        elif switch_id == C4SID_FUNCTION:
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_FUNCTION]:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_FUNCTION]
                update_self = True

        if update_self:
            for button_id in self.system_switch_assignments.keys():
                button_dict = self.system_switch_assignments[button_id]
                if switch_id == button_id:
                    if button_dict["press_count"] % 2 == 0:
                        button_dict["press_count"] += 1
                else:
                    if button_dict["press_count"] % 2 > 0:
                        button_dict["press_count"] += 1

            if not self.__assignment_mode == C4M_USER:
                self.update_system_switch_leds()
            self.update_assignment_mode_leds()
            self.__reassign_encoder_parameters()
            self.request_rebuild_midi_map()
            # need to wipe USER mode LCD screen displays when we leave USER mode, but not too soon, wait 20 ms
            self.one_delayed_display_update(.020)
        # else don't update self because self is already in this mode

    def handle_slot_nav_switch_ids(self, switch_id):
        """ "slot navigation" (arrow up 🔼/down 🔽) switches between Devices in all modes except User """
        if self.__assignment_mode != button_id_to_assignment_mode[C4SID_MARKER]:
            current_trk_device_index = self.__eah.get_selected_device_index()
            max_trk_device_index = self.__eah.get_max_device_count() - 1
            update_self = False
            if switch_id == C4SID_SLOT_DOWN:
                if current_trk_device_index > 0:
                    current_trk_device_index -= 1
                    update_self = True
            elif switch_id == C4SID_SLOT_UP:
                if current_trk_device_index < max_trk_device_index:
                    current_trk_device_index += 1
                    update_self = True

            if not self.is_locked_to_device and update_self:
                self.__eah.set_selected_device_index(current_trk_device_index)
                extended_device_list = self.get_device_list(self.selected_track.devices)
                if len(extended_device_list) > current_trk_device_index:
                    current_selected_device = extended_device_list[current_trk_device_index]
                elif len(extended_device_list) > 0:
                    current_selected_device = extended_device_list[0]
                    self.__eah.set_selected_device_index(0)
                else:
                    current_selected_device = None
                    self.__eah.set_selected_device_index(-1)

                if liveobj_valid(current_selected_device):
                    self.song().view.select_device(current_selected_device)
                else:
                    self.__update_chosen_plugin_device(current_selected_device) # current_selected_device == None


    def handle_modifier_switch_ids(self, switch_id, value):
        if switch_id == C4SID_SHIFT:
            self.__shift_state = value
            self.main_script().set_shift_is_pressed(value)
        elif switch_id == C4SID_OPTION:
            self.__option_state = value
            self.main_script().set_option_is_pressed(value)
        elif switch_id == C4SID_CONTROL:
            self.__ctrl_state = value
            self.main_script().set_ctrl_is_pressed(value)
        elif switch_id == C4SID_ALT:
            self.__alt_state = value
            self.main_script().set_alt_is_pressed(value)

    def _show_assignment_mode_change_message(self):
        new_mode = self.__assignment_mode
        old_mode = self.__last_assignment_mode
        new_name = new_mode
        old_name = old_mode
        if new_name == 0:
            new_name = "SEQUENCER"
            if old_mode == 1:
                old_name = "DEVICE CHAIN"
            elif old_mode == 2:
                old_name = "CHANNEL STRIP"
            else:# 3:
                old_name = "MAIN FUNCTIONS"
        if new_name == 1:
            new_name = "DEVICE CHAIN"
            if old_mode == 2:
                old_name = "CHANNEL STRIP"
            elif old_mode == 3:
                old_name = "MAIN FUNCTIONS"
            else:# 0
                old_name = "SEQUENCER"
        elif new_name == 2:
            new_name = "CHANNEL STRIP"
            if old_mode == 3:
                old_name = "MAIN FUNCTIONS"
            elif old_mode == 0:
                old_name = "SEQUENCER"
            else:# 1
                old_name = "DEVICE CHAIN"
        elif new_name == 3:
            new_name = "MAIN FUNCTIONS"
            if old_mode == 0:
                old_name = "SEQUENCER"
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

        if self.__assignment_mode == C4M_USER:
            # going INTO USER mode these feedback messages pass through the Max patch before it starts processing messages
            # self.main_script().log_message("EC.update_assignment_mode_leds: entering USER mode")
            for i in range(C4SID_MARKER, C4SID_FUNCTION + 1) :
                self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_OFF))

        elif self.__last_assignment_mode == C4M_USER:
            # leaving USER mode, messages from here would be processed by the Max patch
            # which would generate the feedback messages going directly to the C4 (before it receives the "button 22" signal sent below)
            # blindly telling the Max patch to toggle the assignment LED states from here would rarely leave the LEDs
            # accurately depicting the script's new current "assignment mode"
            delay_assignment_led_update = True
            # self.main_script().log_message("EC.update_assignment_mode_leds: leaving USER mode")
            # self.main_script().show_message("mode change from {} to {}".format(old_name, new_name))
        else:
            # log_msg = f"EC.update_assignment_mode_leds: changing non USER mode {old_name} ({old_mode}) to {new_name} ({new_mode})"
            # self.main_script().log_message(log_msg)
            # not in USER mode these feedback messages pass through the Max patch
            current_mode_id = assignment_mode_to_button_id[self.__assignment_mode]
            for i in assignment_mode_switch_ids:
                if i == current_mode_id:
                    self.main_script().log_message(f"EC.update_assignment_mode_leds: led id {i} ON")
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_ON))
                else:
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_OFF))

        if delay_assignment_led_update:
            # self.main_script().log_message("EC.update_assignment_mode_leds: updating assignment LEDs after leaving USER mode")
            current_mode_id = assignment_mode_to_button_id[self.__assignment_mode]
            done = False
            for i in range(C4SID_SPLIT, C4SID_FUNCTION + 1):
                if i < C4SID_MARKER and not done:
                    self.update_system_switch_leds()
                    done = True
                if i == current_mode_id:
                    self.main_script().log_message(f"EC.update_assignment_mode_leds: led id {i} ON")
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_ON))
                else:
                    self.send_midi((NOTE_ON_STATUS, i, BUTTON_STATE_OFF))

        self._show_assignment_mode_change_message()

    def handle_vpot_rotation(self, vpot_index, cc_value):
        """For any encoder that is not midi mapped to some control in Live where we want to control some other function of Live.
           For any encoder that is midi mapped to some control in Live, handling here is a bad idea"""

        if self.__assignment_mode == C4M_FUNCTION:
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
        elif self.__assignment_mode == C4M_CHANNEL_STRIP:
            if vpot_index in row_01_encoders:
                self.toggle_devices(vpot_index, cc_value)
            # else: address of midi mapped or unused encoder in C4M_CHANNEL_STRIP mode

        self.one_display_update()

    def unsolo_all_functionality(self, mode_name, vpot_index):
        mode_function = self.mode_functions.get(mode_name)
        if mode_function:
            if mode_name == "handle_pressed_v_pot":
                song_util.unsolo_all(self)
            # elif mode_name == "reassign_encoder_parameters":
            #     encoders_to_display_text = {vpot_index: ('all', 'unsolo')}
            #     return encoders_to_display_text
            elif mode_name == "on_update_display_timer":
                if song_util.any_soloed_track(self):
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
                if self.__time_display.TimeDisplay__show_beat_time:
                    time_string = str(self.song().get_current_beats_song_time()) + ' '
                    upper_string2 += 'Bar:Bt:Sb:Tik '
                    lower_string2 += time_string
                else:
                    time_string = str(self.song().get_current_smpte_song_time(self.__time_display.TimeDisplay__smpt_format)) + ' '
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
                    if self.__filter_mst_trk:
                        state = self.selected_track.mixer_device.crossfade_assign
                        value_to_send = None
                        if state == 0:
                            value_to_send = 'Mixer.Crossfade.A'
                        elif state == 1:
                            value_to_send = 'Mixer.Crossfade.Off'
                        elif state == 2:
                            value_to_send = 'Mixer.Crossfade.B'
                        track_util._crossfade_toggle_value(self,value_to_send)  # vpot push for Crossfade assign A/B/off on Audio or Return tracks
                    else:
                        param = self.__encoders[vpot_index].v_pot_parameter()
                        param.value = param.default_value  # button press == jump to default value for Crossfader on Master track
                    self.one_display_update(force=True)

            elif mode_name == "reassign_encoder_parameters":
                vpot_display_text = EncoderDisplaySegment(self, vpot_index)
                vpot_display_text.set_encoder_controller(self)
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                if self.selected_track.has_audio_output:
                    if self.__filter_mst_trk != 1:
                        vpot_display_text.set_text(self.selected_track.mixer_device.crossfader,'X-Fade')  # Crossfader on Master track
                        vpot_param = (self.selected_track.mixer_device.crossfader, VPOT_DISPLAY_BOOST_CUT)

                xfade_vpot = self.__encoders[vpot_index]
                xfade_vpot.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

            elif mode_name == "on_update_display_timer":
                if liveobj_valid(self.selected_track):
                    if self.selected_track.has_audio_output:
                        if self.__filter_mst_trk:
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

    def handle_pressed_v_pot(self, vpot_index):
        """ 'encoder button' /vpot push clicks"""
        encoder_index = vpot_index - C4SID_VPOT_PUSH_BASE  # 0x20  32
        selected_device_bank_index = self.__eah.get_selected_device_bank_index()
        old_selected_bank = selected_device_bank_index
        max_device_bank_index = self.__eah.get_selected_device_bank_count() - 1
        if self.__assignment_mode == C4M_CHANNEL_STRIP:
            is_armable_track_selected = track_util.can_be_armed(self.selected_track)

            if encoder_index in row_00_encoders:
                encoder_04_index = 3
                encoder_05_index = 4
                encoder_06_index = 5
                encoder_07_index = 6
                encoder_08_index = 7
                update_self = False

                # group track fold toggle, also groups from within
                if encoder_index == encoder_04_index:
                    track_util.toggle_fold(self.selected_track)

                if encoder_index == encoder_07_index:
                    if selected_device_bank_index > 0:
                        selected_device_bank_index -= 1
                        update_self = True
                    else:
                        self.main_script().log_message("can't decrement selected_device_bank_index: already bank 0")
                elif encoder_index == encoder_08_index:
                    if selected_device_bank_index < max_device_bank_index:
                        selected_device_bank_index += 1
                        update_self = True
                    else:
                        self.main_script().log_message("can't increment selected_device_bank_index: already on last bank")

                if update_self:
                    # log_msg = f"EC.handle_pressed_v_pot: updating selected device bank index from <{old_selected_bank}> to <{selected_device_bank_index}>"
                    # self.main_script().log_message(log_msg)
                    self.__eah.set_selected_device_bank_index(selected_device_bank_index)
                    self.__reassign_encoder_parameters()
                    self.one_display_update()

            elif encoder_index in row_01_encoders:
                # (row 2 "index" is 01) these encoders represent devices 1 - 8 in the device chain on the selected track in C4M_CHANNEL_STRIP mode
                # behavior implemented is: encoder button press == automatically switch to Track/Plugins mode
                # AND IF not already locked to a device
                # switch to Track/Plugins mode  and update "self.__chosen_plugin" to the device represented by the encoder clicked
                # ELSE
                # switch to Track/Plugins mode using "self.__chosen_plugin" the "device to which the script is locked"
                self.handle_assignment_switch_ids(C4SID_TRACK)

                device_bank_offset = int(NUM_ENCODERS_ONE_ROW * selected_device_bank_index)
                device_offset = vpot_index - C4SID_VPOT_PUSH_BASE - NUM_ENCODERS_ONE_ROW + device_bank_offset
                extended_device_list = self.get_device_list(self.selected_track.devices)
                if not self.is_locked_to_device:
                    if len(extended_device_list) > device_offset:  # if the calculated offset is valid device index
                        self.__eah.set_selected_device_index(encoder_index - NUM_ENCODERS_ONE_ROW + device_bank_offset)
                        device = extended_device_list[device_offset]
                        if liveobj_valid(device):
                            self.song().view.select_device(device)
                        else:
                            self.__update_chosen_plugin_device(device) # device == None
                    else:
                        msg = f"EC.handle_pressed_v_pot: can't update __chosen_plugin: the calculated device_offset {device_offset} is NOT a valid device index"
                        self.main_script().log_message(msg)
                        self.__update_chosen_plugin_device(None) # ???
            elif encoder_index in row_02_encoders:
                # these encoders represent Sends 1 - 8 in C4M_CHANNEL_STRIP mode
                param = self.__filter_mst_trk_allow_audio and self.__encoders[encoder_index].v_pot_parameter()
                if liveobj_valid(param):
                    if isinstance(param, int):  # PyCharm says 'param' is an int based on the
                        #                         self.__encoders[encoder_index].v_pot_parameter() assignment above.
                        #                         int also doesn't have a default_value?
                        param.value = 0  # if param is never actually an int when it isn't None, this assignment just satisfies PyCharm
                    else:
                        param.value = param.default_value  # button press == jump to default value of Send
                else:
                    self.main_script().log_message("EC.handle_pressed_v_pot: can't update param.value to default: None object")
            elif encoder_index in row_03_encoders:

                encoder_27_index = 26  # X-Fade
                encoder_28_index = 27  # Solo
                encoder_29_index = 28  # Rec Arm
                encoder_30_index = 29  # Mute
                s = next(x for x in self.__encoders if x.vpot_index() == encoder_index)

                if encoder_index < encoder_27_index:
                    # these encoders are the four < encoder_29_index, left half of bottom row, sends 9 - 12
                    param = self.__filter_mst_trk_allow_audio and self.__encoders[encoder_index].v_pot_parameter()
                    if liveobj_valid(param):
                        if isinstance(param, int):
                            param.value = 0
                        else:
                            param.value = param.default_value  # button press == jump to default value of Send
                    else:
                        self.main_script().log_message("EC.handle_pressed_v_pot: can't update param.value to default: param not liveobj_valid()")

                elif encoder_index == encoder_27_index:
                    self.xfade("handle_pressed_v_pot", encoder_index)

                elif encoder_index == encoder_28_index:
                    if self.__filter_mst_trk:
                        if self.selected_track.solo is not True:
                            self.selected_track.solo = True
                        else:
                            self.selected_track.solo = False
                    else:
                        self.main_script().show_message("track cannot be soloed")
                        s.unlight_vpot_leds()

                elif encoder_index == encoder_29_index:
                    if self.__filter_mst_trk:
                        if is_armable_track_selected:
                            if self.selected_track.arm is not True:
                                self.selected_track.arm = True
                            else:
                                self.selected_track.arm = False
                        else:
                            self.main_script().show_message("track cannot be armed")
                            s.unlight_vpot_leds()

                elif encoder_index == encoder_30_index:
                    if self.__filter_mst_trk:
                        if self.selected_track.mute:
                            self.selected_track.mute = False
                        else:
                            self.selected_track.mute = True
                    else:
                        self.main_script().show_message("master track cannot be muted")
                        # s.unlight_vpot_leds()  # why only this encoder ring moved to on_update_display_timer

                elif encoder_index > encoder_30_index:
                    #  encoder 31 is "Pan"
                    #  encoder 32 is "Volume"
                    param = self.__encoders[encoder_index].v_pot_parameter()
                    param.value = param.default_value  # button press == jump to default value of Pan or Vol
            self.one_display_update(force=True)
        elif self.__assignment_mode == C4M_PLUGINS:
            encoder_04_index = 3
            encoder_07_index = 6
            encoder_08_index = 7
            current_device_track = self.__eah.get_selected_device_index()
            current_parameter_bank_track = self.__eah.get_current_track_device_parameter_bank_nbr(current_device_track)
            current_track_device_parameter_bank_nbr_changed = False
            # self.main_script().log_message("current_parameter_bank_track: {0}".format(current_parameter_bank_track))
            stop = len(self.__display_parameters) + SETUP_DB_DEVICE_BANK_SIZE  # always 40?
            display_params_range = range(SETUP_DB_DEVICE_BANK_SIZE, stop)  # display_params_range always 8 - 39?
            # suspect display_params_range is supposed to protect against "short" parameter lists < 24
            # when self.__display_parameters is always 32 EncoderDisplaySegments now
            # we might need to check the length of the actual parameter list of the selected device
            update_self = False

            # group track fold toggle, also groups from within
            if encoder_index == encoder_04_index:
                track_util.toggle_fold(self.selected_track)
                update_self = True

            if encoder_index == encoder_07_index:
                if current_parameter_bank_track > 0:
                    current_parameter_bank_track -= 1
                    # self.main_script().log_message("self.t_d_p_bank_current[self.t_current]: {0}".format(self.__eah.get_selected_device_index()))
                    update_self = True
                    current_track_device_parameter_bank_nbr_changed = True
                # else:
                #     self.main_script().log_message("can't decrement current_parameter_bank_track: already bank 0")
            elif encoder_index == encoder_08_index:
                current_track_device_preset_bank = current_parameter_bank_track
                # self.main_script().log_message("current_track_device_preset_bank: {0}".format(current_track_device_preset_bank))
                track_device_preset_bank_count = self.__eah.get_max_current_track_device_parameter_bank_nbr(current_device_track)
                # self.main_script().log_message("track_device_preset_bank_count: {0}".format(track_device_preset_bank_count))
                if current_track_device_preset_bank < track_device_preset_bank_count - 1:
                    current_parameter_bank_track += 1
                    update_self = True
                    current_track_device_parameter_bank_nbr_changed = True
                # else:
                #     self.main_script().log_message("can't increment current_parameter_bank_track: already last bank")
            # should be encoders 9 - 32 (on each param page), but stopping short on last/only (short is < 24) parameter page
            elif encoder_index in display_params_range:
                # if a device has less than 24 parameters exposed on this page, param will be (None, '    ')
                param = self.__encoders[encoder_index].v_pot_parameter()
                if liveobj_valid(param):
                    # if param is not tuple:
                    try:
                        if param.is_enabled:
                            if util.is_parameter_quantized(param, current_device_track):  # for stepped params or those that only have a limited range
                                toggle_or_cycle_parameter_value(param)
                            else:
                                # button press == jump to default value of device parameter
                                param.value = param.default_value
                    except (RuntimeError, AttributeError):
                        # There is no default value available for this type of parameter
                        # 'NoneType' object has no attribute 'default_value'
                        pass

            if update_self:
                # old_t_d_p_bank_nbr = self.__eah.get_current_track_device_parameter_bank_nbr()
                # log_msg = f"EC.handle_pressed_v_pot: updating current_track_device_parameter_bank_nbr from <{old_t_d_p_bank_nbr}> to {current_parameter_bank_track}"
                # self.main_script().log_message(log_msg)
                if current_track_device_parameter_bank_nbr_changed:
                    self.__eah.set_current_track_device_parameter_bank_nbr(current_parameter_bank_track)
                self.__reassign_encoder_parameters()
                self.request_rebuild_midi_map()

            self.one_display_update()

        elif self.__assignment_mode == C4M_FUNCTION:
            encoder_01_index = 0  # follow
            encoder_02_index = 1  # loop
            encoder_03_index = 2  # Detail / Clip
            encoder_04_index = 3  # Session / Arrange mode
            encoder_05_index = 4  # browser visible on/off
            encoder_06_index = 5  # unsolo all
            encoder_07_index = 6  # unmute all
            encoder_08_index = 7  # BTA
            encoder_09_index = 8  # Undo
            encoder_10_index = 9  # Redo
            encoder_11_index = 10  # unarm all
            encoder_12_index = 11  # SPP
            # encoder_13_index is covered / occupied by SPP from 12
            encoder_14_index = 13
            encoder_16_index = 15  # Scroll / Zoom
            encoder_17_index = 16  # Metronome
            encoder_18_index = 17  # re-enable automation
            encoder_19_index = 18  # stop scrub
            encoder_25_index = 24  # Stop
            encoder_26_index = 25  # Play
            encoder_27_index = 26  # continue play
            encoder_28_index = 27  # overdub
            s = next(x for x in self.__encoders if x.vpot_index() == encoder_index)

            if encoder_index == encoder_01_index:
                song_util.toggle_follow(self)
                if self.song().view.follow_song:
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_02_index:
                if self.song().loop:
                    song_util.toggle_loop(self)
                    s.unlight_vpot_leds()
                else:
                    song_util.toggle_loop(self)
                    s.show_full_enlighted_poti()

            elif encoder_index == encoder_03_index:
                song_util.toggle_detail_sub_view(self)
                if self.application().view.is_view_visible('Detail/Clip'):
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_04_index:
                song_util.toggle_session_arranger_is_visible(self)
                if song_util.is_arranger_visible(self):
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_05_index:
                song_util.toggle_browser_is_visible(self)
                if song_util.is_browser_visible(self):
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_06_index:
                self.unsolo_all_functionality("handle_pressed_v_pot", encoder_index)

            elif encoder_index == encoder_07_index:
                song_util.unmute_all(self)

            elif encoder_index == encoder_08_index:
                song_util.toggle_back_to_arranger(self)

            elif encoder_index == encoder_09_index:  # Undo
                if self.song().can_undo:
                    result = self.song().undo()
                    clean = result.removeprefix("Undo ").strip() if result else ""
                    self._last_redo_label = clean
                    self._last_redo_label_time = time.time()
                else:
                    s.unlight_vpot_leds()

            elif encoder_index == encoder_10_index:  # Redo
                if self.song().can_redo:
                    result = self.song().redo()
                    clean = result.removeprefix("Redo ").strip() if result else ""
                    self._last_undo_label = clean
                    self._last_undo_label_time = time.time()

            elif encoder_index == encoder_11_index:
                song_util.unarm_all_button(self)

            # toggle between BEAT and SMPTE mode for SPP
            elif encoder_index == encoder_12_index:
                self.beat_pointer("handle_pressed_v_pot", encoder_index)

            elif encoder_index == encoder_16_index:
                nav = Live.Application.Application.View.NavDirection
                if self.application().view.is_view_visible('Arranger'):
                    self.application().view.zoom_view(nav.left, '', self.alt_is_pressed())

            elif encoder_index == encoder_17_index:
                self.song().metronome = not self.song().metronome

            elif s.vpot_index() == encoder_18_index:
                if self.song().re_enable_automation_enabled:
                    """Returns true if some automated parameter has been overriden"""
                    self.song().re_enable_automation()

            elif s.vpot_index() == encoder_19_index:
                if self.song().view.detail_clip:
                    self.song().view.detail_clip.stop_scrub()

            #  capture_midi placeholder

            elif encoder_index == encoder_25_index:
                self.song().stop_playing()
                self.__encoders[encoder_26_index].unlight_vpot_leds()
                self.__encoders[encoder_27_index].unlight_vpot_leds()
            elif encoder_index == encoder_26_index:
                if self.shift_is_pressed():
                    if not self.song().is_playing:
                        self.song().continue_playing()
                    else:
                        self.song().stop_playing()
                elif self.ctrl_is_pressed():
                    self.song().play_selection()
                else:
                    self.song().start_playing()
                s.show_full_enlighted_poti()
            elif encoder_index == encoder_27_index:
                self.song().continue_playing()
                s.show_full_enlighted_poti()
            elif encoder_index == encoder_28_index:
                if self.song().overdub:
                    s.unlight_vpot_leds()  # if lit (because overdub), turn off
                else:
                    s.show_full_enlighted_poti()
                self.song().overdub = not self.song().overdub

            self.one_display_update()

    def __send_parameter(self, vpot_index):
        """ Returns the send parameter that is assigned to the given encoder as a tuple (param, param.name) """
        if vpot_index < len(self.song().view.selected_track.mixer_device.sends):
            p = self.song().view.selected_track.mixer_device.sends[vpot_index]
            #  self.main_script().log_message("Param name <{0}>".format(p.name))
            return p, p.name
        else:
            # The Song doesn't have this many sends
            return None, '      '

    def __plugin_parameter(self, vpot_index):
        """ Return the plugin parameter that is assigned to the given encoder as a tuple (param, param.name) """

        parameters = self.__ordered_plugin_parameters
        if vpot_index in encoder_range:
            current_track_device_preset_bank = self.__eah.get_current_track_device_parameter_bank_nbr()
            preset_bank_index = current_track_device_preset_bank * SETUP_DB_PARAM_BANK_SIZE
            current_track_param_count = len(parameters)
            is_param_index = current_track_param_count > vpot_index + preset_bank_index
            if is_param_index:
                p = parameters[vpot_index + preset_bank_index]
                return p

            # The device doesn't have this many parameters
            return None, '      '
        else: # theoretically not possible, vpot_index should never be outside the encoder_range
            return None, 'PPppPP'

    def __reorder_parameters(self):
        result = []
        if liveobj_valid(self.__chosen_plugin):
            device_class_name = self.__chosen_plugin.class_name

            if device_class_name in DEVICE_DICT:
                device_banks = DEVICE_DICT[device_class_name]

                for device_bank_index, bank in enumerate(device_banks):
                    for param_bank_index, param_name in enumerate(bank):
                        parameter = get_parameter_by_name(self.__chosen_plugin, param_name)

                        if not parameter:
                            param_index = param_bank_index + (SETUP_DB_DEVICE_BANK_SIZE * device_bank_index)
                            if len(self.__chosen_plugin.parameters) > param_index:
                                parameter = self.__chosen_plugin.parameters[param_index]

                        result.append((parameter, parameter.name if parameter else None))

            else:
                result = [(p, p.name) for p in self.__chosen_plugin.parameters]

        self.__ordered_plugin_parameters = result

        num_params = len(self.__ordered_plugin_parameters)
        nbr_of_full_pages = min(num_params // SETUP_DB_PARAM_BANK_SIZE, SETUP_DB_MAX_PARAM_BANKS)
        nbr_of_remainders = num_params % SETUP_DB_PARAM_BANK_SIZE

        if nbr_of_remainders > 0:
            nbr_of_full_pages = min(nbr_of_full_pages + 1, SETUP_DB_MAX_PARAM_BANKS)

        self.__eah.set_max_current_track_device_parameter_bank_nbr(nbr_of_full_pages)

    @staticmethod
    def get_on_off_parameter(device=None):
        if liveobj_valid(device):
            return find_if(lambda p: p.original_name.startswith('Device On') and liveobj_valid(p) and p.is_enabled, device.__ordered_plugin_parameters)
        return device # device == None

    def __reassign_encoder_parameters(self):
        """ Reevaluate all v-pot -> parameter assignments """
        self.__filter_mst_trk = 0
        self.__filter_mst_trk_allow_audio = 0
        if not liveobj_valid(self.selected_track):
            self.main_script().log_message(f"EC.__reassign_encoder_parameters: self.selected track is not valid, blowing up soon")
    #     # execution ends up here after deleting some tracks, bug hunting we are
    # else:
        self.__current_track_name = self.selected_track.name if liveobj_valid(self.selected_track) else "None"
        extended_device_list = self.get_device_list(self.selected_track.devices)
        if self.selected_track != self.song().master_track:
            self.__filter_mst_trk = 1  # a regular track is selected (not master track)
            if self.selected_track.has_audio_output:
                self.__filter_mst_trk_allow_audio = 1  # a regular track with audio is selected (not master)

        self.__display_parameters = []
        encoder_01_index = 0
        encoder_02_index = 1
        encoder_03_index = 2
        encoder_04_index = 3
        encoder_05_index = 4
        encoder_06_index = 5
        encoder_07_index = 6
        encoder_08_index = 7
        encoder_09_index = 8
        encoder_10_index = 9
        encoder_11_index = 10
        encoder_12_index = 11
        encoder_13_index = 12
        encoder_14_index = 13
        encoder_16_index = 14
        encoder_17_index = 16  # Metronome in Function mode
        encoder_18_index = 17
        encoder_19_index = 18
        encoder_21_index = 20
        encoder_22_index = 21
        encoder_24_index = 23
        encoder_25_index = 24
        encoder_26_index = 25
        encoder_27_index = 26
        encoder_28_index = 27
        encoder_29_index = 28
        encoder_30_index = 29
        encoder_31_index = 30
        encoder_32_index = 31
        if self.__assignment_mode == C4M_CHANNEL_STRIP:

            is_armable_track_selected = track_util.can_be_armed(self.selected_track)

            current_nbr_of_devices_on_selected_track = len(extended_device_list)
            self.__eah.set_max_device_count(current_nbr_of_devices_on_selected_track)

            nbr_of_full_device_pages = int(current_nbr_of_devices_on_selected_track / SETUP_DB_DEVICE_BANK_SIZE)  # / 8
            nbr_of_remainder_devices = int(current_nbr_of_devices_on_selected_track % SETUP_DB_DEVICE_BANK_SIZE)
            if nbr_of_full_device_pages >= SETUP_DB_MAX_DEVICE_BANKS:
                nbr_of_full_device_pages = SETUP_DB_MAX_DEVICE_BANKS
            elif nbr_of_full_device_pages < 0:
                nbr_of_full_device_pages = 0
                self.main_script().log_message("EC.__reassign_encoder_parameters: Not possible, right? and yet I am logged")

            if nbr_of_full_device_pages == 0 and nbr_of_remainder_devices > 0:
                nbr_of_full_device_pages = 1
            elif nbr_of_remainder_devices > 0:  # 0 < nbr_of_full_device_pages <= SETUP_DB_MAX_DEVICE_BANKS  #  <= 16
                nbr_of_full_device_pages += 1

            # this is the max (channel mode) device page count (based on the current number of devices on the selected track)
            self.__eah.set_selected_device_bank_count(nbr_of_full_device_pages)

            # the current selected bank should already be updated (and accurate)?
            current_device_bank_track = self.__eah.get_selected_device_bank_index()

            for s in self.__encoders:
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)
                vpot_display_text.set_encoder_controller(self)  # also sets associated Encoder reference
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

                if s_index in row_00_encoders:
                    if s_index == encoder_07_index:
                        if current_device_bank_track > 0:
                            vpot_display_text.set_text('<<Bank', 'Device')
                            s.show_full_enlighted_poti()
                        else:
                            s.unlight_vpot_leds()
                    elif s_index == encoder_08_index:
                        if current_device_bank_track < nbr_of_full_device_pages - 1:
                            vpot_display_text.set_text('Bank>>', 'Device')
                            s.show_full_enlighted_poti()
                        else:
                            s.unlight_vpot_leds()
                    else:
                        s.unlight_vpot_leds()
                    self.__display_parameters.append(vpot_display_text)

                elif s_index in row_01_encoders:

                    row_index = s_index - SETUP_DB_DEVICE_BANK_SIZE  # row_index == "index of" s_index in row_01_encoders range
                    current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)

                    # display part
                    if row_index + current_encoder_bank_offset < self.__eah.get_max_device_count():
                        encoder_index_in_row = row_index + int(current_encoder_bank_offset)
                        if encoder_index_in_row < len(extended_device_list):
                            device_name = extended_device_list[encoder_index_in_row].name

                            # device_name in bottom row, blanks on top (top text blocked across full LCD)
                            vpot_display_text.set_text(device_name, '')

                        else:
                            vpot_display_text.set_text('dvcNme', 'No')  # could just leave as default blank spaces

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                    # to light up vpot ring for active devices
                    # Get list of active devices
                    active_devices = [device for device in extended_device_list if device.is_active]

                    # add listener for devices
                    for device in extended_device_list:
                        device_encoder_index_in_row = extended_device_list.index(device)
                        try:
                            extended_device_list[device_encoder_index_in_row].add_is_active_listener(self._update_vpot_leds_for_device_toggle)
                        except RuntimeError:
                            pass

                    # Loop over active devices and update their LEDs once initially
                    active_device_encoder_indices = [extended_device_list.index(device) for device in active_devices]
                    for encoder_index in range(len(self.__encoders)):
                        if encoder_index in row_01_encoders:
                            row_index = encoder_index - SETUP_DB_DEVICE_BANK_SIZE
                            current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)
                            per_encoder_index_in_row = row_index + current_encoder_bank_offset
                            if per_encoder_index_in_row < len(extended_device_list):
                                if per_encoder_index_in_row in active_device_encoder_indices:
                                    self.__encoders[encoder_index].show_full_enlighted_poti()
                                else:
                                    self.__encoders[encoder_index].unlight_vpot_leds()
                            else:
                                self.__encoders[encoder_index].unlight_vpot_leds()

                elif s_index < encoder_27_index:
                    # changed from 29, which means that the 12th send will not be shown on the C4, but who needs 12 sends that anyway?
                    # if you want to get back to 12 sends being shown, out-comment all encoder_28_index stuff and change "elif s_index < encoder_28_index" to 29
                    if self.__filter_mst_trk_allow_audio:
                        send_param = self.__send_parameter(s_index - SETUP_DB_DEVICE_BANK_SIZE * 2)
                        vpot_param = (send_param[0], VPOT_DISPLAY_WRAP)
                        format_nbr = s_index % NUM_ENCODERS_ONE_ROW
                        if s_index in row_03_encoders:
                            format_nbr += NUM_ENCODERS_ONE_ROW
                        # encoder 17 index is (16 % 8) = send 0
                        # encoder 25 index is (24 % 8) = send 8 (8 == 0 when modulo is 8)
                        if liveobj_valid(send_param[0]):
                            vpot_display_text.set_text(send_param[0], send_param[1])
                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                elif s_index == encoder_27_index:
                    self.xfade("reassign_encoder_parameters", s.vpot_index())

                elif s_index == encoder_28_index:
                    self.returns_switch = 0
                    if self.__filter_mst_trk and not self.selected_track.solo:
                        vpot_display_text.set_text(None, 'Solo')
                    else:
                        vpot_display_text.set_text(None, 'Solo' if self.__filter_mst_trk else 'Master')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                elif s_index == encoder_29_index:
                    self.returns_switch = 0
                    if self.__filter_mst_trk:
                        vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                        if is_armable_track_selected:
                            is_armed = self.selected_track.arm
                            vpot_display_text.set_text(is_armed, 'RecArm')  # this is static text
                        else:
                            vpot_display_text.set_text('Never', 'RecArm')
                    else:
                        vpot_display_text.set_text(None, 'Master')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                elif s_index == encoder_30_index:
                    if self.__filter_mst_trk:
                        is_muted = self.selected_track.mute
                        vpot_display_text.set_text(is_muted, 'Mute')

                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_31_index:
                    if self.selected_track.has_audio_output:
                        vpot_display_text.set_text(self.selected_track.mixer_device.panning, 'Pan')  # static text
                        vpot_param = (self.selected_track.mixer_device.panning, VPOT_DISPLAY_BOOST_CUT)  # the actual param

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_32_index:
                    if self.selected_track.has_audio_output:
                        vpot_display_text.set_text(self.selected_track.mixer_device.volume, 'Volume')
                        vpot_param = (self.selected_track.mixer_device.volume, VPOT_DISPLAY_WRAP)
                    else:
                        vpot_display_text.set_text('', '')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_PLUGINS:
            current_device_bank_param_track = self.__eah.get_current_track_device_parameter_bank_nbr()
            max_device_bank_param_track = self.__eah.get_max_current_track_device_parameter_bank_nbr()
            for s in self.__encoders:
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)
                vpot_display_text.set_encoder_controller(self)  # also sets associated Encoder reference
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

                if s_index == encoder_07_index:
                    if self.__chosen_plugin is None:
                        s.unlight_vpot_leds()
                    elif current_device_bank_param_track > 0:
                        vpot_display_text.set_text('<<  - ', 'PrvBnk')
                        s.show_full_enlighted_poti()
                    else:
                        vpot_display_text.set_text(' Bank ', 'NoPrev')
                        s.unlight_vpot_leds()
                elif s_index == encoder_08_index:
                    if self.__chosen_plugin is None:
                        s.unlight_vpot_leds()
                    elif current_device_bank_param_track < max_device_bank_param_track - 1:
                        vpot_display_text.set_text('  + >>', 'NxtBnk')
                        s.show_full_enlighted_poti()
                    else:
                        vpot_display_text.set_text(' Bank ', 'NoNext')
                        s.unlight_vpot_leds()
                else:
                    # these are the 24 encoders from 9 to 32. Some devices do not have more than 1 or 2 parameters
                    # we are only concerned with the 24 encoders on the current "device bank page"
                    plugin_param = self.__plugin_parameter(s_index - SETUP_DB_DEVICE_BANK_SIZE)
                    if plugin_param is not None:
                        vpot_param = (plugin_param[0], VPOT_DISPLAY_WRAP)
                        # parameter name in top display row, param value in bottom row
                        if liveobj_valid(plugin_param[0]):  # then it is a DeviceParameter object
                            vpot_display_text.set_text(plugin_param[0], plugin_param[1])

                if self.selected_track.is_frozen:
                    # disconnect encoder from param mapping, display now shows blank values reinforcing track frozen status.
                    s.set_v_pot_parameter(None,None)
                else:
                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])

                self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_FUNCTION:
            encoders_to_display_text = {
                encoder_01_index: ('unfllw', 'follow'),
                encoder_02_index: ('on/off', 'Loop'),
                encoder_03_index: ('Detail', 'Clip/'),
                encoder_04_index: ('Arrang', 'Sessn'),
                encoder_05_index: ('on/off', 'Browsr'),
                encoder_06_index: ('all', 'unsolo'),
                encoder_07_index: ('all', 'unmute'),
                encoder_08_index: ('Arrang', 'Back 2'),
                encoder_11_index: ('all', 'unarm'),
                encoder_17_index: ('nome  ', 'Metro '),
                encoder_18_index: ('Autmtn', 'Renabl'),
                encoder_19_index: ('Clip  ', 'Scrub '),
                encoder_22_index: (None, 'BPM   '),
                encoder_28_index: ('on/off', 'Ovrdub'),
            }

            for s in self.__encoders:
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)
                vpot_display_text.set_encoder_controller(self)  # also sets associated Encoder reference

                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

                if s_index in encoders_to_display_text:
                    display_text = encoders_to_display_text[s_index]
                    if display_text[0] is not None:
                        vpot_display_text.set_text(display_text[0], display_text[1])
                    else:
                        vpot_display_text.set_upper_text(display_text[1])
                elif s.vpot_index() == encoder_09_index:
                    vpot_display_text.set_upper_text_and_alt('NoUndo', 'Undo  ')
                elif s.vpot_index() == encoder_10_index:
                    vpot_display_text.set_upper_text_and_alt('NoRedo', 'Redo  ')

                #  capture_midi

                elif s.vpot_index() == encoder_25_index:
                    if self.song().is_playing:
                        vpot_display_text.set_text(' Stop ', ' Song ')
                    else:
                        vpot_display_text.set_text(' Stop ', ' Song ')
                elif s.vpot_index() == encoder_26_index:
                    if not self.song().is_playing:
                        vpot_display_text.set_text(' Play ', ' Song ')
                    else:
                        vpot_display_text.set_text(' Play ', ' Song ')
                elif s.vpot_index() == encoder_27_index:
                    if not self.song().is_playing:
                        vpot_display_text.set_text('contin', ' Song ')
                    else:
                        vpot_display_text.set_text('contin', ' Song ')

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_USER:
            # need to rebuild the midi map for every encoder (disconnect from all parameters)
            for s in self.__encoders:
                s.unlight_vpot_leds()
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)
                vpot_display_text.set_encoder_controller(self)  # also sets associated Encoder reference

                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            # don't actively listen for updates in USER mode
            for device in extended_device_list:
                device_encoder_index_in_row = extended_device_list.index(device)
                try:
                    extended_device_list[device_encoder_index_in_row].remove_is_active_listener(self._update_vpot_leds_for_device_toggle)
                except RuntimeError:
                    pass

            # display these once only here because the Max sequencer handles its own display in C4M_USER mode
            # users see these instructions displayed when the Max sequencer is NOT connected,
            # and when it is connected but MIDI bandwidth is bottle-necked and slow
            top_line = 'MackieC4Pro remote script User mode'.center(NUM_CHARS_PER_DISPLAY_LINE)
            bottom_line = 'Switching to Max Sequencer patch control'.center(NUM_CHARS_PER_DISPLAY_LINE)
            self.send_display_string(LCD_ANGLED_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
            self.send_display_string(LCD_ANGLED_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)
            top_line = 'Press and Hold the Marker button again'.center(NUM_CHARS_PER_DISPLAY_LINE)
            bottom_line = 'Then Press the Lock button to Exit USER mode and'.center(NUM_CHARS_PER_DISPLAY_LINE)
            self.send_display_string(LCD_TOP_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
            self.send_display_string(LCD_TOP_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)
            top_line = 'Return to the previous remote script mode. All other'.center(NUM_CHARS_PER_DISPLAY_LINE)
            bottom_line = 'button and pot control functions pass to the Max patch'.center(NUM_CHARS_PER_DISPLAY_LINE)
            self.send_display_string(LCD_MDL_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
            self.send_display_string(LCD_MDL_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)
            top_line = 'Press and Hold Marker then Press Lock'.center(NUM_CHARS_PER_DISPLAY_LINE)
            bottom_line = 'to exit USER mode'.center(NUM_CHARS_PER_DISPLAY_LINE)
            self.send_display_string(LCD_BTM_FLAT_ADDRESS, top_line, LCD_TOP_ROW_OFFSET)
            self.send_display_string(LCD_BTM_FLAT_ADDRESS, bottom_line, LCD_BOTTOM_ROW_OFFSET)

        self.one_display_update(force=True)
        return

    def _update_vpot_leds_for_device_toggle(self):
        extended_device_list = self.get_device_list(self.selected_track.devices)
        current_device_bank_track = self.__eah.get_selected_device_bank_index()

        for s in self.__encoders:
            s_index = s.vpot_index()

            if s_index in row_01_encoders:
                row_index = s_index - SETUP_DB_DEVICE_BANK_SIZE
                current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)

                if row_index + current_encoder_bank_offset < self.__eah.get_max_device_count():
                    device_index = row_index + current_encoder_bank_offset
                    if device_index < len(extended_device_list):
                        device = extended_device_list[device_index]
                        device_encoder_index = row_index + NUM_ENCODERS_ONE_ROW

                        if device.is_active:
                            self.__encoders[device_encoder_index].show_full_enlighted_poti()
                        else:
                            self.__encoders[device_encoder_index].unlight_vpot_leds()

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

    def on_update_display_timer(self):
        """Called by Live every 100 ms. This is the original "real time" device-display update callback method"""

        if self.song().is_playing:
            self.__do_display_update()
        elif self.__display_lag_timer_bang():
            self.__do_display_update()


    def one_delayed_display_update(self, delay_secs=.050, force=False): # 50 ms
        time.sleep(delay_secs)
        self.one_display_update(force=force)

    def one_display_update(self, force=False):
        self.__do_display_update(force=force)

    def __display_lag_timer_bang(self):
        # (when song is NOT playing) count to _upper_bounds[bounds_index] before returning True and resetting the count
        max_lag = self.__display_update_lag_upper_bounds[self.__display_update_lag_upper_bounds_index]
        if self.__display_update_lag_counter < max_lag:
            self.__display_update_lag_counter += 1
            return False
        else:
            self.__display_update_lag_counter = 0
            return True

    def __do_display_update(self, force=False):
        """force means send the generated LCD screen display update messages even if they match the previous update messages sent"""
        upper_string1 = ''
        lower_string1 = ''
        lower_string1a = ''
        lower_string1b = ''
        upper_string2 = ''
        lower_string2 = ''
        upper_string3 = ''
        lower_string3 = ''
        upper_string4 = ''
        lower_string4 = ''

        encoder_27_index = 26
        encoder_28_index = 27
        encoder_29_index = 28
        encoder_30_index = 29
        encoder_31_index = 30
        encoder_32_index = 31
        # so_many_spaces = '                                                       '
        selected_track = self.__locked_device_track  # == self.selected_track when not locked
        if self.__assignment_mode == C4M_USER:
            # no display updates in this mode
            return
        elif self.__assignment_mode == C4M_CHANNEL_STRIP:

            is_group_track = track_util.is_group_track(selected_track)
            is_grouped = track_util.is_grouped(selected_track)
            is_folded = track_util.is_folded(selected_track) if liveobj_valid(selected_track) else False
            is_view_visible_session = self.application().view.is_view_visible('Session')
            is_view_visible_arranger = self.application().view.is_view_visible('Arranger')
            if self.is_locked_to_device and liveobj_valid(self.__chosen_plugin):
                selected_device_name = adjust_string(self.__chosen_plugin.name, 22)
            elif liveobj_valid(self.__chosen_plugin):
                selected_device_name = adjust_string(self.__chosen_plugin.name, 22)
            else:  # not locked or valid
                selected_device_name = '                      '  # length: 22

            # shows "fold" or "unfold" or nothing depending on if group track or grouped track
            if is_group_track or is_grouped:
                fold_text = 'unfold' if is_folded else 'fold'
                upper_string1 += '------ Track ------- {} ---------------'.format(fold_text)
            else:
                upper_string1 += '------ Track -------       ---------------'

            # 'selected track' name, centered over the first 3 encoders in top row, also indicates frozen tracks
            if liveobj_valid(selected_track):
                lower_string1 += adjust_string(selected_track.name, 12)
                if self.is_locked_to_device:
                    if selected_track.is_frozen:
                        # can you lock to a device on a frozen track? (where you can't change any (frozen) device parameter values)
                        lower_string1 += 'Frzn+Lck'
                    else:
                        lower_string1 += '-Locked-'
                elif selected_track.is_frozen:
                    lower_string1 += '-Frozen-'
                else: # not locked or frozen
                    lower_string1 = adjust_string(selected_track.name, 20)
            else:
                lower_string1 += adjust_string('invalid Track object', 20)

            if is_view_visible_session:
                group_text = ' Group ' if (is_group_track or is_grouped) else '       '
                lower_string1 += group_text
            elif is_view_visible_arranger:
                lower_string1 += ' Track '

            lower_string1 += adjust_string(selected_device_name, 15)

            # This text 'covers' display segments over all 8 encoders in the second row
            upper_string2 += '----------------------- Devices -----------------------'  # length 55
            # todo MS maybe try to visualize Racks/Groups here by using |  |  ?

            for t in encoder_range:
                try:
                    text_for_display = next(x for x in self.__display_parameters if (x.filter_index(t)))
                except StopIteration:
                    text_for_display = EncoderDisplaySegment(self, t)
                    text_for_display.set_text('zzzzzz', 'ZZZZZZ')

                u_alt_text = text_for_display.get_upper_text()
                l_alt_text = text_for_display.get_lower_text()

                if t in range(6, NUM_ENCODERS_ONE_ROW):
                    upper_string1 += ''.join([adjust_string(u_alt_text, 6), ' '])
                    lower_string1 += ''.join([adjust_string(str(l_alt_text), 6), ' '])
                elif t in row_01_encoders:
                    l_alt2_text = self.get_scrolling_display_text(l_alt_text, t)
                    lower_string2 += adjust_string(l_alt2_text, 6) + ' '

                elif t in row_02_encoders:
                    upper_string3 += ''.join([adjust_string(u_alt_text, 6), ' '])
                    lower_string3 += ''.join([adjust_string(str(l_alt_text), 6), ' '])
                elif t in row_03_encoders:
                    if t < encoder_27_index:
                        lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])

                    if t == encoder_27_index:
                        upper, lower = self.xfade("on_update_display_timer", t, u_alt_text, l_alt_text)
                        upper_string4 += upper
                        lower_string4 += lower

                    if t == encoder_28_index:
                        if liveobj_valid(selected_track):
                            if self.__filter_mst_trk:
                                if selected_track.solo:
                                    l_alt_text = "ON"
                                    self.__encoders[encoder_28_index].show_full_enlighted_poti()
                                else:
                                    l_alt_text = "OFF"
                                    self.__encoders[encoder_28_index].unlight_vpot_leds()
                            else:
                                l_alt_text = "NoSolo"

                        lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])

                    elif t == encoder_29_index:
                        if liveobj_valid(selected_track):
                            if selected_track.can_be_armed:
                                if selected_track.arm:
                                    l_alt_text = "ON"
                                    self.__encoders[encoder_29_index].show_full_enlighted_poti()
                                else:
                                    l_alt_text = "OFF"
                                    self.__encoders[encoder_29_index].unlight_vpot_leds()
                            else:
                                l_alt_text = "No Arm"

                        lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])

                    elif t == encoder_30_index:
                        if selected_track != self.song().master_track and liveobj_valid(selected_track):
                            if selected_track.mute:
                                l_alt_text = "ON"
                                self.__encoders[encoder_30_index].show_full_enlighted_poti()
                            else:
                                l_alt_text = "OFF"
                                self.__encoders[encoder_30_index].unlight_vpot_leds()
                            lower_string4 += adjust_string(l_alt_text, 6)

                        else:
                            lower_string4 += adjust_string(l_alt_text, 6)
                        lower_string4 += ' '
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])

                    elif t == encoder_31_index:
                        lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])

                    elif t == encoder_32_index:
                        lower_string4 += ''.join([adjust_string(l_alt_text, 6), ' '])
                        upper_string4 += ''.join([adjust_string(u_alt_text, 6), ' '])

        so_many_spaces = '                                                       '

        if self.__assignment_mode == C4M_PLUGINS:

            t_d_idx = self.__eah.get_selected_device_index()
            add_tail = False
            if self.is_locked_to_device and liveobj_valid(self.__chosen_plugin):
                upper_string1 += f"------ Track --- LOCKED to Device {t_d_idx}"
                add_tail = True
            elif liveobj_valid(self.__chosen_plugin):
                upper_string1 += f"------ Track ------- ----- Device {t_d_idx}"
                add_tail = True
            else:  # not locked or valid
                upper_string1 +=  "------ Track ------- --No--Device----------"
            if add_tail:
                if t_d_idx > 99:
                    upper_string1 += ' --- '
                else:
                    upper_string1 += ' ---- ' if t_d_idx > 9 else ' ----- '
            # self.main_script().log_message(f"device index is {t_d_idx} ")


            if liveobj_valid(selected_track):
                track_name = selected_track.name
                # lower_string1a += f"{adjust_string(track_name, 12)}(Frozen)" if self.selected_track.is_frozen else adjust_string(track_name, 20)
                lower_string1a += " " + adjust_string(track_name, 11)
                if not self.is_locked_to_device and not selected_track.is_frozen:
                    lower_string1a = adjust_string(selected_track.name, 20)
                elif selected_track.is_frozen:
                    lower_string1a += "-Frozen-"
            else:
                lower_string1a += adjust_string('invalid Track object', 20)

            lower_string1a = self.pad_right_if_less(lower_string1a, max_length=27)

            if not liveobj_valid(self.__chosen_plugin):
                # blank everything out
                upper_string1 += '             '
                lower_string1b += '                                   '
                lower_string1 += lower_string1a + lower_string1b
                upper_string2 += '               NO DEVICES ON THIS TRACK                '
                lower_string2 += so_many_spaces
                upper_string3 += so_many_spaces
                lower_string3 += so_many_spaces
                upper_string4 += so_many_spaces
                lower_string4 += so_many_spaces
            else:
                device_name = '  '
                if self.is_locked_to_device:
                    device_name = self.__chosen_plugin.name
                elif t_d_idx > -1:
                    extended_device_list = self.get_device_list(selected_track.devices)
                    if liveobj_valid(selected_track) and len(extended_device_list) > t_d_idx:
                        if liveobj_valid(extended_device_list[t_d_idx]):
                            device_name = extended_device_list[t_d_idx].name
                        else:
                            device_name = f"trk{t_d_idx}: " + selected_track.name  # is "blanks" better?
                    else:
                        # is "blanks" better? ("new" group track with no devices just two grouped tracks landed here)
                        device_name = "trk: " + selected_track.name
                # else:
                #     self.main_script().log_message(f"Current Track Device List length too short for index: name display blank over device index {t_d_idx}")

                lower_string1b = str(device_name) # adjust_string(str(device_name), 20).center(20)
                if self.is_locked_to_device:
                    if selected_track.is_frozen:
                        lower_string1b += ' FL'
                    else:
                        lower_string1b += ' Lk'
                elif selected_track.is_frozen:
                    lower_string1b += ' Fz'
                #else: # not locked or frozen
                lower_string1 += lower_string1a + adjust_string(str(lower_string1b), 20).center(20)
                # make sure there is room for control text <<Bank and Bank>>
                lower_string1 = self.pad_right_if_less(lower_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - len('<<BankBank>>'))
                if self.is_locked_to_device:
                    upper_string1 = self.pad_right_if_less(upper_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - len('-Params Bank-'))
                # else:
                #     self.pad_right_if_less(upper_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - 7)
                upper_string1 += '-Params Bank-'
                for t in encoder_range:
                    try:
                        text_for_display = self.__display_parameters[t]  # assumes always 32
                    except IndexError:
                        text_for_display = EncoderDisplaySegment(self, t)
                        text_for_display.set_text('---', ' X ')

                    u_raw_text = text_for_display.get_upper_text()
                    l_raw_text = text_for_display.get_lower_text()

                    # change the next 2 lines from get_scrolling_display_text to get_alternating_display_text to stop scrolling and just switch between 123456 and 789101112
                    u_alt_text = self.get_scrolling_display_text(u_raw_text, t)
                    l_alt_text = self.get_scrolling_display_text(l_raw_text, t)

                    if t in range(6, NUM_ENCODERS_ONE_ROW):
                        lower_string1 += adjust_string(str(l_alt_text), 6) + ' '
                    elif t in row_01_encoders:
                        upper_string2 += adjust_string(u_alt_text, 6) + ' '
                        lower_string2 += adjust_string(str(l_alt_text), 6) + ' '
                    elif t in row_02_encoders:
                        upper_string3 += adjust_string(u_alt_text, 6) + ' '
                        lower_string3 += adjust_string(str(l_alt_text), 6) + ' '
                    elif t in row_03_encoders:
                        upper_string4 += adjust_string(u_alt_text, 6) + ' '
                        lower_string4 += adjust_string(str(l_alt_text), 6) + ' '

        elif self.__assignment_mode == C4M_FUNCTION:

            encoder_06_index = 5  # unsolo all
            encoder_07_index = 6  # unmute all
            encoder_08_index = 7  # BTA
            encoder_09_index = 8
            encoder_10_index = 9
            encoder_11_index = 10
            encoder_12_index = 11
            # encoder_13_index is covered / occupied by SPP from 12
            encoder_14_index = 12  # because 12 is occupied, we still need 12 otherwise everything be shifted over
            encoder_15_index = 13
            encoder_16_index = 14
            encoder_17_index = 16  # Metronome
            encoder_18_index = 17  # re-enable automation
            encoder_19_index = 18  # scrub clip
            encoder_20_index = 19  # scroll clip
            encoder_21_index = 20  # zoom clip
            encoder_22_index = 21  # BPM
            encoder_25_index = 24
            encoder_26_index = 25
            encoder_27_index = 26
            for e in self.__encoders:
                try:
                    dspl_sgmt = next(x for x in self.__display_parameters if x.vpot_index() == e.vpot_index())
                except StopIteration:
                    break # nothing to display (coming out of USER mode: no parameters are mapped to encoders in USER mode, so no display parameters either (yet))

                if e.vpot_index() in row_00_encoders:
                    if e.vpot_index() == encoder_06_index:
                        self.unsolo_all_functionality("on_update_display_timer", e.vpot_index())

                    upper_string1 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                    lower_string1 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                elif e.vpot_index() in row_01_encoders:
                    if e.vpot_index() == encoder_09_index:
                        upper_string2 += adjust_string(dspl_sgmt.alter_upper_text(self.song().can_undo), 6) + ' '
                        # NEW: lower row = last undo label (from redo), scroll if available
                        if time.time() - self._last_undo_label_time < 15.0 and self._last_undo_label:
                            lower_string2 += self.get_scrolling_display_text(self._last_undo_label, e.vpot_index()) + ' '
                        else:
                            lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                        if self.song().can_undo:
                            e.show_full_enlighted_poti()
                        else:
                            e.unlight_vpot_leds()

                    elif e.vpot_index() == encoder_10_index:
                        upper_string2 += adjust_string(dspl_sgmt.alter_upper_text(self.song().can_redo), 6) + ' '
                        # NEW: lower row = last redo label (from undo), scroll if available
                        if time.time() - self._last_redo_label_time < 15.0 and self._last_redo_label:
                            lower_string2 += self.get_scrolling_display_text(self._last_redo_label, e.vpot_index()) + ' '
                        else:
                            lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                        if self.song().can_redo:
                            e.show_full_enlighted_poti()
                        else:
                            e.unlight_vpot_leds()

                    elif e.vpot_index() == encoder_11_index:
                        upper_string2 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                        if song_util.any_armed_track(self):
                            e.show_full_enlighted_poti()
                        else:
                            e.unlight_vpot_leds()

                    elif e.vpot_index() == encoder_12_index:
                        # show beat position pointer or SPP at encoder 12 AND encoder 13 position in second row
                        upper, lower = self.beat_pointer("on_update_display_timer", e.vpot_index())
                        upper_string2 += upper
                        lower_string2 += lower

                    # show loop length
                    elif e.vpot_index() == encoder_14_index:
                        upper, lower = self.loop_length("on_update_display_timer", e.vpot_index())
                        upper_string2 += self.get_scrolling_display_text(upper, e.vpot_index()) + ' '
                        lower_string2 += lower

                    # show loop start
                    elif e.vpot_index() == encoder_15_index:
                        get_loop_start = str(self.song().loop_start / 4)
                        upper_string2 += self.get_scrolling_display_text('LoopStart', e.vpot_index()) + ' '
                        lower_string2 += adjust_string(get_loop_start, 6) + ' '

                        # vpot ring light
                        display_mode_cc_first = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_WRAP][0]
                        display_mode_cc_last = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_WRAP][1]

                        scaler = make_interpolater(0, self.song().last_event_time, display_mode_cc_first, display_mode_cc_last)
                        loop_start = int(self.song().loop_start)
                        led_ring_val = int(scaler(loop_start))
                        spp_vpot_index = 14
                        spp_vpot = self.__encoders[spp_vpot_index]
                        spp_vpot.update_led_ring(led_ring_val)

                    elif e.vpot_index() == encoder_16_index:
                        # show if we are in Session or Arrange view in upper row and selected track name in lower row
                        upper_string2 += ('Scroll' if self.application().view.is_view_visible('Session') else 'Zoom  ')
                        if liveobj_valid(selected_track):
                            lower_string2 += self.get_scrolling_display_text(selected_track.name, e.vpot_index())
                        else:
                            lower_string2 += '      '

                    else:
                        upper_string2 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                elif e.vpot_index() in row_02_encoders:
                    if e.vpot_index() == encoder_22_index:
                        upper_string3 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                        lower_string3 += adjust_string(('%3.2f' % self.song().tempo), 6) + ' '

                    else:
                        upper_string3 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                        lower_string3 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                elif e.vpot_index() in row_03_encoders:
                    upper_string4 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                    lower_string4 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                    if e.vpot_index() == encoder_25_index:  # Song STOP
                        if self.song().is_playing:
                            e.unlight_vpot_leds()
                        else:
                            e.show_full_enlighted_poti()
                    elif e.vpot_index() == encoder_26_index:  # Song PLAY
                        if self.song().is_playing:
                            e.show_full_enlighted_poti()
                        else:
                            e.unlight_vpot_leds()

            unmute_all_encoder = self.__encoders[encoder_07_index]
            if song_util.any_muted_track(self):
                unmute_all_encoder.show_full_enlighted_poti()  # some track is muted (unmute has something to do)
            else:
                unmute_all_encoder.unlight_vpot_leds()  # no tracks are muted

            back_to_arranger_encoder = self.__encoders[encoder_08_index]
            if self.song().back_to_arranger:
                back_to_arranger_encoder.show_full_enlighted_poti()
            else:
                back_to_arranger_encoder.unlight_vpot_leds()

            metronome_encoder = self.__encoders[encoder_17_index]
            if self.song().metronome:
                metronome_encoder.show_full_enlighted_poti()
            else:
                metronome_encoder.unlight_vpot_leds()

            re_enable_automation_encoder = self.__encoders[encoder_18_index]
            if self.song().re_enable_automation_enabled:
                re_enable_automation_encoder.show_full_enlighted_poti()
            else:
                re_enable_automation_encoder.unlight_vpot_leds()

        # ONLY update displays when Not in USER mode
        if self.__assignment_mode != C4M_USER:
            self.send_display_string(LCD_ANGLED_ADDRESS, self.pad_right_if_less(upper_string1), LCD_TOP_ROW_OFFSET, force=force)
            self.send_display_string(LCD_TOP_FLAT_ADDRESS, self.pad_right_if_less(upper_string2), LCD_TOP_ROW_OFFSET, force=force)
            self.send_display_string(LCD_MDL_FLAT_ADDRESS, self.pad_right_if_less(upper_string3), LCD_TOP_ROW_OFFSET, force=force)
            self.send_display_string(LCD_BTM_FLAT_ADDRESS, self.pad_right_if_less(upper_string4), LCD_TOP_ROW_OFFSET, force=force)
            # sometimes the firmware version info doesn't get cleared from the end of this LCD "display line". If this lower_string1 is ever too short to
            # cover that firmware version info, log the padding was added here
            self.send_display_string(LCD_ANGLED_ADDRESS, self.pad_right_if_less(lower_string1, log_success=True), LCD_BOTTOM_ROW_OFFSET, force=force)
            self.send_display_string(LCD_TOP_FLAT_ADDRESS, self.pad_right_if_less(lower_string2), LCD_BOTTOM_ROW_OFFSET, force=force)
            self.send_display_string(LCD_MDL_FLAT_ADDRESS, self.pad_right_if_less(lower_string3), LCD_BOTTOM_ROW_OFFSET, force=force)
            self.send_display_string(LCD_BTM_FLAT_ADDRESS, self.pad_right_if_less(lower_string4), LCD_BOTTOM_ROW_OFFSET, force=force)

        return

    def pad_right_if_less(self, text, pad_char=" ", max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG, log_success=False):
        """operates like string.ljust(pad_char, max_length), but logs details"""
        if len(text) > max_length:
            temp = text[:max_length]
            # input display line string length seems to "always" be 56 instead of 55  (56 is the "bottom line offset", 56th byte of "top line" text is actually
            # the first byte of the "bottom line".  The C4 would accept 110 bytes (or more) in one message and write both top and bottom lines, but
            # this script always writes full single lines, 55 bytes
            # self.main_script().log_message(f"EC.pad_right_if_less: input text was too long {len(text)}, truncated to {len(temp)}: {temp}")
            text = temp
        elif len(text) < max_length:
            pad_len = max_length - len(text)
            temp = text
            old_len = len(text)
            text = text + "".join([pad_char for i in range(pad_len)])
            if not len(text) == max_length:
                self.main_script().log_message(f"EC.pad_right_if_less: oopsie? padded length {len(text)} not equal to max length {max_length}")
                self.main_script().log_message(f"EC.pad_right_if_less: before ({temp}) from length ({text})")
            elif log_success:
                self.main_script().log_message(f"EC.pad_right_if_less: successfully padded text to max length {max_length} from length {old_len}")
                self.main_script().log_message(f"EC.pad_right_if_less: before ({temp}) from length ({text})")

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
        is_update = self.__last_send_messages[display_address][display_row_offset] != ascii_text_sysex_ints

        if force or is_update:
            self.__last_send_messages[display_address][display_row_offset] = ascii_text_sysex_ints
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
        self.main_script().set_shift_is_pressed(False)
        self.main_script().set_option_is_pressed(False)
        self.main_script().set_ctrl_is_pressed(False)
        self.main_script().set_alt_is_pressed(False)
        self.main_script().set_marker_is_pressed(False)
        for s in self.__encoders:
            s.refresh_state()
