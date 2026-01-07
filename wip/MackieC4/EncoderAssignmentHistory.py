
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
import sys

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
        """ index of this track's selected device in the track's device list """
        self._selected_devices_bank_index = None if selected_device_index is None else selected_device_index % SETUP_DB_DEVICE_BANK_SIZE
        """ 0 - 7 index within a device bank where the selected device index would fall, automatically calculated 
            when selected device changes. (9th device falls in the second bank at bank index 0) """
        self._track_view_device_bank_index = self._selected_devices_bank_index
        """ device bank index currently "on display" on the C4 (and selected in Live) of this track's device-bank list (0 - 9 if the track device list has 80 devices) """
        if selected_device_index is None or self.required_device_banks < 1:
            self._device_bank_index_of_selected_device = None
            """ device bank index of this track's selected device in the track's device-bank list (0 unless the track has more than 8 devices), automatically calculated 
when selected device changes. This value can differ from the device bank index currently "on display". You can 'browse' device banks without changing selected devices. """
        else:
            self._device_bank_index_of_selected_device = int(math.floor(selected_device_index % self.required_device_banks))

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
        self.track_index = song_track_index
        self.track_index_by_type = callback_type_index
        self._parameter_count = parameter_count
        self._selected_parameter_index = selected_parameter_index
        """ index of this device's selected parameter in the device's parameter list """
        self._parameter_bank_count = math.ceil(parameter_count // SETUP_DB_PARAM_BANK_SIZE)
        """ the number of parameter banks worth of parameters in the device's parameter list (0 unless the device has more than 24 parameters) """
        self._selected_parameters_bank_index = selected_parameter_index % SETUP_DB_PARAM_BANK_SIZE
        """ the index of the parameter bank where the selected parameter would fall (0 - 23 unless SETUP_DB_PARAM_BANK_SIZE changes) """        

        self._device_view_parameter_bank_index = self._selected_parameters_bank_index
        """ device bank index currently "on display" on the C4 (and selected in Live) of this device's parameter-bank list (indexes 0 - 9 if the device parameter list 
        has 240 parameters) """
        
        if self.required_parameter_banks < 1:
            self._bank_index_of_selected_parameter = 0
            """ parameter bank index of this device's selected parameter in the device's parameter-bank list (0 unless the device has more than 8 parameters), 
automatically calculated when selected parameter changes. This value can differ from the parameter bank index currently "on display". You can 'browse' parameter 
banks without changing selected parameters. """  
        else:
            self._bank_index_of_selected_parameter = int(math.floor(selected_parameter_index % self.required_parameter_banks))

    def __str__(self):
        if self is None:
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
    
    # @parameter_count.setter
    # def parameter_count(self, new_count):
    #     """ parameter count is automatically set by devices and constant """
    #     self._parameter_count = new_count
    #     self._parameter_bank_count = math.ceil(self._parameter_count // SETUP_DB_PARAM_BANK_SIZE)

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
        return self._device_view_parameter_bank_index
    @device_parameter_bank_view_index.setter
    def device_parameter_bank_view_index(self, next_bank_index):
        self._device_view_parameter_bank_index = next_bank_index


class ActiveDeviceList:

    def __init__(self, active_track_ref, devices=None):

        self.active_track = active_track_ref
        self.devices = {}
        if devices is not None:
            for i, d in enumerate(devices):
                d_ref = ActiveDevice(d, i, len(d.parameters), song_track_index=self.song_track_index, callback_type_index=self.track_index_by_type)
                self.devices[i] = d_ref

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
        """ index of this Track within its callback type collection, except the master track index is not really in a collection (since there is only ever one master track),
         the master track index always equals the number of visible + return tracks in the song (and moves automatically when tracks are added or removed from the song """
        return self.active_track.index_by_type
    @property
    def device_count(self):
        """ The number of devices on this Track """
        return self.active_track.device_count
    @property
    def selected_device_index(self):
        """ The index of the selected device in the device list (of size == device_count)"""
        return self.active_track.selected_device_index

    @property
    def is_device_list_empty(self):
        return self.devices is None or len(self.devices.keys()) < 1

    def to_string(self):
        return self.active_track.to_string()


track_callback_types = {0: "plain", 1: "return", 2: "master"}
""" keys [0, 1, 2] are the track callback types used by Live; values ["plain", "return", "master"] are the associated 'primary keys' used for local SongData storage """

class SongData(object):
    # keys "plain", "return", and "master" are the "primary key column" in self.track_table and device_table
    # values 0, 1, and 2 are the track callback types used elsewhere in the script
    table_keys = {"plain": 0, "return": 1, "master": 2}
    """ keys ["plain", "return", "master"] are the 'primary keys' used in SongData; values [0, 1, 2] are the track callback types used by Live """

    @depends(logger=None, get_device_list=None)
    def __init__(self, logger=None, get_device_list=None):
        self.logger = logger
        self.extend_device_list = get_device_list
        # enable "class logging" to see mostly debug logging output from __shift_keys_right() and __shift_keys_left() methods
        # uncomment logging messages in other class methods to see more verbose debug logging from earlier in the class method call stack
        self.__class_logging = True # False #
        self.device_list_table = {track_callback_types[0]: {},
                             track_callback_types[1]: {},
                             track_callback_types[2]: {}}
        
        self.__master_track_count = 1
        self.__initializing_database = True

    def log_msg(self, level, msg):
        if self.__class_logging:
            self.logger(level, msg)

    def get_callback_type_for_song_index(self, track_index):
        rtn = 3
        if track_index < self.plain_track_count:
            rtn = 0
        elif track_index < self.plain_track_count + self.return_track_count:
            rtn = 1
        elif track_index == self.plain_track_count + self.return_track_count:
            rtn = 2
        return rtn

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

    def get_active_device_list_at_song_index(self, song_track_index) -> ActiveDeviceList | None:
        rtns_index = song_track_index - self.plain_track_count
        if song_track_index < self.plain_track_count:
            return self.get_active_device_list_reference(track_callback_types[0], song_track_index)
        elif rtns_index < self.return_track_count:
            return self.get_active_device_list_reference(track_callback_types[1], rtns_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            return self.get_active_device_list_reference(track_callback_types[2], song_track_index)
        return None

    def get_active_device_list_reference(self, track_callback_type_key, track_index_by_type):
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
        track_device_list = ActiveDeviceList(track_ref, ext_devices)
        self.device_list_table[track_callback_types[2]][song_index] = track_device_list
        track_device_list = self.device_list_table[track_callback_types[2]][song_index]
        self.log_msg(logging.DEBUG, f"EAH.SD.init_master_track: AFTER: master ref {track_device_list.active_track} at index {song_index}")
        # only use self._insert_track_slot() for non-master tracks (ordered lists with indexes from 0)

    def update_master_track_index(self, master_device_list_ref):
        if len(self.device_list_table[track_callback_types[2]]) > 0:
            self.clear_tracks_by_type_key(track_callback_types[2]) # remove master_device_list_ref with key == old master index
        master_ref = master_device_list_ref.active_track
        master_ref.index = self.master_track_index
        master_ref.index_by_type = self.master_track_index
        master_device_list_ref.active_track = master_ref
        # add master_ref back with new key == self.master_track_index
        self.device_list_table[track_callback_types[2]][self.master_track_index] = master_device_list_ref
        # only use self._insert_track_slot() for non-master tracks (ordered lists with indexes from 0)

    # NOTE: no functions to update any other "internal stored object indexes" to match their associated track or device "slot index" (map key)"
    #       See get_track() and get_device() below, the ActiveTrack and ActiveDevice object internal property index values are updated automatically
    #       before ActiveTrack or ActiveDevice objects return from get_track() and get_device() (so they can "set themselves" back, see set_device() for example)
    # The stored internal property index values fall out of sync with their actual associated "map key index" values every time tracks are added to or removed from the Song
    # I.E. This class.  (Except for Master Track index, ) The internal indexes are not resynchronized / updated until "fetched" by get_track() or get_device()

    def clear_all_tracks(self):
        self.clear_tracks_by_type_key(track_callback_types[0])
        self.clear_tracks_by_type_key(track_callback_types[1])
        self.clear_tracks_by_type_key(track_callback_types[2])

    def clear_tracks_by_type_key(self, track_callback_type_key):
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

    def __update_track_devices(self, primary_key, track_type_index, device_count, selected_device_index):
        stored_device_refs = self.get_track_device_map_by_callback_type(primary_key, track_type_index)
        assert len(stored_device_refs.keys()) == device_count
        track_ref = self.get_track_by_type_key(primary_key, track_type_index)
        track_ref.device_count = device_count
        assert selected_device_index < device_count
        track_ref.selected_device_index = selected_device_index
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

    def get_all_tracks_by_type_key(self, track_callback_type_key):
        return self.device_list_table[track_callback_type_key]

    def get_track_by_type_key(self, track_callback_type_key, track_index_by_type):
        return self.get_all_tracks_by_type_key(track_callback_type_key)[track_index_by_type].active_track

    def set_track_by_type_key(self, track_callback_type_key, track_index_by_type, active_track):
        self.device_list_table[track_callback_type_key][track_index_by_type].active_track = active_track

    def set_track(self, active_track):
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

    def init_tracks_by_callback_type(self, track_callback_type_key, tracks):
        rtn = None
        log_id = f"EAH.SD.init_tracks_by_callback_type: "
        self.log_msg(logging.DEBUG, f"{log_id}getting master track at index {self.master_track_index}")
        master_device_list_ref = self.get_active_device_list_reference(track_callback_types[2], self.master_track_index)
        last_master_track_ref = master_device_list_ref.active_track
        # last_master_track_ref = self.get_master_track(self.master_track_index)
        # self.log_msg(logging.DEBUG, f"{log_id}master track before {track_callback_type_key} tracks initialized: {last_master_track_ref}")
        if len(self.device_list_table[track_callback_type_key]) > 0:
            rtn = f"{log_id}assumption issue: device list table {track_callback_type_key} not already clear?"

        if rtn is None:
            track_type_index = 0
            track_count = len(tracks)
            song_index = 0
            if self.table_keys[track_callback_type_key] > 0:
                song_index = self.plain_track_count
            for track in tracks:
                self.add_track_by_callback_type(track_callback_type_key, song_index, track_type_index, track)
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

    def add_track(self, track, track_type, song_track_index):

        rtns_index = song_track_index - self.plain_track_count
        song_index = 0
        if track_type > 0:
            song_index = self.plain_track_count

        if song_track_index < self.plain_track_count:
            self.add_track_by_callback_type(track_callback_types[0], song_index, song_track_index, track)
        elif rtns_index < self.return_track_count:
            self.add_track_by_callback_type(track_callback_types[1], song_index, rtns_index, track)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            raise RuntimeError(f"can't add or remove master track at index {song_track_index}")
        else:
            raise RuntimeError(f"can't add track at OOB index {song_track_index}, max new index is less than {self.master_track_index}")

    def add_track_by_callback_type(self, track_callback_type_key, song_track_index, track_index_by_type, track):
        log_id = "EAH.SD.add_track_by_callback_type: "
        master_device_list_ref = self.get_active_device_list_reference(track_callback_types[2], self.master_track_index)
        last_master_track_ref = master_device_list_ref.active_track
        ext_devices = None if len(track.devices) < 1 else self.extend_device_list(track.devices)
        nbr_devices = 0 if ext_devices is None else len(ext_devices)
        selected_device_index = 0 if nbr_devices > 0 else None
        cumulative_song_index = song_track_index + track_index_by_type
        track_ref = ActiveTrack(track, self.table_keys[track_callback_type_key], cumulative_song_index, track_index_by_type, nbr_devices, selected_device_index)
        track_device_list_ref = ActiveDeviceList(track_ref, devices=ext_devices)
        self._insert_track_slot(self.device_list_table[track_callback_type_key], track_index_by_type, track_device_list_ref)
        if last_master_track_ref.index < self.master_track_index:
            self.log_msg(logging.DEBUG, f"{log_id}after adding track, updating master track index to {self.master_track_index}")
            self.update_master_track_index(master_device_list_ref)

    def remove_track(self, song_track_index):
        rtns_index = song_track_index - self.plain_track_count
        # log_msg = f"EAH.SD.remove_track: at song track index {song_track_index}"
        # self.log_msg(logging.DEBUG, log_msg)
        if song_track_index < self.plain_track_count:
            self.remove_track_by_callback_type(track_callback_types[0], song_track_index)
        elif rtns_index < self.return_track_count:
            self.remove_track_by_callback_type(track_callback_types[1], rtns_index)
        else:
            raise RuntimeError(f"can't remove track at OOB index {song_track_index}, can't remove master_track {self.master_track_index} or after")

    def remove_track_by_callback_type(self, track_callback_type_key, track_index_by_type):
        log_id = "EAH.SD.remove_track_by_callback_type: "
        master_device_list_ref = self.get_active_device_list_reference(track_callback_types[2], self.master_track_index)
        last_master_track_ref = master_device_list_ref.active_track
        # last_master_track_ref = self.get_track(self.master_track_index)
        old = self.device_list_table[track_callback_type_key][track_index_by_type]
        # if old.track_name == "Invalidobj":
        #     log_msg = f"{log_id}collapsing slot holding invalid liveobj "
        # else:
        #     log_msg = f"{log_id}collapsing slot holding a valid liveobj {old.track_name} "
        #
        # self.log_msg(logging.DEBUG, log_msg)
        # log_msg = f"{log_id}{track_callback_type_key} track at {track_callback_type_key} callback type index {track_index_by_type}: {old} "
        # self.log_msg(logging.DEBUG, log_msg)
        # self.log_msg(logging.DEBUG, f"{log_id}BEFORE: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        self._collapse_track_slot(self.device_list_table[track_callback_type_key], track_index_by_type)
        # new_count = len(self.track_table[track_callback_type_key])
        # self.log_msg(logging.DEBUG, f"{log_id}AFTER: new track count={new_count}")
        self.log_msg(logging.DEBUG, f"{log_id}AFTER: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        if last_master_track_ref is not None and last_master_track_ref.index_by_type != self.master_track_index:
            self.update_master_track_index(master_device_list_ref)

    def get_track_device_map(self, song_track_index):
        device_map = None
        rtns_index = song_track_index - self.plain_track_count
        # log_msg = f"EAH.SD.get_track_device_map: at song track index "
        try:
            if song_track_index < self.plain_track_count:
                # self.log_msg(logging.DEBUG, log_msg + song_track_index)
                device_map = self.get_track_device_map_by_callback_type(track_callback_types[0], song_track_index)
            elif rtns_index < self.return_track_count:
                # self.log_msg(logging.DEBUG, log_msg + rtns_index)
                device_map =  self.get_track_device_map_by_callback_type(track_callback_types[1], rtns_index)
            elif song_track_index == self.plain_track_count + self.return_track_count:
                # self.log_msg(logging.DEBUG, log_msg + song_track_index)
                device_map = self.get_track_device_map_by_callback_type(track_callback_types[0], song_track_index)
        except KeyError:
            # track should always have a device map that might be empty
            raise RuntimeError(f"can't get device map for track at song index {song_track_index}")

        return device_map

    def get_track_device_map_by_callback_type(self, track_callback_type_key, track_index_by_type):
        # log_id = "EAH.SD.get_track_device_map_by_callback_type: "
        # self.log_msg(logging.DEBUG, f"{log_id}returning device map from {track_callback_type_key} track index {track_index_by_type}")
        return self.device_list_table[track_callback_type_key][track_index_by_type].devices


    def set_track_device_map_by_callback_type(self, track_callback_type_key, track_index_by_type, device_map):
        # log_id = "EAH.SD.set_track_device_map_by_callback_type: "
        # self.log_msg(logging.DEBUG, f"{log_id}setting device map for {track_callback_type_key} track index {track_index_by_type}")
        self.device_list_table[track_callback_type_key][track_index_by_type].devices = device_map

    def get_device(self, song_track_index, device_index)-> ActiveDevice | None:
        active_device = None
        device_map = self.get_track_device_map(song_track_index)
        if device_map is not None and device_index < len(device_map.keys()):
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

    def set_device(self, active_device):
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

    def add_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index, device_ref):
        log_msg = f"EAH.SD.add_device_by_track_callback_type: adding device to {track_callback_type_key} track at callback index {callback_type_index} and "
        self.log_msg(logging.DEBUG, log_msg + f"device list index {device_index}")
        device_map = self.get_active_device_list_reference(track_callback_type_key, callback_type_index).devices
        if device_index < len(device_map.keys()) and device_map[device_index] == device_ref:
            log_msg = f"EAH.SD.add_device_by_track_callback_type: device to add already present in device map at index {device_map}, device not added again"
            self.log_msg(logging.DEBUG, log_msg)
        else:
            self._insert_track_device_list_slot(device_map, device_index, device_ref)
            old_count = self.get_track_by_type_key(track_callback_type_key, callback_type_index).device_count
            log_msg = f"EAH.SD.add_device_by_track_callback_type: incrementing device count and setting selected device index values on associated {track_callback_type_key} "
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

    def rekey_device_list_by_track_callback_type(self, track_callback_type_key, callback_type_index, all_track_devices, selected_device_obj):
        old_keyed_map = self.get_track_device_map_by_callback_type(track_callback_type_key, callback_type_index)
        new_keyed_map = {}
        track_ref = self.get_track_by_type_key(track_callback_type_key, callback_type_index)
        if len(all_track_devices) == len(old_keyed_map.keys()) == track_ref.device_count:
            for new_index, device_obj in enumerate(all_track_devices):
                for device_ref_index in old_keyed_map.keys():
                    device_ref = old_keyed_map[device_ref_index]
                    if device_ref.device == device_obj:
                        new_keyed_map[new_index] = device_ref
                        if device_obj == selected_device_obj:
                            track_ref.selected_device_index = new_index
                        break
            assert len(old_keyed_map.keys()) == len(new_keyed_map.keys())
            old_keyed_map.update(new_keyed_map)
            self.set_track_device_map_by_callback_type(track_callback_type_key, callback_type_index, old_keyed_map)
        else:  # len(all_track_devices) == len(old_keyed_map.keys()) == track_ref.device_count
            log_msg = f"EAH.SD.rekey_device_list_by_track_callback_type: counts don't match, stored device list order not changed: "
            self.log_msg(logging.DEBUG, log_msg + f"new {len(all_track_devices)} old {len(old_keyed_map.keys())} old count {track_ref.device_count}")

    def remove_devices(self, song_track_index, nbr_devices_to_remove, track_device_list_first_remove_index=0):
        active_devices = self.get_track_device_map(song_track_index)
        if (track_device_list_first_remove_index < len(active_devices.keys()) and
                track_device_list_first_remove_index + nbr_devices_to_remove <= len(active_devices.keys())):  # 5 active devices remove 2 starting from index 3
            for i in range(track_device_list_first_remove_index, track_device_list_first_remove_index + nbr_devices_to_remove):
                self.remove_device(song_track_index, i)
        else:
            log_msg = f"EAH.SD.remove_devices: song track index {song_track_index} has {len(active_devices.keys())} active devices, can't remove "
            if not track_device_list_first_remove_index < len(active_devices.keys()):
                log_msg += f"any devices starting from OOB index {track_device_list_first_remove_index}"
            elif not track_device_list_first_remove_index + nbr_devices_to_remove <= len(active_devices.keys()):
                log_msg += f"{nbr_devices_to_remove} devices starting from index {track_device_list_first_remove_index}, not enough devices after index"
            self.log_msg(logging.DEBUG, log_msg)

        device_count = self.get_track(song_track_index).device_count
        nbr_remaining_devices = len(self.get_track_device_map(song_track_index))
        assert nbr_remaining_devices == track_device_list_first_remove_index == device_count


    def remove_device(self, song_track_index, device_index):
        rtns_index = song_track_index - self.plain_track_count
        # log_msg = f"EAH.SD.remove_device: at song track index {song_track_index} "
        # self.log_msg(logging.DEBUG, log_msg)
        if song_track_index < self.plain_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[0], song_track_index, device_index)
        elif rtns_index < self.return_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[1], rtns_index, device_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[2], song_track_index, device_index)
        else:
            raise RuntimeError(f"can't remove device at OOB track index {song_track_index}, max track index is master_track {self.master_track_index}")

    def remove_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index):
        # log_id = "EAH.SD.remove_device_by_track_callback_type: "
        # log_msg = f"{log_id}collapsing device at index {device_index} at {track_callback_type_key} "
        device_map = self.device_list_table[track_callback_type_key][callback_type_index].devices
        # self.log_msg(logging.DEBUG, log_msg + f"track callback index {callback_type_index}")
        # self.log_msg(logging.DEBUG, f"{log_id}BEFORE: device count {len(device_map)}")
        self._collapse_track_device_list_slot(device_map, device_index)
        # self.log_msg(logging.DEBUG, f"{log_id}AFTER: device count {len(device_map)}")
        self.device_list_table[track_callback_type_key][callback_type_index].devices = device_map
        track_ref = self.device_list_table[track_callback_type_key][callback_type_index].active_track
        # self.log_msg(logging.DEBUG, f"{log_id}after device removal BEFORE updating track ref {track_ref}")
        self._update_track_table_after_device_removal(track_ref, device_index)
        # self.log_msg(logging.DEBUG, f"{log_id}after device removal AFTER updating track ref {track_ref}")

    @staticmethod
    def _update_track_table_after_device_removal(track_ref, device_index):
        old_device_count = track_ref.device_count
        new_device_count = old_device_count - 1 if old_device_count > 0 else 0
        track_ref.device_count = new_device_count
        if 0 >= device_index < new_device_count:
            track_ref.selected_device_index = device_index
        elif device_index >= new_device_count:
            track_ref.selected_device_index = new_device_count - 1
        else:
            track_ref.selected_device_index = None
        return track_ref

    @staticmethod
    def _update_track_table_after_device_add(track_ref, at_device_index):
        old_device_count = track_ref.device_count
        new_device_count = old_device_count + 1
        track_ref.device_count = new_device_count
        if 0 >= at_device_index < new_device_count:
            track_ref.selected_device_index = at_device_index
        elif at_device_index >= new_device_count:
            track_ref.selected_device_index = new_device_count - 1
        else:
            track_ref.selected_device_index = None
        return track_ref

    def _insert_track_slot(self, type_dict, track_callback_type_index, track_device_list_ref)-> dict[int, ActiveDeviceList]:
        log_id = "EAH.SD._insert_track_slot: "
        if track_callback_type_index in type_dict.keys():
            type_dict = self.__shift_keys_right(type_dict, track_callback_type_index, track_device_list_ref)
        else:
            assert track_callback_type_index == len(type_dict.keys())
            self.log_msg(logging.DEBUG, f"{log_id}inserting last or only track of type at type index {track_callback_type_index}, no shift")
            type_dict[track_callback_type_index] = track_device_list_ref
        return type_dict

    def _insert_track_device_list_slot(self, type_dict, device_index, active_device)-> dict[int, ActiveDevice]:
        log_id = "EAH.SD._insert_track_device_list_slot: "
        if device_index in type_dict.keys():
            type_dict = self.__shift_keys_right(type_dict, device_index, active_device)
        else:
            assert device_index == len(type_dict.keys())
            self.log_msg(logging.DEBUG, f"{log_id}inserting last or only device at device index {device_index}, no shift")
            type_dict[device_index] = active_device
        return type_dict

    def _collapse_track_slot(self, type_dict, track_callback_type_index)-> dict[int, ActiveDeviceList]:
        return self.__shift_keys_left(type_dict, track_callback_type_index)

    def _collapse_track_device_list_slot(self, type_dict, device_index)-> dict[int, ActiveDevice]:
        return self.__shift_keys_left(type_dict, device_index)

    def __shift_keys_right(self, local_dict, key_of_add, value_to_add):
        log_id = "EAH.SD.__shift_keys_right: "
        # local_dict is either an active_track reference mapped by type index
        #     {callback_type_index=key_of_add: active_device_list=value_to_add}
        # or an active_device reference mapped by device index (active_device_list.devices)
        #     {device_index=key_of_add: active_device=value_to_add
        # "left slots" range is (0, key_of_add) if any
        # "right slots" range is (key_of_add, len(local_dict.keys()) if any (and index shifted right)
        # assumes local_dict is not empty
        vals = [x.active_track.common_name if isinstance(x, ActiveDeviceList) else x.common_name for x in local_dict.values()]
        txt_to_add = value_to_add.active_track.common_name if isinstance(value_to_add, ActiveDeviceList) else value_to_add.common_name
        self.log_msg(logging.DEBUG, f"{log_id}input dict keys {local_dict.keys()} and values {vals} with input key={key_of_add}, value={txt_to_add}")
        right_slots = {j + 1: local_dict[j] for j in range(key_of_add, len(local_dict.keys()))}
        left_slots = {j: local_dict[j] for j in range(0, key_of_add)}

        left_slots[key_of_add] = value_to_add
        if len(right_slots.keys()) > 0:
            left_slots.update(right_slots)
        if len(left_slots.keys()) > 0:
            local_dict.update(left_slots)

        vals = [x.active_track.common_name if isinstance(x, ActiveDeviceList) else x.common_name for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id}returning updated dict keys {local_dict.keys()} and values {vals}")
        return local_dict

    def __shift_keys_left(self, local_dict, key_before_del):
        log_id = "EAH.SD.__shift_keys_left: "
        key_to_remove = key_before_del + 1
        # local_dict is either an active_track reference mapped by track type index
        #     {callback_type_index=key_of_add: active_device_list=value_to_add}
        # or an active_device reference mapped by device index (active_device_list.devices)
        #     {device_index=key_of_add: active_device=value_to_add
        # "left slots" range is (0, key_to_remove) if any
        # "right slots" range is (key_to_remove + 1, len(local_dict.keys()) if any (and index shifted left)
        # delete 3 of 3 == range(2, 3), 2 "left slots", 0 "right slots"
        # delete 2 of 3 == range(1, 3), 1 "left slots", 1 "right_slots"
        # delete 1 of 3 == range(0, 3), 0 "left slots", 2 "right slots"
        # returned local_dict has 2 keys [0, 1], one less than before
        vals = [x.active_track.common_name if isinstance(x, ActiveDeviceList) else x.common_name for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id}input dict keys {local_dict.keys()} and values {vals}")
        # self.log_msg(logging.DEBUG, f"{log_id} with input key {key_before_del} means remove key {key_to_remove}")
        if key_before_del in local_dict.keys():
            if key_to_remove in local_dict.keys():
                right_slots = None
                if key_to_remove + 1 in local_dict.keys():
                    right_slots = {j - 1: local_dict[j] for j in range(key_to_remove + 1, len(local_dict.keys()))}
                left_slots = {j: local_dict[j] for j in range(0, key_to_remove)}

                if isinstance(local_dict[key_to_remove], ActiveDeviceList):
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

        vals = [x.active_track.track_name if isinstance(x, ActiveDeviceList) else x.common_name for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id} returning updated dict keys {local_dict.keys()} and values {vals}")
        return local_dict


class EncoderAssignmentHistory(MackieC4Component):
    """
     Keeps track of Song Track and Device content supporting SYSEX "LCD feedback message" generation and other script functions
    """
    __module__ = __name__

    def __init__(self, main_script, encoder_controller):
        MackieC4Component.__init__(self, main_script)

        self.data = SongData(logger=self.main_script().log_message, get_device_list=self.get_device_list)

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
    def track_count(self):
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
        return self.data.get_track(self.last_selected_track_index).selected_device_index

    @last_selected_device_index.setter
    def last_selected_device_index(self, device_index):
        self.data.get_track(self.last_selected_track_index).selected_device_index = device_index

    @property
    def selected_device_bank_count(self):
        return self.data.get_track(self.last_selected_track_index).device_bank_count

    @selected_device_bank_count.setter
    def selected_device_bank_count(self, selected_device_bank_count):
        self.data.get_track(self.last_selected_track_index).device_bank_count = selected_device_bank_count

    @property
    def selected_device_bank_index(self):
        return self.data.get_track(self.last_selected_track_index).device_bank_index_of_selected_device

    @property
    def max_device_count(self):
        return self.data.get_track(self.last_selected_track_index).device_count

    @max_device_count.setter
    def max_device_count(self, max_device_count):
        self.data.get_track(self.last_selected_track_index).device_count = max_device_count

    @property
    def max_last_selected_track_device_parameter_bank_nbr(self, t_d_idx=None):
        device_ref = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
        if device_ref is not None:
            return device_ref.required_parameter_banks
        else:
            return 0

    @property
    def last_selected_track_device_parameter_bank_nbr(self, t_d_idx=None):
        return self.last_selected_device_parameter_bank_view_index  # parameter_bank_index_of_selected_parameter
        
    @property
    def last_selected_track_device_bank_view_index(self):
        """ index of the selected track's current device-bank-view.  Which could differ from the device-bank of the track's selected device """
        rtn = 0
        if self.data.get_track(self.last_selected_track_index).track_device_bank_view_index is not None:
            rtn = self.data.get_track(self.last_selected_track_index).track_device_bank_view_index
        return rtn
    @last_selected_track_device_bank_view_index.setter
    def last_selected_track_device_bank_view_index(self, next_bank_view_index):
        self.data.get_track(self.last_selected_track_index).track_device_bank_view_index = next_bank_view_index
        
    @property
    def last_selected_device_parameter_bank_view_index(self):
        """ index of the selected device's current parameter-bank-view.  Which could differ from the parameter-bank of the device's selected (last changed) parameter """
        rtn = 0
        if self.last_selected_device_index is not None:
            d = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
            if d.device_parameter_bank_view_index is not None:
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
        track_ref = self.data.get_track(track_index)
        self.last_selected_track_index = track_index
        return track_ref.selected_device_index

    def unselected_tracks_changed(self, found_changed_track_callback_type, callback_type_track_count):
        # Not sure unselected "tracks" can actually just change in this respect.  Say master track is selected when "all return tracks"
        # change, and the change is not adding or removing tracks from view (folding/unfolding a group track for example)
        log_id = "EAH.unselected_tracks_changed: "
        type = track_callback_types[found_changed_track_callback_type]
        msg = f"{log_id}assumption issue? the count ({callback_type_track_count} of {type} track callback type {found_changed_track_callback_type} "
        self.main_script().log_message(logging.ERROR, msg + "tracks didn't change, but the tracks_changed() callback fired for some other reason")

    def tracks_added(self, song_track_index, song_tracks_after, callback_type):
        log_id = "EAH.tracks_added: "
        log_msg = f"{log_id}can't add master"
        final_callback_type_track_count = 1  # minimum == 1 master
        # self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        if callback_type == 0:
            final_callback_type_track_count = len(song_tracks_after) - self.data.return_track_count
            at_index = song_track_index
            while final_callback_type_track_count > self.data.plain_track_count:
                # self.main_script().log_message(logging.DEBUG, f"{log_id} adding at plains index: {at_index}")
                track_obj = song_tracks_after[at_index]
                d_list = self.get_device_list(track_obj.devices)
                self.track_added(at_index, track_obj, d_list)
                at_index = self.last_selected_track_index
                # self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: plain {self.data.plain_track_count}")
            assert final_callback_type_track_count == self.data.plain_track_count
            final_callback_type_track_count += self.data.return_track_count
        elif callback_type == 1:
            final_callback_type_track_count = len(song_tracks_after) - self.data.plain_track_count
            at_index = song_track_index
            while final_callback_type_track_count > self.data.return_track_count:
                # self.main_script().log_message(logging.DEBUG, f"{log_id} adding at returns index: {at_index}")
                track_obj = song_tracks_after[at_index]
                d_list = self.get_device_list(track_obj.devices)
                self.track_added(at_index, track_obj, d_list)
                at_index = self.last_selected_track_index
                # self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: return {self.data.return_track_count}")
            assert final_callback_type_track_count == self.data.return_track_count
            final_callback_type_track_count += self.data.plain_track_count

        self.main_script().log_message(logging.DEBUG, f"{log_id}AFTER: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        assert final_callback_type_track_count == self.data.total_track_count - 1  # not counting master here

    def unselected_tracks_added(self, found_changed_track_callback_type, callback_type_track_count):
        # unselected means we can't find the tracks that "came into view" in the list of tracks of this callback type
        # by the selected track index.  When tracks are added, no tracks are invalidated, we can search for the
        # index of the first liveobj_valid track not equal to the stored track reference at that callback type index,
        # add that track at that index, rinse and repeat. Imagine unfolding a group track using a mouse while master track is selected
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
            if track_obj == changed_track_type_table[at_index].active_track.track:
                # msg = f"{log_id}{t_type} tracks added, but cb type index {at_index} track_ref matches {track_obj.name}, no add"
                # self.main_script().log_message(logging.DEBUG, msg)
                pass
            else:
                msg = f"{log_id}{t_type} tracks added, and cb type index {at_index} track_ref doesn't equal {track_obj.name}, "
                extended_device_list = self.get_device_list(track_obj.devices)
                if found_changed_track_callback_type == 1:
                    self.main_script().log_message(logging.DEBUG, msg + f"adding unselected track at returns offset track index {rtns_offset + at_index}")
                    self.track_added(rtns_offset + at_index, track_obj, extended_device_list, is_selected=False)
                else:
                    self.main_script().log_message(logging.DEBUG, msg + f"adding unselected track at plains track index {at_index}")
                    self.track_added(at_index, track_obj, extended_device_list, is_selected=False)
            at_index += 1
            table_size = len(self.data.get_all_tracks_by_type_key(t_type))
        assert len(changed_track_type_table.keys()) == callback_type_track_count == table_size

    def track_added(self, song_track_index, track_obj=None, devices_on_selected_track=None, is_selected=True):

        if devices_on_selected_track is None:
            devices_on_selected_track = []

        rtn_idx = song_track_index - self.data.plain_track_count

        type_key = None
        if song_track_index < self.data.plain_track_count:
            type_key = self.data.table_keys[track_callback_types[0]]
            self.data.add_track(track_obj, type_key, song_track_index)
        elif rtn_idx < self.data.return_track_count:
            type_key = self.data.table_keys[track_callback_types[1]]
            self.data.add_track(track_obj, type_key, rtn_idx)
        # else can't add master

        if len(devices_on_selected_track) > 0:
            type_index = song_track_index
            if type_key > 0:
                type_index = rtn_idx
            for i, dev_obj in enumerate(devices_on_selected_track):
                self.data.add_device(song_track_index, type_index, i, dev_obj)

        if is_selected:
            self.last_selected_track_index = song_track_index
        else:
            if self.last_selected_track_index < self.data.plain_track_count + self.data.return_track_count:
                self.last_selected_track_index = self.last_selected_track_index + 1
            else:
                self.last_selected_track_index = self.master_track_index

    def tracks_deleted(self, song_track_index, tracks_to_process, callback_type):
        log_id = "EAH.tracks_deleted: "
        log_msg = f"{log_id}can't remove master"
        final_callback_type_track_count = 1 # minimum == 1 master
            
        # self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        if callback_type == 0:
            final_callback_type_track_count = len(tracks_to_process) - self.data.return_track_count
            at_index = song_track_index
            log_msg = f"{log_id}removing {self.data.plain_track_count - final_callback_type_track_count} plain tracks at index {at_index}"
            self.main_script().log_message(logging.DEBUG, log_msg)
            while final_callback_type_track_count < self.data.plain_track_count:
                # self.main_script().log_message(logging.DEBUG, f"{log_id} deleting at plains index: {at_index}")
                self.track_deleted(at_index)
                at_index = self.last_selected_track_index
                # self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: plains {self.data.plain_track_count}")
            final_callback_type_track_count += self.data.return_track_count
        elif callback_type == 1:
            # these tracks_to_process are ONLY the type 1 (return) tracks, not all the song tracks
            final_callback_type_track_count = len(tracks_to_process)
            at_rtns_index = song_track_index - self.data.plain_track_count
            log_msg = f"{log_id}removing {self.data.return_track_count - final_callback_type_track_count} return tracks at returns index {at_rtns_index}"
            self.main_script().log_message(logging.DEBUG, log_msg)
            while final_callback_type_track_count < self.data.return_track_count:
                # self.main_script().log_message(logging.DEBUG, f"{log_id} deleting at returns index: {at_rtns_index}")
                self.track_deleted(at_rtns_index)
                at_rtns_index = self.last_selected_track_index
                # self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: returns {self.data.return_track_count}")
            final_callback_type_track_count += self.data.plain_track_count

        # else:
        #     # can't remove master

        self.main_script().log_message(logging.DEBUG, f"{log_id}AFTER: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        assert final_callback_type_track_count == self.data.total_track_count - 1 # not counting master here

    def unselected_tracks_deleted(self, found_changed_track_callback_type, callback_type_track_count):
        # when tracks "disappear from view" the stored track references at the "deleted indexes" become not liveobj valid
        log_id = "EAH.unselected_tracks_deleted: "
        tracks_of_type = self.main_script().song().visible_tracks
        rtns_offset = len(tracks_of_type)
        t_type_key = track_callback_types[found_changed_track_callback_type]

        if found_changed_track_callback_type == 1:
            tracks_of_type = self.main_script().song().return_tracks
        assert len(tracks_of_type) == callback_type_track_count
        changed_track_type_table = self.data.get_all_tracks_by_type_key(t_type_key)
        at_index = 0
        tracks_of_type_index = 0
        table_size = len(changed_track_type_table.keys())
        self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")
        while len(changed_track_type_table.keys()) > callback_type_track_count and at_index < table_size:
            track_obj = None if not tracks_of_type_index < len(tracks_of_type) else tracks_of_type[tracks_of_type_index]
            track_ref = changed_track_type_table[at_index].active_track.track
            if liveobj_valid(track_ref):
                # msg = f"{log_id}{t_type_key} tracks deleted, and cb type index {at_index} track_ref is liveobj valid {track_ref.name}, "
                if track_obj is None or liveobj_changed(track_ref, track_obj):
                    # msg += f"but changed to {'None' if track_obj is None else track_obj.name} "
                    if found_changed_track_callback_type == 1:
                        # self.main_script().log_message(logging.DEBUG, msg + f"deleting track ref at returns offset track index {rtns_offset + at_index}")
                        index_before_deleted_track = 0 if rtns_offset + at_index < 1 else rtns_offset + at_index - 1
                        self.track_deleted(index_before_deleted_track, is_selected=False)
                    else:
                        # self.main_script().log_message(logging.DEBUG, msg + f"deleting track ref at plains track index {at_index}")
                        index_before_deleted_track = 0 if at_index < 1 else at_index - 1
                        self.track_deleted(index_before_deleted_track, is_selected=False)
                else:
                    # self.main_script().log_message(logging.DEBUG, msg + "no delete, incrementing")
                    at_index += 1
            else:
                # execution would land here if 2 or more unselected tracks were (not just removed from view but) deleted at the same time (not possible?)
                msg = f"{log_id}unselected {t_type_key} tracks deleted, but assumption issue? cb type index {at_index} track_ref is not liveobj valid "
                if found_changed_track_callback_type == 1:
                    self.main_script().log_message(logging.WARNING, msg + f"deleting track ref from returns offset track index {rtns_offset + at_index}")
                    index_before_deleted_track = 0 if rtns_offset + at_index < 1 else rtns_offset + at_index - 1
                    self.track_deleted(index_before_deleted_track, is_selected=False)
                else:
                    self.main_script().log_message(logging.WARNING, msg + f"deleting track ref from plains track index {at_index}")
                    index_before_deleted_track = 0 if at_index < 1 else at_index - 1
                    self.track_deleted(index_before_deleted_track, is_selected=False)
            tracks_of_type_index += 1
        table_size = len(self.data.get_all_tracks_by_type_key(t_type_key).keys())
        self.main_script().log_message(logging.DEBUG, f"{log_id}AFTER: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")
        assert len(changed_track_type_table.keys()) == callback_type_track_count == table_size

    def track_deleted(self, track_index, is_selected=True):
        log_id = "EAH.track_deleted: "
        # if self.last_selected_track_index != track_index:
        #     msg = f"{log_id} deleting track index {track_index} that is not last_selected_index {self.last_selected_track_index}"
        #     self.main_script().log_message(logging.DEBUG, msg)
        track_ref = self.data.get_track(track_index)
        # self.main_script().log_message(logging.DEBUG, f"{log_id}removing track_ref {track_ref.track_name} at index {track_index}")
        self.data.remove_track(track_index)
        if is_selected:
            self.last_selected_track_index = 0 if track_index < 1 else track_index - 1
        else:
            self.last_selected_track_index = 0 if self.last_selected_track_index < 1 else self.last_selected_track_index - 1
            # self.main_script().log_message(logging.DEBUG, f"{log_id}removed unselected track reference at song index {track_index}")
        # track_ref = self.data.get_track(self.last_selected_track_index)
        # self.main_script().log_message(logging.DEBUG, f"{log_id}selected track_ref is now {track_ref.track_name} at index {self.last_selected_track_index}")


    def device_added_deleted_or_changed(self, all_track_devices, selected_device, selected_device_idx):
        log_id = "EAH.device_added_deleted_or_changed: "
        new_device_count_track = len(all_track_devices)
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
        # if liveobj_valid(selected_device):
        #     self.main_script().log_message(logging.DEBUG, f"{log_id}input selected_device is a valid Live object named<{selected_device.name}>")
        # if selected_device_idx > -1:
        #     self.main_script().log_message(logging.DEBUG, f"{log_id}input selected_device_idx<{selected_device_idx}> points to a non-negative index")
        active_device_list_ref = self.data.get_active_device_list_at_song_index(self.last_selected_track_index)
        last_track_ref = active_device_list_ref.active_track
        # last_track_ref = self.data.get_track(self.last_selected_track_index)
        old_device_count_track = last_track_ref.device_count
        old_selected_device_index = last_track_ref.selected_device_index # could be None
        msg = f"{log_id}track index ref {last_track_ref.index} has name {last_track_ref.track_name} and old device count {old_device_count_track}"
        self.main_script().log_message(logging.DEBUG, msg)

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
        # last_track_ref.device_count = new_device_count_track  <--- device count updated automatically
        # last_track_ref.selected_device_index = new_device_index
        if not last_track_ref.device_count < new_device_count_track:
            self.main_script().log_message(logging.WARNING, f"{log_id}assumption issue: nothing added, what was updated?")
        else:
            # self.data.set_track(last_track_ref)
            self.data.add_device(last_track_ref.index, last_track_ref.index_by_type, new_device_index, new_device)
            # msg = f"{log_id}updated {last_track_ref.track_name}, device added {new_device.name} at index {new_device_index}, new device count is {last_track_ref.device_count}"
            # self.main_script().log_message(logging.DEBUG, msg)


    def update_device_counts_on_removal(self, deleted_device_index, rack_devices_deleted, found_input_device_index,
                                        old_device_count_track, new_device_count_track):
        log_id = "EAH.update_device_counts_on_removal: "
        # self.main_script().log_message(logging.DEBUG, f"{log_id}deletion index {deleted_device_index}")

        last_device_in_chain = deleted_device_index == old_device_count_track - 1  # 0 != -1 here
        empty_chain = old_device_count_track == 0 and not found_input_device_index
        
        last_track_ref = self.data.get_track(self.last_selected_track_index)
        # if last_device_in_chain or empty_chain:
        #     # only decrement "device count" if deleted device wasn't the only device
        #     if deleted_device_index > 0:
        #           last_track_ref.device_count -= rack_devices_deleted  # self.t_d_count[self.t_current] -= rack_devices_deleted
        #     else:
        #         last_track_ref.device_count = 0  # self.t_d_count[self.t_current] = 0
        # else: # device chain is not empty and "current device" isn't the only device
        #     last_track_ref.device_count -= rack_devices_deleted  # self.t_d_count[self.t_current] -= rack_devices_deleted
        #
        # assert new_device_count_track == last_track_ref.device_count  # self.t_d_count[self.t_current]  # self.t_d_count[self.t_current]
        # last_track_ref.selected_device_index = deleted_device_index  # self.t_d_current[self.t_current] = deleted_device_index
        # self.data.set_track(last_track_ref)
        # last_track_ref counts updated automatically by remove_device()
        self.data.remove_device(last_track_ref.index, deleted_device_index)
        # msg = f"{log_id}updated track {last_track_ref.track_name}, removed device at index {deleted_device_index} new device count is {last_track_ref.device_count}"
        # self.main_script().log_message(logging.DEBUG, msg)

        decremented_device_count_track = self.data.get_track(self.last_selected_track_index).device_count
        max_needed_device_banks = int(math.ceil(decremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
        if max_needed_device_banks != last_track_ref.required_device_banks:
            msg = f"{log_id}assumption issue: {max_needed_device_banks} calculated and required_device_banks {last_track_ref.required_device_banks} not matching"
            self.main_script().log_message(logging.ERROR, msg)


    def update_device_counts_on_change(self, all_track_devices, selected_device, old_selected_device_index, changed_device_index, new_device_count_track):
        log_id = "EAH.update_device_counts_on_change: "
        # self.main_script().log_message(logging.DEBUG, f"{log_id}")

        last_track_ref = self.data.get_track(self.last_selected_track_index)
        # can't assert this 'condition' because some drag&drop device movements fail to trigger this script's callbacks
        # (so the local database doesn't reflect the last selected index (or the new one) yet)
        # assert old_selected_device_index == self.last_selected_device_index

        last_selected_device_ref = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
        if old_selected_device_index != changed_device_index and not liveobj_changed(last_selected_device_ref.device, selected_device):
            msg = f"{log_id}selected device index of track {last_track_ref.track_name} changed from {last_track_ref.selected_device_index} to {changed_device_index} "
            self.main_script().log_message(logging.DEBUG, msg + f"but selected device remains {last_selected_device_ref.device_name}, moving device reference to new index")
            self.data.rekey_device_list_by_track_callback_type(track_callback_types[last_track_ref.type], last_track_ref.index_by_type, all_track_devices, selected_device)
        # msg = f"{log_id}selected device index of track {last_track_ref.track_name} changed from {last_track_ref.selected_device_index} to {changed_device_index}"
        # self.main_script().log_message(logging.DEBUG, msg)
        last_track_ref.selected_device_index = changed_device_index
        self.last_selected_device_index = changed_device_index
        assert new_device_count_track == last_track_ref.device_count
        self.data.set_track(last_track_ref)

