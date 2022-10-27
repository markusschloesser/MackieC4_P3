
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from .C4_DEFINES import *

# from folder.file import class
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.LogicalDisplaySegment import LogicalDisplaySegment
from _Framework.PhysicalDisplayElement import DisplayElement


#
#  At a high level this model contains 3 components
# The 3 modeled components align along midi boundaries
# SYSEX midi messages beginning with 0xF0
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
# scratch comments
# SYSEX_HEADER = (0xF0, 0, 0, 0x66, 0x17)  # (240, 0, 0, 102, 23)
# SYSEX_FOOTER = 0xF7  # 247
# sysex_msg = SYSEX_HEADER + (LCD_ANGLED_ADDRESS, LCD_TOP_ROW_OFFSET) + tuple(ascii_text_sysex_ints) + (SYSEX_FOOTER,)
#

#
class C4Model(V2C4Component):

    __module__ = __name__

    def __init__(self, *a, **k):
        V2C4Component.__init__(self, *a, **k)

        self.LCD_display = {
            LCD_ANGLED_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
                                 LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)},
            LCD_TOP_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
                                   LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)},
            LCD_MDL_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
                                   LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)},
            LCD_BTM_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
                                   LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)}}

        lcd_00_up_sgmts = []
        lcd_00_dn_sgmts = []
        lcd_01_up_sgmts = []
        lcd_01_dn_sgmts = []
        lcd_02_up_sgmts = []
        lcd_02_dn_sgmts = []
        lcd_03_up_sgmts = []
        lcd_03_dn_sgmts = []
        for i in range(ENCODER_BANK_SIZE):
            lcd_00_up_sgmts.append(LCDLogicalSegment(i, LCD_TOP_ROW_OFFSET, "000000", "I", *a, **k))
            lcd_00_dn_sgmts.append(LCDLogicalSegment(i, LCD_BOTTOM_ROW_OFFSET, "111111", "I", *a, **k))
            lcd_01_up_sgmts.append(LCDLogicalSegment(i, LCD_TOP_ROW_OFFSET, "222222", "I", *a, **k))
            lcd_01_dn_sgmts.append(LCDLogicalSegment(i, LCD_BOTTOM_ROW_OFFSET, "333333", "I", *a, **k))
            lcd_02_up_sgmts.append(LCDLogicalSegment(i, LCD_TOP_ROW_OFFSET, "444444", "I", *a, **k))
            lcd_02_dn_sgmts.append(LCDLogicalSegment(i, LCD_BOTTOM_ROW_OFFSET, "555555", "I", *a, **k))
            lcd_03_up_sgmts.append(LCDLogicalSegment(i, LCD_TOP_ROW_OFFSET, "666666", "I", *a, **k))
            lcd_03_dn_sgmts.append(LCDLogicalSegment(i, LCD_BOTTOM_ROW_OFFSET, "777777", "I", *a, **k))

        self.LCD_display[LCD_ANGLED_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_00_up_sgmts)
        self.LCD_display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_00_dn_sgmts)
        self.LCD_display[LCD_TOP_FLAT_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_01_up_sgmts)
        self.LCD_display[LCD_TOP_FLAT_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_01_dn_sgmts)
        self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_02_up_sgmts)
        self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_02_dn_sgmts)
        self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_03_up_sgmts)
        self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_03_dn_sgmts)

    def destroy(self):
        V2C4Component.destroy(self)
        self.LCD_display = None # deep destroy()?


class LCDDisplayElement(DisplayElement):
    """This class models an entire LCD Top or Bottom row"""

    def __init__(self, *a, **k):
        super(LCDDisplayElement, self).__init__(NUM_TEXT_BYTES_PER_SYSEX_MSG, ENCODER_BANK_SIZE, *a, **k)


class LCDLogicalSegment(object):
    """This class models just the text data over an encoder LCD Top or Bottom row"""

    _row_offset_text = ""

    def __init__(self, encoder_row_index, display_row_offset, display_text, separator="", *a, **k):

        self.encoder_row_index = encoder_row_index  # index of the encoder in its row 0 - 7
        self.bottom_row_offset = display_row_offset  # offset of 0 means "top row"
        width = len(display_text)
        if width < 6:
            width = 6

        self.__data_source = DisplayDataSource(display_text, separator, *a, **k)
        # setting this callback here would get overwritten by the next two lines anyway
        # self.__data_source.set_update_callback(self.on_display_text_changed())
        self.__logicalDisplay = LogicalDisplaySegment(width, self.__on_display_text_changed(), *a, **k)
        self.__logicalDisplay.set_data_source(self.__data_source)
        #  Giant SWAG - "position identifier" could be used to construct the full two-rows-of-text needed
        # to make a full LCD screen SYSEX message from these "chunks" of logical display
        # offset of 0, then 8 row indexes;
        # offset of 53, then 8 row indexes is how we want this tuple interpreted
        self.__logicalDisplay.set_position_identifier(tuple([display_row_offset, encoder_row_index]))

    def __on_display_text_changed(self):
        """callback method, called when the LCDDataSource display text changes"""
        # may need to pass this callback further up to the level of an entire LCD
        self._row_offset_text = self.__data_source.display_string()

    def get_text(self):
        return self._row_offset_text

    def get_logical_segment(self):
        return self.__logicalDisplay
