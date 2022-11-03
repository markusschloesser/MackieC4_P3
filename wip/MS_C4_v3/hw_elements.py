# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\elements.py
# Compiled at: 2021-03-17 12:36:39
# Size of source mod 2**32: 4080 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import object
from functools import partial
import Live
from ableton.v2.base import depends, recursive_map
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement
SESSION_WIDTH = 8
SESSION_HEIGHT = 4


@depends(skin=None)
def create_button(identifier, name, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_signed_bit, name=name, **k)


class HW_Elements(object):

    def __init__(self, *a, **k):
        (super(HW_Elements, self).__init__)(*a, **k)
        self.shift_button = create_button(0x0D,
          'Shift_Button', resource_type=PrioritizedResource)

        self.bank_button = create_button(26, 'Bank_Button')

        self.up_button = create_button(0x11, 'Up_Button')
        self.down_button = create_button(0x12, 'Down_Button')
        self.left_button = create_button(0x13, 'Left_Button')
        self.right_button = create_button(0x14, 'Right_Button')

        self.pads_raw = [[create_button((offset + col_index), ('{}_Pad_{}'.format(col_index, row_index)), msg_type=MIDI_NOTE_TYPE) for col_index in range(SESSION_WIDTH)] for row_index, offset in enumerate(range(48, 32, -4))]
        self.pads = ButtonMatrixElement(rows=(self.pads_raw), name='Pads')

        def with_modifier(modifier_button, button):
            return ComboElement(control=button,
              modifier=modifier_button,
              name=('{}_With_{}'.format(button.name, modifier_button.name.split('_')[0])))

        self.pads_with_shift = ButtonMatrixElement(name='Pads_With_Shift',
          rows=(recursive_map(partial(with_modifier, self.shift_button), self.pads_raw)))
        self.encoders = ButtonMatrixElement(rows=[
         [create_encoder(index + 14, 'Encoder_{}'.format(index)) for index in range(4)]],
          name='Encoders')
