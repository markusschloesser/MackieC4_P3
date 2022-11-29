from .V2C4Component import *

import Live

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement

from .C4EncoderElement import C4EncoderElement
from .C4Encoders import C4Encoders

#
# SYSEX midi messages beginning with 0xF0  and end with 0xF7
# CC    midi messages beginning with 0xB0 (The C4 only uses midi channel 1, so 0xB0 only)
# Note  midi messages beginning with 0x90 (The C4 only uses midi channel 1, so 0x90 only)
#
# The 4 LCD screens are addressed using midi SYSEX messages
# The 32 "endless encoders" (and their associated "LED rings") are addressed using midi CC messages
# The 32 + 19 "buttons" (and their associated "LEDs") are addressed using midi Note messages
#
# The 32 "encoder knobs" and 32 "encoder buttons" use the same message number, but CC versus Note message type
# (0xB0, 0x20, 0x7F) is a CC message from encoder knob 0 with CC value 127
# (0x90, 0x20, 0x7F) is a Note message from encoder button 0 with Note value (velocity) 127
# (0xB0, 0x20, 0x7F) is also a CC message TO encoder LED Ring 0 with CC value 127
#
#
# scratch comments
# SYSEX_HEADER = (0xF0, 0, 0, 0x66, 0x17)  # (240, 0, 0, 102, 23)
# SYSEX_FOOTER = 0xF7  # 247
# sysex_msg = SYSEX_HEADER + (LCD_xxx_ADDRESS, LCD_yyy_ROW_OFFSET) + tuple(ascii_text_sysex_ints) + (SYSEX_FOOTER,)
#
# message from the C4 logged by _Framework.ControlSurface base class
# C4 sends this message at "power on" and "LCD wake-up",  also after it receives
# # whatever SYSEX message displays the Mackie welcome
# (240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 65, 51, 6, 0, 247)
# (240, 0, 0, 102, 23)     Z,  T,  1,  0,  4,  7,  3,  A,  3,  ,  ,(247)
#
# The serial number of my C4 is ZT10473.  A3 might indicate firmware version?  mine is 3.0.0 per the Mackie Welcome
#
#


class C4ElementFactory:

    __module__ = __name__

    def __init__(self):
        pass

    @staticmethod
    def make_button(identifier, channel=0, is_momentary=True, *a, **k):
        #   is_momentary: True because C4 buttons send a message on being released
        # MIDI_NOTE_TYPE: because C4 buttons send and receive "Midi Note" messages (0x90 id byte)
        #        channel: 0 because the C4 communicates on channel 0
        return ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, identifier, *a, **k)

    @staticmethod
    def make_encoder(identifier, name=None, *a, **k):
        return C4EncoderElement(identifier, name, *a, **k)

    @staticmethod
    def make_framework_encoder(identifier, *a, **k):
        return EncoderElement(MIDI_CC_TYPE, C4_MIDI_CHANNEL, identifier,
                              Live.MidiMap.MapMode.relative_signed_bit, *a, **k)

    @staticmethod
    def make_encoder_and_button(common_identifier, channel=0, is_momentary=True, name='', *a, **k):
        # if len(name) < 1:
        #     name = 'Encoder'
        # button_name = '%s_Button' % name
        # button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, common_identifier, name=button_name, *a, **k)
        # encoder = C4EncoderElement(common_identifier, name=name, *a, **k)
        button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, common_identifier, *a, **k)
        encoder = C4EncoderElement(common_identifier, *a, **k)
        encoder.set_encoder_button(button)
        return encoder


