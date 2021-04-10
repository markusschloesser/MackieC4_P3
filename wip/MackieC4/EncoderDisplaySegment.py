# new class for this C4 project
#
from __future__ import absolute_import, print_function, unicode_literals

import itertools

from .MackieC4Component import *
from ableton.v2.base import liveobj_valid  # MS

import sys
# from Live import DeviceParameter
from Push2.model import DeviceParameter
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range

from itertools import chain
from ableton.v2.base import liveobj_valid, listenable_property, listens  # MS not needed right now, but will in the future
from ableton.v2.control_surface import InternalParameterBase, ParameterInfo, PitchParameter


class EncoderDisplaySegment(MackieC4Component):
    """ Represents what to display on the LCD over one encoder of the Mackie C4 """
    __module__ = __name__

    def __init__(self, main_script, vpot_index):
        # starting from same basic constructor as Encoders
        MackieC4Component.__init__(self, main_script)
        self.within_destroy = False
        self.__encoder_controller = None  # controls both the encoder and this LCD display segment
        self.__encoder = None  # the encoder associated with this LCD display segment
        self.__vpot_index = vpot_index
        # self.__vpot_cc_nbr = vpot_index + C4SID_VPOT_CC_ADDRESS_BASE

        self.__upper_text = '      '  # top line of the LCD display over the encoder at __vpot_index
        self.__lower_text = '      '  # bottom line

        return

    def set_encoder_controller(self, encoder_controller):
        """ The EncoderController that controls the Encoders should also control these EncoderDisplayParameters"""
        self.__encoder_controller = encoder_controller
        self.__set_encoder()

    def __set_encoder(self):
        self.__encoder = next(x for x in self.__encoder_controller.get_encoders() if x.vpot_index() == self.__vpot_index)

    def vpot_index(self):
        """ The zero based index (0 - 31) of the LCD screen space over the encoder at the same index"""
        return self.__vpot_index

    def filter_index(self, test_index):
        if test_index == self.__vpot_index:
            return True
        else:
            return False

    def set_text(self, lower, upper):  # lower first in param list supports refactoring
        self.__lower_text = lower
        self.__upper_text = upper

    def clear_text(self):
        self.__upper_text = '      '
        self.__lower_text = '      '  # bottom line

    def set_lower_text(self, lower):
        self.__lower_text = lower

    def set_upper_text(self, upper):
        self.__upper_text = upper

    def get_upper_text(self):
        return self.__upper_text

    def get_lower_text(self):
        try:
            ascii_encoded = self.__lower_text.encode('ascii','ignore')
        except AttributeError:  # DeviceParameter
            ascii_encoded = unicode(self.__lower_text).encode('ascii',errors = 'ignore')

        return ascii_encoded.decode()
