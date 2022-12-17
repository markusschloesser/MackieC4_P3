from .V2C4Component import *

from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

from .C4DeviceComponent import C4DeviceComponent
from .C4MixerComponent import C4MixerComponent
from .C4EncoderMixin import LedMappingType


class C4ModeSelector(ModeSelectorComponent, V2C4Component):
    """class that selects between assignment modes using modifiers"""
    __module__ = __name__

    def __init__(self, mixer, device, session, channel_encoders, device_encoders,
                 assignment_buttons, modifier_buttons, bank_buttons, transport_buttons, *a, **k):
        assert isinstance(mixer, C4MixerComponent)
        assert isinstance(device, C4DeviceComponent)
        assert isinstance(session, SessionComponent)
        assert isinstance(channel_encoders, tuple)
        assert isinstance(device_encoders, tuple)
        assert isinstance(assignment_buttons, tuple)
        assert isinstance(modifier_buttons, tuple)
        assert isinstance(bank_buttons, tuple)
        assert isinstance(transport_buttons, tuple)
        ModeSelectorComponent.__init__(self)
        V2C4Component.__init__(self)
        self._mixer = mixer
        self._device = device
        self._transport = TransportComponent(*a, **k)
        self._transport_buttons = transport_buttons
        self._transport.set_stop_button(transport_buttons[0])
        self._transport.set_play_button(transport_buttons[1])
        self._transport.set_record_button(transport_buttons[2])
        self._session = session
        self._channel_encoders = channel_encoders
        self._device_encoders = device_encoders
        self._assignment_buttons = assignment_buttons
        self._modifier_buttons = modifier_buttons
        self._device_bank_buttons = bank_buttons
        self._peek_button = None
        self._default_displays = {LCD_ANGLED_ADDRESS: {0: None}}
        self._encoder_row00_displays = ()
        self._encoder_row01_displays = ()
        self._encoder_row02_displays = ()
        self._encoder_row03_displays = ()
        self._value_display = None
        self._device_dummy_source = DisplayDataSource()
        self._parameter_source = DisplayDataSource()
        self._device_dummy_source.set_display_string('Ch Str')
        self._clean_value_display_in = -1
        self._channel_strip_displays = ()
        self._must_update_encoder_display = False

        self._control_elements = []
        for c in self._device_encoders:
            self._control_elements.append(c)  # self._channel_encoders are also device encoders
        for c in self._device_bank_buttons:
            self._control_elements.append(c)
        for c in self._transport_buttons:
            self._control_elements.append(c)
        # self._register_timer_callback(self._on_timer)

        # identify_sender = True
        # for encoder in self._device_encoders:
        #     encoder.add_value_listener(self._parameter_value, identify_sender)

        # self.set_mode(0) # displays must be connected before we set the mode
        return

    def disconnect(self):
        # self._unregister_timer_callback(self._on_timer)
        for e in self._device_encoders:
            # e.remove_value_listener(self._parameter_value)
            e.send_led_ring_full_off()

        for c in self._control_elements:
            c.release_parameter()

        self._mixer = None
        self._device = None
        self._transport = None
        self._transport_buttons = None
        self._session = None
        self._channel_encoders = None
        self._device = None
        self._device_encoders = None
        self._assignment_buttons = None
        self._modifier_buttons = None
        self._device_bank_buttons = None
        self._default_displays = None
        self._channel_strip_displays = None
        self._encoder_row00_displays = None
        self._encoder_row01_displays = None
        self._encoder_row02_displays = None
        self._encoder_row03_displays = None
        self._value_display = None  # peek value display? (maybe use part of channel strip "static" name display)
        self._device_dummy_source = None
        self._parameter_source = None
        self._channel_strip_displays = None
        ModeSelectorComponent.disconnect(self)
        return

    def set_displays(self, device_displays, channel_strip_display, value_display=None):
        # if self.is_enabled():
        assert isinstance(device_displays, dict)
        assert len(device_displays.keys()) == len(LCD_DISPLAY_ADDRESSES)
        assert isinstance(channel_strip_display, dict)
        assert channel_strip_display.keys()[0] == LCD_ANGLED_ADDRESS
        assert isinstance(channel_strip_display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement)

        if self._default_displays[LCD_ANGLED_ADDRESS][0] is None and device_displays[LCD_ANGLED_ADDRESS][0] is not None:
            self._default_displays = device_displays

        one_lcd = device_displays[LCD_ANGLED_ADDRESS]
        self._encoder_row00_displays = tuple([one_lcd[LCD_TOP_ROW_OFFSET], one_lcd[LCD_BOTTOM_ROW_OFFSET]])
        one_lcd = device_displays[LCD_TOP_FLAT_ADDRESS]
        self._encoder_row01_displays = tuple([one_lcd[LCD_TOP_ROW_OFFSET], one_lcd[LCD_BOTTOM_ROW_OFFSET]])
        one_lcd = device_displays[LCD_MDL_FLAT_ADDRESS]
        self._encoder_row02_displays = tuple([one_lcd[LCD_TOP_ROW_OFFSET], one_lcd[LCD_BOTTOM_ROW_OFFSET]])
        one_lcd = device_displays[LCD_BTM_FLAT_ADDRESS]
        self._encoder_row03_displays = tuple([one_lcd[LCD_TOP_ROW_OFFSET], one_lcd[LCD_BOTTOM_ROW_OFFSET]])

        self.set_value_display(value_display)

        one_lcd = channel_strip_display[LCD_ANGLED_ADDRESS]
        self._channel_strip_displays = tuple([one_lcd[LCD_TOP_ROW_OFFSET], one_lcd[LCD_BOTTOM_ROW_OFFSET]])
        self.set_mode(0)
        return

    def update_displays(self):
        if self._mode_index == 0:
            self._channel_strip_displays[0].update()
            self._channel_strip_displays[1].update()
        elif self._mode_index == 1:
            self._encoder_row00_displays[0].update()
            self._encoder_row00_displays[1].update()
            self._encoder_row01_displays[0].update()
            self._encoder_row01_displays[1].update()
            self._encoder_row02_displays[0].update()
            self._encoder_row02_displays[1].update()
            self._encoder_row03_displays[0].update()
            self._encoder_row03_displays[1].update()
        else:
            self._log_message('Invalid mode index')
            assert False

    def set_value_display(self, value_display):
        if self.is_enabled():
            if value_display is not None and isinstance(value_display, PhysicalDisplayElement):
                self._value_display = value_display

            if self._value_display is not None:
                self._value_display.segment(1).set_data_source(self._parameter_source)
            self.update()

    # NOTE: PyCharm can't find a reference to an implementation of
    # add or remove _value_listener methods, and neither can "find in files" except in
    # _Framework.CompoundElement, but CompoundElement defers to a super class.
    # ButtonElement and CompoundElement are unrelated descendants of
    # the common super class ControlElement. Actual add or remove _value_listener
    # methods don't seem to be present in the _Framework (or v2), but lots of scripts
    # call them like this, not just "Axiom scripts"
    def set_peek_button(self, button):
        assert button is None or isinstance(button, ButtonElement)
        if self._peek_button is not button:
            if self._peek_button is not None:
                self._peek_button.remove_value_listener(self._peek_value)
            self._peek_button = button
            if self._peek_button is not None:
                self._peek_button.add_value_listener(self._peek_value)
            self.update()
        return

    def number_of_modes(self):
        # self._assignment_buttons + self._assignment_buttons * self._modifier_buttons = up to 20 eventually?
        # need to build a 4 x 4 "Select ModeSelector" modeled on Axiom
        return 2

    def update(self):
        super(C4ModeSelector, self).update()
        if self.is_enabled():
            # for c in self._control_elements:
            #     c.release_parameter()

            # the mixer track and bank select buttons stay set in both modes
            # but these "transport buttons" are also "device encoder buttons"
            self._transport.set_stop_button(self._transport_buttons[0])
            self._transport.set_play_button(self._transport_buttons[1])
            self._transport.set_record_button(self._transport_buttons[2])

            if self._mode_index == 0:
                self._device.set_parameter_controls(None)
                self._device.set_bank_buttons(None)
                for e in self._device_encoders:
                    e.send_led_ring_full_off()
                    # e.disconnect()

                # encoder_32_index = V2C4Component.convert_encoder_id_value(C4SID_VPOT_CC_ADDRESS_32)
                self._channel_encoders[0].update_led_ring_display_mode(LedMappingType.LED_RING_MODE_SINGLE_DOT)
                self._log_message("mode<0> setting selected strip volume")
                self._mixer.set_selected_strip_volume_control(self._channel_encoders[0])

                # encoder_31_index = V2C4Component.convert_encoder_id_value(C4SID_VPOT_CC_ADDRESS_31)
                self._channel_encoders[1].update_led_ring_display_mode(LedMappingType.LED_RING_MODE_BOOST_CUT)
                self._mixer.set_selected_strip_pan_control(self._channel_encoders[1])

                if self._channel_strip_displays is not None:
                    self._channel_strip_displays[0].segment(0).set_data_source(
                        self._mixer.selected_strip().static_data_sources[0])
                    self._channel_strip_displays[0].segment(1).set_data_source(
                        self._mixer.selected_strip().static_data_sources[1])
                    self._channel_strip_displays[1].segment(0).set_data_source(
                        self._mixer.selected_strip().track_name_data_source())
                    self._channel_strip_displays[1].segment(1).set_data_source(
                        self._device.device_name_data_source())

                if self._encoder_row00_displays is not None and \
                    len(self._encoder_row00_displays) == 2 and \
                    len(self._encoder_row01_displays) == 2 and \
                    len(self._encoder_row02_displays) == 2 and \
                    len(self._encoder_row03_displays) == 2:
                    self._encoder_row00_displays[0].reset()
                    self._encoder_row00_displays[1].reset()
                    self._encoder_row01_displays[0].reset()
                    self._encoder_row01_displays[1].reset()
                    self._encoder_row02_displays[0].reset()
                    self._encoder_row02_displays[1].reset()
                    self._encoder_row03_displays[0].reset()
                    self._encoder_row03_displays[1].reset()

            elif self._mode_index == 1:
                self._mixer.set_selected_strip_volume_control(None)
                self._mixer.set_selected_strip_pan_control(None)
                self._transport.set_stop_button(None)
                self._transport.set_play_button(None)
                self._transport.set_record_button(None)

                for e in self._channel_encoders:
                    e.send_led_ring_full_off()
                    # e.disconnect()

                self._device.set_parameter_controls(self._device_encoders)
                for e in self._device_encoders:
                    e.update_led_ring_display_mode(LedMappingType.LED_RING_MODE_WRAP)

                self._device.set_bank_buttons(self._device_bank_buttons)

                if self._channel_strip_displays is not None:
                    self._channel_strip_displays[0].reset()
                    self._channel_strip_displays[1].reset()

                if self._encoder_row00_displays is not None and \
                    len(self._encoder_row00_displays) == 2 and \
                    len(self._encoder_row01_displays) == 2 and \
                    len(self._encoder_row02_displays) == 2 and \
                    len(self._encoder_row03_displays) == 2:
                    for index in range(len(self._device_encoders)):
                        if index in row_00_encoder_indexes:
                            self._encoder_row00_displays[0].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_name_data_source(index))
                            self._encoder_row00_displays[1].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_value_data_source(index))
                        elif index in row_01_encoder_indexes:
                            self._encoder_row01_displays[0].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_name_data_source(index))
                            self._encoder_row01_displays[1].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_value_data_source(index))
                        elif index in row_02_encoder_indexes:
                            self._encoder_row02_displays[0].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_name_data_source(index))
                            self._encoder_row02_displays[1].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_value_data_source(index))
                        elif index in row_03_encoder_indexes:
                            self._encoder_row03_displays[0].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_name_data_source(index))
                            self._encoder_row03_displays[1].segment(index % NUM_ENCODERS_ONE_ROW).set_data_source(
                                self._device.parameter_value_data_source(index))

                # if self._page_displays is not None:
                #     for index in range(len(self._page_displays)):
                #         self._page_displays[index].segment(0).set_data_source(self._device.page_name_data_source(index))
                #         self._page_displays[index].update()

            else:
                self._log_message('Invalid mode index')
                assert False

            self.update_displays()
        return

    def _parameter_value(self, value, control):
        assert control in self._device_encoders
        self._log_message("mode selector <{}> parameter value listener popped value<{}>".format(control.name, value))
        if self.is_enabled():
            parameter = control.mapped_parameter()
            if parameter is not None:
                self._parameter_source.set_display_string("{}: {}".format(parameter.name, parameter.__str__()))
                self._log_message(
                    "parameter <{}> has value<{}> mapped".format(parameter.name, parameter.__str__()))
            else:
                self._parameter_source.set_display_string('<unmapped>')
                self._log_message("parameter <None> has value<None> mapped")
            self._clean_value_display_in = 20
        return

    def _on_timer(self):
        self.update_displays()
        if self._clean_value_display_in > 0:
            self._clean_value_display_in -= 1
            if self._clean_value_display_in == 0:
                self._parameter_source.set_display_string('')
                self._clean_value_display_in = -1
        if self._must_update_encoder_display:
            self.update_displays()
            self._must_update_encoder_display = False

    def _peek_value(self, value):
        assert self._peek_button is not None
        assert value in range(LIVE_DEFAULT_MAX_SIZE)
        new_peek_mode = value != 0
        peek_changed = False
        for encoder in self._device_encoders:
            if new_peek_mode != encoder.get_peek_mode():
                encoder.set_peek_mode(new_peek_mode)
                peek_changed = True

        if peek_changed and len(self._encoder_row00_displays) == 2:
            self._must_update_encoder_display = True
        return

    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)
