from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

import logging

from . import script_utils
from .script_utils import EncoderDisplaySegment
from .consts import *

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

    nbr_of_full_device_pages = int(current_nbr_of_devices_on_selected_track / SETUP_DB_DEVICE_BANK_SIZE)  # / 8
    nbr_of_remainder_devices = int(current_nbr_of_devices_on_selected_track % SETUP_DB_DEVICE_BANK_SIZE)
    if nbr_of_full_device_pages >= SETUP_DB_MAX_DEVICE_BANKS:
        nbr_of_full_device_pages = SETUP_DB_MAX_DEVICE_BANKS
    elif nbr_of_full_device_pages < 0:
        nbr_of_full_device_pages = 0
        log_msg(logging.ERROR, f"{log_id}Not possible, right? and yet I am logged")

    if nbr_of_full_device_pages == 0 and nbr_of_remainder_devices > 0:
        nbr_of_full_device_pages = 1
    elif nbr_of_remainder_devices > 0:  # 0 < nbr_of_full_device_pages <= SETUP_DB_MAX_DEVICE_BANKS  #  <= 16
        nbr_of_full_device_pages += 1

    # this is the max (channel mode) device page count (based on the current number of devices on the selected track)
    # value automatically calculated when devices are added/removed from track device list
    # ds.selected_device_bank_count = nbr_of_full_device_pages

    # the current selected bank should already be updated (and accurate)?
    current_device_bank_track = ds.last_selected_track_device_bank_view_index  # .selected_device_bank_index
    if current_device_bank_track is None:
        current_device_bank_track = 0

    for s in encoders:
        s_index = s.vpot_index()
        vpot_display_text = EncoderDisplaySegment(s_index)
        vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

        if s_index in row_00_encoders:
            vpot_display_text.set_text(f"{current_device_bank_track + 1:02d}", 'Device')
            if s_index == encoder_07_index:
                if current_device_bank_track > 0:
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            elif s_index == encoder_08_index:
                vpot_display_text.set_text(f"{nbr_of_full_device_pages :02d}", ' Bank ')
                if current_device_bank_track < nbr_of_full_device_pages - 1:
                    s.show_full_enlighted_poti()
                else:
                    s.unlight_vpot_leds()
            else:
                s.unlight_vpot_leds()
            display_parameters.append(vpot_display_text)

        elif s_index in row_01_encoders:

            row_index = s_index - SETUP_DB_DEVICE_BANK_SIZE  # row_index == "index of" s_index in row_01_encoders range
            current_encoder_bank_offset = int(current_device_bank_track * SETUP_DB_DEVICE_BANK_SIZE)

            # display part
            if row_index + current_encoder_bank_offset < ds.max_device_count:
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
                      btn_ctlr, scrolling_display_text, xfade, subordinate_track_is_selected, encoders, show_device_bank_pair):
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
    device_name_limit = 22
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
        lower_string1 += adjust_string(selected_track.name, 12) + " "
        if is_locked_to_device:
            if selected_track.is_frozen:
                # can you lock to a device on a frozen track? (where you can't change any (frozen) device parameter values)
                lower_string1 += 'Frzn+Lck' # lgth 8
            else:
                lower_string1 += '-Locked-'  # lgth 8
        elif selected_track.is_frozen:
            lower_string1 += '-Frozen-'      # lgth 8
        else:  # not locked or frozen
            lower_string1 = adjust_string(selected_track.name, 20) + " "
    else:
        lower_string1 += adjust_string('invalid Track object', 20) + " "

    # assert len(lower_string1) == 21 == # * 7
    group_text = ' Track ' if is_view_visible_arranger else ' Group ' if is_view_visible_session and (is_group_track or is_grouped) else '       '
    # assert len(group_text) == 7
    lower_string1 += group_text

    # assert len(lower_string1) == 28
    lower_string1 += adjust_string(selected_device_name, 14) # len(lower_string1) == 42

    #                 1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) upper
    upper_string2 += '----------------------- Devices -----------------------'  # length 55
    # todo MS maybe try to visualize Racks/Groups here by using |  |  ?

    try:
        text_for_encoder_7 = display_parameters[encoder_7_index]
        l_7raw_text = text_for_encoder_7.get_lower_text()
        text_for_encoder_8 = display_parameters[encoder_8_index]
        l_8raw_text = text_for_encoder_8.get_lower_text()
    except IndexError:
        l_7raw_text = "<<xxx "
        l_8raw_text = "xxx>>"

    upper_string1 += '-Device Bank-'
    # assert len(upper_string1) == 42 + len('-Device Bank-') == 42 + 13 == 55
    if show_device_bank_pair:
        lower_string1 += adjust_string(l_7raw_text, 6) + "/"  # for '<< 01 /' 7 chars
        lower_string1 += " " + adjust_string(l_8raw_text, 5)  # for ' 01 >>' 6 chars (end of line)
    else:
        lower_string1 += ''.join(" " for x in range(13))


    for t in encoder_range:
        try:
            text_for_display = next(x for x in display_parameters if (x.is_index_match(t)))
        except StopIteration:
            text_for_display = EncoderDisplaySegment(t)
            text_for_display.set_text('zzzzzz', 'ZZZZZZ')

        u_alt_text = text_for_display.get_upper_text()
        l_alt_text = text_for_display.get_lower_text()

        # if t in range(6, NUM_ENCODERS_ONE_ROW):
        #     upper_string1 += adjust_and_tag(u_alt_text)
        #     lower_string1 += adjust_and_tag(l_alt_text)
        # elif t in row_01_encoders:
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
                    lower_string4 += adjust_string(l_alt_text, 6)  # and_tag?

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