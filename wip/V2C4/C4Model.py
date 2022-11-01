
from .V2C4Component import *

import Live
# from folder.file import class
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
# from _Framework.DisplayDataSource import DisplayDataSource
# from _Framework.LogicalDisplaySegment import LogicalDisplaySegment
# from _Framework.PhysicalDisplayElement import DisplayElement

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement

from .C4EncoderElement import C4EncoderElement

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


class C4Model(V2C4Component):

    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)  #

        # self.LCD_display = {
        #     LCD_ANGLED_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
        #                          LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)},
        #     LCD_TOP_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
        #                            LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)},
        #     LCD_MDL_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
        #                            LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)},
        #     LCD_BTM_FLAT_ADDRESS: {LCD_TOP_ROW_OFFSET: LCDDisplayElement(*a, **k),
        #                            LCD_BOTTOM_ROW_OFFSET: LCDDisplayElement(*a, **k)}}
        #
        # lcd_00_up_sgmts = []
        # lcd_00_dn_sgmts = []
        # lcd_01_up_sgmts = []
        # lcd_01_dn_sgmts = []
        # lcd_02_up_sgmts = []
        # lcd_02_dn_sgmts = []
        # lcd_03_up_sgmts = []
        # lcd_03_dn_sgmts = []
        # width = int(LCD_BOTTOM_ROW_OFFSET / ENCODER_BANK_SIZE) # == 7
        # separator = "I"
        # for i in range(ENCODER_BANK_SIZE):
        #     lcd_00_up_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_00_up_sgmts[-1].set_data_source(DisplayDataSource("000000", separator))
        #     lcd_00_up_sgmts[-1].set_position_identifier(tuple([LCD_TOP_ROW_OFFSET, i]))
        #     lcd_00_dn_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_00_dn_sgmts[-1].set_data_source(DisplayDataSource("11111", separator))
        #     lcd_00_dn_sgmts[-1].set_position_identifier(tuple([LCD_BOTTOM_ROW_OFFSET, i]))
        #     lcd_01_up_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_01_up_sgmts[-1].set_data_source(DisplayDataSource("222222", separator))
        #     lcd_01_up_sgmts[-1].set_position_identifier(tuple([LCD_TOP_ROW_OFFSET, i]))
        #     lcd_01_dn_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_01_dn_sgmts[-1].set_data_source(DisplayDataSource("333333", separator))
        #     lcd_01_dn_sgmts[-1].set_position_identifier(tuple([LCD_BOTTOM_ROW_OFFSET, i]))
        #
        #     lcd_02_up_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_02_up_sgmts[-1].set_data_source(DisplayDataSource("444444", separator))
        #     lcd_02_up_sgmts[-1].set_position_identifier(tuple([LCD_TOP_ROW_OFFSET, i]))
        #     lcd_02_dn_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_02_dn_sgmts[-1].set_data_source(DisplayDataSource("555555", separator))
        #     lcd_02_dn_sgmts[-1].set_position_identifier(tuple([LCD_BOTTOM_ROW_OFFSET, i]))
        #     lcd_03_up_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_03_up_sgmts[-1].set_data_source(DisplayDataSource("666666", separator))
        #     lcd_03_up_sgmts[-1].set_position_identifier(tuple([LCD_TOP_ROW_OFFSET, i]))
        #     lcd_03_dn_sgmts.append(LogicalDisplaySegment(width, self.on_display_text_changed))
        #     lcd_03_dn_sgmts[-1].set_data_source(DisplayDataSource("777777", separator))
        #     lcd_03_dn_sgmts[-1].set_position_identifier(tuple([LCD_BOTTOM_ROW_OFFSET, i]))

        # self.LCD_display[LCD_ANGLED_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_00_up_sgmts)
        # self.LCD_display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_00_dn_sgmts)
        # self.LCD_display[LCD_TOP_FLAT_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_01_up_sgmts)
        # self.LCD_display[LCD_TOP_FLAT_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_01_dn_sgmts)
        # self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_02_up_sgmts)
        # self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_02_dn_sgmts)
        # self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_TOP_ROW_OFFSET].set_data_sources(lcd_03_up_sgmts)
        # self.LCD_display[LCD_MDL_FLAT_ADDRESS][LCD_BOTTOM_ROW_OFFSET].set_data_sources(lcd_03_dn_sgmts)

        # the 56th byte/char defined on each row here will be ignored by the C4 which only has 55 actual
        # text positions per line/row on the LCDs.  But 56 / 8 has 0 remainder, there must be a natural number
        # of display_text_characters (7) defined per display segment in a "Control Surface script".
        # per
        self.LCD_display = {
            LCD_ANGLED_ADDRESS:   # 0x38 == 48 + 8 == 56
                {LCD_TOP_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE),
                 LCD_BOTTOM_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE)},
            LCD_TOP_FLAT_ADDRESS:
                {LCD_TOP_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE),
                 LCD_BOTTOM_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE)},
            LCD_MDL_FLAT_ADDRESS:
                {LCD_TOP_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE),
                 LCD_BOTTOM_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE)},
            LCD_BTM_FLAT_ADDRESS:
                {LCD_TOP_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE),
                 LCD_BOTTOM_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE)}}

        self.channel_strip_display = {
            LCD_ANGLED_ADDRESS:  # 0x38 == 48 + 8 == 56
                {LCD_TOP_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, 2),
                 LCD_BOTTOM_ROW_OFFSET: PhysicalDisplayElement(LCD_BOTTOM_ROW_OFFSET, 2)}}
        # Bottom area Buttons
        # C4 sends Note ON vel 127 for "button pressed"
        #      and Note ON vel   0 for "button released"  (or Note Off vel 0?)
        # which is "not momentary", but could be proven wrong. Axiom code "required" True here
        is_momentary = True
        channel = 0
        self.split_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SPLIT)
        self.lock_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_LOCK)
        self.spot_erase_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SPLIT_ERASE)
        self.function_buttons = tuple([self.split_button, self.lock_button, self.spot_erase_button])

        self.marker_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_MARKER)
        self.chan_strip_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_CHANNEL_STRIP)
        self.track_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_TRACK)
        self.function_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_FUNCTION)
        self.assignment_buttons = tuple([self.marker_button, self.chan_strip_button,
                                         self.track_button, self.function_button])

        self.shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SHIFT)
        self.control_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_CONTROL)
        self.option_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_OPTION)
        self.alt_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_ALT)
        self.modifier_buttons = tuple([self.shift_button, self.control_button, self.option_button, self.alt_button])

        self.bank_left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_BANK_LEFT)
        self.bank_right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_BANK_RIGHT)
        self.single_left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SINGLE_LEFT)
        self.single_right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SINGLE_RIGHT)
        self.parameter_buttons = tuple([self.bank_left_button, self.bank_right_button,
                                        self.single_left_button, self.single_right_button])

        self.slot_up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SLOT_UP)
        self.slot_down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_SLOT_DOWN)
        self.track_left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_TRACK_LEFT)
        self.track_right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_TRACK_RIGHT)
        self.cardinal_buttons = tuple([self.slot_up_button, self.slot_down_button,
                                       self.track_left_button, self.track_right_button])

        # Encoders, Encoder Buttons
        # 32 of each in 4 rows by 8 columns
        # Encoders        originate MIDI CC messages for their channel and CC number
        # Encoder LED rings receive MIDI CC messages for their channel and CC number
        # Encoder Buttons   originate MIDI Note messages for their channel and Note number
        # Encoder Button LEDs receive MIDI Note messages for their channel and Note number
        # the "receivers" are the "midi feedback" targets of the "originators"
        # the "receivers" are not generally modeled in code other than as "midi feedback" targets
        # sometimes though, you just want to send SYSEX to the encoder rings, for example,
        # that's handled elsewhere.
        self.encoders = []
        self.encoder_buttons = []
        for i in range(NUM_ENCODERS):
            self.encoders.append(C4EncoderElement(MIDI_CC_TYPE, channel,
                                                  C4SID_VPOT_CC_ADDRESS_BASE + i,
                                                  Live.MidiMap.MapMode.relative_signed_bit))
            self.encoders[(-1)].set_feedback_delay(-1)
            self.encoder_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, C4SID_VPOT_PUSH_BASE + i))

    def destroy(self):
        V2C4Component.destroy(self)
        # self.LCD_display = None # deep destroy()?

    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)


    # def on_display_text_changed(self):
    #     """callback method, called when the display text changes"""
    #     # alert the Physical Display to send midi?
    #     pass


# class LCDDisplayElement(DisplayElement):
#     """This class models an entire LCD Top or Bottom row
#     NOTE: each C4 "LCD line" only has 55 bytes of text, but the char width of a DisplayElement needs to evenly divide by
#     the number of segments. Saying the width is 56 means the 56th character of each line is never visible, but it
#     gives each of 8 segments 7 chars per line
#     LCD_BOTTOM_ROW_OFFSET = 0x38  # 56
#     NUM_TEXT_BYTES_PER_SYSEX_MSG = 55  # 0x37
#     """
#     def __init__(self, *a, **k):
#         DisplayElement.__init__(self, LCD_BOTTOM_ROW_OFFSET, ENCODER_BANK_SIZE, *a, **k)
#
#
# class LCDLogicalSegment(object):
#     """This class models just the text data over an encoder LCD Top or Bottom row"""
#
#     _row_offset_text = ""
#
#     def __init__(self, encoder_row_index, display_row_offset, display_text, separator="", *a, **k):
#
#         self.encoder_row_index = encoder_row_index  # index of the encoder in its row 0 - 7
#         self.bottom_row_offset = display_row_offset  # offset of 0 means "top row"
#         width = len(display_text)
#         if width < 6:
#             width = 6
#
#         # self.__data_source = DisplayDataSource(display_text, separator, *a, **k)
#         # setting this callback here would get overwritten by the next two lines anyway
#         # self.__data_source.set_update_callback(self.on_display_text_changed())
#         self.__logicalDisplay = LogicalDisplaySegment(width, self.__on_display_text_changed(), *a, **k)
#         self.__logicalDisplay.set_data_source(DisplayDataSource(display_text, separator, *a, **k))
#         #  Giant SWAG - "position identifier" could be used to construct the full two-rows-of-text needed
#         # to make a full LCD screen SYSEX message from these "chunks" of logical display
#         # offset of 0, then 8 row indexes;
#         # offset of 53, then 8 row indexes is how we want this tuple interpreted
#         self.__logicalDisplay.set_position_identifier(tuple([display_row_offset, encoder_row_index]))
#
#     def __on_display_text_changed(self):
#         """callback method, called when the LCDDataSource display text changes"""
#         # may need to pass this callback further up to the level of an entire LCD
#         # self._row_offset_text = self.__logicalDisplay.display_string()
#         pass
#
#     def get_text(self):
#         return self._row_offset_text
#
#     def get_logical_segment(self):
#         return self.__logicalDisplay
