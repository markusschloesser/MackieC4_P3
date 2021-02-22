# Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/EncoderController.py
# Compiled at: 2011-01-22 05:02:32
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals  #MS
from __future__ import division
from past.utils import old_div
from builtins import range
from . consts import *
from . MackieC4Component import *
from _Generic.Devices import *
import math, time


class EncoderController(MackieC4Component):
    """
     Controls all encoders of the Mackie C4pro controller extension
  """
    __module__ = __name__

    def __init__(self, main_script, encoders):
        # suspect MackieC4Component exists because MackieC4 and EncoderController share some method_names.
        # MackieC4Component means EncoderController doesn't need to use super-class-shared-method-name
        # method calling semantics. Functions in MackieC4Component all delegate to functions in MackieC4,
        # known as main_script here
        MackieC4Component.__init__(self, main_script)

        self.__own_encoders = encoders  # why separate references? This reference is only used here in __init__
        self.__encoders = encoders  # why these __encoders too? This reference is used everywhere else
        # suspect the reason is because, at runtime, while this __init__ is running; the main_script here,
        # the caller, MackieC4, is still inside its own __init__ (and thus can't be referenced successfully yet?)
        # The encoders here though, are fully initialized and are successfully referenced

        # tell these encoders my self is now your controller
        for s in self.__own_encoders:
            s.set_encoder_controller(self)

        self.__assignment_mode = C4M_CHANNEL_STRIP
        self.__last_assignment_mode = C4M_USER
        self.__current_track_name = ''  # Live's Track Name of selected track
        self.t_count = 0    # nbr of regular tracks
        self.t_r_count = 0  # nbr of return tracks
        self.t_current = 0  # index of current selected track
        self.selected_track = None  # Live's selected-Track Object?

        # track device count -- the count of devices loaded on the t_current track
        # see device_counter(self, t, d):
        self.t_d_count = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]

        # track device current -- the index of the currently selected device indexed by the t_current track
        self.t_d_current = [0 for i in range(SETUP_DB_DEFAULT_SIZE)]

        # t_d bank count -- the count of the devices on the t_current track (in banks of 8 parameters)
        # see device_counter(self, t, d): (at the same index) the same number as t_d_count but divided by 8
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

        self.__ordered_plugin_parameters = []  # Live objects?
        self.__chosen_plugin = None  # Live's selected

        # a list of 32 tuples representing 'what text to display' on the LCD screen above each encoder
        # where slot 0 of each tuple contains the bottom row text
        # and slot 1 contain the top row text
        self.__display_parameters = [[] for x in range(NUM_ENCODERS)]

        # __display_repeat_timer is a work-around for when the C4 LCD display changes due to a MIDI sysex message
        # received by the C4 from somewhere else, not-here.  Such a display change is not tracked here (obviously),
        # and the C4 itself can't be asked "what are you displaying right now?". So we just blast the display sysex
        # from here about every 5 seconds to overwrite any possible "other change".  (each LCD is "refreshed" in turn
        # each time this timer "pops" (every 4th pop per LCD))
        self.__display_repeat_timer = LCD_DISPLAY_UPDATE_REPEAT_MULTIPLIER * 5
        self.__display_repeat_count = 0

        self.__master_track_index = 0
        self.__filter_mst_trk = 0
        self.__filter_mst_trk_allow_audio = 0
        tracks = self.song().visible_tracks + self.song().return_tracks
        selected_track = self.song().view.selected_track
        self.returns_switch = 0
        index = 0
        found = 0
        for track in tracks:
            index = index + 1
            if track == selected_track:
                self.t_current = index - 1
                found = 1

        if found == 0:
            self.t_current = index

        self.selected_track = self.song().view.selected_track
        self.update_assignment_mode_leds()
        self.__last_send_messages1 = {LCD_ANGLED_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        self.__last_send_messages2 = {LCD_TOP_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        self.__last_send_messages3 = {LCD_MDL_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        self.__last_send_messages4 = {LCD_BTM_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        return

    # function provided by MackieC4Component super #MS reversed to Leighs version, Sissy had delegated destroy to Super
    def destroy(self):
    #     self.destroy()
        MackieC4Component.destroy(self)

    # function provided by MackieC4Component super #MS reversed to Leighs version, Sissy had delegated destroy to Super
    def request_rebuild_midi_map(self):
        self._MackieC4Component__main_script.request_rebuild_midi_map()
    #     self.
    #     self.main_script.request_rebuild_midi_map(self)
    #     self._MackieC4Component.request_rebuild_midi_map(self)

    def reset_device_counter(self):
        self.t_d_count = []
        self.t_d_bank_count = []

    def device_counter(self, t, d):
        self.t_d_count[t] = d
        self.t_d_bank_count[t] = int(d / SETUP_DB_DEVICE_BANK_SIZE)  # no ceiling call?

    def build_setup_database(self):
        self.t_count = 0

        tracks_in_song = self.song().tracks
        for i1 in range(len(tracks_in_song)):
            devices_on_track = tracks_in_song[i1].devices
            self.t_d_count[i1] = len(devices_on_track)
            self.t_d_bank_count[i1] = math.ceil(len(devices_on_track) / SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_current[i1] = 0
            self.t_d_current[i1] = 0
            for j in range(len(devices_on_track)):
                params_of_devices_on_trk = devices_on_track[j].parameters
                self.t_d_p_count[i1][j] = len(params_of_devices_on_trk)
                self.t_d_p_bank_count[i1][j] = math.ceil(len(params_of_devices_on_trk) / SETUP_DB_PARAM_BANK_SIZE)
                self.t_d_p_bank_current[i1][j] = 0

            self.t_count += 1

        nbr_nrml_trks = i1  # assert nbr_nrml_trks == self.t_count
        for i2 in range(len(self.song().return_tracks)):
            devices_on_rtn_track = self.song().return_tracks[i2].devices
            device_index = nbr_nrml_trks + i2 + 1
            self.t_d_count[device_index] = len(devices_on_rtn_track)
            self.t_d_bank_count[device_index] = math.ceil(len(devices_on_rtn_track) / SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_current[device_index] = 0
            self.t_d_current[device_index] = 0
            for j in range(len(devices_on_rtn_track)):
                params_of_devices_on_rtn_trk = devices_on_rtn_track[j].parameters
                self.t_d_p_count[device_index][j] = len(params_of_devices_on_rtn_trk)
                sum_nbr = math.ceil(len(params_of_devices_on_rtn_trk) / SETUP_DB_PARAM_BANK_SIZE)
                self.t_d_p_bank_count[device_index][j] = sum_nbr
                self.t_d_p_bank_current[device_index][j] = 0

            self.t_count += 1
            self.t_r_count += 1

        nbr_nrml_and_rtn_trks = device_index  # assert nbr_nrml_and_rtn_trks == self.t_count
        self.__master_track_index = nbr_nrml_and_rtn_trks + 1
        lmti = self.__master_track_index
        devices_on_mstr_track = self.song().master_track.devices
        self.t_d_count[lmti] = len(devices_on_mstr_track)
        self.t_d_bank_count[lmti] = math.ceil(len(devices_on_mstr_track) / SETUP_DB_DEVICE_BANK_SIZE)
        self.t_d_bank_current[lmti] = 0
        self.t_d_current[lmti] = 0
        for j in range(len(devices_on_mstr_track)):
            params_of_devices_on_rtn_trk = devices_on_mstr_track[j].parameters
            self.t_d_p_count[lmti][j] = len(params_of_devices_on_rtn_trk)
            self.t_d_p_bank_count[lmti][j] = math.ceil(len(params_of_devices_on_rtn_trk) / SETUP_DB_PARAM_BANK_SIZE)
            self.t_d_p_bank_current[lmti][j] = 0

        devices_on_selected_trk = self.song().view.selected_track.devices
        if len(devices_on_selected_trk) == 0:
            self.__chosen_plugin = None
        else:
            self.__chosen_plugin = devices_on_selected_trk[0]
            self.song().view.select_device(devices_on_selected_trk[0])

        self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)  # MS for_display_only=False is new! Seems ok
        self.request_rebuild_midi_map()
        return

    def master_track_index(self):
        return self.__master_track_index

    def track_changed(self, track_index):
        self.selected_track = self.song().view.selected_track
        self.t_current = track_index
        if len(self.selected_track.devices) == 0:
            self.__chosen_plugin = None
            self.__reorder_parameters()
        else:
            self.__chosen_plugin = self.selected_track.devices[self.t_d_current[self.t_current]]
            self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)  # MS for_display_only=False is new! Seems ok
        self.request_rebuild_midi_map()
        return

    def track_added(self, track_index):
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
        self.selected_track = self.song().view.selected_track
        self.t_count += 1
        devices_on_selected_track = self.selected_track.devices
        self.t_d_count[track_index] = len(devices_on_selected_track)
        self.t_d_current[track_index] = 0
        self.t_d_bank_count[track_index] = math.ceil(len(devices_on_selected_track) / SETUP_DB_DEVICE_BANK_SIZE)
        self.t_d_bank_current[track_index] = 0
        for d in range(len(devices_on_selected_track)):
            parms_of_devs_on_trk = devices_on_selected_track[d].parameters
            self.t_d_p_count[track_index][d] = len(parms_of_devs_on_trk)
            self.t_d_p_bank_count[track_index][d] = math.ceil(len(parms_of_devs_on_trk) / SETUP_DB_PARAM_BANK_SIZE)
            self.t_d_p_bank_current[track_index][d] = 0

        # self.refresh_state() #MS out-commented, copy from Leigh on next line
        self._MackieC4Component__main_script.refresh_state()
        if self.t_d_count[track_index] == 0:
            self.__chosen_plugin = None
            self.__reorder_parameters()
        else:
            selected_device = self.selected_track.devices[0]
            self.__chosen_plugin = selected_device
            self.song().view.select_device(selected_device)
            self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()
        return

    def track_deleted(self, track_index):
        # suspect this breaks if the only normal or return track is deleted,
        # the master-track becomes the only track "tracked here", and then
        # fun would ensue elsewhere such as in __reassign_encoder_parameters() or request_rebuild_midi_map()
        # because of 0 regular or return tracks in the song
        for t in range(self.t_current + 1, self.t_count, 1):
            for d in range(self.t_d_count[t]):
                self.t_d_p_count[(t - 1)][d] = self.t_d_p_count[t][d]
                self.t_d_p_bank_count[(t - 1)][d] = self.t_d_p_bank_count[t][d]
                self.t_d_p_bank_current[(t - 1)][d] = self.t_d_p_bank_current[t][d]

            self.t_d_count[t - 1] = self.t_d_count[t]
            self.t_d_current[t - 1] = self.t_d_current[t]
            self.t_d_bank_count[t - 1] = self.t_d_bank_count[t]
            self.t_d_bank_current[t - 1] = self.t_d_bank_current[t]

        self.selected_track = self.song().view.selected_track
        self.t_count -= 1
        self.refresh_state()  # MS potentially copy from leigh over as above
        if len(self.selected_track.devices) == 0:
            self.__chosen_plugin = None
            self.__reorder_parameters()
        else:
            selected_device = self.selected_track.devices[self.t_d_current[self.t_current]]
            self.__chosen_plugin = selected_device
            self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)  # MS things in bracket from leigh, seems ok
        self.request_rebuild_midi_map()
        return

    def device_added_deleted_or_changed(self):  # MS this is where things currently break when device delete line 358

        device_count_track = self.t_d_count[self.t_current]
        device_was_added = len(self.selected_track.devices) > device_count_track
        device_was_removed = len(self.selected_track.devices) < device_count_track

        index = 0
        new_device_index = 0
        deleted_device_index = 0
        changed_device_index = 0
        for device in self.selected_track.devices:
            if self.selected_track.view.selected_device == device:
                new_device_index = index
                deleted_device_index = index
                changed_device_index = index
            else:
                index += 1

        if device_was_added:
            param_count_track = self.t_d_p_count[self.t_current]
            param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            param_bank_current_track = self.t_d_p_bank_current[self.t_current]
            for d in range(device_count_track, new_device_index + 1, -1):
                c = d - 1
                param_count_track[d] = param_count_track[c]
                param_bank_count_track[d] = param_bank_count_track[c]
                param_bank_current_track[d] = param_bank_current_track[c]

            param_count_track[new_device_index] = len(self.selected_track.devices[new_device_index].parameters)
            sum_nbr = math.ceil(param_count_track[new_device_index] / SETUP_DB_PARAM_BANK_SIZE)
            param_bank_count_track[new_device_index] = sum_nbr
            param_bank_current_track[new_device_index] = 0

            self.t_d_count[self.t_current] += 1
            device_count_track = self.t_d_count[self.t_current]

            self.t_d_current[self.t_current] = new_device_index
            self.t_d_bank_count[self.t_current] = math.ceil(device_count_track / SETUP_DB_DEVICE_BANK_SIZE)
            self.t_d_bank_current[self.t_current] = math.ceil((device_count_track + 1) / SETUP_DB_DEVICE_BANK_SIZE)
            self.__chosen_plugin = self.selected_track.devices[new_device_index]
            self.__reorder_parameters()
            self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket from Leigh, seems ok
            self.request_rebuild_midi_map()
        elif device_was_removed:  # MS this is  where things currently really break when last device delete
            param_count_track = self.t_d_p_count[self.t_current]
            param_bank_count_track = self.t_d_p_bank_count[self.t_current]
            param_bank_current_track = self.t_d_p_bank_current[self.t_current]
            for d in range(deleted_device_index + 1, device_count_track, 1):
                c = d - 1
                param_count_track[d] = param_count_track[c]
                param_bank_count_track[d] = param_bank_count_track[c]
                param_bank_current_track[d] = param_bank_current_track[c]

            if deleted_device_index == device_count_track - 1:
                self.t_d_current[self.t_current] -= 1
            else:
                self.t_d_current[self.t_current] = deleted_device_index
                sum_nbr = math.ceil((self.t_d_current[self.t_current] + 1) / SETUP_DB_DEVICE_BANK_SIZE)
                self.t_d_bank_current[self.t_current] = sum_nbr

            self.t_d_count[self.t_current] -= 1
            self.t_d_bank_count[self.t_current] = math.ceil(self.t_d_count[self.t_current] / SETUP_DB_DEVICE_BANK_SIZE)
            self.__chosen_plugin = self.selected_track.devices[deleted_device_index]  # MS this produces an Index error?
            self.__reorder_parameters()
            self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket from Leigh, seems ok
            self.request_rebuild_midi_map()
        else:  # selected device changed
            self.__chosen_plugin = self.selected_track.devices[changed_device_index]
            self.__reorder_parameters()
            self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket entry new from Leigh, works
            self.request_rebuild_midi_map()

    def assignment_mode(self):
        return self.__assignment_mode

    def last_assignment_mode(self):
        return self.__last_assignment_mode

    # no wrap around:
    # stop moving left at track 0,
    # stop moving right at master track
    def handle_bank_switch_ids(self, switch_id):
        """ works in all modes """
        current_bank_nbr = self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]]
        update_self = False
        if switch_id == C4SID_BANK_LEFT:
            if current_bank_nbr > 0:
                current_bank_nbr -= 1
                update_self = True
        elif switch_id == C4SID_BANK_RIGHT:
            max_bank_nbr = self.t_d_p_bank_count[self.t_current][self.t_d_current[self.t_current]] - 1
            if current_bank_nbr < max_bank_nbr:
                current_bank_nbr += 1
                update_self = True

        if update_self:
            self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]] = current_bank_nbr
            self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket entry new from Leigh, works
            self.request_rebuild_midi_map()

    def handle_assignment_switch_ids(self, switch_id):

        # C4 assignment.marker button == C4M_USER mode
        update_self = False
        if switch_id == C4SID_MARKER:

            # self.__last_assignment_mode = self.__assignment_mode != C4M_USER and self.__assignment_mode
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_MARKER]:  # C4M_USER:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_MARKER]  # C4M_USER
                update_self = True

        # C4 assignment.track button == C4M_PLUGINS mode
        elif switch_id == C4SID_TRACK:
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_TRACK]:  # C4M_PLUGINS:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_TRACK]  # C4M_PLUGINS

                # **  If the local "db" says the index of the current device is 0,
                # ** And the local "db" says the count of devices is not 0
                # ** force the first device on the track to be
                # ** the selected device in Live?
                # self.t_d_current[self.t_current] == 0 and self.t_d_count[self.t_current] != 0 and
                # self.song().view.select_device(self.selected_track.devices[0])
                if self.t_d_current[self.t_current] == 0 and self.t_d_count[self.t_current] != 0:
                    self.song().view.select_device(self.selected_track.devices[0])
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
            self.update_assignment_mode_leds()
            self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket entry new from Leigh, works
            self.request_rebuild_midi_map()
        # else don't update because nothing changed here

    def handle_slot_nav_switch_ids(self, switch_id):
        """ "slot navigation" only functions if the current mode is C4M_PLUGINS """
        if self.__assignment_mode == button_id_to_assignment_mode[C4SID_TRACK]:  # C4M_PLUGINS:
            current_trk_device_index = self.t_d_current[self.t_current]
            max_trk_device_index = self.t_d_count[self.t_current] - 1
            update_self = False
            if switch_id == C4SID_SLOT_UP:
                if current_trk_device_index > 0:
                    current_trk_device_index -= 1
                    update_self = True
            elif switch_id == C4SID_SLOT_DOWN:
                if current_trk_device_index < max_trk_device_index:
                    current_trk_device_index += 1
                    update_self = True

            if update_self:
                self.t_d_current[self.t_current] = current_trk_device_index
                current_selected_device = self.selected_track.devices[current_trk_device_index]
                self.song().view.select_device(current_selected_device)
                self.__chosen_plugin = current_selected_device
                self.__reorder_parameters()
                self.__reassign_encoder_parameters(for_display_only=False)  # MS for_display_only=False is new! Seems ok
                self.request_rebuild_midi_map()

    def update_assignment_mode_leds(self):
        """
          Make C4 device turn off the button LED of the button associated with the last assignment mode
          Make C4 device turn  on the button LED of the button associated with the current assignment mode
        """
        # sends for example (90, 08, 00, channel)  channel value provided by Live?, if any
        self.send_midi((NOTE_ON_STATUS, assignment_mode_to_button_id[self.__last_assignment_mode], BUTTON_STATE_OFF))
        # sends for example (90, 05, 7F, channel)
        self.send_midi((NOTE_ON_STATUS, assignment_mode_to_button_id[self.__assignment_mode], BUTTON_STATE_ON))

    def handle_vpot_rotation(self, vpot_index, cc_value):
        """ "vpot rotation" only functions if the current mode is C4M_CHANNEL_STRIP """
        # coming from the C4 these midi messages look like: B0  20  01  1
        # or B0  21  01  1  where vpot_index here would be 00 or 01 (after subtracting 0x20 from 0x20 or 0x21),
        # and cc_value would be 01 in both examples but could be any value 01 - 0x7F,
        # However in here (because coming from the C4) if cc_value is in the
        # range 01 - 0F, the encoder is being turned clockwise, and if cc_value is in the
        # range 41 - 4F, the encoder is being turned counter-clockwise
        # the higher the value, the faster the knob is turning, so theoretically 16 steps of "knob twisting speed"
        # in either direction
        #
        # suspect this is because other encoder rotation messages are "midi mapped" through Live with feedback
        # i.e. when you rotate encoder 32 in C4M_CHANNEL_STRIP mode, the "level number" updates itself via the
        # midi mapping through Live (see Encoders.build_midi_map()), not via code here
        is_not_master_track_selected = self.selected_track != self.song().master_track
        is_armable_track_selected = self.selected_track.can_be_armed
        self.main_script().log_message("potIndex<{}> cc_value<{}> received".format(vpot_index, cc_value))
        if self.__assignment_mode == C4M_CHANNEL_STRIP:
            # encoder = self.__encoders[vpot_index]
            encoder_29_index = 28
            encoder_30_index = 29
            if vpot_index == encoder_29_index:  #
                for s in self.__encoders:
                    is_correct_index = s.vpot_index() == encoder_29_index
                    if is_correct_index and is_not_master_track_selected:  # and cc_value >= 0x44:
                        if is_armable_track_selected:
                            if cc_value in encoder_cw_values:  # if cc_value is in the range 01 - 0F
                                self.main_script().log_message("arming track")
                                self.selected_track.arm = True
                                s.show_full_enlighted_poti()
                            elif cc_value in encoder_ccw_values:  # if cc_value is in the range 41 - 4F
                                self.main_script().log_message("disarming track")
                                self.selected_track.arm = False
                                s.unlight_vpot_leds()
            elif vpot_index == encoder_30_index:
                for s in self.__encoders:
                    is_correct_index = s.vpot_index() == encoder_30_index
                    if is_correct_index and is_not_master_track_selected:  # and cc_value >= 0x44:
                        if cc_value in encoder_cw_values:  # if cc_value is in the range 01 - 0F
                            self.main_script().log_message("muting track")
                            self.selected_track.mute = True
                            s.show_full_enlighted_poti()
                        elif cc_value in encoder_ccw_values:  # if cc_value is in the range 41 - 4F
                            self.main_script().log_message("un-muting track")
                            self.selected_track.mute = False
                            s.unlight_vpot_leds()

    def handle_pressed_v_pot(self, vpot_index):
        """ 'encoder button' clicks are not handled in C4M_USER assignment mode  """
        encoder_index = vpot_index - C4SID_VPOT_PUSH_BASE  # 0x20  32
        selected_device_bank_index = self.t_d_bank_current[self.t_current]
        max_device_bank_index = self.t_d_bank_count[self.t_current] - 1
        if self.__assignment_mode == C4M_CHANNEL_STRIP:
            if encoder_index in row_00_encoders:
                encoder_07_index = 6
                encoder_08_index = 7
                update_self = False
                if encoder_index == encoder_07_index:
                    if selected_device_bank_index > 0:
                        selected_device_bank_index -= 1
                        # update_self = True #MS this was from sissy, next line from Leigh, maybe swap again? try!
                        self.__reassign_encoder_parameters(for_display_only=False)
                elif encoder_index == encoder_08_index:
                    if selected_device_bank_index < max_device_bank_index:
                        selected_device_bank_index += 1
                        update_self = True

                if update_self:
                    self.t_d_bank_current[self.t_current] = selected_device_bank_index
                    self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket from Leigh, seems to work
            elif encoder_index in row_01_encoders:

                # automatically switch to Track/Plugins mode
                self.handle_assignment_switch_ids(C4SID_TRACK)

                device_bank_offset = int(NUM_ENCODERS_ONE_ROW * selected_device_bank_index)
                device_offset = vpot_index - C4SID_VPOT_PUSH_BASE - NUM_ENCODERS_ONE_ROW + device_bank_offset
                self.__chosen_plugin = self.selected_track.devices[device_offset]
                self.__reorder_parameters()
                self.t_d_current[self.t_current] = encoder_index - NUM_ENCODERS_ONE_ROW + device_bank_offset
                self.song().view.select_device(self.selected_track.devices[device_offset])
                self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket from Leigh, seems to work
                self.request_rebuild_midi_map()
            elif encoder_index in row_02_encoders:
                param = self.__filter_mst_trk_allow_audio and self.__encoders[encoder_index].v_pot_parameter()
                param.value = param.default_value
            elif encoder_index in row_03_encoders:
                encode_29_index = 28  # 28th index is the 29th element
                encode_30_index = 29  # 29th index is the 30th element
                if encoder_index < encode_29_index:
                    param = self.__filter_mst_trk_allow_audio and self.__encoders[encoder_index].v_pot_parameter()
                    param.value = param.default_value
                elif encoder_index == encode_29_index:
                    if self.__filter_mst_trk:
                        if self.selected_track.can_be_armed:
                            if self.selected_track.arm is not True:
                                self.selected_track.arm = True
                                turn_on_encoder_led_msg = (CC_STATUS, C4SID_VPOT_PUSH_29, 0x43)  # any value 40 - 4F?
                                self.send_midi(turn_on_encoder_led_msg)
                            else:
                                self.selected_track.arm = False
                                turn_off_encoder_led_msg = (CC_STATUS, C4SID_VPOT_PUSH_29, 0x06)  # any value 00 - 0F?
                                self.send_midi(turn_off_encoder_led_msg)
                        # else the selected track can't be armed
                elif encoder_index == encode_30_index:
                    if self.__filter_mst_trk:
                        if self.selected_track.mute:
                            self.selected_track.mute = False
                            turn_off_encoder_led_msg = (CC_STATUS, C4SID_VPOT_PUSH_30, 0x06)
                            self.send_midi(turn_off_encoder_led_msg)
                        else:
                            self.selected_track.mute = True
                            turn_on_encoder_led_msg = (CC_STATUS, C4SID_VPOT_PUSH_30, 0x43)
                            self.send_midi(turn_on_encoder_led_msg)
                elif encoder_index > encode_30_index:
                    param = self.__encoders[encoder_index].v_pot_parameter()
                    param.value = param.default_value

        elif self.__assignment_mode == C4M_PLUGINS:
            encoder_07_index = 6
            encoder_08_index = 7
            current_device_track = self.t_d_current[self.t_current]
            current_parameter_bank_track = self.t_d_p_bank_current[self.t_current]
            stop = len(self.__display_parameters) + SETUP_DB_DEVICE_BANK_SIZE
            display_params_range = range(SETUP_DB_DEVICE_BANK_SIZE, stop)
            update_self = False
            if encoder_index == encoder_07_index:
                if current_parameter_bank_track[current_device_track] > 0:
                    current_parameter_bank_track[current_device_track] -= 1
                    update_self = True
            elif encoder_index == encoder_08_index:
                current_track_device_preset_bank = current_parameter_bank_track[current_device_track]
                track_device_preset_bank_count = self.t_d_p_bank_count[self.t_current][current_device_track]
                if  current_track_device_preset_bank < track_device_preset_bank_count - 1:
                    current_parameter_bank_track[current_device_track] += 1
                    update_self = True
            elif encoder_index in display_params_range:  # row_01_encoders
                param = self.__encoders[encoder_index].v_pot_parameter()
                try:
                    param.value = param.default_value
                except (RuntimeError, AttributeError):
                    # There is no default value available for this type of parameter
                    # 'NoneType' object has no attribute 'default_value'
                    pass

            if update_self:
                self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket new, this replaces to instances from sissy
                self.request_rebuild_midi_map()

        elif self.__assignment_mode == C4M_FUNCTION:
            encoder_25_index = 24
            encoder_26_index = 25
            if encoder_index == encoder_25_index:
                self.song().stop_playing()
                turn_off_encoder_led_msg = (CC_STATUS, C4SID_VPOT_PUSH_26, 0x06)
                self.send_midi(turn_off_encoder_led_msg)
            if encoder_index == encoder_26_index:
                self.song().start_playing()
                turn_on_encoder_led_msg = (CC_STATUS, C4SID_VPOT_PUSH_26, 0x43)
                self.send_midi(turn_on_encoder_led_msg)

    def __send_parameter(self, vpot_index):
        """ Returns the send parameter that is assigned to the given encoder as a tuple (param, param.name) """
        if vpot_index < len(self.selected_track.mixer_device.sends):
            p = self.selected_track.mixer_device.sends[vpot_index]
            self.main_script().log_message("Param name <{0}>".format(p.name))
            return p, p.name
        else:
            return None, 'None'

    def __plugin_parameter(self, vpot_index):
        """ Return the plugin parameter that is assigned to the given encoder as a tuple (param, param.name)
    """
        parameters = self.__ordered_plugin_parameters
        if vpot_index in encoder_range:
            current_track_device_preset_bank = self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]]
            preset_bank_index = current_track_device_preset_bank * SETUP_DB_PARAM_BANK_SIZE
            is_param_index = len(parameters) > vpot_index + preset_bank_index
            if is_param_index:
                p = parameters[vpot_index + preset_bank_index]
                try:
                    self.main_script().log_message("Param {0} name <{1}>".format(vpot_index, p.name))
                except AttributeError:  # 'tuple' object has no attribute 'name'
                    self.main_script().log_message("Param {0} tuple name <{1}>".format(vpot_index, p[1]))
                return p

        return None, 'None'

    def __on_parameter_list_of_chosen_plugin_changed(self):
        assert self.__chosen_plugin is not None
        self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)  # MS bracket from leigh, seems to work
        self.request_rebuild_midi_map()
        return

    def __reorder_parameters(self):
        result = []
        if self.__chosen_plugin:

            # if a default Live device is chosen, iterate the DEVICE_DICT constant
            # to reorder the local list of plugin parameters
            if self.__chosen_plugin.class_name in DEVICE_DICT.keys(): #MS should we import device dict from generic devices or Live?
                device_banks = DEVICE_DICT[self.__chosen_plugin.class_name]
                for bank in device_banks:
                    for param_name in bank:
                        parameter_name = ''
                        parameter = get_parameter_by_name(self.__chosen_plugin, param_name)
                        if parameter:
                            parameter_name = parameter.name
                        else:
                            parameter = ''
                        result.append((parameter, parameter_name))

            # otherwise reorder the local list to the order provided by the parameter itself
            else:
                result = [(p, p.name) for p in self.__chosen_plugin.parameters]

        self.__ordered_plugin_parameters = result
        count = 0
        for p in self.__ordered_plugin_parameters:
            self.main_script().log_message("Param {0} name <{1}>".format(count, p[1]))
            count += 1

    def __reassign_encoder_parameters(self, for_display_only):  # MS "=False" after display only removed
        """ Reevaluate all v-pot parameter assignments """
        self.__filter_mst_trk = 0
        self.__filter_mst_trk_allow_audio = 0
        self.__current_track_name = self.selected_track.name
        if self.selected_track != self.song().master_track:
            self.__filter_mst_trk = 1  # a regular track is selected (not master track)
            if self.selected_track.has_audio_output:
                self.__filter_mst_trk_allow_audio = 1  # a regular track with audio is selected (not master)

        self.__display_parameters = []
        encoder_07_index = 6
        encoder_08_index = 7
        encoder_25_index = 24
        encoder_26_index = 25
        encoder_29_index = 28
        encoder_30_index = 29
        encoder_31_index = 30
        encoder_32_index  = 31
        if self.__assignment_mode == C4M_CHANNEL_STRIP:
            current_device_bank_track = self.t_d_bank_current[self.t_current]
            max_device_bank_track = self.t_d_bank_count[self.t_current]

            for s in self.__encoders:
                vpot_display_text = ('      ', '      ')
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                s_index = s.vpot_index()
                if s_index in row_00_encoders:
                    # if s_index < encoder_07_index:
                    #     always fill the __displayParameters list
                    if s_index == encoder_07_index:
                        if current_device_bank_track > 0:
                            vpot_display_text = ('<<Bank', 'Device')
                            s.show_full_enlighted_poti()
                        else:
                            s.unlight_vpot_leds()
                    elif s_index == encoder_08_index:
                        if current_device_bank_track < max_device_bank_track - 1:
                            vpot_display_text = ('Bank>>', 'Device')
                            s.show_full_enlighted_poti()
                        else:
                            s.unlight_vpot_leds()
                    self.__display_parameters.append(vpot_display_text)
                elif s_index in row_01_encoders:
                    count = s_index - SETUP_DB_DEVICE_BANK_SIZE
                    current_encoder_offset = current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE
                    if count + current_encoder_offset < self.t_d_count[self.t_current]:
                        s.show_full_enlighted_poti()
                        device_name = self.selected_track.devices[(count + int(current_encoder_offset))].name
                        vpot_display_text = (device_name, '')  # device_name in bottom row, blanks on top
                    else:
                        s.unlight_vpot_leds()

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index < encoder_29_index:
                    if self.__filter_mst_trk_allow_audio:
                        send_param = self.__send_parameter(s_index - SETUP_DB_DEVICE_BANK_SIZE * 2)
                        vpot_param = (send_param[0], VPOT_DISPLAY_WRAP)
                        format_nbr = s_index % NUM_ENCODERS_ONE_ROW
                        if s_index in row_03_encoders:
                            format_nbr += NUM_ENCODERS_ONE_ROW
                        # encoder 17 index is (16 % 8) = send 0
                        # encoder 25 index is (24 % 8) = send 8
                        vpot_display_text = (send_param[1], 'send{0}'.format(format_nbr))
                    # else:
                    #     vpot_display_text = ('      ', '      ')
                    #     vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                    #
                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_29_index:
                    self.returns_switch = 0
                    if self.__filter_mst_trk:
                        vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                        if self.selected_track.can_be_armed:
                            if self.selected_track.arm:
                                s.show_full_enlighted_poti()
                                vpot_display_text = (' Off   ', 'RecArm ')
                            else:
                                s.unlight_vpot_leds()
                                vpot_display_text = ('  ON   ', 'RecArm ')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_30_index:
                    vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                    if self.__filter_mst_trk:

                        if self.selected_track.mute:
                            s.show_full_enlighted_poti()
                            vpot_display_text = (' Off  ', ' Mute ')
                        else:
                            s.unlight_vpot_leds()
                            vpot_display_text = (' On   ', ' Mute ')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_31_index:
                    if self.selected_track.has_audio_output:
                        vpot_display_text = (self.selected_track.mixer_device.panning, 'Pan')  # ( value, value label)
                        vpot_param = (self.selected_track.mixer_device.panning, VPOT_DISPLAY_BOOST_CUT)
                    else:
                        vpot_display_text = ('', '')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_32_index:
                    if self.selected_track.has_audio_output:
                        vpot_display_text = (self.selected_track.mixer_device.volume, 'Volume')  # ( value, value label)
                        vpot_param = (self.selected_track.mixer_device.volume, VPOT_DISPLAY_WRAP)
                    else:
                        vpot_display_text = ('', '')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_PLUGINS:
            current_device_bank_param_track = self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]]
            max_device_bank_param_track = self.t_d_p_bank_count[self.t_current][self.t_d_current[self.t_current]]
            for s in self.__encoders:
                vpot_display_text = ('      ', '      ')
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                s_index = s.vpot_index()
                # if s_index < encoder_07_index:

                # always fill the __displayParameters list
                if s_index == encoder_07_index:
                    if self.__chosen_plugin is None:
                        s.unlight_vpot_leds()
                    elif current_device_bank_param_track > 0:
                        vpot_display_text = ('<<  - ', 'PrvBnk')
                        s.show_full_enlighted_poti()
                    else:
                        s.unlight_vpot_leds()
                elif s_index == encoder_08_index:
                    if self.__chosen_plugin is None:
                        s.unlight_vpot_leds()
                    elif current_device_bank_param_track < max_device_bank_param_track - 1:
                        vpot_display_text = ('  + >>', 'NxtBnk')
                        s.show_full_enlighted_poti()
                    else:
                        s.unlight_vpot_leds()
                else:
                    plugin_param = self.__plugin_parameter(s_index - SETUP_DB_DEVICE_BANK_SIZE)
                    vpot_param = (plugin_param[0], VPOT_DISPLAY_WRAP)
                    vpot_display_text = (plugin_param[1], '')  # parameter name in bottom display row, blank on top
                    # s.set_v_pot_parameter(vpot_param[0], vpot_param[1])

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_FUNCTION:
            for s in self.__encoders:
                vpot_display_text = ('      ', '      ')
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                if s.vpot_index() == encoder_26_index:
                    vpot_param = (None, VPOT_DISPLAY_WRAP)
                    if self.song().is_playing:
                        vpot_display_text = (' Play ', ' Song ')
                        s.show_full_enlighted_poti()
                    else:
                        vpot_display_text = (' Stop ', ' Song ')
                        s.unlight_vpot_leds()

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_USER:
            for s in self.__encoders:
                # vpot_display_text = ('      ', '      ')
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                s_index = s.vpot_index()
                if s_index == row_00_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 0'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text = (bottom_line, top_line)
                elif s_index == row_01_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 1'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text = (bottom_line, top_line)
                elif s_index == row_02_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 2'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text = (bottom_line, top_line)
                else:  # if s_index == row_03_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 3'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text = (bottom_line, top_line)
                    update_self = True

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        return

    def on_update_display_timer(self):
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
        self.__display_repeat_count += 1

        encoder_29_index = 28
        encoder_30_index = 29
        encoder_31_index = 30
        encoder_32_index = 31
        if self.__assignment_mode == C4M_CHANNEL_STRIP:
            upper_string1 += '-------Track--------                      '
            upper_string2 += '------------------------Devices------------------------'
            lower_string1 += self.__transform_to_size(str(self.selected_track.name), 20)
            lower_string1 = lower_string1.center(20)
            lower_string1 += '                      '
            for t in encoder_range:

                text_for_display = self.__display_parameters[t]
                u_alt_text = ' '
                l_alt_text = ' '
                if len(text_for_display) > 1:
                    u_alt_text = text_for_display[1]
                    l_alt_text = text_for_display[0]
                elif len(text_for_display) > 0:
                    l_alt_text = text_for_display[0]

                if t in range(6, NUM_ENCODERS_ONE_ROW):
                    upper_string1 += self.__transform_to_size(u_alt_text, 6)
                    upper_string1 += ' '
                    lower_string1 += self.__transform_to_size(str(l_alt_text), 6)
                    lower_string1 += ' '
                elif t in row_01_encoders:
                    lower_string2 += self.__transform_to_size(str(l_alt_text), 6)
                    lower_string2 += ' '
                elif t in row_02_encoders:
                    lower_string3 += self.__transform_to_size(str(l_alt_text), 6)
                    lower_string3 += ' '
                    upper_string3 += self.__transform_to_size(u_alt_text, 6)
                    upper_string3 += ' '
                elif t in row_03_encoders:
                    if t < encoder_29_index:
                        lower_string4 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string4 += ' '
                        upper_string4 += self.__transform_to_size(u_alt_text, 6)
                        upper_string4 += ' '
                    elif t == encoder_29_index:
                        if self.selected_track.can_be_armed:
                            if self.selected_track.arm:
                                lower_string4 += '  ON   '
                            else:
                                lower_string4 += ' Off   '
                            upper_string4 += 'RecArm '
                        else:
                            lower_string4 += '       '
                            upper_string4 += '       '
                    elif t == encoder_30_index:
                        if self.__filter_mst_trk:
                            if self.selected_track.mute:
                                lower_string4 += '  ON   '
                                upper_string4 += ' MUTE  '
                            else:
                                lower_string4 += ' Off   '
                                upper_string4 += ' Mute  '
                        else:
                            lower_string4 += '       '
                            upper_string4 += '       '
                    elif t == encoder_31_index:
                        lower_string4 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string4 += ' '
                        if self.selected_track.has_audio_output:
                            upper_string4 += ' Pan   '
                        else:
                            upper_string4 += '       '
                    elif t == encoder_32_index:
                        lower_string4 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string4 += ' '
                        if self.selected_track.has_audio_output:
                            upper_string4 += 'Volume '
                        else:
                            upper_string4 += '       '

        so_many_spaces = '                                                       '
        if self.__assignment_mode == C4M_PLUGINS:
            upper_string1 += '-------Track-------- -----Device '
            upper_string1 += str(self.t_d_current[self.t_current])
            if self.t_d_current[self.t_current] > 9:  # allow for tens track device number digit
                upper_string1 += '------ '
            else:
                upper_string1 += '------- '

            lower_string1a += self.__transform_to_size(str(self.selected_track.name), 20)
            lower_string1a = lower_string1a.center(20)  # should already be centered?
            lower_string1a += ' '
            if self.__chosen_plugin is None:
                upper_string1 += '             '
                lower_string1b += '                                   '
                lower_string1 += lower_string1a
                lower_string1 += lower_string1b
                upper_string2 += '           NO DEVICES INSERTED ON THIS TRACK           '
                # so_many_spaces '                                                       '
                lower_string2 += so_many_spaces
                upper_string3 += so_many_spaces
                lower_string3 += so_many_spaces
                upper_string4 += so_many_spaces
                lower_string4 += so_many_spaces
            else:
                device_name = self.selected_track.devices[self.t_d_current[self.t_current]].name
                # MS: this throws massive Index errors when THE LAST device is deleted, maybe needs fallback to "none"?

                lower_string1b += self.__transform_to_size(str(device_name), 20)
                #  self.main_script().log_message("problematic string source <{0}>, transformed <{1}>".format(device_name, lower_string1b))
                lower_string1b = lower_string1b.center(20)
                lower_string1 += lower_string1a
                lower_string1 += lower_string1b
                lower_string1 += ' '
                upper_string1 += '-Params Bank-'
                for t in encoder_range:
                    try:
                        text_for_display = self.__display_parameters[t]  # assumes there are always 32
                    except IndexError:
                        text_for_display = ('---', ' X ')

                    u_alt_text = ''
                    l_alt_text = ''
                    if len(text_for_display) > 1:
                        u_alt_text = text_for_display[1]
                        l_alt_text = text_for_display[0]
                    elif len(text_for_display) > 0:
                        l_alt_text = text_for_display[0]

                    if t in range(6, NUM_ENCODERS_ONE_ROW):
                        lower_string1 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string1 += ' '
                    elif t in row_01_encoders:
                        upper_string2 += self.__transform_to_size(u_alt_text, 6)
                        upper_string2 += ' '
                        lower_string2 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string2 += ' '
                    elif t in row_02_encoders:
                        upper_string3 += self.__transform_to_size(u_alt_text, 6)
                        upper_string3 += ' '
                        lower_string3 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string3 += ' '
                    elif t in row_03_encoders:
                        upper_string4 += self.__transform_to_size(u_alt_text, 6)
                        upper_string4 += ' '
                        lower_string4 += self.__transform_to_size(str(l_alt_text), 6)
                        lower_string4 += ' '

        elif self.__assignment_mode == C4M_FUNCTION:
            upper_string1 += so_many_spaces
            lower_string1 += so_many_spaces
            upper_string2 += so_many_spaces
            lower_string2 += so_many_spaces
            upper_string3 += so_many_spaces
            lower_string3 += so_many_spaces
            upper_string4 += ' STOP   PLAY                                           '
            lower_string4 += so_many_spaces

        elif self.__assignment_mode == C4M_USER:
            upper_string1 += self.__display_parameters[0][1]
            lower_string1 += self.__display_parameters[0][0]
            upper_string2 += self.__display_parameters[1][1]
            lower_string2 += self.__display_parameters[1][0]
            upper_string3 += self.__display_parameters[2][1]
            lower_string3 += self.__display_parameters[2][0]
            upper_string4 += self.__display_parameters[3][1]
            lower_string4 += self.__display_parameters[3][0]

        # each of these is sent as a 63 byte SYSEX message to the C4 LCD displays
        self.send_display_string1(LCD_ANGLED_ADDRESS, upper_string1, LCD_TOP_ROW_OFFSET)
        self.send_display_string2(LCD_TOP_FLAT_ADDRESS, upper_string2, LCD_TOP_ROW_OFFSET)
        self.send_display_string3(LCD_MDL_FLAT_ADDRESS, upper_string3, LCD_TOP_ROW_OFFSET)
        self.send_display_string4(LCD_BTM_FLAT_ADDRESS, upper_string4, LCD_TOP_ROW_OFFSET)
        self.send_display_string1(LCD_ANGLED_ADDRESS, lower_string1, LCD_BOTTOM_ROW_OFFSET)
        self.send_display_string2(LCD_TOP_FLAT_ADDRESS, lower_string2, LCD_BOTTOM_ROW_OFFSET)
        self.send_display_string3(LCD_MDL_FLAT_ADDRESS, lower_string3, LCD_BOTTOM_ROW_OFFSET)
        self.send_display_string4(LCD_BTM_FLAT_ADDRESS, lower_string4, LCD_BOTTOM_ROW_OFFSET)
        return

    def __generate_6_char_string(self, display_string):
        return self.__transform_to_size(display_string, 6)

    def __generate_20_char_string(self, display_string):
        return self.__transform_to_size(display_string, 20)

    def __transform_to_size(self, raw_text, new_size):
        """ trim a string down to a given new_size, removing trailing or leading blank spaces first
            followed by a trailing 'dB' substring (if a '.' is also found somewhere in string)
            followed by spaces and lower case vowels in order [' ', 'i', 'o', 'u', 'e', 'a']
            or center smaller length strings within the new_size
            returns a string exactly new_size
        """
        if not raw_text or not isinstance(raw_text, str):
            return ''.join(list((' ' for i in range(new_size))))  # if given nothing return blanks
        
        transformed_text = raw_text.strip()
        is_ends_db = transformed_text.endswith('dB')
        has_dot = transformed_text.find('.') != -1
        if len(transformed_text) > new_size and is_ends_db and has_dot:
            transformed_text = transformed_text[:-2]  # remove the trailing 'dB'

        if len(transformed_text) > new_size:
            for um in (' ', 'i', 'o', 'u', 'e', 'a'):  # MS rounded or eckige Brackets? Sissy had eckig, decompiled Live11 had rounded
                while len(transformed_text) > new_size and transformed_text.rfind(um, 1) != -1:
                    um_pos = transformed_text.rfind(um, 1)
                    transformed_text = transformed_text[:um_pos]
                    if len(transformed_text) > um_pos + 1:  # if um_pos is last char, um_pos + 1 is OB
                        transformed_text += transformed_text[um_pos + 1:]

        transformed_text = transformed_text.center(new_size)
        return ''.join([transformed_text[i] for i in range(new_size)])

    def send_display_string1(self, display_address, text_to_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Angled display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_to_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages1[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 3
        if is_update or is_stale:  # don't send the same sysex message back-to-back unless the repeat timer pops
            self.__last_send_messages1[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints)   + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def send_display_string2(self, display_address, text_to_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Top-flat display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_to_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages2[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 2
        if is_update or is_stale:
            self.__last_send_messages2[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def send_display_string3(self, display_address, text_to_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Middle-flat display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_to_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages3[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 1
        if is_update or is_stale:
            self.__last_send_messages3[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def send_display_string4(self, display_address, text_to_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Bottom-flat display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_to_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages4[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 0
        if is_update or is_stale:
            self.__last_send_messages4[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def __generate_sysex_body(self, text_to_display, display_row_offset, cursor_offset=0):

        # looks like cursor_offset is supposed to be an index to each cell in an LCD row
        # but the SYSEX message for writing to any display row is always 63 bytes
        # (55 bytes of ASCII text) i.e. the whole row, so cursor_offset can be eliminated
        if display_row_offset == LCD_TOP_ROW_OFFSET:  # 0x00
            offset = cursor_offset
        elif display_row_offset == LCD_BOTTOM_ROW_OFFSET:  # 0x38 (56 == NUM_CHARS_PER_DISPLAY_LINE + 2)
            # offset = NUM_CHARS_PER_DISPLAY_LINE + 2 + cursor_offset
            offset = LCD_BOTTOM_ROW_OFFSET + cursor_offset
        else:
            assert 0

        # convert unicode string (list of character values) to list of integer values
        ascii_text_sysex_ints = [ord(c) for c in text_to_display]
        for i in range(len(ascii_text_sysex_ints)):
            if ascii_text_sysex_ints[i] > MIDI_DATA_LAST_VALID:

                # replace any integer values above the ASCII 7-bit (MIDI_DATA) range (0x00 - 0x7F)
                # replacement value is the code for #
                ascii_text_sysex_ints[i] = ASCII_HASH

        return ascii_text_sysex_ints

    def refresh_state(self):
        for s in self.__encoders:
            s.refresh_state()