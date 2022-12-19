import Live

from _Framework.Util import const, nop

from .Utils import *
from .V2C4Component import *


class LedMappingType(object):
    """ The various types of parameter mappings that correspond to C4 LED ring modes. """
    __module__ = __name__
    LED_RING_MODE_SINGLE_DOT = 0
    LED_RING_MODE_BOOST_CUT = 1
    LED_RING_MODE_WRAP = 2
    LED_RING_MODE_SPREAD = 3
    LED_RING_MODE_BOOLEAN = 4


# min  max leds in ring illuminated
# (multiples of 0x10 mean "all ring LEDS OFF" [0, 16, 32, 48]
encoder_ring_led_mode_cc_min_max_values = {
    LedMappingType.LED_RING_MODE_SINGLE_DOT: (0x01, 0x0B),  # 01 - 0B
    LedMappingType.LED_RING_MODE_BOOST_CUT: (0x11, 0x1B),  # 11 - 1B
    LedMappingType.LED_RING_MODE_WRAP: (0x21, 0x2B),  # 21 - 2B
    LedMappingType.LED_RING_MODE_SPREAD: (0x31, 0x36),  # 31 - 36
    # -- goes to ON in about 6 steps
    LedMappingType.LED_RING_MODE_BOOLEAN: (0x20, 0x2B)}  # 20 - 2B

encoder_ring_led_mode_mode_select_values = {
    LedMappingType.LED_RING_MODE_SINGLE_DOT: 0x01,
    LedMappingType.LED_RING_MODE_BOOST_CUT: 0x16,
    LedMappingType.LED_RING_MODE_WRAP: 0x26,
    LedMappingType.LED_RING_MODE_SPREAD: 0x33,
    LedMappingType.LED_RING_MODE_BOOLEAN: 0x2B}


class C4EncoderMixin(object):
    """
        C4EncoderMixin (modeled after RingedEncoderMixin) is a mixin for an encoder/slider that includes LEDs that can
        operate in several modes (such as single dot, boost cut, wrap, spread, etc).
    """
    __module__ = __name__

    _cc_feedback_value_map = ()
    _feedback_ring_mode = LedMappingType.LED_RING_MODE_SINGLE_DOT
    __default_midi_map_mode = Live.MidiMap.MapMode.relative_signed_bit
    feedback_value_scaler = const(nop)

    def release_parameter(self):
        """ Extends standard to update ring mode. """
        super(C4EncoderMixin, self).release_parameter()
        self._update_ring_mode()

    def install_connections(self, *a, **k):
        """ Extends standard to update ring mode. """
        super(C4EncoderMixin, self).install_connections(*a, **k)
        self._update_ring_mode()

    def connect_to(self, p):
        """ Extends standard to update ring mode. """
        super(C4EncoderMixin, self).connect_to(p)
        self._update_ring_mode()

    def set_property_to_map_to(self, prop):
        """ Extends standard to update ring mode. """
        super(C4EncoderMixin, self).set_property_to_map_to(prop)
        self._update_ring_mode()

    def c4_row_id(self):
        encoder_index = self.message_identifier()
        row_id = 3
        if encoder_index in row_00_encoder_indexes:
            row_id = 0
        elif encoder_index in row_01_encoder_indexes:
            row_id = 1
        elif encoder_index in row_02_encoder_indexes:
            row_id = 2
        return row_id

    def c4_row_index(self):
        return self.message_identifier() % NUM_ENCODERS_ONE_ROW

    def c4_encoder_index(self):
        return self.message_identifier()

    def message_feedback_identifier(self):
        return V2C4Component.convert_encoder_id_value(self.message_identifier())

    def led_ring_feedback_delay(self):
        return -1  # this is where the const -1 delay value is defined

    def update_led_ring_display_mode(self, mode):
        """ Called to set the ring mode based on the passed mode. To be overridden. """
        raise NotImplementedError

    def set_led_ring_display_mode(self, display_mode):
        """ no change unless display_mode is in C4EncoderMixin.encoder_ring_led_mode_mode_select_values.keys() """
        if display_mode in encoder_ring_led_mode_mode_select_values.keys():
            self._feedback_ring_mode = display_mode
            display_mode_min_value = encoder_ring_led_mode_cc_min_max_values[display_mode][0]
            display_mode_max_value = encoder_ring_led_mode_cc_min_max_values[display_mode][1]
            feedback_val_range_len = display_mode_max_value - display_mode_min_value + 1
            if display_mode == LedMappingType.LED_RING_MODE_BOOLEAN:
                halfway = feedback_val_range_len / 2
                bool_values = [display_mode_min_value if x < halfway else display_mode_max_value
                               for x in range(feedback_val_range_len)]
                self._cc_feedback_value_map = tuple(bool_values)
            else:
                self._cc_feedback_value_map = tuple([display_mode_min_value + x for x in range(feedback_val_range_len)])

            self.feedback_value_scaler = V2C4Component.make_scaling_function(0, 127,
                                                                             display_mode_min_value,
                                                                             display_mode_max_value)

    def specialize_feedback_rule(self, feedback_rule=Live.MidiMap.CCFeedbackRule()):
        feedback_rule.channel = self.message_channel()
        feedback_rule.cc_no = self.message_feedback_identifier()
        feedback_rule.cc_value_map = self.led_ring_cc_values()
        feedback_rule.delay_in_ms = self._mapping_feedback_delay
        return feedback_rule

    def led_ring_cc_values(self):
        return self._cc_feedback_value_map

    def send_led_ring_midi_cc(self, cc_val, force=False):
        assert cc_val in self.led_ring_cc_values() or cc_val == 0
        self.send_value(cc_val, force=force, channel=self.message_channel())

    def send_led_ring_full_off(self, force=False):
        self.send_led_ring_midi_cc(LED_OFF_DATA, force)

    def send_led_ring_min_on(self, force=False):
        """
           for Boost Cut Mode "minimum ON" means in effect "full pan left"
           for Spread mode "minimum ON" means in effect "pan Center"
           for Boolean mode "minimum ON" means in effect "OFF"
        """
        min_on_value_index = 0
        min_on_value = encoder_ring_led_mode_cc_min_max_values[self.feedback_map_mode()][min_on_value_index]
        self.send_led_ring_midi_cc(min_on_value, force)

    def send_led_ring_max_on(self, force=False):
        """
            for Boost Cut Mode "maximum ON" means in effect "full pan right"
            for all other ring modes "maximum ON" means all leds illuminated
        """
        max_on_value_index = 1
        max_on_value = encoder_ring_led_mode_cc_min_max_values[self.feedback_map_mode()][max_on_value_index]
        self.send_led_ring_midi_cc(max_on_value, force)

    def map_mode(self):
        return self.__default_midi_map_mode

    def feedback_map_mode(self):
        return self._feedback_ring_mode

    def send_value_on_ring_mode_change(self, value):
        """ Sends a value to the ring mode button upon the ring mode being changed.  This
        is broken out for specializations. """
        self.send_value(self.feedback_value_scaler(value), True)

    def _update_ring_mode(self):
        value_to_send = 0
        param = self.mapped_parameter()
        if self._property_to_map_to:
            param = self._property_to_map_to

        if self.is_mapped_manually():
            self.set_ring_mode(LedMappingType.LED_RING_MODE_WRAP)
        else:
            if live_object_is_valid(param):
                p_range = param.max - param.min
                if p_range > 0:
                    value = parameter_value_to_midi_value(param.value, param.min, param.max)
                    if param.min == -1 * param.max:
                        self.set_ring_mode(LedMappingType.LED_RING_MODE_BOOST_CUT)
                    else:
                        if parameter_is_quantized(param):
                            self.set_ring_mode(LedMappingType.LED_RING_MODE_SINGLE_DOT)
                        else:
                            self.set_ring_mode(LedMappingType.LED_RING_MODE_WRAP)
                    value_to_send = int(value)
                else:
                    self.set_ring_mode(LedMappingType.LED_RING_MODE_BOOLEAN)  # only when p_range <= 0
            else:
                self.set_ring_mode(LedMappingType.LED_RING_MODE_SPREAD)  # only when not live_object_is_valid(param)
        self.send_value_on_ring_mode_change(value_to_send)