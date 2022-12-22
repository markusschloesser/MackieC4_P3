
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

SPECIAL_NAME_DICT = {'InstrumentImpulse': (
                       (u'Pad1', u'Pad2'),
                       (u'Pad3', u'Pad4'),
                       (u'Pad5', u'Pad6'),
                       (u'Pad7', u'Pad8')),
   'Operator': (
              (u'OscA', u'OscB', u'OscC', u'OscD'),
              (u'LFO', u'Fltr'),
              (u'Pitch', ),
              (u'Glob.', )),
   'MultiSampler': (
                  (u'Vol.', u'Pitch'),
                  (u'Fltr', u'FEnv'),
                  (u'LFO1', u'LFO2', u'LFO3'),
                  (u'Osc', )),
   'UltraAnalog': (
                 (u'Osc', ), (u'Fltr', u'FEnv', u'FMod'), (u'VEnv', u'Mix'), (u'Out', )),
   'LoungeLizard': (
                  (u'Ma&Ti', ), (u'To&Da', ), (u'Pick', u'Mod'), (u'Glob.', )),
   'StringStudio': (
                  (u'Ex&St', u'Damp'),
                  (u'Te&Pi', u'Body'),
                  (u'Fltr', u'LFO'),
                  (u'Glob.', u'Vibr')),
   'Eq8': (
         (u'Bands', u'EQ1-3'), (u'Freq', u'Gain'), (u'Reso', u'Fltr'), (u'Glob.', ))}
SPECIAL_DEVICE_DICT = {'InstrumentImpulse': [
                       (
                        IMP_BANK1, IMP_BANK2),
                       (
                        IMP_BANK3, IMP_BANK4),
                       (
                        IMP_BANK5, IMP_BANK6),
                       (
                        IMP_BANK7, IMP_BANK8)],
   'Operator': [
              (
               OPR_BANK1, OPR_BANK2, OPR_BANK3, OPR_BANK4),
              (
               OPR_BANK5, OPR_BANK6),
              (
               OPR_BANK7,),
              (
               OPR_BANK8,)],
   'MultiSampler': [
                  (
                   SAM_BANK1, SAM_BANK8),
                  (
                   SAM_BANK2, SAM_BANK3),
                  (
                   SAM_BANK4, SAM_BANK5, SAM_BANK6),
                  (
                   SAM_BANK7,)],
   'UltraAnalog': [
                 (
                  ALG_BANK1,),
                 (
                  ALG_BANK2, ALG_BANK3, ALG_BANK4),
                 (
                  ALG_BANK5, ALG_BANK6),
                 (
                  ALG_BANK7,)],
   'LoungeLizard': [
                  (
                   ELC_BANK1,), (ELC_BANK2,), (ELC_BANK3, ELC_BANK4), (ELC_BANK5,)],
   'StringStudio': [
                  (
                   TNS_BANK1, TNS_BANK2),
                  (
                   TNS_BANK3, TNS_BANK4),
                  (
                   TNS_BANK6, TNS_BANK7),
                  (
                   TNS_BANK8, TNS_BANK5)],
   'Eq8': [
         (
          EQ8_BANK1, EQ8_BANK7),
         (
          EQ8_BANK2, EQ8_BANK3),
         (
          EQ8_BANK4, EQ8_BANK5),
         (
          EQ8_BANK6,)]}


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
            self._parameter_value_data_sources.append(DisplayDataSource())  # encoder LED rings get feedback mapped
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

    # def set_bank_buttons(self, buttons):
    #     assert buttons is None or isinstance(buttons, tuple) and len(buttons) == 2
    #     if buttons is not None:
    #         DeviceComponent.set_bank_nav_buttons(self, buttons[1], buttons[0])
    #     else:
    #         DeviceComponent.set_bank_nav_buttons(self, None, None)
    #     return

    def set_parameter_controls(self, encoder_controls):
        assert encoder_controls is None or (isinstance(encoder_controls, tuple) and len(encoder_controls) == NUM_ENCODERS)

        if encoder_controls is None and self._parameter_controls is not None:
            self.reset_encoder_ring_leds(encoder_controls)

        filled = [ p for p in encoder_controls if p ] if encoder_controls else None
        self._num_filled_banks = len(filled) / NUM_ENCODERS_ONE_ROW if filled else 0
        super(C4DeviceComponent, self).set_parameter_controls(encoder_controls)

        encoder_count = len(self._parameter_controls)
        max_full_banks = LIVE_DEFAULT_MAX_SIZE / encoder_count
        partial_bank = LIVE_DEFAULT_MAX_SIZE % encoder_count
        if (max_full_banks == 4 and partial_bank > 0) or encoder_count != NUM_ENCODERS:
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


    # def _update_encoder_row_page_indexes(self):
    #
    #     if self._bank_index >= NUM_ENCODER_ROWS:
    #         for range_index, bank_nbr in enumerate(range(self._bank_index, -1, -1)):  # range counting down
    #             # enumerate returns two values, (index_of_range_rtn_list, range_value_at_that_index), so
    #             # the first enumerated return value processed will be (0, self._bank_index),
    #             # then (1, self._bank_index - 1), etc
    #             if range_index < NUM_ENCODER_ROWS:
    #                 adjusted_index = range_index + (-1 - (2 * range_index))
    #                 # iterating row pages backward, adjusted_index = -1, -2, -3, -4 (only)
    #                 # 0 + (-1 - (0)) = 0 - 1 = -1
    #                 # 1 + (-1 - (2)) = 1 - 3 = -2
    #                 # 2 + (-1 - (4)) = 2 - 5 = -3
    #                 # 3 + (-1 - (6)) = 3 - 7 = -4
    #                 self._encoder_row_page_indexes[adjusted_index] = bank_nbr - range_index
    #                 # net effect is
    #                 # if a device has 48 mappable parameters in 6 banks that all get mapped,
    #                 # this self._page_index list should contain [0, 1, 2, 3] to start, then [1, 2, 3, 4], then
    #                 # [2, 3, 4, 5] after a user hits "parameter page next" twice, then a third hit would
    #                 # result in "no action" and not [3, 4, 5, x]
    #             else:
    #                 pass

    # def _assign_parameters(self):
    #     assert self.is_enabled()
    #     assert self._device is not None
    #     assert self._parameter_controls is not None
    #     if self._device.class_name in SPECIAL_DEVICE_DICT.keys():
    #         self.__assign_parameters_special()
    #     else:
    #         if self._device.class_name in DEVICE_DICT.keys():
    #             self.__assign_parameters_normal()
    #         else:
    #             self.__assign_parameters_plugin()
    #
    #     self.update_device_displays()
    #     return
    #
    # def __assign_parameters_special(self):
    #     """
    #         Assign the controls to the parameters of a device in SPECIAL_DEVICE_DICT
    #     """
    #     # (with more than 4 pages, but don't really understand what pages were before.  I think each AxiomPro encoder
    #     # bank has 8 encoders, so 4 bank pages of parameters would be 32.
    #     # The SPECIAL_DEVICE_DICT is defined here top of this file)
    #     banks = SPECIAL_DEVICE_DICT[self._device.class_name]
    #     bank_names = SPECIAL_NAME_DICT[self._device.class_name]
    #     pages = banks[self._bank_index]
    #     self._encoder_row_page_indexes[self._bank_index] %= len(pages)
    #     self._bank_name = bank_names[self._bank_index][self._encoder_row_page_indexes[self._bank_index]]
    #     page = pages[self._encoder_row_page_indexes[self._bank_index]]
    #     # assert len(page) >= len(self._parameter_controls)
    #     for index in range(len(self._parameter_controls)):
    #         if index < len(page):
    #             parameter = get_parameter_by_name(self._device, page[index])
    #             if parameter is not None:
    #                 self._parameter_controls[index].connect_to(parameter)
    #                 # parameter.callback = self._on_parameter_value_changed
    #             else:
    #                 self._log_message(
    #                     "releasing encoder <{}> because device param in page<{}> bank<{}> is None".
    #                     format(index, self._encoder_row_page_indexes[self._bank_index], self._bank_index))
    #                 self._parameter_controls[index].release_parameter()
    #                 # parameter.callback = None
    #         else:
    #             # self._log_message(
    #             #     "releasing encoder <{}> because more encoders than params in page<{}> bank<{}>".
    #             #     format(index, self._page_index[self._bank_index], self._bank_index))
    #             self._parameter_controls[index].release_parameter()
    #             # parameter.callback = None
    #
    #     for index in range(len(self._page_name_data_sources)):
    #         if index < len(bank_names):
    #             page_names = bank_names[index]
    #             if self._bank_index == index:
    #                 self._page_name_data_sources[index].set_display_string(page_names[((self._encoder_row_page_indexes[index] + 1) % len(page_names))])
    #             else:
    #                 self._page_name_data_sources[index].set_display_string(page_names[(self._encoder_row_page_indexes[index] % len(page_names))])
    #         else:
    #             self._page_name_data_sources[index].set_display_string(' - ')
    #
    #     return
    #
    # def __assign_parameters_normal(self):
    #     """
    #         Assign the controls to the parameters of a device in DEVICE_BOB_DICT  (generic devices)
    #     """
    #     # (with less than 4 pages, but don't really understand what pages were before.  I think each AxiomPro encoder
    #     # bank has 8 encoders, so 4 pages of parameters would be 32)
    #
    #     assert self._device.class_name in DEVICE_BOB_DICT.keys()
    #     self._log_message("page index len is <{}> and _bank_index is <{}>".format(len(self._encoder_row_page_indexes),
    #                                                                               self._bank_index))
    #     self._encoder_row_page_indexes[self._bank_index] = 0
    #     banks = DEVICE_DICT[self._device.class_name]
    #     bank_names = []
    #     if len(banks) > self._bank_index:
    #         if self._device.class_name in BANK_NAME_DICT.keys() and len(BANK_NAME_DICT[self._device.class_name]) > 1:
    #             bank_names = BANK_NAME_DICT[self._device.class_name]
    #         bank_params = banks[self._bank_index]
    #         if self._bank_index in range(len(bank_names)):
    #             self._bank_name = bank_names[self._bank_index]
    #         else:
    #             self._bank_name = "Bank {}".format(self._bank_index + 1)
    #         # self._log_message("ParamsInBank<{}> >= encoder controls<{}>".format(len(bank_params),
    #         #                                                                     len(self._parameter_controls)))
    #         # assert len(bank_params) >= len(self._parameter_controls)
    #         for index in range(len(self._parameter_controls)):
    #             if index < len(bank_params):
    #                 parameter = get_parameter_by_name(self._device, bank_params[index])
    #                 if parameter is not None:
    #                     self._parameter_controls[index].connect_to(parameter)
    #                     # parameter.callback = self._on_parameter_value_changed
    #                 else:
    #                     self._log_message(
    #                         "releasing encoder <{}> because device param in bank<{}> is None".format(index,
    #                                                                                                  self._bank_index))
    #                     self._parameter_controls[index].release_parameter()
    #                     # parameter.callback = None
    #             else:
    #                 # self._log_message(
    #                 #     "releasing encoder <{}> because more encoders than params in bank<{}>".format(index,
    #                 #                                                                                   self._bank_index))
    #                 self._parameter_controls[index].release_parameter()
    #
    #     for index in range(len(self._page_name_data_sources)):
    #         if index < len(bank_names):
    #             self._page_name_data_sources[index].set_display_string(bank_names[index])
    #         else:
    #             self._page_name_data_sources[index].set_display_string(' - ')
    #
    #     return
    #
    # def __assign_parameters_plugin(self):
    #     """
    #         Assign the controls to the parameters of any other plugin not in DEVICE_BOB_DICT or SPECIAL_DEVICE_DICT
    #     """
    #     num_controls = len(self._parameter_controls)
    #     num_banks = min(8, number_of_parameter_banks(self._device))
    #     num_double_pages = 0
    #     num_double_pages_before = 0
    #     parameters_to_use = self._device.parameters[1:]
    #     self._bank_name = "Bank {}".format(self._bank_index + 1)
    #     if num_banks > 4:
    #         num_double_pages = num_banks - 4
    #     if self._bank_index < num_double_pages:
    #         self._encoder_row_page_indexes[self._bank_index] %= 2
    #         num_double_pages_before = self._bank_index
    #     else:
    #         self._encoder_row_page_indexes[self._bank_index] = 0
    #         num_double_pages_before = num_double_pages
    #     if self._bank_index + num_double_pages_before < num_banks:
    #         bank_offset = (self._bank_index + num_double_pages_before) * num_controls
    #         page_offset = bank_offset + self._encoder_row_page_indexes[self._bank_index] * num_controls
    #         for index in range(len(self._parameter_controls)):
    #             if index < len(parameters_to_use):
    #                 if page_offset < len(parameters_to_use):
    #                     # parameter = get_parameter_by_name(self._device, parameters_to_use[page_offset])
    #                     parameter = parameters_to_use[page_offset]
    #                     if parameter is not None:
    #                         self._parameter_controls[index].connect_to(parameter)
    #                         # parameter.callback = self._on_parameter_value_changed
    #                     else:
    #                         self._log_message("releasing encoder <{}> because device param in bank<{}> is None".
    #                             format(index, self._bank_index))
    #                         self._parameter_controls[index].release_parameter()
    #                         # parameter.callback = None
    #                 else:
    #                     self._parameter_controls[index].release_parameter()
    #             else:
    #                 # more encoders than device parameters to map
    #                 self._parameter_controls[index].release_parameter()
    #
    #         # if page_offset < len(parameters_to_use):
    #         #     for control in self._parameter_controls:
    #         #         if page_offset < len(parameters_to_use):
    #         #             control.connect_to(parameters_to_use[page_offset])
    #         #             parameters_to_use[page_offset].callback = self._on_parameter_value_changed
    #         #         else:
    #         #             control.release_parameter()
    #         #             parameters_to_use[page_offset].callback = None
    #         #         page_offset += 1
    #         # else:
    #
    #
    #         bank_names = []
    #         parameter_offset = 0
    #         for index in range(4):
    #             display_string = ' - '
    #             if index < num_banks:
    #                 r_offset = "{}".format(parameter_offset + 1)
    #                 l_offset = "{}".format(parameter_offset + num_controls)
    #                 if index < num_double_pages:
    #                     add_offset_before = (self._bank_index == index and self._encoder_row_page_indexes[index] == 0 or
    #                                          self._bank_index != index and self._encoder_row_page_indexes[index] != 0)
    #                     if add_offset_before:
    #                         parameter_offset += num_controls
    #                         r_offset = "{}".format(parameter_offset + 1)
    #                         l_offset = "{}".format(parameter_offset + num_controls)
    #                     display_string = r_offset.rjust(2) + '-' + l_offset.rjust(2)
    #                     if not add_offset_before:
    #                         parameter_offset += num_controls
    #                 else:
    #                     display_string = r_offset.rjust(2) + '-' + l_offset.rjust(2)
    #             self._page_name_data_sources[index].set_display_string(display_string)
    #             parameter_offset += num_controls
