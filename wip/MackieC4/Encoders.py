# was Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/Encoders.py
# Compiled at: 2011-01-13 21:07:51
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals  # MS
from . MackieC4Component import *
from ableton.v2.base import liveobj_valid  # MS

import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

from _Framework.ControlSurface import ControlSurface  # MS
from _Framework.Control import Control  # MS
from itertools import chain
from ableton.v2.base import liveobj_valid  # MS not needed right now, but will in the future


class Encoders(MackieC4Component):
    """ Represents one encoder of the Mackie C4 """
    __module__ = __name__

    def __init__(self, main_script, vpot_index):
        MackieC4Component.__init__(self, main_script)
        self.within_destroy = False
        self.__encoder_controller = None
        self.__vpot_index = vpot_index
        self.__vpot_cc_nbr = vpot_index + C4SID_VPOT_CC_ADDRESS_BASE
        self.__v_pot_parameter = None
        self.__v_pot_display_mode = VPOT_DISPLAY_SINGLE_DOT
        self._Encoders__assigned_track = None
        return

    # function provided by MackieC4Component super
    def destroy(self):
        # self.destroy()
        self.within_destroy = True
        self.unlight_vpot_leds()
        self.refresh_state()
        MackieC4Component.destroy(self)
        self.within_destroy = False

    def set_encoder_controller(self, encoder_controller):
        self.__encoder_controller = encoder_controller

    def vpot_index(self):
        return self.__vpot_index

    def v_pot_parameter(self):
        return self.__v_pot_parameter

    def set_v_pot_parameter(self, parameter, display_mode=VPOT_DISPLAY_BOOLEAN):
        self.__v_pot_display_mode = display_mode
        self.__v_pot_parameter = parameter
        if not parameter:
            self.unlight_vpot_leds()

    def unlight_vpot_leds(self):
        data2 = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_BOOLEAN][0]
        # midi CC messages (0xB0, 0x20, data) (CC_STATUS, C4SID_VPOT_CC_ADDRESS_1, data)
        self.send_midi((CC_STATUS, self.__vpot_cc_nbr, RING_LED_ALL_OFF))

    def show_full_enlighted_poti(self):
        data2 = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_BOOLEAN][1]
        # midi CC messages (0xB0, 0x20, data) (CC_STATUS, C4SID_VPOT_CC_ADDRESS_1, data)
        self.send_midi((CC_STATUS, self.__vpot_cc_nbr, data2))

    def build_midi_map(self, midi_map_handle):
        needs_takeover = False
        encoder = self.__vpot_index
        param = self.__v_pot_parameter
        if liveobj_valid(param):

            feedback_rule = Live.MidiMap.CCFeedbackRule()  # MS interestingly in ALL Mackie scripts this is originally "feeback_rule" without the "d"
            feedback_rule.channel = 0  # MS now with the stub installed, pycharm says that according to Live this "cannot be set", lets try without. Doesn't make a difference
            feedback_rule.cc_no = self.__vpot_cc_nbr  # MS now with the stub installed, pycharm says that according to Live this "cannot be set", lets try without. Doesn't make a difference
            display_mode_cc_base = encoder_ring_led_mode_cc_values[self.__v_pot_display_mode][0]
            range_end = encoder_ring_led_mode_cc_values[self.__v_pot_display_mode][1] - display_mode_cc_base
            feedback_rule.cc_value_map = tuple([display_mode_cc_base + x for x in range(range_end)])  # MS now with the stub installed, pycharm says that according to Live this "cannot be set", lets try without. Doesn't make a difference
            feedback_rule.delay_in_ms = -1.0  # MS now with the stub installed, pycharm says that according to Live this "cannot be set", lets try without. Doesn't make a difference
            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, param, 0, encoder, Live.MidiMap.MapMode.relative_signed_bit, feedback_rule, needs_takeover, sensitivity=1.0)  # MS "sensitivity" added
            self.main_script().log_message("potIndex<{}> feedback<{}> mapped".format(encoder, param))
            #  MS: now wtf does the line give a Boost Error with:
            #  RemoteScriptError: Python argument types in
            #  MidiMap.map_midi_cc_with_feedback_map(int, DeviceParameter, int, int, MapMode, CCFeedbackRule, bool)
            #  did not match C++ signature:
            #  map_midi_cc_with_feedback_map(unsigned int midi_map_handle, class TPyHandle<class ATimeableValue> parameter, int midi_channel, int controller_number, enum NRemoteMapperTypes::TControllerMapMode map_mode, class NPythonMidiMap::TCCFeedbackRule feedback_rule, bool avoid_takeover, float sensitivity=1.0)
            #  maybe LOM thing??
            # _Framework.ControlSurface first does an "installmapping" and then uses that to do a "buildmidimap"

            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, param)
        else:
            if not liveobj_valid(param):
                if param is None:
                    channel = 0
                    cc_no = self.__vpot_cc_nbr
                    Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, channel, cc_no)
                    self.main_script().log_message(
                        "potIndex<{0}> mapping encoder to forward CC <{1}>".format(encoder, cc_no))
                else:
                    self.main_script().log_message("potIndex<{0}> nothing mapped param is lost weakref".format(encoder))
            else:
                self.main_script().log_message("potIndex<{0}> nothing mapped param <{1}>".format(encoder, param))


    def assigned_track(self):
        return self._Encoders__assigned_track

    def __assigned_track_index(self):  # MS new from Mackie Control.ChannelStrip
        index = 0
        for t in chain(self.song().visible_tracks, self.song().return_tracks):
            if t == self._Encoders__assigned_track:
                return index
            index += 1

        if self._Encoders__assigned_track:
            pass

    def __select_track(self):
        #  pass  # MS: SISSY put this pass in, and commented everything following out, why? lets try reversing that
        #  lots of changes here, trying to do what mackie control does
        if self._Encoders__assigned_track:
            all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)  # MS tuple is new and from Mackie script
            if self.song().view.selected_track != all_tracks[self.__assigned_track_index()]:  # MS new but seems to work
                self.song().view.selected_track = all_tracks[self.__assigned_track_index()]
            elif self.application().view.is_view_visible('Arranger'):
                if self._Encoders__assigned_track:
                    self._Encoders__assigned_track.view.is_collapsed = not self._Encoders__assigned_track.view.is_collapsed

    def refresh_state(self):
        return ' '

    def on_update_display_timer(self):
        pass
