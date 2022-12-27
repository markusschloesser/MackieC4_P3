from .V2C4Component import *

from _Framework.EncoderElement import EncoderElement, map_modes
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler
from _Framework.SubjectSlot import SlotManager, subject_slot
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Skin import Skin


from .C4EncoderMixin import C4EncoderMixin, LedMappingType, TWO_COMP, SIGNED_BIT
from .Utils import live_object_is_valid

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


class C4EncoderElement(EncoderElement, SlotManager, C4EncoderMixin, V2C4Component):
    """
        Mostly modeled now on SpecialEncoderElement.  This class directly imports from the framework
        EncoderElement class again.  Almost all C4 custom functionality is now implemented in the C4EncoderElementMixin
        class.
    """

    __module__ = __name__
    __subject_events__ = ('parameter', 'parameter_name', 'parameter_value')

    def __init__(self, identifier=C4_ENCODER_CC_ID_BASE, channel=C4_MIDI_CHANNEL,
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
        self._last_received_value = -1
        self._thinner = 0
        self._property_to_map_to = None
        self._is_enabled = True

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



    @property
    def parameter(self):
        """ Returns the parameter or property this encoder is assigned to. """
        return self._parameter_to_map_to or self._property_to_map_to

    @property
    def parameter_name(self):
        """ (For use with M4L and displays): Returns the name of the parameter or property
        this encoder is assigned to. If not assigned, returns the CC# of the encoder if
        it's been translated. """
        param = self._parameter_to_map_to or self._property_to_map_to
        if param is None:
            if self.message_channel() != self.original_channel():
                header = 'Map#' if self.is_enabled() else 'CC#'
                return '%s %s' % (header, self.message_identifier())
            return ''
        return param.name

    @property
    def parameter_value(self):
        """ (For use with M4L and displays): Returns the unicode value of the parameter
        or property this encoder is assigned to. """
        param = self._parameter_to_map_to or self._property_to_map_to
        if param is not None:
            return unicode(param)
        else:
            return ''

    @subject_slot('value')
    def _on_parameter_value_changed(self):
        """ Notifies listeners of parameter_value upon changes. """
        self.notify_parameter_value(self.parameter_value)

    @subject_slot('name')
    def _on_parameter_name_changed(self):
        """ Notifies listeners of parameter_name upon changes. """
        self.notify_parameter_name(self.parameter_name)

    def release_parameter(self):
        """ Extends standard to send 0 value to clear LED if no parameter to map to
        and notify listener. """
        self._property_to_map_to = None
        super(C4EncoderElement, self).release_parameter()
        if not self.is_mapped_manually() and not self._parameter_to_map_to:
            self.send_value(0, force=True)
        self._update_assignment_and_notify()
        return

    def install_connections(self, install_translation=None, install_mapping=None, install_forwarding=None):
        """ Extends standard to notify listener. """
        super(C4EncoderElement, self).install_connections(install_translation, install_mapping, install_forwarding)
        self._update_assignment_and_notify()

    def set_property_to_map_to(self, prop):
        """ Sets the property to map to and notifies listeners. """
        notify = prop != self._property_to_map_to
        self._property_to_map_to = prop
        if notify:
            self._update_assignment_and_notify()

    def _update_assignment_and_notify(self):
        """ Updates/verifies this encoder's assignment, notifies listeners and sets up
        value and name listeners. """
        param = self.mapped_parameter()
        if self._property_to_map_to:
            param = self._property_to_map_to
        if self.is_mapped_manually() or not live_object_is_valid(param):
            param = None
        self.notify_parameter(param)
        self.notify_parameter_name(self.parameter_name)
        self.notify_parameter_value(self.parameter_value)
        self._on_parameter_value_changed.subject = param
        self._on_parameter_name_changed.subject = param
        return

    def is_enabled(self):
        """ Returns whether this control is enabled. """
        return self._is_enabled

    def set_enabled(self, enabled):
        """ Enables/disables the control. When disabled, it can be used for sending data
        to MIDI tracks. """
        if self._is_enabled != bool(enabled):
            self._is_enabled = bool(enabled)
            self._request_rebuild()

    def is_mapped_manually(self):
        """ Returns whether the encoder has been MIDI mapped. """
        return not self._is_mapped and not self._is_being_forwarded

    # def receive_value(self, value):
    #     """ Extends standard to store last received value. """
    #     super(C4EncoderElement, self).receive_value(value)
    #     self._last_received_value = value

    def get_adjustment_factor(self, value, threshold=10):
        """ Returns the adjustment factor to use for endless encoders. Applies thinning
        (using the given threshold if it isn't 0) to allow for more coarse adjustment. """
        if threshold:
            factor = -1
            if value <= 63:
                factor = 1
            if self._thinner is not 0:
                self._thinner += factor
                if abs(self._thinner) >= threshold:
                    self._thinner = 0
                    return factor
            else:
                self._thinner = factor
        else:
            factor = value
            if value > 63:
                if self.message_map_mode() in TWO_COMP:
                    factor = -(128 - value)
                elif self.message_map_mode() in SIGNED_BIT:
                    factor = 64 - value
            return factor
        return 0

    def script_wants_forwarding(self):
        """ Returns whether or not the control should be used in the script or to send
        data to MIDI tracks. """
        return self._is_enabled

    def should_suppress_feedback_for_property_controls(self):
        """ For use with absolute encoders with LEDs, this determines if PropertyControl
        should send feedback to the control or should suppress the feedback after the
        control has been moved.  This will be True in most cases. """
        return True
