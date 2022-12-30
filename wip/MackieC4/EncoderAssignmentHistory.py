
from __future__ import absolute_import, print_function, unicode_literals  # MS
from __future__ import division
import sys

from ableton.v2.base import liveobj_valid

# from Encoders import Encoders

if sys.version_info[0] >= 3:  # Live 11
    from builtins import range


# from .EncoderController import EncoderController
from . MackieC4Component import *
from . import track_util
from _Generic.Devices import *
import math


class EncoderAssignmentHistory(MackieC4Component):
    """
     Keeps track of all encoder assignments made by EncoderController
     This is a refactoring waypoint
    """
    __module__ = __name__

    def __init__(self, main_script, encoderController):
        MackieC4Component.__init__(self, main_script)

        self.__my_controlling_encoder = encoderController
        self.__master_track_index = 0
        self.t_count = 0  # nbr of regular tracks
        """number of regular tracks"""

        self.t_r_count = 0  # nbr of return tracks
        """number of return tracks"""

        self.t_current = 0  # index of current selected track
        """index of current selected track"""

        self.t_d_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]  # @Whiner: why is the "i" not used?
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

    def master_track_index(self):
        return self.__master_track_index

    def get_device_list(self, container):
        # add each device in order. if device is a rack, process each chain recursively
        # don't add racks that are not showing devices.
        # device_list = track_util.get_racks_recursive(track)  # this refers method used by Ableton in track_selection
        device_list = []
        for device in container:
            device_list.append(device)
            if device.can_have_chains:  # is a rack and it's open
                if device.view.is_showing_chain_devices:
                    for ch in device.chains:
                        device_list += self.get_device_list(ch.devices)
        return device_list

    def build_setup_database(self, song_ref=None):
        if song_ref is None:
            song_ref = self.song()

        self.t_count = 0
        self.main_script().log_message("t_current idx <{0}> t_count <{1}> BEFORE setup_db".format(self.t_current, self.t_count))

        tracks_in_song = self.song().tracks

        self.main_script().log_message("nbr tracks in song {0}".format(len(tracks_in_song)))
        loop_index_tracker = 0
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
                self.t_d_p_bank_count[t_idx][d_idx] = int(max_param_banks)
                self.t_d_p_bank_current[t_idx][d_idx] = 0

            self.t_count += 1
            loop_index_tracker = t_idx

        idx_nrml_trks = loop_index_tracker
        assert idx_nrml_trks == self.t_count - 1
        for rt_idx in range(len(self.song().return_tracks)):
            devices_on_rtn_track = self.song().return_tracks[rt_idx].devices
        # for rt_idx in range(len(song_ref.return_tracks)):
        #     devices_on_rtn_track = song_ref.return_tracks[rt_idx].devices
            ttl_t_idx = idx_nrml_trks + rt_idx + 1
            self.t_d_count[ttl_t_idx] = len(devices_on_rtn_track)
            max_device_banks = math.ceil(len(devices_on_rtn_track) // SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_count[ttl_t_idx] = int(max_device_banks)
            self.t_d_bank_current[ttl_t_idx] = 0
            self.t_d_current[ttl_t_idx] = 0
            for rt_d_idx in range(len(devices_on_rtn_track)):
                params_of_devices_on_rtn_trk = devices_on_rtn_track[rt_d_idx].parameters
                self.t_d_p_count[ttl_t_idx][rt_d_idx] = len(params_of_devices_on_rtn_trk)
                max_param_banks = math.ceil(len(params_of_devices_on_rtn_trk) // SETUP_DB_PARAM_BANK_SIZE)
                self.t_d_p_bank_count[ttl_t_idx][rt_d_idx] = int(max_param_banks)
                self.t_d_p_bank_current[ttl_t_idx][rt_d_idx] = 0

            self.t_count += 1
            self.t_r_count += 1
            loop_index_tracker = ttl_t_idx

        idx_nrml_and_rtn_trks = loop_index_tracker
        assert idx_nrml_and_rtn_trks == self.t_count - 1
        self.__master_track_index = idx_nrml_and_rtn_trks + 1
        mt_idx = self.__master_track_index
        assert mt_idx == self.t_count # the master track index == the number of tracks and returns
        devices_on_mstr_track = self.get_device_list(self.song().master_track)
        # devices_on_mstr_track = song_ref.master_track.devices
        self.t_d_count[mt_idx] = len(devices_on_mstr_track)
        max_device_banks = math.ceil(len(devices_on_mstr_track) // SETUP_DB_DEVICE_BANK_SIZE)
        self.t_d_bank_count[mt_idx] = int(max_device_banks)
        self.t_d_bank_current[mt_idx] = 0
        self.t_d_current[mt_idx] = 0
        for mt_d_idx in range(len(devices_on_mstr_track)):
            params_of_devices_on_mstr_trk = devices_on_mstr_track[mt_d_idx].parameters
            self.t_d_p_count[mt_idx][mt_d_idx] = len(params_of_devices_on_mstr_trk)
            max_param_banks = math.ceil(len(params_of_devices_on_mstr_trk) // SETUP_DB_PARAM_BANK_SIZE)
            self.t_d_p_bank_count[mt_idx][mt_d_idx] = int(max_param_banks)
            self.t_d_p_bank_current[mt_idx][mt_d_idx] = 0

        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> AFTER setup_db".format(self.t_current, self.t_count))

    def track_changed(self, track_index):
        rtn = -1
        self.main_script().log_message("t_current idx <{0}> t_count <{1}> BEFORE track change".format(self.t_current, self.t_count))
        self.t_current = track_index
        self.main_script().log_message("t_current idx <{0}> t_count <{1}> AFTER track change".format(self.t_current, self.t_count))
        if self.t_current == self.t_count:
            assert self.t_current == self.__master_track_index
            self.main_script().log_message("This is the index of the master Track")
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
        self.__master_track_index = self.t_count  # master track is "one past" the end of regular + return tracks
        # devices_on_selected_track = self.selected_track.devices
        self.t_d_count[track_index] = len(devices_on_selected_track)
        self.t_d_current[track_index] = 0
        self.t_d_bank_count[track_index] = int(math.ceil(len(devices_on_selected_track) // SETUP_DB_DEVICE_BANK_SIZE))
        self.t_d_bank_current[track_index] = 0
        for d in range(len(devices_on_selected_track)):
            parms_of_devs_on_trk = devices_on_selected_track[d].parameters
            self.t_d_p_count[track_index][d] = len(parms_of_devs_on_trk)
            self.t_d_p_bank_count[track_index][d] = int(math.ceil(len(parms_of_devs_on_trk) // SETUP_DB_PARAM_BANK_SIZE))
            self.t_d_p_bank_current[track_index][d] = 0

    def track_deleted(self, track_index):
        self.main_script().log_message(
            "t_current idx <{0}> t_count <{1}> BEFORE track delete device slide activity".format(self.t_current, self.t_count))
        for t in range(self.t_current + 1, self.t_count, 1):
            self.main_script().log_message(
                "t <{0}> t_d_count[t] <{1}> during device delete activity".format(t, self.t_d_count[t]))
            for d in range(self.t_d_count[t]):
                self.main_script().log_message("d <{0}> t_d_p_count[t][d] <{1}> during device param slide down activity".format(d, self.t_d_p_count[t][d]))
                self.t_d_p_count[(t - 1)][d] = self.t_d_p_count[t][d]
                self.main_script().log_message("d <{0}> t_d_p_bank_count[t][d] <{1}> during device param bank count slide down activity".format(d, self.t_d_p_bank_count[t][d]))
                self.t_d_p_bank_count[(t - 1)][d] = self.t_d_p_bank_count[t][d]
                self.main_script().log_message("d <{0}> t_d_p_bank_current[t][d] <{1}> during device param bank count slide down activity".format(d, self.t_d_p_bank_current[t][d]))
                self.t_d_p_bank_current[(t - 1)][d] = self.t_d_p_bank_current[t][d]

            self.main_script().log_message("t <{0}> t_d_count[t] <{1}> during device slide down activity".format(t, self.t_d_count[t]))
            self.t_d_count[t - 1] = self.t_d_count[t]
            self.main_script().log_message("t <{0}> t_d_current[t] <{1}> during current device slide down activity".format(t, self.t_d_current[t]))
            self.t_d_current[t - 1] = self.t_d_current[t]
            self.main_script().log_message("t <{0}> t_d_bank_count[t] <{1}> during current device slide down activity".format(t, self.t_d_bank_count[t]))
            self.t_d_bank_count[t - 1] = self.t_d_bank_count[t]
            self.main_script().log_message("t <{0}> t_d_bank_current[t] <{1}> during current device slide down activity".format(t,self.t_d_bank_current[t]))
            self.t_d_bank_current[t - 1] = self.t_d_bank_current[t]

        self.t_count -= 1
        self.__master_track_index = self.t_count  # master track is "one past" the end of regular + return tracks
        self.t_current = track_index
        self.main_script().log_message("t_current idx <{0}> t_count <{1}> AFTER track delete device slide activity".format(self.t_current, self.t_count))

    def device_added_deleted_or_changed(self, all_devices, selected_device, selected_device_idx):

        new_device_count_track = len(all_devices)
        self.main_script().log_message("EAH: track device list size <{0}> BEFORE device update".format(new_device_count_track))
        idx = 0
        for device in all_devices:
            if liveobj_valid(device):
                self.main_script().log_message("idx <{0}> before <{1}>".format(idx, device.name))
            else:
                self.main_script().log_message("idx <{0}> before <None> or lost weakref".format(idx))
            idx += 1

        if liveobj_valid(selected_device) and selected_device_idx > -1:
            self.main_script().log_message("passed idx <{0}> and device <{1}>".format(selected_device_idx, selected_device.name))

        # this is the "old count"
        device_count_track = self.t_d_count[self.t_current]

        device_was_added = new_device_count_track > device_count_track
        device_was_removed = new_device_count_track < device_count_track
        selected_device_was_changed = new_device_count_track == device_count_track
        no_devices_on_track = new_device_count_track == 0
        if selected_device_idx == -1:
            assert no_devices_on_track  # == True

        self.main_script().log_message("no devices currently on track <{0}>".format(no_devices_on_track))
        self.main_script().log_message("add event <{0}> delete event <{1}> change event <{2}>".format(device_was_added, device_was_removed, selected_device_was_changed))

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

            self.t_d_count[self.t_current] = new_device_count_track
            incremented_device_count_track = self.t_d_count[self.t_current]

            self.t_d_current[self.t_current] = new_device_index
            max_needed_device_banks = int(math.ceil(incremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
            if SETUP_DB_MAX_DEVICE_BANKS > max_needed_device_banks:
                self.t_d_bank_count[self.t_current] = max_needed_device_banks
            else:
                self.t_d_bank_count[self.t_current] = SETUP_DB_MAX_DEVICE_BANKS

            # only update the current bank if this added device goes over the current page boundary
            # and is inside the max page boundary
            # page 0 is devices 1 - 8  page 16 is devices 121 - 128
            new_current_device_bank_offset = incremented_device_count_track % SETUP_DB_DEVICE_BANK_SIZE
            if incremented_device_count_track > SETUP_DB_DEVICE_BANK_SIZE and new_current_device_bank_offset == 1:
                self.t_d_bank_current[self.t_current] += 1
                self.main_script().log_message("updated current track device bank to <{0}>"
                                               .format(self.t_d_bank_current[self.t_current]))
            else:
                self.main_script().log_message("not updating current track device bank from <{0}>"
                                               .format(self.t_d_bank_current[self.t_current]))

        elif device_was_removed:
            self.main_script().log_message("for 'delete' device event handling")

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
                    self.t_d_count[self.t_current] -= 1
                else:
                    self.t_d_count[self.t_current] = 0
            else:
                self.t_d_count[self.t_current] -= 1

            assert new_device_count_track == self.t_d_count[self.t_current]
            decremented_device_count_track = self.t_d_count[self.t_current]
            self.t_d_current[self.t_current] = deleted_device_index
            max_needed_device_banks = int(math.ceil(decremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
            if SETUP_DB_MAX_DEVICE_BANKS > max_needed_device_banks:
                self.t_d_bank_count[self.t_current] = max_needed_device_banks
            else:
                self.t_d_bank_count[self.t_current] = SETUP_DB_MAX_DEVICE_BANKS

            # only update the current bank if this removed device puts the selected device on the previous page bank
            # and is not the minimum page bank already
            # page 0 is devices 1 - 8  page 16 is devices 121 - 128
            new_current_device_bank_offset = decremented_device_count_track % SETUP_DB_DEVICE_BANK_SIZE
            if decremented_device_count_track > SETUP_DB_DEVICE_BANK_SIZE and new_current_device_bank_offset == 0:
                self.t_d_bank_current[self.t_current] -= 1

        elif selected_device_was_changed:
            self.main_script().log_message("EAH for 'change' device event handling")
            # param_count_track = self.t_d_p_count[self.t_current]
            # param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            # param_bank_current_track = self.t_d_p_bank_current[self.t_current]

            self.t_d_current[self.t_current] = changed_device_index
            assert new_device_count_track == self.t_d_count[self.t_current]
            new_current_device_bank_offset = new_device_count_track % SETUP_DB_DEVICE_BANK_SIZE
            if new_device_count_track > SETUP_DB_DEVICE_BANK_SIZE and new_current_device_bank_offset == 0:
                # changing from device 9 to device 8 decrements the current bank
                self.t_d_bank_current[self.t_current] -= 1
            elif new_device_count_track > SETUP_DB_DEVICE_BANK_SIZE and new_current_device_bank_offset == 1:
                # changing from device 8 to device 9 increments the current bank
                self.t_d_bank_current[self.t_current] += 1

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
        
        