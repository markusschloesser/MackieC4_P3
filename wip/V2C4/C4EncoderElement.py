
from .V2C4Component import *

import Live

from _Framework.EncoderElement import EncoderElement  # , _not_implemented  # , ENCODER_VALUE_NORMALIZER
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler
from _Framework.CompoundElement import CompoundElement
from _Framework.InputControlElement import InputControlElement, MIDI_NOTE_TYPE, MIDI_CC_TYPE, InputSignal
from _Framework.SubjectSlot import SubjectEvent, subject_slot
from _Framework.Skin import Skin
from _Framework.Util import nop, const, in_range

from .C4Encoders import C4Encoders
from .C4EncoderMixin import C4EncoderMixin, LedMappingType
from .C4EncoderMixin import encoder_ring_led_mode_mode_select_values, encoder_ring_led_mode_cc_min_max_values


def _not_implemented(value):
    raise NotImplementedError

def signed_bit_delta(value):
    delta = SIGNED_BIT_DEFAULT_DELTA
    is_increment = value <= 64
    index = value - 1 if is_increment else value - 64
    if in_range(index, 0, len(SIGNED_BIT_VALUE_MAP)):
        delta = SIGNED_BIT_VALUE_MAP[index]
    if is_increment:
        return delta
    return -delta

SIGNED_BIT_DEFAULT_DELTA = 20.0
SIGNED_BIT_VALUE_MAP = (1, 2, 3, 4, 5, 8, 10, 20, 50)

_map_modes = map_modes = Live.MidiMap.MapMode
ENCODER_VALUE_NORMALIZER = {_map_modes.relative_smooth_two_compliment: lambda v: v if v <= 64 else v - 128,
   _map_modes.relative_smooth_signed_bit: lambda v: v if v <= 64 else 64 - v,
   _map_modes.relative_smooth_binary_offset: lambda v: v - 64,
   _map_modes.relative_signed_bit: signed_bit_delta}


class C4EncoderElement(InputControlElement, C4EncoderMixin, V2C4Component):
    """
    currently modeled on EncoderElement itself inheriting from InputControlElement
    formerly modeled on RingedEncoderElement in _APC and PeekableEncoderElement in _AxiomPro
    and TouchEncoderElementBase + TouchEncoderElement in EncoderElement itself
    """

    __module__ = __name__

    def __init__(self, identifier=C4_ENCODER_CC_ID_BASE, extended=False, channel=C4_MIDI_CHANNEL,
                 map_mode=_map_modes.relative_signed_bit, encoder_sensitivity=None, name=None, *a, **k):
        if name is None:
            name = 'Encoder_Control_%d' % identifier
        super(C4EncoderElement, self).__init__(MIDI_CC_TYPE, channel, identifier, map_mode,
                                               encoder_sensitivity, name=name, *a, **k)

        # C4EncoderElement.__init__() additions
        V2C4Component.__init__(self)
        encoder_index = identifier
        self.c4_encoder = C4Encoders(self, extended, encoder_index, map_mode)
        self._feedback_rule = None  # Live.MidiMap.CCFeedbackRule()
        self.set_feedback_delay(-1)
        self._button = None  # maybe this could be nested?
        self._undo_step_handler = DummyUndoStepHandler()
        self._skin = Skin()
        self._last_received_value = 0
        # self._last_received_raw_value = 0
        # self._input_signal_listener_count = 1

        # InputControlElement.set_report_values
        # self.set_report_values(True, True)
        self.set_needs_takeover(False)

    def disconnect(self):
        super(C4EncoderElement, self).disconnect()
        self._undo_step_handler = None
        return

    # EncoderElement methods
    # def relative_value_to_delta(self, value):
    #     assert value >= 0 and value < 128
    #     return self.__value_normalizer(value)
    #
    # def normalize_value(self, value):
    #     return self.relative_value_to_delta(value) / 64.0 * self.encoder_sensitivity
    #
    # def notify_value(self, value):
    #     super(C4EncoderElement, self).notify_value(value)
    #     if self.normalized_value_listener_count():
    #         self.notify_normalized_value(self.normalize_value(value))

    # inherited methods from ControlElement, overrides from InputControlElement
    # def reset(self):
    #     self._log_message("encoder<{}> reset".format(self.c4_encoder.encoder_index))
    #     super(C4EncoderElement, self).reset()
    #
    # def reset_state(self):
    #     self._log_message("encoder<{}> reset_state".format(self.c4_encoder.encoder_index))
    #     super(C4EncoderElement, self).reset_state()

    # inherited abstract methods from InputControlElement
    def message_map_mode(self):
        assert self.message_type() is MIDI_CC_TYPE
        return self.c4_encoder.map_mode()

    # override methods from InputControlElement
    def _mapping_feedback_values(self):
        # see def update_led_ring_display_mode(self, display_mode)
        return self.c4_encoder.led_ring_cc_values

    def receive_value(self, value):
        # self._last_received_raw_value = value
        # self._log_message("encoder<{}> received raw value<{}>".format(self.c4_encoder.encoder_index, value))
        super(C4EncoderElement, self).receive_value(value)
        # self._log_message("after super did getattr on midi_value<{}>".format(value))
        self._last_received_value = value

    # def _report_value(self, value, is_input):
    #     self._verify_value(value)
    #     message = str(self.name) + ' ('
    #     if self._msg_type == MIDI_CC_TYPE:
    #         message += 'CC ' + str(self._msg_identifier) + ', '
    #         message += 'Chan. ' + str(self._msg_channel)
    #         message += ') '
    #         message += 'received value ' if is_input else 'sent value '
    #         message += str(value)
    #         self._log_message(message)
    #     else:
    #         super(C4EncoderElement, self)._report_value(value, is_input)


    # V2C4 specific methods
    def set_script_handle(self, main_script=None):
        self._set_script_handle(main_script)

    # C4EncoderMixin abstract methods
    def set_ring_mode(self, mode):
        self.update_led_ring_display_mode(mode)

    # C4EncoderElement specific methods
    def feedback_cc_id(self):
        return self.c4_encoder.encoder_ring_feedback_cc_id

    def update_led_ring_display_mode(self, display_mode=LedMappingType.VPOT_DISPLAY_SINGLE_DOT, extended=False):
        if display_mode in encoder_ring_led_mode_mode_select_values.keys():
            # side effect of new C4Encoder: updates self.c4_encoder.led_ring_cc_values tuple,
            # see def _mapping_feedback_values(self)
            self.c4_encoder = C4Encoders(self, extended, self.c4_encoder.encoder_index,
                                         self.c4_encoder.map_mode(), display_mode)
            self.set_midi_feedback_data()

    def set_midi_feedback_data(self):
        self.set_feedback_delay(self.c4_encoder.led_ring_feedback_delay)
        # c4_encoder.specialize_feedback_rule() returns a Live.MidiMap.CCFeedbackRule() instance
        self._feedback_rule = self.c4_encoder.specialize_feedback_rule()
        self._request_rebuild()

    def send_led_ring_midi_cc(self, cc_val, force=False):
        self.c4_encoder.send_led_ring_midi_cc(self, cc_val, force)

    def send_led_ring_full_off(self, force=False):
        self.c4_encoder.send_led_ring_full_off(self, force)

    def send_led_ring_min_on(self, force=False):
        self.c4_encoder.send_led_ring_min_on(self, force)

    def send_led_ring_max_on(self, force=False):
        self.c4_encoder.send_led_ring_max_on(self, force)

    def set_encoder_button(self, new_button):
        assert new_button is None or isinstance(new_button, ButtonElement)
        # if self._button is not None:
        #     self._button.
        self._button = new_button

    def get_encoder_button(self):
        return self._button

