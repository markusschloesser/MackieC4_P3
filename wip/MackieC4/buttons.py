# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\elements.py
# Compiled at: 2021-03-17 12:36:39
# Size of source mod 2**32: 14773 bytes
from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range
    from builtins import object
import Live
from ableton.v2.base import depends, mixin
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.control_element import ControlElement
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement, SliderElement, SysexElement
from ableton.v2.control_surface.elements.physical_display import *
from . import consts


DISPLAY_LINE_WIDTH = consts.NUM_CHARS_PER_DISPLAY_LINE
NUM_DISPLAY_LINE_SEGMENTS = 6


@depends(skin=None)
def create_button(identifier, name, channel=0, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


def create_text_display_line(v_position):
    display = mixin(ControlElement, PhysicalDisplayElement)(v_position=v_position,
      width_in_chars=DISPLAY_LINE_WIDTH,
      num_segments=NUM_DISPLAY_LINE_SEGMENTS,
      name=('Text_Display_{}'.format(v_position)))
    display.set_message_parts(sysex.SET_PROPERTY_MSG_HEADER, (sysex.SYSEX_END_BYTE,))
    for index in range(NUM_DISPLAY_LINE_SEGMENTS):
        display.segment(index).set_position_identifier((index,))

    return display


class Elements(object):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.up_button = create_button(85, 'Up_Button')
        self.down_button = create_button(86, 'Down_Button')

        self.options_button = create_button(90, 'Options_Button')
        self.shift_button = create_button(91,
          'Shift_Button', resource_type=PrioritizedResource)

        self.track_left_button = create_button(102, 'Track_Left_Button')
        self.track_right_button = create_button(103, 'Track_Right_Button')

        self.stop_button = create_button(114, 'Stop_Button')
        self.play_button = create_button(115, 'Play_Button')
        self.loop_button = create_button(116, 'Loop_Button')
        self.record_button = create_button(117, 'Record_Button')

        def with_shift(button):
            return ComboElement(control=button,
              modifier=(self.shift_button),
              name=('{}_With_Shift'.format(button.name)))

        self.up_button_with_shift = with_shift(self.up_button)
        self.down_button_with_shift = with_shift(self.down_button)
        self.record_button_with_shift = with_shift(self.record_button)
        self.play_button_with_shift = with_shift(self.play_button)
        self.track_left_button_with_shift = with_shift(self.track_left_button)
        self.track_right_button_with_shift = with_shift(self.track_right_button)

        self.message_display = PhysicalDisplayElement(width_in_chars=38,
          num_segments=NUM_MESSAGE_SEGMENTS,
          name='Message_Display')
        self.message_display.set_message_parts(sysex.SHOW_MESSAGE_MSG_HEADER, (sysex.SYSEX_END_BYTE,))
        self.center_display_1 = mixin(ControlElement, PhysicalDisplayElement)(v_position=0,
          width_in_chars=9,
          name='Center_Display_1')
        self.center_display_2 = mixin(ControlElement, PhysicalDisplayElement)(v_position=1,
          width_in_chars=9,
          name='Center_Display_2')
        self.mixer_display_1 = mixin(ControlElement, PhysicalDisplayElement)(v_position=2,
          width_in_chars=9,
          name='Mixer_Button_Display_1')
        self.mixer_display_2 = mixin(ControlElement, PhysicalDisplayElement)(v_position=3,
          width_in_chars=9,
          name='Mixer_Button_Display_2')
        for display in (
         self.center_display_1,
         self.center_display_2,
         self.mixer_display_1,
         self.mixer_display_2):
            display.set_message_parts(sysex.SET_PROPERTY_MSG_HEADER, (sysex.SYSEX_END_BYTE,))
            display.segment(0).set_position_identifier((8, ))

        self.text_display_line_0 = create_text_display_line(0)
        self.text_display_line_1 = create_text_display_line(1)
        self.text_display_line_2 = create_text_display_line(2)
        self.text_display_line_3 = create_text_display_line(3)
        self.text_display_line_5 = create_text_display_line(5)
        self.text_display_line_3_with_shift = with_shift(self.text_display_line_3)
        self.text_display_line_5_with_shift = with_shift(self.text_display_line_5)
        self.text_display_lines = [
         self.text_display_line_0,
         self.text_display_line_1,
         self.text_display_line_2,
         self.text_display_line_3,
         self.text_display_line_5]

        encoders = [EncoderElement(MIDI_CC_TYPE, 0, (21 + index), map_mode=(Live.MidiMap.MapMode.relative_smooth_two_compliment), name=('Encoder_{}'.format(index))) for index in range(8)]
        for encoder in encoders:
            encoder.set_feedback_delay(1)

        self.encoders = ButtonMatrixElement(rows=[encoders], name='Encoders')
