
from .V2C4Component import *

from _Generic.Devices import *
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.SubjectSlot import subject_slot, subject_slot_group, Subject
from _Framework.Util import nop

from .C4EncoderElement import C4EncoderElement
from .Utils import live_object_is_valid


class C4DeviceComponent(DeviceComponent, V2C4Component):
    """
        Now modeled on _NKFW2 SpecialDeviceComponent
        was Modeled on Axiom Pro PageableDeviceComponent
    """

    __module__ = __name__

    def __init__(self, *a, **k):
        super(C4DeviceComponent, self).__init__(*a, **k)
        V2C4Component.__init__(self)
        self._parameter_name_data_sources = []
        self._parameter_value_data_sources = []
        self._page_name_data_sources = []
        # each "page index" element in this list keeps track of which "bank of 8 parameters" page
        # each row of encoders has loaded.
        # self._page_index[0] represents the top row of encoders
        # self._page_index[3] represents the bottom row of encoders
        # if a device has 48 mappable parameters in 6 banks that all get mapped,
        # this self._page_index list should contain [0, 1, 2, 3] to start, then [1, 2, 3, 4], then
        # [2, 3, 4, 5] after a user hits "parameter page up" twice
        # self._encoder_row_page_indexes = [0, 0, 0, 0]
        self._num_filled_banks = 0
        self._empty_control_slots = self.register_slot_manager()
        for i in range(NUM_ENCODERS):
            self._parameter_name_data_sources.append(DisplayDataSource())
            # encoder LED rings get feedback mapped, this is the same value data as display text
            self._parameter_value_data_sources.append(DisplayDataSource())
            # not currently used
            self._page_name_data_sources.append(DisplayDataSource())

        self.reset_device_displays()

        def make_property_slot(name, alias=None):
            alias = alias or name
            return self.register_slot(None, getattr(self, '_on_%s_changed' % alias), name)

        self._parameter_value_property_slot = make_property_slot('value', alias='parameter_value')
        self.__on_selected_device_parameter_value_changed.subject = self.song().view.selected_track.view

    @subject_slot('selected_device')
    def __on_selected_device_parameter_value_changed(self):
        self.update_device_displays()

    @subject_slot_group('value')
    def _on_parameter_value_changed(self):
        self.update_device_displays()

    def disconnect(self):
        self._parameter_value_data_sources = None
        self._parameter_name_data_sources = None
        self._page_name_data_sources = None
        DeviceComponent.disconnect(self)
        return

    def set_script_handle(self, main_script):
        self._set_script_handle(main_script)

    def set_device(self, device):
        DeviceComponent.set_device(self, device)
        self._parameter_value_property_slot.subject = self._on_parameter_value_changed()
        self.update_device_displays()

    def reset_encoder_ring_leds(self, controls=None):
        if controls is None and self._parameter_controls is not None:
            controls = self._parameter_controls
        if controls is not None:
            for control in controls:
                control.send_led_ring_full_off(force=True)

    def reset_device_displays(self):
        for source in self._parameter_name_data_sources:
            source.set_display_string(' - ')

        for source in self._parameter_value_data_sources:
            source.set_display_string(' * ')

        for source in self._page_name_data_sources:
            source.set_display_string(' - ')

    def update_device_displays(self):
        if self._device is not None:
            if self._parameter_controls is not None and len(self._parameter_controls) > 0:
                for index in range(len(self._parameter_controls)):
                    param = self._parameter_controls[index].mapped_parameter()
                    if param is not None:
                        # Live.Device.DeviceParameter.name
                        self._parameter_name_data_sources[index].set_display_string(param.name)
                        # Live.Device.DeviceParameter.str_for_value(Live.Device.DeviceParameter.value)
                        self._parameter_value_data_sources[index].set_display_string(param.str_for_value(param.value))
                    else:
                        self._parameter_name_data_sources[index].set_display_string(' - ')
                        self._parameter_value_data_sources[index].set_display_string(' * ')
            else:
                # device is here but device parameters are not yet mapped to encoder controls or displays
                self.reset_device_displays()
        else:
            self.reset_device_displays()

    def set_parameter_controls(self, encoder_controls):
        assert encoder_controls is None or (isinstance(encoder_controls, tuple) and len(encoder_controls) == NUM_ENCODERS)

        if encoder_controls is None and self._parameter_controls is not None:
            self.reset_encoder_ring_leds(encoder_controls)

        filled = [ p for p in encoder_controls if p ] if encoder_controls else None
        self._num_filled_banks = len(filled) / NUM_ENCODERS_ONE_ROW if filled else 0
        super(C4DeviceComponent, self).set_parameter_controls(encoder_controls)

        if self._parameter_controls is not None:
            encoder_count = len(self._parameter_controls)
            if encoder_count > 0:
                max_full_banks = LIVE_DEFAULT_MAX_SIZE / encoder_count
                partial_bank = LIVE_DEFAULT_MAX_SIZE % encoder_count
                # enforcing maximum 32 encoder controls and multiples of 8 here
                # mismatch check logic probably represents a tautology, likely both unnecessary?
                c4_encoder_mismatch = encoder_count <= NUM_ENCODERS and encoder_count % NUM_ENCODERS_ONE_ROW != 0
                api_encoder_mismatch = max_full_banks == 4 and partial_bank > 0
                if api_encoder_mismatch or c4_encoder_mismatch:
                    raise AssertionError("encoder control count mismatch")
        return

    def parameter_value_data_sources(self):
        return self._parameter_value_data_sources

    def parameter_value_data_source(self, index):
        assert index < len(self._parameter_value_data_sources)
        return self._parameter_value_data_sources[index]

    def parameter_name_data_sources(self):
        return self._parameter_name_data_sources

    def parameter_name_data_source(self, index):
        assert index < len(self._parameter_name_data_sources)
        return self._parameter_name_data_sources[index]

    def page_name_data_sources(self):
        return self._page_name_data_sources

    def page_name_data_source(self, index):
        assert index in len(self._page_name_data_sources)
        return self._page_name_data_sources[index]

    def update(self):
        if self._num_filled_banks == 0:
            return
        self._empty_control_slots.disconnect()
        super(C4DeviceComponent, self).update()
        self.update_device_displays()

    def _on_parameters_changed(self):
        self.update()

    def _can_bank_up(self):
        num_banks = self._number_of_parameter_banks()
        return self._bank_index is None or num_banks > self._bank_index + self._num_filled_banks

    def _can_bank_down(self):
        return self._bank_index is None or self._bank_index > 0

    def _bank_up_value(self, value):
        """ Overrides standard to properly deal with more than 8 parameter controls. """
        if self.is_enabled() and self._device and value and self._can_bank_up():
            self._increment_bank_index(1)

    def _bank_down_value(self, value):
        """ Overrides standard to properly deal with more than 8 parameter controls. """
        if self.is_enabled() and self._device and value and self._can_bank_down():
            self._increment_bank_index(-1)

    def _increment_bank_index(self, delta):
        delta = self._num_filled_banks * delta
        self._bank_name = ''
        self._bank_index = max(0, min(self._number_of_parameter_banks() - 1, self._bank_index + delta))
        self.update()

    def _assign_parameters(self):
        """ Overrides standard to add listeners for unused controls to prevent
        leaking. """
        assert self.is_enabled()
        assert self._device is not None
        assert self._parameter_controls is not None
        self._bank_name, bank = self._current_bank_details()
        for control, parameter in zip(self._parameter_controls, bank):
            if control is not None:
                if isinstance(control, C4EncoderElement):
                    control.send_led_ring_full_off(force=True)

                if live_object_is_valid(parameter):
                    control.connect_to(parameter)
                else:
                    control.release_parameter()
                    self._empty_control_slots.register_slot(control, nop, 'value')

        self._release_parameters(self._parameter_controls[len(bank):])
        return

    def _release_parameters(self, controls):
        """
            Extends standard to add listeners for unused controls to prevent leaking and
            turn off any connected LED rings
        """
        self.reset_encoder_ring_leds(controls)

        super(C4DeviceComponent, self)._release_parameters(controls)
        if controls:
            for control in controls:
                if control:
                    self._empty_control_slots.register_slot(control, nop, 'value')

    def _current_bank_details(self):
        """ Overrides standard to assign multiple banks of parameters where possible. """
        bank_name = self._bank_name
        bank = []
        best_of = self._best_of_parameter_bank()
        banks = self._parameter_banks()
        if banks:
            num_extra_control_banks = self._num_filled_banks - 1
            if self._bank_index is not None or not best_of:
                index = self._bank_index if self._bank_index is not None else 0
                bank = list(banks[index])
                bank_name = self._parameter_bank_names()[index]
                num_extra_param_banks = self._number_of_parameter_banks() - index - 1
                for i in xrange(num_extra_param_banks):
                    target_index = index + i + 1
                    if i < num_extra_control_banks:
                        bank.extend(banks[target_index])
                        bank_name += '   /   %s' % self._parameter_bank_names()[target_index]

            else:
                bank = best_of
                bank_name = 'Best of Parameters'
        return (
         bank_name, bank)


