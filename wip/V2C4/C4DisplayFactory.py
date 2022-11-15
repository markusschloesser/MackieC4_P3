from .V2C4Component import *
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

from _Framework.InputControlElement import *


class C4DisplayFactory(V2C4Component):

    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)

        # self.lcd_physical_displays = {0: {0: None}}
        # self.lcd_display_track_name_message = tuple(V2C4Component.generate_sysex_body(
        #     'Track Name'.center(LCD_BOTTOM_ROW_OFFSET/2)))
        # self.lcd_display_device_name_message = tuple(V2C4Component.generate_sysex_body(
        #     'Device Name'.center(LCD_BOTTOM_ROW_OFFSET/2)))
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

        # self.channel_strip_display = {0: {0: None}}

    def destroy(self):
        # self.lcd_physical_displays = None
        # self.channel_strip_display = None

        # self.lcd_display_track_name_message = None
        # self.lcd_display_device_name_message = None
        self.lcd_display_hello_message = None
        self.lcd_display_goodbye_message = None
        self.lcd_display_clear_message = None
        self.lcd_display_id_message = None

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