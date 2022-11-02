from __future__ import absolute_import, print_function, unicode_literals
import logging
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent

# from .C4ControlSurfaceComponent import C4ControlSurfaceComponent
from .C4EncoderElement import C4EncoderElement
from .C4Encoders import C4Encoders
from .C4ChannelStripComponent import C4ChannelStripComponent
from .C4ModelElements import C4ModelElements
from .C4ModeSelector import C4ModeSelector
from .C4DeviceComponent import C4DeviceComponent
from .C4EncodersComponent import C4EncodersComponent
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
            # self._controller = C4ControlSurfaceComponent()

            assert len(self._model.encoders) == NUM_ENCODERS
            assert len(self._model.encoder_buttons) == NUM_ENCODERS

            self._suggested_input_port = 'MackieC4'
            self._suggested_output_port = 'MackieC4'
            self._waiting_for_first_response = True

            self._encoders_component = C4EncodersComponent()
            self._encoders_component.set_script_handle(self)

            nbr_tracks = 1
            mixer = MixerComponent(nbr_tracks)
            mixer.set_select_buttons(self._model.track_right_button, self._model.track_left_button)
            mixer.set_bank_buttons(self._model.bank_right_button, self._model.bank_left_button)

            strip = C4ChannelStripComponent()
            strip.set_script_handle(self)
            strip.set_mixer(mixer)

            encoder_32_index = C4SID_VPOT_CC_ADDRESS_32 - C4SID_VPOT_CC_ADDRESS_BASE
            strip.set_volume_control(self._model.encoders[encoder_32_index])
            encoder_31_index = C4SID_VPOT_CC_ADDRESS_31 - C4SID_VPOT_CC_ADDRESS_BASE
            strip.set_pan_control(self._model.encoders[encoder_31_index])

            encoder_30_index = C4SID_VPOT_PUSH_30 - C4SID_VPOT_PUSH_BASE
            encoder_29_index = C4SID_VPOT_PUSH_29 - C4SID_VPOT_PUSH_BASE
            encoder_28_index = C4SID_VPOT_PUSH_28 - C4SID_VPOT_PUSH_BASE
            strip.set_mute_button(self._model.encoder_buttons[encoder_30_index])
            strip.set_solo_button(self._model.encoder_buttons[encoder_29_index])
            strip.set_arm_button(self._model.encoder_buttons[encoder_28_index])
            strip.set_shift_button(self._model.shift_button)

            device = C4DeviceComponent(device_selection_follows_track_selection=True)
            device.set_script_backdoor(self)
            self.set_device_component(device)

            transport = TransportComponent()
            encoder_27_index = C4SID_VPOT_PUSH_27 - C4SID_VPOT_PUSH_BASE
            encoder_26_index = C4SID_VPOT_PUSH_26 - C4SID_VPOT_PUSH_BASE
            encoder_25_index = C4SID_VPOT_PUSH_25 - C4SID_VPOT_PUSH_BASE

            transport.set_record_button(self._model.encoder_buttons[encoder_27_index])
            transport.set_play_button(self._model.encoder_buttons[encoder_26_index])
            transport.set_stop_button(self._model.encoder_buttons[encoder_25_index])

            session = SessionComponent(0, 0)

            self._lcd_displays = self._model.LCD_display
            self.blanks = self._model.LCD_display_clear_display_msg
            for i in LCD_DISPLAY_ADDRESSES:
                for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                    self._lcd_displays[i][j].set_clear_all_message(SYSEX_HEADER + (i, j) + self.blanks + (SYSEX_FOOTER, ))
                    self._lcd_displays[i][j].set_message_parts(SYSEX_HEADER + (i, j), (SYSEX_FOOTER, ))

                    # encoder_data_sources = []
                    for k in range(NUM_ENCODERS_ONE_ROW):  # ENCODER_BANK_SIZE
                        self._lcd_displays[i][j].segment(k).set_position_identifier((k,))  # necessary???
                    # these data sources will need to be dynamically updated depending on selected mode
                    #     if i == LCD_ANGLED_ADDRESS:
                    #         encoder_data_sources.append(self.__model.encoders[row_00_encoder_indexes[k]])
                    #     elif i == LCD_TOP_FLAT_ADDRESS:
                    #         encoder_data_sources.append(self.__model.encoders[row_01_encoder_indexes[k]])
                    #     elif i == LCD_MDL_FLAT_ADDRESS:
                    #         encoder_data_sources.append(self.__model.encoders[row_02_encoder_indexes[k]])
                    #     elif i == LCD_MDL_FLAT_ADDRESS:
                    #         encoder_data_sources.append(self.__model.encoders[row_03_encoder_indexes[k]])
                    #
                    # assert len(encoder_data_sources) > 0
                    # self._lcd_displays[i][j].set_data_sources(encoder_data_sources)

            self._chan_strip_display = self._model.channel_strip_display
            i = LCD_ANGLED_ADDRESS
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                self._chan_strip_display[i][j].set_clear_all_message(SYSEX_HEADER + (i, j) + self.blanks + (SYSEX_FOOTER,))
                self._chan_strip_display[i][j].set_message_parts(SYSEX_HEADER + (i, j), (SYSEX_FOOTER,))

            strip.set_display(self._chan_strip_display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET])

            midi_map_encoders = tuple(self._encoders_component.encoder_components())
            model_encoders = tuple(self._model.encoders)
            assignment_buttons = self._model.assignment_buttons
            modifier_buttons = self._model.modifier_buttons
            bank_buttons = tuple([self._model.bank_right_button, self._model.bank_left_button])

            mode_selector = C4ModeSelector(mixer, strip, device, transport, session, midi_map_encoders, model_encoders,
                                           assignment_buttons, modifier_buttons, bank_buttons)

            for component in self.components:
                component.set_enabled(False)

            # these settings will get "locked in" when the "firmware handshake" update runs
            # after a successful handshake
            mode_selector.set_mode_toggle(self._model.marker_button)
            mode_selector.set_peek_button(self._model.spot_erase_button)

            # clear all screens and show firmware on top angled LCD,
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
        for i in LCD_DISPLAY_ADDRESSES:
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                self.schedule_message(10, self._send_midi, (SYSEX_HEADER + (i, j) + self.blanks + (SYSEX_FOOTER, )))

    def build_midi_map(self, midi_map_handle):

        for encoder in self._encoders_component.encoder_components():
            encoder.build_midi_map(midi_map_handle)

        # uncomment to see "unknown midi messages" from the C4 in the logs
        # of if you want to directly implement handlers for those midi messages
        # for i in range(C4SID_FIRST, C4SID_LAST + 1):
        #     Live.MidiMap.forward_midi_note(self._c_instance.handle(), midi_map_handle, 0, i)
        #     Live.MidiMap.forward_midi_cc(self._c_instance.handle(), midi_map_handle, 0, i)

        super(V2C4, self).build_midi_map(midi_map_handle)

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
            self.log_message("enabling <{}> components".format(len(self.components)))
            for component in self.components:
                component.set_enabled(True)

            self.update()
            # TODO translate serial number to text versus ascii bytes
            if len(midi_bytes) > 13:
                self.show_message("connected to C4 with serial number {}".format(serial_nbr[0:4]))
            else:
                self.show_message("connected to C4 with firmware version {}".format(serial_nbr))

    def request_firmware_version(self):
        sysex = SYSEX_HEADER + (SYSEX_MACKIE_CONTROL_FIRMWARE_REQUEST, 0, SYSEX_FOOTER)
        if self._waiting_for_first_response:
            self.log_message("C4 firmware request sysex ({})".format(sysex))
            self._send_midi(sysex)

            for i in LCD_DISPLAY_ADDRESSES:
                for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                    # this "id message" should clear any "firmware garbage" off the screens before
                    # the screens get "refreshed/cleared"
                    sysex = SYSEX_HEADER + (self._model.LCD_display_id_message[i][j], 0, SYSEX_FOOTER)
                    self.schedule_message(2, self._send_midi, sysex)

    def disconnect(self):
        for component in self.components:
            component.disconnect()

        ControlSurface.disconnect(self)
        for i in LCD_DISPLAY_ADDRESSES:
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                self._send_midi((SYSEX_HEADER + (i, j) + self.blanks + (SYSEX_FOOTER, )))

    def log_message(self, *message):
        """ Overrides standard to use logger instead of c_instance. """
        try:
            message = '(%s) %s' % (self.__class__.__name__,
             (' ').join(map(str, message)))
            logger.info(message)
        except:
            logger.info('Logging encountered illegal character(s)!')

    # @staticmethod
    def get_logger(self):
        """ Returns this script's logger object. """
        return logger
