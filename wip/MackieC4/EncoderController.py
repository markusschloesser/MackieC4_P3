# coding=utf-8
# was once Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/EncoderController.py
# Compiled at: 2011-01-22 05:02:32
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals  # MS
from __future__ import division

from itertools import chain

import sys
# from _multiprocessing import send

from ableton.v2.base import liveobj_valid, liveobj_changed  # ,  move_current_song_time # only works for Live 11.1, was introduced into live_api_utils
from ableton.v2.control_surface.elements.display_data_source import adjust_string


# from Encoders import Encoders

if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

from . import track_util
from . import song_util
from .EncoderAssignmentHistory import EncoderAssignmentHistory
from .EncoderDisplaySegment import EncoderDisplaySegment
from .MackieC4Component import *
from _Generic.Devices import *
from .TimeDisplay import TimeDisplay


class EncoderController(MackieC4Component):
    """
     Controls all (the sum) encoders of the Mackie C4 Pro controller extension
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

        self.__eah = EncoderAssignmentHistory(main_script, self)
        self.__time_display = TimeDisplay(self)
        self.__assignment_mode = C4M_CHANNEL_STRIP
        self.__last_assignment_mode = C4M_USER
        self.__current_track_name = ''  # Live's Track Name of selected track
        self.selected_track = None  # Live's selected-Track Object

        self.__ordered_plugin_parameters = []  # Live's DeviceParameters of __chosen_plugin (if exists)
        self.__chosen_plugin = None

        self.__display_parameters = []
        for x in range(NUM_ENCODERS):
            # initialize to blank screen segments
            self.__display_parameters.append(EncoderDisplaySegment(self, x))

        # __display_repeat_timer is a work-around for when the C4 LCD display changes due to a MIDI sysex message
        # received by the C4 from somewhere else, not-here.  Such a display change is not tracked here (obviously),
        # and the C4 itself can't be asked "what are you displaying right now?". So we just blast the display sysex
        # from here about every 5 seconds to overwrite any possible "other change".  (each LCD is "refreshed" in turn
        # each time this timer "pops" (every 4th pop per LCD))
        # turn this off to let the C4 LEDs and LCDs "go to sleep" after nothing changes for 15 or 20 minutes
        # If you randomly see the standard C4 welcome message (because of the rogue SYSEX message)
        # a "real" display update from Live always removes a standard C4 welcome message
        self.__display_repeat_timer = LCD_DISPLAY_UPDATE_REPEAT_MULTIPLIER * 5
        self.__display_repeat_count = 0

        # self.__master_track_index = 0
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
                # self.t_current = index - 1
                # self.__eah.track_changed(index - 1)
                self.track_changed(index - 1)
                found = 1

        if found == 0:
            # self.t_current = index
            # self.__eah.track_changed(index)
            self.track_changed(index)

        self.selected_track = self.song().view.selected_track
        self.update_assignment_mode_leds()
        self.__last_send_messages1 = {LCD_ANGLED_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        self.__last_send_messages2 = {LCD_TOP_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        self.__last_send_messages3 = {LCD_MDL_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        self.__last_send_messages4 = {LCD_BTM_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: [], LCD_BOTTOM_ROW_OFFSET: []}}
        return

    def destroy(self):
        # self.destroy()
        so_many_spaces = '                                                       '
        self.send_display_string1(LCD_ANGLED_ADDRESS, '                     Ableton Live                      ', LCD_TOP_ROW_OFFSET)
        self.send_display_string2(LCD_TOP_FLAT_ADDRESS, so_many_spaces, LCD_TOP_ROW_OFFSET)
        self.send_display_string3(LCD_MDL_FLAT_ADDRESS, so_many_spaces, LCD_TOP_ROW_OFFSET)
        self.send_display_string4(LCD_BTM_FLAT_ADDRESS, so_many_spaces, LCD_TOP_ROW_OFFSET)
        self.send_display_string1(LCD_ANGLED_ADDRESS, '                   Device is offline                   ', LCD_BOTTOM_ROW_OFFSET)
        self.send_display_string2(LCD_TOP_FLAT_ADDRESS, so_many_spaces, LCD_BOTTOM_ROW_OFFSET)
        self.send_display_string3(LCD_MDL_FLAT_ADDRESS, so_many_spaces, LCD_BOTTOM_ROW_OFFSET)
        self.send_display_string4(LCD_BTM_FLAT_ADDRESS, so_many_spaces, LCD_BOTTOM_ROW_OFFSET)
        for note in system_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))
        for note in assignment_mode_switch_ids:
            self.send_midi((NOTE_ON_STATUS, note, BUTTON_STATE_OFF))
        MackieC4Component.destroy(self)

    def request_rebuild_midi_map(self):
        MackieC4Component.request_rebuild_midi_map(self)  # MS mmh good idea? was next line
        # self._MackieC4Component__main_script.request_rebuild_midi_map()
        #
        # self.main_script.request_rebuild_midi_map(self)
        # self._MackieC4Component.request_rebuild_midi_map(self)

    def get_encoders(self):
        return self.__encoders

    def build_setup_database(self):
        self.main_script().log_message("building setup db")
        self.__eah.build_setup_database(self.song())        # self.track_count

        self.main_script().log_message("t_count after setup <{0}>".format(self.__eah.t_count))
        self.main_script().log_message("main_script().track_count after setup <{0}>".format(self.main_script().track_count))

        devices_on_selected_trk = self.song().view.selected_track.devices
        if len(devices_on_selected_trk) == 0:
            self.__chosen_plugin = None
        else:
            self.__chosen_plugin = devices_on_selected_trk[0]
            self.song().view.select_device(devices_on_selected_trk[0])

        self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()
        return

    def master_track_index(self):
        return self.__eah.master_track_index()

    def track_changed(self, track_index):
        self.selected_track = self.song().view.selected_track
        selected_device_index = self.__eah.track_changed(track_index)
        if len(self.selected_track.devices) == 0:
            self.__chosen_plugin = None
            self.__eah.update_device_counter(track_index, 0)
            self.__reorder_parameters()
        else:
            if selected_device_index > -1:
                if len(self.selected_track.devices) > selected_device_index:
                    self.__chosen_plugin = self.selected_track.devices[selected_device_index]
                    self.__eah.update_device_counter(track_index, len(self.selected_track.devices))
                    self.__reorder_parameters()
                else:
                    # something isn't getting updated correctly at startup and/or when devices are deleted
                    self.main_script().log_message(
                        "len(self.selected_track.devices) <= selected_device_index")
                    self.main_script().log_message(
                        "{0} <= {1}".format(len(self.selected_track.devices), selected_device_index))
            else:
                # something isn't getting updated correctly at startup and/or when devices are deleted
                self.main_script().log_message("len(self.t_d_current) <= self.t_current")
                self.main_script().log_message("{0} <= {1}".format(len(self.__eah.t_d_current), self.__eah.t_current))

        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()
        return

    def track_added(self, track_index):
        self.selected_track = self.song().view.selected_track
        self.__eah.track_added(track_index, self.selected_track.devices)

        # This is a way to call a super-class method from a sub-class with
        # a method of the same name see def refresh_state() below (way, way below)
        MackieC4Component.refresh_state(self)
        selected_device_index = self.__eah.get_selected_device_index()
        if selected_device_index > -1:
            if len(self.selected_track.devices) > selected_device_index:
                selected_device = self.selected_track.devices[selected_device_index]
                self.__chosen_plugin = selected_device
                self.song().view.select_device(selected_device)
                self.__reorder_parameters()
            elif len(self.selected_track.devices) > 0:
                selected_device = self.selected_track.devices[0]
                self.__eah.set_selected_device_index(0)
                self.__chosen_plugin = selected_device
                self.song().view.select_device(selected_device)
                self.__reorder_parameters()
            else:
                self.__chosen_plugin = None
                self.__reorder_parameters()
        else:
            self.__chosen_plugin = None
            self.__reorder_parameters()

        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()
        return

    def track_deleted(self, track_index):
        self.main_script().log_message("del tk idx before deleted track: {0}".format(track_index))
        self.__eah.track_deleted(track_index)
        self.selected_track = self.song().view.selected_track
        self.main_script().log_message("selected tk after: {0}".format(self.selected_track.name))
        self.refresh_state()

        selected_device_index = self.__eah.get_selected_device_index()
        self.main_script().log_message("selected tk device index after: {0}".format(selected_device_index))
        self.main_script().log_message("nbr of devices on selected track after: {0}".format(len(self.selected_track.devices)))
        if selected_device_index > -1:
            if len(self.selected_track.devices) > selected_device_index:
                selected_device = self.selected_track.devices[selected_device_index]
                self.__chosen_plugin = selected_device
                self.__reorder_parameters()
            elif len(self.selected_track.devices) > 0:
                selected_device = self.selected_track.devices[0]
                self.__eah.set_selected_device_index(0)
                self.__chosen_plugin = selected_device
                self.__reorder_parameters()
            else:
                self.__chosen_plugin = None
                self.__reorder_parameters()
        else:
            self.__chosen_plugin = None
            self.__reorder_parameters()

        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()
        return

    def device_added_deleted_or_changed(self, track, tid, type):
        updated_idx = -1
        if liveobj_valid(track):
            self.main_script().log_message("EC: processing device changestate of type <{0}> on track <{1}> at index {2}"
                                           .format(type, track.name, tid))
            if liveobj_changed(self.selected_track, track):
                self.main_script()\
                    .log_message("because liveobj_changed(), updating selected track to <{0}> ".format(track.name) +
                                 "and track_changed() at index {0}".format(tid))
                self.selected_track = track
                self.track_changed(tid)

            if liveobj_valid(self.selected_track):
                if liveobj_valid(self.selected_track.view.selected_device):
                    selected_device_idx = next((x for x in range(len(self.selected_track.devices))
                                               if self.selected_track.devices[x] ==
                                               self.selected_track.view.selected_device), -1)

                    updated_idx = self.__eah.device_added_deleted_or_changed(self.selected_track.devices,
                                                                             self.selected_track.view.selected_device,
                                                                             selected_device_idx)

        if not liveobj_valid(self.__chosen_plugin):
            self.main_script().log_message("switching not liveobj_valid(__chosen_plugin) to device at index {0}"
                                           .format(updated_idx))
        else:
            self.main_script().log_message("switching __chosen_plugin {0} to device at index {1}"
                                           .format(self.__chosen_plugin.name, updated_idx))

        if len(self.selected_track.devices) > updated_idx > -1:
            self.__chosen_plugin = self.selected_track.devices[updated_idx]  # == new selected device
            #  self.main_script().log_message("updated __chosen_plugin is now {0} ".format(self.__chosen_plugin.name))
        elif len(self.selected_track.devices) > 0:
            self.__chosen_plugin = self.selected_track.devices[0]  # == new selected device
            self.__eah.set_selected_device_index(0)
            # self.main_script().log_message("only device __chosen_plugin is now {0} ".format(self.__chosen_plugin.name))
        else:
            self.__chosen_plugin = None
            # might happen if track with no devices deleted, and the next selected track also has no devices?
            self.__eah.set_selected_device_index(-1)  # danger -1 is OOB for an index
            self.main_script().log_message("__chosen_plugin is now None")

        self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()

        new_device_count_track = len(self.selected_track.devices)
        self.main_script().log_message(
            "track device list size <{0}> AFTER device_added_deleted_or_changed update".format(new_device_count_track))

        idx = 0
        for device in self.selected_track.devices:
            if liveobj_valid(device):
                self.main_script().log_message("idx <{0}> after <{1}>".format(idx, device.name))
            else:
                self.main_script().log_message("idx <{0} after <None>".format(idx))

            idx += 1

    def assignment_mode(self):
        return self.__assignment_mode

    def last_assignment_mode(self):
        return self.__last_assignment_mode

    # no wrap around:
    #   stop moving left at track 0,
    #   stop moving right at master track
    def handle_bank_switch_ids(self, switch_id):
        """ works in all modes """
        self.main_script().log_message("self.__assignment_mode == C4M_CHANNEL_STRIP is <{0}>"
                                       .format(self.__assignment_mode == C4M_CHANNEL_STRIP))
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
        elif self.__assignment_mode == C4M_CHANNEL_STRIP:
            selected_device_index = self.__eah.get_selected_device_index()
            if selected_device_index > -1:
                #  self.main_script().log_message("selected device index before <{0}>".format(selected_device_index))

                if switch_id == C4SID_SINGLE_LEFT:  # to previous device
                    selected_device_index -= 1
                    #  self.main_script().log_message("selected device left")
                elif switch_id == C4SID_SINGLE_RIGHT:  # to next device
                    #  self.main_script().log_message("selected device right")
                    selected_device_index += 1

                self.main_script().log_message("selected device index after <{0}>".format(selected_device_index))
                nbr_devices = len(self.selected_track.devices)
                if nbr_devices > 0 and nbr_devices > selected_device_index:

                    self.__eah.set_selected_device_index(selected_device_index)
                    current_selected_device = self.selected_track.devices[selected_device_index]
                    self.song().view.select_device(current_selected_device)
                    self.__chosen_plugin = current_selected_device
                    self.__reorder_parameters()
                    self.__reassign_encoder_parameters(for_display_only=False)
                    self.request_rebuild_midi_map()
                    self.main_script().log_message("new selected device <{0}>".format(self.__chosen_plugin.name))
                else:
                    # something isn't getting updated correctly at startup and/or when devices are deleted
                    self.main_script().log_message("nbr_devices <= self.t_d_current[self.t_current]")
                    self.main_script().log_message("{0} <= {1}".format(nbr_devices,
                                                                       self.__eah.get_selected_device_index()))
            else:
                # something isn't getting updated correctly at startup and/or when devices are deleted
                self.main_script().log_message("len(self.t_d_current) <= self.t_current")
                self.main_script().log_message("{0} <= {1}".format(len(self.__eah.t_d_current), self.__eah.t_current))

        if update_self:
            # self.t_d_p_bank_current[self.t_current][self.t_d_current[self.t_current]] = current_bank_nbr
            self.__eah.set_current_track_device_parameter_bank_nbr(current_bank_nbr)
            self.__reassign_encoder_parameters(for_display_only=False)
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
            # only switch mode and set "last mode" when the mode actually changes
            if self.__assignment_mode != button_id_to_assignment_mode[C4SID_TRACK]:  # C4M_PLUGINS:
                self.__last_assignment_mode = self.__assignment_mode
                self.__assignment_mode = button_id_to_assignment_mode[C4SID_TRACK]  # C4M_PLUGINS

                # **  If the local "db" says the index of the current device is 0,
                # ** And the local "db" says the count of devices is not 0
                # ** force the first device on the track to be
                # ** the selected device in Live?
                # self.t_d_current[self.t_current] == 0 and self.t_d_count[self.t_current] != 0 and
                # self.song().view.select_device(self.selected_track.devices[0])

                # MS this could be something
                # this code says only set (in Live) an updated current selected device at index 0
                # if the current selected device index is 0 AND there is actually a device on the track
                # this might be a hack working around initializing all the history values to 0
                # if self.t_d_current[self.t_current] == 0 and self.t_d_count[self.t_current] != 0:
                if self.__eah.get_selected_device_index() == 0 and self.__eah.get_max_device_count() > 0:
                    self.song().view.select_device(self.selected_track.devices[0])
                # else: self.song().view.select_device() has already been correctly performed somewhere?
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
            self.__reassign_encoder_parameters(for_display_only=False)
            self.request_rebuild_midi_map()
        # else don't update because nothing changed here

    def handle_slot_nav_switch_ids(self, switch_id):  # MS currently only half working, only works for normal devices, not grouped devices
        """ "slot navigation" only functions if the current mode is C4M_PLUGINS """
        if self.__assignment_mode == button_id_to_assignment_mode[C4SID_TRACK]:  # C4M_PLUGINS:
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

            if update_self:
                self.__eah.set_selected_device_index(current_trk_device_index)
                if len(self.selected_track.devices) > current_trk_device_index:
                    current_selected_device = self.selected_track.devices[current_trk_device_index]
                elif len(self.selected_track.devices) > 0:
                    current_selected_device = self.selected_track.devices[0]
                    self.__eah.set_selected_device_index(0)
                else:
                    current_selected_device = None
                    self.__eah.set_selected_device_index(-1)

                if liveobj_valid(current_selected_device):
                    self.song().view.select_device(current_selected_device)
                    self.__chosen_plugin = current_selected_device
                    self.__reorder_parameters()

                self.__reassign_encoder_parameters(for_display_only=False)
                self.request_rebuild_midi_map()

    def handle_modifier_switch_ids(self, switch_id, value):
        if switch_id == C4SID_SHIFT:
            self.main_script().set_shift_is_pressed(value == NOTE_ON_STATUS)
        pass

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
        """ currently does nothing. If we want something done here, it needs to be forwarded by MackieC4/receive_midi """
        # coming from the C4 these midi messages look like: B0  20  01  1 or B0  21  01  1, where vpot_index here would be 00 or 01 (after subtracting 0x20 from 0x20 or 0x21),
        # and cc_value would be 01 in both examples but could be any value 01 - 0x7F, however in here (because coming from the C4) if cc_value is in the range 01 - 0F (0-64),
        # the encoder is being turned clockwise, and if cc_value is in the range 41 - 4F (65-128), the encoder is being turned counter-clockwise the higher the value,
        # the faster the knob is turning, so theoretically 16 steps of "knob twisting speed" in either direction. Suspect this is because other encoder rotation messages
        # are "midi mapped" through Live with feedback i.e. when you rotate encoder 32 in C4M_CHANNEL_STRIP mode, the "level number" updates itself via the
        # midi mapping through Live (see Encoders.build_midi_map()), not via code here. MS: correct! :-)
        self.main_script().log_message("potIndex<{0}> cc_value<{1}> received".format(vpot_index, cc_value))
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
        encoder_25_index = 24
        encoder_26_index = 25
        encoder_27_index = 26
        encoder_28_index = 27
        encoder_29_index = 28
        encoder_30_index = 29
        encoder_31_index = 30
        encoder_32_index = 31

        if self.__assignment_mode == C4M_FUNCTION:
            for s in self.__encoders:
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)  # MS moved to on_update_display_timer
                vpot_display_text.set_encoder_controller(self)
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

                if s_index == encoder_12_index:
                    self.main_script().log_message("cc_nbr<{}> cc_value<{}> received in handle_vpot_rotation".format(vpot_index, cc_value))
                    # time display was moved to on_update_display_timer because song position needs to be updated in real-time

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])

    def handle_pressed_v_pot(self, vpot_index):
        """ 'encoder button' clicks are not handled in C4M_USER assignment mode  """
        encoder_index = vpot_index - C4SID_VPOT_PUSH_BASE  # 0x20  32
        selected_device_bank_index = self.__eah.get_selected_device_bank_index()
        old_selected_bank = selected_device_bank_index
        max_device_bank_index = self.__eah.get_selected_device_bank_count() - 1
        if self.__assignment_mode == C4M_CHANNEL_STRIP:
            is_armable_track_selected = track_util.can_be_armed(self.selected_track)

            if encoder_index in row_00_encoders:
                # only "top row" encoders 7 and 8 are mapped in C4M_CHANNEL_STRIP mode
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

                    self.main_script().log_message("updating selected device bank index from <{0}> to <{1}>"
                                                   .format(old_selected_bank, selected_device_bank_index))
                    self.__eah.set_selected_device_bank_index(selected_device_bank_index)
                    self.__reassign_encoder_parameters(for_display_only=False)

            elif encoder_index in row_01_encoders:
                # (row 2 "index" is 01) these encoders represent devices 1 - 8 on the selected track in C4M_CHANNEL_STRIP mode
                # encoder button press == automatically switch to Track/Plugins mode AND update "current selected Plugin" to the device represented by the encoder clicked
                self.handle_assignment_switch_ids(C4SID_TRACK)

                device_bank_offset = int(NUM_ENCODERS_ONE_ROW * selected_device_bank_index)
                device_offset = vpot_index - C4SID_VPOT_PUSH_BASE - NUM_ENCODERS_ONE_ROW + device_bank_offset
                if len(self.selected_track.devices) > device_offset:  # if the calculated offset is valid device index
                    self.__chosen_plugin = self.selected_track.devices[device_offset]
                    self.__reorder_parameters()
                    self.__eah.set_selected_device_index(encoder_index - NUM_ENCODERS_ONE_ROW + device_bank_offset)
                    self.song().view.select_device(self.selected_track.devices[device_offset])
                    self.__reassign_encoder_parameters(for_display_only=False)
                    self.request_rebuild_midi_map()
                else:
                    msg = "can't update __chosen_plugin: the calculated device_offset {0} is NOT a valid device index"\
                        .format(device_offset)
                    self.main_script().log_message(msg)
                    self.__chosen_plugin = None
            elif encoder_index in row_02_encoders:
                # these encoders represent sends 1 - 8 (row 3 "index" is 02) in C4M_CHANNEL_STRIP mode
                param = self.__filter_mst_trk_allow_audio and self.__encoders[encoder_index].v_pot_parameter()
                if liveobj_valid(param):
                    if isinstance(param, int):  # PyCharm says 'param' is an int based on the
                        #                         self.__encoders[encoder_index].v_pot_parameter() assignment above.
                        #                         int also doesn't have a default_value?
                        param.value = 0  # if param is never actually an int when it isn't None,
                        #                  this assignment just satisfies PyCharm
                    else:
                        param.value = param.default_value  # button press == jump to default value of Send?
                else:
                    self.main_script().log_message("can't update param.value to default: None object")
            elif encoder_index in row_03_encoders:
                # encoder 29 is "Rec Arm" encoder in C4M_CHANNEL_STRIP mode
                # encoder 30 is "Mute"
                encoder_28_index = 27
                encoder_29_index = 28
                encoder_30_index = 29
                s = next(x for x in self.__encoders if x.vpot_index() == encoder_index)

                if encoder_index < encoder_28_index:
                    # these encoders are the four < encoder_29_index, left half of bottom row, sends 9 - 12
                    param = self.__filter_mst_trk_allow_audio and self.__encoders[encoder_index].v_pot_parameter()
                    if liveobj_valid(param):
                        if isinstance(param, int):
                            param.value = 0
                        else:
                            param.value = param.default_value  # button press == jump to default value of Send?
                    else:
                        self.main_script().log_message("can't update param.value to default: param not liveobj_valid()")

                elif encoder_index == encoder_28_index:
                    if self.__filter_mst_trk:
                        if self.selected_track.solo is not True:
                            self.selected_track.solo = True
                        else:
                            self.selected_track.solo = False
                    else:
                        self.main_script().log_message("track not soloable")
                        s.unlight_vpot_leds()

                elif encoder_index == encoder_29_index:
                    if self.__filter_mst_trk:
                        if is_armable_track_selected:
                            if self.selected_track.arm is not True:
                                self.selected_track.arm = True
                            else:
                                self.selected_track.arm = False
                        else:
                            self.main_script().log_message("track not armable")
                            s.unlight_vpot_leds()

                elif encoder_index == encoder_30_index:
                    if self.__filter_mst_trk:
                        if self.selected_track.mute:
                            self.selected_track.mute = False
                        else:
                            self.selected_track.mute = True
                    else:
                        self.main_script().log_message("something about master track")
                        # s.unlight_vpot_leds()  # moved to on_update_display_timer

                elif encoder_index > encoder_30_index:
                    #  encoder 31 is "Pan"
                    #  encoder 32 is "Volume"
                    param = self.__encoders[encoder_index].v_pot_parameter()
                    param.value = param.default_value  # button press == jump to default value of Pan or Vol?

        elif self.__assignment_mode == C4M_PLUGINS:
            encoder_07_index = 6
            encoder_08_index = 7
            current_device_track = self.__eah.get_selected_device_index()
            current_parameter_bank_track = self.__eah.get_current_track_device_parameter_bank_nbr(current_device_track)
            # self.main_script().log_message("current_parameter_bank_track: {0}".format(current_parameter_bank_track))
            stop = len(self.__display_parameters) + SETUP_DB_DEVICE_BANK_SIZE  # always 40?
            display_params_range = range(SETUP_DB_DEVICE_BANK_SIZE, stop)  # display_params_range always 8 - 39?
            # suspect display_params_range is supposed to protect against "short" parameter lists < 24
            # when self.__display_parameters is always 32 EncoderDisplaySegments now
            # we might need to check the length of the actual parameter list of the selected device
            update_self = False
            if encoder_index == encoder_07_index:
                if current_parameter_bank_track > 0:
                    current_parameter_bank_track -= 1
                    # self.main_script().log_message("self.t_d_p_bank_current[self.t_current]: {0}".format(self.__eah.get_selected_device_index()))
                    update_self = True
                else:
                    self.main_script().log_message("can't decrement current_parameter_bank_track: already bank 0")
            elif encoder_index == encoder_08_index:
                current_track_device_preset_bank = current_parameter_bank_track
                # self.main_script().log_message("current_track_device_preset_bank: {0}".format(current_track_device_preset_bank))
                track_device_preset_bank_count = self.__eah.get_max_current_track_device_parameter_bank_nbr(current_device_track)
                # self.main_script().log_message("track_device_preset_bank_count: {0}".format(track_device_preset_bank_count))
                if current_track_device_preset_bank < track_device_preset_bank_count - 1:
                    current_parameter_bank_track += 1
                    update_self = True
                else:
                    self.main_script().log_message("can't increment current_parameter_bank_track: already last bank")
            # should be encoders 9 - 32 (on each param page), but stopping short on last/only (short is < 24) parameter page
            elif encoder_index in display_params_range:
                # if a device has less than 24 parameters exposed on this page, param will be (None, '    ')
                param = self.__encoders[encoder_index].v_pot_parameter()
                if liveobj_valid(param):
                    if param is not tuple:
                        try:
                            if param.is_enabled:
                                if param.is_quantized:  # for stepped params or those that only have a limited range
                                    if param.value + 1 > param.max:
                                        param.value = param.min
                                    else:
                                        param.value = param.value + 1
                                else:
                                    # button press == jump to default value of device parameter
                                    param.value = param.default_value
                        except (RuntimeError, AttributeError):
                            # There is no default value available for this type of parameter
                            # 'NoneType' object has no attribute 'default_value'
                            pass

            if update_self:
                self.main_script().log_message(
                    "updating current_track_device_parameter_bank_nbr from <{0}> to {1}".format(
                        self.__eah.get_current_track_device_parameter_bank_nbr(), current_parameter_bank_track))
                self.__eah.set_current_track_device_parameter_bank_nbr(current_parameter_bank_track)
                self.__reassign_encoder_parameters(for_display_only=False)
                self.request_rebuild_midi_map()

        elif self.__assignment_mode == C4M_FUNCTION:
            # encoder 25 is bottom row left "Stop Playback"
            # encoder 26 is bottom row second from left "Start Playback"
            encoder_01_index = 0  # follow
            encoder_02_index = 1  # loop
            encoder_03_index = 2  # Detail / Clip
            encoder_04_index = 3
            encoder_05_index = 4
            encoder_06_index = 5
            encoder_07_index = 6
            encoder_08_index = 7
            encoder_09_index = 8
            encoder_10_index = 9
            encoder_11_index = 10
            encoder_12_index = 11  # SPP
            # encoder_13_index is covered / occupied by SPP from 12
            encoder_14_index = 13
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
                song_util.unsolo_all(self)
                for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
                    if track.solo:
                        s.show_full_enlighted_poti()
                    else:
                        s.unlight_vpot_leds()
            elif encoder_index == encoder_07_index:
                song_util.unmute_all(self)
                s.unlight_vpot_leds()
            elif encoder_index == encoder_08_index:
                song_util.toggle_back_to_arranger(self)
                if song_util.toggle_back_to_arranger:
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_09_index:
                if self.song().can_undo:  # if you can (still) undo something, LEDs stay lit
                    s.show_full_enlighted_poti()
                    song_util.undo(self)
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_10_index:
                if self.song().can_redo:  # if you can (still) redo something, LEDs stay lit
                    s.show_full_enlighted_poti()
                    song_util.redo(self)
                else:
                    s.unlight_vpot_leds()
            elif encoder_index == encoder_11_index:
                if song_util.unarm_all_button(self):
                    s.show_full_enlighted_poti()
                    song_util.unsolo_all(self)

            # toggle between BEAT and SMPTE mode for SPP
            elif encoder_index == encoder_12_index:
                self.__time_display.toggle_mode()
                # displaying part moved to on_update_display_timer, also for vpot lights

            elif encoder_index == encoder_25_index:
                self.song().stop_playing()
                self.__encoders[encoder_26_index].unlight_vpot_leds()
                self.__encoders[encoder_27_index].unlight_vpot_leds()
            elif encoder_index == encoder_26_index:
                self.song().is_playing = True
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

    def __send_parameter(self, vpot_index):
        """ Returns the send parameter that is assigned to the given encoder as a tuple (param, param.name) """
        if vpot_index < len(self.song().view.selected_track.mixer_device.sends):
            p = self.song().view.selected_track.mixer_device.sends[vpot_index]
            #  self.main_script().log_message("Param name <{0}>".format(p.name))
            return (p, p.name)
        else:
            # The Song doesn't have this many sends
            return None, '      '  # remove this text after you see it in the LCD, just use blanks

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
                try:
                    self.main_script().log_message("Param {0} name <{1}>".format(vpot_index, p.name))
                except AttributeError:  # 'tuple' object has no attribute 'name'
                    self.main_script().log_message("Param {0} tuple name <{1}>".format(vpot_index, p[1]))
                return p
            else:
                # self.main_script().log_message("vpot_index + preset_bank_index == invalid parameter index")
                # self.main_script().log_message("{0} + {1} >= {2}".format(
                #                            vpot_index, preset_bank_index, current_track_param_count))
                self.main_script().log_message("Param {0} + {1} not mapped".format(
                                            vpot_index, preset_bank_index))

            # The device doesn't have this many parameters
            return None, '      '  # remove this text after you see it in the LCD, just use blanks

    def __on_parameter_list_of_chosen_plugin_changed(self):
        assert liveobj_valid(self.__chosen_plugin)
        self.__reorder_parameters()
        self.__reassign_encoder_parameters(for_display_only=False)
        self.request_rebuild_midi_map()
        return

    def __reorder_parameters(self):
        result = []
        if liveobj_valid(self.__chosen_plugin):

            # if a default Live device is chosen, iterate the DEVICE_DICT constant to reorder the local list of plugin parameters
            if self.__chosen_plugin.class_name in list(DEVICE_DICT.keys()):
                device_banks = DEVICE_DICT[self.__chosen_plugin.class_name]
                device_bank_index = 0
                for bank in device_banks:
                    param_bank_index = 0
                    for param_name in bank:
                        parameter_name = ''
                        parameter = get_parameter_by_name(self.__chosen_plugin, param_name)
                        if parameter:
                            parameter_name = parameter.name
                        else:  # get parameter by index if possible
                            param_index = param_bank_index + (SETUP_DB_DEVICE_BANK_SIZE * device_bank_index)
                            if len(self.__chosen_plugin.parameters) > param_index:
                                parameter = self.__chosen_plugin.parameters[param_index]
                                parameter_name = parameter.name
                            else:
                                parameter = None

                        result.append((parameter, parameter_name))
                        param_bank_index += 1

                    device_bank_index += 1

            # otherwise reorder the local list to the order provided by the parameter itself
            else:
                result = [(p, p.name) for p in self.__chosen_plugin.parameters]

        self.__ordered_plugin_parameters = result  # these are tuples where index 0 is a DeviceParameter object
        count = 0

        nbr_of_full_pages = int(len(self.__ordered_plugin_parameters) / SETUP_DB_PARAM_BANK_SIZE)  # len() / 24
        nbr_of_remainders = int(len(self.__ordered_plugin_parameters) % SETUP_DB_PARAM_BANK_SIZE)  # len() % 24
        if nbr_of_full_pages >= SETUP_DB_MAX_PARAM_BANKS:
            nbr_of_full_pages = SETUP_DB_MAX_PARAM_BANKS
        elif nbr_of_full_pages < 0:
            nbr_of_full_pages = 0
            self.main_script().log_message("Not possible, right? and yet I am logged")

        if nbr_of_full_pages == 0 and nbr_of_remainders > 0:
            nbr_of_full_pages = 1
        elif nbr_of_remainders > 0:  # 0 < nbr_of_full_pages < SETUP_DB_MAX_PARAM_BANKS
            nbr_of_full_pages += 1

        # Note: see above handle_pressed_vpot(encoder 8 click in device mode)
        self.__eah.set_max_current_track_device_parameter_bank_nbr(nbr_of_full_pages)
        for p in self.__ordered_plugin_parameters:
            # log the param names to the Live log in order
            self.main_script().log_message("Param {0} name <{1}>".format(count, p[1]))
            count += 1

    def __reassign_encoder_parameters(self, for_display_only):  # this is where the real assignment is going on, not vpot_rotation
        """ Reevaluate all v-pot -> parameter assignments """
        self.__filter_mst_trk = 0
        self.__filter_mst_trk_allow_audio = 0
        self.__current_track_name = self.selected_track.name
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
            current_nbr_of_devices_on_selected_track = len(self.selected_track.devices)
            self.__eah.set_max_device_count(current_nbr_of_devices_on_selected_track)

            nbr_of_full_device_pages = int(current_nbr_of_devices_on_selected_track / SETUP_DB_DEVICE_BANK_SIZE)  # / 16
            nbr_of_remainder_devices = int(current_nbr_of_devices_on_selected_track % SETUP_DB_DEVICE_BANK_SIZE)
            if nbr_of_full_device_pages >= SETUP_DB_MAX_DEVICE_BANKS:
                nbr_of_full_device_pages = SETUP_DB_MAX_DEVICE_BANKS
            elif nbr_of_full_device_pages < 0:
                nbr_of_full_device_pages = 0
                self.main_script().log_message("Not possible, right? and yet I am logged")

            if nbr_of_full_device_pages == 0 and nbr_of_remainder_devices > 0:
                nbr_of_full_device_pages = 1
            elif nbr_of_remainder_devices > 0:  # 0 < nbr_of_full_device_pages < SETUP_DB_MAX_DEVICE_BANKS
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
                    # if s_index < encoder_07_index:
                    #     always fill the __displayParameters list
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
                    self.__display_parameters.append(vpot_display_text)
                elif s_index in row_01_encoders:

                    row_index = s_index - SETUP_DB_DEVICE_BANK_SIZE
                    current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)
                    # self.main_script().log_message("(ch mode) device row row_index {0} current bank offset <{1}>"
                    #                                .format(row_index, current_encoder_bank_offset))

                    # watch out for 'no device on track' when row_index = 0 and current bank = 0
                    # if row_index = 0 and current bank = 0, then offset is 0
                    #                  and encoder is mapped to 1st device on track
                    # if row_index = 1 and current bank = 0, then offset is 0
                    #                  and encoder is mapped to 2nd device on track
                    # if row_index = 7 and current bank = 0, then offset is 0
                    #                  and encoder is mapped to 8th device on track
                    # if row_index = 0 and current bank = 1, then offset is 8
                    #                  and encoder is mapped to 9th device on track
                    # if row_index = 1 and current bank = 1, then offset is 8
                    #                  and encoder is mapped to 10th device on track
                    # if row_index = 7 and current bank = 1, then offset is 8
                    #                  and encoder is mapped to 16th device on track
                    # if row_index + current_encoder_bank_offset < self.t_d_count[self.t_current]:
                    if row_index + current_encoder_bank_offset < self.__eah.get_max_device_count():
                        s.show_full_enlighted_poti()
                        encoder_index_in_row = row_index + int(current_encoder_bank_offset)
                        if encoder_index_in_row < len(self.selected_track.devices):
                            device_name = self.selected_track.devices[encoder_index_in_row].name
                            # device_name in bottom row, blanks on top (top text blocked across full LCD)
                            vpot_display_text.set_text(device_name, '')
                        else:
                            vpot_display_text.set_text('dvcNme', 'No')  # could just leave as default blank spaces
                    else:
                        s.unlight_vpot_leds()

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                elif s_index < encoder_28_index:
                    # changed from 29, which means that the 12th send will not be shown on the C4, but who needs 12 sends that anyway?
                    # if you wanna get back to 12 sends being shown, out-comment all encoder_28_index stuff and change "elif s_index < encoder_28_index" to 29
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

                elif s_index == encoder_28_index:
                    self.returns_switch = 0
                    if self.__filter_mst_trk:
                        if self.selected_track.solo is not True:
                            vpot_display_text.set_text(None, 'Solo')  # this is static text
                        else:
                            vpot_display_text.set_text(None, 'Solo')  # text never updates from here

                    elif not self.__filter_mst_trk:
                        vpot_display_text.set_text(None, 'Master')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                elif s_index == encoder_29_index:
                    self.returns_switch = 0
                    if self.__filter_mst_trk:
                        vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                        if is_armable_track_selected:
                            is_armed = self.selected_track.arm
                            if is_armed:
                                vpot_display_text.set_text(is_armed, 'RecArm')  # this is static text
                            else:
                                vpot_display_text.set_text(is_armed, 'RecArm')  # text never updates from here
                        else:
                            vpot_display_text.set_text('Never', 'RecArm')
                    elif not self.__filter_mst_trk:
                        vpot_display_text.set_text(None, 'Master')

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)

                elif s_index == encoder_30_index:
                    vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                    if self.__filter_mst_trk:
                        is_muted = self.selected_track.mute
                        if is_muted:
                            vpot_display_text.set_text(is_muted, 'Mute')  # this is static text
                        else:
                            vpot_display_text.set_text(is_muted, 'Mute')  # text never updates from here

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_31_index:
                    if self.selected_track.has_audio_output:
                        # lower == value, upper == value label
                        vpot_display_text.set_text(self.selected_track.mixer_device.panning, 'Pan')  # static text
                        vpot_param = (self.selected_track.mixer_device.panning, VPOT_DISPLAY_BOOST_CUT)  # the actual param
                    # else:
                        # plain midi tracks for example don't have audio output, no "Pan" per se

                    s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                    self.__display_parameters.append(vpot_display_text)
                elif s_index == encoder_32_index:
                    if self.selected_track.has_audio_output:
                        # lower == value, upper == value label)
                        vpot_display_text.set_text(self.selected_track.mixer_device.volume, 'Volume')
                        vpot_param = (self.selected_track.mixer_device.volume, VPOT_DISPLAY_WRAP)
                    else:
                        # plain midi tracks do NOT have "Volume Sliders", so KEEP MOVING, NOTHING TO SHOW HERE
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
                # if s_index < encoder_07_index:
                #     Only display text
                if s_index == encoder_07_index:
                    if self.__chosen_plugin is None:
                        vpot_display_text.set_text('Device', 'EditMe')
                        s.unlight_vpot_leds()
                    elif current_device_bank_param_track > 0:
                        vpot_display_text.set_text('<<  - ', 'PrvBnk')
                        s.show_full_enlighted_poti()
                    else:
                        vpot_display_text.set_text(' Bank ', 'NoPrev')
                        s.unlight_vpot_leds()
                elif s_index == encoder_08_index:
                    if self.__chosen_plugin is None:
                        vpot_display_text.set_text('Device', 'No')
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
                    else:
                        vpot_display_text.set_text('Param', ' No ')

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_FUNCTION:
            # ????  in the "button pressed" method, "Play" and "Stop" are different encoder buttons ????
            # here if the song is playing or stopped is written over just encoder 26

            for s in self.__encoders:
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)
                vpot_display_text.set_encoder_controller(self)  # also sets associated Encoder reference
                # this is where a "placeholder" internal_parameter object could replace None
                dummy_param = (None, VPOT_DISPLAY_BOOLEAN)
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

                if s.vpot_index() == encoder_01_index:
                    vpot_display_text.set_text('unfllw', 'follow')
                elif s.vpot_index() == encoder_02_index:
                    vpot_display_text.set_text('on/off', 'Loop')
                elif s.vpot_index() == encoder_03_index:
                    vpot_display_text.set_text('Detail', 'Clip/')
                elif s.vpot_index() == encoder_04_index:
                    vpot_display_text.set_text('Arrang', 'Sessn')
                elif s.vpot_index() == encoder_05_index:
                    vpot_display_text.set_text('on/off', 'Browsr')
                elif s.vpot_index() == encoder_06_index:
                    vpot_display_text.set_text('all', 'unsolo')
                elif s.vpot_index() == encoder_07_index:
                    vpot_display_text.set_text('all', 'unmute')
                elif s.vpot_index() == encoder_08_index:
                    vpot_display_text.set_text('Arrang', 'Back 2')
                elif s.vpot_index() == encoder_09_index:
                    vpot_display_text.set_upper_text_and_alt('undo', '------')
                elif s.vpot_index() == encoder_10_index:
                    vpot_display_text.set_upper_text_and_alt('redo', '------')
                elif s.vpot_index() == encoder_11_index:
                    vpot_display_text.set_text('all', 'unarm')
                # elif s.vpot_index() == encoder_12_index:
                #     # time display was moved to on_update_display_timer because song position needs to be updated in real-time

                elif s.vpot_index() == encoder_25_index:
                    dummy_param = (None, VPOT_DISPLAY_WRAP)
                    if self.song().is_playing:
                        vpot_display_text.set_text(' Play ', ' Song ')
                    else:
                        vpot_display_text.set_text(' Stop ', ' Song ')
                elif s.vpot_index() == encoder_26_index:
                    dummy_param = (None, VPOT_DISPLAY_WRAP)
                    if not self.song().is_playing:
                        vpot_display_text.set_text(' Play ', ' Song ')
                    else:
                        vpot_display_text.set_text(' Stop ', ' Song ')
                elif s.vpot_index() == encoder_27_index:
                    dummy_param = (None, VPOT_DISPLAY_WRAP)
                    if not self.song().is_playing:
                        vpot_display_text.set_text('contin', ' Song ')
                    else:
                        vpot_display_text.set_text(' Stop ', ' Song ')
                elif s.vpot_index() == encoder_28_index:
                    vpot_display_text.set_text('on/off', 'Ovrdub')

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        elif self.__assignment_mode == C4M_USER:
            for s in self.__encoders:
                s_index = s.vpot_index()
                vpot_display_text = EncoderDisplaySegment(self, s_index)
                vpot_display_text.set_encoder_controller(self)  # also sets associated Encoder reference
                vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

                vpot_display_text.set_text('', '')
                # can only write a "long message" (more than 6 or 7 chars)
                # like this if it won't interfere with subsequent Display segments
                # only the first 56 bytes or whatever of any string fit on the LCDs
                if s_index == row_00_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 0'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text.set_text(bottom_line, top_line)
                elif s_index < row_00_encoders[4]:
                    vpot_param = (None, VPOT_DISPLAY_BOOST_CUT)
                elif s_index < row_01_encoders[0]:
                    vpot_param = (None, VPOT_DISPLAY_WRAP)
                elif s_index == row_01_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 1'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text.set_text(bottom_line, top_line)
                elif s_index < row_01_encoders[4]:
                    vpot_param = (None, VPOT_DISPLAY_SPREAD)
                elif s_index < row_02_encoders[0]:
                    vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                elif s_index == row_02_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 2'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text.set_text(bottom_line, top_line)
                elif s_index < row_02_encoders[4]:
                    vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)
                elif s_index < row_03_encoders[0]:
                    vpot_param = (None, VPOT_DISPLAY_BOOST_CUT)
                elif s_index == row_03_encoders[0]:
                    top_line = 'Welcome to C4'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    bottom_line = 'USER mode row 3'.center(NUM_CHARS_PER_DISPLAY_LINE)
                    vpot_display_text.set_text(bottom_line, top_line)
                elif s_index < row_03_encoders[4]:
                    vpot_param = (None, VPOT_DISPLAY_WRAP)
                else:
                    vpot_param = (None, VPOT_DISPLAY_SPREAD)

                s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
                self.__display_parameters.append(vpot_display_text)

        return

    def on_update_display_timer(self):
        """Called by a timer which gets called every 100 ms. This is where the real time updating of the displays is happening"""
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
        self.__display_repeat_count += 1  # see comments near lines 97 - 102 in __init__

        # uncommenting this condition check when the two lengths are not equal
        # will result in spamming the log file with the indented log message
        # If you comment out initializing self.__display_parameters with EncoderDisplaySegment objects
        # inside __init__ above, and just leave the empty list assignment self.__display_parameters = []
        # you can force the two lengths to not be equal here after the script loads,
        # but for example before the first "track change" message is processed when everything "reloads"

        # dsply_sgmts = len(self.__display_parameters)
        # encdr_range = len(encoder_range)
        # if dsply_sgmts != encdr_range:
        #     self.main_script().log_message("display segments loaded {0} encoder range {1}"
        #                                    .format(dsply_sgmts, encdr_range))
        encoder_28_index = 27
        encoder_29_index = 28
        encoder_30_index = 29
        encoder_31_index = 30
        encoder_32_index = 31
        if self.__assignment_mode == C4M_CHANNEL_STRIP:

            # shows "fold" or "unfold" or nothing depending on if group or grouped
            if track_util.is_group_track(self.selected_track) or (track_util.is_grouped(self.selected_track)):
                if track_util.is_folded(self.selected_track):
                    upper_string1 += '-------Track--------' + ' unfold---------------'
                elif not track_util.is_folded(self.selected_track):
                    upper_string1 += '-------Track--------' + ' fold  -----------------'
            else:
                upper_string1 += '-------Track--------       ---------------'

            # "selected track's name, centered over roughly the first 3 encoders in top row
            if liveobj_valid(self.selected_track):
                lower_string1 += adjust_string(self.selected_track.name, 20)
            else:
                lower_string1 += "---------0--------1"

            if self.application().view.is_view_visible('Session'):
                lower_string1 += (' Group' if (track_util.is_group_track(self.selected_track) or (track_util.is_grouped(self.selected_track))) else '       ')
            elif self.application().view.is_view_visible('Arranger'):
                lower_string1 += ' Track '

            if liveobj_valid(self.selected_track) and liveobj_valid(self.selected_track.view.selected_device):
                lower_string1 += adjust_string(self.selected_track.view.selected_device.name, 15)
            else:
                lower_string1 += '                      '

            # This text 'covers' display segments over all 8 encoders in the second row
            upper_string2 += '------------------------Devices------------------------'

            for t in encoder_range:
                try:
                    text_for_display = next(x for x in self.__display_parameters if (x.filter_index(t)))
                except StopIteration:
                    text_for_display = EncoderDisplaySegment(self, t)
                    text_for_display.set_text('zzzzzz', 'ZZZZZZ')

                u_alt_text = text_for_display.get_upper_text()
                l_alt_text = text_for_display.get_lower_text()

                if t in range(6, NUM_ENCODERS_ONE_ROW):
                    upper_string1 += adjust_string(u_alt_text, 6)
                    upper_string1 += ' '
                    lower_string1 += adjust_string(str(l_alt_text), 6)
                    lower_string1 += ' '
                elif t in row_01_encoders:
                    lower_string2 += adjust_string(str(l_alt_text), 6)
                    lower_string2 += ' '
                elif t in row_02_encoders:
                    lower_string3 += adjust_string(l_alt_text, 6)
                    lower_string3 += ' '
                    upper_string3 += adjust_string(u_alt_text, 6)
                    upper_string3 += ' '
                elif t in row_03_encoders:
                    if t < encoder_28_index:
                        lower_string4 += adjust_string(l_alt_text, 6)
                        lower_string4 += ' '
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '

                    if t == encoder_28_index:
                        if liveobj_valid(self.selected_track):
                            if self.__filter_mst_trk:
                                if self.selected_track.solo:
                                    l_alt_text = "ON"
                                    self.__encoders[encoder_28_index].show_full_enlighted_poti()
                                else:
                                    l_alt_text = "OFF"
                                    self.__encoders[encoder_28_index].unlight_vpot_leds()
                            else:
                                l_alt_text = "NoSolo"

                        lower_string4 += adjust_string(l_alt_text, 6)
                        lower_string4 += ' '
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '

                    elif t == encoder_29_index:
                        if liveobj_valid(self.selected_track):
                            if self.selected_track.can_be_armed:
                                if self.selected_track.arm:
                                    l_alt_text = "ON"
                                    self.__encoders[encoder_29_index].show_full_enlighted_poti()
                                else:
                                    l_alt_text = "OFF"
                                    self.__encoders[encoder_29_index].unlight_vpot_leds()
                            else:
                                l_alt_text = "No Arm"

                        lower_string4 += adjust_string(l_alt_text, 6)
                        lower_string4 += ' '
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '
                    elif t == encoder_30_index:
                        if self.selected_track != self.song().master_track and liveobj_valid(self.selected_track):
                            if self.selected_track.mute:
                                l_alt_text = "ON"
                                self.__encoders[encoder_30_index].show_full_enlighted_poti()
                            else:
                                l_alt_text = "OFF"
                            lower_string4 += adjust_string(l_alt_text, 6)
                            self.__encoders[encoder_30_index].unlight_vpot_leds()
                        else:
                            lower_string4 += adjust_string(l_alt_text, 6)
                        lower_string4 += ' '
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '
                        # if self.__filter_mst_trk:
                        #     if liveobj_valid(self.selected_track):
                        #         if self.selected_track.mute:
                        #             lower_string4 += '  ON   '  # refactor to DisplaySegment text?
                        #             upper_string4 += ' MUTE  '
                        #         else:
                        #             lower_string4 += ' Off   '
                        #             upper_string4 += ' Mute  '
                        # else:
                        #     lower_string4 += '       '
                        #     upper_string4 += '       '
                    elif t == encoder_31_index:
                        lower_string4 += adjust_string(str(l_alt_text), 6)
                        lower_string4 += ' '
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '
                        # if liveobj_valid(self.selected_track):
                        #     if self.selected_track.has_audio_output:
                        #         upper_string4 += ' Pan   '  # refactor to DisplaySegment text?
                        # else:
                        #     upper_string4 += '       '
                    elif t == encoder_32_index:
                        lower_string4 += adjust_string(str(l_alt_text), 6)
                        lower_string4 += ' '
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '
                        # if liveobj_valid(self.selected_track):
                        #     if self.selected_track.has_audio_output:
                        #         upper_string4 += 'Volume '  # refactor to DisplaySegment text?
                        # else:
                        #     upper_string4 += '       '
        so_many_spaces = '                                                       '

        if self.__assignment_mode == C4M_PLUGINS:
            upper_string1 += '-------Track-------- -----Device '
            # upper_string1 += str(self.t_d_current[self.t_current])
            upper_string1 += str(self.__eah.get_selected_device_index())
            # if self.t_d_current[self.t_current] > 9:  # allow for tens track device number digit
            if self.__eah.get_selected_device_index() > 9:
                upper_string1 += '------ '
            else:
                upper_string1 += '------- '

            # upper_string1 == '-------Track-------- -----Device 10------ ' for example

            if liveobj_valid(self.selected_track):
                lower_string1a += adjust_string(self.selected_track.name, 20)
            else:
                lower_string1a += "---------0---------1"
            lower_string1a = lower_string1a.center(20)
            lower_string1a += ' '
            if not liveobj_valid(self.__chosen_plugin):
                # blank everything out
                upper_string1 += '             '
                lower_string1b += '                                   '
                lower_string1 += lower_string1a
                lower_string1 += lower_string1b
                upper_string2 += '           NO DEVICES SELECTED ON THIS TRACK           '
                # so_many_spaces '                                                       '
                lower_string2 += so_many_spaces
                upper_string3 += so_many_spaces
                lower_string3 += so_many_spaces
                upper_string4 += so_many_spaces
                lower_string4 += so_many_spaces
            else:
                device_name = '  '
                t_d_idx = self.__eah.get_selected_device_index()
                if t_d_idx > -1:
                    if liveobj_valid(self.selected_track) and len(self.selected_track.devices) > t_d_idx:
                        if liveobj_valid(self.selected_track.devices[t_d_idx]):
                            device_name = self.selected_track.devices[t_d_idx].name
                        else:
                            msg = "selected track and device index were valid but the device "
                            msg += "at index {0} is not liveobj_valid() Danger! Will Robinson! Danger!"
                            self.main_script().log_message(msg.format(t_d_idx))
                    else:
                        msg = "Not enough devices loaded for index and __chosen_device is liveobj_valid()"
                        msg += " name display blank over device index {0} Danger! Will Robinson! Danger!"
                        self.main_script().log_message(msg.format(t_d_idx))
                else:
                    msg = "Current Track Device List length too short for index:"
                    msg += " name display blank over device index {0}"
                    self.main_script().log_message(msg.format(t_d_idx))
                lower_string1b += adjust_string(str(device_name), 20)
                lower_string1b = lower_string1b.center(20)
                lower_string1 += lower_string1a
                lower_string1 += lower_string1b
                lower_string1 += ' '
                upper_string1 += '-Params Bank-'
                for t in encoder_range:
                    try:
                        text_for_display = self.__display_parameters[t]  # assumes there are always 32
                    except IndexError:
                        text_for_display = EncoderDisplaySegment(self, t)
                        text_for_display.set_text('---', ' X ')

                    u_alt_text = text_for_display.get_upper_text()
                    l_alt_text = text_for_display.get_lower_text()

                    if t in range(6, NUM_ENCODERS_ONE_ROW):
                        lower_string1 += adjust_string(str(l_alt_text), 6)
                        lower_string1 += ' '
                    elif t in row_01_encoders:
                        # parameter name plugin_param[1] == text_for_display[1] in top display row,
                        # parameter value plugin_param[0] == text_for_display[0] in bottom row
                        upper_string2 += adjust_string(u_alt_text, 6)
                        upper_string2 += ' '
                        lower_string2 += adjust_string(str(l_alt_text), 6)
                        lower_string2 += ' '
                    elif t in row_02_encoders:
                        upper_string3 += adjust_string(u_alt_text, 6)
                        upper_string3 += ' '
                        lower_string3 += adjust_string(str(l_alt_text), 6)
                        lower_string3 += ' '
                    elif t in row_03_encoders:
                        upper_string4 += adjust_string(u_alt_text, 6)
                        upper_string4 += ' '
                        lower_string4 += adjust_string(str(l_alt_text), 6)
                        lower_string4 += ' '

        elif self.__assignment_mode == C4M_FUNCTION:

            encoder_09_index = 8
            encoder_10_index = 9
            encoder_12_index = 11
            # encoder_13_index is covered / occupied by SPP from 12
            encoder_14_index = 12  # because 12 is occupied, we still need 12 otherwise everything be shifted over
            encoder_15_index = 13
            encoder_25_index = 24
            encoder_26_index = 25
            for e in self.__encoders:

                dspl_sgmt = next(x for x in self.__display_parameters if x.vpot_index() == e.vpot_index())
                if e.vpot_index() in row_00_encoders:
                    upper_string1 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                    lower_string1 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                elif e.vpot_index() in row_01_encoders:
                    if e.vpot_index() == encoder_09_index:
                        upper_string2 += adjust_string(dspl_sgmt.alter_upper_text(self.song().can_undo), 6) + ' '
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                    elif e.vpot_index() == encoder_10_index:
                        upper_string2 += adjust_string(dspl_sgmt.alter_upper_text(self.song().can_redo), 6) + ' '
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '

                    # show beat position pointer or SPP at encoder 12 AND encoder 13 position in second row
                    elif e.vpot_index() == encoder_12_index:
                        if self.__time_display.TimeDisplay__show_beat_time:
                            time_string = str(self.song().get_current_beats_song_time()) + ' '
                            upper_string2 += 'Bar:Bt:Sb:Tik '
                            lower_string2 += time_string
                        else:
                            time_string = str(self.song().get_current_smpte_song_time(self.__time_display.TimeDisplay__smpt_format)) + ' '
                            upper_string2 += 'Hrs:Mn:Sc:Fra '
                            lower_string2 += time_string

                    # show loop length
                    elif e.vpot_index() == encoder_14_index:
                        get_loop_length = str(self.song().loop_length)
                        upper_string2 += 'LoopLg '
                        lower_string2 += adjust_string(get_loop_length, 6) + ' '

                    # show loop start
                    elif e.vpot_index() == encoder_15_index:
                        get_loop_start = str(self.song().loop_start)
                        upper_string2 += 'LoopSt '
                        lower_string2 += adjust_string(get_loop_start, 6) + ' '

                    else:
                        upper_string2 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                elif e.vpot_index() in row_02_encoders:
                    upper_string3 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                    lower_string3 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                elif e.vpot_index() in row_03_encoders:
                    upper_string4 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                    lower_string4 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '

            unsolo_all_encoder_index = 5
            unsolo_all_encoder = self.__encoders[unsolo_all_encoder_index]
            if song_util.any_soloed_track(self):
                unsolo_all_encoder.show_full_enlighted_poti()  # some track is soloed (unsolo has something to do)
            else:
                unsolo_all_encoder.unlight_vpot_leds()  # no tracks are soloed

            unmute_all_encoder_index = 6
            unmute_all_encoder = self.__encoders[unmute_all_encoder_index]

            if song_util.any_muted_track(self):
                unmute_all_encoder.show_full_enlighted_poti()  # some track is muted (unmute has something to do)
            else:
                unmute_all_encoder.unlight_vpot_leds()  # no tracks are muted

        elif self.__assignment_mode == C4M_USER:

            this_pass = self.__display_repeat_count + 1  # + 1 so we don't begin at zero
            for s in self.__encoders:

                reverse = (this_pass % self.__display_repeat_timer) % 2 > 0
                s.animate_v_pot_led_ring(this_pass, reverse)

                s_index = s.vpot_index()
                try:
                    text_for_display = self.__display_parameters[s_index]  # assumes there are always 32
                except IndexError:
                    text_for_display = EncoderDisplaySegment(self, s_index)
                    text_for_display.set_text('---', ' Z ')

                if s_index == row_00_encoders[0]:
                    upper_string1 += text_for_display.get_upper_text()
                    lower_string1 += text_for_display.get_lower_text()
                elif s_index == row_01_encoders[0]:
                    upper_string2 += text_for_display.get_upper_text()
                    lower_string2 += text_for_display.get_lower_text()
                elif s_index == row_02_encoders[0]:
                    upper_string3 += text_for_display.get_upper_text()
                    lower_string3 += text_for_display.get_lower_text()
                elif s_index == row_03_encoders[0]:
                    upper_string4 += text_for_display.get_upper_text()
                    lower_string4 += text_for_display.get_lower_text()

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

    def send_display_string1(self, display_address, text_for_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Angled display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_for_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages1[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 3
        if is_update or is_stale:  # don't send the same sysex message back-to-back unless the repeat timer pops
            self.__last_send_messages1[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def send_display_string2(self, display_address, text_for_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Top-flat display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_for_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages2[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 2
        if is_update or is_stale:
            self.__last_send_messages2[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def send_display_string3(self, display_address, text_for_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Middle-flat display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_for_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages3[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 1
        if is_update or is_stale:
            self.__last_send_messages3[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def send_display_string4(self, display_address, text_for_display, display_row_offset, cursor_offset=0):
        """
            sends a sysex message to C4 device
            (display_address == Bottom-flat display, display_row_offset == top row or bottom row)
        """
        ascii_text_sysex_ints = self.__generate_sysex_body(text_for_display, display_row_offset, cursor_offset)
        is_update = self.__last_send_messages4[display_address][display_row_offset] != ascii_text_sysex_ints
        is_stale = self.__display_repeat_count % self.__display_repeat_timer == 0
        if is_update or is_stale:
            self.__last_send_messages4[display_address][display_row_offset] = ascii_text_sysex_ints
            sysex_msg = SYSEX_HEADER + (display_address, display_row_offset) + tuple(ascii_text_sysex_ints) + \
                        (SYSEX_FOOTER,)
            self.send_midi(sysex_msg)

    def __generate_sysex_body(self, text_for_display, display_row_offset, cursor_offset=0):

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
        ascii_text_sysex_ints = [ord(c) for c in text_for_display]
        for i in range(len(ascii_text_sysex_ints)):
            if ascii_text_sysex_ints[i] > MIDI_DATA_LAST_VALID:

                # replace any integer values above the ASCII 7-bit (MIDI_DATA) range (0x00 - 0x7F)
                # replacement value is the code for #
                ascii_text_sysex_ints[i] = ASCII_HASH

        return ascii_text_sysex_ints

    def refresh_state(self):
        for s in self.__encoders:
            s.refresh_state()
