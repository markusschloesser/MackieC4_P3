from .V2C4Component import *

from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

from .C4DeviceComponent import C4DeviceComponent
from .C4ChannelStripComponent import C4ChannelStripComponent


class C4ModeSelector(ModeSelectorComponent, V2C4Component):
    """class that selects between assignment modes using modifiers"""
    __module__ = __name__

    def __init__(self, mixer, channel_strip, device, transport, session, encoders,
                 assignment_buttons, modifier_buttons, bank_buttons):
        assert isinstance(mixer, MixerComponent)
        assert isinstance(channel_strip, C4ChannelStripComponent)
        assert isinstance(device, C4DeviceComponent)
        assert isinstance(transport, TransportComponent)
        assert isinstance(session, SessionComponent)
        assert isinstance(encoders, tuple)
        assert isinstance(assignment_buttons, tuple)
        assert isinstance(modifier_buttons, tuple)
        assert isinstance(bank_buttons, tuple)
        ModeSelectorComponent.__init__(self)
        V2C4Component.__init__(self)
        self._mixer = mixer
        self._chan_strip = channel_strip
        self._device = device
        self._transport = transport
        self._session = session
        self._c4_model_encoders = encoders
        self._assignment_buttons = assignment_buttons
        self._modifier_buttons = modifier_buttons
        self._bank_buttons = bank_buttons
        self._peek_button = None
        self._default_displays = {LCD_ANGLED_ADDRESS: {0: None}}
        self._encoder_row00_displays = None
        self._encoder_row01_displays = None
        self._encoder_row02_displays = None
        self._encoder_row03_displays = None
        self._value_display = None
        self._device_dummy_source = DisplayDataSource()
        self._parameter_source = DisplayDataSource()
        self._device_dummy_source.set_display_string('Ch Str')
        self._clean_value_display_in = -1
        self._must_update_encoder_display = False
        self._register_timer_callback(self._on_timer)
        identify_sender = True
        for encoder in self._c4_model_encoders:
            encoder.add_value_listener(self._parameter_value, identify_sender)

        # self.set_mode(0) # displays must be connected before we set the mode
        return

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self._device = None
        self._c4_model_encoders = None
        self._assignment_buttons = None
        self._modifier_buttons = None
        self._bank_buttons = None
        self._default_displays = None
        self._encoder_row00_displays = ()
        self._encoder_row01_displays = ()
        self._encoder_row02_displays = ()
        self._encoder_row03_displays = ()
        self._value_display = None
        self._device_dummy_source = None
        self._parameter_source = None
        ModeSelectorComponent.disconnect(self)
        return

    def set_displays(self, displays, value_display=None):
        if self.is_enabled():
            assert isinstance(displays, dict)
            assert len(displays.keys()) == len(LCD_DISPLAY_ADDRESSES)
            if self._default_displays[LCD_ANGLED_ADDRESS][0] is None and displays[LCD_ANGLED_ADDRESS][0] is not None:
                self._default_displays = displays

            one_LCD = displays[LCD_ANGLED_ADDRESS]
            self._encoder_row00_displays = tuple([one_LCD[LCD_TOP_ROW_OFFSET], one_LCD[LCD_BOTTOM_ROW_OFFSET]])
            one_LCD = displays[LCD_TOP_FLAT_ADDRESS]
            self._encoder_row01_displays = tuple([one_LCD[LCD_TOP_ROW_OFFSET], one_LCD[LCD_BOTTOM_ROW_OFFSET]])
            one_LCD = displays[LCD_MDL_FLAT_ADDRESS]
            self._encoder_row02_displays = tuple([one_LCD[LCD_TOP_ROW_OFFSET], one_LCD[LCD_BOTTOM_ROW_OFFSET]])
            one_LCD = displays[LCD_BTM_FLAT_ADDRESS]
            self._encoder_row03_displays = tuple([one_LCD[LCD_TOP_ROW_OFFSET], one_LCD[LCD_BOTTOM_ROW_OFFSET]])

            self.set_value_display(value_display)

        return

    def update_displays(self):
        self._encoder_row00_displays[0].update()
        self._encoder_row00_displays[1].update()
        self._encoder_row01_displays[0].update()
        self._encoder_row01_displays[1].update()
        self._encoder_row02_displays[0].update()
        self._encoder_row02_displays[1].update()
        self._encoder_row03_displays[0].update()
        self._encoder_row03_displays[1].update()

    def set_value_display(self, value_display):
        if self.is_enabled():
            if value_display is not None and isinstance(value_display, PhysicalDisplayElement):
                self._value_display = value_display

            if self._value_display is not None:
                self._value_display.segment(0).set_data_source(self._parameter_source)
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
            if self._mode_index == 0:
                self._device.set_parameter_controls(None)
                self._device.set_bank_buttons(None)
                encoder_32_index = V2C4Component.convert_encoder_id_value(C4SID_VPOT_CC_ADDRESS_32)
                self._c4_model_encoders[encoder_32_index].c4_encoder.set_led_ring_display_mode(VPOT_DISPLAY_SINGLE_DOT)
                self._chan_strip.set_volume_control(self._c4_model_encoders[encoder_32_index])
                if self._encoder_row00_displays is not None:
                    self._chan_strip.set_display(self._encoder_row00_displays[0])

                encoder_31_index = V2C4Component.convert_encoder_id_value(C4SID_VPOT_CC_ADDRESS_31)
                self._c4_model_encoders[encoder_31_index].c4_encoder.set_led_ring_display_mode(VPOT_DISPLAY_BOOST_CUT)
                self._chan_strip.set_pan_control(self._c4_model_encoders[encoder_31_index])
                self._mixer.set_bank_buttons(self._bank_buttons[0], self._bank_buttons[1])

            elif self._mode_index == 1:
                self._chan_strip.set_volume_control(None)
                self._chan_strip.set_display(None)
                self._chan_strip.set_pan_control(None)
                self._mixer.set_bank_buttons(None, None)

                for e in self._c4_model_encoders:
                    e.c4_encoder.set_led_ring_display_mode(VPOT_DISPLAY_WRAP)

                self._device.set_parameter_controls(self._c4_model_encoders)
                self._device.set_bank_buttons(self._bank_buttons)
                # if self._device_display is not None:
                #     self._device_display.segment(0).set_data_source(self._device.device_name_data_source())
                #     self._device_display.update()
                if self._encoder_row00_displays is not None and \
                    len(self._encoder_row00_displays) == 2 and \
                    len(self._encoder_row01_displays) == 2 and \
                    len(self._encoder_row02_displays) == 2 and \
                    len(self._encoder_row03_displays) == 2:
                    for index in range(len(self._c4_model_encoders)):
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

                    self.update_displays()
                # if self._page_displays is not None:
                #     for index in range(len(self._page_displays)):
                #         self._page_displays[index].segment(0).set_data_source(self._device.page_name_data_source(index))
                #         self._page_displays[index].update()

            else:
                self._log_message('Invalid mode index')
                assert False
        return

    def _parameter_value(self, value, control):
        assert control in self._c4_model_encoders
        if self.is_enabled():
            parameter = control.mapped_parameter()
            if parameter is not None:
                self._parameter_source.set_display_string("{}: {}".format(parameter.name, parameter.__str__()))
            else:
                self._parameter_source.set_display_string('<unmapped>')
            self._clean_value_display_in = 20
        return

    def _on_timer(self):
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
        for encoder in self._c4_model_encoders:
            if new_peek_mode != encoder.get_peek_mode():
                encoder.set_peek_mode(new_peek_mode)
                peek_changed = True

        if peek_changed and len(self._encoder_row00_displays) == 2:
            self._must_update_encoder_display = True
        return

    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)
