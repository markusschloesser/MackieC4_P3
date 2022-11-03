
from .V2C4Component import *

# import Live

from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import MIDI_MSG_TYPES, MIDI_CC_TYPE

from .C4Encoders import C4Encoders


class C4EncoderElement(EncoderElement, V2C4Component):
    """ modeled on RingedEncoderElement in _APC and PeekableEncoderElement in _AxiomPro"""

    __module__ = __name__

    def __init__(self, identifier=C4SID_VPOT_CC_ADDRESS_BASE, extended=False, channel=C4_MIDI_CHANNEL,
                 map_mode=C4Encoders.map_mode(), *a, **k):
        super(C4EncoderElement, self).__init__(MIDI_CC_TYPE, channel, identifier, map_mode, *a, **k)

        V2C4Component.__init__(self)

        encoder_index = V2C4Component.convert_encoder_id_value(identifier)
        V2C4Component._log_message(self, "encoderId <{}> calc idx <{}>".format(identifier, encoder_index))
        self.c4_encoder = C4Encoders(self, extended, encoder_index, map_mode)
        self._feedback_rule = None
        self.set_feedback_delay(0.0)
        self._button = ButtonElement


    def set_script_handle(self, main_script):
        """ to log from this class only through Python, for example, need to set this script handle """
        self._set_script_handle(main_script)

    def update_led_ring_display_mode(self, display_mode=VPOT_DISPLAY_SINGLE_DOT, extended=False):
        if display_mode in encoder_ring_led_mode_values.keys():
            self.c4_encoder = C4Encoders(self, extended, self.c4_encoder.encoder_index,
                                         C4Encoders.map_mode(), display_mode)
            self.set_midi_feedback_data()

    def set_midi_feedback_data(self):
        self.set_feedback_delay(self.c4_encoder.led_ring_feedback_delay)
        self._feedback_rule = self.c4_encoder.specialize_feedback_rule()
        self._request_rebuild()

    def _mapping_feedback_values(self):
        return self.c4_encoder.led_ring_cc_values

    def send_led_ring_midi_cc(self, cc_val):
        self.c4_encoder.send_led_ring_midi_cc(self, cc_val)

    def send_led_ring_full_off(self):
        self.c4_encoder.send_led_ring_full_off(self)

    def send_led_ring_min_on(self):
        self.c4_encoder.send_led_ring_min_on(self)

    def send_led_ring_max_on(self):
        self.c4_encoder.send_led_ring_max_on(self)

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

