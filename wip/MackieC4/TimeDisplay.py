# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:01:55) [MSC v.1900 32 bit (Intel)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\TimeDisplay.py
# Compiled at: 2022-04-21 16:02:21
# Size of source mod 2**32: 4062 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .MackieC4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str


class TimeDisplay(MackieC4Component):

    def __init__(self, main_script):
        MackieC4Component.__init__(self, main_script)
        self._TimeDisplay__main_script = main_script
        self._TimeDisplay__show_beat_time = False
        self._TimeDisplay__smpt_format = Live.Song.TimeFormat.smpte_25
        self._TimeDisplay__last_send_time = []
        self.show_beats()

    def destroy(self):
        MackieC4Component.destroy(self)

    def show_beats(self):
        self._TimeDisplay__show_beat_time = True

    def show_smpte(self, smpte_mode):
        self._TimeDisplay__show_beat_time = False
        self._TimeDisplay__smpt_format = smpte_mode

    def toggle_mode(self):
        if self._TimeDisplay__show_beat_time:
            self.show_smpte(self._TimeDisplay__smpt_format)
        else:
            self.show_beats()

    def refresh_state(self):
        self.show_beats()
        self._TimeDisplay__last_send_time = []

    def on_update_display_timer(self):  # needed? should be covered by on_update_display_timer in EncoderController
        if self._TimeDisplay__show_beat_time:
            time_string = str(self.song().get_current_beats_song_time())
        else:
            time_string = str(self.song().get_current_smpte_song_time(self._TimeDisplay__smpt_format))
        time_string = [c for c in time_string if c not in ('.', ':')]
        if self._TimeDisplay__last_send_time != time_string:
            self._TimeDisplay__last_send_time = time_string
            self.__send_time_string(time_string, show_points=True)

    def __send_time_string(self, time_string, show_points):
        for c in range(0, 10):
            char = time_string[9 - c].upper()
            # char_code = g7_seg_led_conv_table[char]
            # if show_points:
            #     if c in (3, 5, 7):
            #         char_code += 64
            # self.send_midi((176, 64 + c, char_code))

    # @property
    def _TimeDisplay__show_beat_time(self):
        return self._TimeDisplay__show_beat_time

    @property
    def TimeDisplay__show_beat_time(self):
        return self._TimeDisplay__show_beat_time

    @property
    def TimeDisplay__smpt_format(self):
        return self._TimeDisplay__smpt_format
