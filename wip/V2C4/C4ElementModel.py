from .V2C4Component import *

from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from .C4ElementFactory import C4ElementFactory
from .C4DisplayFactory import C4DisplayFactory
from .C4EncoderElement import C4EncoderElement


class C4ElementModel(V2C4Component):

    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)
        self._element_factory = C4ElementFactory()
        self._display_factory = C4DisplayFactory()

        self._model = {
            MIDI_NOTE_TYPE: {
                C4SID_SPLIT: None, C4SID_LOCK: None, C4SID_SPLIT_ERASE: None,
                C4SID_MARKER: None, C4SID_TRACK: None, C4SID_CHANNEL_STRIP: None,
                C4SID_FUNCTION: None, C4SID_BANK_LEFT: None, C4SID_BANK_RIGHT: None,
                C4SID_SINGLE_LEFT: None, C4SID_SINGLE_RIGHT: None, C4SID_SHIFT: None,
                C4SID_OPTION: None, C4SID_CONTROL: None, C4SID_ALT: None,
                C4SID_SLOT_UP: None, C4SID_SLOT_DOWN: None, C4SID_TRACK_LEFT: None,
                C4SID_TRACK_RIGHT: None,
                C4SID_VPOT_PUSH_1: None, C4SID_VPOT_PUSH_2: None, C4SID_VPOT_PUSH_3: None,
                C4SID_VPOT_PUSH_4: None, C4SID_VPOT_PUSH_5: None, C4SID_VPOT_PUSH_6: None,
                C4SID_VPOT_PUSH_7: None, C4SID_VPOT_PUSH_8: None, C4SID_VPOT_PUSH_9: None,
                C4SID_VPOT_PUSH_10: None, C4SID_VPOT_PUSH_11: None, C4SID_VPOT_PUSH_12: None,
                C4SID_VPOT_PUSH_13: None, C4SID_VPOT_PUSH_14: None, C4SID_VPOT_PUSH_15: None,
                C4SID_VPOT_PUSH_16: None, C4SID_VPOT_PUSH_17: None, C4SID_VPOT_PUSH_18: None,
                C4SID_VPOT_PUSH_19: None, C4SID_VPOT_PUSH_20: None, C4SID_VPOT_PUSH_21: None,
                C4SID_VPOT_PUSH_22: None, C4SID_VPOT_PUSH_23: None, C4SID_VPOT_PUSH_24: None,
                C4SID_VPOT_PUSH_25: None, C4SID_VPOT_PUSH_26: None, C4SID_VPOT_PUSH_27: None,
                C4SID_VPOT_PUSH_28: None, C4SID_VPOT_PUSH_29: None, C4SID_VPOT_PUSH_30: None,
                C4SID_VPOT_PUSH_31: None, C4SID_VPOT_PUSH_32: None},
            MIDI_CC_TYPE: {
                C4SID_VPOT_CC_ADDRESS_1: None, C4SID_VPOT_CC_ADDRESS_2: None, C4SID_VPOT_CC_ADDRESS_3: None,
                C4SID_VPOT_CC_ADDRESS_4: None, C4SID_VPOT_CC_ADDRESS_5: None, C4SID_VPOT_CC_ADDRESS_6: None,
                C4SID_VPOT_CC_ADDRESS_7: None, C4SID_VPOT_CC_ADDRESS_8: None, C4SID_VPOT_CC_ADDRESS_9: None,
                C4SID_VPOT_CC_ADDRESS_10: None, C4SID_VPOT_CC_ADDRESS_11: None, C4SID_VPOT_CC_ADDRESS_12: None,
                C4SID_VPOT_CC_ADDRESS_13: None, C4SID_VPOT_CC_ADDRESS_14: None, C4SID_VPOT_CC_ADDRESS_15: None,
                C4SID_VPOT_CC_ADDRESS_16: None, C4SID_VPOT_CC_ADDRESS_17: None, C4SID_VPOT_CC_ADDRESS_18: None,
                C4SID_VPOT_CC_ADDRESS_19: None, C4SID_VPOT_CC_ADDRESS_20: None, C4SID_VPOT_CC_ADDRESS_21: None,
                C4SID_VPOT_CC_ADDRESS_22: None, C4SID_VPOT_CC_ADDRESS_23: None, C4SID_VPOT_CC_ADDRESS_24: None,
                C4SID_VPOT_CC_ADDRESS_25: None, C4SID_VPOT_CC_ADDRESS_26: None, C4SID_VPOT_CC_ADDRESS_27: None,
                C4SID_VPOT_CC_ADDRESS_28: None, C4SID_VPOT_CC_ADDRESS_29: None, C4SID_VPOT_CC_ADDRESS_30: None,
                C4SID_VPOT_CC_ADDRESS_31: None, C4SID_VPOT_CC_ADDRESS_32: None}}

    def disconnect(self):
        self._element_factory = None
        self._display_factory = None
        self._model = {
            MIDI_NOTE_TYPE: {
                C4SID_SPLIT: None, C4SID_LOCK: None, C4SID_SPLIT_ERASE: None,
                C4SID_MARKER: None, C4SID_TRACK: None, C4SID_CHANNEL_STRIP: None,
                C4SID_FUNCTION: None, C4SID_BANK_LEFT: None, C4SID_BANK_RIGHT: None,
                C4SID_SINGLE_LEFT: None, C4SID_SINGLE_RIGHT: None, C4SID_SHIFT: None,
                C4SID_OPTION: None, C4SID_CONTROL: None, C4SID_ALT: None,
                C4SID_SLOT_UP: None, C4SID_SLOT_DOWN: None, C4SID_TRACK_LEFT: None,
                C4SID_TRACK_RIGHT: None,
                C4SID_VPOT_PUSH_1: None, C4SID_VPOT_PUSH_2: None, C4SID_VPOT_PUSH_3: None,
                C4SID_VPOT_PUSH_4: None, C4SID_VPOT_PUSH_5: None, C4SID_VPOT_PUSH_6: None,
                C4SID_VPOT_PUSH_7: None, C4SID_VPOT_PUSH_8: None, C4SID_VPOT_PUSH_9: None,
                C4SID_VPOT_PUSH_10: None, C4SID_VPOT_PUSH_11: None, C4SID_VPOT_PUSH_12: None,
                C4SID_VPOT_PUSH_13: None, C4SID_VPOT_PUSH_14: None, C4SID_VPOT_PUSH_15: None,
                C4SID_VPOT_PUSH_16: None, C4SID_VPOT_PUSH_17: None, C4SID_VPOT_PUSH_18: None,
                C4SID_VPOT_PUSH_19: None, C4SID_VPOT_PUSH_20: None, C4SID_VPOT_PUSH_21: None,
                C4SID_VPOT_PUSH_22: None, C4SID_VPOT_PUSH_23: None, C4SID_VPOT_PUSH_24: None,
                C4SID_VPOT_PUSH_25: None, C4SID_VPOT_PUSH_26: None, C4SID_VPOT_PUSH_27: None,
                C4SID_VPOT_PUSH_28: None, C4SID_VPOT_PUSH_29: None, C4SID_VPOT_PUSH_30: None,
                C4SID_VPOT_PUSH_31: None, C4SID_VPOT_PUSH_32: None},
            MIDI_CC_TYPE: {
                C4SID_VPOT_CC_ADDRESS_1: None, C4SID_VPOT_CC_ADDRESS_2: None, C4SID_VPOT_CC_ADDRESS_3: None,
                C4SID_VPOT_CC_ADDRESS_4: None, C4SID_VPOT_CC_ADDRESS_5: None, C4SID_VPOT_CC_ADDRESS_6: None,
                C4SID_VPOT_CC_ADDRESS_7: None, C4SID_VPOT_CC_ADDRESS_8: None, C4SID_VPOT_CC_ADDRESS_9: None,
                C4SID_VPOT_CC_ADDRESS_10: None, C4SID_VPOT_CC_ADDRESS_11: None, C4SID_VPOT_CC_ADDRESS_12: None,
                C4SID_VPOT_CC_ADDRESS_13: None, C4SID_VPOT_CC_ADDRESS_14: None, C4SID_VPOT_CC_ADDRESS_15: None,
                C4SID_VPOT_CC_ADDRESS_16: None, C4SID_VPOT_CC_ADDRESS_17: None, C4SID_VPOT_CC_ADDRESS_18: None,
                C4SID_VPOT_CC_ADDRESS_19: None, C4SID_VPOT_CC_ADDRESS_20: None, C4SID_VPOT_CC_ADDRESS_21: None,
                C4SID_VPOT_CC_ADDRESS_22: None, C4SID_VPOT_CC_ADDRESS_23: None, C4SID_VPOT_CC_ADDRESS_24: None,
                C4SID_VPOT_CC_ADDRESS_25: None, C4SID_VPOT_CC_ADDRESS_26: None, C4SID_VPOT_CC_ADDRESS_27: None,
                C4SID_VPOT_CC_ADDRESS_28: None, C4SID_VPOT_CC_ADDRESS_29: None, C4SID_VPOT_CC_ADDRESS_30: None,
                C4SID_VPOT_CC_ADDRESS_31: None, C4SID_VPOT_CC_ADDRESS_32: None}}

    def destroy(self):
        self.disconnect()
        self._model = None
        super(C4ElementModel, self).destroy()

    def make_encoder(self, cc_id=C4SID_VPOT_CC_ADDRESS_1, *a, **k):
        if self._model[MIDI_CC_TYPE][cc_id] is None:
            self._model[MIDI_CC_TYPE][cc_id] = self._element_factory.make_encoder(cc_id, *a, **k)
        else:
            assert False
        return self._model[MIDI_CC_TYPE][cc_id]

    def make_all_encoders(self, *a, **k):
        for cc_id in encoder_cc_ids:
            self.make_encoder(cc_id, *a, **k)

    def make_button(self, note_id=C4SID_SPLIT, *a, **k):
        if self._model[MIDI_NOTE_TYPE][note_id] is None:
            self._model[MIDI_NOTE_TYPE][note_id] = self._element_factory.make_button(note_id, *a, **k)
        else:
            assert False
        return self._model[MIDI_NOTE_TYPE][note_id]

    def make_all_encoder_buttons(self, *a, **k):
        for note_id in encoder_switch_ids:
            self.make_button(note_id, *a, **k)

    def make_all_button_buttons(self, *a, **k):
        self.make_button(C4SID_SPLIT, *a, **k)
        self.make_button(C4SID_LOCK, *a, **k)
        self.make_button(C4SID_SPLIT_ERASE, *a, **k)
        self.make_button(C4SID_MARKER, *a, **k)
        self.make_button(C4SID_TRACK, *a, **k)
        self.make_button(C4SID_CHANNEL_STRIP, *a, **k)
        self.make_button(C4SID_FUNCTION, *a, **k)
        self.make_button(C4SID_BANK_LEFT, *a, **k)
        self.make_button(C4SID_BANK_RIGHT, *a, **k)
        self.make_button(C4SID_SINGLE_LEFT, *a, **k)
        self.make_button(C4SID_SINGLE_RIGHT, *a, **k)
        self.make_button(C4SID_SHIFT, *a, **k)
        self.make_button(C4SID_OPTION, *a, **k)
        self.make_button(C4SID_CONTROL, *a, **k)
        self.make_button(C4SID_ALT, *a, **k)
        self.make_button(C4SID_SLOT_UP, *a, **k)
        self.make_button(C4SID_SLOT_DOWN, *a, **k)
        self.make_button(C4SID_TRACK_LEFT, *a, **k)
        self.make_button(C4SID_TRACK_RIGHT, *a, **k)

    def make_all_elements(self, *a, **k):
        self.make_all_encoders(*a, **k)
        self.make_all_encoder_buttons(*a, **k)
        self.make_all_button_buttons(*a, **k)

    def get_encoder(self, cc_id=C4SID_VPOT_CC_ADDRESS_1):
        return self._model[MIDI_CC_TYPE][cc_id]

    def get_encoder_by_index(self, encoder_index=0):
        cc_id = V2C4Component.convert_encoder_id_value(encoder_index)
        return self.get_encoder(cc_id)

    def get_encoder_by_row_and_column(self, row=0, column=0):
        assert row in range(NUM_ENCODER_ROWS)
        assert column in range(NUM_ENCODERS_ONE_ROW)
        return self.get_encoder_by_index(row * NUM_ENCODERS_ONE_ROW + column)

    def get_button(self, note_id=C4SID_SPLIT):
        return self._model[MIDI_NOTE_TYPE][note_id]

    def get_button_by_encoder_index(self, encoder_index=0):
        note_id = V2C4Component.convert_encoder_id_value(encoder_index)
        return self.get_button(note_id)

    def get_button_by_encoder_row_and_column(self, row=0, column=0):
        assert row in range(NUM_ENCODER_ROWS)
        assert column in range(NUM_ENCODERS_ONE_ROW)
        return self.get_button_by_encoder_index(row * NUM_ENCODERS_ONE_ROW + column)

    def get_assignment_buttons(self):  # C4SID_MARKER: C4SID_TRACK: C4SID_CHANNEL_STRIP: C4SID_FUNCTION:
        return {
            C4SID_MARKER: self._model[MIDI_NOTE_TYPE][C4SID_MARKER],
            C4SID_TRACK: self._model[MIDI_NOTE_TYPE][C4SID_TRACK],
            C4SID_CHANNEL_STRIP: self._model[MIDI_NOTE_TYPE][C4SID_CHANNEL_STRIP],
            C4SID_FUNCTION: self._model[MIDI_NOTE_TYPE][C4SID_FUNCTION]
                }

    def get_modifier_buttons(self):  # C4SID_SHIFT: C4SID_OPTION: C4SID_CONTROL: C4SID_ALT
        return {
            C4SID_SHIFT: self._model[MIDI_NOTE_TYPE][C4SID_SHIFT],
            C4SID_OPTION: self._model[MIDI_NOTE_TYPE][C4SID_OPTION],
            C4SID_CONTROL: self._model[MIDI_NOTE_TYPE][C4SID_CONTROL],
            C4SID_ALT: self._model[MIDI_NOTE_TYPE][C4SID_ALT]
                }

    def get_parameter_buttons(self):  # C4SID_BANK_LEFT: C4SID_BANK_RIGHT: C4SID_SINGLE_LEFT: C4SID_SINGLE_RIGHT
        return {
            C4SID_BANK_LEFT: self._model[MIDI_NOTE_TYPE][C4SID_BANK_LEFT],
            C4SID_BANK_RIGHT: self._model[MIDI_NOTE_TYPE][C4SID_BANK_RIGHT],
            C4SID_SINGLE_LEFT: self._model[MIDI_NOTE_TYPE][C4SID_SINGLE_LEFT],
            C4SID_SINGLE_RIGHT: self._model[MIDI_NOTE_TYPE][C4SID_SINGLE_RIGHT]
                }

    def get_session_nav_buttons(self):  # C4SID_SLOT_UP: C4SID_SLOT_DOWN: C4SID_TRACK_LEFT: C4SID_TRACK_RIGHT
        return {
            C4SID_SLOT_UP: self._model[MIDI_NOTE_TYPE][C4SID_SLOT_UP],
            C4SID_SLOT_DOWN: self._model[MIDI_NOTE_TYPE][C4SID_SLOT_DOWN],
            C4SID_TRACK_LEFT: self._model[MIDI_NOTE_TYPE][C4SID_TRACK_LEFT],
            C4SID_TRACK_RIGHT: self._model[MIDI_NOTE_TYPE][C4SID_TRACK_RIGHT]
                }

    def make_physical_display(self, nbr_segments=ENCODER_BANK_SIZE, nbr_display_chars=LCD_BOTTOM_ROW_OFFSET, *a, **k):
        return self._display_factory.make_physical_display(nbr_segments, nbr_display_chars, *a, **k)

    def get_lcd_hello_message(self):
        return self._display_factory.lcd_display_hello_message

    def get_lcd_goodbye_message(self):
        return self._display_factory.lcd_display_goodbye_message

    def get_lcd_display_clear_message(self):
        """ returns ASCII blank spaces as sysex integers """
        return self._display_factory.lcd_display_clear_message

    def get_lcd_display_id_message(self):
        return self._display_factory.lcd_display_id_message

    def set_script_handle(self, main_script=None):
        self._set_script_handle(main_script)

        