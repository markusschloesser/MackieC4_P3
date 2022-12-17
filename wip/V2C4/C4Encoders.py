#
# from .V2C4Component import *
# from .C4EncoderMixin import LedMappingType, encoder_ring_led_mode_mode_select_values, encoder_ring_led_mode_cc_min_max_values
#
# import Live
#
# from _Generic.Devices import *
# from _Framework.InputControlElement import InputControlElement
#
#
# class C4Encoders:
#     """ Class representing behaviors associated with all encoders on the C4 device
#         sliced by the 4 encoder rows under each of the 4 LCD screens
#         and by each individual encoder
#      modeled after _Axiom/Encoders class
#      """
#     __module__ = __name__
#
#     def __init__(self, parent, extended, encoder_index, map_mode=None,
#                  display_mode=LedMappingType.LED_RING_MODE_SINGLE_DOT):
#         assert 0 <= encoder_index < NUM_ENCODERS
#         self.__parent = parent
#         self.__param_bank = 0
#         self.__param_bank_index = 0
#         # self.__selected_device = None
#         self.__extended = extended
#         self.__modifier = False
#         # self.__device_locked = False
#         self.__param_locked = False
#         self.__show_param_bank = False
#
#         self.__encoder_index = encoder_index
#         self.__midi_cc_channel = C4_MIDI_CHANNEL
#         self.__midi_cc_id = encoder_cc_ids[self.__encoder_index]
#         self.__feedback_cc_id = V2C4Component.convert_encoder_id_value(self.__midi_cc_id)
#         self._midi_feedback_delay = -1
#         self._map_mode = map_mode
#
#         self.__display_mode = display_mode
#         self._cc_value_map = ()
#         self.set_led_ring_display_mode(self.__display_mode)
#
#         if encoder_index in row_00_encoder_indexes:
#             self.__row_id = 0
#         elif encoder_index in row_01_encoder_indexes:
#             self.__row_id = 1
#         elif encoder_index in row_02_encoder_indexes:
#             self.__row_id = 2
#         else:
#             self.__row_id = 3
#
#     def disconnect(self):
#         self.__parent = None
#
#     def map_mode(self):
#         if self._map_mode is None:
#             return Live.MidiMap.MapMode.relative_signed_bit  # could be relative_smooth_signed_bit?
#         else:
#             return self._map_mode
#
#     @property
#     def c4_row_id(self):
#         return self.__row_id
#
#     @property
#     def c4_row_index(self):
#         return self.__encoder_index % NUM_ENCODERS_ONE_ROW
#
#     @property
#     def led_ring_cc_values(self):
#         return self._cc_value_map
#
#     @property
#     def led_ring_feedback_delay(self):
#         return self._midi_feedback_delay
#
#     @property
#     def encoder_index(self):
#         return self.__encoder_index
#
#     @property
#     def encoder_cc_id(self):
#         return self.__midi_cc_id
#
#     @property
#     def encoder_ring_feedback_cc_id(self):
#         return self.__feedback_cc_id
#
#     def set_led_ring_display_mode(self, display_mode):
#         """ no change unless display_mode is in C4EncoderMixin.encoder_ring_led_mode_mode_select_values.keys() """
#         if display_mode in encoder_ring_led_mode_mode_select_values.keys():
#             self.__display_mode = display_mode
#             display_mode_cc_base = encoder_ring_led_mode_cc_min_max_values[self.__display_mode][0]
#             feedback_val_range_len = encoder_ring_led_mode_cc_min_max_values[self.__display_mode][1]
#             feedback_val_range_len = feedback_val_range_len - display_mode_cc_base + 1
#             self._cc_value_map = tuple([display_mode_cc_base + x for x in range(feedback_val_range_len)])
#
#     def specialize_feedback_rule(self, feedback_rule=Live.MidiMap.CCFeedbackRule()):
#         feedback_rule.channel = self.__midi_cc_channel
#         feedback_rule.cc_no = self.__feedback_cc_id
#         feedback_rule.cc_value_map = self._cc_value_map
#         feedback_rule.delay_in_ms = self._midi_feedback_delay
#         return feedback_rule
#
#     def build_midi_map(self, midi_map_handle):
#         self.__parent.build_midi_map(midi_map_handle)
#
#     def build_midi_map_to_track_volume(self, midi_map_handle):
#         if self.__parent.is_enabled() and self.__parent.encoders_track is not None:
#             track = self.__parent.encoders_track
#             if self.__extended or self.__modifier:
#                 device_parameter = track.mixer_device.panning
#             else:
#                 device_parameter = track.mixer_device.volume
#
#             self.build_midi_map_to_device_param(midi_map_handle, device_parameter)
#
#     def build_midi_map_to_track_pan(self, midi_map_handle):
#         if self.__parent.is_enabled() and self.__parent.encoders_track is not None:
#             track = self.__parent.encoders_track
#             if self.__extended or self.__modifier:
#                 device_parameter = track.mixer_device.volume
#             else:
#                 device_parameter = track.mixer_device.panning
#
#             self.build_midi_map_to_device_param(midi_map_handle, device_parameter)
#
#     def build_midi_map_to_device_param(self, midi_map_handle, device_parameter):
#         if self.__parent.is_enabled():
#             feedback_rule = self.specialize_feedback_rule()
#             avoid_takeover = True
#             takeover_mode = not avoid_takeover
#             Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, device_parameter,
#                                                        self.__midi_cc_channel, self.__midi_cc_id, self._map_mode,
#                                                        feedback_rule, takeover_mode, sensitivity=1.0)
#         self.build_midi_map(midi_map_handle)
#
#     def set_modifier(self, mod_state):
#         if self.__parent.is_enabled():
#             self.__modifier = mod_state
#
#     def receive_midi_cc(self, cc_nbr, cc_val, chan):
#         # here we could process any CC directly from a caller (such as the top level script)?
#         # the C4 only sends on channel 0 ( ch 1 in Live)
#         pass
#
#     def send_led_ring_midi_cc(self, control_element, cc_val, force=False):
#         assert isinstance(control_element, InputControlElement)
#         assert cc_val in self._cc_value_map or cc_val == 0
#         control_element.send_value(cc_val, force=force, channel=self.__midi_cc_channel)
#
#     def send_led_ring_full_off(self, control_element, force=False):
#         self.send_led_ring_midi_cc(control_element, LED_OFF_DATA, force)
#
#     def send_led_ring_min_on(self, control_element, force=False):
#         min_on_value = 0
#         min_on_value = encoder_ring_led_mode_cc_min_max_values[self.__display_mode][min_on_value]
#         self.send_led_ring_midi_cc(control_element, min_on_value, force)
#
#     def send_led_ring_max_on(self, control_element, force=False):
#         max_on_value = 1
#         max_on_value = encoder_ring_led_mode_cc_min_max_values[self.__display_mode][max_on_value]
#         self.send_led_ring_midi_cc(control_element, max_on_value, force)
#
#     # builds an encoder midi map of "device_parameter" controls
#     # for up to all 32 encoders, in up to 4 "banks" (128 maximum device parameters)
#     # but only maps up to the number of parameters of "selected device" on Track
#     # def __connect_to_device(self, midi_map_handle):
#     #     if self.__parent.is_enabled():
#     #         assignment_necessary = True
#     #         avoid_takeover = True
#     #         takeover_mode = not avoid_takeover
#     #         if not self.__selected_device is None:
#     #             device_parameters = self.__selected_device.parameters[1:]  # element 0 is always device's mixer
#     #             device_bank = 0
#     #             param_bank = None
#     #             if self.__selected_device.class_name in DEVICE_DICT.keys():
#     #                 device_bank = DEVICE_DICT[self.__selected_device.class_name]
#     #                 if len(device_bank) > self.__param_bank:
#     #                     param_bank = device_bank[self.__param_bank]
#     #                 else:
#     #                     assignment_necessary = False
#     #             if assignment_necessary:
#     #                 if self.__show_param_bank:
#     #                     self.__show_param_bank = False
#     #                     if self.__selected_device.class_name in DEVICE_DICT.keys():
#     #                         if len(list(DEVICE_DICT[self.__selected_device.class_name])) > 1:
#     #                             if self.__selected_device.class_name in BANK_NAME_DICT.keys():
#     #                                 bank_names = BANK_NAME_DICT[self.__selected_device.class_name]
#     #                                 if bank_names and len(bank_names) > self.__param_bank:
#     #                                     bank_name = bank_names[self.__param_bank]
#     #                                     self.__show_bank_select(bank_name)
#     #                             else:
#     #                                 self.__show_bank_select('Best of Parameters')
#     #                         else:
#     #                             self.__show_bank_select("Bank {}".format(self.__param_bank + 1))
#     #                 free_encoders = 0
#     #                 for encoder_index in range(ENCODER_BASE, NUM_ENCODERS):
#     #                     feedback_rule = Live.MidiMap.CCFeedbackRule()
#     #                     parameter_index = encoder_index + self.__param_bank * NUM_ENCODERS
#     #                     if len(device_parameters) + free_encoders >= parameter_index:
#     #                         self.specialize_feedback_rule(feedback_rule)
#     #                         parameter = 0
#     #                         if param_bank is not None:
#     #                             if param_bank[encoder_index] != '':
#     #                                 parameter = get_parameter_by_name(self.__selected_device, param_bank[encoder_index])
#     #                             else:
#     #                                 free_encoders += 1
#     #                         else:
#     #                             if len(device_parameters) > parameter_index:
#     #                                 parameter = device_parameters[parameter_index]
#     #                         if parameter:
#     #                             Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter,
#     #                                                                        self.__cc_channel, self.__cc_nbr,
#     #                                                                        Live.MidiMap.MapMode.relative_signed_bit,
#     #                                                                        feedback_rule, takeover_mode, sensitivity=1.0)
#     #                         elif not param_bank:
#     #                             break
#     #                     else:
#     #                         break
#     #
#     #     return
#
#     # def lock_to_device(self, device):
#     #     if self.__parent.is_enabled():
#     #         if device:
#     #             self.__device_locked = True
#     #             self.__change_appointed_device(device)
#     #
#     # def unlock_from_device(self, device):
#     #     if self.__parent.is_enabled():
#     #         if device and device == self.__selected_device:
#     #             self.__device_locked = False
#     #             if not self.__parent.song().appointed_device == self.__selected_device:
#     #                 self.__parent.request_rebuild_midi_map()
#     #
#     # def set_appointed_device(self, device):
#     #     if self.__parent.is_enabled():
#     #         if not self.__device_locked:
#     #             self.__change_appointed_device(device)
#
#     # def set_bank(self, new_bank):
#     #     result = False
#     #     if self.__parent.is_enabled():
#     #         if self.__selected_device:
#     #             if number_of_parameter_banks(self.__selected_device) > new_bank:
#     #                 self.__show_param_bank = True
#     #                 if not self.__device_locked:
#     #                     self.__param_bank = new_bank
#     #                     result = True
#     #                 else:
#     #                     self.__selected_device.store_chosen_bank(self.__parent.instance_identifier(), new_bank)
#     #     return result
#     #
#     # def restore_bank(self, new_bank):
#     #     if self.__parent.is_enabled():
#     #         self.__param_bank = new_bank
#     #         self.__show_param_bank = True
#     #
#     # def reset_bank(self):
#     #     if self.__parent.is_enabled():
#     #         self.__param_bank = 0
#     #
#     # def __show_bank_select(self, bank_name):
#     #     if self.__parent.is_enabled():
#     #         if self.__selected_device:
#     #             self.__parent.show_message(str(self.__selected_device.name + ' Bank: ' + bank_name))
#     #
#     # def __change_appointed_device(self, device):
#     #     if self.__parent.is_enabled():
#     #         if not device == self.__selected_device:
#     #             if self.__selected_device is not None:
#     #                 self.__selected_device.remove_parameters_listener(self.__on_device_parameters_changed)
#     #             if device is not None:
#     #                 device.add_parameters_listener(self.__on_device_parameters_changed)
#     #             self.__param_bank = 0
#     #         self.__show_param_bank = False
#     #         self.__selected_device = device
#     #         self.__parent.request_rebuild_midi_map()
#     #         return
#     #
#     # def __on_device_parameters_changed(self):
#     #     if self.__parent.is_enabled():
#     #         self.__parent.request_rebuild_midi_map()
