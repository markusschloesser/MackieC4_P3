
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
        self._selected_devices_bank_index = None if selected_device_index is None else selected_device_index % SETUP_DB_DEVICE_BANK_SIZE
        if selected_device_index is None or self.required_device_banks < 1:
            self._device_bank_index_of_selected_device = None
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
        """ the raw device index value % self.device_bank_count (0 unless a track has more than 8 devices) or None if no devices """
        return self._device_bank_index_of_selected_device

    @selected_device_index.setter
    def selected_device_index(self, selected_device_index):
        self._selected_device_index = selected_device_index
        self._selected_devices_bank_index = None if selected_device_index is None else selected_device_index % SETUP_DB_DEVICE_BANK_SIZE
        if selected_device_index is None or self.required_device_banks < 1:
            self._device_bank_index_of_selected_device = None
        else:
            self._device_bank_index_of_selected_device = selected_device_index % self.required_device_banks

class ActiveDevice:

    def __init__(self, dev_obj, dev_index=0, parameter_count=0, selected_parameter_index=0, song_track_index=0, callback_type_index=0):
        self.device = dev_obj
        self.index = dev_index
        self.track_index = song_track_index
        self.track_index_by_type = callback_type_index
        self._selected_parameter_index = selected_parameter_index
        self._parameter_count = parameter_count
        self._parameter_bank_count = math.ceil(parameter_count // SETUP_DB_PARAM_BANK_SIZE)
        self._selected_parameters_bank_index = selected_parameter_index % SETUP_DB_PARAM_BANK_SIZE
        if self.required_parameter_banks < 1:
            self._bank_index_of_selected_parameter = 0
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
    def device_name(self):
        nm = "None"
        if not liveobj_valid(self.device):
            nm = "Invalidobj"
        elif self.device.name is not None:
            nm = self.device.name
        return nm

    @property
    def parameter_count(self):
        return self._parameter_count
    @property
    def required_parameter_banks(self):
        return self._parameter_bank_count
    
    @parameter_count.setter
    def parameter_count(self, new_count):
        self._parameter_count = new_count
        self._parameter_bank_count = math.ceil(self._parameter_count // SETUP_DB_PARAM_BANK_SIZE)

    @property
    def selected_parameter_index(self):
        """ the raw parameter index value in parameter list """
        return self._selected_parameter_index
    @property
    def selected_parameters_bank_index(self):
        """ the raw parameter index value % SETUP_DB_PARAM_BANK_SIZE (0 - 23 by default) """
        return self._selected_parameters_bank_index
    @property
    def parameter_bank_index_of_selected_parameter(self):
        """ the raw parameter index value % self.parameter_bank_count (0 unless a device has more than 24 parameters) """
        return self._bank_index_of_selected_parameter

    @selected_parameter_index.setter
    def selected_parameter_index(self, selected_parameter_index):
        self._selected_parameter_index = selected_parameter_index
        self._selected_parameters_bank_index = 0 if selected_parameter_index is None else selected_parameter_index % SETUP_DB_PARAM_BANK_SIZE
        if selected_parameter_index is None or self.required_parameter_banks < 1:
            self._bank_index_of_selected_parameter = 0
        else:
            self._bank_index_of_selected_parameter = selected_parameter_index % self.required_parameter_banks

track_callback_types = {0: "plain", 1: "return", 2: "master"}

class SongData(object):
    # keys "plain", "return", and "master" are the "primary key column" in self.track_table and device_table
    # values 0, 1, and 2 are the track callback types used elsewhere in the script
    table_keys = {"plain": 0, "return": 1, "master": 2}

    @depends(logger=None)
    def __init__(self, logger=None):
        self.logger = logger
        self.__class_logging = False # True # False #
        self.track_table = {track_callback_types[0]: {},
                            track_callback_types[1]: {},
                            track_callback_types[2]: {}}
        self.device_table = {track_callback_types[0]: {},
                            track_callback_types[1]: {},
                            track_callback_types[2]: {}}
        
        self.__master_track_count = 1

    def log_msg(self, level, msg):
        if self.__class_logging:
            self.logger(level, msg)

    @property
    def plain_track_count(self):
        return int(len(self.track_table[track_callback_types[0]].keys()))

    @property
    def return_track_count(self):
        return int(len(self.track_table[track_callback_types[1]].keys()))

    @property
    def total_track_count(self):
        return self.plain_track_count + self. return_track_count + self.__master_track_count

    @property
    def master_track_index(self):
        tracks_before = self.plain_track_count + self. return_track_count
        # minimum example: 1 plain + 0 return == 1 track before master, master index is never less than 1 (second track, during init)
        rtn = tracks_before if tracks_before > 0 else 1
        return rtn

    def get_master_track(self, master_track_index=None):
        if master_track_index is None:
            master_track_index = self.master_track_index
        return self.get_track_by_type_key(track_callback_types[2], master_track_index)

    def init_master_track(self, track, song_index):
        self.clear_tracks_by_type_key(track_callback_types[2])
        nbr_devices = len(track.devices)
        selected_device_index = 0 if nbr_devices > 0 else None
        track_ref = ActiveTrack(track, self.table_keys[track_callback_types[2]], song_index, song_index, nbr_devices, selected_device_index)
        self.log_msg(logging.DEBUG, f"EAH.SD.init_master_track: BEFORE: master ref {track_ref} at index {song_index}")
        self.track_table[track_callback_types[2]][song_index] = track_ref
        track_ref = self.track_table[track_callback_types[2]][song_index]
        self.log_msg(logging.DEBUG, f"EAH.SD.init_master_track: AFTER: master ref {track_ref} at index {song_index}")
        # only use self._insert_track_slot() for non-master tracks (ordered lists with indexes from 0)

    def update_master_track_index(self, master_ref):
        if len(self.track_table[track_callback_types[2]]) > 0:
            self.clear_tracks_by_type_key(track_callback_types[2]) # remove master_ref with key == old master index
        master_ref.index = self.master_track_index
        master_ref.index_by_type = self.master_track_index
        # add master_ref back with new key == self.master_track_index
        self.track_table[track_callback_types[2]][self.master_track_index] = master_ref
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
        self.track_table[track_callback_type_key].clear()

    def clear_all_devices(self):
        self.clear_devices_by_track_type_key(track_callback_types[0])
        self.clear_devices_by_track_type_key(track_callback_types[1])
        self.clear_devices_by_track_type_key(track_callback_types[2])

    def clear_devices_by_track_type_key(self, track_callback_type_key):
        self.device_table[track_callback_type_key].clear()

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
            self.device_table[primary_key][track_type_index].clear()
        except KeyError:
            pass # no devices to clear
        if self.track_table[primary_key][track_type_index].device_count > 0:
            self.track_table[primary_key][track_type_index].device_count = 0
        if self.track_table[primary_key][track_type_index].selected_device_index is not None:
            self.track_table[primary_key][track_type_index].selected_device_index = None

    def get_track(self, song_track_index):
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
        return self.track_table[track_callback_type_key]

    # def set_all_tracks_by_type_key(self, track_callback_type_key, track_callback_type_dict):
    #     self.track_table[track_callback_type_key] = track_callback_type_dict

    def get_track_by_type_key(self, track_callback_type_key, track_index_by_type):
        return self.get_all_tracks_by_type_key(track_callback_type_key)[track_index_by_type]

    def set_track_by_type_key(self, track_callback_type_key, track_index_by_type, active_track):
        self.track_table[track_callback_type_key][track_index_by_type] = active_track

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

        msg = f"EAH.SD.set_track: done track_ref {active_track} at song track index {active_track.index} and callback type track index {active_track.index_by_type}"
        self.log_msg(logging.DEBUG, msg)
        self.log_msg(logging.DEBUG, f"EAH.SD.set_track: plain tracks {self.plain_track_count} return tracks {self.return_track_count}")

    def init_tracks(self, p_tracks, r_tracks, m_track):
        rtn = None
        if len(self.track_table[track_callback_types[0]]) > 0 or len(self.track_table[track_callback_types[1]]) > 0:
            # already initialized...  clear dicts, raise error, just log and return? (SongData can't reference self.main_script().log_message)
            rtn = "EAH.SD.init_tracks: assumption issue: track tables not already clear?"

        rtn_val = None
        if rtn is None:
            self.log_msg(logging.DEBUG, f"EAH.SD.init_tracks: initializing master track {m_track.name} at index {self.master_track_index}")
            self.init_master_track(m_track, self.master_track_index)
            new_master_track_ref = self.get_master_track()

            if new_master_track_ref is None:
                raise KeyError(f"EAH.SD.init_tracks: unable to retrieve initialized master track at index {self.master_track_index}")
            else:
                self.log_msg(logging.DEBUG, f"EAH.SD.init_tracks: master track after init: {new_master_track_ref}")

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
        last_master_track_ref = self.get_master_track(self.master_track_index)
        self.log_msg(logging.DEBUG, f"{log_id}master track before {track_callback_type_key} tracks initialized: {last_master_track_ref}")
        if len(self.track_table[track_callback_type_key]) > 0:
            rtn = f"{log_id}assumption issue: track table {track_callback_type_key} not already clear?"

        if rtn is None:
            track_type_index = 0
            track_count = len(tracks)
            song_index = 0
            if self.table_keys[track_callback_type_key] > 0:
                song_index = self.plain_track_count
            for track in tracks:
                nbr_devices = len(track.devices)
                selected_device_index = 0 if nbr_devices > 0 else None
                cumulative_song_index = song_index + track_type_index
                track_ref = ActiveTrack(track, self.table_keys[track_callback_type_key], cumulative_song_index, track_type_index, nbr_devices, selected_device_index)
                self._insert_track_slot(self.track_table[track_callback_type_key], track_type_index, track_ref)
                track_type_index += 1
            assert track_count == len(self.track_table[track_callback_type_key])
            if last_master_track_ref is not None:
                if last_master_track_ref.index < self.master_track_index:
                    self.log_msg(logging.DEBUG, f"{log_id}updating master track index to {self.master_track_index}")
                    self.update_master_track_index(last_master_track_ref)
                else:
                    self.log_msg(logging.DEBUG, f"{log_id}master track index is already {self.master_track_index}?")
            else:
                self.log_msg(logging.DEBUG, f"{log_id}master track ref was None, no update at index {self.master_track_index}?")

            self.log_msg(logging.DEBUG, f"{log_id}master track after {track_callback_type_key} tracks initialized: {last_master_track_ref}")

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
        last_master_track_ref = self.get_track(self.master_track_index)
        nbr_devices = len(track.devices)
        selected_index = 0 if nbr_devices > 0 else None
        track_ref = ActiveTrack(track, self.table_keys[track_callback_type_key], song_track_index, track_index_by_type, nbr_devices, selected_index)
        log_msg = f"EAH.SD.add_track_by_callback_type: inserting {track_callback_type_key} track {track_ref} at {track_callback_type_key} callback type index "
        log_msg += f"{track_index_by_type} and song tracks index {song_track_index}"
        self.log_msg(logging.DEBUG, log_msg)
        self.log_msg(logging.DEBUG, f"EAH.SD.add_track_by_callback_type: BEFORE: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        self._insert_track_slot(self.track_table[track_callback_type_key], track_index_by_type, track_ref)
        self.log_msg(logging.DEBUG, f"EAH.SD.add_track_by_callback_type: AFTER: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")

        if last_master_track_ref is not None and last_master_track_ref.index_by_type != self.master_track_index:
            self.update_master_track_index(last_master_track_ref)

    def add_track_devices_by_track_callback_type(self, track_callback_type_key, song_track_index, track_index_by_type, track):
        self.add_device_list(song_track_index, 0, track.devices)

    def remove_track(self, song_track_index):
        rtns_index = song_track_index - self.plain_track_count
        log_msg = f"EAH.SD.remove_track: at song track index {song_track_index}"
        self.log_msg(logging.DEBUG, log_msg)
        if song_track_index < self.plain_track_count:
            self.remove_track_by_callback_type(track_callback_types[0], song_track_index)
            self.remove_track_devices_by_callback_type(track_callback_types[0], song_track_index)
        elif rtns_index < self.return_track_count:
            self.remove_track_by_callback_type(track_callback_types[1], rtns_index)
            self.remove_track_devices_by_callback_type(track_callback_types[1], rtns_index)
        else:
            raise RuntimeError(f"can't remove track at OOB index {song_track_index}, can't remove master_track {self.master_track_index} or after")

    def remove_track_by_callback_type(self, track_callback_type_key, track_index_by_type):
        log_id = "EAH.SD.remove_track_by_callback_type: "
        last_master_track_ref = self.get_track(self.master_track_index)
        old = self.track_table[track_callback_type_key][track_index_by_type]
        if old.track_name == "Invalidobj":
            log_msg = f"{log_id}collapsing slot holding invalid liveobj "
        else:
            log_msg = f"{log_id}collapsing slot holding a valid liveobj {old.track_name} "

        self.log_msg(logging.DEBUG, log_msg)
        log_msg = f"{log_id}{track_callback_type_key} track at {track_callback_type_key} callback type index {track_index_by_type}: {old} "
        self.log_msg(logging.DEBUG, log_msg)
        self.log_msg(logging.DEBUG, f"{log_id}BEFORE: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        self._collapse_track_slot(self.track_table[track_callback_type_key], track_index_by_type)
        new_count = len(self.track_table[track_callback_type_key])
        self.log_msg(logging.DEBUG, f"{log_id}AFTER: new track count={new_count}")
        self.log_msg(logging.DEBUG, f"{log_id}AFTER: plain tracks {self.plain_track_count}, return tracks {self.return_track_count}")
        if last_master_track_ref is not None and last_master_track_ref.index_by_type != self.master_track_index:
            self.update_master_track_index(last_master_track_ref)

    def remove_track_devices_by_callback_type(self, track_callback_type_key, track_index_by_type):
        log_msg = f"EAH.SD.remove_track_devices_by_callback_type: collapsing slot holding {track_callback_type_key} track device list "
        log_msg += f"at {track_callback_type_key} callback type index {track_index_by_type}"
        self.log_msg(logging.DEBUG, log_msg)
        self._collapse_track_slot(self.device_table[track_callback_type_key], track_index_by_type)


    def get_track_device_map(self, song_track_index):
        device_map = None
        rtns_index = song_track_index - self.plain_track_count
        log_msg = f"EAH.SD.get_track_device_map: at song track index "
        try:
            if song_track_index < self.plain_track_count:
                self.log_msg(logging.DEBUG, log_msg + song_track_index)
                device_map = self.get_track_device_map_by_callback_type(track_callback_types[0], song_track_index)
            elif rtns_index < self.return_track_count:
                self.log_msg(logging.DEBUG, log_msg + rtns_index)
                device_map =  self.get_track_device_map_by_callback_type(track_callback_types[1], rtns_index)
            elif song_track_index == self.plain_track_count + self.return_track_count:
                self.log_msg(logging.DEBUG, log_msg + song_track_index)
                device_map = self.get_track_device_map_by_callback_type(track_callback_types[0], song_track_index)
        except KeyError:
            pass # track has no devices

        return device_map

    def get_track_device_map_by_callback_type(self, track_callback_type_key, track_index_by_type):
        log_id = "EAH.SD.get_track_device_map_by_callback_type: "
        self.log_msg(logging.DEBUG, f"{log_id}returning device map from {track_callback_type_key} track index {track_index_by_type}")
        return self.device_table[track_callback_type_key][track_index_by_type]

    def get_device(self, song_track_index, device_index):
        rtn = None
        device_map = self.get_track_device_map(song_track_index)
        if device_map and device_index < len(device_map.keys()):
            rtn = device_map[device_index]
            rtn.index = device_index
            rtn.track_index = song_track_index
            if self.plain_track_count <= song_track_index < self.return_track_count:
                rtn.track_index_by_type = song_track_index - self.plain_track_count
            else:
                rtn.track_index_by_type = song_track_index # plain or master track index by type

        # self.log_msg(logging.DEBUG, f"EAH.SD.get_device: returning device_ref from song index {song_track_index} and d_index {device_index}")
        # self.log_msg(logging.DEBUG, f"EAH.SD.get_device: {rtn}")
        return rtn

    def set_device(self, active_device):
        device_map = self.get_track_device_map(active_device.track_index)
        self.log_msg(logging.DEBUG, f"EAH.SD.set_device: got device list from device's song track index {active_device.track_index}")
        if device_map and active_device.index < len(device_map.keys()):
            old = device_map[active_device.index]
            # self.log_msg(logging.DEBUG, f"EAH.SD.set_device: setting device <{active_device}> in device list at device index {active_device.index}")
            # self.log_msg(logging.DEBUG, f"EAH.SD.set_device: overwriting device <{old}> previously stored at index {active_device.index}")
            device_map[active_device.index] = active_device
        else:
            raise RuntimeError("can't set a device not already in the device map")

    def add_device_list(self, track_index, device_index, device_list):
        rtns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            self.add_device_list_by_track_callback_type(track_callback_types[0], track_index, device_index, device_list)
        elif rtns_index < self.return_track_count:
            self.add_device_list_by_track_callback_type(track_callback_types[1], rtns_index, device_index, device_list)
        elif track_index == self.plain_track_count + self.return_track_count:
            self.add_device_list_by_track_callback_type(track_callback_types[2], track_index, device_index, device_list)

    def add_device_list_by_track_callback_type(self, callback_type_key, callback_type_index, from_device_index, device_list):
        song_index = callback_type_index
        if callback_type_key == track_callback_types[1]:
            song_index = self.plain_track_count + callback_type_index
        if len(device_list) > 0:
            for i, device in enumerate(device_list):
                self.add_device(song_index, callback_type_index, from_device_index + i, device)
        else:
            self.device_table[callback_type_key][song_index] = {}

    def init_device(self, song_track_index, track_callback_type_index, device_index, device_obj):
        selected_parameter_index = 0 if len(device_obj.parameters) > 0 else None  # devices always have at least 1 parameter
        rtns_index = song_track_index - self.plain_track_count

        if song_track_index < self.plain_track_count:
            device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, song_track_index, track_callback_type_index)
            self.init_device_by_track_callback_type(track_callback_types[0], song_track_index, device_index, device_ref)
        elif rtns_index < self.return_track_count:
            device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, rtns_index, track_callback_type_index)
            self.init_device_by_track_callback_type(track_callback_types[1], rtns_index, device_index, device_ref)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, song_track_index, track_callback_type_index)
            self.init_device_by_track_callback_type(track_callback_types[2], song_track_index, device_index, device_ref)

    def init_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index, device_ref):
        self._insert_device_slot(self.device_table[track_callback_type_key], callback_type_index, device_index, device_ref)

    def add_device(self, song_track_index, track_callback_type_index, device_index, device_obj):
        selected_parameter_index = 0 if len(device_obj.parameters) > 0 else None  # devices always have at least 1 parameter
        device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, song_track_index, track_callback_type_index)
        rtns_index = song_track_index - self.plain_track_count
        log_msg = f"EAH.SD.add_device: adding device ref {device_ref} at "
        if song_track_index < self.plain_track_count:
            self.log_msg(logging.DEBUG, log_msg + f"song index {song_track_index} and callback type index {song_track_index}")
            self.add_device_by_track_callback_type(track_callback_types[0], song_track_index, device_index, device_ref)
        elif rtns_index < self.return_track_count:
            self.log_msg(logging.DEBUG, log_msg + f"song index {song_track_index} and callback type index {rtns_index}")
            self.add_device_by_track_callback_type(track_callback_types[1], rtns_index, device_index, device_ref)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            self.log_msg(logging.DEBUG, log_msg + f"song index {song_track_index} and callback type index {song_track_index}")
            self.add_device_by_track_callback_type(track_callback_types[2], song_track_index, device_index, device_ref)
        else:
            raise RuntimeError(f"can't add device at OOB track index {song_track_index}, max track index is master_track {self.master_track_index}")

    def add_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index, device_ref):
        log_msg = f"EAH.SD.add_device_by_track_callback_type: adding device to {track_callback_type_key} track at callback index {callback_type_index} and "
        self.log_msg(logging.DEBUG, log_msg + f"device list index {device_index}")
        self._insert_device_slot(self.device_table[track_callback_type_key], callback_type_index, device_index, device_ref)
        old_count = self.track_table[track_callback_type_key][callback_type_index].device_count
        log_msg = f"EAH.SD.add_device_by_track_callback_type: incrementing device count and setting selected device index values on associated {track_callback_type_key} "
        self.log_msg(logging.DEBUG, log_msg + f"track at callback type index {callback_type_index} to {old_count + 1} devices and selected index {device_index}")
        self.track_table[track_callback_type_key][callback_type_index].device_count += 1
        self.track_table[track_callback_type_key][callback_type_index].selected_device_index = device_index

    def clear_device_list(self, track_index):
        """ defers to: self.clear_track_devices(track_index) """
        self.clear_track_devices(track_index)

        rtns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            new_device_count = self.track_table[track_callback_types[0]][track_index].device_count
        elif rtns_index < self.return_track_count:
            new_device_count = self.track_table[track_callback_types[1]][rtns_index].device_count
        elif track_index == self.plain_track_count + self.return_track_count:
            new_device_count = self.track_table[track_callback_types[2]][track_index].device_count
        else:
            raise RuntimeError(f"can't clear device list at OOB track index {track_index}, max track index is master_track {self.master_track_index}")
        device_map_len = len(self.get_track_device_map(track_index))
        assert new_device_count == 0 == device_map_len

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
        log_msg = f"EAH.SD.remove_device: at song track index {song_track_index} "
        self.log_msg(logging.DEBUG, log_msg)
        if song_track_index < self.plain_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[0], song_track_index, device_index)
        elif rtns_index < self.return_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[1], rtns_index, device_index)
        elif song_track_index == self.plain_track_count + self.return_track_count:
            self.remove_device_by_track_callback_type(track_callback_types[2], song_track_index, device_index)
        else:
            raise RuntimeError(f"can't remove device at OOB track index {song_track_index}, max track index is master_track {self.master_track_index}")

    def remove_device_by_track_callback_type(self, track_callback_type_key, callback_type_index, device_index):
        log_id = "EAH.SD.remove_device_by_track_callback_type: "
        log_msg = f"{log_id}collapsing device at index {device_index} at {track_callback_type_key} "
        device_map = self.device_table[track_callback_type_key]
        self.log_msg(logging.DEBUG, log_msg + f"track callback index {callback_type_index}")
        self.log_msg(logging.DEBUG, f"{log_id}BEFORE: device count {len(device_map)}")
        self._collapse_device_slot(device_map, callback_type_index, device_index)
        self.log_msg(logging.DEBUG, f"{log_id}AFTER: device count {len(device_map)}")
        self.device_table[track_callback_type_key] = device_map
        track_ref = self.track_table[track_callback_type_key][callback_type_index]
        self.log_msg(logging.DEBUG, f"{log_id}after device removal BEFORE updating track ref {track_ref}")
        self._update_track_table_after_device_removal(track_ref, device_index)
        self.log_msg(logging.DEBUG, f"{log_id}after device removal AFTER updating track ref {track_ref}")

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

    def _insert_track_slot(self, type_dict, track_callback_type_index, track_ref):
        return self.__shift_keys_right(type_dict, track_callback_type_index, track_ref)

    def _insert_device_slot(self, type_dict, track_callback_type_index, device_index, device_ref):
        if track_callback_type_index in type_dict.keys():
            device_map = type_dict[track_callback_type_index]
            type_dict = self.__shift_keys_right(device_map, device_index, device_ref)
        else:
            type_dict[track_callback_type_index] = {device_index: device_ref}
        return type_dict

    def _collapse_track_slot(self, type_dict, track_callback_type_index):
        return self.__shift_keys_left(type_dict, track_callback_type_index)

    def _collapse_device_track_slot(self, type_dict, track_callback_type_index):
        return self.__shift_keys_left(type_dict, track_callback_type_index)


    def _collapse_device_slot(self, type_dict, track_callback_type_index, device_index):
        if track_callback_type_index in type_dict.keys():
            device_map = type_dict[track_callback_type_index]
            type_dict[track_callback_type_index] = self.__shift_keys_left(device_map, device_index)
            return type_dict
        else:
            return None

    def __shift_keys_right(self, local_dict, key, value):
        log_id = "EAH.SD.__shift_keys_right: "
        self.log_msg(logging.DEBUG, f"{log_id} input dict keys {local_dict.keys()} and key, value {key}, {value}")
        if key in local_dict.keys():
            right_slots = {j + 1: local_dict[j] for j in range(key, len(local_dict.keys()))}
            self.log_msg(logging.DEBUG, f"{log_id} right slots {right_slots.keys()} from range({key}, {len(local_dict.keys())})")
            local_dict[key] = value
            local_dict.update(right_slots)
            self.log_msg(logging.DEBUG, f"{log_id} insert-into-key-sequence dict keys {local_dict.keys()}")
        else:
            local_dict[key] = value
            self.log_msg(logging.DEBUG, f"{log_id} append-to-key-sequence dict keys {local_dict.keys()}")

        vals = ["device list" if isinstance(x, dict) else x.to_string() for x in local_dict.values()]
        self.log_msg(logging.DEBUG, f"{log_id} returning updated dict keys {local_dict.keys()} and values {vals}")
        return local_dict

    def __shift_keys_left(self, local_dict, key):
        log_id = "EAH.SD.__shift_keys_left: "
        self.log_msg(logging.DEBUG, f"{log_id} input dict keys {local_dict.keys()} and key {key}")
        if key in local_dict.keys():
            # delete 3 of 3 == range(2, 2), 0 "right slots"
            # delete 2 of 3 == range(1, 2), 1 "right_slots" starting at key 
            # delete 1 of 3 == range(0, 2), 2 "right_slots" starting at key
            right_slots = {j: local_dict[j + 1] for j in range(key, len(local_dict.keys()) - 1)}
            self.log_msg(logging.DEBUG, f"{log_id} right slots {right_slots.keys()} from input range({key + 1}, {len(local_dict.keys())})")
            del local_dict[key]
            left_slots = {k: local_dict[k] for k in local_dict.keys() if k < key}

            self.log_msg(logging.DEBUG, f"{log_id} left slots {left_slots.keys()} with key < {key})")
            self.log_msg(logging.DEBUG, f"{log_id} deleted dict keys {local_dict.keys()}")
            local_dict.clear()
            if len(right_slots.keys()) > 0:
                left_slots.update(right_slots)
            if len(left_slots.keys()) > 0:
                local_dict.update(left_slots)
            vals = ["device list" if isinstance(x, dict) else x.to_string() for x in local_dict.values()]
            self.log_msg(logging.DEBUG, f"{log_id} returning updated dict keys {local_dict.keys()} and values {vals}")
        return local_dict


class EncoderAssignmentHistory(MackieC4Component):
    """
     Keeps track of Song Track and Device content supporting SYSEX "LCD feedback message" generation and other script functions
    """
    __module__ = __name__

    def __init__(self, main_script, encoder_controller):
        MackieC4Component.__init__(self, main_script)

        self.data = SongData(logger=self.main_script().log_message)

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

    # track table device_bank_index value automatically updated when selected_device_index changes
    # @selected_device_bank_index.setter 
    # def selected_device_bank_index(self, selected_device_bank_index):
    #     self.data.get_track(self.last_selected_track_index).device_bank_index = selected_device_bank_index

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

    # @max_last_selected_track_device_parameter_bank_nbr.setter <--- automatically set when device added
    # def max_last_selected_track_device_parameter_bank_nbr(self, updated_bank_nbr):
    #     device_ref = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
    #     if device_ref is not None:
    #         device_ref.required_parameter_banks = updated_bank_nbr

    @property
    def last_selected_track_device_parameter_bank_nbr(self, t_d_idx=None):
        device_ref = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
        if device_ref is not None:
            return device_ref.parameter_bank_index_of_selected_parameter
        else:
            return 0

    # @last_selected_track_device_parameter_bank_nbr.setter <--- automatically set when selected device parameter cahnges
    # def last_selected_track_device_parameter_bank_nbr(self, last_selected_bank_nbr):
    #     device_ref = self.data.get_device(self.last_selected_track_index, self.last_selected_device_index)
    #     if device_ref is not None:
    #         device_ref.parameter_bank_index = last_selected_bank_nbr


    def update_device_counter(self, track_index, device_count):
        log_id = "EAH.update_device_counter: "
        max_device_banks = math.ceil(device_count // SETUP_DB_DEVICE_BANK_SIZE)
        self.data.get_track(track_index).device_bank_count = max_device_banks
        if self.last_selected_track_index != track_index:
            msg = f"{log_id}track index {track_index} for device count update didn't match last selected track index {self.last_selected_track_index}, updating"
            self.main_script().log_message(logging.DEBUG, msg)
            self.track_changed(track_index)

    def build_setup_database(self, song_ref=None):
        if song_ref is None:
            song_ref = self.song()

        self.data.clear_all_tracks()
        self.data.clear_all_devices()

        # tracks first
        error_msg = self.data.init_tracks(song_ref.visible_tracks, song_ref.return_tracks, song_ref.master_track)
        if error_msg is not None:
            self.main_script().log_message(logging.ERROR, error_msg)

        # then devices

        for i, track in enumerate(song_ref.visible_tracks):
            self.data.add_device_list(i, 0, track.devices)
        #     for j, device in enumerate(track.devices):
        #         self.data.init_device(i, i, j, device)
        plain_count = len(song_ref.visible_tracks)
        for i, track in enumerate(song_ref.return_tracks):
            self.data.add_device_list(plain_count + i, 0, track.devices)
            # for j, device in enumerate(track.devices):
            #     self.data.init_device(plain_count + i, i, j, device)

        self.data.add_device_list(self.data.master_track_index, 0, song_ref.master_track.devices)
        # for j, device in enumerate(song_ref.master_track.devices):
        #     self.data.init_device(self.data.master_track_index, self.data.master_track_index, j, device)

    def rebuild_database_on_tracks_change(self, song_ref=None):
        if song_ref is None:
            song_ref = self.song()

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
        self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        if callback_type == 0:
            final_callback_type_track_count = len(song_tracks_after) - self.data.return_track_count
            at_index = song_track_index
            while final_callback_type_track_count > self.data.plain_track_count:
                self.main_script().log_message(logging.DEBUG, f"{log_id} adding at plains index: {at_index}")
                track_obj = song_tracks_after[at_index]
                self.track_added(at_index, track_obj, track_obj.devices)
                at_index = self.last_selected_track_index
                self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: plain {self.data.plain_track_count}")
            assert final_callback_type_track_count == self.data.plain_track_count
            final_callback_type_track_count += self.data.return_track_count
        elif callback_type == 1:
            final_callback_type_track_count = len(song_tracks_after) - self.data.plain_track_count
            at_index = song_track_index
            while final_callback_type_track_count > self.data.return_track_count:
                self.main_script().log_message(logging.DEBUG, f"{log_id} adding at returns index: {at_index}")
                track_obj = song_tracks_after[at_index]
                self.track_added(at_index, track_obj, track_obj.devices)
                at_index = self.last_selected_track_index
                self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: return {self.data.return_track_count}")
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
        self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")
        while len(changed_track_type_table.keys()) < callback_type_track_count and at_index < len(tracks_of_type):
            track_obj = tracks_of_type[at_index]
            if track_obj == changed_track_type_table[at_index].track:
                self.main_script().log_message(logging.DEBUG, f"{log_id}{t_type} tracks added, but cb type index {at_index} track_ref matches {track_obj.name}, no add")
            else:
                msg = f"{log_id}{t_type} tracks added, and cb type index {at_index} track_ref doesn't equal {track_obj.name}, "
                if found_changed_track_callback_type == 1:
                    self.main_script().log_message(logging.DEBUG, msg + f"adding track at returns offset track index {rtns_offset + at_index}")
                    self.track_added(rtns_offset + at_index, track_obj, track_obj.devices, is_selected=False)
                else:
                    self.main_script().log_message(logging.DEBUG, msg + f"adding track at plains track index {at_index}")
                    self.track_added(at_index, track_obj, track_obj.devices, is_selected=False)
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
                self.last_selected_track_index = self.data.plain_track_count + self.data.return_track_count

    def tracks_deleted(self, song_track_index, tracks_to_process, callback_type):
        log_id = "EAH.tracks_deleted: "
        log_msg = f"{log_id}can't remove master"
        final_callback_type_track_count = 1 # minimum == 1 master
            
        self.main_script().log_message(logging.DEBUG, f"{log_id}BEFORE: plains {self.data.plain_track_count}, returns {self.data.return_track_count}")
        if callback_type == 0:
            final_callback_type_track_count = len(tracks_to_process) - self.data.return_track_count
            at_index = song_track_index
            log_msg = f"{log_id}removing {self.data.plain_track_count - final_callback_type_track_count} plain tracks from index {at_index}"
            self.main_script().log_message(logging.DEBUG, log_msg)
            while final_callback_type_track_count < self.data.plain_track_count:
                self.main_script().log_message(logging.DEBUG, f"{log_id} deleting at plains index: {at_index}")
                self.track_deleted(at_index)
                at_index = self.last_selected_track_index
                self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: plains {self.data.plain_track_count}")
            final_callback_type_track_count += self.data.return_track_count
        elif callback_type == 1:
            # these tracks_to_process are ONLY the type 1 (return) tracks, not all the song tracks
            final_callback_type_track_count = len(tracks_to_process)
            at_rtns_index = song_track_index - self.data.plain_track_count
            log_msg = f"{log_id}removing {self.data.return_track_count - final_callback_type_track_count} return tracks from returns index {at_rtns_index}"
            self.main_script().log_message(logging.DEBUG, log_msg)
            while final_callback_type_track_count < self.data.return_track_count:
                self.main_script().log_message(logging.DEBUG, f"{log_id} deleting at returns index: {at_rtns_index}")
                self.track_deleted(at_rtns_index)
                at_rtns_index = self.last_selected_track_index
                self.main_script().log_message(logging.DEBUG, f"{log_id}DURING: returns {self.data.return_track_count}")
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
            track_obj = tracks_of_type[tracks_of_type_index]
            track_ref = changed_track_type_table[at_index].track
            if liveobj_valid(track_ref):
                msg = f"{log_id}{t_type_key} tracks deleted, and cb type index {at_index} track_ref is liveobj valid {track_ref.name}, "
                if  liveobj_changed(track_ref, track_obj):
                    msg += f"but changed to {track_obj.name} "
                    if found_changed_track_callback_type == 1:
                        self.main_script().log_message(logging.DEBUG, msg + f"deleting track ref from returns offset track index {rtns_offset + at_index}")
                        self.track_deleted(rtns_offset + at_index, is_selected=False)
                    else:
                        self.main_script().log_message(logging.DEBUG, msg + f"deleting track ref from plains track index {at_index}")
                        self.track_deleted(at_index, is_selected=False)
                else:
                    self.main_script().log_message(logging.DEBUG, msg + "no delete")
                    at_index += 1
            else:
                msg = f"{log_id}{t_type_key} tracks deleted, but cb type index {at_index} track_ref is not liveobj valid "
                if found_changed_track_callback_type == 1:
                    self.main_script().log_message(logging.DEBUG, msg + f"deleting track ref from returns offset track index {rtns_offset + at_index}")
                    self.track_deleted(rtns_offset + at_index, is_selected=False)
                else:
                    self.main_script().log_message(logging.DEBUG, msg + f"deleting track ref from plains track index {at_index}")
                    self.track_deleted(at_index, is_selected=False)
            tracks_of_type_index += 1
        table_size = len(self.data.get_all_tracks_by_type_key(t_type_key).keys())
        self.main_script().log_message(logging.DEBUG, f"{log_id}AFTER: cbtt_count={callback_type_track_count}, db_cbtt_keys={table_size}")
        assert len(changed_track_type_table.keys()) == callback_type_track_count == table_size

    def track_deleted(self, track_index, is_selected=True):
        log_id = "EAH.track_deleted: "
        if self.last_selected_track_index != track_index:
            msg = f"{log_id} deleting track index {track_index} that is not last_selected_index {self.last_selected_track_index}"
            self.main_script().log_message(logging.DEBUG, msg)
        track_ref = self.data.get_track(track_index)
        self.main_script().log_message(logging.DEBUG, f"{log_id}removing track_ref {track_ref.track_name} at index {track_index}")
        self.data.remove_track(track_index)
        if is_selected:
            self.last_selected_track_index = 0 if track_index < 1 else track_index - 1
        else:
            self.last_selected_track_index = 0 if self.last_selected_track_index < 1 else self.last_selected_track_index - 1
            self.main_script().log_message(logging.DEBUG, f"{log_id}removed unselected track reference at song index {track_index}")
        track_ref = self.data.get_track(self.last_selected_track_index)
        self.main_script().log_message(logging.DEBUG, f"{log_id}selected track_ref is now {track_ref.track_name} at index {self.last_selected_track_index}")


    def device_added_deleted_or_changed(self, all_devices, selected_device, selected_device_idx):
        log_id = "EAH.device_added_deleted_or_changed: "
        new_device_count_track = len(all_devices)
        idx = 0
        log_msg = f"{log_id}device in input device list at index<{idx}> is "
        for device in all_devices:
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
        last_track_ref = self.data.get_track(self.last_selected_track_index)
        old_device_count_track = last_track_ref.device_count # self.t_d_count[self.t_current]
        old_selected_device_index = last_track_ref.selected_device_index # self.t_d_current[self.t_current]
        msg = f"{log_id}track index ref {last_track_ref.index} has name {last_track_ref.track_name} and old device count {old_device_count_track}"
        self.main_script().log_message(logging.DEBUG, msg)

        device_was_added = new_device_count_track > old_device_count_track
        device_was_removed = new_device_count_track < old_device_count_track
        selected_device_was_changed = new_device_count_track > 0 and new_device_count_track == old_device_count_track
        no_devices_on_track = new_device_count_track == 0
        rack_devices_deleted = old_device_count_track - new_device_count_track if device_was_removed else 0

        log_msg = f"{log_id}input selected_device_idx<{selected_device_idx}> and input device list len<{new_device_count_track}> "
        if selected_device_idx is None or selected_device_idx == -1:
            self.main_script().log_message(logging.DEBUG, f"{log_msg}agree that no devices currently populate the device chain for this track")
            assert no_devices_on_track
        else:
            self.main_script().log_message(logging.DEBUG, f"{log_msg}allow modification of the device chain for this track")

        new_device_index = 0
        deleted_device_index = 0
        changed_device_index = 0
        rtn_device_index = -1
        found_input_device_index = False  # selected_device is in all_devices

        # if there are no devices on track, there are no devices in input all_devices list and this loop is not entered,
        # all "change indexes" stay 0. If a device was deleted, selected_device will be at the index before the deleted device
        for index,device in enumerate(all_devices):
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
            self.update_device_counts_on_addition(new_device_index, all_devices, old_device_count_track, new_device_count_track)

        elif device_was_removed:
            self.update_device_counts_on_removal(deleted_device_index, rack_devices_deleted, found_input_device_index,
                                                 old_device_count_track, new_device_count_track)

        elif selected_device_was_changed:
            self.update_device_counts_on_change(changed_device_index, new_device_count_track)

        return rtn_device_index

    def update_device_counts_on_addition(self, new_device_index, all_devices, old_device_count_track, new_device_count_track):
        log_id = f"EAH.update_device_counts_on_addition: "
        new_device = all_devices[new_device_index]
        last_track_ref = self.data.get_track(self.last_selected_track_index)
        # last_track_ref.device_count = new_device_count_track  <--- device count updated automatically
        # last_track_ref.selected_device_index = new_device_index
        if not last_track_ref.device_count < new_device_count_track:
            self.main_script().log_message(logging.DEBUG, f"{log_id}assumption issue: nothing added, what was updated?")
        else:
            # self.data.set_track(last_track_ref)
            self.data.add_device(last_track_ref.index, new_device_index, new_device)
            msg = f"{log_id}updated {last_track_ref.track_name}, device added {new_device.name} at index {new_device_index}, new device count is {last_track_ref.device_count}"
            self.main_script().log_message(logging.DEBUG, msg)


    def update_device_counts_on_removal(self, deleted_device_index, rack_devices_deleted, found_input_device_index,
                                        old_device_count_track, new_device_count_track):
        log_id = "EAH.update_device_counts_on_removal: "
        self.main_script().log_message(logging.DEBUG, f"{log_id}deletion index {deleted_device_index}")

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
        self.data.set_track(last_track_ref)
        self.data.remove_device(last_track_ref.index, deleted_device_index)
        msg = f"{log_id}updated track {last_track_ref.track_name}, removed device at index {deleted_device_index} new device count is {last_track_ref.device_count}"
        self.main_script().log_message(logging.DEBUG, msg)

        decremented_device_count_track = self.data.get_track(self.last_selected_track_index).device_count
        max_needed_device_banks = int(math.ceil(decremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
        if max_needed_device_banks != last_track_ref.required_device_banks:
            msg = f"{log_id}assumption issue: {max_needed_device_banks} calculated and required_device_banks {last_track_ref.required_device_banks} not matching"
            self.main_script().log_message(logging.ERROR, msg)


    def update_device_counts_on_change(self, changed_device_index, new_device_count_track):
        log_id = "EAH.update_device_counts_on_change: "
        self.main_script().log_message(logging.DEBUG, f"{log_id}")

        last_track_ref = self.data.get_track(self.last_selected_track_index)
        msg = f"{log_id}selected device index of track {last_track_ref.track_name} changed from {last_track_ref.selected_device_index} to {changed_device_index}"
        self.main_script().log_message(logging.DEBUG, msg)
        last_track_ref.selected_device_index = changed_device_index
        assert new_device_count_track == last_track_ref.device_count
        self.data.set_track(last_track_ref)


#    def __init__(self, main_script, encoderController):
#        MackieC4Component.__init__(self, main_script)
#
#        self.__my_controlling_encoder = encoderController
#         self.__master_track_index = 0
#         self.t_count = 0
#         """number of regular tracks"""
#
#         self.t_r_count = 0
#         """number of return tracks"""
#
#        self.t_current = 0
#        """index of current selected track"""
#
#         self.t_d_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
#         """current track device count"""
#
#        self.t_d_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
#        """track device current -- the index of the currently selected device indexed by the t_current track"""
#
#         self.t_d_bank_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
#         """count of the devices on the t_current track (in banks of 8 parameters), see device_counter(self, t, d):
#         (at the same index) the same number as t_d_current but divided by 8"""
#
#         self.t_d_bank_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
#         """index of currently selected device indexed by the t_current track (in banks of 8 parameters) the same index as t_d_current divided by 8"""
#
#         self.t_d_p_count = [[0 for i in range(SETUP_DB_DEFAULT_SIZE)] for j in range(SETUP_DB_DEFAULT_SIZE)]
#         """count of remote controllable parameters available for the currently selected device on the t_current track"""
#
#         self.t_d_p_bank_count = [[0 for i in range(SETUP_DB_DEFAULT_SIZE)] for j in range(SETUP_DB_DEFAULT_SIZE)]
#         """count of remote controllable parameters available for the currently selected device on the t_current track (in banks of 24 params)
#         [at the same index, the same number as t_d_p_count but divided by 8]"""
#
#         self.t_d_p_bank_current = [[0 for i in range(SETUP_DB_DEFAULT_SIZE)] for j in range(SETUP_DB_DEFAULT_SIZE)]
#         """index of the selected remote controllable parameter of the currently selected device on the t_current track (in banks of 24 params)"""
#
#    def update_device_counter(self, t, d):
#         self.t_d_count[t] = d
#         max_device_banks = math.ceil(d // SETUP_DB_DEVICE_BANK_SIZE)
#         self.t_d_bank_count[t] = int(max_device_banks)
#
#    def master_track_index(self):
#         return self.__master_track_index
#
#    def build_setup_database(self, song_ref=None):
#        if song_ref is None:
#            song_ref = self.song()
#
#         self.t_count = 0
#         # self.main_script().log_message(logging.DEBUG, f"EAH.build_setup_database: t_current idx <{self.t_current}> t_count <{self.t_count}> BEFORE setup_db")
#
#         # tracks_in_song = self.song().tracks
#         tracks_in_song = self.song().visible_tracks + self.song().return_tracks  # same way as everywhere else, right?
#
#         # self.main_script().log_message(logging.DEBUG, "EAH.build_setup_database: nbr tracks in song {0}".format(len(tracks_in_song)))
#         loop_index_tracker = 0
#         for t_idx in range(len(tracks_in_song)):
#             devices_on_track = tracks_in_song[t_idx].devices
#             self.t_d_count[t_idx] = len(devices_on_track)
#             max_device_banks = math.ceil(len(devices_on_track) // SETUP_DB_DEVICE_BANK_SIZE)
#             self.t_d_bank_count[t_idx] = int(max_device_banks)
#             self.t_d_bank_current[t_idx] = 0
#             self.t_d_current[t_idx] = 0
#             for d_idx in range(len(devices_on_track)):
#                 params_of_devices_on_trk = devices_on_track[d_idx].parameters
#                 self.t_d_p_count[t_idx][d_idx] = len(params_of_devices_on_trk)
#                 max_param_banks = math.ceil(len(params_of_devices_on_trk) // SETUP_DB_PARAM_BANK_SIZE)
#                 self.t_d_p_bank_count[t_idx][d_idx] = int(max_param_banks)
#                 self.t_d_p_bank_current[t_idx][d_idx] = 0
#
#             self.t_count += 1
#             loop_index_tracker = t_idx
#
#         idx_nrml_trks = loop_index_tracker
#         assert idx_nrml_trks == self.t_count - 1
#         for rt_idx in range(len(self.song().return_tracks)):
#             devices_on_rtn_track = self.song().return_tracks[rt_idx].devices
#         # for rt_idx in range(len(song_ref.return_tracks)):
#         #     devices_on_rtn_track = song_ref.return_tracks[rt_idx].devices
#             ttl_t_idx = idx_nrml_trks + rt_idx + 1
#             self.t_d_count[ttl_t_idx] = len(devices_on_rtn_track)
#             max_device_banks = math.ceil(len(devices_on_rtn_track) // SETUP_DB_DEVICE_BANK_SIZE)
#             self.t_d_bank_count[ttl_t_idx] = int(max_device_banks)
#             self.t_d_bank_current[ttl_t_idx] = 0
#             self.t_d_current[ttl_t_idx] = 0
#             for rt_d_idx in range(len(devices_on_rtn_track)):
#                 params_of_devices_on_rtn_trk = devices_on_rtn_track[rt_d_idx].parameters
#                 self.t_d_p_count[ttl_t_idx][rt_d_idx] = len(params_of_devices_on_rtn_trk)
#                 max_param_banks = math.ceil(len(params_of_devices_on_rtn_trk) // SETUP_DB_PARAM_BANK_SIZE)
#                 self.t_d_p_bank_count[ttl_t_idx][rt_d_idx] = int(max_param_banks)
#                 self.t_d_p_bank_current[ttl_t_idx][rt_d_idx] = 0
#
#             self.t_count += 1
#             self.t_r_count += 1
#             loop_index_tracker = ttl_t_idx
#
#         idx_nrml_and_rtn_trks = loop_index_tracker
#         assert idx_nrml_and_rtn_trks == self.t_count - 1
#         self.__master_track_index = idx_nrml_and_rtn_trks + 1
#         mt_idx = self.__master_track_index
#         assert mt_idx == self.t_count  # the master track index == the number of tracks and returns
#         devices_on_mstr_track = self.get_device_list(self.song().master_track.devices)
#
#         self.t_d_count[mt_idx] = len(devices_on_mstr_track)
#         max_device_banks = math.ceil(len(devices_on_mstr_track) // SETUP_DB_DEVICE_BANK_SIZE)
#         self.t_d_bank_count[mt_idx] = int(max_device_banks)
#         self.t_d_bank_current[mt_idx] = 0
#         self.t_d_current[mt_idx] = 0
#         for mt_d_idx in range(len(devices_on_mstr_track)):
#             params_of_devices_on_mstr_trk = devices_on_mstr_track[mt_d_idx].parameters
#             self.t_d_p_count[mt_idx][mt_d_idx] = len(params_of_devices_on_mstr_trk)
#             max_param_banks = math.ceil(len(params_of_devices_on_mstr_trk) // SETUP_DB_PARAM_BANK_SIZE)
#             self.t_d_p_bank_count[mt_idx][mt_d_idx] = int(max_param_banks)
#             self.t_d_p_bank_current[mt_idx][mt_d_idx] = 0
#
#         # self.main_script().log_message(logging.DEBUG, "t_current idx <{0}> t_count <{1}> AFTER setup_db".format(self.t_current, self.t_count))
#
#    def track_changed(self, track_index):
#        """expecting track_index to be the new track index, return value is -1 or the index of the selected device at that new track index """
#         rtn = -1
#         # self.main_script().log_message(logging.DEBUG, "t_current idx <{0}> t_count <{1}> BEFORE track change".format(self.t_current, self.t_count))
#         self.t_current = track_index
#         # self.main_script().log_message(logging.DEBUG, "t_current idx <{0}> t_count <{1}> AFTER track change".format(self.t_current, self.t_count))
#         if self.t_current == self.t_count:
#             assert self.t_current == self.__master_track_index
#             # self.main_script().log_message(logging.DEBUG, "This is the index of the master Track")
#         if len(self.t_d_current) > self.t_current:
#             rtn = self.t_d_current[self.t_current]
#         elif len(self.t_d_current) > 0:
#             rtn = 0
#         else:
#             # something isn't getting updated correctly at startup and/or when devices are deleted
#             self.main_script().log_message(logging.ERROR, "len(self.t_d_current) <= self.t_current")
#             self.main_script().log_message(logging.ERROR, "{0} <= {1}".format(len(self.t_d_current), self.t_current))
#
#         return rtn
#
#    def tracks_added(self, track_index, tracks):
#         new_t_count = len(tracks)
#         at_index = track_index
#         while new_t_count > self.t_count:
#             self.track_added(at_index)
#             at_index = self.t_current # if self.t_current > 0 else 0
#
#    def track_added(self, track_index, devices_on_selected_track=None):
#         if devices_on_selected_track is None:
#             devices_on_selected_track = []
#
#         start = self.t_count + 1
#         stop = track_index - 1
#         track_index_range = range(start, stop, -1)
#         # There is always a "selected track" if a new track is inserted in Live and the new track is (or tracks are) inserted
#         # to the right of the selected track, so there should always be t's in track_index_range to loop over
#         #
#         # this only works as long as everything still fits inside 128 indexes, SETUP_DB_DEFAULT_SIZE
#         # i.e. (regular_tracks + return_tracks + master_track) must be >= 0 AND <= 128
#         # similarly the number of devices on any one track must be >= 0 AND <= 128
#         # similarly the number of remote-controllable parameters on any one device must be >= 0 AND <= 128
#         for t in track_index_range:
#             for d in range(self.t_d_count[t]):
#
#                 # shift values up one index to make room for new track data
#                 self.t_d_p_count[(t + 1)][d] = self.t_d_p_count[t][d]
#                 self.t_d_p_bank_count[(t + 1)][d] = self.t_d_p_bank_count[t][d]
#                 self.t_d_p_bank_current[(t + 1)][d] = self.t_d_p_bank_current[t][d]
#
#             # insert new values in freshly opened index
#             self.t_d_count[t + 1] = self.t_d_count[t]
#
#             self.t_d_current[t + 1] = self.t_d_current[t]
#             self.t_d_bank_count[t + 1] = self.t_d_bank_count[t]
#             self.t_d_bank_current[t + 1] = self.t_d_bank_current[t]
#
#         self.t_current = track_index
#
#         self.t_count += 1
#         self.__master_track_index = self.t_count  # master track is "one past" the end of regular + return tracks
#
#         self.t_d_count[track_index] = len(devices_on_selected_track)
#         self.t_d_current[track_index] = 0
#         self.t_d_bank_count[track_index] = int(math.ceil(len(devices_on_selected_track) // SETUP_DB_DEVICE_BANK_SIZE))
#         self.t_d_bank_current[track_index] = 0
#         for d in range(len(devices_on_selected_track)):
#             parms_of_devs_on_trk = devices_on_selected_track[d].parameters
#             self.t_d_p_count[track_index][d] = len(parms_of_devs_on_trk)
#             self.t_d_p_bank_count[track_index][d] = int(math.ceil(len(parms_of_devs_on_trk) // SETUP_DB_PARAM_BANK_SIZE))
#             self.t_d_p_bank_current[track_index][d] = 0
#
#    def tracks_deleted(self, track_index, tracks):
#         new_t_count = len(tracks)
#         at_index = track_index
#         while new_t_count < self.t_count:
#             self.track_deleted(at_index)
#             at_index = self.t_current # if self.t_current > 0 else 0
#
#     def track_deleted(self, track_index):
#
#         for t in range(self.t_current + 1, self.t_count, 1):
#
#             for d in range(self.t_d_count[t]):
#                 self.t_d_p_count[(t - 1)][d] = self.t_d_p_count[t][d]
#                 self.t_d_p_bank_count[(t - 1)][d] = self.t_d_p_bank_count[t][d]
#                 self.t_d_p_bank_current[(t - 1)][d] = self.t_d_p_bank_current[t][d]
#
#             self.t_d_count[t - 1] = self.t_d_count[t]
#             self.t_d_current[t - 1] = self.t_d_current[t]
#             self.t_d_bank_count[t - 1] = self.t_d_bank_count[t]
#             self.t_d_bank_current[t - 1] = self.t_d_bank_current[t]
#
#         self.t_count -= 1
#         self.__master_track_index = self.t_count  # master track is "one past" the end of regular + return tracks
#         self.t_current = track_index
#
#     def update_device_counts_on_addition(self, new_device_index, all_devices, old_device_count_track, new_device_count_track):
#         # self.main_script().log_message(logging.DEBUG, f"EAH.update_device_counts_on_addition: ")
#         param_count_track = self.t_d_p_count[self.t_current]
#         param_bank_count_track = self.t_d_p_bank_count[self.t_current]
#         param_bank_current_track = self.t_d_p_bank_current[self.t_current]
#         for d in range(old_device_count_track, new_device_index + 1, -1):
#             c = d - 1
#             param_count_track[d] = param_count_track[c]
#             param_bank_count_track[d] = param_bank_count_track[c]
#             param_bank_current_track[d] = param_bank_current_track[c]
#
#         param_count_track[new_device_index] = len(all_devices[new_device_index].parameters)
#         max_param_banks = math.ceil(param_count_track[new_device_index] // SETUP_DB_PARAM_BANK_SIZE)
#         param_bank_count_track[new_device_index] = max_param_banks
#         param_bank_current_track[new_device_index] = 0
#
#         self.t_d_count[self.t_current] = new_device_count_track
#         incremented_device_count_track = self.t_d_count[self.t_current]
#
#         self.t_d_current[self.t_current] = new_device_index
#         max_needed_device_banks = int(math.ceil(incremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
#         if SETUP_DB_MAX_DEVICE_BANKS >= max_needed_device_banks:
#             self.t_d_bank_count[self.t_current] = max_needed_device_banks
#         else:
#             # self.main_script().log_message(logging.DEBUG, "{0}because we don't need no stinking badges".format(log_id))
#             self.t_d_bank_count[self.t_current] = 1
#
#     def update_device_counts_on_removal(self, deleted_device_index, rack_devices_deleted, found_input_device_index,
#                                         old_device_count_track, new_device_count_track):
#         # self.main_script().log_message(logging.DEBUG, "{0}device_was_removed: for 'delete' device event handling".format(log_id))
#
#         param_count_track = self.t_d_p_count[self.t_current]
#         param_bank_count_track = self.t_d_p_bank_count[self.t_current]
#         param_bank_current_track = self.t_d_p_bank_current[self.t_current]
#         # self.main_script().log_message(logging.DEBUG, "{0}device_was_removed: deleted_device_index<{1}> old_device_count_track<{2}>".format(log_id, deleted_device_index, old_device_count_track))
#
#         for d in range(deleted_device_index + 1, old_device_count_track, 1):
#             c = d - 1
#             param_count_track[d] = param_count_track[c]
#             param_bank_count_track[d] = param_bank_count_track[c]
#             param_bank_current_track[d] = param_bank_current_track[c]
#
#         # "only" device in device chain is also "last" device in device chain
#         last_device_in_chain = deleted_device_index == old_device_count_track - 1  # 0 != -1 here
#         empty_chain = old_device_count_track == 0 and not found_input_device_index
#         if last_device_in_chain or empty_chain:
#             # only decrement "device count" if deleted device wasn't the only device
#             if deleted_device_index > 0:
#                 self.t_d_count[self.t_current] -= rack_devices_deleted
#             else:
#                 self.t_d_count[self.t_current] = 0
#         else:
#             # device chain is not empty and "current device" isn't the only device
#             self.t_d_count[self.t_current] -= rack_devices_deleted
#
#         assert new_device_count_track == self.t_d_count[self.t_current]
#         decremented_device_count_track = self.t_d_count[self.t_current]
#         self.t_d_current[self.t_current] = deleted_device_index
#         max_needed_device_banks = int(math.ceil(decremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
#         if SETUP_DB_MAX_DEVICE_BANKS > max_needed_device_banks:
#             self.t_d_bank_count[self.t_current] = max_needed_device_banks
#         else:
#             self.t_d_bank_count[self.t_current] = SETUP_DB_MAX_DEVICE_BANKS
#
#     def update_device_counts_on_change(self, changed_device_index, new_device_count_track):
#         # self.main_script().log_message(logging.DEBUG, "{0}selected_device_was_changed: for 'change' device event handling".format(log_id))
#
#         self.t_d_current[self.t_current] = changed_device_index
#         assert new_device_count_track == self.t_d_count[self.t_current]
#
#     def device_added_deleted_or_changed(self, all_devices, selected_device, selected_device_idx):
#         log_id = "EAH.device_added_deleted_or_changed: "
#         new_device_count_track = len(all_devices)
#         # self.main_script().log_message(logging.DEBUG, "{0}input device list len<{1}>".format(log_id, new_device_count_track))
#         idx = 0
#         log_msg = "{0}device in input device list at index<{1}> is ".format(log_id, idx)
#         for device in all_devices:
#             if liveobj_valid(device):
#                 pass  # self.main_script().log_message(logging.DEBUG, "{0}a valid Live object named <{1}>".format(log_msg, device.name))
#             else:
#                 self.main_script().log_message("{0}<None> or a lost weakref".format(log_msg))
#             idx += 1
#             log_msg = "{0}device in input device list at index<{1}> is ".format(log_id, idx)
#
#         # if liveobj_valid(selected_device):
#         #     self.main_script().log_message(logging.DEBUG, "{0}input selected_device is a valid Live object named<{1}>".format(log_id, selected_device.name))
#         # if selected_device_idx > -1:
#         #     self.main_script().log_message(logging.DEBUG, "{0}input selected_device_idx<{1}> points to a forward index".format(log_id, selected_device_idx))
#
#         old_device_count_track = self.t_d_count[self.t_current]
#         old_selected_device_index = self.t_d_current[self.t_current]
#
#         device_was_added = new_device_count_track > old_device_count_track
#         device_was_removed = new_device_count_track < old_device_count_track
#         selected_device_was_changed = new_device_count_track == old_device_count_track
#         no_devices_on_track = new_device_count_track == 0
#
#         rack_devices_deleted = old_device_count_track - new_device_count_track if device_was_removed else 0
#
#         log_msg = "{0}input selected_device_idx<{1}> and input device list len<{2}> ".format(log_id, selected_device_idx,new_device_count_track)
#         if selected_device_idx == -1:
#             # self.main_script().log_message(logging.DEBUG, "{0}agree that no devices currently populate the device chain for this track".format(log_msg))
#             assert no_devices_on_track  # == True
#
#         index = 0
#         new_device_index = 0
#         deleted_device_index = 0
#         changed_device_index = 0
#         rtn_device_index = -1
#         found_input_device_index = False  # selected_device is in all_devices
#
#         # if there are no devices on track, there are no devices in input all_devices list and this loop is not entered,
#         # all "change indexes" stay 0. If a device was deleted, selected_device will be at the index before the deleted device
#         for index,device in enumerate(all_devices):
#             if selected_device == device:
#                 new_device_index = index
#                 deleted_device_index = index
#                 changed_device_index = index
#                 rtn_device_index = index
#                 found_input_device_index = True
#                 # self.main_script().log_message(logging.DEBUG, "{0}matched input selected_device<{1}> with device<{2}> at index<{3}> of input device list".format(log_id, selected_device.name, device.name, index))
#                 break
#
#         cb = self.t_d_bank_current[self.t_current]
#         if found_input_device_index:
#             new_track_device_bank_index = int(math.floor(selected_device_idx / SETUP_DB_DEVICE_BANK_SIZE))
#             new_device_bank_bank_index = selected_device_idx % SETUP_DB_DEVICE_BANK_SIZE
#
#             log_msg = "{0}old_track_device_bank_index <{1}> ".format(log_id, cb)
#             if selected_device_idx >= SETUP_DB_DEVICE_BANK_SIZE and new_device_bank_bank_index == 0:
#                 # new index is an exact bank size match
#
#                 self.t_d_bank_current[self.t_current] = new_track_device_bank_index
#                 cb = self.t_d_bank_current[self.t_current]
#                 # self.main_script().log_message(logging.DEBUG, "{0}updated to <{1}> because exact boundary".format(log_msg, cb))
#             else:
#                 log_msg = "{0}new_track_device_bank_index <{1}> ".format(log_id, cb)
#                 self.t_d_bank_current[self.t_current] = new_track_device_bank_index
#                 cb = self.t_d_bank_current[self.t_current]
#                 # self.main_script().log_message(logging.DEBUG, "{0}updated to <{1}> because not boundary".format(log_msg, cb))
#         else:
#             log_msg = "{0}new_track_device_bank_index <{1}> ".format(log_id, cb)
#             self.t_d_bank_current[self.t_current] = 0  # reset to default?
#             cb = self.t_d_bank_current[self.t_current]
#             # self.main_script().log_message(logging.DEBUG, "{0}updated to <{1}> because else".format(log_msg, cb))
#
#         # FROM HERE: "found event index <{0}> and device <{1}>".format(index, device.name) represent "source of truth"
#         # device == self.selected_track.devices[index]  and we could return rtn_device_index right here, except for updating the "assignment history" database
#
#         if device_was_added:
#             self.update_device_counts_on_addition(new_device_index, all_devices, old_device_count_track,new_device_count_track)
#
#         elif device_was_removed:
#             self.update_device_counts_on_removal(deleted_device_index, rack_devices_deleted, found_input_device_index,
#                                                  old_device_count_track,new_device_count_track)
#
#         elif selected_device_was_changed:
#             self.update_device_counts_on_change(changed_device_index, new_device_count_track)
#
#         return rtn_device_index
#
#     def get_current_track_device_parameter_bank_nbr(self, t_d_idx=None):
#         if t_d_idx is None:
#             t_d_idx = self.t_d_current[self.t_current]
#
#         return self.t_d_p_bank_current[self.t_current][t_d_idx]
#
#     def set_current_track_device_parameter_bank_nbr(self, current_bank_nbr):
#         self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]] = current_bank_nbr
#
#     def get_max_current_track_device_parameter_bank_nbr(self, t_d_idx=None):
#         if t_d_idx is None:
#             t_d_idx = self.t_d_current[self.t_current]
#
#         return self.t_d_p_bank_count[self.t_current][t_d_idx]
#
#     def set_max_current_track_device_parameter_bank_nbr(self, updated_bank_nbr):
#         self.t_d_p_bank_count[self.t_current][self.t_d_current[self.t_current]] = updated_bank_nbr
#
#     def get_selected_device_index(self):
#         selected_device_index = -1
#         if len(self.t_d_current) > self.t_current:
#             selected_device_index = self.t_d_current[self.t_current]
#         elif len(self.t_d_current) > 0:
#             selected_device_index = 0
#         return selected_device_index
#
#     def set_selected_device_index(self, selected_device_index):
#         self.t_d_current[self.t_current] = selected_device_index
#
#     def get_max_device_count(self):
#         max_device_count = -1
#         if len(self.t_d_count) > self.t_current:
#             max_device_count = self.t_d_count[self.t_current]
#         elif len(self.t_d_count) > 0:
#             max_device_count = 0
#         return max_device_count
#
#     def set_max_device_count(self, max_device_count):
#         self.t_d_count[self.t_current] = max_device_count
#
#     def get_selected_device_bank_index(self):
#         selected_device_bank_index = -1
#         if len(self.t_d_bank_current) > self.t_current:
#             selected_device_bank_index = self.t_d_bank_current[self.t_current]
#         elif len(self.t_d_bank_current) > 0:
#             selected_device_bank_index = 0
#         return selected_device_bank_index
#
#     def set_selected_device_bank_index(self, selected_device_bank_index):
#         self.t_d_bank_current[self.t_current] = selected_device_bank_index
#
#     def get_selected_device_bank_count(self):
#         selected_device_bank_count = -1
#         if len(self.t_d_bank_count) > self.t_current:
#             selected_device_bank_count = self.t_d_bank_count[self.t_current]
#         elif len(self.t_d_bank_count) > 0:
#             selected_device_bank_count = 0
#         return selected_device_bank_count
#
#     def set_selected_device_bank_count(self, selected_device_bank_count):
#         self.t_d_bank_count[self.t_current] = selected_device_bank_count
#
