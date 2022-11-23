
from .V2C4Component import *

# import Live

from _Framework.EncoderElement import EncoderElement, _not_implemented, ENCODER_VALUE_NORMALIZER
from _Framework.ButtonElement import ButtonElement
from _Framework.CompoundElement import CompoundElement
from _Framework.InputControlElement import InputControlElement, MIDI_CC_TYPE, InputSignal
from _Framework.SubjectSlot import SubjectEvent, subject_slot
from _Framework.Util import nop, const

from .C4Encoders import C4Encoders


class C4EncoderElement(InputControlElement, V2C4Component):
    """
    currently modeled on EncoderElement itself inheriting from InputControlElement
    formerly modeled on RingedEncoderElement in _APC and PeekableEncoderElement in _AxiomPro
    and TouchEncoderElementBase + TouchEncoderElement in EncoderElement itself
    """

    __module__ = __name__

    class ProxiedInterface(InputControlElement.ProxiedInterface):
        __module__ = __name__
        normalize_value = nop

    __subject_events__ = (
     SubjectEvent(name='normalized_value', signal=InputSignal),)
    encoder_sensitivity = 1.0

    def __init__(self, identifier=C4SID_VPOT_CC_ADDRESS_BASE, extended=False, channel=C4_MIDI_CHANNEL,
                 map_mode=C4Encoders.map_mode(), encoder_sensitivity=None, name=None, *a, **k):
        if name is None:
            name = 'Encoder_Control_%d' % V2C4Component.convert_encoder_id_value(identifier)
        super(C4EncoderElement, self).__init__(MIDI_CC_TYPE, channel, identifier, name=name, *a, **k)

        # _Framework.EncoderElement.__init__()
        if encoder_sensitivity is not None:  # if input parameter is not None
            # replaces assignment above __init__  encoder_sensitivity = 1.0
            self.encoder_sensitivity = encoder_sensitivity
        self.__map_mode = map_mode
        self.__value_normalizer = ENCODER_VALUE_NORMALIZER.get(map_mode, _not_implemented)

        # C4EncoderElement.__init__() additions
        V2C4Component.__init__(self)
        encoder_index = V2C4Component.convert_encoder_id_value(identifier)
        self.c4_encoder = C4Encoders(self, extended, encoder_index, map_mode)
        self._feedback_rule = None  # Live.MidiMap.CCFeedbackRule()
        self.set_feedback_delay(-1)
        self._button = None  # maybe this could be nested?

        # InputControlElement.set_report_values
        self.set_report_values(True, True)

    # EncoderElement methods
    def relative_value_to_delta(self, value):
        assert value >= 0 and value < 128
        return self.__value_normalizer(value)

    def normalize_value(self, value):
        return self.relative_value_to_delta(value) / 64.0 * self.encoder_sensitivity

    def notify_value(self, value):
        super(C4EncoderElement, self).notify_value(value)
        if self.normalized_value_listener_count():
            self.notify_normalized_value(self.normalize_value(value))

    # inherited abstract methods from InputControlElement
    def message_map_mode(self):
        # assert self.message_type() is MIDI_CC_TYPE
        return self.__map_mode

    # override methods from InputControlElement
    def _mapping_feedback_values(self):
        # see def update_led_ring_display_mode(self, display_mode)
        return self.c4_encoder.led_ring_cc_values

    def receive_value(self, value):
        self._log_message("encoder<{}> received midi value<{}>".format(self.message_identifier(), value))
        value = getattr(value, 'midi_value', value)
        self._log_message("after getattr on midi_value<{}>".format(value))
        self._verify_value(value)
        self._last_sent_message = None
        self.notify_value(value)
        if self._report_input:
            is_input = True
            self._report_value(value, is_input)

    # V2C4 specific methods
    def set_script_handle(self, main_script=None):
        self._set_script_handle(main_script)

    def update_led_ring_display_mode(self, display_mode=VPOT_DISPLAY_SINGLE_DOT, extended=False):
        if display_mode in encoder_ring_led_mode_values.keys():
            # side effect of new C4Encoder: updates self.c4_encoder.led_ring_cc_values tuple,
            # see def _mapping_feedback_values(self)
            self.c4_encoder = C4Encoders(self, extended, self.c4_encoder.encoder_index,
                                         C4Encoders.map_mode(), display_mode)
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


    # def install_connections(self, install_translation, install_mapping, install_forwarding):
    #     self._send_delayed_messages_task.kill()
    #     self._is_mapped = False
    #     self._is_being_forwarded = False
    #     if self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
    #         install_translation(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)
    #     if self._parameter_to_map_to != None:
    #         self._is_mapped = install_mapping(self, self._parameter_to_map_to, self._mapping_feedback_delay, self._mapping_feedback_values())
    #     if self.script_wants_forwarding():
    #         self._is_being_forwarded = install_forwarding(self)
    #         if self._is_being_forwarded and self.send_depends_on_forwarding:
    #             self._send_delayed_messages_task.restart()
    #     return
    #

    # def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
    #     super(C4EncoderElement, self).install_connections(install_translation_callback,
    #                                                       install_mapping_callback, install_forwarding_callback)
    #     if not self._is_mapped and self.value_listener_count() == 0:
    #         self._is_being_forwarded = install_forwarding_callback(self)
    #     self._update_ring_mode()
    #
    # def is_mapped_manually(self):
    #     return not self._is_mapped and not self._is_being_forwarded
    #
    #
    # def _update_ring_mode(self):
    #     pass
        # if self._ring_mode_button != None:
        #     if self.is_mapped_manually():
        #         self._ring_mode_button.send_value(RING_SIN_VALUE, force=True)
        #     elif self._parameter_to_map_to != None:
        #         param = self._parameter_to_map_to
        #         p_range = param.max - param.min
        #         value = (param.value - param.min) / p_range * 127
        #         self.send_value(int(value), force=True)
        #         if self._parameter_to_map_to.min == -1 * self._parameter_to_map_to.max:
        #             self._ring_mode_button.send_value(RING_PAN_VALUE, force=True)
        #         elif self._parameter_to_map_to.is_quantized:
        #             self._ring_mode_button.send_value(RING_SIN_VALUE, force=True)
        #         else:
        #             self._ring_mode_button.send_value(RING_VOL_VALUE, force=True)
        #     else:
        #         self._ring_mode_button.send_value(RING_OFF_VALUE, force=True)
        # return

    # def build_midi_map(self, midi_map_handle):
    #     avoid_takeover = True
    #     takeover_mode = not avoid_takeover
    #     Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, self.mapped_parameter(),
    #                                                self.message_channel, self.message_identifier,
    #                                                self.message_map_mode(),
    #                                                self._feedback_rule, takeover_mode, sensitivity=1.0)

