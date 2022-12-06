# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Code_Series\element_utils.py
# Compiled at: 2021-01-27 15:20:47
# Size of source mod 2**32: 910 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE
from ableton.v2.control_surface.elements import ButtonElement, EncoderElement, SliderElement
IS_MOMENTARY = True
CHANNEL = 0

@depends(skin=None)
def make_button(identifier, name, **k):
    return ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, CHANNEL, identifier, name=name, **k)


def make_slider(channel, name):
    return SliderElement(MIDI_PB_TYPE, channel, 0, name=name)


def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE,
      0,
      identifier,
      (Live.MidiMap.MapMode.relative_smooth_signed_bit),
      name=name)
