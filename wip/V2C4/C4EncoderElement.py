from .V2C4Component import *

from _Framework.EncoderElement import EncoderElement, map_modes
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Skin import Skin


from .C4EncoderMixin import C4EncoderMixin, LedMappingType

# # from ableton.v2.control_surface.elements.encoder import signed_bit_delta
# def signed_bit_delta(value):
#     delta = SIGNED_BIT_DEFAULT_DELTA
#     is_increment = value <= 64
#     index = value - 1 if is_increment else value - 64
#     if in_range(index, 0, len(SIGNED_BIT_VALUE_MAP)):
#         delta = SIGNED_BIT_VALUE_MAP[index]
#     if is_increment:
#         return delta
#     return -delta

SIGNED_BIT_VALUE_MAP = (1, 1, 2, 3, 4, 5, 8, 11, 11, 13, 13, 15, 15, 20, 50)  # length is 15


class C4EncoderElement(EncoderElement, C4EncoderMixin, V2C4Component):
    """
        The direct modeling heritage of this class has changed so many times, it's too much work for too little payoff
        to document all the change details accurately now.  This class directly imports from the framework
        EncoderElement class again.  Almost all C4 custom functionality is now implemented in the C4EncoderElementMixin
        class.
    """

    __module__ = __name__

    def __init__(self, identifier=C4_ENCODER_CC_ID_BASE, extended=False, channel=C4_MIDI_CHANNEL,
                 map_mode=map_modes.relative_signed_bit, encoder_sensitivity=None, name=None, *a, **k):
        if name is None:
            name = 'Encoder_Control_%d' % identifier
        super(C4EncoderElement, self).__init__(MIDI_CC_TYPE, channel, identifier, map_mode,
                                               encoder_sensitivity, name=name, *a, **k)

        # C4EncoderElement.__init__() specific overrides of InputControlElement defaults
        self.set_feedback_delay(self.led_ring_feedback_delay())
        self.set_needs_takeover(False)
        # self.set_report_values(True, True)

        # C4EncoderElement.__init__() additions
        V2C4Component.__init__(self)

        # not currently used (bug hunting leftovers that might become useful?)
        self._button = None
        # see v2 "TouchEncoderElement" and _Framework ButtonElement
        # (also _NKFW2 "SpecialEncoderElement")
        self._undo_step_handler = DummyUndoStepHandler()
        self._skin = Skin()
        self._last_received_value = 0

    def disconnect(self):
        super(C4EncoderElement, self).disconnect()
        self._undo_step_handler = None
        return

    # inherited abstract methods from C4EncoderElementMixin
    def update_led_ring_display_mode(self, display_mode=LedMappingType.LED_RING_MODE_SINGLE_DOT):
        self.set_led_ring_display_mode(display_mode)
        self._request_rebuild()

    # override methods from InputControlElement
    def _mapping_feedback_values(self):
        return self.led_ring_cc_values()

    def _do_send_value(self, value, channel=None):
        data_byte1 = self.message_feedback_identifier()
        data_byte2 = value
        status_byte = self._status_byte(self._original_channel)
        if self.send_midi((status_byte, data_byte1, data_byte2)):
            # following probably still uses "message_identifier" not "message_feedback_identifier"
            self._last_sent_message = (value, channel)
            if self._report_output:
                is_input = False
                self._report_value(value, is_input)
        return

    def receive_value(self, value):
        # override standard to store _last_received_value and maybe log
        # see InputControlElement._last_sent_value
        super(C4EncoderElement, self).receive_value(value)
        # self._log_message("encoder<{}> received value<{}>".format(self.encoder_index(), value))
        self._last_received_value = value

    # # override standard to report values in normal script log (not DEBUG log mode)
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

    # C4EncoderElement specific methods
    def set_encoder_button(self, new_button):
        assert new_button is None or isinstance(new_button, ButtonElement)
        # if self._button is not None:
        #     self._button.
        self._button = new_button

    def get_encoder_button(self):
        return self._button

    # def set_midi_feedback_data(self):
    #     self.set_feedback_delay(self.led_ring_feedback_delay())
    #     # specialize_feedback_rule() returns a Live.MidiMap.CCFeedbackRule() instance
    #     self._feedback_rule = self.specialize_feedback_rule()
    #     self._request_rebuild()

