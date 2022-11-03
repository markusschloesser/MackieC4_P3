from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import object, range, str

from .C4_DEFINES import *

# can't import like this, circular dependency city
# from .V2C4 import V2C4



class V2C4Component(object):
    """ Baseclass for every specialized 'subcomponent' of the Mackie C4 in this V2 script.
        This class allows inheriting subclasses to reference public methods of the V2C4
        ControlSurface class as if they were referencing inherited methods of V2C4Component
         (because they are inheriting methods of V2C4Component)"""
    __module__ = __name__

    def __init__(self):
        self._script_backdoor_handle = None

    def destroy(self):
        pass

    def _set_script_handle(self, main_script):
        # can't validate like this because can't import V2C4
        # assert isinstance(main_script, V2C4)
        self._script_backdoor_handle = main_script

    def _log_message(self, *message):
        """ Overrides ControlSurface standard to only use python logger and not also c_instance logger """
        if self._script_backdoor_handle is not None:
            try:
                message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
                self._script_backdoor_handle.get_logger().info(message)
            except:
                self._script_backdoor_handle.get_logger().info('Logging encountered illegal character(s)!')

    @staticmethod
    def make_scaling_function(self, lval_min, lval_max, rval_min, rval_max):
        # Figure out how 'wide' each range is
        fixed_range = lval_max - lval_min
        range_to_scale = rval_max - rval_min

        # Compute the scale factor between left and right values
        scaleFactor = float(range_to_scale) / float(fixed_range)

        # create interpolation function using pre-calculated scaleFactor
        def interpolation_function(value):
            return rval_min + (value - lval_min) * scaleFactor

        return interpolation_function

    @staticmethod
    def convert_encoder_id_value(convertable_value):
        """
            directly Sconverts between index values in the ranges 0x00 - 0x01F and 0x20 - 0x3F
            input 0x00      output 0x20
            input 0x3F      output 0x1F
            input any number outside either range, output the same number
        """
        return_value = convertable_value
        if convertable_value in encoder_cc_ids:
            return_value = convertable_value - 0x20
        elif convertable_value in encoder_index_range:
            return_value = convertable_value + 0x20
        return return_value
