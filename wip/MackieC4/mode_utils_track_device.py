
import logging

from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

from . import script_utils
from .script_utils import EncoderDisplaySegment
from .consts import *


def reassign_encoder_parameters(selected_track, ds, encoders, chosen_plugin, plugin_parameter, display_parameters ):
    log_id = "mode_utils_td.reassign_encoder_parameters: "
    encoder_07_index = 6
    encoder_08_index = 7
    current_device_bank_param_track = ds.last_selected_track_device_parameter_bank_nbr
    c_bank_text = f"{(current_device_bank_param_track + 1):02d}"
    max_device_bank_param_track = ds.max_last_selected_track_device_parameter_bank_nbr
    m_bank_text = f"{max_device_bank_param_track:02d}"
    for s in encoders:
        s_index = s.vpot_index()
        vpot_display_text = EncoderDisplaySegment(s_index)
        vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

        if s_index == encoder_07_index:

            if chosen_plugin is None:
                s.unlight_vpot_leds()
            elif current_device_bank_param_track > 0:
                vpot_display_text.set_text("<< " + c_bank_text, "")
                s.show_full_enlighted_poti()
            else:
                vpot_display_text.set_text("   " + c_bank_text, "")
                s.unlight_vpot_leds()
        elif s_index == encoder_08_index:
            if chosen_plugin is None:
                s.unlight_vpot_leds()
            elif current_device_bank_param_track < max_device_bank_param_track - 1:
                vpot_display_text.set_text(m_bank_text + ' >>', "")
                s.show_full_enlighted_poti()
            else:
                vpot_display_text.set_text(m_bank_text + "   ", "")
                s.unlight_vpot_leds()
        else:
            # these are the 24 encoders from 9 to 32. Some devices do not have more than 1 or 2 parameters
            # we are only concerned with the 24 encoders on the current "device bank page"
            plugin_param = plugin_parameter(s_index - SETUP_DB_DEVICE_BANK_SIZE)
            if plugin_param is not None:
                vpot_param = (plugin_param[0], VPOT_DISPLAY_WRAP)
                # parameter name in top display row, param value in bottom row
                if liveobj_valid(plugin_param[0]):  # then it is a DeviceParameter object
                    vpot_display_text.set_text(plugin_param[0], plugin_param[1])

        if selected_track.is_frozen:
            # disconnect encoder from param mapping, display now shows blank values reinforcing track frozen status.
            s.set_v_pot_parameter(None, None)
        else:
            s.set_v_pot_parameter(vpot_param[0], vpot_param[1])

        display_parameters.append(vpot_display_text)

def do_display_update(t_d_idx, selected_track, chosen_plugin, is_locked_to_device, pad_right_if_less, device_ref, display_parameters,
                      btn_ctlr, scrolling_display_text, log_msg):
    log_id = "mode_utils_td.do_display_update: "
    upper_string1 = ''
    lower_string1 = ''
    upper_string2 = ''
    lower_string2 = ''
    upper_string3 = ''
    lower_string3 = ''
    upper_string4 = ''
    lower_string4 = ''
    so_many_spaces = ''.join(' ' for x in range(NUM_TEXT_BYTES_PER_SYSEX_MSG))  # 55

    encoder_7_index = 6
    encoder_8_index = 7

    nnn = "---" if t_d_idx is None else f"{t_d_idx:3d}"  # "  9", " 99", or "999"
    if is_locked_to_device and liveobj_valid(chosen_plugin):

        #                  1------
        #                         2------
        #                                3------
        #                                       4------
        #                                              5------
        #                                                     6------
        #                                                            7------
        #                                                                   8------
        #                  1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) upper
        upper_string1 += f"------ Track --- LOCKED to Device {nnn} --"  # upper length == 42 chars
    elif liveobj_valid(chosen_plugin):
        upper_string1 += f"------ Track ------- ----- Device {nnn} --"
    else:  # not locked or valid
        upper_string1 += f"------ Track -------- --No-Device-{nnn}---"
    # assert len(upper_string1) == 42 chars

    if liveobj_valid(selected_track):
        track_name = selected_track.name
        # lower_string1a += f"{adjust_string(track_name, 12)}(Frozen)" if selected_track.is_frozen else adjust_string(track_name, 20)
        #                  1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) lower
        #                  track-name12-Frozen-
        track_name = adjust_string(track_name, 13)
        # same status details as in channel strip mode
        if is_locked_to_device:
            if selected_track.is_frozen:
                lower_string1 += track_name + 'Frzn+Lck' # lgth 8
            else:
                lower_string1 += track_name + '-Locked-' # lgth 8
        elif selected_track.is_frozen:
            lower_string1 += track_name + '-Frozen-'     # lgth 8
        else:  # not locked or frozen
            lower_string1 = adjust_string(selected_track.name, 21)
    else:
        lower_string1 += adjust_string('invalid Track object', 21)
    # assert len(lower_string1) == 21 chars

    if not liveobj_valid(chosen_plugin):
        # blank everything out
        upper_string1  += ''.join(' ' for x in range(14))  # blank spaces over encoders 7 and 8
        # assert len(upper_string1) == 42 + 14 == 56 == 8 * 7

        lower_string1 += ''.join(' ' for x in range(28))  # blank spaces over encoders 5, 6, 7, and 8 (4 * 7 = 28) # lower_string1b
        # assert len(lower_string1) == 21 + 28 == 48
        #                 1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) upper
        upper_string2 += '               NO DEVICES ON THIS TRACK                ' # 55 chars
        lower_string2 += so_many_spaces
        upper_string3 += so_many_spaces
        lower_string3 += so_many_spaces
        upper_string4 += so_many_spaces
        lower_string4 += so_many_spaces
    else:
        # assert len(upper_string1) == 42 chars
        # assert len(lower_string1) == 21 chars
        device_name = 'dummy'
        if is_locked_to_device:
            device_name = chosen_plugin.name
        elif t_d_idx is not None and t_d_idx > -1:
            device_name = device_ref.device_name

        # device_name = adjust_string(str(device_name), 17)
        # if is_locked_to_device:
        #     if selected_track.is_frozen:  # possible when locked?
        #         device_name += ' FL'
        #     else:
        #         device_name += ' Lk'
        # elif selected_track.is_frozen:
        #     device_name += ' Fz'
        # else: # not locked or frozen
        #     device_name = adjust_string(str(device_name), 20) + " "
        device_name = adjust_string(device_name, 20) + " "
        # assert len(device_name) == 21
        lower_string1 += device_name
        # assert len(upper_string1) == 42 chars (still)
        # assert len(lower_string1) == 42 == 21 + 21 == 6 * 7
        # leave room for control text
        pad_limit = NUM_TEXT_BYTES_PER_SYSEX_MSG - len('<< 01 / 01 >>') # '<<Bank/Bank>>' pad_limit == 42 == 55 - len('<< 01 / 01 >>')
        lower_string1 = pad_right_if_less(lower_string1, max_length=pad_limit)

        pad_limit = NUM_TEXT_BYTES_PER_SYSEX_MSG - len('-Params Bank-')  # pad_limit == 42 == 55 - len('-Params Bank-')
        upper_string1 = ''.join([upper_string1[:pad_limit], '-Params Bank-'])
        # assert len(upper_string1) == 55 == 8 * 7

        # assert len(lower_string1) == pad_limit == 55 - 13 == 42 == 6 * 7
        try:
            text_for_encoder_7 = display_parameters[encoder_7_index]
            l_7raw_text = text_for_encoder_7.get_lower_text()
            text_for_encoder_8 = display_parameters[encoder_8_index]
            l_8raw_text = text_for_encoder_8.get_lower_text()
        except IndexError:
            l_7raw_text = "<<xxx "
            l_8raw_text = "xxx>>"

        lower_string1 += adjust_string(l_7raw_text, 6) + "/" # for '<< 01 /' 7 chars
        lower_string1 += " " + adjust_string(l_8raw_text, 5) # for ' 01 >>' 6 chars (end of line)


        # assert len(lower_string1) == 55 == 8 * 7
        # assert len(upper_string1) == 55 == 8 * 7

        for t in encoder_range:
            try:
                text_for_display = display_parameters[t]  # assumes always 32
            except IndexError:
                text_for_display = EncoderDisplaySegment(t)
                text_for_display.set_text('---', ' X ')

            u_raw_text = text_for_display.get_upper_text()
            l_raw_text = text_for_display.get_lower_text()

            # change the next 2 lines from get_scrolling_display_text to get_alternating_display_text to stop scrolling
            # and start toggling between 'front half' and 'back half' of the display text
            if btn_ctlr.spot_erase_led_state > 0:
                u_alt_text = scrolling_display_text(u_raw_text, t)
                l_alt_text = scrolling_display_text(l_raw_text, t)
            else:
                u_alt_text = u_raw_text
                l_alt_text = l_raw_text

            if t in row_01_encoders:
                upper_string2 += adjust_string(u_alt_text, 6) + ' '
                lower_string2 += adjust_string(str(l_alt_text), 6) + ' '
            elif t in row_02_encoders:
                upper_string3 += adjust_string(u_alt_text, 6) + ' '
                lower_string3 += adjust_string(str(l_alt_text), 6) + ' '
            elif t in row_03_encoders:
                upper_string4 += adjust_string(u_alt_text, 6) + ' '
                lower_string4 += adjust_string(str(l_alt_text), 6) + ' '
            else:
                if t < row_01_encoders[0]:
                    pass  # valid indexes 0 - 7 get a pass
                else:
                    log_msg(logging.ERROR, f"{log_id}oopsie? {t} is NOT a valid encoder index?")

    return upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4