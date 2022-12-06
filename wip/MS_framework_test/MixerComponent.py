# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\MixerComponent.py
# Compiled at: 2021-03-17 12:36:39
# Size of source mod 2**32: 1635 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from builtins import range
import _Framework.MixerComponent as MixerComponentBase


class MixerComponent(MixerComponentBase):

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)
