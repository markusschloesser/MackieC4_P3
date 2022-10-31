

from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)

from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent

from .C4Controller import C4Controller
from .C4EncoderElement import C4EncoderElement
from .C4ChannelStripComponent import C4ChannelStripComponent
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
            self._model = C4Model(self, *a, **k)
            self._controller = C4Controller(self, *a, **k)

            assert len(self._model.encoders) == NUM_ENCODERS
            assert len(self._model.encoder_buttons) == NUM_ENCODERS

            self._suggested_input_port = 'MackieC4'
            self._suggested_output_port = 'MackieC4'
            self._waiting_for_first_response = True

            nbr_tracks = 1
            mixer = MixerComponent(nbr_tracks)
            mixer.set_select_buttons(self._model.track_right_button, self._model.track_left_button)
            mixer.set_bank_buttons(self._model.bank_right_button, self._model.bank_left_button)

            strip = C4ChannelStripComponent(mixer)

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
            self.set_device_component(device)

            transport = TransportComponent()
            encoder_24_index = C4SID_VPOT_PUSH_24 - C4SID_VPOT_PUSH_BASE
            encoder_25_index = C4SID_VPOT_PUSH_25 - C4SID_VPOT_PUSH_BASE
            encoder_26_index = C4SID_VPOT_PUSH_26 - C4SID_VPOT_PUSH_BASE
            transport.set_stop_button(self._model.encoder_buttons[encoder_24_index])
            transport.set_play_button(self._model.encoder_buttons[encoder_25_index])
            transport.set_record_button(self._model.encoder_buttons[encoder_26_index])
            session = SessionComponent(0, 0)

            encoders = tuple(self._model.encoders)
            assignment_buttons = self._model.assignment_buttons
            modifier_buttons = self._model.modifier_buttons
            device_bank_buttons = tuple([self._model.single_left_button, self._model.single_left_button])

            mode_selector = C4ModeSelector(mixer, strip, device, transport, session, encoders,
                                           assignment_buttons, modifier_buttons, device_bank_buttons)
            mode_selector.set_mode_toggle(self._model.marker_button)
            mode_selector.set_peek_button(self._model.spot_erase_button)

            self._lcd_displays = self._model.LCD_display
            self.blanks = tuple([ASCII_SPACE for x in range(LCD_BOTTOM_ROW_OFFSET)])
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

            # still need to connect the "data sources" associated with
            # each encoder to the physical displays, don't we?

            for component in self.components:
                component.set_enabled(False)

            # clear all screens and show firmware on top angled LCD,
            # firmware version SYSEX message from C4 unlocks components locked above
            # self.schedule_message(10, self.request_firmware_version)
            self.request_firmware_version()
            self.show_message("Mackie C4 v2 script initialized")
            self.log_message("Mackie C4 v2 script initialized")

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self._waiting_for_first_response = True
        for i in LCD_DISPLAY_ADDRESSES:
            for j in (LCD_TOP_ROW_OFFSET, LCD_BOTTOM_ROW_OFFSET):
                self.schedule_message(10, self._send_midi, (SYSEX_HEADER + (i, j) + self.blanks + (SYSEX_FOOTER, )))

    #                            v   3   .   0   0       <--- C4 firmware version
    # (240, 0, 0, 102, 23, 20, 118, 51, 46, 48, 48, 247)
    #                          Z   T   1   0   4   7   3         <---- C4 serial number (ZT10473 on a sticker)
    # (240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 65, 51, 6, 0, 247)
    # (240, 0, 0, 102, 23, 1, 90, 84, 49, 48, 52, 55, 51, 121, 16, 6, 0, 247)
    def handle_sysex(self, midi_bytes):
        if midi_bytes[0:5] == SYSEX_HEADER:
            self.log_message("midi SYSEX message from C4 {}".format(midi_bytes))
            serial_nbr = midi_bytes[6:13]
            self.log_message("connected to C4 serial number {}".format(serial_nbr))
            self._waiting_for_first_response = False
            self.log_message("enabling <{}> components".format(len(self.components)))
            for component in self.components:
                component.set_enabled(True)

            self.update()
            # translate serial number to text versus ascii bytes
            self.show_message("connected to C4 serial number {}".format(serial_nbr))


    def request_firmware_version(self):
        sysex = SYSEX_HEADER + (SYSEX_MACKIE_CONTROL_FIRMWARE_REQUEST, 0, SYSEX_FOOTER)
        self.log_message("requesting C4 firmware {}".format(sysex))
        if self._waiting_for_first_response:
            self._send_midi(sysex)

    def disconnect(self):
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
    # def get_logger():
    #     """ Returns this script's logger object. """
    #     return logger