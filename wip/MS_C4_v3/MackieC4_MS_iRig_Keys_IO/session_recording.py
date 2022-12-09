# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\session_recording.py
# Compiled at: 2021-01-27 15:20:55
# Size of source mod 2**32: 550 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.control import ButtonControl


class SessionRecordingComponent(SessionRecordingComponentBase):
    record_stop_button = ButtonControl()

    @record_stop_button.pressed
    def record_stop_button(self, _):
        self.song.session_record = False
