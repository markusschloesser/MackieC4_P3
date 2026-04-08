
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division

import sys
from itertools import zip_longest
from typing import Dict

from ableton.v2.base import liveobj_valid, depends, liveobj_changed

if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

from . MackieC4Component import *

import math
import logging

class ActiveTrack:

    def __init__(self, track_obj, track_type=0, song_track_index=0, callback_type_index=0, device_count=0, selected_device_index=None):

        self.track = track_obj
        self.type = track_type
        self.index = song_track_index
        self.index_by_type = callback_type_index
        self._device_count = device_count
        self._device_bank_count = int(math.ceil(device_count // SETUP_DB_DEVICE_BANK_SIZE))
        self._selected_device_index = selected_device_index
        """ index of this track's selected device in the track's device list, or None """
        self._selected_devices_bank_index = None if selected_device_index is None else selected_device_index % SETUP_DB_DEVICE_BANK_SIZE
        """ 0 - 7 index within a device bank where the selected device index would fall, automatically calculated 
            when selected device changes. (9th device falls in the second bank at bank index 0) """
        self._track_view_device_bank_index = self._selected_devices_bank_index
        """device bank index currently "on display" on the C4 (and selected in Live) of this track's device-bank list (0 - 9 if the track device list has 80 devices) """
        if selected_device_index is None or self.required_device_banks < 1:
            self._device_bank_index_of_selected_device = None
            """device bank index of this track's selected device in the track's device-bank list (0 unless the track has more than 8 devices), automatically calculated """ \
            """when selected device changes. This value can differ from the device bank index currently "on display". You can 'browse' device banks without changing """ \
            """selected devices. """
        else:
            self._device_bank_index_of_selected_device = int(math.floor(selected_device_index % self.required_device_banks))

    def new_copy(self, new_song_index, new_type_index):
        return ActiveTrack(self.track, self.type, new_song_index, new_type_index, self.device_count, self.selected_device_index)

    def __str__(self):
        if self is None:
            return "None"
        else:
            return self.to_string()

    def to_string(self):
        d_index = "None"
        if self._selected_device_index is not None:
            d_index = self.selected_device_index
        return f"track {self.track_name} type {self.type} s_index {self.index} t_index {self.index_by_type} devices {self._device_count} d_index {d_index}"

    @property
    def live_obj(self):
        return self.track

    @property
    def common_name(self):
        return self.track_name

    @property
    def track_name(self):
        nm = "None"
        if not liveobj_valid(self.track):
            nm = "Invalidobj"
        elif self.track.name is not None:
            nm = self.track.name
        return nm

    @property
    def device_count(self):
        return self._device_count
    @property
    def required_device_banks(self):
        return self._device_bank_count
    
    @device_count.setter
    def device_count(self, new_count):
        self._device_count = new_count
        self._device_bank_count = math.ceil(self._device_count // SETUP_DB_DEVICE_BANK_SIZE)

    @property
    def selected_device_index(self):
        """ the raw device index value in device list or None if no devices """
        return self._selected_device_index
    @property
    def selected_devices_bank_index(self):
        """ the raw device index value % SETUP_DB_DEVICE_BANK_SIZE (0 - 7 by default) or None if no devices """
        return self._selected_devices_bank_index
    @property
    def device_bank_index_of_selected_device(self):
        """ the raw device index value % self.device_bank_count (0 unless a track has more than 8 devices, 10+ if a track has more than 80 devices) or None if no devices """
        return self._device_bank_index_of_selected_device

    @selected_device_index.setter
    def selected_device_index(self, selected_device_index):
        self._selected_device_index = selected_device_index
        self._selected_devices_bank_index = None if selected_device_index is None else selected_device_index % SETUP_DB_DEVICE_BANK_SIZE
        if selected_device_index is None or self.required_device_banks < 1:
            self._device_bank_index_of_selected_device = None
        else:
            self._device_bank_index_of_selected_device = selected_device_index % self.required_device_banks
    
    @property
    def track_device_bank_view_index(self):
        return self._track_view_device_bank_index
    @track_device_bank_view_index.setter
    def track_device_bank_view_index(self, next_bank_index):
        self._track_view_device_bank_index = next_bank_index

class ActiveDevice:

    def __init__(self, dev_obj, dev_index=0, parameter_count=0, selected_parameter_index=0, song_track_index=0, callback_type_index=0):
        self.device = dev_obj
        self.index = dev_index
        """ device's index-key in its device map """
        self.track_index = song_track_index
        """ song track index of track holding device's device map """
        self.track_index_by_type = callback_type_index
        """callback type index of track holding device's map"""
        # self.type = 0  <---- we never need to 'back find' the track this device "belongs to" based only on info stored with this class
        self._parameter_count = parameter_count
        self._selected_parameter_index = selected_parameter_index
        """ index of this device's selected parameter in the device's parameter list """
        self._parameter_bank_count = math.ceil(parameter_count // SETUP_DB_PARAM_BANK_SIZE)
        """ the number of parameter banks worth of parameters in the device's parameter list (1 unless the device has more than 24 parameters) """
        if self._parameter_bank_count * SETUP_DB_PARAM_BANK_SIZE < parameter_count:
            self._parameter_bank_count += 1
        self._selected_parameters_bank_index = selected_parameter_index % SETUP_DB_PARAM_BANK_SIZE
        """ the index of the parameter bank where the selected parameter would fall (0 - 23 unless SETUP_DB_PARAM_BANK_SIZE changes) """
        if self._selected_parameters_bank_index == 0 and self.required_parameter_banks > 1:
            # device has a multiple of 24 parameters 48, 72, 96, etc
            self._selected_parameters_bank_index = selected_parameter_index // SETUP_DB_PARAM_BANK_SIZE

        self._bank_index_of_device_param_view = self._selected_parameters_bank_index
        """ device bank index currently "on display" on the C4 (and selected in Live) of this device's parameter-bank list (indexes 0 - 9 if the device """ \
        """parameter list has 240 parameters) """

        self._bank_index_of_selected_parameter = 0
        """parameter bank index of this device's selected parameter in the device's parameter-bank list (0 unless the device has more than 24 parameters), """ \
        """automatically calculated when selected parameter changes. This value can differ from the parameter bank index currently "on display". You can """ \
        """'browse' parameter banks without changing selected parameters. """
        
        if self.required_parameter_banks > 1:
            self._bank_index_of_selected_parameter = int(math.floor(selected_parameter_index % self.required_parameter_banks))

    def new_copy(self, new_device_index):
        return ActiveDevice(self.device, new_device_index, self.parameter_count, self.selected_parameter_index, self.track_index, self.track_index_by_type)

    def __str__(self):
        if self is None:  #  :)
            return "None"
        else:
            return self.to_string()

    def to_string(self):
        return f"device {self.device_name} d_index {self.index} t_index {self.track_index} tt_index {self.track_index_by_type} p_index {self._selected_parameter_index}"

    @property
    def live_obj(self):
        return self.device

    @property
    def common_name(self):
        return self.device_name

    @property
    def device_name(self):
        nm = "None"
        if not liveobj_valid(self.device):
            nm = "Invalidobj"
        elif self.device.name is not None:
            nm = self.device.name
        return nm

    @property
    def parameter_count(self):
        """ the raw count of parameters in parameter list """
        return self._parameter_count
    @property
    def required_parameter_banks(self):
        """ the calculated number of banks of (24) parameters required to support all parameters in parameter list """
        return self._parameter_bank_count

    @property
    def selected_parameter_index(self):
        """ the raw parameter index value in parameter list """
        return self._selected_parameter_index
    @property
    def selected_parameters_bank_index(self):
        """ the raw parameter index value % SETUP_DB_PARAM_BANK_SIZE (0 - 23 unless SETUP_DB_PARAM_BANK_SIZE changes) """
        return self._selected_parameters_bank_index
    @property
    def parameter_bank_index_of_selected_parameter(self):
        """ the raw parameter index value % self.parameter_bank_count (0 unless a device has more than 24 parameters, 5+ if a device has more than 120 parameters) """
        return self._bank_index_of_selected_parameter

    @selected_parameter_index.setter
    def selected_parameter_index(self, selected_parameter_index):
        self._selected_parameter_index = selected_parameter_index
        self._selected_parameters_bank_index = 0 if selected_parameter_index is None else selected_parameter_index % SETUP_DB_PARAM_BANK_SIZE
        if selected_parameter_index is None or self.required_parameter_banks < 1:
            self._bank_index_of_selected_parameter = 0
        else:
            self._bank_index_of_selected_parameter = selected_parameter_index % self.required_parameter_banks
    
    @property
    def device_parameter_bank_view_index(self):
        return self._bank_index_of_device_param_view
    @device_parameter_bank_view_index.setter
    def device_parameter_bank_view_index(self, next_bank_index):
        self._bank_index_of_device_param_view = next_bank_index

class ActiveDeviceParameter:
    """This class is strictly for storing the enabled status of track 'sends' which are (a list of) 'device parameters' of the track's 'mixer device' """ \
    """Return track 'sends' are disabled by default but can be enabled (by right-clicking the send and choosing enable)"""
    def __init__(self, param_obj, param_index=0, song_track_index=0, callback_track_type=0, callback_type_index=0):
        self.param = param_obj
        self.index = param_index
        self.track_index = song_track_index
        self.track_callback_type = callback_track_type
        self.track_index_by_type = callback_type_index

    @property
    def is_enabled(self):
        rtn = True
        if self.track_callback_type == 1:
            rtn = liveobj_valid(self.param) and self.param.is_enabled
        return rtn

    @property
    def live_obj(self):
        return self.param

    @property
    def common_name(self):
        return self.param_name

    @property
    def param_name(self):
        nm = "None"
        if not liveobj_valid(self.param):
            nm = "Invalidobj"
        elif self.param.name is not None:
            nm = self.param.name
        return nm

class ActiveTrackDetails:

    def __init__(self, active_track_ref: ActiveTrack, devices=None, sends=None):

        self.active_track = active_track_ref
        self.devices = dict[int, ActiveDevice]({})
        self.sends = dict[int, ActiveDeviceParameter]({})
        if devices is not None:
            self.build_device_map(devices)
        if sends is not None:
            self.build_sends_map(sends)

    def new_copy(self, new_song_index, new_type_index):
        track_ref = self.active_track.new_copy(new_song_index, new_type_index)
        copy = ActiveTrackDetails(track_ref)
        copy.devices = self.devices
        copy.sends = self.sends
        return copy

    def build_device_map(self, new_devices=None):
        if new_devices is not None and len(new_devices) > 0:
            self.devices.clear()
            new_map = {}
            for i, d in enumerate(new_devices):
                d_ref = ActiveDevice(d, i, len(d.parameters), song_track_index=self.song_track_index, callback_type_index=self.track_index_by_type)
                new_map[i] = d_ref
            self.set_track_device_map(new_map, 0)

    def build_sends_map(self, new_sends):
        if new_sends is not None and len(new_sends) > 0:
            self.sends.clear()
            new_map = {}
            for i, p in enumerate(new_sends):
                dp_ref = ActiveDeviceParameter(p, i, song_track_index=self.song_track_index,
                                              callback_track_type=self.callback_type_key, callback_type_index=self.track_index_by_type)
                new_map[i] = dp_ref
            self.set_track_sends_map(new_map)

    @property
    def song_track_index(self):
        """ when type 0 (visible) and type 1 (return) tracks are combined into one collection, index of this Track in that collection """
        return self.active_track.index
    @property
    def callback_type_key(self):
        """ type 0 (visible); type 1 (return); or type 2 (master) callback type of this Track """
        return self.active_track.type
    @property
    def track_index_by_type(self):
        """index of this Track within its callback type collection, except the master track index is not really in a collection (since there is only ever one """ \
        """master track), the master track index always equals the number of visible + return tracks in the song (and moves automatically when tracks are added """ \
        """or removed from the song """
        return self.active_track.index_by_type
    @property
    def device_count(self):
        """ The number of devices in the device map associated with the active track reference"""
        count = len(self.devices.keys())
        if self.active_track.device_count != count:
            self.active_track.device_count = count
        return self.active_track.device_count
    @property
    def selected_device_index(self):
        """ The stored index-key of the selected device in the device map (of track == active_track and of size == device_count)"""
        return self.active_track.selected_device_index

    @property
    def selected_device(self) -> ActiveDevice|None:
        """the ActiveDevice reference obj stored at self.selected_device_index or None"""
        if self.selected_device_index is not None and self.selected_device_index < self.device_count:
            return self.devices[self.selected_device_index]
        else:
            return None

    @property
    def is_device_list_empty(self):
        return self.devices is None or len(self.devices.keys()) < 1

    def has_matching_device_map(self, other_devices: dict[int, ActiveDevice]):
        return self.has_matching_deviceobj_list([other_devices.values()])

    def has_matching_deviceobj_list(self, other_devices: list):
        rtn = True
        for this, that in zip_longest(self.devices.values(), other_devices):
            if liveobj_valid(this.live_obj) and not liveobj_valid(that):
                rtn = False
                break
            elif not liveobj_valid(this.live_obj) and liveobj_valid(that):
                rtn = False
                break
            elif not (liveobj_valid(this.live_obj) or liveobj_valid(that)):  # !x and !y == !(x or y)
                # both items are "not valid", this is a match that should only happen if both dict value lists contain
                # a "deleted device" reference at the same index at the time of comparison?
                pass
            elif liveobj_changed(this.live_obj, that):
                rtn = False
                break
        return rtn
    
    def set_track_device_map(self, device_map: dict[int, ActiveDevice], selected_index: int|None=None):
        """Setting an empty map won't change the track's selected device index to None, use clear_device_list()"""
        set_count = len(device_map.keys())
        if self.active_track.device_count != set_count:
            self.active_track.device_count = len(device_map.keys())
        # else:
        #     pass
        if selected_index is not None and self.active_track.selected_device_index != selected_index:
            self.active_track.selected_device_index = selected_index
        # else:
        #     pass
        self.devices = device_map

    def set_track_sends_map(self, sends_map: dict[int,ActiveDeviceParameter]):
        self.sends = sends_map

    def is_send_enabled(self, send_index):
        """sends are disabled for example if they are controlled by automation or a macro. This method returns True 'is_enabled' for return track sends """ \
        """that are greyed out in Live's GUI """
        return self.sends[send_index].is_enabled

    def to_string(self):
        return self.active_track.to_string()


track_callback_types = {0: "plain", 1: "return", 2: "master"}
""" keys [0, 1, 2] are the track callback types used by Live; values ["plain", "return", "master"] are the associated 'primary keys' used for local SongData storage """

class SongData(object):

    table_keys = {"plain": 0, "return": 1, "master": 2}
    """ keys ["plain", "return", "master"] are the 'primary keys' used in SongData; values [0, 1, 2] are the track callback types used by Live """

    @depends(logger=None, get_device_list=None)
    def __init__(self, logger=None, get_device_list=None):
        self.logger = logger
        self.extend_device_list = get_device_list
        # enable "class logging" to see debug logging mostly from __shift_keys_right() and __shift_keys_left() methods
        # uncomment logging messages in other class methods to see more verbose debug logging from earlier in the class method call stack
        self.class_logging = False # True #
        self.device_list_table = dict[str, dict[int, ActiveTrackDetails]]({
            track_callback_types[0]: {},
            track_callback_types[1]: {},
            track_callback_types[2]: {}})
        
        self.__master_track_count = 1
        self.__initializing_database = True
        # the default swap alg is O^2 but more accurate, the fallback alg is not much better ln(O^2) (I think)
        # and has boundary issues like when moving a track or device to the zero index position (fix the boundary issues, or find a better swap alg eventually?)
        # 500^2 is 25k operations, 100^2 is "only" 10k operations, 50^2 is 2500.
        self.__rekey_map_algorithm_swap_limit = 50  # use fallback alg if 50+ devices on track or 50+ plain or return tracks in song

    def log_msg(self, level, msg):
        if self.class_logging:
            self.logger(level, msg)

    def log_dump(self):
        self.log_dump_by_callback_track_type_key(track_callback_types[0])
        self.log_dump_by_callback_track_type_key(track_callback_types[1])
        self.log_dump_by_callback_track_type_key(track_callback_types[2])
    def log_dump_with_devices(self):
        self.log_dump_with_devices_by_callback_track_type_key(track_callback_types[0])
        self.log_dump_with_devices_by_callback_track_type_key(track_callback_types[1])
        self.log_dump_with_devices_by_callback_track_type_key(track_callback_types[2])

    def log_dump_with_devices_by_callback_track_type_key(self, type_key):
        log_id = "EAH.SD.dump_w_devs: "
        msg = f"{log_id}{type_key} cb_type index "
        dump_dict = self.get_all_tracks_by_type_key(type_key)
        vals = [x.active_track.track_name if isinstance(x, ActiveTrackDetails) else str(x) for x in dump_dict.values()]
        for key_index in dump_dict.keys():
            atdl_ref = dump_dict[key_index]
            device_map = atdl_ref.devices
            d_vals = [x.device_name if isinstance(x, ActiveDevice) else str(x) for x in device_map.values()]
            d_dump = f"{key_index}: {atdl_ref.active_track.track_name} "
            self.log_msg(logging.DEBUG, msg + d_dump)
            self.log_msg(logging.DEBUG, f"d_list {device_map.keys()}: {d_vals}")

    def log_dump_by_callback_track_type_key(self, type_key):
        log_id = "EAH.SD.dump: "
        msg = f"{log_id}"
        dump_dict = self.get_all_tracks_by_type_key(type_key)
        vals = [x.active_track.track_name if isinstance(x, ActiveTrackDetails) else str(x) for x in dump_dict.values()]
        self.log_msg(logging.DEBUG, f"{type_key} cb_type dict keys {dump_dict.keys()} and values {vals}")

    def get_callback_type_for_song_index(self, track_index):
        rtn = 3
        if track_index < self.plain_track_count:
            rtn = 0 # visible
        elif track_index < self.plain_track_count + self.return_track_count:
            rtn = 1 # return
        elif track_index == self.plain_track_count + self.return_track_count:
            rtn = 2 # master
        return rtn
    def get_callback_type_key_for_song_index(self, track_index):
        return track_callback_types[self.get_callback_type_for_song_index(track_index)]

    def get_callback_index_for_song_index(self, track_index):
        rtn = track_index
        if self.get_callback_type_for_song_index(track_index) == 1: # callback-track-type == return
            rtn = track_index - self.plain_track_count
        return rtn

    def get_song_index_for_callback_index(self, callback_type, callback_type_index):
        """converts -1 callback_type_index input values to 0, for example, returns song_index of "plain track count" (return track index 0) instead "plain track count """ \
        """- 1 (return track index -1).  Don't use the raw return value from this method to remove the item at the zero map type-index-key, at that level you need to use """ \
        """the -1 value to remove the 0 index item.  This method won't return an OOB index value like -1. (which is ambiguous when referring to the 'index before' the """ \
        """first return track in the 'song array' because that's the index of the last plain (regular visible) track (not -1)"""
        song_index = self.master_track_index
        if callback_type_index >= 0:
            if callback_type == 0:
                song_index = callback_type_index
            if callback_type == 1:
                song_index = self.plain_track_count + callback_type_index
        else:
            song_index = 0
            if callback_type == 1:
                song_index = self.plain_track_count

        return song_index

    @property
    def initializing_database(self):
        return self.__initializing_database

    @initializing_database.setter
    def initializing_database(self, state):
        self.__initializing_database = state

    @property
    def plain_track_count(self):
        return int(len(self.device_list_table[track_callback_types[0]].keys()))

    @property
    def return_track_count(self):
        return int(len(self.device_list_table[track_callback_types[1]].keys()))

    @property
    def total_track_count(self):
        return self.plain_track_count + self. return_track_count + self.__master_track_count

    @property
    def master_track_index(self):
        tracks_before = self.plain_track_count + self. return_track_count
        # minimum example: 1 plain + 0 return == 1 track before master, master index is never less than 1 (second track, during init)
        rtn = tracks_before if tracks_before > 0 else 1
        return rtn

    def get_active_track_details_at_song_index(self, song_track_index) -> ActiveTrackDetails | None:
        rtns_index = song_track_index - self.plain_track_count
        if song_track_index < self.plain_track_count:
            return self.get_active_track_details_ref_by_type_key(track_callback_types[0], song_track_index)
        elif rtns_index < self.return_track_count:
            return self.get_active_track_details_ref_by_type_key(track_callback_types[1], rtns_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            return self.get_active_track_details_ref_by_type_key(track_callback_types[2], song_track_index)
        return None

    def get_active_track_details_ref_by_type_key(self, track_callback_type_key, track_index_by_type) -> ActiveTrackDetails | None:
        if track_callback_type_key == "return" and len(self.device_list_table[track_callback_type_key].keys()) < 1:
            return None # song may not have any return tracks
        return self.device_list_table[track_callback_type_key][track_index_by_type]

    def get_master_track(self, master_track_index=None)-> ActiveTrack:
        if master_track_index is None:
            master_track_index = self.master_track_index
        return self.get_track_by_type_key(track_callback_types[2], master_track_index)

    def init_master_track(self, track, song_index):
        self.clear_tracks_by_type_key(track_callback_types[2])
        nbr_devices = len(track.devices)
        ext_devices = self.extend_device_list(track.devices)
        selected_device_index = 0 if nbr_devices > 0 else None
        track_ref = ActiveTrack(track, self.table_keys[track_callback_types[2]], song_index, song_index, nbr_devices, selected_device_index)
        self.log_msg(logging.DEBUG, f"EAH.SD.init_master_track: BEFORE: master track ref {track_ref} at index {song_index}")
        track_device_list = ActiveTrackDetails(track_ref, ext_devices)
        self.device_list_table[track_callback_types[2]][song_index] = track_device_list
        track_device_list = self.device_list_table[track_callback_types[2]][song_index]
        self.log_msg(logging.DEBUG, f"EAH.SD.init_master_track: AFTER: master ref {track_device_list.active_track} at index {song_index}")
        # only use self._insert_track_slot() for non-master tracks (ordered lists with indexes from 0)

    def update_master_track_index(self, master_track_details_ref):
        if len(self.device_list_table[track_callback_types[2]]) > 0:
            self.clear_tracks_by_type_key(track_callback_types[2]) # remove master_device_list_ref with key == old master index
        master_ref = master_track_details_ref.active_track
        master_ref.index = self.master_track_index
        master_ref.index_by_type = self.master_track_index
        master_track_details_ref.active_track = master_ref
        # add master_ref back with new key == self.master_track_index
        self.device_list_table[track_callback_types[2]][self.master_track_index] = master_track_details_ref
        # only use self._insert_track_slot() for non-master tracks (ordered lists with indexes from 0)

    # NOTE: no functions to update any other "internal stored object indexes" to match their associated track or device "slot index" (map key)"
    #       See get_track() and get_device() below, the ActiveTrackDetails and ActiveDevice object internal property index values are updated automatically
    #       before ActiveTrackDetails or ActiveDevice objects return from get_track() and get_device() (so they can "set themselves" back, see set_device() for example)
    # The stored internal property index values fall out of sync with their actual associated "map key index" values every time tracks are added to or removed from the Song
    # I.E. This class.  (Except for Master Track index, ) The internal ref-obj indexes are not resynchronized / updated until "fetched" by get_track() or get_device()

    def clear_all_tracks(self):
        self.clear_tracks_by_type_key(track_callback_types[0])
        self.clear_tracks_by_type_key(track_callback_types[1])
        self.clear_tracks_by_type_key(track_callback_types[2])

    def clear_tracks_by_type_key(self, track_callback_type_key):
        """clears devices too"""
        self.device_list_table[track_callback_type_key].clear()

    # clear_tracks_by_type_key() clears devices too as a side effect

    def clear_track_devices(self, song_track_index):
        rtns_index = song_track_index - self.plain_track_count
        if song_track_index < self.plain_track_count:
            self.clear_track_devices_by_type_key(track_callback_types[0], song_track_index)
        elif rtns_index < self.return_track_count:
            self.clear_track_devices_by_type_key(track_callback_types[1], rtns_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            self.clear_track_devices_by_type_key(track_callback_types[2], song_track_index)

    def clear_track_devices_by_type_key(self, track_callback_type_key, track_index_by_type):
        self.__clear_track_devices(track_callback_type_key, track_index_by_type)

    def __clear_track_devices(self, primary_key, track_type_index):
        try:
            self.device_list_table[primary_key][track_type_index].devices.clear()
        except KeyError:
            pass # no devices to clear
        if self.device_list_table[primary_key][track_type_index].active_track.device_count > 0:
            self.device_list_table[primary_key][track_type_index].active_track.device_count = 0
        if self.device_list_table[primary_key][track_type_index].active_track.selected_device_index is not None:
            self.device_list_table[primary_key][track_type_index].active_track.selected_device_index = None

    def update_track_refs_device_properties(self, primary_key, track_type_index, device_count, selected_device_index):
        """The track's device map should have already been updated, device count or selected device already changed (or neither because the selected device moved)"""
        active_track_details_ref = self.get_active_track_details_ref_by_type_key(primary_key, track_type_index)
        track_ref = active_track_details_ref.active_track
        stored_device_refs = active_track_details_ref.devices
        track_ref.device_count = device_count if len(stored_device_refs.keys()) == device_count else len(stored_device_refs.keys())
        if 0 == track_ref.device_count:
            track_ref.selected_device_index = None
        elif selected_device_index is not None:
            track_ref.selected_device_index = selected_device_index if selected_device_index < track_ref.device_count else track_ref.device_count - 1
        else:
            track_ref.selected_device_index = selected_device_index # selected_device_index == None
        # is setting back the updated track_ref strictly necessary?
        self.set_track_by_type_key(primary_key, track_type_index, track_ref)

    def get_track(self, song_track_index)-> ActiveTrack | None:
        callback_type_index = song_track_index
        rtns_index = song_track_index - self.plain_track_count
        rtn = None
        if song_track_index < self.plain_track_count:
            rtn = self.get_track_by_type_key(track_callback_types[0], song_track_index)
            rtn.index = song_track_index
            rtn.index_by_type = song_track_index
        elif rtns_index < self.return_track_count:
            callback_type_index = rtns_index
            rtn = self.get_track_by_type_key(track_callback_types[1], rtns_index)
            rtn.index = song_track_index
            rtn.index_by_type = rtns_index
        elif song_track_index == self.plain_track_count + self.return_track_count:
            rtn = self.get_track_by_type_key(track_callback_types[2], song_track_index)
            rtn.index = song_track_index
            rtn.index_by_type = song_track_index

        # self.log_msg(logging.DEBUG, f"EAH.SD.get_track: {rtn}")
        # self.log_msg(logging.DEBUG, f"EAH.SD.get_track: returning track_ref from index {callback_type_index}")
        return rtn

    def get_all_tracks_by_type_key(self, track_callback_type_key) -> Dict[int, ActiveTrackDetails]:
        return self.device_list_table[track_callback_type_key]

    def get_track_by_type_key(self, track_callback_type_key, track_index_by_type) -> ActiveTrack:
        rtn = self.get_all_tracks_by_type_key(track_callback_type_key)[track_index_by_type].active_track
        song_index = track_index_by_type if track_callback_types[0] == track_callback_type_key else self.plain_track_count + track_index_by_type
        song_index = self.plain_track_count + self.return_track_count if track_callback_types[2] == track_callback_type_key else song_index
        rtn.index = song_index
        rtn.index_by_type = track_index_by_type
        rtn.type = self.table_keys[track_callback_type_key]
        return rtn

    def set_track_by_type_key(self, track_callback_type_key, track_index_by_type, active_track: ActiveTrack):
        self.device_list_table[track_callback_type_key][track_index_by_type].active_track = active_track

    def set_track(self, active_track: ActiveTrack):
        rtns_index = active_track.index - self.plain_track_count
        if active_track.index < self.plain_track_count:
            self.set_track_by_type_key(track_callback_types[0], active_track.index_by_type, active_track)
        elif rtns_index < self.return_track_count:
            self.set_track_by_type_key(track_callback_types[1], active_track.index_by_type, active_track)
        elif active_track.index == self.plain_track_count + self.return_track_count:
            self.set_track_by_type_key(track_callback_types[2], active_track.index_by_type, active_track)
        else:
            raise RuntimeError("can't set a track not already in the track table")

        # msg = f"EAH.SD.set_track: done track_ref {active_track} at song track index {active_track.index} and callback type track index {active_track.index_by_type}"
        # self.log_msg(logging.DEBUG, msg)
        # self.log_msg(logging.DEBUG, f"EAH.SD.set_track: plain tracks {self.plain_track_count} return tracks {self.return_track_count}")

    def init_tracks(self, p_tracks, r_tracks, m_track):
        rtn = None
        if len(self.device_list_table[track_callback_types[0]]) > 0 or len(self.device_list_table[track_callback_types[1]]) > 0:
            # already initialized...  clear dicts, raise error, just log and return? (SongData can't reference self.main_script().log_message)
            rtn = "EAH.SD.init_tracks: assumption issue: track tables not already clear?"

        rtn_val = None
        if rtn is None:
            # self.log_msg(logging.DEBUG, f"EAH.SD.init_tracks: initializing master track {m_track.name} at index {self.master_track_index}")
            self.init_master_track(m_track, self.master_track_index)
            new_master_track_ref = self.get_master_track()

            if new_master_track_ref is None:
                raise KeyError(f"EAH.SD.init_tracks: unable to retrieve initialized master track at index {self.master_track_index}")
            # else:
            #     self.log_msg(logging.DEBUG, f"EAH.SD.init_tracks: master track after init: {new_master_track_ref}")

            rtn = self.init_tracks_by_callback_type(track_callback_types[0], p_tracks)
            rtn_rtn = self.init_tracks_by_callback_type(track_callback_types[1], r_tracks)
            if rtn is not None:
                rtn_val = rtn
            if rtn_val is not None and rtn_rtn is not None:
                rtn_val += rtn_rtn

            master_index = len(p_tracks) + len(r_tracks)
            assert self.master_track_index == master_index

        return rtn_val

    def init_tracks_by_callback_type(self, track_callback_type_key, tracks) -> str|None:
        rtn = None
        log_id = f"EAH.SD.init_tracks_by_callback_type: "
        self.log_msg(logging.DEBUG, f"{log_id}getting master track at index {self.master_track_index}")
        master_device_list_ref = self.get_active_track_details_ref_by_type_key(track_callback_types[2], self.master_track_index)
        last_master_track_ref = master_device_list_ref.active_track
        # last_master_track_ref = self.get_master_track(self.master_track_index)
        # self.log_msg(logging.DEBUG, f"{log_id}master track before {track_callback_type_key} tracks initialized: {last_master_track_ref}")
        if len(self.device_list_table[track_callback_type_key]) > 0:
            rtn = f"{log_id}assumption issue: device list table {track_callback_type_key} not already clear?"

        if rtn is None:
            track_type_index = 0
            track_count = len(tracks)
            song_index_offset = 0
            if self.table_keys[track_callback_type_key] > 0:
                song_index_offset = self.plain_track_count
            for track in tracks:
                self.add_track_by_callback_type(track_callback_type_key, song_index_offset, track_type_index, track)
                track_type_index += 1
            assert track_count == len(self.device_list_table[track_callback_type_key].keys())
            if last_master_track_ref is not None:
                if last_master_track_ref.index < self.master_track_index:
                    self.log_msg(logging.DEBUG, f"{log_id}updating master track index to {self.master_track_index}")
                    self.update_master_track_index(master_device_list_ref)
            #     else:
            #         self.log_msg(logging.DEBUG, f"{log_id}master track index is already {self.master_track_index}?")
            # else:
            #     self.log_msg(logging.DEBUG, f"{log_id}master track ref was None, no update at index {self.master_track_index}?")
            #
            # self.log_msg(logging.DEBUG, f"{log_id}master track after {track_callback_type_key} tracks initialized: {last_master_track_ref}")

        return rtn

    def add_track(self, track, track_type, song_track_index, selected_device_index=0):
        """automatically adds existing devices on input Live track objects"""

        rtns_index = song_track_index - self.plain_track_count
        song_index = 0
        if track_type > 0:
            song_index = self.plain_track_count

        if song_track_index < self.plain_track_count:
            self.add_track_by_callback_type(track_callback_types[0], song_index, song_track_index, track, selected_device_index)
        elif rtns_index < self.return_track_count:
            self.add_track_by_callback_type(track_callback_types[1], song_index, rtns_index, track, selected_device_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            raise RuntimeError(f"can't add or remove master track at index {song_track_index}")
        else:
            raise RuntimeError(f"can't add track at OOB index {song_track_index}, max new index is less than {self.master_track_index}")

    def add_track_by_callback_type(self, track_callback_type_key, song_index_type_offset, track_index_by_type, track, selected_device_index=0):
        """automatically adds existing devices on input Live track objects"""
        log_id = "EAH.SD.add_track_by_callback_type: "
        master_device_list_ref = self.get_active_track_details_ref_by_type_key(track_callback_types[2], self.master_track_index)
        last_master_track_ref = master_device_list_ref.active_track
        ext_devices = None if len(track.devices) < 1 else self.extend_device_list(track.devices)
        nbr_devices = 0 if ext_devices is None else len(ext_devices)
        selected_device_index = selected_device_index if nbr_devices > 0 else None
        cumulative_song_index = song_index_type_offset + track_index_by_type
        track_ref = ActiveTrack(track, self.table_keys[track_callback_type_key], cumulative_song_index, track_index_by_type, nbr_devices, selected_device_index)
        track_details_ref = ActiveTrackDetails(track_ref, devices=ext_devices, sends=track.mixer_device.sends)
        self.add_atd_ref_by_callback_type(track_callback_type_key, track_index_by_type, track_details_ref)
        if last_master_track_ref.index < self.master_track_index:
            self.log_msg(logging.DEBUG, f"{log_id}after adding track, updating master track index to updated track count {self.master_track_index}")
            self.update_master_track_index(master_device_list_ref)


    def add_atd_ref_by_callback_type(self, track_callback_type_key, track_index_by_type, track_details_ref):
        tracks_of_type = self.get_all_tracks_by_type_key(track_callback_type_key)
        self._insert_track_details_slot(tracks_of_type, track_index_by_type, track_details_ref)

    def remove_track(self, song_track_index):
        """input song_track_index values should be >= 0 and 'left of' the index to remove"""
        rtns_index = song_track_index - self.plain_track_count
        log_msg = f"EAH.SD.remove_track: at song track index {song_track_index}"
        self.log_msg(logging.DEBUG, log_msg)
        if song_track_index < self.plain_track_count:
            self.remove_track_by_callback_type(track_callback_types[0], song_track_index)
        elif rtns_index < self.return_track_count:
            self.remove_track_by_callback_type(track_callback_types[1], rtns_index)
        else:
            raise RuntimeError(f"can't remove track at OOB index {song_track_index}, can't remove master_track {self.master_track_index} or after")

    def remove_track_by_callback_type(self, track_callback_type_key, track_index_by_type, is_track_move=False):
        """type index values input should be >= 0, the track slot to the right of this index will be removed.  If a track at index 0 is deleted, the stored liveobj """ \
        """reference will not be liveobj valid and the zero value input will be adjusted automatically.  If a Track moves (is dragged left) to index 0, use the """ \
        """is_track_move=True flag"""
        log_id = "EAH.SD.remove_track_by_callback_type: "
        master_device_list_ref = self.get_active_track_details_ref_by_type_key(track_callback_types[2], self.master_track_index)
        last_master_track_ref = master_device_list_ref.active_track
        old = self.device_list_table[track_callback_type_key][track_index_by_type]
        if old.active_track.track_name == "Invalidobj":
            log_msg = f"{log_id}collapsing slot holding invalid liveobj "
        else:
            log_msg = f"{log_id}collapsing slot holding a valid liveobj {old.active_track.track_name} "

        self.log_msg(logging.DEBUG, log_msg)
        log_msg = f"{log_id}{track_callback_type_key} track at {track_callback_type_key} callback type index {track_index_by_type}: {old.active_track.track_name} "
        self.log_msg(logging.DEBUG, log_msg)
        self.log_msg(logging.DEBUG, f"{log_id}BEFORE: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        tracks_of_type = self.get_all_tracks_by_type_key(track_callback_type_key)
        if (not liveobj_valid(old.active_track.track) or is_track_move) and track_index_by_type == 0:
            track_index_by_type = -1

        self._collapse_track_details_slot(tracks_of_type, track_index_by_type)
        new_count = len(self.device_list_table[track_callback_type_key])
        self.log_msg(logging.DEBUG, f"{log_id}AFTER: new track count={new_count}")
        self.log_msg(logging.DEBUG, f"{log_id}AFTER: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        if last_master_track_ref is not None and last_master_track_ref.index_by_type != self.master_track_index:
            self.update_master_track_index(master_device_list_ref)

    def get_track_device_map(self, song_track_index) -> Dict[int, ActiveDevice]:
        device_map = None
        rtns_index = song_track_index - self.plain_track_count
        # log_msg = f"EAH.SD.get_track_device_map: at song track index "
        try:
            type_key = self.get_callback_type_key_for_song_index(song_track_index)
            if song_track_index < self.plain_track_count:
                # self.log_msg(logging.DEBUG, log_msg + song_track_index)
                device_map = self.get_track_device_map_by_callback_type(type_key, song_track_index)
            elif rtns_index < self.return_track_count:
                # self.log_msg(logging.DEBUG, log_msg + rtns_index)
                device_map =  self.get_track_device_map_by_callback_type(type_key, rtns_index)
            elif song_track_index == self.plain_track_count + self.return_track_count:
                # self.log_msg(logging.DEBUG, log_msg + song_track_index)
                device_map = self.get_track_device_map_by_callback_type(type_key, song_track_index)
        except KeyError:
            # track should always have a device map that might be empty
            raise RuntimeError(f"can't get device map for track at song index {song_track_index}")

        return device_map

    def get_track_device_map_by_callback_type(self, track_callback_type_key, track_index_by_type) -> Dict[int, ActiveDevice]:
        # log_id = "EAH.SD.get_track_device_map_by_callback_type: "
        # self.log_msg(logging.DEBUG, f"{log_id}returning device map from {track_callback_type_key} track index {track_index_by_type}")
        return self.device_list_table[track_callback_type_key][track_index_by_type].devices


    def set_track_device_map_by_callback_type(self, track_callback_type_key, track_index_by_type, device_map: Dict[int, ActiveDevice]):
        # log_id = "EAH.SD.set_track_device_map_by_callback_type: "
        # self.log_msg(logging.DEBUG, f"{log_id}setting device map for {track_callback_type_key} track index {track_index_by_type}")
        active_device_list_ref = self.get_active_track_details_ref_by_type_key(track_callback_type_key, track_index_by_type)
        active_device_list_ref.set_track_device_map(device_map)
        # self.device_list_table[track_callback_type_key][track_index_by_type].devices = device_map

    def get_device(self, song_track_index, device_index)-> ActiveDevice | None:
        active_device = None
        device_map = self.get_track_device_map(song_track_index)
        if device_map is not None and device_index is not None and device_index < len(device_map.keys()):
            active_device = device_map[device_index]
            active_device.index = device_index
            active_device.track_index = song_track_index
            if self.plain_track_count <= song_track_index < self.return_track_count:
                active_device.track_index_by_type = song_track_index - self.plain_track_count
            else:
                active_device.track_index_by_type = song_track_index # plain or master track index by type

        # self.log_msg(logging.DEBUG, f"EAH.SD.get_device: returning device_ref from song index {song_track_index} and d_index {device_index}")
        # self.log_msg(logging.DEBUG, f"EAH.SD.get_device: {active_device}")
        return active_device

    def set_device(self, active_device: ActiveDevice):
        device_map = self.get_track_device_map(active_device.track_index)
        # self.log_msg(logging.DEBUG, f"EAH.SD.set_device: got device list from device's song track index {active_device.track_index}")
        if device_map and active_device.index < len(device_map.keys()):
            old = device_map[active_device.index]
            # self.log_msg(logging.DEBUG, f"EAH.SD.set_device: setting device <{active_device}> in device list at device index {active_device.index}")
            # self.log_msg(logging.DEBUG, f"EAH.SD.set_device: overwriting device <{old}> previously stored at index {active_device.index}")
            device_map[active_device.index] = active_device
        else:
            raise RuntimeError("can't set a device not already in the device map")

    def add_device(self, song_track_index, track_callback_type_index, device_index, device_obj):
        selected_parameter_index = 0 if len(device_obj.parameters) > 0 else None  # devices always have at least 1 parameter
        device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, song_track_index, track_callback_type_index)
        rtns_index = song_track_index - self.plain_track_count
        # log_msg = f"EAH.SD.add_device: adding device ref {device_ref} at "
        if song_track_index < self.plain_track_count:
            # self.log_msg(logging.DEBUG, log_msg + f"song index {song_track_index} and callback type index {song_track_index}")
            self.add_device_by_track_callback_type(track_callback_types[0], song_track_index, device_index, device_ref)
        elif rtns_index < self.return_track_count:
            # self.log_msg(logging.DEBUG, log_msg + f"song index {song_track_index} and callback type index {rtns_index}")
            self.add_device_by_track_callback_type(track_callback_types[1], rtns_index, device_index, device_ref)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            # self.log_msg(logging.DEBUG, log_msg + f"song index {song_track_index} and callback type index {song_track_index}")
            self.add_device_by_track_callback_type(track_callback_types[2], song_track_index, device_index, device_ref)
        else:
            raise RuntimeError(f"can't add device at OOB track index {song_track_index}, max track index is master_track {self.master_track_index}")

    def add_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index, device_ref: ActiveDevice):
        log_msg = f"EAH.SD.add_device_by_track_callback_type: adding device to {track_callback_type_key} track at callback index {callback_type_index} and "
        self.log_msg(logging.DEBUG, log_msg + f"device list index {device_index}")
        device_map = self.get_active_track_details_ref_by_type_key(track_callback_type_key, callback_type_index).devices
        if device_index < len(device_map.keys()) and device_map[device_index] == device_ref:
            log_msg = f"EAH.SD.add_device_by_track_callback_type: device to add already present in device map at index {device_map}, device not added again"
            self.log_msg(logging.DEBUG, log_msg)
        else:
            self._insert_track_device_slot(device_map, device_index, device_ref)
            old_count = self.get_track_by_type_key(track_callback_type_key, callback_type_index).device_count
            # if a track has enough devices and the selected device moves left or right in the "device chain", the ActiveDevice device reference is removed from the old
            # index and added back at the new index, so even though the before and after device counts don't change in this case, this "device count update" is legit
            log_msg = f"EAH.SD.add_device_by_track_callback_type: updating device count and setting selected device index values on associated {track_callback_type_key} "
            self.log_msg(logging.DEBUG, log_msg + f"track at callback type index {callback_type_index} to {old_count + 1} devices and selected index {device_index}")
        track_ref = self.get_track_by_type_key(track_callback_type_key, callback_type_index)
        self._update_track_table_after_device_add(track_ref, device_index)
        self.set_track_by_type_key(track_callback_type_key, callback_type_index, track_ref)

    def clear_device_list(self, track_index):
        """ defers to: self.clear_track_devices(track_index) """
        self.clear_track_devices(track_index)

        rtns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            new_device_count = self.device_list_table[track_callback_types[0]][track_index].active_track.device_count
        elif rtns_index < self.return_track_count:
            new_device_count = self.device_list_table[track_callback_types[1]][rtns_index].active_track.device_count
        elif track_index == self.plain_track_count + self.return_track_count:
            new_device_count = self.device_list_table[track_callback_types[2]][track_index].active_track.device_count
        else:
            raise RuntimeError(f"can't clear device list at OOB track index {track_index}, max track index is master_track {self.master_track_index}")
        device_map_len = len(self.get_track_device_map(track_index))
        assert new_device_count == 0 == device_map_len

    def find_track_obj_type_and_index(self, track_obj):
        """returns the "callback type of" and "type index of" the stored type 0 or 1 ActiveTrackDeviceList reference obj associated with """ \
        """the input valid Live track object (visible or return). returns -1, -1 if no == match is found."""
        # NOTE: a None "object" will == a not liveobj_valid "object" and that index would be returned (possibly spuriously)
        rtn = -1, -1
        if liveobj_valid(track_obj):
            found = False
            all_plain_track_list_refs = self.get_all_tracks_by_type_key(track_callback_types[0])
            for i in all_plain_track_list_refs.keys():
                track_ref = all_plain_track_list_refs[i]
                if track_ref.active_track.track == track_obj:
                    rtn = 0, i
                    found = True
                    break
            if not found:
                all_return_track_list_refs = self.get_all_tracks_by_type_key(track_callback_types[1])
                for i in all_return_track_list_refs.keys():
                    track_ref = all_return_track_list_refs[i]
                    if track_ref.active_track.track == track_obj:
                        rtn = 1, i
                        found = True
                        break
            if not found:
                master_track_ref = self.get_master_track(self.master_track_index)
                if master_track_ref.track == track_obj:
                    rtn = 2, self.master_track_index
        return rtn


    def rekey_track_list_of_callback_type(self, track_callback_type, next_selected_callback_type_index, all_tracks_of_type, selected_track_obj):
        """moves the stored ActiveDeviceList track reference representing the selected track obj input from its last stored index to its next stored index"""
        # uses two algorithms first traverses "all tracks of type" input once and "old tracks of type" once for every track in "all tracks of type" until it finds the
        # matching track.  The inner loop gets smaller after each match, but it's still an expensive big-O algorithm.  The second algorithm does a swap, removing the
        # "track that moved" from its old stored index location, and re-inserting an updated copy at its new stored index location (matching Live).
        # This second algorithm is at its least efficient when a song has many tracks and tracks with low index numbers move
        # (meaning lots of tracks to the right of the moving track also move (twice)), its performance decline is less exponential than the first algorithm,
        # closer to constant time but still not great
        log_id = "EAH.SD.rekey_track_list_of_callback_type: "
        type_key = track_callback_types[track_callback_type]
        old_track_list_of_type = self.get_all_tracks_by_type_key(type_key)
        self.log_msg(logging.DEBUG, f"{log_id}BEFORE: stored {type_key} track count {len(old_track_list_of_type)} vs input count {len(all_tracks_of_type)}")
        new_keyed_map = {}
        if len(all_tracks_of_type) < self.__rekey_map_algorithm_swap_limit:
            if len(all_tracks_of_type) == len(old_track_list_of_type.keys()):
                shallow_copy = old_track_list_of_type.copy()
                missed = {}
                for new_index, track_obj in enumerate(all_tracks_of_type):
                    assigned = False
                    for track_ref_index in shallow_copy.keys():
                        track_list_ref = old_track_list_of_type[track_ref_index]
                        if track_list_ref.active_track.track == track_obj:
                            track_list_ref.active_track.index_by_type = new_index
                            track_list_ref.active_track.index = new_index
                            if track_list_ref.active_track.type == 1:
                                track_list_ref.active_track.index += self.plain_track_count
                            if track_obj == selected_track_obj and not next_selected_callback_type_index == new_index:
                                e_msg = f"input track obj {selected_track_obj.name} found at different index {new_index} from input index {next_selected_callback_type_index}"
                                raise RuntimeError(e_msg)
                            assigned = True
                            self.log_msg(logging.DEBUG, f"{log_id}{track_list_ref.active_track.track_name} assigned to new stored index {new_index}")
                            new_keyed_map[new_index] = track_list_ref
                            del shallow_copy[track_ref_index]  # so the inner search loop gets smaller after each match
                            break
                    if not assigned:
                        missed[new_index] = track_obj


                self.log_msg(logging.DEBUG, f"{log_id}AFTER: updated {type_key} track count {len(new_keyed_map.keys())} vs input count {len(all_tracks_of_type)}")
                if len(all_tracks_of_type) != len(new_keyed_map.keys()):
                    msg = f"{log_id}no match found for input keys {shallow_copy.keys()} and values {[x.active_track.track_name for x in shallow_copy.values()]}"
                    self.log_msg(logging.DEBUG, msg)
                    msg = f"{log_id}missed keys {missed.keys()} and values {[x.name for x in missed.values()]}"
                    self.log_msg(logging.DEBUG, msg)
                assert len(all_tracks_of_type) == len(new_keyed_map.keys())
                old_track_list_of_type.update(new_keyed_map)
        else: # too many tracks for worst case above? delete ref from old stored index location, then add back at new index location
            old_cb_type_of_selected_track, old_cb_index_of_selected_track = self.find_track_obj_type_and_index(selected_track_obj)
            if old_cb_type_of_selected_track >= 0:
                cb_key = track_callback_types[old_cb_type_of_selected_track]
                if cb_key == type_key:
                    old_atd_ref_at_old_index = self.get_active_track_details_ref_by_type_key(type_key, old_cb_index_of_selected_track)
                    old_atd_ref_at_new_index = self.get_active_track_details_ref_by_type_key(type_key, next_selected_callback_type_index)
                    msg = f"{log_id}stored track ref at old index {old_cb_index_of_selected_track} is {old_atd_ref_at_old_index.active_track.track_name}"
                    self.log_msg(logging.DEBUG, msg)
                    msg = f"{log_id}stored track ref at new index {next_selected_callback_type_index} is {old_atd_ref_at_new_index.active_track.track_name}"
                    self.log_msg(logging.DEBUG, msg)
                    if old_atd_ref_at_new_index.active_track.track == selected_track_obj:
                        self.log_msg(logging.DEBUG, f"{log_id}stored track ref at next index {next_selected_callback_type_index} already matches {selected_track_obj.name} ")
                        pass # no sorting required, no "track move" detected
                    else:
                        master_device_list_ref = self.get_active_track_details_ref_by_type_key(track_callback_types[2], self.master_track_index)
                        last_master_track_ref = master_device_list_ref.active_track
                        new_song_index = self.get_song_index_for_callback_index(type_key, next_selected_callback_type_index)
                        copy_of_old_ref_at_old_loc = old_atd_ref_at_old_index.new_copy(new_song_index, next_selected_callback_type_index)
                        msg = f"{log_id}removing {copy_of_old_ref_at_old_loc.active_track.track_name} from type index {old_atd_ref_at_old_index.track_index_by_type}"
                        self.log_msg(logging.DEBUG, msg)
                        old_idx = old_atd_ref_at_old_index.track_index_by_type  # removes "right of" input index, zero index requires special handling
                        self.remove_track_by_callback_type(type_key, 0 if old_idx < 1 else old_idx - 1, is_track_move=True)
                        # don't rebuild track's extended device list from scratch
                        # self.add_track_by_callback_type(type_key, song_index, next_selected_callback_type_index, selected_track_obj)
                        msg = f"{log_id}adding {copy_of_old_ref_at_old_loc.active_track.track_name} at type index {copy_of_old_ref_at_old_loc.track_index_by_type}"
                        self.log_msg(logging.DEBUG, msg)
                        self.add_atd_ref_by_callback_type(type_key, next_selected_callback_type_index, copy_of_old_ref_at_old_loc)
                        if last_master_track_ref.index < self.master_track_index:
                            self.log_msg(logging.DEBUG, f"{log_id}after removing and re-adding track, updating master track ref index to {self.master_track_index}")
                            self.update_master_track_index(master_device_list_ref)
                        else:
                            self.log_msg(logging.DEBUG, f"{log_id}oddly, after removing and re-adding track, master track ref index is already {self.master_track_index}")
                    msg = f"{log_id}AFTER: updated {type_key} track count {len(old_track_list_of_type.keys())} vs input count {len(all_tracks_of_type)}"
                    self.log_msg(logging.DEBUG, msg)
                    assert len(all_tracks_of_type) == len(old_track_list_of_type.keys())
                else:
                    self.log_msg(logging.WARNING, f"{log_id}oddly, callback type table keys didn't match?")
            else: # old_cb_type_of_selected_track < 0 and old_cb_index_of_selected_track < 0
                msg = f"{log_id}pass, self.find_track_obj_type_and_index() was unable to locate stored reference to selected_track_obj {selected_track_obj.name} "
                self.log_msg(logging.WARNING, msg)
                type_key = track_callback_types[track_callback_type]
                pass

    def find_stored_device_obj_index(self, track_callback_type_key, callback_type_index, selected_device_obj):
        stored_devices = self.get_track_device_map_by_callback_type(track_callback_type_key, callback_type_index)
        rtn = -1, None
        for i in stored_devices.keys():
            device_ref = stored_devices[i]
            if device_ref.device == selected_device_obj:
                rtn = i, device_ref
                break
        return rtn

    def rekey_device_list_by_track_callback_type(self, track_callback_type_key, callback_type_index, all_track_devices, selected_device_obj, selected_device_obj_index=None):

        old_keyed_map = self.get_track_device_map_by_callback_type(track_callback_type_key, callback_type_index)
        new_keyed_map = {}
        track_ref = self.get_track_by_type_key(track_callback_type_key, callback_type_index)
        self.log_msg(logging.DEBUG, f"EAH.SD.rekey_device_list_by_track_callback_type: track {track_ref.track_name} has {track_ref.device_count} active devices")
        if len(all_track_devices) == len(old_keyed_map.keys()) == track_ref.device_count:
            if track_ref.device_count < self.__rekey_map_algorithm_swap_limit:
                shallow_copy = old_keyed_map.copy()
                for new_index, device_obj in enumerate(all_track_devices):
                    for device_ref_index in shallow_copy.keys():
                        device_ref = old_keyed_map[device_ref_index]
                        if device_ref.device == device_obj:
                            new_keyed_map[new_index] = device_ref
                            self.log_msg(logging.INFO, f"EAH.SD.rekey_device_list_by_track_callback_type: moving {device_ref.device_name} to new stored index {new_index}")
                            if device_obj == selected_device_obj:
                                track_ref.selected_device_index = new_index
                            del shallow_copy[device_ref_index]  # <-- inner search loop gets smaller after every match
                            break
                if not len(old_keyed_map.keys()) == len(new_keyed_map.keys()):
                    log_msg = f"EAH.SD.rekey_device_list_by_track_callback_type: updated key counts don't match: live {len(all_track_devices)} "
                    self.log_msg(logging.WARNING, log_msg + f"old stored {len(old_keyed_map.keys())} new stored {new_keyed_map} old count {track_ref.device_count}")
                else:
                    assert len(old_keyed_map.keys()) == len(new_keyed_map.keys())
                old_keyed_map.update(new_keyed_map)
                self.set_track_device_map_by_callback_type(track_callback_type_key, callback_type_index, old_keyed_map)
            else:
                # old_device_index, old_active_device = self.find_stored_device_obj_index(track_callback_type_key, callback_type_index, selected_device_obj)
                stored_track_device_map = self.get_track_device_map_by_callback_type(track_callback_type_key, callback_type_index)
                new_device_index = -1
                old_device_index = -1
                old_active_device = None
                found_items = 0
                for new_index, device_obj in enumerate(all_track_devices):
                    device_ref = stored_track_device_map[new_index]
                    if device_ref.device == selected_device_obj:
                        old_device_index = new_index
                        old_active_device = device_ref
                        found_items += 1
                    if device_obj == selected_device_obj:
                        new_device_index = new_index
                        found_items += 1
                    if found_items > 1:
                        break

                copy_of_device_at_new_index = old_active_device.new_copy(new_device_index)
                old_device_index = 0 if old_device_index < 1 else old_device_index - 1
                self.remove_device_by_track_callback_type(track_callback_type_key, callback_type_index, old_device_index)
                self.add_device_by_track_callback_type(track_callback_type_key, callback_type_index, new_device_index, copy_of_device_at_new_index)
                track_ref.selected_device_index = new_device_index

        else:  # not len(all_track_devices) == len(old_keyed_map.keys()) == track_ref.device_count
            log_msg = f"EAH.SD.rekey_device_list_by_track_callback_type: counts don't match, stored device list order not changed: "
            self.log_msg(logging.DEBUG, log_msg + f"new {len(all_track_devices)} old {len(old_keyed_map.keys())} old count {track_ref.device_count}")

    def remove_devices(self, song_track_index, nbr_devices_to_remove, track_device_list_first_remove_index=0):

        orig_nbr_keys = len(self.get_track_device_map(song_track_index).keys())
        if orig_nbr_keys == nbr_devices_to_remove and track_device_list_first_remove_index == 0:
            self.clear_track_devices(song_track_index)
        elif (track_device_list_first_remove_index < orig_nbr_keys and
                track_device_list_first_remove_index + nbr_devices_to_remove <= orig_nbr_keys):  # 5 active devices remove 2 starting from index 3
            nbr = track_device_list_first_remove_index + nbr_devices_to_remove
            end_of_remove_range = nbr if track_device_list_first_remove_index == 0 else nbr + 1
            remove_range_nbr = end_of_remove_range - track_device_list_first_remove_index
            log_msg = f"EAH.SD.remove_devices: removing {remove_range_nbr} devices between indexes {track_device_list_first_remove_index} and {end_of_remove_range} (one past) "
            self.log_msg(logging.DEBUG, log_msg)
            for i in range(track_device_list_first_remove_index, end_of_remove_range):
                index_left_of_remove_index = i if i == 0 else i - 1
                self.remove_device(song_track_index, index_left_of_remove_index)
        else:
            log_msg = f"EAH.SD.remove_devices: song track index {song_track_index} has {orig_nbr_keys} active devices, can't remove "
            if not track_device_list_first_remove_index < orig_nbr_keys:
                log_msg += f"any devices starting from OOB index {track_device_list_first_remove_index}"
            elif not track_device_list_first_remove_index + nbr_devices_to_remove <= orig_nbr_keys:
                log_msg += f"{nbr_devices_to_remove} devices starting from index {track_device_list_first_remove_index}, not enough devices after index"
            self.log_msg(logging.DEBUG, log_msg)

        device_count = self.get_track(song_track_index).device_count
        nbr_remaining_devices = len(self.get_track_device_map(song_track_index))
        assert nbr_remaining_devices == track_device_list_first_remove_index == device_count


    def remove_device(self, song_track_index, device_index_before_remove_index):
        rtns_index = song_track_index - self.plain_track_count
        # log_msg = f"EAH.SD.remove_device: at song track index {song_track_index} "
        # self.log_msg(logging.DEBUG, log_msg)
        if song_track_index < self.plain_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[0], song_track_index, device_index_before_remove_index)
        elif rtns_index < self.return_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[1], rtns_index, device_index_before_remove_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[2], song_track_index, device_index_before_remove_index)
        else:
            raise RuntimeError(f"can't remove device at OOB track index {song_track_index}, max track index is master_track {self.master_track_index}")

    def remove_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index_before_remove_index):
        # log_id = "EAH.SD.remove_device_by_track_callback_type: "
        # log_msg = f"{log_id}collapsing device at index {device_index} at {track_callback_type_key} "
        active_device_list_ref = self.get_active_track_details_ref_by_type_key(track_callback_type_key, callback_type_index)
        device_map = active_device_list_ref.devices
        # self.log_msg(logging.DEBUG, log_msg + f"track callback index {callback_type_index}")
        # self.log_msg(logging.DEBUG, f"{log_id}BEFORE: device count {len(device_map)}")
        self._collapse_track_device_slot(device_map, device_index_before_remove_index)
        # self.log_msg(logging.DEBUG, f"{log_id}AFTER: device count {len(device_map)}")
        active_device_list_ref.devices = device_map
        track_ref = active_device_list_ref.active_track
        # self.log_msg(logging.DEBUG, f"{log_id}after device removal BEFORE updating track ref {track_ref}")
        self._update_track_table_after_device_removal(track_ref, 0 if device_index_before_remove_index == -1 else device_index_before_remove_index)
        # self.log_msg(logging.DEBUG, f"{log_id}after device removal AFTER updating track ref {track_ref}")

    @staticmethod
    def _update_track_table_after_device_removal(track_ref, updated_device_index):
        old_device_count = track_ref.device_count
        new_device_count = old_device_count - 1 if old_device_count > 0 else 0
        track_ref.device_count = new_device_count
        if 0 >= updated_device_index < new_device_count:
            track_ref.selected_device_index = updated_device_index
        elif updated_device_index >= new_device_count:
            track_ref.selected_device_index = new_device_count - 1
        else:
            track_ref.selected_device_index = None
        return track_ref

    @staticmethod
    def _update_track_table_after_device_add(track_ref, updated_device_index):
        old_device_count = track_ref.device_count
        new_device_count = old_device_count + 1
        track_ref.device_count = new_device_count
        if 0 >= updated_device_index < new_device_count:
            track_ref.selected_device_index = updated_device_index
        elif updated_device_index >= new_device_count:
            track_ref.selected_device_index = new_device_count - 1
        else:
            track_ref.selected_device_index = None
        return track_ref

    def _insert_track_details_slot(self, type_dict: Dict[int, ActiveTrackDetails], insert_at_track_callback_type_index, track_device_list_ref: ActiveTrackDetails)-> dict[int, ActiveTrackDetails]:
        log_id = "EAH.SD._insert_track_details_slot: "
        if insert_at_track_callback_type_index in type_dict.keys():
            type_dict = self.__shift_keys_right(type_dict, insert_at_track_callback_type_index, track_device_list_ref)
        else:
            assert insert_at_track_callback_type_index == len(type_dict.keys())
            self.log_msg(logging.DEBUG, f"{log_id}inserting last or only track of type at type index {insert_at_track_callback_type_index}, no shift")
            type_dict[insert_at_track_callback_type_index] = track_device_list_ref
        return type_dict

    def _insert_track_device_slot(self, type_dict: Dict[int, ActiveDevice], insert_at_device_index, active_device: ActiveDevice)-> dict[int, ActiveDevice]:
        log_id = "EAH.SD._insert_track_device_slot: "
        if insert_at_device_index in type_dict.keys():
            type_dict = self.__shift_keys_right(type_dict, insert_at_device_index, active_device)
        else:
            try:
                assert insert_at_device_index == len(type_dict.keys())
                self.log_msg(logging.DEBUG, f"{log_id}inserting last or only device at device index {insert_at_device_index}, insert without shift")
                type_dict[insert_at_device_index] = active_device
            except AssertionError:
                self.log_msg(logging.DEBUG, f"{log_id}NOT inserting at non-consecutive device index {insert_at_device_index}, max insert index is {len(type_dict.keys())}")
                # raise RuntimeError()

        return type_dict

    def _collapse_track_details_slot(self, type_dict, track_callback_type_index_left_of_collapse_index)-> dict[int, ActiveTrackDetails]:
        """track_callback_type_index_left_of_collapse_index means input value should be one less than the collapsing index"""
        log_id = "EAH.SD._collapse_track_details_slot: "
        if track_callback_type_index_left_of_collapse_index in type_dict.keys():
            return self.__shift_keys_left(type_dict, track_callback_type_index_left_of_collapse_index)
        else:
            try:
                assert track_callback_type_index_left_of_collapse_index == -1
                self.log_msg(logging.DEBUG, f"{log_id}collapsing first track of type at type index 0, collapse and shift here")
                del type_dict[0]
                self.log_msg(logging.DEBUG, f"{log_id}type dict keys after del {type_dict.keys()} and values {[x.active_track.track_name for x in type_dict.values()]}")
                remaining_slots = {i - 1:type_dict[i] for i in type_dict.keys()}
                type_dict.clear()
                self.log_msg(logging.DEBUG, f"{log_id}remaining dict after shift {remaining_slots.keys()} and values {[x.active_track.track_name for x in remaining_slots.values()]}")
                type_dict.update(remaining_slots)
                self.log_msg(logging.DEBUG, f"{log_id}returning keys {type_dict.keys()} and values {[x.active_track.track_name for x in type_dict.values()]}")
                return type_dict
            except AssertionError:
                self.log_msg(logging.DEBUG, f"{log_id}NOT collapsing at negative track index {track_callback_type_index_left_of_collapse_index}, min collapse index is -1")

    def _collapse_track_device_slot(self, type_dict, device_index_left_of_collapse_index)-> dict[int, ActiveDevice]:
        log_id = "EAH.SD._collapse_track_device_slot: "
        if device_index_left_of_collapse_index in type_dict.keys():
            return self.__shift_keys_left(type_dict, device_index_left_of_collapse_index)
        else:
            try:
                assert device_index_left_of_collapse_index == -1
                self.log_msg(logging.DEBUG, f"{log_id}collapsing first device at device index 0, collapse and shift here")
                del type_dict[0]
                remaining_slots = {i - 1:type_dict[i] for i in type_dict.keys()}
                type_dict.clear()
                type_dict.update(remaining_slots)
                return type_dict
            except AssertionError:
                self.log_msg(logging.DEBUG, f"{log_id}NOT collapsing at negative device index {device_index_left_of_collapse_index}, min collapse index is -1")


    def __shift_keys_right(self, local_dict: dict[int, ActiveDevice]|dict[int,ActiveTrackDetails], key_of_add, value_to_add: ActiveDevice | ActiveTrackDetails) -> dict[int, ActiveDevice] | dict[int,ActiveTrackDetails]:
        log_id = "EAH.SD.__shift_keys_right: "
        # local_dict is either an active_track reference mapped by type index
        #     {callback_type_index=key_of_add: active_device_list=value_to_add}
        # or an active_device reference mapped by device index (active_device_list.devices)
        #     {device_index=key_of_add: active_device=value_to_add
        # "left slots" range is (0, key_of_add) if any
        # "right slots" range is (key_of_add, len(local_dict.keys()) if any (and index shifted right)
        # assumes local_dict is not empty
        vals = [x.active_track.common_name if isinstance(x, ActiveTrackDetails) else x.common_name for x in local_dict.values()]
        txt_to_add = value_to_add.active_track.common_name if isinstance(value_to_add, ActiveTrackDetails) else value_to_add.common_name
        self.log_msg(logging.DEBUG, f"{log_id}with input key={key_of_add}, value={txt_to_add}, input dict keys {local_dict.keys()} and values {vals}")
        right_slots = {j + 1: local_dict[j] for j in range(key_of_add, len(local_dict.keys()))}
        left_slots = {j: local_dict[j] for j in range(0, key_of_add)}

        left_slots[key_of_add] = value_to_add
        if len(right_slots.keys()) > 0:
            left_slots.update(right_slots)
        if len(left_slots.keys()) > 0:
            local_dict.update(left_slots)

        vals = [x.active_track.common_name if isinstance(x, ActiveTrackDetails) else x.common_name for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id}returning updated dict keys {local_dict.keys()} and values {vals}")
        return local_dict

    def __shift_keys_left(self, local_dict: Dict[int, ActiveDevice]|Dict[int,ActiveTrackDetails], key_before_del) -> Dict[int, ActiveDevice] | Dict[int,ActiveTrackDetails]:
        """special key_before_del input range expected: given a standard local_dict index-key range(0, m), the associated special input is 'shifted left', range(-1, m-1)"""
        log_id = "EAH.SD.__shift_keys_left: "
        key_to_remove = key_before_del + 1
        # local_dict is either an ActiveTrackDetails reference mapped by (track type and) type index
        #     {callback_type_index=key_of_add: active_device_list=value_to_add}
        # or an ActiveDevice reference mapped by device index (active_device_list.devices)
        #     {device_index=key_of_add: active_device=value_to_add}
        # "left slots" range is (0, key_to_remove) if any
        # "right slots" range is (key_to_remove + 1, len(local_dict.keys()) if any (and index shifted left)
        # delete 3 of 3 == range(2, 3), 2 "left slots", 0 "right slots"
        # delete 2 of 3 == range(1, 3), 1 "left slots", 1 "right_slots"
        # delete 1 of 3 == range(0, 3), 0 "left slots", 2 "right slots"
        # returned local_dict has 2 keys [0, 1], one less than before
        vals = [x.active_track.common_name if isinstance(x, ActiveTrackDetails) else x.common_name for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id}input dict keys {local_dict.keys()} and values {vals}")
        # self.log_msg(logging.DEBUG, f"{log_id} with input key {key_before_del} means remove key {key_to_remove}")
        if key_before_del == -1 and key_to_remove in local_dict.keys():
            if key_to_remove + 1 in local_dict.keys():
                right_slots = {j - 1: local_dict[j] for j in range(key_to_remove + 1, len(local_dict.keys()))}
                del local_dict[key_to_remove]
                local_dict.update(right_slots)
            else:
                del local_dict[key_to_remove]
        elif key_before_del in local_dict.keys():
            if key_to_remove in local_dict.keys():
                right_slots = None
                if key_to_remove + 1 in local_dict.keys():
                    right_slots = {j - 1: local_dict[j] for j in range(key_to_remove + 1, len(local_dict.keys()))}
                left_slots = {j: local_dict[j] for j in range(0, key_to_remove)}

                if isinstance(local_dict[key_to_remove], ActiveTrackDetails):
                    obj = local_dict[key_to_remove].active_track.live_obj
                else:
                    obj = local_dict[key_to_remove].live_obj

                # if not liveobj_valid(obj):
                #     self.log_msg(logging.DEBUG, f"{log_id} removed data ref stored object was invalid, Live object was deleted")
                # else:
                #     self.log_msg(logging.DEBUG, f"{log_id} removed data ref stored object was still valid, Live object disappeared from view")

                del local_dict[key_to_remove]
                local_dict.clear()
                if right_slots is not None and len(right_slots.keys()) > 0:
                    left_slots.update(right_slots)
                if len(left_slots.keys()) > 0:
                    local_dict.update(left_slots)
            else:
                self.log_msg(logging.DEBUG, f"{log_id} assumption issue? key to remove {key_to_remove} is not in the key set {local_dict.keys()}")
        else:
            self.log_msg(logging.DEBUG, f"{log_id} assumption issue? input key {key_before_del} is not in the key set {local_dict.keys()}")

        vals = [x.active_track.track_name if isinstance(x, ActiveTrackDetails) else x.common_name for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id} returning updated dict keys {local_dict.keys()} and values {vals}")
        return local_dict


class EncoderAssignmentHistory(MackieC4Component):
    """
     Keeps track of Song Track and Device content supporting SYSEX "LCD feedback message" generation and other script functions
    """
    __module__ = __name__

    def __init__(self, main_script, encoder_controller):
        MackieC4Component.__init__(self, main_script)

        self.log_levels = main_script.script_log_levels
        self.data = SongData(logger=self.main_script().log_message, get_device_list=self.get_device_list)
        self.data.class_logging = main_script.current_script_log_level < self.log_levels["TRACE"] # or True

        self.__my_controlling_encoder = encoder_controller
        self.__selected_track = self.main_script().song().view.selected_track
        self.__alt_selected_track = self.main_script().song().view.selected_track
        self.__selected_device = self.__selected_track.view.selected_device
        self.__alt_selected_device = self.__selected_track.view.selected_device
        self.__master_track_index = self.data.master_track_index  # not a valid index until build_setup_database() runs
        self.__last_selected_track_index = 0
        self.__next_selected_track_index = 0
        self.__next_selected_device_index = 0


    @property
    def next_selected_track(self):
        return self.__alt_selected_track

    @next_selected_track.setter
    def next_selected_track(self, track):
        self.__alt_selected_track = track

    @property
    def next_selected_device(self):
        return self.__alt_selected_device

    @next_selected_device.setter
    def next_selected_device(self, device):
        self.__alt_selected_device = device

    @property
    def last_selected_track(self):
        return self.__selected_track

    @last_selected_track.setter
    def last_selected_track(self, track):
        self.__selected_track = track

    @property
    def last_selected_device(self):
        return self.__selected_device

    @last_selected_device.setter
    def last_selected_device(self, device):
        self.__selected_device = device

    @property
    def master_track_index(self):
        return self.data.master_track_index

    @property
    def next_selected_track_index(self):
        """ temporary and volatile property, this value might become "permanent" as the last_selected_track_index """
        return self.__next_selected_track_index

    @next_selected_track_index.setter
    def next_selected_track_index(self, track_index):
        self.__next_selected_track_index = track_index

    @property
    def last_selected_track_index(self):
        return self.__last_selected_track_index

    @last_selected_track_index.setter
    def last_selected_track_index(self, track_index):
        self.__last_selected_track_index = track_index

    @property
    def last_selected_track_callback_type(self):
        return self.data.get_callback_type_for_song_index(self.last_selected_track_index)

    @property
    def last_selected_track_callback_type_index(self):
        return self.data.get_callback_index_for_song_index(self.last_selected_track_index)

    @property
    def is_plain_track_selected(self):
        """True if track at selected track index is listener callback type 0"""
        return self.last_selected_track_callback_type == 0

    @property
    def is_return_track_selected(self):
        """True if track at selected track index is listener callback type 1"""
        return self.last_selected_track_callback_type == 1

    @property
    def is_master_track_selected(self):
        """True if track at selected track index is listener callback type 2"""
        return self.last_selected_track_callback_type == 2

    @property
    def song_track_count(self):
        return self.data.total_track_count - 1 # self.data.total_track_count - 1 == self.data.master_track_index

    @property
    def master_track_count(self):
        return self.data.total_track_count

    @property
    def next_selected_device_index(self):
        """ temporary and volatile property, this value might become "permanent" as the last_selected_device_index """
        return self.__next_selected_device_index

    @next_selected_device_index.setter
    def next_selected_device_index(self, selected_device_index):
        self.__next_selected_device_index = selected_device_index

    @property
    def last_selected_device_index(self):
        last_track_ref = self.data.get_track(self.last_selected_track_index)
        idx = None if last_track_ref is None else 0 if not liveobj_valid(last_track_ref.track) else last_track_ref.selected_device_index
        return idx

    @last_selected_device_index.setter
    def last_selected_device_index(self, device_index):
        if isinstance(self.data.get_track(self.last_selected_track_index), ActiveTrack):
            self.data.get_track(self.last_selected_track_index).selected_device_index = device_index

    @property
    def selected_device_bank_count(self):
        if self.data.get_track(self.last_selected_track_index) is not None:
            return self.data.get_track(self.last_selected_track_index).required_device_banks
        else:
            return -1

    @property
    def selected_device_bank_index(self):
        if self.data.get_track(self.last_selected_track_index) is not None:
            return self.data.get_track(self.last_selected_track_index).device_bank_index_of_selected_device
        else:
            return -1

    @property
    def max_device_count(self):
        if self.data.get_track(self.last_selected_track_index) is not None:
            return self.data.get_track(self.last_selected_track_index).device_count
        else:
            return -1

    @property
    def max_last_selected_track_device_parameter_bank_nbr(self, t_d_idx=None):
        log_id = "EAH.max_last_selected_track_device_parameter_bank_nbr: "
        device_ref = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
        if device_ref is not None:
            msg = f"{log_id}device {device_ref.device_name} occupies {device_ref.required_parameter_banks} banks for {device_ref.parameter_count} parameters"
            self.main_script().log_message(self.log_levels["TRACE"], msg)
            return device_ref.required_parameter_banks
        else:
            return -1

    @property
    def last_selected_track_device_parameter_bank_nbr(self, t_d_idx=None):
        return self.last_selected_device_parameter_bank_view_index  # parameter_bank_index_of_selected_parameter
        
    @property
    def last_selected_track_device_bank_view_index(self):
        """ index of the selected track's current device-bank-view.  Which could differ from the device-bank of the track's selected device """
        rtn = 0
        if self.data.get_track(self.last_selected_track_index) is not None and self.data.get_track(self.last_selected_track_index).track_device_bank_view_index is not None:
            rtn = self.data.get_track(self.last_selected_track_index).track_device_bank_view_index
        return rtn
    @last_selected_track_device_bank_view_index.setter
    def last_selected_track_device_bank_view_index(self, next_bank_view_index):
        if self.data.get_track(self.last_selected_track_index) is not None:
            self.data.get_track(self.last_selected_track_index).track_device_bank_view_index = next_bank_view_index
        
    @property
    def last_selected_device_parameter_bank_view_index(self):
        """ index of the selected device's current parameter-bank-view.  Which could differ from the parameter-bank of the device's selected (last changed) parameter """
        rtn = 0
        if self.last_selected_device_index is not None:
            d = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
            if liveobj_valid(d) and d.device_parameter_bank_view_index is not None:
                rtn = d.device_parameter_bank_view_index
        return rtn
    @last_selected_device_parameter_bank_view_index.setter
    def last_selected_device_parameter_bank_view_index(self, next_bank_view_index):
        if self.last_selected_device_index is not None:
            self.data.get_device(self.last_selected_track_index, self.last_selected_device_index).device_parameter_bank_view_index = next_bank_view_index


    def on_param_state_change(self, callback_track_type, callback_track_type_index, device_index, parameter_index, param):
        track_of_type = self.song().master_track
        if callback_track_type == 0:
            track_of_type = self.song().visible_tracks[callback_track_type_index]
        elif callback_track_type == 1:
            track_of_type = self.song().return_tracks[callback_track_type_index]
        elif callback_track_type != 2:
            track_of_type = None  # not possible?

        if track_of_type is not None:
            device_obj = track_of_type.devices[device_index]
            if liveobj_valid(device_obj):
                device_map = self.data.get_track_device_map_by_callback_type(track_callback_types[callback_track_type], callback_track_type_index)
                if device_index < len(device_map.keys()):
                    device_ref = device_map[device_index]
                    if device_ref.device == device_obj:
                        device_ref.selected_parameter_index = parameter_index
                    else:
                        extended_index = None
                        for i in device_map.keys():
                            active_device = device_map[i]
                            if active_device.device == device_obj:
                                extended_index = i
                                break

                        if extended_index is not None:
                            device_ref = device_map[extended_index]
                            device_ref.selected_parameter_index = parameter_index
                        else: # unknown device on this track?
                            pass


    def update_device_counter(self, track_index, device_count):
        log_id = "EAH.update_device_counter: "
        max_device_banks = math.ceil(device_count // SETUP_DB_DEVICE_BANK_SIZE)
        self.data.get_track(track_index).device_bank_count = max_device_banks
        if self.last_selected_track_index != track_index:
            msg = f"{log_id}track index {track_index} for device count update didn't match last selected track index {self.last_selected_track_index}, updating"
            self.main_script().log_message(logging.DEBUG, msg)
            self.track_changed(track_index)

    def build_setup_database(self, song_ref=None):
        log_id = "EAH.build_setup_database: "
        if song_ref is None:
            song_ref = self.song()

        self.data.initializing_database = True
        self.data.clear_all_tracks()

        # tracks include devices
        error_msg = self.data.init_tracks(song_ref.visible_tracks, song_ref.return_tracks, song_ref.master_track)
        if error_msg is not None:
            self.main_script().log_message(logging.ERROR, error_msg)

        self.data.initializing_database = False

    def track_changed(self, track_index):
        """track changes update local 'last selected index' values for tracks, devices, and track-device-bank-views. Returns last selected device index """ \
        """value for track at input track index"""
        track_ref = self.data.get_track(track_index)
        self.last_selected_track_index = track_index
        self.last_selected_device_index = track_ref.selected_device_index
        self.last_selected_track_device_bank_view_index = 0
        if self.last_selected_device_index is not None:
            last_d_ref = self.data.get_device(track_index, self.last_selected_device_index)
            bvi = 0 if last_d_ref is None else last_d_ref.parameter_bank_index_of_selected_parameter
            self.last_selected_track_device_bank_view_index = bvi
        return self.last_selected_device_index

    def track_moved(self, callback_track_type, next_song_index, track_obj_that_moved):
        log_id = "EAH.track_moved: "
        all_track_objs_of_type = self.song().visible_tracks
        next_callback_type_index = next_song_index
        if callback_track_type == 1:
            all_track_objs_of_type = self.song().return_tracks
            next_callback_type_index = next_song_index - self.data.plain_track_count
        stored_track_refs_of_type = self.data.get_all_tracks_by_type_key(track_callback_types[callback_track_type])
        if len(stored_track_refs_of_type.keys()) == len(all_track_objs_of_type):
            if stored_track_refs_of_type[next_callback_type_index].active_track.track == track_obj_that_moved:
                self.main_script().log_message(logging.WARNING, f"{log_id}no move {track_obj_that_moved.name} ref already stored at cb type index {next_callback_type_index}")
                return
            self.main_script().log_message(logging.INFO, f"{log_id}moving {track_obj_that_moved.name} to new stored cb type index {next_callback_type_index}")
            self.data.rekey_track_list_of_callback_type(callback_track_type, next_callback_type_index, all_track_objs_of_type, track_obj_that_moved)
            self.track_changed(next_song_index)
        # else:
        #     # stored and live counts don't match, a track was added or removed, not moved
        #     pass

    def unselected_tracks_changed(self, found_changed_track_callback_type, callback_type_track_count):
        # Not sure unselected "tracks" can actually just change in this respect.  Say master track is selected when "all return tracks"
        # change, and the change is not adding or removing tracks from view (folding/unfolding a group track for example)
        log_id = "EAH.unselected_tracks_changed: "
        cb_type = track_callback_types[found_changed_track_callback_type]
        msg = f"{log_id}the count ({callback_type_track_count} of {cb_type} track callback type {found_changed_track_callback_type} "
        self.main_script().log_message(logging.ERROR, msg + "tracks didn't change, but the tracks_changed() callback fired. Did the track list order change?")

    def tracks_added(self, selected_song_track_index_after, tracks_of_type_after, callback_type):
        """automatically adds existing devices on added Live (song) track objects"""
        log_id = "EAH.tracks_added: "
        log_msg = f"{log_id}can't add master"
        if selected_song_track_index_after != self.last_selected_track_index and self.last_selected_track_callback_type == callback_type:
            # tracks (of the same callback type) were added to the left of the selected track
            update_selected_track_index_after = True
        else:
            # tracks were added to the right of the selected track
            update_selected_track_index_after = False

        final_callback_type_track_count = 0  # minimum == no return tracks (always 1 master and 1 visible for 2 total minimum)
        trace_level = self.log_levels["TRACE"]
        self.main_script().log_message(trace_level, f"{log_id}BEFORE: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        if callback_type == 0:
            final_callback_type_track_count = len(tracks_of_type_after)
            self.unselected_tracks_added(callback_type, final_callback_type_track_count)
            assert final_callback_type_track_count == self.data.plain_track_count
            final_callback_type_track_count += self.data.return_track_count
        elif callback_type == 1:
            final_callback_type_track_count = len(tracks_of_type_after)
            self.unselected_tracks_added(callback_type, final_callback_type_track_count)
            assert final_callback_type_track_count == self.data.return_track_count
            final_callback_type_track_count += self.data.plain_track_count

        if update_selected_track_index_after:
            self.last_selected_track_index = selected_song_track_index_after

        self.main_script().log_message(trace_level, f"{log_id}AFTER: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        assert final_callback_type_track_count == self.data.total_track_count - 1  # not counting master here


    def unselected_tracks_added(self, found_changed_track_callback_type, callback_type_track_count):
        """automatically adds existing devices on input Live track objects"""
        # unselected means we can't find the tracks that "came into view" in the list of tracks of this callback type
        # by the selected track index.  When tracks are added, no tracks are invalidated, we can search for the
        # index of the first liveobj_valid track not equal to the stored track reference at that callback type index,
        # add that track at that index, rinse and repeat. Imagine unfolding a group track using a mouse while any other track is selected,
        # the "added tracks" will occupy indexes formerly occupied by non-group tracks (of the same callback type) that shifted right to make room (index += 1)
        log_id = "EAH.unselected_tracks_added: "
        tracks_of_type = self.main_script().song().visible_tracks
        rtns_offset = len(tracks_of_type)
        t_type = track_callback_types[found_changed_track_callback_type]
        if found_changed_track_callback_type == 1:
            tracks_of_type = self.main_script().song().return_tracks
        assert len(tracks_of_type) == callback_type_track_count
        changed_track_type_table = self.data.get_all_tracks_by_type_key(t_type)
        at_index = 0

        table_size = len(changed_track_type_table.keys())
        # self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")
        while len(changed_track_type_table.keys()) < callback_type_track_count and at_index < len(tracks_of_type):
            track_obj = tracks_of_type[at_index]
            if at_index < len(changed_track_type_table.keys()) and track_obj == changed_track_type_table[at_index].active_track.track:
                # msg = f"{log_id}{t_type} tracks added, but cb type index {at_index} track_ref matches {track_obj.name}, no add"
                # self.main_script().log_message(logging.DEBUG, msg)
                pass
            else:
                msg = f"{log_id}"
                if self.main_script().current_script_log_level < logging.DEBUG:
                    msg += f"{t_type} tracks added, and cb type index {at_index} track_ref doesn't equal {track_obj.name}, "
                if found_changed_track_callback_type == 1:
                    self.main_script().log_message(logging.DEBUG, msg + f"adding unselected track at returns offset track index {rtns_offset + at_index}")
                    self.track_added(rtns_offset + at_index, track_obj, is_selected=False, found_changed_track_callback_type=1)
                else:
                    self.main_script().log_message(logging.DEBUG, msg + f"adding unselected track at plains track index {at_index}")
                    self.track_added(at_index, track_obj, is_selected=False, found_changed_track_callback_type=0)
            at_index += 1
            table_size = len(self.data.get_all_tracks_by_type_key(t_type))
        assert len(changed_track_type_table.keys()) == callback_type_track_count == table_size

    def track_added(self, song_track_index, track_obj=None, is_selected=True, found_changed_track_callback_type=2):
        """automatically adds existing devices on input Live track objects"""

        if song_track_index == self.data.plain_track_count and found_changed_track_callback_type < 1:
            # new added track is "last" type 0 track, not "first" type 1 track, override normal add_track() logic
            self.data.add_track_by_callback_type(track_callback_types[0], 0, song_track_index, track_obj, selected_device_index=0)
        elif song_track_index == self.data.total_track_count - 1 and found_changed_track_callback_type == 1: # total count minus master
            # new added track is "last" type 1 track, not a "new" master track, override normal add_track() logic
            rtns_index = song_track_index - self.data.plain_track_count
            self.data.add_track_by_callback_type(track_callback_types[1], self.data.plain_track_count, rtns_index, track_obj, selected_device_index=0)
        else: # not a "callback type boundary" case
            cb_type = self.data.get_callback_type_for_song_index(song_track_index)
            # msg = f"EAH.track_added: get_cb_type {cb_type} for input index {song_track_index} and "
            # self.main_script().log_message(logging.DEBUG, msg + f"input found type {found_changed_track_callback_type}")
            self.data.add_track(track_obj, cb_type, song_track_index)

        if is_selected:
            self.last_selected_track_index = song_track_index
        else:
            if self.last_selected_track_index < self.data.plain_track_count + self.data.return_track_count:
                self.last_selected_track_index = self.last_selected_track_index + 1
            else:
                self.last_selected_track_index = self.master_track_index


    def tracks_deleted(self, selected_song_track_index_after, tracks_of_type_after, callback_type):
        log_id = "EAH.tracks_deleted: "
        log_msg = f"{log_id}can't remove master"
        if selected_song_track_index_after != self.last_selected_track_index and self.last_selected_track_callback_type == callback_type:
            # tracks (of the same callback type) were removed to the left of the selected track
            update_selected_track_index_after = True
        else:
            # tracks were removed to the right of the selected track
            update_selected_track_index_after = False
        final_callback_type_track_count = 0 # minimum == no return tracks (total minimum is 2 == 1 plain + 1 master)

        trace_level = self.log_levels["TRACE"]
        self.main_script().log_message(trace_level, f"{log_id}BEFORE: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        if callback_type == 0:
            nbr_to_remove = self.data.plain_track_count - len(tracks_of_type_after)
            final_callback_type_track_count = self.data.plain_track_count - nbr_to_remove
            self.unselected_tracks_deleted(callback_type, final_callback_type_track_count)
            assert final_callback_type_track_count == self.data.plain_track_count
            final_callback_type_track_count += self.data.return_track_count
        elif callback_type == 1:
            nbr_to_remove = self.data.return_track_count - len(tracks_of_type_after)
            final_callback_type_track_count = self.data.return_track_count - nbr_to_remove
            self.unselected_tracks_deleted(callback_type, final_callback_type_track_count)
            assert final_callback_type_track_count == self.data.return_track_count
            final_callback_type_track_count += self.data.plain_track_count
        # else:
        #     # can't remove master
        if update_selected_track_index_after:
            self.last_selected_track_index = selected_song_track_index_after

        self.main_script().log_message(trace_level, f"{log_id}AFTER: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        assert final_callback_type_track_count == self.data.total_track_count - 1 # not counting master here

    def unselected_tracks_deleted(self, found_changed_track_callback_type, callback_type_track_count):
        # when deleted tracks "disappear from view" the stored track references at the "deleted indexes" become not liveobj valid
        # when grouped tracks "disappear from view" the stored track references at the "deleted indexes" remain liveobj valid and become not visible
        log_id = "EAH.unselected_tracks_deleted: "
        tracks_of_type = self.main_script().song().visible_tracks
        rtns_offset = len(tracks_of_type)
        t_type_key = track_callback_types[found_changed_track_callback_type]
        trace_level = self.log_levels["TRACE"]

        if found_changed_track_callback_type == 1:
            tracks_of_type = self.main_script().song().return_tracks
        assert len(tracks_of_type) == callback_type_track_count
        changed_track_type_table = self.data.get_all_tracks_by_type_key(t_type_key)
        table_size = len(changed_track_type_table.keys())
        nbr_tracks_removed = table_size - callback_type_track_count
        selected_callback_type_before = self.last_selected_track_callback_type

        self.main_script().log_message(trace_level, f"{log_id}BEFORE: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")
        shallow_copy = changed_track_type_table.copy()
        type_index_offset = 0
        for type_index in shallow_copy.keys():
            live_track_obj = shallow_copy[type_index].active_track.track
            if not liveobj_valid(live_track_obj) or not live_track_obj.is_visible:
                cb_type = "returns" if found_changed_track_callback_type == 1 else "plains"
                self.main_script().log_message(logging.DEBUG, f"{log_id}deleting track ref at {cb_type} track type index {type_index}")
                type_index -= type_index_offset # changed_track_type_table is getting smaller and smaller
                type_index_before_deleted_track = 0 if type_index < 1 else type_index - 1
                self.data.remove_track_by_callback_type(track_callback_types[found_changed_track_callback_type], type_index_before_deleted_track)
                type_index_offset += 1
        table_size = len(self.data.get_all_tracks_by_type_key(t_type_key).keys())
        self.main_script().log_message(trace_level, f"{log_id}AFTER: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")

        assert len(changed_track_type_table.keys()) == callback_type_track_count == table_size

        oopsie = False
        # iterating through the remaining track list "again" is an expensive validation if everything is working as expected
        if self.main_script().current_script_log_level < logging.DEBUG:
            for t_obj, t_ref in zip_longest(tracks_of_type, changed_track_type_table.values()):
                if liveobj_changed(t_obj, t_ref.active_track.track):
                    msg = f"{log_id}after deletes, stored reference {t_ref.active_track.track_name} doesn't equal Live object {t_obj.name} at same index"
                    self.main_script().log_message(logging.WARNING, msg)
                    oopsie = True
            if not oopsie:
                msg = f"{log_id}after deletes, all stored references equal the Live objects at same indexes"
                self.main_script().log_message(logging.INFO, msg)

        next_selected_index = self.last_selected_track_index - nbr_tracks_removed
        if found_changed_track_callback_type == 0 and selected_callback_type_before > 0:
            # given: 1 (expanded) Group of 2 and 3 others makes 6 plain tracks, add 2 returns plus master makes 9 total tracks
            # if the last selected index was 7 (last return track) before the two type 0 "unselected tracks" were removed because the group collapsed
            # the stored "last selected callback type index" doesn't change, but the stored "last selected song index" does
            msg = f"{log_id}shifting local stored last selected (song) index from {self.last_selected_track_index} to {next_selected_index}"
            self.main_script().log_message(logging.DEBUG, msg)
            self.last_selected_track_index = next_selected_index
        elif found_changed_track_callback_type == 1 and selected_callback_type_before > 0:
            if selected_callback_type_before == 2:
                # return track(s) removed from view while master was selected  (can happen by undo/redo while master selected)
                msg = f"{log_id}shifting local stored (master) last selected (song) index from {self.last_selected_track_index} to {next_selected_index}"
                self.main_script().log_message(logging.DEBUG, msg)
                self.last_selected_track_index = next_selected_index
            else:  # selected_callback_type_before == 1
                # if unselected return track left of selected return track was deleted (by undo/redo), decrement selected index
                # else don't decrement selected index. Ambiguous conditions - find song selected index directly
                # self.find_track_index() returns a tuple (selected_index, callback_track_type_of_selected_index, callback_type_index, nbr_song_tracks)
                track_info = self.find_track_index(self.song().view.selected_track)
                self.last_selected_track_index = track_info[0]
        # else:
        #     msg = f"{log_id}last selected index remains {self.last_selected_track_index} because last selected cb type was {selected_callback_type_before}"
        #     self.main_script().log_message(logging.DEBUG, msg)


    def track_deleted(self, track_index_before_delete_index, is_selected=True):
        """input track_index value should be 'before' (one less than) the index to be deleted"""
        log_id = "EAH.track_deleted: "
        # if self.last_selected_track_index != track_index:
        #     msg = f"{log_id} deleting track index {track_index} that is not last_selected_index {self.last_selected_track_index}"
        #     self.main_script().log_message(logging.DEBUG, msg)
        # track_ref = self.data.get_track(track_index_before_delete_index)
        # self.main_script().log_message(logging.DEBUG, f"{log_id}removing track_ref {track_ref.track_name} at index {track_index}")
        self.data.remove_track(0 if track_index_before_delete_index < 0 else track_index_before_delete_index)
        if is_selected:
            self.last_selected_track_index = 0 if track_index_before_delete_index < 1 else track_index_before_delete_index
        else:
            self.last_selected_track_index = 0 if self.last_selected_track_index < 1 else self.last_selected_track_index
            # self.main_script().log_message(logging.DEBUG, f"{log_id}removed unselected track reference at song index {track_index}")
        # track_ref = self.data.get_track(self.last_selected_track_index)
        # self.main_script().log_message(logging.DEBUG, f"{log_id}selected track_ref is now {track_ref.track_name} at index {self.last_selected_track_index}")


    def device_added_deleted_or_changed(self, all_track_devices, selected_device, selected_device_idx):
        log_id = "EAH.device_added_deleted_or_changed: "
        new_device_count_track = len(all_track_devices)
        trace_level = self.log_levels["TRACE"]
        if self.main_script().current_script_log_level < trace_level:
            idx = 0
            log_msg = f"{log_id}device in input device list at index<{idx}> is "
            for device in all_track_devices:
                if liveobj_valid(device):
                    # pass
                    self.main_script().log_message(logging.DEBUG, f"{log_msg}a valid Live object named <{device.name}>")
                else:
                    self.main_script().log_message(logging.WARNING, f"{log_msg}<None> or a lost weakref")
                idx += 1
                log_msg = "{0}device in input device list at index<{1}> is ".format(log_id, idx)
            if not new_device_count_track == idx:
                self.main_script().log_message(logging.WARNING, f"{log_id}assumption issue, collection size {new_device_count_track} doesn't match iterator {idx}")
            if liveobj_valid(selected_device):
                self.main_script().log_message(logging.DEBUG, f"{log_id}input selected_device is a valid Live object named<{selected_device.name}>")
            if selected_device_idx > -1:
                self.main_script().log_message(logging.DEBUG, f"{log_id}input selected_device_idx<{selected_device_idx}> points to a non-negative index")

        active_device_list_ref = self.data.get_active_track_details_at_song_index(self.last_selected_track_index)
        last_track_ref = active_device_list_ref.active_track
        old_device_count_track = last_track_ref.device_count
        old_selected_device_index = last_track_ref.selected_device_index # could be None
        msg = f"{log_id}track index ref {last_track_ref.index} has name {last_track_ref.track_name} and old device count {old_device_count_track}"
        self.main_script().log_message(trace_level, msg)

        device_was_added = new_device_count_track > old_device_count_track
        device_was_removed = new_device_count_track < old_device_count_track
        selected_device_was_changed = new_device_count_track > 0 and new_device_count_track == old_device_count_track
        no_devices_on_track = new_device_count_track == 0
        rack_devices_deleted = old_device_count_track - new_device_count_track if device_was_removed else 0

        # log_msg = f"{log_id}input selected_device_idx<{selected_device_idx}> and input device list len<{new_device_count_track}> "
        # if selected_device_idx is None or selected_device_idx == -1:
        #     self.main_script().log_message(logging.DEBUG, f"{log_msg}agree that no devices currently populate the device chain for this track")
        #     assert no_devices_on_track
        # else:
        #     self.main_script().log_message(logging.DEBUG, f"{log_msg}allow modification of the device chain for this track")

        new_device_index = 0
        deleted_device_index = 0
        changed_device_index = 0
        rtn_device_index = -1
        found_input_device_index = False  # selected_device is in all_devices

        # if there are no devices on track, there are no devices in input all_devices list and this loop is not entered,
        # all "change indexes" stay 0. If a device was deleted, selected_device will be at the index before the deleted device
        for index,device in enumerate(all_track_devices):
            if selected_device == device:
                new_device_index = index
                deleted_device_index = index
                changed_device_index = index
                rtn_device_index = index
                found_input_device_index = True
                # log_msg = f"{log_id}matched input selected_device<{selected_device.name}> with device<{device.name}> at index<{index}> of input device list"
                # self.main_script().log_message(logging.DEBUG, log_msg)
                break


        current_bank = last_track_ref.device_bank_index_of_selected_device # cb = self.t_d_bank_current[self.t_current]

        if found_input_device_index:
            last_track_ref.selected_device_index = rtn_device_index
            self.next_selected_device_index = rtn_device_index
        else:
            last_track_ref.selected_device_index = None
            current_bank = last_track_ref.device_bank_index_of_selected_device

        self.data.set_track(last_track_ref)
        # FROM HERE: f"the found 'track_changed' event changed device index <{index}> and device <{device.name}> represent 'source of truth'"
        # device == self.last_selected_track.devices[index]
        # so we could return rtn_device_index right here, except for updating the "assignment history" database

        if device_was_added:
            self.update_device_counts_on_addition(new_device_index, all_track_devices, old_device_count_track, new_device_count_track)

        elif device_was_removed:
            self.update_device_counts_on_removal(deleted_device_index, rack_devices_deleted, found_input_device_index,
                                                 old_device_count_track, new_device_count_track)

        elif selected_device_was_changed:
            self.update_device_counts_on_change(all_track_devices, selected_device, old_selected_device_index, changed_device_index, new_device_count_track)

        return rtn_device_index

    def update_device_counts_on_addition(self, new_device_index, all_devices, old_device_count_track, new_device_count_track):
        log_id = f"EAH.update_device_counts_on_addition: "
        new_device = all_devices[new_device_index]
        last_track_ref = self.data.get_track(self.last_selected_track_index)
        if not last_track_ref.device_count < new_device_count_track:
            self.main_script().log_message(logging.WARNING, f"{log_id}assumption issue: nothing added, what was updated?")
        else:
            self.data.add_device(last_track_ref.index, last_track_ref.index_by_type, new_device_index, new_device)
            # msg = f"{log_id}updated {last_track_ref.track_name}, device added {new_device.name} at index {new_device_index}, new device count is {last_track_ref.device_count}"
            # self.main_script().log_message(self.log_levels["TRACE"], msg)


    def update_device_counts_on_removal(self, deleted_device_index, rack_devices_deleted, found_input_device_index,
                                        old_device_count_track, new_device_count_track):
        log_id = "EAH.update_device_counts_on_removal: "
        # self.main_script().log_message(logging.DEBUG, f"{log_id}deletion index {deleted_device_index}")

        # last_device_in_chain = deleted_device_index == old_device_count_track - 1  # 0 != -1 here
        # empty_chain = old_device_count_track == 0 and not found_input_device_index
        
        last_track_ref = self.data.get_track(self.last_selected_track_index)
        # last_track_ref counts updated automatically by remove_device()
        self.data.remove_device(last_track_ref.index, deleted_device_index - 1)
        # msg = f"{log_id}updated track {last_track_ref.track_name}, removed device at index {deleted_device_index} new device count is {last_track_ref.device_count}"
        # self.main_script().log_message(logging.DEBUG, msg)

        decremented_device_count_track = self.data.get_track(self.last_selected_track_index).device_count
        max_needed_device_banks = int(math.ceil(decremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
        if max_needed_device_banks != last_track_ref.required_device_banks:
            msg = f"{log_id}assumption issue: {max_needed_device_banks} calculated and required_device_banks {last_track_ref.required_device_banks} not matching"
            self.main_script().log_message(logging.ERROR, msg)


    def update_device_counts_on_change(self, all_track_devices, selected_device, old_selected_device_index, changed_device_index, new_device_count_track):
        # self.data.rekey_device_list_by_track_callback_type() is called directly from EC.device_list_changed() as needed,
        # just updating the stored selected device index to the new selected index here

        last_track_ref = self.data.get_track(self.last_selected_track_index)
        last_track_ref.selected_device_index = changed_device_index
        self.last_selected_device_index = changed_device_index
        assert new_device_count_track == last_track_ref.device_count
        self.data.set_track(last_track_ref)

