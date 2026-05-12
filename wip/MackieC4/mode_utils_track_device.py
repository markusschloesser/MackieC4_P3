
import logging

from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

from . import script_utils
from .consts import *
from .EncoderDisplaySegment import EncoderDisplaySegment


def do_display_update(t_d_idx, selected_track, chosen_plugin, is_locked_to_device, pad_right_if_less, device_ref, display_parameters,
                      btn_ctlr, scrolling_display_text, log_msg):
    log_id = "mode_utils_td.do_display_update: "
    upper_string1 = ''
    lower_string1 = ''
    lower_string1a = ''
    lower_string1b = ''
    upper_string2 = ''
    lower_string2 = ''
    upper_string3 = ''
    lower_string3 = ''
    upper_string4 = ''
    lower_string4 = ''
    so_many_spaces = ''.join(' ' for x in range(NUM_TEXT_BYTES_PER_SYSEX_MSG))  # 55

    encoder_7_index = 6
    encoder_8_index = 7

    add_tail = False
    if is_locked_to_device and liveobj_valid(chosen_plugin):
        upper_string1 += f"------ Track --- LOCKED to Device {t_d_idx}"
        add_tail = True
    elif liveobj_valid(chosen_plugin):
        upper_string1 += f"------ Track ------- ----- Device {t_d_idx}"
        add_tail = True
    else:  # not locked or valid
        upper_string1 += "------ Track ------- --No--Device----------"
    if add_tail:
        if t_d_idx is None:
            upper_string1 += ' ----- '
        elif t_d_idx > 99:
            upper_string1 += ' --- '
        else:
            upper_string1 += ' ---- ' if t_d_idx > 9 else ' ----- '
    # log_msg(f"device index is {t_d_idx} ")

    if liveobj_valid(selected_track):
        track_name = selected_track.name
        # lower_string1a += f"{adjust_string(track_name, 12)}(Frozen)" if selected_track.is_frozen else adjust_string(track_name, 20)
        lower_string1a += " " + adjust_string(track_name, 11)
        if not is_locked_to_device and not selected_track.is_frozen:
            lower_string1a = adjust_string(selected_track.name, 20)
        elif selected_track.is_frozen:
            lower_string1a += "-Frozen-"
    else:
        lower_string1a += adjust_string('invalid Track object', 20)

    lower_string1a = pad_right_if_less(lower_string1a, max_length=27)

    if not liveobj_valid(chosen_plugin):
        # blank everything out
        upper_string1 += '             '
        lower_string1b += '                                   '
        lower_string1 += lower_string1a + lower_string1b
        upper_string2 += '               NO DEVICES ON THIS TRACK                '
        lower_string2 += so_many_spaces
        upper_string3 += so_many_spaces
        lower_string3 += so_many_spaces
        upper_string4 += so_many_spaces
        lower_string4 += so_many_spaces
    else:
        device_name = '  '
        if is_locked_to_device:
            device_name = chosen_plugin.name
        elif t_d_idx is not None and t_d_idx > -1:
            # device_ref = self.__eah.data.get_device(self.__eah.last_selected_track_index, t_d_idx)
            device_name = device_ref.device_name
        lower_string1b = str(device_name)  # adjust_string(str(device_name), 20).center(20)
        if is_locked_to_device:
            if selected_track.is_frozen:
                lower_string1b += ' FL'
            else:
                lower_string1b += ' Lk'
        elif selected_track.is_frozen:
            lower_string1b += ' Fz'
        # else: # not locked or frozen
        lower_string1 += lower_string1a + adjust_string(str(lower_string1b), 20).center(20)
        # make sure there is room for control text <<Bank and Bank>>
        lower_string1 = pad_right_if_less(lower_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - len('<<BankBank>>'))
        if is_locked_to_device:
            upper_string1 = pad_right_if_less(upper_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - len('-Params Bank-'))
        # else:
        #     self.pad_right_if_less(upper_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - 7)
        upper_string1 += '-Params Bank-'
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

            # if t in range(6, NUM_ENCODERS_ONE_ROW):
            if t in (encoder_7_index, encoder_8_index):
                l_alt_text = l_raw_text
                lower_string1 += adjust_string((str(l_alt_text)), 6)
                if t == encoder_7_index:
                    lower_string1 += "/"
                elif t == encoder_8_index:
                    pass
                else:
                    lower_string1 += " "
            elif t in row_01_encoders:
                upper_string2 += adjust_string(u_alt_text, 6) + ' '
                lower_string2 += adjust_string(str(l_alt_text), 6) + ' '
            elif t in row_02_encoders:
                upper_string3 += adjust_string(u_alt_text, 6) + ' '
                lower_string3 += adjust_string(str(l_alt_text), 6) + ' '
            elif t in row_03_encoders:
                upper_string4 += adjust_string(u_alt_text, 6) + ' '
                lower_string4 += adjust_string(str(l_alt_text), 6) + ' '
            else:
                if t < encoder_7_index:
                    pass  # valid indexes 0 - 5 get a pass
                else:
                    log_msg(logging.ERROR, f"{log_id}oopsie? {t} is NOT a valid encoder index?")

    return upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4