
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

import logging

from . import script_utils
from .script_utils import EncoderDisplaySegment
from .EncoderControllerDataStore import ActiveTrackDetails
from .consts import *


def toggle_devices(active_track_details, cc_nbr, cc_val):
    log_id = "mode_utils_tcs.toggle_devices: "
    device_encoder_row_offset = row_01_encoders[0]
    bank_start = active_track_details.active_track.track_device_bank_view_index * SETUP_DB_DEVICE_BANK_SIZE
    rtn = ""
    for i in range(SETUP_DB_DEVICE_BANK_SIZE):
        device_index = bank_start + i
        encoder_cc_nbr = device_encoder_row_offset + i
        if device_index < active_track_details.device_count:
            dev_ref = active_track_details.devices[device_index]
            parameter = dev_ref.device_on_off_parameter # property value assigned will be None if not liveobj_valid(device_on_off_parameter)
            if liveobj_valid(parameter) and parameter.is_enabled:
                ccw_turn = cc_val > 64
                if ccw_turn and cc_nbr == encoder_cc_nbr:
                    parameter.value = False
                elif not ccw_turn and cc_nbr == encoder_cc_nbr:
                    parameter.value = True
            else:
                if not liveobj_valid(parameter):
                    if len(rtn) > 0:
                        rtn += f", and: device_ref {dev_ref.device_name}?"
                    else:
                        rtn += f"{log_id}assumption issue: device_ref {dev_ref.device_name} parameters[0] was not liveobj_valid?"
    return rtn

def handle_pressed_vpot(active_track_details:ActiveTrackDetails, pressed_encoder_button_id, handle_track_device_bank_view_update, handle_assignment_switch_ids,
                        locked_to_device, ds, song, update_chosen_plugin_device, log_message, subordinate_selected_track_allows_audio, encoders, xfade,
                        subordinate_track_is_selected, show_message):
    log_id = "mode_utils_tcs.handle_pressed_vpot: "
    selected_track = active_track_details.active_track.track
    # encoder button ids are offset from associated encoder ids by 32 (0x20), feedback goes to one LED ring at CC nbr == encoder button id
    encoder_index = pressed_encoder_button_id - C4SID_VPOT_PUSH_BASE
    is_armable_track_selected = script_utils.can_be_armed(selected_track)
    update_self = False
    if encoder_index in row_00_encoders:
        encoder_04_index = 3
        update_self = False

        # group track fold toggle, also groups from within
        if encoder_index == encoder_04_index:
            script_utils.toggle_fold(selected_track)  # <-- triggers track_changed() callback, maybe selected_track_changed() also
        else:
            update_self = handle_track_device_bank_view_update(encoder_index)

    elif encoder_index in row_01_encoders:
        # (row 2 "index" is 01) these encoders represent devices 1 - 8 in the device chain on the selected track in C4M_CHANNEL_STRIP mode
        # behavior implemented is: encoder button press == automatically switch to Track/Plugins mode
        # AND IF not already locked to a device
        # switch to Track/Plugins mode  and update "self.__chosen_plugin" to the device represented by the encoder clicked
        # ELSE
        # switch to Track/Plugins mode using "self.__chosen_plugin" the "device to which the script is locked"
        handle_assignment_switch_ids(C4SID_TRACK)

        device_bank_start_offset = NUM_ENCODERS_ONE_ROW * active_track_details.active_track.track_device_bank_view_index
        device_offset = encoder_index - NUM_ENCODERS_ONE_ROW + device_bank_start_offset
        if not locked_to_device:
            if device_offset < active_track_details.device_count:  # if the calculated offset is valid device index

                ds.last_selected_device_index = device_offset
                device_ref = active_track_details.devices[device_offset]
                if liveobj_valid(device_ref.device):
                    song.view.select_device(device_ref.device)  # <-- triggers on_device_changed() callback
                else:
                    update_chosen_plugin_device(device_ref.device)  # device == None
            else:
                msg = f"{log_id}can't update __chosen_plugin: the calculated device_offset {device_offset} is NOT a valid device index"
                log_message(logging.WARNING, msg)
                update_chosen_plugin_device(None)  # ???
    elif encoder_index in row_02_encoders:
        # these encoders represent Sends 1 - 8 in C4M_CHANNEL_STRIP mode
        param = subordinate_selected_track_allows_audio and encoders[encoder_index].v_pot_parameter()
        if liveobj_valid(param):
            if isinstance(param, int):  # PyCharm says 'param' is an int based on the
                #                         self.__encoders[encoder_index].v_pot_parameter() assignment above.
                #                         int also doesn't have a default_value?
                param.value = 0  # if param is never actually an int when it isn't None, this assignment just satisfies PyCharm
            else:
                param.value = param.default_value  # button press == jump to default value of Send
        else:
            log_message(logging.WARNING, f"{log_id}can't update param.value to default: None object")
    elif encoder_index in row_03_encoders:

        encoder_27_index = 26  # X-Fade
        encoder_28_index = 27  # Solo
        encoder_29_index = 28  # Rec Arm
        encoder_30_index = 29  # Mute
        s = next(x for x in encoders if x.vpot_index() == encoder_index)

        if encoder_index < encoder_27_index:
            # these encoders are the four < encoder_29_index, left half of bottom row, sends 9 - 12
            param = subordinate_selected_track_allows_audio and encoders[encoder_index].v_pot_parameter()
            if liveobj_valid(param):
                if isinstance(param, int):
                    param.value = 0
                else:
                    param.value = param.default_value  # button press == jump to default value of Send
            else:
                log_message(logging.WARNING, f"{log_id}can't update param.value to default: param not liveobj_valid()")

        elif encoder_index == encoder_27_index:
            xfade("handle_pressed_v_pot", encoder_index)

        elif encoder_index == encoder_28_index:
            if subordinate_track_is_selected:
                if not selected_track.solo:
                    selected_track.solo = True
                else:
                    selected_track.solo = False
            else:
                show_message("track cannot be soloed")
                s.unlight_vpot_leds()

        elif encoder_index == encoder_29_index:
            if subordinate_track_is_selected:
                if is_armable_track_selected:
                    if not selected_track.arm:
                        selected_track.arm = True
                    else:
                        selected_track.arm = False
                else:
                    show_message("track cannot be armed")
                    s.unlight_vpot_leds()

        elif encoder_index == encoder_30_index:
            if subordinate_track_is_selected:
                if selected_track.mute:
                    selected_track.mute = False
                else:
                    selected_track.mute = True
            else:
                show_message("master track cannot be muted")

        elif encoder_index > encoder_30_index:
            #  encoder 31 is "Pan"
            #  encoder 32 is "Volume"
            param = encoders[encoder_index].v_pot_parameter()
            param.value = param.default_value  # button press == jump to default value of Pan or Vol

    return update_self

def reassign_encoder_parameters(selected_track, extended_device_list, log_msg, ds, encoders, display_parameters,
                                update_vpot_leds_for_device_toggle, subordinate_track_is_selected, subordinate_selected_track_allows_audio, send_parameter,
                                is_log_less_than_info, xfade):
    log_id = "mode_utils_tcs.reassign_encoder_parameters: "
    encoder_07_index = 6
    encoder_08_index = 7
    encoder_27_index = 26
    encoder_28_index = 27
    encoder_29_index = 28
    encoder_30_index = 29
    encoder_31_index = 30
    encoder_32_index = 31

    is_armable_track_selected = script_utils.can_be_armed(selected_track)
    current_nbr_of_devices_on_selected_track = len(extended_device_list)

    nbr_of_available_device_pages = int(current_nbr_of_devices_on_selected_track / SETUP_DB_DEVICE_BANK_SIZE)  # / 8
    nbr_of_remainder_devices = int(current_nbr_of_devices_on_selected_track % SETUP_DB_DEVICE_BANK_SIZE)
    if nbr_of_available_device_pages >= SETUP_DB_MAX_DEVICE_BANKS:
        nbr_of_available_device_pages = SETUP_DB_MAX_DEVICE_BANKS
    elif nbr_of_available_device_pages < 0:
        nbr_of_available_device_pages = 0
        log_msg(logging.ERROR, f"{log_id}Not possible, right? and yet I am logged")

    if nbr_of_available_device_pages == 0 and nbr_of_remainder_devices > 0:
        nbr_of_available_device_pages = 1
    elif nbr_of_remainder_devices > 0:  # 0 < nbr_of_available_device_pages <= SETUP_DB_MAX_DEVICE_BANKS  #  <= 128
        nbr_of_available_device_pages += 1

    # this is the max (channel mode) device page count (based on the current number of devices on the selected track)
    # value automatically calculated when devices are added/removed from track device list
    required_nbr = ds.selected_track_nbr_required_device_banks
    if required_nbr != nbr_of_available_device_pages:
        log_msg(logging.ERROR, f"{log_id}assumtion issue: {required_nbr} stored required banks doesn't match calculated nbr {nbr_of_available_device_pages}")

    # the current selected bank should already be updated (and accurate)?
    current_device_bank_track = ds.last_selected_track_device_bank_view_index  # .selected_device_bank_index
    if current_device_bank_track is None:
        current_device_bank_track = 0

    for s in encoders:
        s_index = s.vpot_index()
        vpot_display_text = EncoderDisplaySegment(s_index)
        vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

        if s_index in row_00_encoders:
            if s_index == encoder_07_index:
                if current_device_bank_track > 0:
                    vpot_display_text.set_text(f"<< {current_device_bank_track + 1:02d}", 'Device')
                    s.show_full_enlighted_poti()
                else:
                    vpot_display_text.set_text(f"   {current_device_bank_track + 1:02d}", 'Device')
                    s.unlight_vpot_leds()
            elif s_index == encoder_08_index:
                if current_device_bank_track < nbr_of_available_device_pages - 1:
                    vpot_display_text.set_text(f"{nbr_of_available_device_pages :02d} >>", ' Bank ')
                    s.show_full_enlighted_poti()
                else:
                    vpot_display_text.set_text(f"{nbr_of_available_device_pages :02d}   ", ' Bank ')
                    s.unlight_vpot_leds()
            else:
                s.unlight_vpot_leds()
            display_parameters.append(vpot_display_text)

        elif s_index in row_01_encoders:

            row_index = s_index - SETUP_DB_DEVICE_BANK_SIZE  # row_index == "index of" s_index in row_01_encoders range
            current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)

            # display part
            if row_index + current_encoder_bank_offset < ds.selected_track_nbr_stored_devices:
                encoder_index_in_row = row_index + int(current_encoder_bank_offset)
                if encoder_index_in_row < len(extended_device_list):
                    device_name = extended_device_list[encoder_index_in_row].name

                    # device_name in bottom row, blanks on top (top text blocked across full LCD)
                    vpot_display_text.set_text(device_name, '')

                else:
                    vpot_display_text.set_text('dvcNme', 'No')  # could just leave as default blank spaces

            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            display_parameters.append(vpot_display_text)

            # to light up vpot ring for active devices
            # Get list of active devices
            active_devices = [device for device in extended_device_list if device.is_active]

            # add listener for devices
            for device in extended_device_list:
                device_encoder_index_in_row = extended_device_list.index(device)
                try:
                    extended_device_list[device_encoder_index_in_row].add_is_active_listener(update_vpot_leds_for_device_toggle)
                except RuntimeError:
                    pass

            # Loop over active devices and update their LEDs once initially
            active_device_encoder_indices = [extended_device_list.index(device) for device in active_devices]
            for encoder_index in range(len(encoders)):
                if encoder_index in row_01_encoders:
                    row_index = encoder_index - SETUP_DB_DEVICE_BANK_SIZE
                    current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)
                    per_encoder_index_in_row = row_index + current_encoder_bank_offset
                    if per_encoder_index_in_row < len(extended_device_list):
                        if per_encoder_index_in_row in active_device_encoder_indices:
                            encoders[encoder_index].show_full_enlighted_poti()
                        else:
                            encoders[encoder_index].unlight_vpot_leds()
                    else:
                        encoders[encoder_index].unlight_vpot_leds()

        elif s_index < encoder_27_index:
            if subordinate_selected_track_allows_audio:

                send_param = send_parameter(s_index - SETUP_DB_DEVICE_BANK_SIZE * 2)
                param_obj = send_param[0]
                if liveobj_valid(param_obj) and param_obj.is_enabled:  # selected_track.mixer_device.sends[index].is_enabled
                    vpot_param = (param_obj, VPOT_DISPLAY_WRAP)
                    # encoder 17 index is (16 % 8) = index 0 ('send bank' 0) <-- 'sends index' 0
                    # encoder 25 index is (24 % 8) = index 0 ('send bank' 1) <-- 'sends index' 8 (if any)
                    vpot_display_text.set_text(param_obj, send_param[1])
                else:
                    # if self.current_log_level < self.log_levels["INFO"]:
                    if is_log_less_than_info:
                        format_nbr = s_index % NUM_ENCODERS_ONE_ROW
                        if s_index in row_03_encoders:
                            format_nbr += NUM_ENCODERS_ONE_ROW
                        vpot_display_text.set_text(" ---- ", f"send{format_nbr}")

            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            display_parameters.append(vpot_display_text)

        elif s_index == encoder_27_index:
            xfade("reassign_encoder_parameters", s.vpot_index())

        elif s_index == encoder_28_index:
            # self.returns_switch = 0
            if subordinate_track_is_selected and not selected_track.solo:
                vpot_display_text.set_text(None, 'Solo')
            else:
                vpot_display_text.set_text(None, 'Solo' if subordinate_track_is_selected else 'Master')

            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            display_parameters.append(vpot_display_text)

        elif s_index == encoder_29_index:
            # self.returns_switch = 0
            if subordinate_track_is_selected:
                vpot_param = (None, VPOT_DISPLAY_BOOLEAN)
                if is_armable_track_selected:
                    is_armed = selected_track.arm
                    vpot_display_text.set_text(is_armed, 'RecArm')  # this is static text
                else:
                    vpot_display_text.set_text('Never', 'RecArm')
            else:
                vpot_display_text.set_text(None, 'Master')

            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            display_parameters.append(vpot_display_text)

        elif s_index == encoder_30_index:
            if subordinate_track_is_selected:
                is_muted = selected_track.mute
                vpot_display_text.set_text(is_muted, 'Mute')

            display_parameters.append(vpot_display_text)
        elif s_index == encoder_31_index:
            if selected_track.has_audio_output:
                vpot_display_text.set_text(selected_track.mixer_device.panning, 'Pan')  # static text
                vpot_param = (selected_track.mixer_device.panning, VPOT_DISPLAY_BOOST_CUT)  # the actual param

            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            display_parameters.append(vpot_display_text)
        elif s_index == encoder_32_index:
            if selected_track.has_audio_output:
                vpot_display_text.set_text(selected_track.mixer_device.volume, 'Volume')
                vpot_param = (selected_track.mixer_device.volume, VPOT_DISPLAY_WRAP)
            else:
                vpot_display_text.set_text('', '')

            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
            display_parameters.append(vpot_display_text)


def do_display_update(app_view, selected_track, chosen_plugin, is_locked_to_device, display_parameters,
                      btn_ctlr, scrolling_display_text, xfade, subordinate_track_is_selected, encoders, show_device_bank_pair, lcd1_device_chain_flags):
    log_id = "mode_utils_tcs.do_display_update: "
    upper_string1 = ''
    lower_string1 = ''
    upper_string2 = ''
    lower_string2 = ''
    upper_string3 = ''
    lower_string3 = ''
    upper_string4 = ''
    lower_string4 = ''

    encoder_7_index = 6
    encoder_8_index = 7

    encoder_27_index = 26
    encoder_28_index = 27
    encoder_29_index = 28
    encoder_30_index = 29
    encoder_31_index = 30
    encoder_32_index = 31

    is_group_track = script_utils.is_group_track(selected_track)
    is_grouped = script_utils.is_grouped(selected_track)
    is_folded = script_utils.is_folded(selected_track) if liveobj_valid(selected_track) else False
    is_view_visible_session = app_view.is_view_visible('Session')
    is_view_visible_arranger = app_view.is_view_visible('Arranger')
    # device name is limited (truncated) to 22 chars if script is locked to a device on a grouped track,
    # device name shifts left by 7 characters if the track is not grouped, and the name can be 7 chars longer before trucation
    # device_name shifts left by another 7 chars if the script is not also locked to a device (on the selected track) and can be 14 characters longer before truncation
    device_name_limit = 22 + 7 + 7
    if liveobj_valid(chosen_plugin):
        selected_device_name = adjust_string(chosen_plugin.name, device_name_limit)
    else:
        selected_device_name = ''.join(' ' for x in range(device_name_limit))

    # shows "fold" or "unfold" or nothing depending on if group track or grouped track
    if is_group_track or is_grouped:
        ftxt = 'unfold' if is_folded else ' fold '
        #                  1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) upper
        upper_string1 += f'------ Track ------- {ftxt} --------------'
    else:
        upper_string1 +=  '------ Track -------        --------------'
    # assert len(upper_string1) == 42 so far

    # 'selected track' name, centered over the first 3 encoders in top row, also indicates frozen tracks
    if liveobj_valid(selected_track):
        segment = adjust_string(selected_track.name, 12) + " "
        if is_locked_to_device:
            if selected_track.is_frozen:
                # can you lock to a device on a frozen track? (where you can't change any (frozen) device parameter values)
                segment += 'Frzn+Lck' # lgth 8
            else:
                segment += '-Locked-'  # lgth 8
        elif selected_track.is_frozen:
            segment += '-Frozen-'      # lgth 8
        else:  # not locked or frozen
            segment = adjust_string(segment, 20) + " "
        lower_string1 += segment
    else:
        lower_string1 += adjust_string('invalid Track object', 20) + " "

    # assert len(lower_string1) == 21 == # * 7
    group_text = ' Track ' if is_view_visible_arranger else ' Group ' if is_view_visible_session and (is_group_track or is_grouped) else '       '
    # assert len(group_text) == 7
    lower_string1 += group_text

    # assert len(lower_string1) == 28
    empty_group_text = is_view_visible_session and not (is_group_track or is_grouped)
    empty_track_details_text = not is_locked_to_device or (liveobj_valid(selected_track) and not selected_track.is_frozen)
    if empty_group_text:
        if empty_track_details_text:
            blank_chars_to_slice = 14
            new_len = len(lower_string1) - blank_chars_to_slice
            lower_string1 = lower_string1[:new_len]
            lower_string1 += adjust_string(selected_device_name, blank_chars_to_slice + 14)
        else:
            blank_chars_to_slice = 7
            new_len = len(lower_string1) - blank_chars_to_slice
            lower_string1 = lower_string1[:new_len]
            lower_string1 += adjust_string(selected_device_name, blank_chars_to_slice + 14)

    else:
        lower_string1 += adjust_string(selected_device_name, 14)
    # assert len(lower_string1) == (28 - 14) + 28 == (28 - 7) + 21 == 28 + 14 == 42,
    # so maybe no space between end of truncated long device name and <<
    # (where long means device names over the length of 22 if script is locked to some device on a grouped track
    # and 36 in most other cases (not locked, not grouped)

    #                 1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) upper
    upper_string2  = '----------------------- Devices -----------------------'  # length 55
    for i in range(len(lcd1_device_chain_flags) - 1):
        if lcd1_device_chain_flags[i]: # flag indexes 0 - 6
            index_base = i * 7             #                        0,  1,  2,  3,  4,  5,  6)
            replace_index = 7 + index_base # indexes are positions (7, 14, 21, 28, 35, 42, 49)
            replace_index -= 1 # positions are indexes again
            upper_string2 = upper_string2[:replace_index] + "|" + upper_string2[replace_index:]  # there is probably a more pythonic way to substitute chars than slicing
    # now if for example, the devices associated with encoders 10, 12, 13, 15 have a class_name that ends with "GroupDevice",
    #                                1------2------3------4------5------6------7------8------   == 56 chars (8 * 7)
    # upper_string2 might look like '-------|-------------|- Devi|es -----------------|-----'  # on the top line of LCD 2 (of 4 from top)

    try:
        text_for_encoder_7 = display_parameters[encoder_7_index]
        l_7raw_text = text_for_encoder_7.get_lower_text()
        text_for_encoder_8 = display_parameters[encoder_8_index]
        l_8raw_text = text_for_encoder_8.get_lower_text()
    except IndexError:
        l_7raw_text = "<< xx"
        l_8raw_text = "xx >>"
    assert len(l_7raw_text) == 5 and len(l_8raw_text) == 5

    upper_string1 += ' Device Bank-'
    # assert len(upper_string1) == 42 + len(' Device Bank-') == 42 + 13 == 55
    # assert len(lower_string1) == 42
    if show_device_bank_pair: # only displaying bank navigation details when there is at least one device and banks to navigate (more than 8 devices)
        lower_string1 += adjust_string(l_7raw_text, 6) + "/"  # for ' << 01 /' 7 chars
        lower_string1 += " " + adjust_string(l_8raw_text, 5)        # for ' 01 >>'   6 chars (end of display line at 55 chars, encoder 8's "divider" char truncated)
    else:
        lower_string1 += ''.join(" " for x in range(13))
    # assert len(lower_string1) == 42 + 13 == 55


    for t in encoder_range:
        try:
            text_for_display = next(x for x in display_parameters if (x.is_index_match(t)))
        except StopIteration:
            text_for_display = EncoderDisplaySegment(t)
            text_for_display.set_text('zzzzzz', 'ZZZZZZ')

        u_alt_text = text_for_display.get_upper_text()
        l_alt_text = text_for_display.get_lower_text()

        # LCD text for row 0 encoders already constructed
        if t in row_01_encoders:
            if btn_ctlr.spot_erase_led_state > 0:
                l_alt2_text = scrolling_display_text(l_alt_text, t)
                lower_string2 += adjust_and_tag(l_alt2_text)
            else:
                lower_string2 += adjust_and_tag(l_alt_text)
        elif t in row_02_encoders:
            if btn_ctlr.spot_erase_led_state > 0:
                upper_string3 += ''.join([scrolling_display_text(u_alt_text, t), ' '])
            else:
                upper_string3 += adjust_and_tag(u_alt_text)
            lower_string3 += adjust_and_tag(l_alt_text)
        elif t in row_03_encoders:
            if t < encoder_27_index:
                if btn_ctlr.spot_erase_led_state > 0:
                    upper_string4 += ''.join([scrolling_display_text(u_alt_text, t), ' '])
                else:
                    upper_string4 += adjust_and_tag(u_alt_text)
                lower_string4 += adjust_and_tag(l_alt_text)

            if t == encoder_27_index:
                upper, lower = xfade("on_update_display_timer", t, u_alt_text, l_alt_text)
                upper_string4 += upper
                lower_string4 += lower

            if t == encoder_28_index:
                if liveobj_valid(selected_track):
                    if subordinate_track_is_selected:
                        if selected_track.solo:
                            l_alt_text = "ON"
                            encoders[encoder_28_index].show_full_enlighted_poti()
                        else:
                            l_alt_text = "OFF"
                            encoders[encoder_28_index].unlight_vpot_leds()
                    else:
                        l_alt_text = "NoSolo"

                lower_string4 += adjust_and_tag(l_alt_text)
                upper_string4 += adjust_and_tag(u_alt_text)

            elif t == encoder_29_index:
                if liveobj_valid(selected_track):
                    if selected_track.can_be_armed:
                        if selected_track.arm:
                            l_alt_text = "ON"
                            encoders[encoder_29_index].show_full_enlighted_poti()
                        else:
                            l_alt_text = "OFF"
                            encoders[encoder_29_index].unlight_vpot_leds()
                    else:
                        l_alt_text = "No Arm"

                lower_string4 += adjust_and_tag(l_alt_text)
                upper_string4 += adjust_and_tag(u_alt_text)

            elif t == encoder_30_index:
                if subordinate_track_is_selected and liveobj_valid(selected_track):
                    if selected_track.mute:
                        l_alt_text = "ON"
                        encoders[encoder_30_index].show_full_enlighted_poti()
                    else:
                        l_alt_text = "OFF"
                        encoders[encoder_30_index].unlight_vpot_leds()
                    lower_string4 += adjust_and_tag(l_alt_text)

                else:
                    lower_string4 += adjust_and_tag(l_alt_text)
                lower_string4 += ' '
                upper_string4 += adjust_and_tag(u_alt_text)

            elif t == encoder_31_index:
                lower_string4 += adjust_and_tag(l_alt_text)
                upper_string4 += adjust_and_tag(u_alt_text)

            elif t == encoder_32_index:
                lower_string4 += adjust_and_tag(l_alt_text)
                upper_string4 += adjust_and_tag(u_alt_text)

    return upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4

def adjust_and_tag(segment, tag=" "):
    tag = tag[:1]
    return ''.join([adjust_string(segment, 6), tag])