from __future__ import absolute_import, print_function, unicode_literals
import logging
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent
from _Framework.InputControlElement import InputControlElement
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent

# from .C4ControlSurfaceComponent import C4ControlSurfaceComponent
from .C4EncoderElement import C4EncoderElement
from .C4Encoders import C4Encoders
from .C4ChannelStripComponent import C4ChannelStripComponent
from .C4ModelElements import C4ModelElements
from .C4ModeSelector import C4ModeSelector
from .C4DeviceComponent import C4DeviceComponent
from .C4MixerComponent import C4MixerComponent
from .V2C4Component import V2C4Component
# from .C4EncodersComponent import C4EncodersComponent
from .C4_DEFINES import *

if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object

logger = logging.getLogger(__name__)


class V2C4(ControlSurface):
    """V2C4 class acts as a container/manager for all the
       C4 subcomponents like Encoders, Displays and so on.
       V2C4 is glued to Live's MidiRemoteScript C instance"""
    __module__ = __name__

    def __init__(self, c_instance, *a, **k):
        ControlSurface.__init__(self, c_instance, *a, **k)
        with self.component_guard():
            self._model = C4ModelElements()
            self._model.set_script_handle(self)

            self._suggested_input_port = 'MackieC4'
            self._suggested_output_port = 'MackieC4'
            self._waiting_for_first_response = True

            mixer = C4MixerComponent()
            mixer.set_select_buttons(
                self._model.make_button(C4SID_TRACK_RIGHT), self._model.make_button(C4SID_TRACK_LEFT))
            mixer.set_bank_buttons(
                self._model.make_button(C4SID_BANK_RIGHT),  self._model.make_button(C4SID_BANK_LEFT))

            # strip = C4ChannelStripComponent()
            # strip.set_script_handle(self)
            # strip.set_mixer(mixer)

            # encoder_32_index = V2C4Component.convert_encoder_id_value(C4SID_VPOT_CC_ADDRESS_32)
            volume_encoder = self._model.make_encoder(C4SID_VPOT_CC_ADDRESS_32, *a, **k)
            volume_encoder.c4_encoder.set_led_ring_display_mode(VPOT_DISPLAY_SINGLE_DOT)
            mixer.set_selected_strip_volume_control(volume_encoder)

            pan_encoder = self._model.make_encoder(C4SID_VPOT_CC_ADDRESS_31, *a, **k)
            pan_encoder.c4_encoder.set_led_ring_display_mode(VPOT_DISPLAY_BOOST_CUT)
            mixer.set_selected_strip_pan_control(pan_encoder)
            channel_encoders = tuple([volume_encoder, pan_encoder])

            mixer.set_selected_strip_mute_button(self._model.make_button(C4SID_VPOT_PUSH_30, *a, **k))
            mixer.set_selected_strip_solo_button(self._model.make_button(C4SID_VPOT_PUSH_29, *a, **k))
            mixer.set_selected_strip_arm_button(self._model.make_button(C4SID_VPOT_PUSH_28, *a, **k))
            mixer.set_shift_button(self._model.make_button(C4SID_SHIFT, *a, **k))

            device = C4DeviceComponent(device_selection_follows_track_selection=True)
            device.set_script_handle(self)
            self.set_device_component(device)

            stop_button = self._model.make_button(C4SID_VPOT_PUSH_25, *a, **k)
            play_button = self._model.make_button(C4SID_VPOT_PUSH_26, *a, **k)
            record_button = self._model.make_button(C4SID_VPOT_PUSH_27, *a, **k)
            transport_buttons = tuple([stop_button, play_button, record_button])

            session = SessionComponent(0, 0)

            self._device_parameter_displays = {
                LCD_ANGLED_ADDRESS:
                    {LCD_TOP_ROW_OFFSET: self._model.make_physical_display(*a, **k),
                     LCD_BOTTOM_ROW_OFFSET: self._model.make_physical_display(*a, **k)},
                LCD_TOP_FLAT_ADDRESS:
                    {LCD_TOP_ROW_OFFSET: self._model.make_physical_display(*a, **k),
                     LCD_BOTTOM_ROW_OFFSET: self._model.make_physical_display(*a, **k)},
                LCD_MDL_FLAT_ADDRESS:
                    {LCD_TOP_ROW_OFFSET: self._model.make_physical_display(*a, **k),
                     LCD_BOTTOM_ROW_OFFSET: self._model.make_physical_display(*a, **k)},
                LCD_BTM_FLAT_ADDRESS:
                    {LCD_TOP_ROW_OFFSET: self._model.make_physical_display(*a, **k),
                     LCD_BOTTOM_ROW_OFFSET: self._model.make_physical_display(*a, **k)}}

            self.clear_display_msg = self._model.lcd_display_clear_message
            self.hello_display_msg = self._model.lcd_display_hello_message
            self.goodbye_display_msg = self._model.lcd_display_goodbye_message
            foot_part = (SYSEX_FOOTER, )
            for i in LCD_DISPLAY_ADDRESSES:
                for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                    head_part = tuple(SYSEX_HEADER + (i, j))
                    self._device_parameter_displays[i][j].set_message_parts(head_part, foot_part)
                    self._device_parameter_displays[i][j].set_clear_all_message(
                        head_part + self.clear_display_msg + foot_part)

                    for m in range(NUM_ENCODERS_ONE_ROW):  # ENCODER_BANK_SIZE
                        self._device_parameter_displays[i][j].segment(m).set_position_identifier((m,))  # necessary???

            self._chan_strip_display = {
                LCD_ANGLED_ADDRESS:
                    {LCD_TOP_ROW_OFFSET: self._model.make_physical_display(nbr_segments=2, *a, **k),
                     LCD_BOTTOM_ROW_OFFSET: self._model.make_physical_display(nbr_segments=2, *a, **k)}}

            i = LCD_ANGLED_ADDRESS
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                head_part = tuple(SYSEX_HEADER + (i, j))
                self._chan_strip_display[i][j].set_clear_all_message(
                    head_part + self.clear_display_msg + foot_part)
                self._chan_strip_display[i][j].set_message_parts(head_part, foot_part)
                # .set_position_identifier here too?

            mixer.set_displays(self._chan_strip_display,
                               self._device_component.device_name_data_source())

            assert len(encoder_cc_ids) == NUM_ENCODERS
            device_encoders = []
            for cc_id in encoder_cc_ids:
                device_encoders.append(self._model.make_encoder(cc_id))
            device_encoders = tuple(device_encoders)

            assignment_buttons = [self._model.make_button(C4SID_MARKER)]  # ,
                                  # self._model.make_button(C4SID_CHANNEL_STRIP),
                                  # self._model.make_button(C4SID_TRACK),
                                  # self._model.make_button(C4SID_FUNCTION)]
            assignment_buttons = tuple(assignment_buttons)
            modifier_buttons = [None]  # [self._model.make_button(C4SID_SHIFT)]  # ,
                                # self._model.make_button(C4SID_CONTROL),
                                # self._model.make_button(C4SID_OPTION),
                                # self._model.make_button(C4SID_ALT)]
            modifier_buttons = tuple(modifier_buttons)

            device_bank_buttons = tuple([self._model.make_button(C4SID_SINGLE_RIGHT),
                                         self._model.make_button(C4SID_SINGLE_LEFT)])

            mode_selector = C4ModeSelector(mixer, device, session, channel_encoders, device_encoders,
                                           assignment_buttons, modifier_buttons, device_bank_buttons,
                                           transport_buttons, *a, **k)
            mode_selector.set_script_handle(self)
            for component in self.components:
                component.set_enabled(False)

            # these settings will get "locked in" when the "firmware handshake" update runs
            # after a successful handshake
            mode_selector.set_mode_toggle(assignment_buttons[0])
            # mode_selector.set_peek_button(self._model.make_button(C4SID_SPLIT_ERASE))
            mode_selector.set_displays(self._device_parameter_displays, self._chan_strip_display)

            # firmware version SYSEX message from C4 unlocks components locked above
            self.request_firmware_version()
            self.show_message("Mackie C4 v2 script initialize finished")
            self.log_message("Mackie C4 v2 script initialize finished")

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self._waiting_for_first_response = True
        self.request_firmware_version()
        # always blank the LCDs when refreshing state?
        # what about the LED rings?
        foot_part = (SYSEX_FOOTER, )
        for i in LCD_DISPLAY_ADDRESSES:
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                head_part = tuple(SYSEX_HEADER + (i, j))
                self.schedule_message(3, self._send_midi, head_part + self.clear_display_msg + foot_part)

    def build_midi_map(self, midi_map_handle):

        # for encoder in self._encoders_component.encoder_components():
        #     encoder.build_midi_map(midi_map_handle)

        # uncomment to see "unknown midi messages" from the C4 in the logs
        # of if you want to directly implement handlers for those midi messages
        # for i in range(C4SID_FIRST, C4SID_LAST + 1):
        #     Live.MidiMap.forward_midi_note(self._c_instance.handle(), midi_map_handle, 0, i)
        #     Live.MidiMap.forward_midi_cc(self._c_instance.handle(), midi_map_handle, 0, i)

        super(V2C4, self).build_midi_map(midi_map_handle)

    # def _install_mapping(self, midi_map_handle, control, parameter, feedback_delay, feedback_map):
    #     assert self._in_build_midi_map
    #     assert control is not None and parameter is not None
    #     self.log_message("control and parameter are not None")
    #     self.log_message("<{}> {}".format(control.__str__(), parameter.__str__()))
    #     assert isinstance(parameter, Live.DeviceParameter.DeviceParameter)
    #     assert isinstance(control, InputControlElement)
    #     self.log_message("control and parameter are instances")
    #     assert isinstance(feedback_delay, int)
    #     assert isinstance(feedback_map, tuple)
    #     self.log_message("feedback delay<{}> and map<{}> are instances".format(feedback_delay, feedback_map))
    #     super(V2C4, self)._install_mapping(midi_map_handle, control, parameter, feedback_delay, feedback_map)

    def receive_midi(self, midi_bytes):
        """ only need to handle CC or Note message types here """
        # superclass will call back separately to handle any SYSEX messages

        # this call forces any "unknown midi messages" logging mentioned above
        ControlSurface.receive_midi(self, midi_bytes)

    #                            v   3   .   0   0       <--- C4 firmware version
    # (240, 0, 0, 102, 23, 20, 118, 51, 46, 48, 48, 247)
    #                          Z   T   1   0   4   7   3         <---- C4 serial number (ZT10473 on a sticker)
    # (240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 65, 51, 6, 0, 247)
    # (240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 121, 16, 6, 0, 247)
    def handle_sysex(self, midi_bytes):
        if midi_bytes[0:5] == SYSEX_HEADER:
            # self.log_message("midi SYSEX message from C4 {}".format(midi_bytes))
            serial_nbr = midi_bytes[6:13]
            # self.log_message("connected to C4 serial number {}".format(serial_nbr))
            self._waiting_for_first_response = False
            self.log_message("C4 responded, enabling <{}> components".format(len(self.components)))
            i = 1
            for component in self.components:
                self.log_message("<{}> {}".format(i, component.__str__()))
                component.set_enabled(True)
                i = i + 1

            show_msg = "V2C4 remote script connected to C4 with "
            self.update()
            if len(midi_bytes) > 13:
                sysex_ints_as_ascii_text = [str(c) for c in serial_nbr[0:4]].__str__()
                self.show_message(show_msg + "serial number {}".format(sysex_ints_as_ascii_text))
            else:
                sysex_ints_as_ascii_text = [str(c) for c in serial_nbr].__str__()
                self.show_message(show_msg + "firmware version {}".format(sysex_ints_as_ascii_text))

    def request_firmware_version(self):
        sysex = SYSEX_HEADER + (SYSEX_MACKIE_CONTROL_FIRMWARE_REQUEST, 0, SYSEX_FOOTER)
        if self._waiting_for_first_response:
            self.log_message("requesting C4 firmware")
            self._send_midi(sysex)

            foot_part = (0, SYSEX_FOOTER)
            for i in LCD_DISPLAY_ADDRESSES:
                for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                    # this "id message" should clear any "firmware garbage" off the screens
                    # before the screens get "refreshed/cleared"
                    head_part = tuple(SYSEX_HEADER + (i, j))
                    sysex = head_part + self._model.lcd_display_id_message[i][j] + foot_part
                    # self.schedule_message(1, self._send_midi, sysex)
                    self._send_midi(sysex)

    def disconnect(self):
        foot_part = (SYSEX_FOOTER, )
        for i in LCD_DISPLAY_ADDRESSES:
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                head_part = tuple(SYSEX_HEADER + (i, j))
                # here, we could display a "goodbye message" instead of blanking the screens again
                sysex = head_part + self.goodbye_display_msg + foot_part
                # self.schedule_message(1, self._send_midi, sysex)
                self._send_midi(sysex)

        ControlSurface.disconnect(self)

    def log_message(self, *message):
        """ Overrides standard to use logger instead of c_instance. """
        try:
            message = '(%s) %s' % (self.__class__.__name__,
             (' ').join(map(str, message)))
            logger.info(message)
        except:
            logger.info('Logging encountered illegal character(s)!')

    @staticmethod
    def get_logger():
        """ Returns this script's logger object. """
        return logger
