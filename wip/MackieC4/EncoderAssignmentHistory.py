
from __future__ import absolute_import, print_function, unicode_literals  # MS
from __future__ import division
import sys

from Push2.model import DeviceParameter
from ableton.v2.base import listenable_property
from ableton.v2.control_surface.components import undo_redo
from . import track_util
from . import song_util

# from Encoders import Encoders

if sys.version_info[0] >= 3:  # Live 11
    from past.utils import old_div
    from builtins import range


# from .EncoderController import EncoderController
from . consts import *
from . MackieC4Component import *
from _Generic.Devices import *
import math
import time
from itertools import chain
import Live


class EncoderAssignmentHistory(MackieC4Component):
    """
     Keeps track of all encoder assignments made by EncoderController
     This is a refactoring waypoint
    """
    __module__ = __name__

    def __init__(self, main_script, encoderController):
        MackieC4Component.__init__(self, main_script)

        self.__my_controlling_encoder = encoderController

        self.t_count = 0  # nbr of regular tracks
        """number of regular tracks"""

        self.t_r_count = 0  # nbr of return tracks
        """number of return tracks"""

        self.t_current = 0  # index of current selected track
        """index of current selected track"""

        self.t_d_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
        """current track device count"""

        # track device current -- the index of the currently selected device indexed by the t_current track
        self.t_d_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]  # MS why is "i" not used??

        # t_d bank count -- the count of the devices on the t_current track (in banks of 8 parameters)
        # see device_counter(self, t, d): (at the same index) the same number as t_d_current but divided by 8
        self.t_d_bank_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]  # MS why is "i" not used??

        # t_d bank current -- the index of currently selected device indexed by the t_current track
        # (in banks of 8 parameters) the same index as t_d_current divided by 8
        self.t_d_bank_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]  # MS why is "i" not used??

        # t_d parameter count -- the count of remote controllable parameters available for the currently selected
        # device on the t_current track
        self.t_d_p_count = [[0 for i in range(SETUP_DB_DEFAULT_SIZE)] for j in range(SETUP_DB_DEFAULT_SIZE)]

        # t_d_p bank count -- the count of remote controllable parameters available for the currently selected device on
        # the t_current track (in banks of 24 params)[at the same index, the same number as t_d_p_count but divided by 8]
        self.t_d_p_bank_count = [[0 for i in range(SETUP_DB_DEFAULT_SIZE)] for j in range(SETUP_DB_DEFAULT_SIZE)]

        # t_d_p bank current -- the index of the selected remote controllable parameter of the currently selected
        # device on the t_current track (in banks of 24 params)
        self.t_d_p_bank_current = [[0 for i in range(SETUP_DB_DEFAULT_SIZE)] for j in range(SETUP_DB_DEFAULT_SIZE)]

    # def reset_device_counter(self):
    #     self.t_d_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
    #     self.t_d_bank_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]

    def update_device_counter(self, t, d):
        self.t_d_count[t] = d
        max_device_banks = math.ceil(d // SETUP_DB_DEVICE_BANK_SIZE)
        self.t_d_bank_count[t] = int(max_device_banks)

    def build_setup_database(self, song_ref=None):
        if song_ref is None:
            song_ref = self.song()

        self.t_count = 0
        self.main_script().log_message("t_current idx <{0}> t_count <{1}> BEFORE setup_db"
                                       .format(self.t_current, self.t_count))

        tracks_in_song = self.song().tracks
        #tracks_in_song = song_ref.tracks
        self.main_script().log_message("nbr tracks in song {0}".format(len(tracks_in_song)))
        for t_idx in range(len(tracks_in_song)):
            devices_on_track = tracks_in_song[t_idx].devices
            self.t_d_count[t_idx] = len(devices_on_track)
            max_device_banks = math.ceil(len(devices_on_track) // SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_count[t_idx] = int(max_device_banks)
            self.t_d_bank_current[t_idx] = 0
            self.t_d_current[t_idx] = 0
            for d_idx in range(len(devices_on_track)):
                params_of_devices_on_trk = devices_on_track[d_idx].parameters
                self.t_d_p_count[t_idx][d_idx] = len(params_of_devices_on_trk)
                max_param_banks = math.ceil(len(params_of_devices_on_trk) // SETUP_DB_PARAM_BANK_SIZE)
                self.t_d_p_bank_count[t_idx][d_idx] = max_param_banks
                self.t_d_p_bank_current[t_idx][d_idx] = 0

            self.t_count += 1

        idx_nrml_trks = t_idx
        assert idx_nrml_trks == self.t_count - 1
        for rt_idx in range(len(self.song().return_tracks)):
            devices_on_rtn_track = self.song().return_tracks[rt_idx].devices
        # for rt_idx in range(len(song_ref.return_tracks)):
        #     devices_on_rtn_track = song_ref.return_tracks[rt_idx].devices
            ttl_t_idx = idx_nrml_trks + rt_idx + 1
            self.t_d_count[ttl_t_idx] = len(devices_on_rtn_track)
            max_device_banks = math.ceil(len(devices_on_rtn_track) // SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_count[ttl_t_idx] = max_device_banks
            self.t_d_bank_current[ttl_t_idx] = 0
            self.t_d_current[ttl_t_idx] = 0
            for rt_d_idx in range(len(devices_on_rtn_track)):
                params_of_devices_on_rtn_trk = devices_on_rtn_track[rt_d_idx].parameters
                self.t_d_p_count[ttl_t_idx][rt_d_idx] = len(params_of_devices_on_rtn_trk)
                max_param_banks = math.ceil(len(params_of_devices_on_rtn_trk) // SETUP_DB_PARAM_BANK_SIZE)
                self.t_d_p_bank_count[ttl_t_idx][rt_d_idx] = max_param_banks
                self.t_d_p_bank_current[ttl_t_idx][rt_d_idx] = 0

            self.t_count += 1
            self.t_r_count += 1

        idx_nrml_and_rtn_trks = ttl_t_idx
        assert idx_nrml_and_rtn_trks == self.t_count - 1
        self.__master_track_index = idx_nrml_and_rtn_trks + 1
        mt_idx = self.__master_track_index
        assert mt_idx == self.t_count # the master track index == the number of tracks and returns
        devices_on_mstr_track = self.song().master_track.devices
        # devices_on_mstr_track = song_ref.master_track.devices
        self.t_d_count[mt_idx] = len(devices_on_mstr_track)
        max_device_banks = math.ceil(len(devices_on_mstr_track) // SETUP_DB_DEVICE_BANK_SIZE)
        self.t_d_bank_count[mt_idx] = max_device_banks
        self.t_d_bank_current[mt_idx] = 0
        self.t_d_current[mt_idx] = 0
        for mt_d_idx in range(len(devices_on_mstr_track)):
            params_of_devices_on_mstr_trk = devices_on_mstr_track[mt_d_idx].parameters
            self.t_d_p_count[mt_idx][mt_d_idx] = len(params_of_devices_on_mstr_trk)
            max_param_banks = math.ceil(len(params_of_devices_on_mstr_trk) // SETUP_DB_PARAM_BANK_SIZE)
            self.t_d_p_bank_count[mt_idx][mt_d_idx] = max_param_banks
            self.t_d_p_bank_current[mt_idx][mt_d_idx] = 0

        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> AFTER setup_db".format(self.t_current, self.t_count))

    def track_changed(self, track_index):
        rtn = -1
        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> BEFORE track change".format(self.t_current, self.t_count))
        self.t_current = track_index
        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> AFTER track change".format(self.t_current, self.t_count))
        if len(self.t_d_current) > self.t_current:
            rtn = self.t_d_current[self.t_current]
        elif len(self.t_d_current) > 0:
            rtn = 0
        else:
            # something isn't getting updated correctly at startup and/or when devices are deleted
            self.main_script().log_message("len(self.t_d_current) <= self.t_current")
            self.main_script().log_message("{0} <= {1}".format(len(self.t_d_current), self.t_current))

        return rtn

    def track_added(self, track_index, devices_on_selected_track=None):
        if devices_on_selected_track is None:
            devices_on_selected_track = []

        start = self.t_count + 1
        stop = track_index - 1
        track_index_range = range(start, stop, -1)
        # There is always a "selected track" if a new track is inserted in Live
        # and the new track is (or tracks are) inserted to the right of the selected track,
        # so there should always be t's in track_index_range to loop over
        #
        # this only works as long as everything still fits inside 128 indexes, SETUP_DB_DEFAULT_SIZE
        # i.e. (regular_tracks + return_tracks + master_track) must be >= 0 AND <= 128
        # similarly the number of devices on any one track must be >= 0 AND <= 128
        # similarly the number of remote-controllable parameters on any one device must be >= 0 AND <= 128
        for t in track_index_range:
            for d in range(self.t_d_count[t]):

                # shift values up one index to make room for new track data
                self.t_d_p_count[(t + 1)][d] = self.t_d_p_count[t][d]
                self.t_d_p_bank_count[(t + 1)][d] = self.t_d_p_bank_count[t][d]
                self.t_d_p_bank_current[(t + 1)][d] = self.t_d_p_bank_current[t][d]

            # insert new values in freshly opened index
            self.t_d_count[t + 1] = self.t_d_count[t]
            self.t_d_current[t + 1] = self.t_d_current[t]
            self.t_d_bank_count[t + 1] = self.t_d_bank_count[t]
            self.t_d_bank_current[t + 1] = self.t_d_bank_current[t]

        self.t_current = track_index
        # self.selected_track = self.song().view.selected_track
        self.t_count += 1
        # devices_on_selected_track = self.selected_track.devices
        self.t_d_count[track_index] = len(devices_on_selected_track)
        self.t_d_current[track_index] = 0
        self.t_d_bank_count[track_index] = math.ceil(len(devices_on_selected_track) // SETUP_DB_DEVICE_BANK_SIZE)
        self.t_d_bank_current[track_index] = 0
        for d in range(len(devices_on_selected_track)):
            parms_of_devs_on_trk = devices_on_selected_track[d].parameters
            self.t_d_p_count[track_index][d] = len(parms_of_devs_on_trk)
            self.t_d_p_bank_count[track_index][d] = math.ceil(len(parms_of_devs_on_trk) // SETUP_DB_PARAM_BANK_SIZE)
            self.t_d_p_bank_current[track_index][d] = 0

    def track_deleted(self, track_index):
        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> BEFORE track delete device slide activity".format(self.t_current, self.t_count))
        for t in range(self.t_current + 1, self.t_count, 1):
            self.main_script().log_message(
                "t <{0}> t_d_count[t] <{1}> during device delete activity".format(t, self.t_d_count[t]))
            for d in range(self.t_d_count[t]):
                self.main_script().log_message(
                    "d <{0}> t_d_p_count[t][d] <{1}> during device param slide down activity".format(d, self.t_d_p_count[t][d]))
                self.t_d_p_count[(t - 1)][d] = self.t_d_p_count[t][d]
                self.main_script().log_message(
                    "d <{0}> t_d_p_bank_count[t][d] <{1}> during device param bank count slide down activity".format(d, self.t_d_p_bank_count[t][d]))
                self.t_d_p_bank_count[(t - 1)][d] = self.t_d_p_bank_count[t][d]
                self.main_script().log_message(
                    "d <{0}> t_d_p_bank_current[t][d] <{1}> during device param bank count slide down activity".format(d, self.t_d_p_bank_current[t][d]))
                self.t_d_p_bank_current[(t - 1)][d] = self.t_d_p_bank_current[t][d]

            self.main_script().log_message(
                "t <{0}> t_d_count[t] <{1}> during device slide down activity".format(t, self.t_d_count[t]))
            self.t_d_count[t - 1] = self.t_d_count[t]
            self.main_script().log_message(
                "t <{0}> t_d_current[t] <{1}> during current device slide down activity".format(t, self.t_d_current[t]))
            self.t_d_current[t - 1] = self.t_d_current[t]
            self.main_script().log_message(
                "t <{0}> t_d_bank_count[t] <{1}> during current device slide down activity".format(t, self.t_d_bank_count[t]))
            self.t_d_bank_count[t - 1] = self.t_d_bank_count[t]
            self.main_script().log_message(
                "t <{0}> t_d_bank_current[t] <{1}> during current device slide down activity".format(t,self.t_d_bank_current[t]))
            self.t_d_bank_current[t - 1] = self.t_d_bank_current[t]

        self.t_count -= 1
        self.t_current = track_index
        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> AFTER track delete device slide activity".format(self.t_current, self.t_count))



    def device_added_deleted_or_changed(self, all_devices, selected_device):

        # new_device_count_track = len(self.selected_track.devices)
        new_device_count_track = len(all_devices)
        self.main_script().log_message("track device list size <{0}> BEFORE device update".format(new_device_count_track))
        for device in all_devices:
            if device is not None:
                self.main_script().log_message("before <{0}>".format(device.name))
            else:
                self.main_script().log_message("before <None>")

        # this is the "old count"
        device_count_track = self.t_d_count[self.t_current]
        device_was_added = new_device_count_track > device_count_track
        device_was_removed = new_device_count_track < device_count_track
        selected_device_was_changed = new_device_count_track == device_count_track
        no_devices_on_track = new_device_count_track == 0

        # self.main_script().log_message("no devices currently on track <{0}>".format(no_devices_on_track))
        #
        # self.main_script().log_message("add event <{0}> delete event <{1}> change event <{2}>"
        #                                .format(device_was_added, device_was_removed, selected_device_was_changed))

        index = 0
        new_device_index = 0
        deleted_device_index = 0
        changed_device_index = 0
        rtn_device_index = -1

        # if there are no devices on track, all indexes are 0
        # which is a valid index??
        for device in all_devices:
            if selected_device == device:
                new_device_index = index
                deleted_device_index = index
                changed_device_index = index
                rtn_device_index = index
                self.main_script().log_message("found event index <{0}> and device <{1}>".format(index, device.name))
                break
            else:
                index += 1

        # FROM HERE: "found event index <{0}> and device <{1}>".format(index, device.name)
        # represent "source of truth"   device == self.selected_track.devices[index]
        if device_was_added:
            self.main_script().log_message("for 'add' device event handling")
            param_count_track = self.t_d_p_count[self.t_current]
            param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            param_bank_current_track = self.t_d_p_bank_current[self.t_current]
            for d in range(device_count_track, new_device_index + 1, -1):
                c = d - 1
                param_count_track[d] = param_count_track[c]
                param_bank_count_track[d] = param_bank_count_track[c]
                param_bank_current_track[d] = param_bank_current_track[c]

            param_count_track[new_device_index] = len(all_devices[new_device_index].parameters)
            max_param_banks = math.ceil(param_count_track[new_device_index] // SETUP_DB_PARAM_BANK_SIZE)
            param_bank_count_track[new_device_index] = max_param_banks
            param_bank_current_track[new_device_index] = 0

            self.t_d_count[self.t_current] += 1
            device_count_track = self.t_d_count[self.t_current]

            self.t_d_current[self.t_current] = new_device_index
            max_device_banks = math.ceil(device_count_track // SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_count[self.t_current] = max_device_banks
            max_device_banks = math.ceil(device_count_track + 1 // SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_current[self.t_current] = max_device_banks
            # self.__chosen_plugin = self.selected_track.devices[new_device_index]
            # self.__reorder_parameters()
            # self.__reassign_encoder_parameters(for_display_only=False)
            # self.request_rebuild_midi_map()
        elif device_was_removed:
            self.main_script().log_message("for 'delete' device event handling")
            # still?
            param_count_track = self.t_d_p_count[self.t_current]
            param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            param_bank_current_track = self.t_d_p_bank_current[self.t_current]
            for d in range(deleted_device_index + 1, device_count_track, 1):
                c = d - 1
                param_count_track[d] = param_count_track[c]
                param_bank_count_track[d] = param_bank_count_track[c]
                param_bank_current_track[d] = param_bank_current_track[c]

            if deleted_device_index == device_count_track - 1:  # "last" device in list or "only" device in list
                # only decrement "current device" index if deleted device wasn't the only device
                if deleted_device_index > 0:
                    self.t_d_current[self.t_current] -= 1
                    max_device_banks = math.ceil((self.t_d_current[self.t_current] + 1) // SETUP_DB_DEVICE_BANK_SIZE)
                    self.t_d_bank_current[self.t_current] = max_device_banks
                else:
                    self.t_d_current[self.t_current] = 0  # zero is the value all "db" lists are initialized with
            else:
                self.t_d_current[self.t_current] = deleted_device_index
                # index of deleted device is now index of current device

                # set the current "parameter bank" page number of new current device
                # calculate the current bank page number of the new current device by adding 1 to
                # the value of the deleted device index (this is index of device on "right" of deleted device because
                # inside this else condition we know there is at least one device at a higher index,
                # "above" the deleted device's index) and then dividing by 8?
                # and that is supposed to be the "selected parameter bank" of the new current device?
                # we wouldn't do this when the only device was deleted, but when the 4th of 4 was deleted, wouldn't
                # we also want to update the new current device's current selected parameter bank? (see change above)
                max_device_banks = math.ceil((self.t_d_current[self.t_current] + 1) // SETUP_DB_DEVICE_BANK_SIZE)
                self.t_d_bank_current[self.t_current] = max_device_banks

            # decrement this track's total device count
            self.t_d_count[self.t_current] -= 1
            # set the device "bank" -- if there are more than 8 devices on a track, 9 - 16 will be in device bank 2
            max_device_banks = math.ceil(self.t_d_count[self.t_current] // SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_count[self.t_current] = max_device_banks

        return rtn_device_index

    def get_current_track_device_parameter_bank_nbr(self, t_d_idx=None):
        if t_d_idx is None:
            t_d_idx = self.t_d_current[self.t_current]

        return self.t_d_p_bank_current[self.t_current][t_d_idx]

    def set_current_track_device_parameter_bank_nbr(self, current_bank_nbr):
        self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]] = current_bank_nbr

    def get_max_current_track_device_parameter_bank_nbr(self, t_d_idx=None):
        if t_d_idx is None:
            t_d_idx = self.t_d_current[self.t_current]

        return self.t_d_p_bank_count[self.t_current][t_d_idx]

    def set_max_current_track_device_parameter_bank_nbr(self, updated_bank_nbr):
        self.t_d_p_bank_count[self.t_current][self.t_d_current[self.t_current]] = updated_bank_nbr

    def get_selected_device_index(self):
        selected_device_index = -1
        if len(self.t_d_current) > self.t_current:
            selected_device_index = self.t_d_current[self.t_current]
        elif len(self.t_d_current) > 0:
            selected_device_index = 0
        return selected_device_index

    def set_selected_device_index(self, selected_device_index):
        self.t_d_current[self.t_current] = selected_device_index

    def get_max_device_count(self):
        max_device_count = -1
        if len(self.t_d_count) > self.t_current:
            max_device_count = self.t_d_count[self.t_current]
        elif len(self.t_d_count) > 0:
            max_device_count = 0
        return max_device_count

    def set_max_device_count(self, max_device_count):
        self.t_d_count[self.t_current] = max_device_count

    def get_selected_device_bank_index(self):
        selected_device_bank_index = -1
        if len(self.t_d_bank_current) > self.t_current:
            selected_device_bank_index = self.t_d_bank_current[self.t_current]
        elif len(self.t_d_bank_current) > 0:
            selected_device_bank_index = 0
        return selected_device_bank_index

    def set_selected_device_bank_index(self, selected_device_bank_index):
        self.t_d_bank_current[self.t_current] = selected_device_bank_index

    def get_selected_device_bank_count(self):
        selected_device_bank_count = -1
        if len(self.t_d_bank_count) > self.t_current:
            selected_device_bank_count = self.t_d_bank_count[self.t_current]
        elif len(self.t_d_bank_count) > 0:
            selected_device_bank_count = 0
        return selected_device_bank_count

    def set_selected_device_bank_count(self, selected_device_bank_count):
        self.t_d_bank_count[self.t_current] = selected_device_bank_count
        
        