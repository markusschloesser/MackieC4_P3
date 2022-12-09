# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\scroll.py
# Compiled at: 2021-01-27 15:20:55
# Size of source mod 2**32: 733 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import nop
from ableton.v2.control_surface.components import ScrollComponent as ScrollComponentBase
from ableton.v2.control_surface.control import EncoderControl


class ScrollComponent(ScrollComponentBase):
    scroll_encoder = EncoderControl()

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        scroll_step = nop
        if value > 0 and self.can_scroll_down():
            scroll_step = self._do_scroll_down
        else:
            if value < 0:
                if self.can_scroll_up():
                    scroll_step = self._do_scroll_up
        scroll_step()
