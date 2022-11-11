
from .V2C4Component import *

# import Live
# from folder.file import class
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement

from .C4EncoderElement import C4EncoderElement

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


class C4ModelElements(V2C4Component):

    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)

        self.lcd_physical_displays = {0: {0: None}}
        self.lcd_display_track_name_message = tuple(V2C4Component.generate_sysex_body(
            'Track Name'.center(LCD_BOTTOM_ROW_OFFSET/2)))
        self.lcd_display_device_name_message = tuple(V2C4Component.generate_sysex_body(
            'Device Name'.center(LCD_BOTTOM_ROW_OFFSET/2)))
        self.lcd_display_hello_message = tuple(V2C4Component.generate_sysex_body(
            'Welcome to V2C4 remote script'.center(LCD_BOTTOM_ROW_OFFSET)))
        self.lcd_display_goodbye_message = tuple(V2C4Component.generate_sysex_body(
            'Ableton Live and V2C4 are offline'.center(LCD_BOTTOM_ROW_OFFSET)))
        self.lcd_display_clear_message = tuple([ASCII_SPACE for x in range(LCD_BOTTOM_ROW_OFFSET)])
        self.lcd_display_id_message = {
            LCD_ANGLED_ADDRESS:   # 0x38 == 48 + 8 == 56
                {LCD_TOP_ROW_OFFSET: tuple([ASCII_ZERO for x in range(LCD_BOTTOM_ROW_OFFSET)]),
                 LCD_BOTTOM_ROW_OFFSET: tuple([ASCII_ZERO + 1 for x in range(LCD_BOTTOM_ROW_OFFSET)])},
            LCD_TOP_FLAT_ADDRESS:
                {LCD_TOP_ROW_OFFSET: tuple([ASCII_ZERO + 2 for x in range(LCD_BOTTOM_ROW_OFFSET)]),
                 LCD_BOTTOM_ROW_OFFSET: tuple([ASCII_ZERO + 3 for x in range(LCD_BOTTOM_ROW_OFFSET)])},
            LCD_MDL_FLAT_ADDRESS:
                {LCD_TOP_ROW_OFFSET: tuple([ASCII_ZERO + 4 for x in range(LCD_BOTTOM_ROW_OFFSET)]),
                 LCD_BOTTOM_ROW_OFFSET: tuple([ASCII_ZERO + 5 for x in range(LCD_BOTTOM_ROW_OFFSET)])},
            LCD_BTM_FLAT_ADDRESS:
                {LCD_TOP_ROW_OFFSET: tuple([ASCII_ZERO + 6 for x in range(LCD_BOTTOM_ROW_OFFSET)]),
                 LCD_BOTTOM_ROW_OFFSET: tuple([ASCII_ZERO + 7 for x in range(LCD_BOTTOM_ROW_OFFSET)])}}

        self.channel_strip_display = {0: {0: None}}


    def destroy(self):
        V2C4Component.destroy(self)



    @staticmethod
    def make_button(identifier, channel=0, is_momentary=True, *a, **k):
        return ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, identifier, *a, **k)

    @staticmethod
    def make_encoder(identifier, *a, **k):
        return C4EncoderElement(identifier, *a, **k)

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

    # the 56th byte/char defined on each row here will be ignored in the sysex message by the C4 which only
    # has 55 actual text positions per line/row on the LCDs.  But 56 / 8 has 0 remainder, there must be a
    # natural number of display_text_characters (7) defined per display segment in a "Control Surface script".
    # The 56th byte on the first line is the same byte as the 1st byte on the second line
    @staticmethod
    def make_physical_display(nbr_segments=ENCODER_BANK_SIZE, nbr_display_chars=LCD_BOTTOM_ROW_OFFSET, *a, **k):
        # 0x38 == 48 + 8 == 56 == LCD_BOTTOM_ROW_OFFSET  0x08 == 0 + 8 == 8 == ENCODER_BANK_SIZE
        # 56 % 8 = 0 and 56 chars / 8 segments = 7 chars per segment
        assert nbr_display_chars % nbr_segments == 0
        return PhysicalDisplayElement(nbr_display_chars, nbr_segments, *a, **k)


    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)
