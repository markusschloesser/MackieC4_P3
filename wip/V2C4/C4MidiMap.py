from .V2C4Component import *

import Live

from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement

from .C4ElementFactory import C4ElementFactory
from .C4DisplayFactory import C4DisplayFactory
from .C4EncoderElement import C4EncoderElement


class C4MidiMap(C4DisplayFactory, V2C4Component):

    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)

        self.lcd_hello_message = self.lcd_display_hello_message()
        self.lcd_goodbye_message = self.lcd_display_goodbye_message()
        self.lcd_clear_message = self.lcd_display_clear_message()
        self.lcd_id_message = self.lcd_display_id_message()

        self._model = {
            MIDI_NOTE_TYPE: {
                C4BTN_SPLIT_NOTE_ID: None, C4BTN_LOCK_NOTE_ID: None, C4BTN_SPLIT_ERASE_NOTE_ID: None,
                C4BTN_MARKER_NOTE_ID: None, C4BTN_TRACK_NOTE_ID: None, C4BTN_CHANNEL_STRIP_NOTE_ID: None,
                C4BTN_FUNCTION_NOTE_ID: None, C4BTN_BANK_LEFT_NOTE_ID: None, C4BTN_BANK_RIGHT_NOTE_ID: None,
                C4BTN_SINGLE_LEFT_NOTE_ID: None, C4BTN_SINGLE_RIGHT_NOTE_ID: None, C4BTN_SHIFT_NOTE_ID: None,
                C4BTN_OPTION_NOTE_ID: None, C4BTN_CONTROL_NOTE_ID: None, C4BTN_ALT_NOTE_ID: None,
                C4BTN_SLOT_UP_NOTE_ID: None, C4BTN_SLOT_DOWN_NOTE_ID: None, C4BTN_TRACK_LEFT_NOTE_ID: None,
                C4BTN_TRACK_RIGHT_NOTE_ID: None,
                C4_ENCODER_BUTTON_1_NOTE_ID: None, C4_ENCODER_BUTTON_2_NOTE_ID: None, C4_ENCODER_BUTTON_3_NOTE_ID: None,
                C4_ENCODER_BUTTON_4_NOTE_ID: None, C4_ENCODER_BUTTON_5_NOTE_ID: None, C4_ENCODER_BUTTON_6_NOTE_ID: None,
                C4_ENCODER_BUTTON_7_NOTE_ID: None, C4_ENCODER_BUTTON_8_NOTE_ID: None, C4_ENCODER_BUTTON_9_NOTE_ID: None,
                C4_ENCODER_BUTTON_10_NOTE_ID: None, C4_ENCODER_BUTTON_11_NOTE_ID: None, C4_ENCODER_BUTTON_12_NOTE_ID: None,
                C4_ENCODER_BUTTON_13_NOTE_ID: None, C4_ENCODER_BUTTON_14_NOTE_ID: None, C4_ENCODER_BUTTON_15_NOTE_ID: None,
                C4_ENCODER_BUTTON_16_NOTE_ID: None, C4_ENCODER_BUTTON_17_NOTE_ID: None, C4_ENCODER_BUTTON_18_NOTE_ID: None,
                C4_ENCODER_BUTTON_19_NOTE_ID: None, C4_ENCODER_BUTTON_20_NOTE_ID: None, C4_ENCODER_BUTTON_21_NOTE_ID: None,
                C4_ENCODER_BUTTON_22_NOTE_ID: None, C4_ENCODER_BUTTON_23_NOTE_ID: None, C4_ENCODER_BUTTON_24_NOTE_ID: None,
                C4_ENCODER_BUTTON_25_NOTE_ID: None, C4_ENCODER_BUTTON_26_NOTE_ID: None, C4_ENCODER_BUTTON_27_NOTE_ID: None,
                C4_ENCODER_BUTTON_28_NOTE_ID: None, C4_ENCODER_BUTTON_29_NOTE_ID: None, C4_ENCODER_BUTTON_30_NOTE_ID: None,
                C4_ENCODER_BUTTON_31_NOTE_ID: None, C4_ENCODER_BUTTON_32_NOTE_ID: None},
            MIDI_CC_TYPE: {
                C4_ENCODER_1_CC_ID: None, C4_ENCODER_2_CC_ID: None, C4_ENCODER_3_CC_ID: None,
                C4_ENCODER_4_CC_ID: None, C4_ENCODER_5_CC_ID: None, C4_ENCODER_6_CC_ID: None,
                C4_ENCODER_7_CC_ID: None, C4_ENCODER_8_CC_ID: None, C4_ENCODER_9_CC_ID: None,
                C4_ENCODER_10_CC_ID: None, C4_ENCODER_11_CC_ID: None, C4_ENCODER_12_CC_ID: None,
                C4_ENCODER_13_CC_ID: None, C4_ENCODER_14_CC_ID: None, C4_ENCODER_15_CC_ID: None,
                C4_ENCODER_16_CC_ID: None, C4_ENCODER_17_CC_ID: None, C4_ENCODER_18_CC_ID: None,
                C4_ENCODER_19_CC_ID: None, C4_ENCODER_20_CC_ID: None, C4_ENCODER_21_CC_ID: None,
                C4_ENCODER_22_CC_ID: None, C4_ENCODER_23_CC_ID: None, C4_ENCODER_24_CC_ID: None,
                C4_ENCODER_25_CC_ID: None, C4_ENCODER_26_CC_ID: None, C4_ENCODER_27_CC_ID: None,
                C4_ENCODER_28_CC_ID: None, C4_ENCODER_29_CC_ID: None, C4_ENCODER_30_CC_ID: None,
                C4_ENCODER_31_CC_ID: None, C4_ENCODER_32_CC_ID: None}}

    def disconnect(self):
        self._model = {
            MIDI_NOTE_TYPE: {
                C4BTN_SPLIT_NOTE_ID: None, C4BTN_LOCK_NOTE_ID: None, C4BTN_SPLIT_ERASE_NOTE_ID: None,
                C4BTN_MARKER_NOTE_ID: None, C4BTN_TRACK_NOTE_ID: None, C4BTN_CHANNEL_STRIP_NOTE_ID: None,
                C4BTN_FUNCTION_NOTE_ID: None, C4BTN_BANK_LEFT_NOTE_ID: None, C4BTN_BANK_RIGHT_NOTE_ID: None,
                C4BTN_SINGLE_LEFT_NOTE_ID: None, C4BTN_SINGLE_RIGHT_NOTE_ID: None, C4BTN_SHIFT_NOTE_ID: None,
                C4BTN_OPTION_NOTE_ID: None, C4BTN_CONTROL_NOTE_ID: None, C4BTN_ALT_NOTE_ID: None,
                C4BTN_SLOT_UP_NOTE_ID: None, C4BTN_SLOT_DOWN_NOTE_ID: None, C4BTN_TRACK_LEFT_NOTE_ID: None,
                C4BTN_TRACK_RIGHT_NOTE_ID: None,
                C4_ENCODER_BUTTON_1_NOTE_ID: None, C4_ENCODER_BUTTON_2_NOTE_ID: None, C4_ENCODER_BUTTON_3_NOTE_ID: None,
                C4_ENCODER_BUTTON_4_NOTE_ID: None, C4_ENCODER_BUTTON_5_NOTE_ID: None, C4_ENCODER_BUTTON_6_NOTE_ID: None,
                C4_ENCODER_BUTTON_7_NOTE_ID: None, C4_ENCODER_BUTTON_8_NOTE_ID: None, C4_ENCODER_BUTTON_9_NOTE_ID: None,
                C4_ENCODER_BUTTON_10_NOTE_ID: None, C4_ENCODER_BUTTON_11_NOTE_ID: None, C4_ENCODER_BUTTON_12_NOTE_ID: None,
                C4_ENCODER_BUTTON_13_NOTE_ID: None, C4_ENCODER_BUTTON_14_NOTE_ID: None, C4_ENCODER_BUTTON_15_NOTE_ID: None,
                C4_ENCODER_BUTTON_16_NOTE_ID: None, C4_ENCODER_BUTTON_17_NOTE_ID: None, C4_ENCODER_BUTTON_18_NOTE_ID: None,
                C4_ENCODER_BUTTON_19_NOTE_ID: None, C4_ENCODER_BUTTON_20_NOTE_ID: None, C4_ENCODER_BUTTON_21_NOTE_ID: None,
                C4_ENCODER_BUTTON_22_NOTE_ID: None, C4_ENCODER_BUTTON_23_NOTE_ID: None, C4_ENCODER_BUTTON_24_NOTE_ID: None,
                C4_ENCODER_BUTTON_25_NOTE_ID: None, C4_ENCODER_BUTTON_26_NOTE_ID: None, C4_ENCODER_BUTTON_27_NOTE_ID: None,
                C4_ENCODER_BUTTON_28_NOTE_ID: None, C4_ENCODER_BUTTON_29_NOTE_ID: None, C4_ENCODER_BUTTON_30_NOTE_ID: None,
                C4_ENCODER_BUTTON_31_NOTE_ID: None, C4_ENCODER_BUTTON_32_NOTE_ID: None},
            MIDI_CC_TYPE: {
                C4_ENCODER_1_CC_ID: None, C4_ENCODER_2_CC_ID: None, C4_ENCODER_3_CC_ID: None,
                C4_ENCODER_4_CC_ID: None, C4_ENCODER_5_CC_ID: None, C4_ENCODER_6_CC_ID: None,
                C4_ENCODER_7_CC_ID: None, C4_ENCODER_8_CC_ID: None, C4_ENCODER_9_CC_ID: None,
                C4_ENCODER_10_CC_ID: None, C4_ENCODER_11_CC_ID: None, C4_ENCODER_12_CC_ID: None,
                C4_ENCODER_13_CC_ID: None, C4_ENCODER_14_CC_ID: None, C4_ENCODER_15_CC_ID: None,
                C4_ENCODER_16_CC_ID: None, C4_ENCODER_17_CC_ID: None, C4_ENCODER_18_CC_ID: None,
                C4_ENCODER_19_CC_ID: None, C4_ENCODER_20_CC_ID: None, C4_ENCODER_21_CC_ID: None,
                C4_ENCODER_22_CC_ID: None, C4_ENCODER_23_CC_ID: None, C4_ENCODER_24_CC_ID: None,
                C4_ENCODER_25_CC_ID: None, C4_ENCODER_26_CC_ID: None, C4_ENCODER_27_CC_ID: None,
                C4_ENCODER_28_CC_ID: None, C4_ENCODER_29_CC_ID: None, C4_ENCODER_30_CC_ID: None,
                C4_ENCODER_31_CC_ID: None, C4_ENCODER_32_CC_ID: None}}

    def destroy(self):
        self.disconnect()
        self._model = None
        super(C4MidiMap, self).destroy()

    def make_framework_encoder(self, cc_id=C4_ENCODER_1_CC_ID, *a, **k):
        if self._model[MIDI_CC_TYPE][cc_id] is None:
            name = 'Encoder_Control_%d' % cc_id
            self._model[MIDI_CC_TYPE][cc_id] = EncoderElement(MIDI_CC_TYPE, C4_MIDI_CHANNEL, cc_id,
                                                              Live.MidiMap.MapMode.relative_signed_bit, *a, **k)
        else:
            assert False
        return self._model[MIDI_CC_TYPE][cc_id]

    def make_encoder(self, cc_id=C4_ENCODER_1_CC_ID, nm=None, *a, **k):
        if self._model[MIDI_CC_TYPE][cc_id] is None:
            self._model[MIDI_CC_TYPE][cc_id] = C4EncoderElement(cc_id, name=nm, *a, **k)
        else:
            assert False
        return self._model[MIDI_CC_TYPE][cc_id]

    def make_all_encoders(self, *a, **k):
        for cc_id in encoder_cc_ids:
            self.make_encoder(cc_id, *a, **k)

    def make_button(self, note_id=C4BTN_SPLIT_NOTE_ID, channel=0, is_momentary=True, *a, **k):
        if self._model[MIDI_NOTE_TYPE][note_id] is None:
            self._model[MIDI_NOTE_TYPE][note_id] = ButtonElement(is_momentary, MIDI_NOTE_TYPE,
                                                                 channel, note_id, *a, **k)
        else:
            assert False
        return self._model[MIDI_NOTE_TYPE][note_id]

    def make_all_encoder_buttons(self, *a, **k):
        for note_id in encoder_switch_ids:
            self.make_button(note_id, *a, **k)

    def make_all_button_buttons(self, *a, **k):
        self.make_button(C4BTN_SPLIT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_LOCK_NOTE_ID, *a, **k)
        self.make_button(C4BTN_SPLIT_ERASE_NOTE_ID, *a, **k)
        self.make_button(C4BTN_MARKER_NOTE_ID, *a, **k)
        self.make_button(C4BTN_TRACK_NOTE_ID, *a, **k)
        self.make_button(C4BTN_CHANNEL_STRIP_NOTE_ID, *a, **k)
        self.make_button(C4BTN_FUNCTION_NOTE_ID, *a, **k)
        self.make_button(C4BTN_BANK_LEFT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_BANK_RIGHT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_SINGLE_LEFT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_SINGLE_RIGHT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_SHIFT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_OPTION_NOTE_ID, *a, **k)
        self.make_button(C4BTN_CONTROL_NOTE_ID, *a, **k)
        self.make_button(C4BTN_ALT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_SLOT_UP_NOTE_ID, *a, **k)
        self.make_button(C4BTN_SLOT_DOWN_NOTE_ID, *a, **k)
        self.make_button(C4BTN_TRACK_LEFT_NOTE_ID, *a, **k)
        self.make_button(C4BTN_TRACK_RIGHT_NOTE_ID, *a, **k)

    def make_all_c4_elements(self, *a, **k):
        self.make_all_encoders(*a, **k)
        self.make_all_encoder_buttons(*a, **k)
        self.make_all_button_buttons(*a, **k)

    def get_encoder(self, cc_id=C4_ENCODER_1_CC_ID):
        return self._model[MIDI_CC_TYPE][cc_id]

    def get_encoder_by_index(self, encoder_index=0):
        cc_id = V2C4Component.convert_encoder_id_value(encoder_index)
        return self.get_encoder(cc_id)

    def get_encoder_by_row_and_column(self, row=0, column=0):
        assert row in range(NUM_ENCODER_ROWS)
        assert column in range(NUM_ENCODERS_ONE_ROW)
        return self.get_encoder_by_index(row * NUM_ENCODERS_ONE_ROW + column)

    def get_button(self, note_id=C4BTN_SPLIT_NOTE_ID):
        return self._model[MIDI_NOTE_TYPE][note_id]

    def get_button_by_encoder_index(self, encoder_index=0):
        note_id = V2C4Component.convert_encoder_id_value(encoder_index)
        return self.get_button(note_id)

    def get_button_by_encoder_row_and_column(self, row=0, column=0):
        assert row in range(NUM_ENCODER_ROWS)
        assert column in range(NUM_ENCODERS_ONE_ROW)
        return self.get_button_by_encoder_index(row * NUM_ENCODERS_ONE_ROW + column)

    def get_assignment_buttons(self):
        return {
            C4BTN_MARKER_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_MARKER_NOTE_ID],
            C4BTN_TRACK_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_TRACK_NOTE_ID],
            C4BTN_CHANNEL_STRIP_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_CHANNEL_STRIP_NOTE_ID],
            C4BTN_FUNCTION_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_FUNCTION_NOTE_ID]
                }

    def get_modifier_buttons(self):
        return {
            C4BTN_SHIFT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_SHIFT_NOTE_ID],
            C4BTN_OPTION_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_OPTION_NOTE_ID],
            C4BTN_CONTROL_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_CONTROL_NOTE_ID],
            C4BTN_ALT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_ALT_NOTE_ID]
                }

    def get_parameter_buttons(self):
        return {
            C4BTN_BANK_LEFT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_BANK_LEFT_NOTE_ID],
            C4BTN_BANK_RIGHT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_BANK_RIGHT_NOTE_ID],
            C4BTN_SINGLE_LEFT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_SINGLE_LEFT_NOTE_ID],
            C4BTN_SINGLE_RIGHT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_SINGLE_RIGHT_NOTE_ID]
                }

    def get_session_nav_buttons(self):
        return {
            C4BTN_SLOT_UP_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_SLOT_UP_NOTE_ID],
            C4BTN_SLOT_DOWN_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_SLOT_DOWN_NOTE_ID],
            C4BTN_TRACK_LEFT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_TRACK_LEFT_NOTE_ID],
            C4BTN_TRACK_RIGHT_NOTE_ID: self._model[MIDI_NOTE_TYPE][C4BTN_TRACK_RIGHT_NOTE_ID]
                }

    def set_script_handle(self, main_script=None):
        self._set_script_handle(main_script)

