# Python bytecode 2.5 (62131)
# Embedded file name:
#             /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/consts.py
# Compiled at: 2011-01-22 04:37:41
# Decompiled by https://python-decompiler.com

# max 128 tracks per song
from __future__ import absolute_import, print_function, unicode_literals  # MS
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

SETUP_DB_DEFAULT_SIZE = 128

# in Channel Strip mode, devices on a track are controlled in banks of 8 devices (8 encoders, one row)
SETUP_DB_DEVICE_BANK_SIZE = 8
SETUP_DB_MAX_DEVICE_BANKS = 16

# max 128 devices per track in 16 banks of 8 encoders/devices
assert SETUP_DB_DEVICE_BANK_SIZE * SETUP_DB_MAX_DEVICE_BANKS == SETUP_DB_DEFAULT_SIZE

# in Track mode, the selected device's parameters are controlled in banks of 24 parameters (24 encoders, three rows)
SETUP_DB_PARAM_BANK_SIZE = 24
SETUP_DB_MAX_PARAM_BANKS = 5

# max 120 parameters per device in 5 banks of 24 encoders/parameters
assert SETUP_DB_PARAM_BANK_SIZE * SETUP_DB_MAX_PARAM_BANKS == SETUP_DB_DEFAULT_SIZE - SETUP_DB_DEVICE_BANK_SIZE

NOTE_OFF_STATUS = 0x80  # 128  0x80 - 0x8F represent the 16 channels a NOTE_OFF message can be sent to (noteNbr, noteVelocity)
NOTE_ON_STATUS = 0x90  # 144  0x90 - 0x9F represent the 16 channels a NOTE_ON message can be sent to (noteNbr, noteVelocity)
PAT_STATUS = 0xA0  # 160  0xA0 - 0xAF represent the 16 channels a POLYPHONIC AFTERTOUCH message can be sent to (noteNbr, aftertouchPressure)
CC_STATUS = 0xB0  # 176  0xB0 - 0xBF represent the 16 channels a CC message can be sent to (ccParamNbr, ccParamData)
PGM_CHG_STATUS = 0xC0  # 192  0xC0 - 0xCF represent the 16 channels a Program Change message can be sent to (pgmNbr)
CAT_STATUS = 0xD0  # 208  0xD0 - 0xDF represent the 16 channels a CHANNEL AFTERTOUCH message can be sent to (aftertouchPressure)
PB_STATUS = 0xE0  # 224  0xE0 - 0xEF represent the 16 channels a PITCHBEND message can be sent to (pbLSB, pbMSB)
SYSEX_STATUS = 0xF0  # 240  0xF0 - 0xFF represent various 'system' messages
SYSEX_END_OF = 0xF7  # 247              End of Sysex Message
MIDI_DATA_START_OFFSET = 0
MIDI_DATA_LAST_VALID = 0x7F  # 127
MIDI_CONTROL_START_OFFSET = MIDI_DATA_LAST_VALID + 1  # 0x80 # 128

"""
ALL SYSEX values IN HEX NOTATION (BASE 16)
-- example SYSEX message telling the C4 to write text to the top row of top (angled) LCD --
 0009FD03   5  --     F0  Buffer:    63 Bytes   System Exclusive    	# F0 00 00 66 17 30 00  
 SYSX: F0 00 00 66 17 30 00 2D 2D 2D 2D 2D 2D 2D 2D 2D 2D 2D            # .......-----------
 SYSX: 20 4F 73 63 69 6C 6C 61 74 6F 72 20 31 20 2D 2D 2D 2D            #  Oscillator 1 ----
 SYSX: 2D 2D 2D 2D 2D 7C 2D 2D 2D 2D 2D 2D 2D 20 4E 6F 69 73            # -----|------- Nois
 SYSX: 65 20 2D 2D 2D 2D 2D 2D F7                                       # e ------.

 F0 Sysex control byte
 00 unknown   second byte of header is Midi Vendor ID or "Universal Exclusive" message ID
 00 unknown   (According to the MackieControl module's __init__ file) Mackie's vendor ID is 2675 which is 0A73 in hex  
 66 unknown   *probably high part of internal sysex message identifier (this is a C4pro sysex message?)
 17 unknown   *probably low part of internal sysex message identifier (this is an LCD Screen sysex message?) 
 30 message label high
 00 message label low
 <55 bytes of message ASCII text>
 F7 Sysex terminator byte 
 
 30 00 message label for the top    row of top (angled) screen
 30 38 message label for the bottom row of top (angled) screen 
 31 00 message label for the top    row of top (flat) screen
 31 38 message label for the bottom row of top (flat) screen 
 32 00 message label for the top    row of middle (flat) screen
 32 38 message label for the bottom row of middle (flat) screen 
 33 00 message label for the top    row of bottom (flat) screen
 33 38 message label for the bottom row of bottom (flat) screen
 
 The two bytes 30 00 mean, for example, this SysEx message contains the 55 bytes of text
 that should be displayed in the top row of the top (angled) LCD screen 
 
 See @EncoderController.send_display_string1 for example
 a SYSEX message from Live (this midi script) to the C4 device looks like
 - (a byte-valued-int array, a tuple of byte-valued-int values, of length 63) 
 -- a byte-valued-int uses 4 bytes (an int) to store a value that could be stored in a single byte
 
 SYSEX_HEADER + LCD_ANGLED_ADDRESS + LCD_TOP_ROW_OFFSET    + 55 ASCII text bytes + SYSEX_FOOTER
 SYSEX_HEADER + LCD_ANGLED_ADDRESS + LCD_BOTTOM_ROW_OFFSET + 55 ASCII text bytes + SYSEX_FOOTER
 or
 SYSEX_HEADER + LCD_MDL_FLAT_ADDRESS + LCD_TOP_ROW_OFFSET    + 55 ASCII text bytes + SYSEX_FOOTER
 SYSEX_HEADER + LCD_MDL_FLAT_ADDRESS + LCD_BOTTOM_ROW_OFFSET + 55 ASCII text bytes + SYSEX_FOOTER

"""
SYSEX_HEADER = (0xF0, 0, 0, 0x66, 0x17)  # (240, 0, 0, 102, 23)
SYSEX_FOOTER = 0xF7  # 247
LCD_DISPLAY_INDEX = (0x30, 0x31, 0x32, 0x33)  # (48, 49, 50, 51)
LCD_ANGLED_ADDRESS = 0x30  # 48
LCD_TOP_FLAT_ADDRESS = 0x31
LCD_MDL_FLAT_ADDRESS = 0x32
LCD_BTM_FLAT_ADDRESS = 0x33
LCD_TOP_ROW_OFFSET = 0
LCD_BOTTOM_ROW_OFFSET = 0x38  # 56
NUM_CHARS_PER_DISPLAY_LINE = 54  # 54 is divisible by more divisors than 55 like 2, 3, 6, and 9
NUM_TEXT_BYTES_PER_SYSEX_MSG = 55
NUM_TOTAL_BYTES_PER_SYSEX_MSG = 63  # 0X3F (but this is not a SYSEX value)
LCD_DISPLAY_UPDATE_REPEAT_MULTIPLIER = 10

ASCII_SPACE = 0x20  # 32
ASCII_DASH = 0x2D  # 45
ASCII_PIPE = 0x7C  # 124
ASCII_HASH = 0x23  # 35

BUTTON_STATE_OFF = 0
BUTTON_STATE_ON = 0x7F  # 127
BUTTON_STATE_BLINKING = 1
BUTTON_PRESSED = 1  # logical?  like is a button currently pressed?
BUTTON_RELEASED = 0
FID_PANNING_BASE = 0

""" 

Encoder Knobs and Encoder Buttons are addressed by the same byte values, but prefixed by a 
different control message category

- Encoder Buttons are midi Note messages (0x80, 0x20, velocity, channel) (NOTE_ON_STATUS, C4SID_VPOT_PUSH_1, velocity, channel)
 -- Coming from the C4 device, a Button message's note velocity value is always 127 or 7F 
 -- Coming from the C4 device, a Button message's channel value is always 0x01
 
- Encoder Knobs are midi CC messages (0xB0, 0x20, data, channel) (CC_STATUS, C4SID_VPOT_CC_ADDRESS_1, data, channel)
 -- Turning encoder knobs faster increases the data increment amount
 --- clockwise turns increase increment amount over the range 0x01 - 0x0F
 --- anti-clockwise turns increase decrement amount over the range 0x40 - 0x4F
 -- Coming from the C4 device, a Knob message's channel value is always 0x01


These CC messages are from Commander out to the C4 (DATA2 values between 00 and 3F are found outbound to C4) 

002D7A93   6  23     B0    20    06    1  ---  CC: Bank LSB            # Change encoder B000 mode to Single Dot
002B89CD   6  23     B0    20    16    1  ---  CC: Bank LSB            # Change encoder B000 mode to boost/cut 
002D7A93   6  23     B0    20    26    1  ---  CC: Bank LSB            # Change encoder B000 mode to wrap
002D7A93   6  23     B0    20    33    1  ---  CC: Bank LSB            # Change encoder B000 mode to spread
002D7A93   6  23     B0    20    2B    1  ---  CC: Bank LSB            # Change encoder B000 mode to on/off

002B89CD   6  23     B0    21    03    1  ---  Control Change          # Change encoder B001 mode to single dot  
002B89CD   6  23     B0    21    13    1  ---  Control Change          # Change encoder B001 mode to boost/cut  
002B89CD   6  23     B0    21    23    1  ---  Control Change          # Change encoder B001 mode to wrap  
002B89CD   6  23     B0    21    32    1  ---  Control Change          # Change encoder B001 mode to spread  
002B89CD   6  23     B0    21    20    1  ---  Control Change          # Change encoder B001 mode to on/off   

002B89CD   6  23     B0    22    02    1  ---  Control Change          # Change encoder B002 mode to single dot  
002B89CD   6  23     B0    22    12    1  ---  Control Change          # Change encoder B002 mode to boost/cut   
002B89CD   6  23     B0    22    22    1  ---  Control Change          # Change encoder B002 mode to wrap   
002B89CD   6  23     B0    22    32    1  ---  Control Change          # Change encoder B002 mode to spread   
002B89CD   6  23     B0    22    20    1  ---  Control Change          # Change encoder B002 mode to on/off   
...
002B89CD   6  23     B0    27    08    1  ---  Control Change          # Change encoder B007 mode to single dot 
002B89CD   6  23     B0    27    18    1  ---  Control Change          # Change encoder B007 mode to boost/cut 
002B89CD   6  23     B0    27    28    1  ---  Control Change          # Change encoder B007 mode to wrap 
002B89CD   6  23     B0    27    34    1  ---  Control Change          # Change encoder B007 mode to spread 
002B89CD   6  23     B0    27    2B    1  ---  Control Change          # Change encoder B007 mode to on/off 

002B89CD   6  23     B0    28    01    1  ---  Control Change          # Change encoder B008 mode to single dot 

002B89CD   6  23     B0    30    01    1  ---  Control Change          # Change encoder B030 mode to single dot 

002B89CD   6  23     B0    38    01    1  ---  Control Change          # Change encoder B038 mode to single dot 

002B89CD   6  23     B0    3F    01    1  ---  Control Change          # Change encoder B03F mode to single dot 

In Live terms (this midi script) 
   0xB0        is CC_STATUS   
   0x20 - 0x3F is C4SID_VPOT_CC_ADDRESS_1 - C4SID_VPOT_CC_ADDRESS_32  (one of 32 encoders)
   0x00 - 0x3F is the data value range
   0x01        is the channel 

"""

VPOT_DISPLAY_SINGLE_DOT = 0  #
VPOT_DISPLAY_BOOST_CUT = 1  #
VPOT_DISPLAY_WRAP = 2  #
VPOT_DISPLAY_SPREAD = 3  #
VPOT_DISPLAY_BOOLEAN = 4  #
VPOT_DISPLAY_HEX_CONVERT = 0x10  # 16

# min  max leds in ring illuminated
encoder_ring_led_mode_cc_values = {VPOT_DISPLAY_SINGLE_DOT: (0x01, 0x0B),  # 01 - 0B
                                   VPOT_DISPLAY_BOOST_CUT: (0x11, 0x1B),  # 11 - 1B
                                   VPOT_DISPLAY_WRAP: (0x21, 0x2B),  # 21 - 2B
                                   VPOT_DISPLAY_SPREAD: (0x31, 0x36),  # 31 - 36
                                   VPOT_DISPLAY_BOOLEAN: (0x20, 0x2B)}  # 20 - 2B  -- goes to ON in about 6 steps

encoder_ring_led_mode_values = {VPOT_DISPLAY_SINGLE_DOT: 0x01,
                                VPOT_DISPLAY_BOOST_CUT: 0x16,
                                VPOT_DISPLAY_WRAP: 0x26,
                                VPOT_DISPLAY_SPREAD: 0x33,
                                VPOT_DISPLAY_BOOLEAN: 0x2B}

RING_LED_ALL_OFF = 0  # encoder disable?

LED_ON_DATA = 0x7F  # any value 40 - 4F?
LED_OFF_DATA = 0x00  # any value 00 - 0F?

CLIP_STATE_INVALID = -1
CLIP_STOPPED = 0
CLIP_TRIGGERED = 1
CLIP_PLAYING = 2

# the 4 "assignment modes" implemented by this C4 script module
C4M_USER = 0  # == the C4SID_MARKER button = 0x05  # 5  F-1
C4M_PLUGINS = 1  # == the C4SID_TRACK button = 0x06  # 6  F#-1
C4M_CHANNEL_STRIP = 2  # == the C4SID_CHANNEL_STRIP button = 0x07  # 7  G-1
C4M_FUNCTION = 3  # == the C4SID_FUNCTION button = 0x08  # 8  G#-1

ENCODER_BASE = 0
NUM_ENCODERS_ONE_ROW = 8
NUM_ENCODERS = NUM_ENCODERS_ONE_ROW * 4
encoder_range = range(ENCODER_BASE, NUM_ENCODERS)  # MS do we need to change "range" cos of Py3? see https://python-future.org/compatible_idioms.html#range
row_00_encoders = range(ENCODER_BASE, NUM_ENCODERS_ONE_ROW)
row_01_encoders = range(NUM_ENCODERS_ONE_ROW, NUM_ENCODERS_ONE_ROW * 2)  # [8,9,10,11,12,13,14,15]
row_02_encoders = range(NUM_ENCODERS_ONE_ROW * 2, NUM_ENCODERS_ONE_ROW * 3)  # [16,17,18,19,20,21,22,23]
row_03_encoders = range(NUM_ENCODERS_ONE_ROW * 3, NUM_ENCODERS)

C4SID_FIRST = 0

# split is a toggle between four "split states" (None, 1/3, 2/2, 3/1)
# if Commander and the C4 are communicating, then you can display one, two, or three
# rows of "the next" layout file Commander has loaded depending on the selected "split state"
# for example, None means apply the current Layout to all the rows of encoders and displays
# while 1/3 would mean apply the "current layout" to the top row of encoders (and the angled display) only
# and then apply the "next layout loaded" to the other three rows of encoders (and their associated displays)
#
# these are Note messages so they correspond to midi notes
C4SID_SPLIT = 0  # C -1
C4SID_LOCK = 0x03  # 3  Eb-1
C4SID_SPLIT_ERASE = 0x04  # 4 E -1

# buttons inside the 'function' box on the C4 graphics
system_switch_ids = range(C4SID_SPLIT, C4SID_SPLIT_ERASE + 1)
C4SID_MARKER = 0x05  # 5  F-1
C4SID_TRACK = 0x06  # 6  F#-1

# if Commander and the C4 are communicating, then you can toggle the bottom row
# of all displays between showing the current encoder value
# and showing any "bottom line text"
# you cannot change/toggle channel while edit mode is active
C4SID_CHANNEL_STRIP = 0x07  # 7  G-1

# if Commander and the C4 are communicating,
# this button toggles the Run/Edit status in Commander/C4
C4SID_FUNCTION = 0x08  # 8  G#-1

# buttons inside the 'assignment' box on the C4 graphics
assignment_mode_switch_ids = range(C4SID_MARKER, C4SID_FUNCTION + 1)
assignment_mode_to_button_id = {C4M_USER: C4SID_MARKER,
                                C4M_PLUGINS: C4SID_TRACK,
                                C4M_CHANNEL_STRIP: C4SID_CHANNEL_STRIP,
                                C4M_FUNCTION: C4SID_FUNCTION}
button_id_to_assignment_mode = {C4SID_MARKER: C4M_USER,
                                C4SID_TRACK: C4M_PLUGINS,
                                C4SID_CHANNEL_STRIP: C4M_CHANNEL_STRIP,
                                C4SID_FUNCTION: C4M_FUNCTION}

# if Commander and the C4 are communicating, then you can move back and forth
# between pages (banks) of the currently loaded layouts (pages have 8 columns and 4 rows)
C4SID_BANK_LEFT = 0x09  # 9     A -1
C4SID_BANK_RIGHT = 0x0A  # 10  A#-1

# buttons inside the 'Parameter' box on the C4 graphics
bank_switch_ids = range(C4SID_BANK_LEFT, C4SID_BANK_RIGHT + 1)

# if Commander and the C4 are communicating, then you can move back and forth
# between page columns of the currently loaded layouts (pages have 8 columns and 4 rows)
# note that page banks and single columns can scroll between loaded layouts too
C4SID_SINGLE_LEFT = 0x0B  # 11    B -1
C4SID_SINGLE_RIGHT = 0x0C  # 12   C 0

# buttons inside the 'Parameter' box on the C4 graphics
single_switch_ids = range(C4SID_SINGLE_LEFT, C4SID_SINGLE_RIGHT + 1)
C4SID_SHIFT = 0x0D  # 13  C# 0
C4SID_OPTION = 0x0E  # 14  D  0

# control functions just like the channel button: toggles between bottom row LCD displays
C4SID_CONTROL = 0x0F  # 15  Eb 0
C4SID_ALT = 0x10  # 16  E  0

# buttons inside the 'Modifiers' box on the C4 graphics
modifier_switch_ids = range(C4SID_SHIFT, C4SID_ALT + 1)

# if Commander and the C4 are communicating, then you can move up and down
# through rows of "layout pages" of currently loaded layouts
C4SID_SLOT_UP = 0x11  # 17  F  0
C4SID_SLOT_DOWN = 0x12  # 18 F# 0

# buttons around the 'solid black' ellipse on the C4 graphics
slot_nav_switch_ids = range(C4SID_SLOT_UP, C4SID_SLOT_DOWN + 1)

# if Commander and the C4 are communicating, then you can move up and down
# then you can move back and forth between pages of loaded layouts
C4SID_TRACK_LEFT = 0x13  # 19  G  0
C4SID_TRACK_RIGHT = 0x14  # 20 G# 0

# buttons around the 'solid black' ellipse on the C4 graphics
track_nav_switch_ids = range(C4SID_TRACK_LEFT, C4SID_TRACK_RIGHT + 1)

# encoder push button addresses
# if Commander and the C4 are communicating, then
# push and hold to toggle the 'button local' LCD display between 'data' and 'label' mode
# push and release quickly to reset the value of the encoder to its default value
C4SID_VPOT_PUSH_BASE = 0x20  # 32
C4SID_VPOT_PUSH_1 = 0x20  # 32  G# 1
C4SID_VPOT_PUSH_2 = 0x21  # 33  A  1
C4SID_VPOT_PUSH_3 = 0x22  # 34  A# 1
C4SID_VPOT_PUSH_4 = 0x23  # 35  B  1
C4SID_VPOT_PUSH_5 = 0x24  # 36  C  2
C4SID_VPOT_PUSH_6 = 0x25  # 37  C# 2
C4SID_VPOT_PUSH_7 = 0x26  # 38  D  2
C4SID_VPOT_PUSH_8 = 0x27  # 39  Eb 2
C4SID_VPOT_PUSH_9 = 0x28  # 40  E  2
C4SID_VPOT_PUSH_10 = 0x29  # 41  F 2
C4SID_VPOT_PUSH_11 = 0x2A  # 42  F# 2
C4SID_VPOT_PUSH_12 = 0x2B  # 43  G  2
C4SID_VPOT_PUSH_13 = 0x2C  # 44  G# 2
C4SID_VPOT_PUSH_14 = 0x2D  # 45  A  2
C4SID_VPOT_PUSH_15 = 0x2E  # 46  A# 2
C4SID_VPOT_PUSH_16 = 0x2F  # 47  B  2
C4SID_VPOT_PUSH_17 = 0x30  # 48  C  3
C4SID_VPOT_PUSH_18 = 0x31  # 49  C# 3
C4SID_VPOT_PUSH_19 = 0x32  # 50  D  3
C4SID_VPOT_PUSH_20 = 0x33  # 51  Eb 3
C4SID_VPOT_PUSH_21 = 0x34  # 52  E  3
C4SID_VPOT_PUSH_22 = 0x35  # 53  F  3
C4SID_VPOT_PUSH_23 = 0x36  # 54  F# 3
C4SID_VPOT_PUSH_24 = 0x37  # 55  G  3
C4SID_VPOT_PUSH_25 = 0x38  # 56  G# 3
C4SID_VPOT_PUSH_26 = 0x39  # 57  A  3
C4SID_VPOT_PUSH_27 = 0x3A  # 58  A# 3
C4SID_VPOT_PUSH_28 = 0x3B  # 59  B  3
C4SID_VPOT_PUSH_29 = 0x3C  # 60  C  4
C4SID_VPOT_PUSH_30 = 0x3D  # 61  C# 4
C4SID_VPOT_PUSH_31 = 0x3E  # 62  D  4
C4SID_VPOT_PUSH_32 = 0x3F  # 63  Eb 4
encoder_switch_ids = range(C4SID_VPOT_PUSH_1, C4SID_VPOT_PUSH_32 + 1)
C4SID_LAST = 0x3F  # 63

"""
C4 device turning encoder 00 clockwise (topmost row left end)
000059F8  22   6     B0    00    01    1  ---  CC: Bank MSB       --> in port 22 from C4 (message reports encoder incremented 1 CW step)
000059FB   6  23     B0    20    09    1  ---  CC: Bank LSB       --> out port 23 to C4  (message commands encoder's dial's LED set to increment 9 CW steps) 
00005A70  22   6     B0    00    01    1  ---  CC: Bank MSB       
00005A73   6  23     B0    20    0B    1  ---  CC: Bank LSB       
00005AE8  22   6     B0    00    01    1  ---  CC: Bank MSB       
00005AEB   6  23     B0    20    0B    1  ---  CC: Bank LSB       

C4 device turning encoder 01 clockwise (topmost row second from left end)
 00031E39  22   6     B0    01    01    1  ---  CC: Modulation
 00031E3C   6  23     B0    21    02    1  ---  Control Change
 00031F65  22   6     B0    01    01    1  ---  CC: Modulation
 00031F68   6  23     B0    21    04    1  ---  Control Change
 000320CD  22   6     B0    01    01    1  ---  CC: Modulation
 000320D0   6  23     B0    21    05    1  ---  Control Change

"""

C4SID_VPOT_CC_ADDRESS_BASE = 0x20  # 32
C4SID_VPOT_CC_ADDRESS_1 = 0x20  # 32
C4SID_VPOT_CC_ADDRESS_2 = 0x21  # 33
C4SID_VPOT_CC_ADDRESS_3 = 0x22  # 34
C4SID_VPOT_CC_ADDRESS_4 = 0x23  # 35
C4SID_VPOT_CC_ADDRESS_5 = 0x24  # 36
C4SID_VPOT_CC_ADDRESS_6 = 0x25  # 37
C4SID_VPOT_CC_ADDRESS_7 = 0x26  # 38
C4SID_VPOT_CC_ADDRESS_8 = 0x27  # 39
C4SID_VPOT_CC_ADDRESS_9 = 0x28  # 40
C4SID_VPOT_CC_ADDRESS_10 = 0x29  # 41
C4SID_VPOT_CC_ADDRESS_11 = 0x2A  # 42
C4SID_VPOT_CC_ADDRESS_12 = 0x2B  # 43
C4SID_VPOT_CC_ADDRESS_13 = 0x2C  # 44
C4SID_VPOT_CC_ADDRESS_14 = 0x2D  # 45
C4SID_VPOT_CC_ADDRESS_15 = 0x2E  # 46
C4SID_VPOT_CC_ADDRESS_16 = 0x2F  # 47
C4SID_VPOT_CC_ADDRESS_17 = 0x30  # 48
C4SID_VPOT_CC_ADDRESS_18 = 0x31  # 49
C4SID_VPOT_CC_ADDRESS_19 = 0x32  # 50
C4SID_VPOT_CC_ADDRESS_20 = 0x33  # 51
C4SID_VPOT_CC_ADDRESS_21 = 0x34  # 52
C4SID_VPOT_CC_ADDRESS_22 = 0x35  # 53
C4SID_VPOT_CC_ADDRESS_23 = 0x36  # 54
C4SID_VPOT_CC_ADDRESS_24 = 0x37  # 55
C4SID_VPOT_CC_ADDRESS_25 = 0x38  # 56
C4SID_VPOT_CC_ADDRESS_26 = 0x39  # 57
C4SID_VPOT_CC_ADDRESS_27 = 0x3A  # 58
C4SID_VPOT_CC_ADDRESS_28 = 0x3B  # 59
C4SID_VPOT_CC_ADDRESS_29 = 0x3C  # 60
C4SID_VPOT_CC_ADDRESS_30 = 0x3D  # 61
C4SID_VPOT_CC_ADDRESS_31 = 0x3E  # 62
C4SID_VPOT_CC_ADDRESS_32 = 0x3F  # 63
encoder_cc_ids = range(C4SID_VPOT_CC_ADDRESS_1, C4SID_VPOT_CC_ADDRESS_32 + 1)
encoder_cw_values = range(0x01, 0x10)  # larger values means knob is turning faster / bigger CW increments
encoder_ccw_values = range(0x41, 0x50)  # larger values means knob is turning faster / bigger CCW increments
