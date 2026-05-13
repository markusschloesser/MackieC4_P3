
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

    if liveobj_valid(selected_track):
        track_name = selected_track.name
        # lower_string1a += f"{adjust_string(track_name, 12)}(Frozen)" if selected_track.is_frozen else adjust_string(track_name, 20)
        #                  1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) lower
        #                  track-name12-Frozen-
        lower_string1a += adjust_string(track_name, 12)
        # same status details as in channel strip mode
        if is_locked_to_device:
            if selected_track.is_frozen:
                lower_string1 += 'Frzn+Lck' # lgth 8
            else:
                lower_string1 += '-Locked-'  # lgth 8
        elif selected_track.is_frozen:
            lower_string1 += '-Frozen-'      # lgth 8
        else:  # not locked or frozen
            lower_string1 = adjust_string(selected_track.name, 21)
    else:
        lower_string1a += adjust_string('invalid Track object', 21)

    # lower_string1a = pad_right_if_less(lower_string1a, max_length=28)

    if not liveobj_valid(chosen_plugin):
        # blank everything out
        upper_string1  += ''.join(' ' for x in range(14))  # blank spaces over encoders 7 and 8
        lower_string1b += ''.join(' ' for x in range(28))  # blank spaces over encoders 5, 6, 7, and 8
        # don't append the track name again if the track is valid and has no devices
        lower_string1 += lower_string1b # if not lower_string1a.startswith('invalid') else lower_string1a + lower_string1b
        # assert len(lower_string1) == 27 + 28 == 55 == NUM_TEXT_BYTES_PER_SYSEX_MSG
        #                 1------2------3------4------5------6------7------8------   == 56 chars (8 * 7) upper
        upper_string2 += '               NO DEVICES ON THIS TRACK                ' # 55 chars
        lower_string2 += so_many_spaces
        upper_string3 += so_many_spaces
        lower_string3 += so_many_spaces
        upper_string4 += so_many_spaces
        lower_string4 += so_many_spaces
    else:
        device_name = 'dummy'
        if is_locked_to_device:
            device_name = chosen_plugin.name
        elif t_d_idx is not None and t_d_idx > -1:
            device_name = device_ref.device_name
        lower_string1b = str(device_name)  # adjust_string(str(device_name), 20).center(20)
        if is_locked_to_device:
            if selected_track.is_frozen:  # possible when locked?
                lower_string1b += ' FL'
            else:
                lower_string1b += ' Lk'
        elif selected_track.is_frozen:
            lower_string1b += ' Fz'
        # else: # not locked or frozen
        # assert len(lower_string1a) == 20
        lower_string1 += lower_string1a + adjust_string(str(lower_string1b), 21).center(21)
        # assert len(lower_string1) == 40
        # leave room for control text <<Bank and Bank>>
        pad_limit = NUM_TEXT_BYTES_PER_SYSEX_MSG - len('<<Bank/Bank>>') # '<< 01 / 01 >>' pad_limit == 55 - 13 == 42
        lower_string1 = pad_right_if_less(lower_string1, max_length=pad_limit)
        if is_locked_to_device:
            pad_limit = NUM_TEXT_BYTES_PER_SYSEX_MSG - len('-Params Bank-')
            upper_string1 = pad_right_if_less(upper_string1, max_length=pad_limit)
        # else:
        #     self.pad_right_if_less(upper_string1, max_length=NUM_TEXT_BYTES_PER_SYSEX_MSG - 7)
        upper_string1 += '-Params Bank-'

        # assert len(lower_string1) == pad_limit == 55 - 13 == 42 == 6 * 7
        # assert len(upper_string1) == pad_limit == 55 - 13 == 42 == 6 * 7
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
                l_alt_text = l_raw_text # this 'bank' text never scrolls
                lower_string1 += adjust_string((str(l_alt_text)), 6)
                if t == encoder_7_index:
                    lower_string1 += "/"
                # elif t == encoder_8_index:
                #     pass
                # else: # never happens here
                #     lower_string1 += " "
                # assert len(lower_string1) == 42 + 7 (+ 6) == 55
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