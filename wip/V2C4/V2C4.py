

from __future__ import absolute_import, print_function, unicode_literals

from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent

from .C4Controller import C4Controller
from .C4EncoderElement import C4EncoderElement
from .C4MixerComponent import C4MixerComponent
from .C4Model import C4Model
from .C4ModeSelector import C4ModeSelector
from .C4DeviceComponent import C4DeviceComponent
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
            mixer.set_select_buttons(self.__model.track_right_button, self.__model.track_left_button)
            mixer.set_bank_buttons(self.__model.bank_left_button, self.__model.bank_right_button)

            encoder_29_index = C4SID_VPOT_PUSH_29 - C4SID_VPOT_PUSH_BASE
            encoder_28_index = C4SID_VPOT_PUSH_28 - C4SID_VPOT_PUSH_BASE
            mixer.set_mute_button(self.__model.encoder_buttons[encoder_29_index])
            mixer.set_solo_button(self.__model.encoder_buttons[encoder_28_index])
            mixer.set_shift_button(self.__model.shift_button)

            device = C4DeviceComponent(device_selection_follows_track_selection=True)
            self.set_device_component(device)

            transport = TransportComponent()
            encoder_24_index = C4SID_VPOT_PUSH_24 - C4SID_VPOT_PUSH_BASE
            encoder_25_index = C4SID_VPOT_PUSH_25 - C4SID_VPOT_PUSH_BASE
            encoder_26_index = C4SID_VPOT_PUSH_26 - C4SID_VPOT_PUSH_BASE
            transport.set_stop_button(self.__model.encoder_buttons[encoder_24_index])
            transport.set_play_button(self.__model.encoder_buttons[encoder_25_index])
            transport.set_record_button(self.__model.encoder_buttons[encoder_26_index])
            session = SessionComponent(0, 0)

            encoders = tuple(self.__model.encoders)
            assignment_buttons = self.__model.assignment_buttons
            modifier_buttons = self.__model.modifier_buttons
            device_bank_buttons = tuple([self.__model.single_left_button, self.__model.single_left_button])

            mode_selector = C4ModeSelector(mixer, device, transport, session, encoders,
                                           assignment_buttons, modifier_buttons, device_bank_buttons)
            mode_selector.set_mode_toggle(self.__model.marker_button)
            mode_selector.set_peek_button(self.__model.spot_erase_button)