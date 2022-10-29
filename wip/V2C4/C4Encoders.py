
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Generic.Devices import *

from .C4_DEFINES import *

class C4Encoders:
    """ Class representing all encoders on the C4 device
        sliced by the 4 encoder rows under each of the 4 LCD screens
     modeled after _Axiom/Encoders class"""
    __module__ = __name__

    def __init__(self, parent, extended, encoder_index):
        self.__parent = parent
        self.__bank = 0
        self.__selected_device = None
        self.__extended = extended
        self.__modifier = False
        self.__device_locked = False
        self.__show_bank = False

        self.__encoder_index = encoder_index
        self.__cc_nbr = encoder_cc_ids[self.__encoder_index]
        if encoder_index in row_00_encoder_indexes:
            self.__row_id = 0
        elif encoder_index in row_01_encoder_indexes:
            self.__row_id = 1
        elif encoder_index in row_02_encoder_indexes:
            self.__row_id = 2
        else:
            self.__row_id = 3

        return

    def disconnect(self):
        if self.__selected_device != None:
            self.__selected_device.remove_parameters_listener(self.__on_device_parameters_changed)
            self.__selected_device = None
        return

    # builds an encoder midi map of "track volume" control
    #                              "track panning" control if self.__extended or self.__modifier
    # for up to all 32 encoders,
    # but only maps for number of visible tracks in song
    def build_midi_map(self, script_handle, midi_map_handle):
        tracks = self.__parent.song().visible_tracks
        feedback_rule = Live.MidiMap.CCFeedbackRule()
        encoder_cc_channel = 0
        for encoder in range(ENCODER_BASE, NUM_ENCODERS):
            track_index = encoder
            if len(tracks) > track_index:
                feedback_rule.channel = encoder_cc_channel
                feedback_rule.cc_no = encoder_cc_ids[encoder]
                feedback_rule.cc_value_map = tuple()
                feedback_rule.delay_in_ms = -1.0
                if self.__extended or self.__modifier:
                    device_parameter = tracks[track_index].mixer_device.panning
                else:
                    device_parameter = tracks[track_index].mixer_device.volume
                avoid_takeover = True
                Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle,
                                                           device_parameter, encoder_cc_channel, encoder_cc_ids[encoder],
                                                           Live.MidiMap.MapMode.relative_signed_bit, feedback_rule,
                                                           not avoid_takeover, sensitivity=1.0)
            else:
                break

        # this call wipes out the above mapping?
        self.__connect_to_device(midi_map_handle)

    def set_modifier(self, mod_state):
        self.__modifier = mod_state

    # builds an encoder midi map of "device_parameter" controls
    # for up to all 32 encoders, in up to 4 "banks" (128 maximum device parameters)
    # but only maps up to the number of parameters of "selected device" on Track
    def __connect_to_device(self, midi_map_handle):
        feedback_rule = Live.MidiMap.CCFeedbackRule()
        encoder_cc_channel = 0
        assignment_necessary = True
        avoid_takeover = True
        if not self.__selected_device is None:
            device_parameters = self.__selected_device.parameters[1:]
            device_bank = 0
            param_bank = None
            if self.__selected_device.class_name in DEVICE_DICT.keys():
                device_bank = DEVICE_DICT[self.__selected_device.class_name]
                if len(device_bank) > self.__bank:
                    param_bank = device_bank[self.__bank]
                else:
                    assignment_necessary = False
            if assignment_necessary:
                if self.__show_bank:
                    self.__show_bank = False
                    if self.__selected_device.class_name in DEVICE_DICT.keys():
                        if len(list(DEVICE_DICT[self.__selected_device.class_name])) > 1:
                            if self.__selected_device.class_name in BANK_NAME_DICT.keys():
                                bank_names = BANK_NAME_DICT[self.__selected_device.class_name]
                                if bank_names and len(bank_names) > self.__bank:
                                    bank_name = bank_names[self.__bank]
                                    self.__show_bank_select(bank_name)
                            else:
                                self.__show_bank_select('Best of Parameters')
                        else:
                            self.__show_bank_select('Bank' + str(self.__bank + 1))
                free_encoders = 0
                for encoder_index in range(ENCODER_BASE, NUM_ENCODERS):
                    parameter_index = encoder_index + self.__bank * NUM_ENCODERS
                    if len(device_parameters) + free_encoders >= parameter_index:
                        feedback_rule.channel = encoder_cc_channel
                        feedback_rule.cc_no = encoder_cc_ids[encoder_index]
                        feedback_rule.cc_value_map = tuple()
                        feedback_rule.delay_in_ms = -1.0
                        parameter = 0
                        if param_bank is not None:
                            if  [encoder_index] != '':
                                parameter = get_parameter_by_name(self.__selected_device, param_bank[encoder_index])
                            else:
                                free_encoders += 1
                        else:
                            if len(device_parameters) > parameter_index:
                                parameter = device_parameters[parameter_index]
                        if parameter:
                            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter, encoder_cc_channel,
                                                                       encoder_cc_ids[encoder_index],
                                                                       Live.MidiMap.MapMode.relative_signed_bit,
                                                                       feedback_rule, not avoid_takeover)
                        elif not param_bank:
                            break
                    else:
                        break

        return

    def receive_midi_cc(self, cc_no, cc_value, channel):
        # here we could process any CC directly from this encoder?
        pass

    def lock_to_device(self, device):
        if device:
            self.__device_locked = True
            self.__change_appointed_device(device)

    def unlock_from_device(self, device):
        if device and device == self.__selected_device:
            self.__device_locked = False
            if not self.__parent.song().appointed_device == self.__selected_device:
                self.__parent.request_rebuild_midi_map()

    def set_appointed_device(self, device):
        if not self.__device_locked:
            self.__change_appointed_device(device)

    def set_bank(self, new_bank):
        result = False
        if self.__selected_device:
            if number_of_parameter_banks(self.__selected_device) > new_bank:
                self.__show_bank = True
                if not self.__device_locked:
                    self.__bank = new_bank
                    result = True
                else:
                    self.__selected_device.store_chosen_bank(self.__parent.instance_identifier(), new_bank)
        return result

    def restore_bank(self, new_bank):
        self.__bank = new_bank
        self.__show_bank = True

    def reset_bank(self):
        self.__bank = 0

    def __show_bank_select(self, bank_name):
        if self.__selected_device:
            self.__parent.show_message(str(self.__selected_device.name + ' Bank: ' + bank_name))

    def __change_appointed_device(self, device):
        if not device == self.__selected_device:
            if self.__selected_device != None:
                self.__selected_device.remove_parameters_listener(self.__on_device_parameters_changed)
            if device != None:
                device.add_parameters_listener(self.__on_device_parameters_changed)
            self.__bank = 0
        self.__show_bank = False
        self.__selected_device = device
        self.__parent.request_rebuild_midi_map()
        return

    def __on_device_parameters_changed(self):
        self.__parent.request_rebuild_midi_map()
