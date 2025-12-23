
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
import sys

from ableton.v2.base import liveobj_valid

if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

from . MackieC4Component import *

import math
import logging

class ActiveTrack:

    def __init__(self, track_obj, track_type=0, track_index=0, device_count=0, selected_device_index=None):

        self.track = track_obj
        self.type = track_type
        self.index = track_index
        self._device_count = device_count
        self._device_bank_count = int(math.ceil(device_count // SETUP_DB_DEVICE_BANK_SIZE))
        self._selected_device_index = selected_device_index
        self._selected_devices_bank_index = None if selected_device_index is None else selected_device_index % SETUP_DB_DEVICE_BANK_SIZE
        if selected_device_index is None or self.required_device_banks < 1:
            self._device_bank_index_of_selected_device = None
        else:
            self._device_bank_index_of_selected_device = int(math.floor(selected_device_index % self.required_device_banks))
        
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

    def __init__(self, dev_obj, dev_index=0, parameter_count=0, selected_parameter_index=0, track_index=0):
        self.device = dev_obj
        self.index = dev_index
        self.track_index = track_index
        self._selected_parameter_index = selected_parameter_index
        self._parameter_count = parameter_count
        self._parameter_bank_count = math.ceil(parameter_count // SETUP_DB_PARAM_BANK_SIZE)
        self._selected_parameters_bank_index = selected_parameter_index % SETUP_DB_PARAM_BANK_SIZE
        if self.required_parameter_banks < 1:
            self._bank_index_of_selected_parameter = 0
        else:
            self._bank_index_of_selected_parameter = int(math.floor(selected_parameter_index % self.required_parameter_banks))

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

    def __init__(self):
        self.track_table = {track_callback_types[0]: {},
                            track_callback_types[1]: {},
                            track_callback_types[2]: {}}
        self.device_table = {track_callback_types[0]: {},
                            track_callback_types[1]: {},
                            track_callback_types[2]: {}}
        
        self.__master_track_count = 1

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

    def clear_tracks(self):
        self.track_table[track_callback_types[0]].clear()
        self.track_table[track_callback_types[1]].clear()
        self.track_table[track_callback_types[2]].clear()

    def clear_devices(self):
        self.device_table[track_callback_types[0]].clear()
        self.device_table[track_callback_types[1]].clear()
        self.device_table[track_callback_types[2]].clear()

    def get_track(self, track_index):
        rtns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            return self.track_table[track_callback_types[0]][track_index]
        elif rtns_index < self.return_track_count:
            return self.track_table[track_callback_types[1]][rtns_index]
        elif track_index == self.plain_track_count + self.return_track_count:
            return self.track_table[track_callback_types[2]][track_index]
        else:
            return None

    def set_track(self, active_track):
        rtns_index = active_track.index - self.plain_track_count
        if active_track.index < self.plain_track_count:
            self.track_table[track_callback_types[0]][active_track.index] = active_track
        elif rtns_index < self.return_track_count:
            self.track_table[track_callback_types[1]][rtns_index] = active_track
        elif active_track.index == self.plain_track_count + self.return_track_count:
            self.track_table[track_callback_types[2]][active_track.index] = active_track
        else:
            raise RuntimeError("can't set a track not already in the track table")

    def init_tracks(self, p_tracks, r_tracks, m_track):
        rtn = None
        if len(self.track_table[track_callback_types[0]]) > 0 or len(self.track_table[track_callback_types[1]]) > 0:
            # already initialized...  clear dicts, raise error, just log and return? (SongData can't reference self.main_script().log_message)
            rtn = "EAH.SD.init_tracks: assumption issue: track tables not already clear?"
        
        if rtn is None:
            track_type_index = 0
            p_track_count = len(p_tracks)
            r_track_count = len(r_tracks)
            for track in p_tracks:
                nbr_devices = len(track.devices)
                selected_device_index = 0 if nbr_devices > 0 else None
                track_ref = ActiveTrack(track, self.table_keys["plain"], track_type_index, nbr_devices, selected_device_index)
                self._insert_track_slot(self.track_table[track_callback_types[0]], track_type_index, track_ref)
                track_type_index += 1
    
            track_type_index = 0
            for track in r_tracks:
                nbr_devices = len(track.devices)
                selected_device_index = 0 if nbr_devices > 0 else None
                track_ref = ActiveTrack(track, self.table_keys["return"], track_type_index, nbr_devices, selected_device_index)
                self._insert_track_slot(self.track_table[track_callback_types[1]], track_type_index, track_ref)
                track_type_index += 1
    
            assert p_track_count == len(self.track_table[track_callback_types[0]])
            assert r_track_count == len(self.track_table[track_callback_types[1]])
            master_index = p_track_count + r_track_count
            nbr_devices = len(m_track.devices)
            selected_device_index = 0 if nbr_devices > 0 else None
            track_ref = ActiveTrack(m_track, self.table_keys["master"], master_index, nbr_devices, selected_device_index)
            self._insert_track_slot(self.track_table[track_callback_types[2]], master_index, track_ref)
            
        return rtn 

    def add_track(self, track, track_type, track_index):
        nbr_devices = len(track.devices)
        selected_index = 0 if nbr_devices > 0 else None
        track_ref = ActiveTrack(track, track_type, track_index, nbr_devices, selected_index)
        returns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            self._insert_track_slot(self.track_table[track_callback_types[0]], track_index, track_ref)
        elif returns_index < self.return_track_count:
            self._insert_track_slot(self.track_table[track_callback_types[1]], returns_index, track_ref)
        elif track_index == self.plain_track_count + self.return_track_count:
            # self._insert_track_slot(self.track_table[track_callback_types[2]], track_index, track_ref)  
            raise RuntimeError(f"can't add or remove master track at index {track_index}")
        else:
            raise RuntimeError(f"can't add track at OOB index {track_index}, max new index is less than {self.master_track_index}")

    def remove_track(self, track_index):
        if track_index < self.plain_track_count:
            self._collapse_track_slot(self.track_table[track_callback_types[0]], track_index)
        elif track_index - self.plain_track_count < self.return_track_count:
            self._collapse_track_slot(self.track_table[track_callback_types[1]], track_index)
        else:
            raise RuntimeError(f"can't remove track at OOB index {track_index}, can't remove master_track {self.master_track_index} or after")

    def get_device_map(self, track_index):
        device_map = None
        rtns_index = track_index - self.plain_track_count
        try:
            if track_index < self.plain_track_count:
                device_map = self.device_table[track_callback_types[0]][track_index]
            elif rtns_index < self.return_track_count:
                device_map =  self.device_table[track_callback_types[1]][rtns_index]
            elif track_index == self.plain_track_count + self.return_track_count:
                device_map = self.device_table[track_callback_types[2]][track_index]
        except KeyError:
            pass # track has no devices

        return device_map

    def get_device(self, track_index, device_index):
        rtn = None
        device_map = self.get_device_map(track_index)
        if device_map and device_index < len(device_map.keys()):
            rtn = device_map[device_index]

        return rtn

    def set_device(self, active_device):
        device_map = self.get_device_map(active_device.track_index)
        if device_map and active_device.index < len(device_map.keys()):
            device_map[active_device.index] = active_device
        else:
            raise RuntimeError("can't set a device not already in the device map")

    def add_device_list(self, track_index, device_index, device_list):
        for i, device in enumerate(device_list):
            self.add_device(track_index, device_index + i, device)

    def init_device(self, track_index, track_type, device_index, device_obj):
        selected_parameter_index = 0 if len(device_obj.parameters) > 0 else None  # devices always have at least 1 parameter
        device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, track_index)
        rtns_index = track_index - self.plain_track_count
        if self.table_keys["plain"] == track_type:
            self._insert_device_slot(self.device_table[track_callback_types[0]], track_index, device_index, device_ref)
            # self.track_table[track_callback_types[0]][track_index] data already initialized
        elif self.table_keys["return"] == track_type:
            self._insert_device_slot(self.device_table[track_callback_types[1]], rtns_index, device_index, device_ref)
        elif self.table_keys["master"] == track_type:
            self._insert_device_slot(self.device_table[track_callback_types[2]], track_index, device_index, device_ref)

    def add_device(self, track_index, device_index, device_obj):
        selected_parameter_index = 0 if len(device_obj.parameters) > 0 else None  # devices always have at least 1 parameter
        device_ref = ActiveDevice(device_obj, device_index, len(device_obj.parameters), selected_parameter_index, track_index)
        rtns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            self._insert_device_slot(self.device_table[track_callback_types[0]], track_index, device_index, device_ref)
            self.track_table[track_callback_types[0]][track_index].device_count += 1
            self.track_table[track_callback_types[0]][track_index].selected_device_index = device_index
        elif rtns_index < self.return_track_count:
            self._insert_device_slot(self.device_table[track_callback_types[1]], rtns_index, device_index, device_ref)
            self.track_table[track_callback_types[1]][rtns_index].device_count += 1
            self.track_table[track_callback_types[1]][rtns_index].selected_device_index = device_index
        elif track_index == self.plain_track_count + self.return_track_count:
            self._insert_device_slot(self.device_table[track_callback_types[2]], track_index, device_index, device_ref)
            self.track_table[track_callback_types[2]][track_index].device_count += 1
            self.track_table[track_callback_types[2]][track_index].selected_device_index = device_index
        else:
            raise RuntimeError(f"can't add device at OOB track index {track_index}, max track index is master_track {self.master_track_index}")

    def remove_device_list(self, track_index, device_index, device_list):
        for i, device in enumerate(device_list):
            self.remove_device(track_index, device_index - i)

    def remove_device(self, track_index, device_index):
        rtns_index = track_index - self.plain_track_count
        if track_index < self.plain_track_count:
            self._collapse_device_slot(self.device_table[track_callback_types[0]], track_index, device_index)
            self.track_table[track_callback_types[0]][track_index].device_count -= 0 if self.track_table[track_callback_types[0]][track_index].device_count < 1 else 1
            self.track_table[track_callback_types[0]][track_index].selected_device_index = device_index
        elif rtns_index < self.return_track_count:
            self._collapse_device_slot(self.device_table[track_callback_types[1]], rtns_index, device_index)
            self.track_table[track_callback_types[1]][rtns_index].device_count -= 0 if self.track_table[track_callback_types[1]][rtns_index].device_count < 1 else 1
            self.track_table[track_callback_types[1]][rtns_index].selected_device_index = device_index
        elif track_index == self.plain_track_count + self.return_track_count:
            self._collapse_device_slot(self.device_table[track_callback_types[2]], track_index, device_index)
            self.track_table[track_callback_types[2]][track_index].device_count -= 0 if self.track_table[track_callback_types[2]][track_index].device_count < 1 else 1
            self.track_table[track_callback_types[2]][track_index].selected_device_index = device_index
        else:
            raise RuntimeError(f"can't remove device at OOB track index {track_index}, max track index is master_track {self.master_track_index}")


    @staticmethod
    def _insert_track_slot(type_dict, track_index, track_ref):
        SongData.__shift_keys_right(type_dict, track_index, track_ref)

    @staticmethod
    def _insert_device_slot(type_dict, track_index, device_index, device_ref):
        if track_index in type_dict.keys():
            device_map = type_dict[track_index]
            SongData.__shift_keys_right(device_map, device_index, device_ref)
        else:
            type_dict[track_index] = {device_index: device_ref}

    @staticmethod
    def _collapse_track_slot(type_dict, track_index):
        SongData.__shift_keys_left(type_dict, track_index)

    @staticmethod
    def _collapse_device_slot(type_dict, track_index, device_index):
        if track_index in type_dict.keys():
            device_map = type_dict[track_index]
            SongData.__shift_keys_left(device_map, device_index)

    @staticmethod
    def __shift_keys_right(local_dict, key, value):
        if key in local_dict.keys():
            right_slots = {j + 1: local_dict[j] for j in range(key, len(local_dict.keys()))}
            local_dict[key] = value
            local_dict.update(right_slots)
        else:
            local_dict[key] = value
        
    @staticmethod
    def __shift_keys_left(local_dict, key):
        if key in local_dict.keys():
            # delete 3 of 3 == range(2, 2), 0 "right slots"
            # delete 2 of 3 == range(1, 2), 1 "right_slots" starting at key 
            # delete 1 of 3 == range(0, 2), 2 "right_slots" starting at key
            right_slots = {j: local_dict[j + 1] for j in range(key, len(local_dict.keys()) - 1)}
            del local_dict[key]
            if len(right_slots.keys()) > 0:
                local_dict.update(right_slots)


class EncoderAssignmentHistory(MackieC4Component):
    """
     Keeps track of Song Track and Device content supporting SYSEX "LCD feedback message" generation and other script functions
    """
    __module__ = __name__

    def __init__(self, main_script, encoder_controller):
        MackieC4Component.__init__(self, main_script)

        self.data = SongData()

        self.__my_controlling_encoder = encoder_controller
        self.__selected_track = self.main_script().song().view.selected_track
        self.__alt_selected_track = self.main_script().song().view.selected_track
        self.__selected_device = self.__selected_track.view.selected_device
        self.__master_track_index = self.data.master_track_index  # not a valid index until build_setup_database() runs
        self.__last_selected_track_index = 0
        self.__next_selected_track_index = 0
        # self.__last_selected_device_index = 0
        self.__next_selected_device_index = 0

    @property
    def next_selected_track(self):
        return self.__alt_selected_track

    @next_selected_track.setter
    def next_selected_track(self, track):
        self.__alt_selected_track = track

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

        self.data.clear_tracks()
        self.data.clear_devices()

        # tracks first
        error_msg = self.data.init_tracks(song_ref.visible_tracks, song_ref.return_tracks, song_ref.master_track)
        self.main_script().log_message(logging.ERROR, error_msg)

        # then devices
        for i, track in enumerate(song_ref.visible_tracks):
            for j, device in enumerate(track.devices):
                self.data.init_device(i, self.data.table_keys["plain"], j, device)

        for i, track in enumerate(song_ref.return_tracks):
            for j, device in enumerate(track.devices):
                self.data.init_device(i, self.data.table_keys["return"], j, device)

        for j, device in enumerate(song_ref.master_track.devices):
            self.data.init_device(self.data.master_track_index, self.data.table_keys["master"], j, device)


    def track_changed(self, track_index):
        track_ref = self.data.get_track(track_index)
        self.last_selected_track_index = track_index
        return track_ref.selected_device_index

    def tracks_added(self, track_index, tracks):
        final_track_count = len(tracks)
        at_index = track_index
        while final_track_count > self.track_count:
            track_obj = tracks[at_index]
            self.track_added(at_index, track_obj, track_obj.devices)
            at_index = self.last_selected_track_index

    def track_added(self, track_index, track_obj=None, devices_on_selected_track=None):

        if devices_on_selected_track is None:
            devices_on_selected_track = []

        rtn_idx = track_index - self.data.plain_track_count
        if track_index < self.data.plain_track_count:
            self.data.add_track(track_obj, self.data.table_keys["plain"], track_index)
        elif rtn_idx < self.data.return_track_count:
            self.data.add_track(track_obj, self.data.table_keys["return"], rtn_idx)
        # else can't add master

        if len(devices_on_selected_track) > 0:
            for i, dev_obj in enumerate(devices_on_selected_track):
                self.data.add_device(track_index, i, dev_obj)

        self.last_selected_track_index = track_index

    def tracks_deleted(self, track_index, tracks):
        final_track_count = len(tracks)
        at_index = track_index
        while final_track_count < self.track_count:
            self.track_deleted(at_index)
            at_index = self.last_selected_track_index

    def track_deleted(self, track_index):
        self.data.remove_track(track_index)
        self.last_selected_track_index = 0 if track_index < 1 else track_index - 1


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
        msg = f"{log_id}track index ref {last_track_ref.index} has name {last_track_ref.track.name} and old device count {old_device_count_track}"
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
            # new_track_device_bank_index = int(math.floor(selected_device_idx / SETUP_DB_DEVICE_BANK_SIZE))
            # new_device_bank_bank_index = selected_device_idx % SETUP_DB_DEVICE_BANK_SIZE
            #
            # log_msg = "{0}old_track_device_bank_index <{1}> ".format(log_id, current_bank)
            # if selected_device_idx >= SETUP_DB_DEVICE_BANK_SIZE and new_device_bank_bank_index == 0:
            #     # new index is an exact bank size match
            #
            #     self.t_d_bank_current[self.t_current] = new_track_device_bank_index
            #     current_bank = self.t_d_bank_current[self.t_current]
            #     # self.main_script().log_message(logging.DEBUG, "{0}updated to <{1}> because exact boundary".format(log_msg, current_bank))
            # else:
            #     log_msg = "{0}new_track_device_bank_index <{1}> ".format(log_id, current_bank)
            #     self.t_d_bank_current[self.t_current] = new_track_device_bank_index
            #     current_bank = self.t_d_bank_current[self.t_current]
            #     # self.main_script().log_message(logging.DEBUG, "{0}updated to <{1}> because not boundary".format(log_msg, current_bank))
        else:
            # log_msg = f"{log_id}new_track_device_bank_index <{current_bank}> "
            last_track_ref.selected_device_index = None # self.t_d_bank_current[self.t_current] = 0  # reset to default?
            current_bank = last_track_ref.device_bank_index_of_selected_device
            # self.main_script().log_message(logging.DEBUG, f"{log_msg}updated to <{current_bank}> because else")

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
            msg = f"{log_id}updated {last_track_ref.track.name}, device added {new_device.name} at index {new_device_index}, new device count is {last_track_ref.device_count}"
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
        msg = f"{log_id}updated {last_track_ref.track.name}, removed device at index {deleted_device_index} new device count is {last_track_ref.device_count}"
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
        msg = f"{log_id}selected device index of track {last_track_ref.track.name} changed from {last_track_ref.selected_device_index} to {changed_device_index}"
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
