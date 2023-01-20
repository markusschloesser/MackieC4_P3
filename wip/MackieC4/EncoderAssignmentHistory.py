
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

        self.t_d_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]
        """current track device count"""

        # track device current -- the index of the currently selected device indexed by the t_current track
        self.t_d_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]

        # t_d bank count -- the count of the devices on the t_current track (in banks of 8 parameters)
        # see device_counter(self, t, d): (at the same index) the same number as t_d_current but divided by 8
        self.t_d_bank_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]

        # t_d bank current -- the index of currently selected device indexed by the t_current track
        # (in banks of 8 parameters) the same index as t_d_current divided by 8
        self.t_d_bank_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]

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
        devices_on_mstr_track = self.get_device_list(self.song().master_track.devices)
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

        # self.main_script().log_message("t_current idx <{0}> t_count <{1}> AFTER setup_db".format(self.t_current, self.t_count))

    def track_changed(self, track_index):
        rtn = -1
        # self.main_script().log_message("t_current idx <{0}> t_count <{1}> BEFORE track change".format(self.t_current, self.t_count))
        self.t_current = track_index
        # self.main_script().log_message("t_current idx <{0}> t_count <{1}> AFTER track change".format(self.t_current, self.t_count))
        if self.t_current == self.t_count:
            assert self.t_current == self.__master_track_index
            # self.main_script().log_message("This is the index of the master Track")
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
            # MS: this assumes that only ONE track is ever inserted, correct? While this is true for right-clicking and adding tracks, one can also insert multiple tracks at once,
            # by loading them from the library. I will test this. We might need to make the +1 dynamic.
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
        # self.main_script().log_message("t_current idx <{0}> t_count <{1}> BEFORE track delete device slide activity".format(self.t_current, self.t_count))
        for t in range(self.t_current + 1, self.t_count, 1):
            # self.main_script().log_message("t <{0}> t_d_count[t] <{1}> during device delete activity".format(t, self.t_d_count[t]))
            for d in range(self.t_d_count[t]):
                # self.main_script().log_message("d <{0}> t_d_p_count[t][d] <{1}> during device param slide down activity".format(d, self.t_d_p_count[t][d]))
                self.t_d_p_count[(t - 1)][d] = self.t_d_p_count[t][d]
                # self.main_script().log_message("d <{0}> t_d_p_bank_count[t][d] <{1}> during device param bank count slide down activity".format(d, self.t_d_p_bank_count[t][d]))
                self.t_d_p_bank_count[(t - 1)][d] = self.t_d_p_bank_count[t][d]
                # self.main_script().log_message("d <{0}> t_d_p_bank_current[t][d] <{1}> during device param bank count slide down activity".format(d, self.t_d_p_bank_current[t][d]))
                self.t_d_p_bank_current[(t - 1)][d] = self.t_d_p_bank_current[t][d]

            # self.main_script().log_message("t <{0}> t_d_count[t] <{1}> during device slide down activity".format(t, self.t_d_count[t]))
            self.t_d_count[t - 1] = self.t_d_count[t]
            # self.main_script().log_message("t <{0}> t_d_current[t] <{1}> during current device slide down activity".format(t, self.t_d_current[t]))
            self.t_d_current[t - 1] = self.t_d_current[t]
            # self.main_script().log_message("t <{0}> t_d_bank_count[t] <{1}> during current device slide down activity".format(t, self.t_d_bank_count[t]))
            self.t_d_bank_count[t - 1] = self.t_d_bank_count[t]
            # self.main_script().log_message("t <{0}> t_d_bank_current[t] <{1}> during current device slide down activity".format(t,self.t_d_bank_current[t]))
            self.t_d_bank_current[t - 1] = self.t_d_bank_current[t]

        self.t_count -= 1
        self.__master_track_index = self.t_count  # master track is "one past" the end of regular + return tracks
        self.t_current = track_index
        # self.main_script().log_message("t_current idx <{0}> t_count <{1}> AFTER track delete device slide activity".format(self.t_current, self.t_count))

    def device_added_deleted_or_changed(self, all_devices, selected_device, selected_device_idx):
        log_id = "EAH/device_added_deleted_or_changed: "
        new_device_count_track = len(all_devices)
        # self.main_script().log_message("{0}input device list len<{1}>".format(log_id, new_device_count_track))
        idx = 0
        log_msg = "{0}device in input device list at index<{1}> is ".format(log_id, idx)
        for device in all_devices:
            if liveobj_valid(device):
                pass  # self.main_script().log_message("{0}a valid Live object named <{1}>".format(log_msg, device.name))
            else:
                self.main_script().log_message("{0}<None> or a lost weakref".format(log_msg))
            idx += 1
            log_msg = "{0}device in input device list at index<{1}> is ".format(log_id, idx)

        # if liveobj_valid(selected_device):
        #     self.main_script().log_message("{0}input selected_device is a valid Live object named<{1}>".format(log_id, selected_device.name))
        # if selected_device_idx > -1:
        #     self.main_script().log_message("{0}input selected_device_idx<{1}> points to a forward index".format(log_id, selected_device_idx))

        old_device_count_track = self.t_d_count[self.t_current]
        old_selected_device_index = self.t_d_current[self.t_current]

        device_was_added = new_device_count_track > old_device_count_track
        device_was_removed = new_device_count_track < old_device_count_track
        selected_device_was_changed = new_device_count_track == old_device_count_track
        no_devices_on_track = new_device_count_track == 0

        rack_devices_deleted = old_device_count_track - new_device_count_track if device_was_removed else 0
        rack_devices_added = new_device_count_track - old_device_count_track if device_was_added else 0
        rack_devices_skipped = old_selected_device_index - selected_device_idx if selected_device_was_changed else 0

        log_msg = "{0}input selected_device_idx<{1}> and input device list len<{2}> ".format(log_id,
                                                                                             selected_device_idx,
                                                                                             new_device_count_track)
        if selected_device_idx == -1:
            # self.main_script().log_message("{0}agree that no devices currently populate the device chain for this track".format(log_msg))
            assert no_devices_on_track  # == True
        # else:
            # self.main_script().log_message("{0}agree that at least one device currently populates the device chain for this track".format(log_msg))

        # self.main_script().log_message("{0}add event <{1}>, delete event <{2}>, change event <{3}>".format(log_id, device_was_added,device_was_removed,selected_device_was_changed))

        index = 0
        new_device_index = 0
        deleted_device_index = 0
        changed_device_index = 0
        rtn_device_index = -1
        found_input_device_index = False  # selected_device is in all_devices

        # if there are no devices on track, there are no devices in input all_devices list
        # and this loop is not entered, all "change indexes" stay 0
        # if a device was deleted, selected_device will be at the index before the deleted device
        for device in all_devices:
            if selected_device == device:
                new_device_index = index
                deleted_device_index = index
                changed_device_index = index
                rtn_device_index = index
                found_input_device_index = True
                # self.main_script().log_message("{0}matched input selected_device<{1}> with device<{2}> at index<{3}> of input device list".format(log_id, selected_device.name, device.name, index))
                break
            else:
                index += 1

        cb = self.t_d_bank_current[self.t_current]
        if found_input_device_index:
            new_track_device_bank_index = int(math.floor(selected_device_idx / SETUP_DB_DEVICE_BANK_SIZE))
            new_device_bank_bank_index = selected_device_idx % SETUP_DB_DEVICE_BANK_SIZE

            log_msg = "{0}old_track_device_bank_index <{1}> ".format(log_id, cb)
            if selected_device_idx >= SETUP_DB_DEVICE_BANK_SIZE and new_device_bank_bank_index == 0:
                # new index is an exact bank size match
                log_msg = "{0}new_track_device_bank_index <{1}> ".format(log_id, cb)
                self.t_d_bank_current[self.t_current] = new_track_device_bank_index
                cb = self.t_d_bank_current[self.t_current]
                # self.main_script().log_message("{0}updated to <{1}> because exact boundary".format(log_msg, cb))
            else:
                log_msg = "{0}new_track_device_bank_index <{1}> ".format(log_id, cb)
                self.t_d_bank_current[self.t_current] = new_track_device_bank_index
                cb = self.t_d_bank_current[self.t_current]
                # self.main_script().log_message("{0}updated to <{1}> because not boundary".format(log_msg, cb))
        else:
            log_msg = "{0}new_track_device_bank_index <{1}> ".format(log_id, cb)
            self.t_d_bank_current[self.t_current] = 0  # reset to default?
            cb = self.t_d_bank_current[self.t_current]
            # self.main_script().log_message("{0}updated to <{1}> because else".format(log_msg, cb))

        # FROM HERE: "found event index <{0}> and device <{1}>".format(index, device.name)
        # represent "source of truth"   device == self.selected_track.devices[index]
        # and we could
        # return rtn_device_index
        # right here, except for updating the "assignment history" database

        if device_was_added:
            # self.main_script().log_message("{0}device_was_added:".format(log_id))
            param_count_track = self.t_d_p_count[self.t_current]
            param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            param_bank_current_track = self.t_d_p_bank_current[self.t_current]
            for d in range(old_device_count_track, new_device_index + 1, -1):
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
            if SETUP_DB_MAX_DEVICE_BANKS >= max_needed_device_banks:
                self.t_d_bank_count[self.t_current] = max_needed_device_banks
            else:
                self.main_script().log_message("{0}because we don't need no stinking badges".format(log_id))
                self.t_d_bank_count[self.t_current] = 1

        elif device_was_removed:
            # self.main_script().log_message("{0}device_was_removed: for 'delete' device event handling".format(log_id))

            param_count_track = self.t_d_p_count[self.t_current]
            param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            param_bank_current_track = self.t_d_p_bank_current[self.t_current]
            # self.main_script().log_message("{0}device_was_removed: deleted_device_index<{1}> old_device_count_track<{2}>".format(log_id, deleted_device_index, old_device_count_track))

            for d in range(deleted_device_index + 1, old_device_count_track, 1):
                c = d - 1
                param_count_track[d] = param_count_track[c]
                param_bank_count_track[d] = param_bank_count_track[c]
                param_bank_current_track[d] = param_bank_current_track[c]

            # "only" device in device chain is also "last" device in device chain
            last_device_in_chain = deleted_device_index == old_device_count_track - 1  # 0 != -1 here
            empty_chain = old_device_count_track == 0 and not found_input_device_index
            if last_device_in_chain or empty_chain:
                # only decrement "device count" if deleted device wasn't the only device
                if deleted_device_index > 0:
                    self.t_d_count[self.t_current] -= rack_devices_deleted
                else:
                    self.t_d_count[self.t_current] = 0
            else:
                # device chain is not empty and "current device" isn't the only device
                self.t_d_count[self.t_current] -= rack_devices_deleted

            assert new_device_count_track == self.t_d_count[self.t_current]
            decremented_device_count_track = self.t_d_count[self.t_current]
            self.t_d_current[self.t_current] = deleted_device_index
            max_needed_device_banks = int(math.ceil(decremented_device_count_track // SETUP_DB_DEVICE_BANK_SIZE))
            if SETUP_DB_MAX_DEVICE_BANKS > max_needed_device_banks:
                self.t_d_bank_count[self.t_current] = max_needed_device_banks
            else:
                self.t_d_bank_count[self.t_current] = SETUP_DB_MAX_DEVICE_BANKS

        elif selected_device_was_changed:
            # self.main_script().log_message("{0}selected_device_was_changed: for 'change' device event handling".format(log_id))

            self.t_d_current[self.t_current] = changed_device_index
            assert new_device_count_track == self.t_d_count[self.t_current]

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
        
        