
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

from .C4DeviceComponent import C4DeviceComponent
from .C4MixerComponent import C4MixerComponent

class C4ModeSelector(ModeSelectorComponent):
    """class that selects between assignment modes using modifiers"""
    __module__ = __name__

    def __init__(self, mixer, device, transport, session, encoders,
                 assignment_buttons, modifier_buttons, device_bank_buttons):
        assert isinstance(mixer, C4MixerComponent)
        assert isinstance(device, C4DeviceComponent)
        assert isinstance(transport, TransportComponent)
        assert isinstance(session, SessionComponent)
        assert isinstance(encoders, tuple)
        assert isinstance(assignment_buttons, tuple)
        assert isinstance(modifier_buttons, tuple)
        assert isinstance(device_bank_buttons, tuple)
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._device = device
        self._transport = transport
        self._session = session
        self._encoders = encoders
        self._assignment_buttons = assignment_buttons
        self._modifier_buttons = modifier_buttons
        self._device_bank_buttons = device_bank_buttons
        self._peek_button = None
        self._encoders_display = None
        self._value_display = None
        self._device_display = None
        self._page_displays = None
        self._device_dummy_source = DisplayDataSource()
        self._parameter_source = DisplayDataSource()
        self._device_dummy_source.set_display_string('Mixer')
        self._clean_value_display_in = -1
        self._must_update_encoder_display = False
        self._register_timer_callback(self._on_timer)
        identify_sender = True
        for encoder in self._encoders:
            encoder.add_value_listener(self._parameter_value, identify_sender)

        self.set_mode(0)
        return

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self._device = None
        self._encoders = None
        self._assignment_buttons = None
        self._modifier_buttons = None
        self._device_bank_buttons = None
        self._encoders_display = None
        self._value_display = None
        self._device_display = None
        self._page_displays = None
        self._device_dummy_source = None
        self._parameter_source = None
        ModeSelectorComponent.disconnect(self)
        return

    def set_displays(self, encoders_display, value_display, device_display, page_displays):
        assert isinstance(encoders_display, PhysicalDisplayElement)
        assert isinstance(value_display, PhysicalDisplayElement)
        assert isinstance(device_display, PhysicalDisplayElement)
        assert isinstance(page_displays, tuple)
        self._encoders_display = encoders_display
        self._value_display = value_display
        self._device_display = device_display
        self._page_displays = page_displays
        if self._value_display is not None:
            self._value_display.segment(0).set_data_source(self._parameter_source)
        self.update()
        return

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
        # self._assignment_buttons * self._modifier_buttons = 16 eventually?
        return 2

    def update(self):
        super(C4ModeSelector, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                self._device.set_parameter_controls(None)
                self._device.set_bank_buttons(None)
                # self._mixer_modes.set_controls(self._encoders)
                # self._mixer_modes.set_modes_buttons(self._page_buttons)
                # if self._device_display is not None:
                #     # self._device_display.segment(0).set_data_source(self._mixer.)
                #     # self._device_display.update()
                # if self._encoders_display is not None:
                #     for index in range(len(self._encoders)):
                #         self._encoders_display.segment(index).set_data_source(self._mixer_modes.parameter_data_source(index))
                #
                #     self._encoders_display.update()
                # if self._page_displays is not None:
                #     for index in range(len(self._page_displays)):
                #         self._page_displays[index].segment(0).set_data_source(self._mixer_modes.page_name_data_source(index))
                #         self._page_displays[index].update()

            elif self._mode_index == 1:
                # self._mixer_modes.set_controls(None)
                # self._mixer_modes.set_modes_buttons(None)
                self._device.set_parameter_controls(self._encoders)
                self._device.set_bank_buttons(self._device_bank_buttons)
                if self._device_display is not None:
                    self._device_display.segment(0).set_data_source(self._device.device_name_data_source())
                    self._device_display.update()
                if self._encoders_display is not None:
                    for index in range(len(self._encoders)):
                        self._encoders_display.segment(index).set_data_source(self._device.parameter_name_data_source(index))

                    self._encoders_display.update()
                if self._page_displays is not None:
                    for index in range(len(self._page_displays)):
                        self._page_displays[index].segment(0).set_data_source(self._device.page_name_data_source(index))
                        self._page_displays[index].update()

            else:
                print('Invalid mode index')
                assert False
        return

    def _parameter_value(self, value, control):
        assert control in self._encoders
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
            self._encoders_display.update()
            self._must_update_encoder_display = False

    def _peek_value(self, value):
        assert self._peek_button is not None
        assert value in range(LIVE_DEFAULT_MAX_SIZE)
        new_peek_mode = value != 0
        peek_changed = False
        for encoder in self._encoders:
            if new_peek_mode != encoder.get_peek_mode():
                encoder.set_peek_mode(new_peek_mode)
                peek_changed = True

        if peek_changed and self._encoders_display is not None:
            self._must_update_encoder_display = True
        return
