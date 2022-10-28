

from __future__ import absolute_import, print_function, unicode_literals

from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent

from .C4Controller import C4Controller
from .C4MixerComponent import C4MixerComponent
from .C4Model import C4Model
from .C4_DEFINES import *

if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object

class V2C4(ControlSurface):
    """V2C4 class acts as a container/manager for all the
       C4 subcomponents like Encoders, Displays and so on.
       V2C4 is glued to Live's MidiRemoteScript C instance"""
    __module__ = __name__

    def __init__(self, c_instance, *a, **k):
        ControlSurface.__init__(self, c_instance, *a, **k)
        with self.component_guard():
            self.__model = C4Model(self, *a, **k)
            self.__controller = C4Controller(self, *a, **k)

            self._suggested_input_port = 'MackieC4'
            self._suggested_output_port = 'MackieC4'

            mixer = C4MixerComponent(1)
            mixer.set_select_buttons(self.__model.track_left_button, self.__model.track_right_button)
            mixer.set_bank_buttons(self.__model.bank_left_button, self.__model.bank_right_button)
            encoder_32_index = C4SID_VPOT_CC_ADDRESS_32 - C4SID_VPOT_CC_ADDRESS_BASE
            mixer.master_strip().set_volume_control(self.__model.encoders[encoder_32_index])
            #  encoder 31 for Track pan
            #  encoder 30 for Track rec arm
            encoder_29_index = C4SID_VPOT_PUSH_29 - C4SID_VPOT_PUSH_BASE
            encoder_28_index = C4SID_VPOT_PUSH_28 - C4SID_VPOT_PUSH_BASE
            mixer.set_mute_button(self.__model.encoder_buttons[encoder_29_index])
            mixer.set_solo_button(self.__model.encoder_buttons[encoder_28_index])
