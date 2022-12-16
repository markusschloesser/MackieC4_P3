
from .Utils import *


class LedMappingType(object):
    """ The various types of parameter mappings that correspond to C4 LED ring modes. """
    __module__ = __name__
    VPOT_DISPLAY_SINGLE_DOT = 0
    VPOT_DISPLAY_BOOST_CUT = 1
    VPOT_DISPLAY_WRAP = 2
    VPOT_DISPLAY_SPREAD = 3
    VPOT_DISPLAY_BOOLEAN = 4


# min  max leds in ring illuminated
# (multiples of 0x10 mean "all ring LEDS OFF" [0, 16, 32, 48]
encoder_ring_led_mode_cc_min_max_values = {
    LedMappingType.VPOT_DISPLAY_SINGLE_DOT: (0x01, 0x0B),  # 01 - 0B
    LedMappingType.VPOT_DISPLAY_BOOST_CUT: (0x11, 0x1B),  # 11 - 1B
    LedMappingType.VPOT_DISPLAY_WRAP: (0x21, 0x2B),  # 21 - 2B
    LedMappingType.VPOT_DISPLAY_SPREAD: (0x31, 0x36),  # 31 - 36
    # -- goes to ON in about 6 steps
    LedMappingType.VPOT_DISPLAY_BOOLEAN: (0x20, 0x2B)}  # 20 - 2B

encoder_ring_led_mode_mode_select_values = {
    LedMappingType.VPOT_DISPLAY_SINGLE_DOT: 0x01,
    LedMappingType.VPOT_DISPLAY_BOOST_CUT: 0x16,
    LedMappingType.VPOT_DISPLAY_WRAP: 0x26,
    LedMappingType.VPOT_DISPLAY_SPREAD: 0x33,
    LedMappingType.VPOT_DISPLAY_BOOLEAN: 0x2B}

class C4EncoderMixin(object):
    """
        C4EncoderMixin (modeled after RingedEncoderMixin) is a mixin for an encoder/slider that includes LEDs that can
        operate in several modes (such as single dot, boost cut, wrap, spread, etc).
    """
    __module__ = __name__


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

    def set_ring_mode(self, mode):
        """ Called to set the ring mode based on the passed mode. To be overridden. """
        raise NotImplementedError

    def send_value_on_ring_mode_change(self, value):
        """ Sends a value to the ring mode button upon the ring mode being changed.  This
        is broken out for specializations. """
        self.send_value(value, True)

    def _update_ring_mode(self):
        value_to_send = 0
        param = self.mapped_parameter()
        if self._property_to_map_to:
            param = self._property_to_map_to
        if self.is_mapped_manually():
            self.set_ring_mode(LedMappingType.VPOT_DISPLAY_WRAP)
        else:
            if live_object_is_valid(param):
                p_range = param.max - param.min
                if p_range > 0:
                    value = parameter_value_to_midi_value(param.value, param.min, param.max)
                    if param.min == -1 * param.max:
                        self.set_ring_mode(LedMappingType.VPOT_DISPLAY_BOOST_CUT)
                    else:
                        if parameter_is_quantized(param):
                            self.set_ring_mode(LedMappingType.VPOT_DISPLAY_SINGLE_DOT)
                        else:
                            self.set_ring_mode(LedMappingType.VPOT_DISPLAY_WRAP)
                    value_to_send = int(value)
                else:
                    self.set_ring_mode(LedMappingType.VPOT_DISPLAY_BOOLEAN)
            else:
                self.set_ring_mode(LedMappingType.VPOT_DISPLAY_SPREAD)
        self.send_value_on_ring_mode_change(value_to_send)