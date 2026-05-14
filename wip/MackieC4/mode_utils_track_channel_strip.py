from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

from . import script_utils
from .script_utils import EncoderDisplaySegment
from .consts import *


def do_display_update(app_view, selected_track, chosen_plugin, is_locked_to_device, display_parameters,
                      btn_ctlr, scrolling_display_text, xfade, subordinate_track_is_selected, encoders):
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

    lower_string1 += adjust_string(l_7raw_text, 6) + "/"  # for '<< 01 /' 7 chars
    lower_string1 += " " + adjust_string(l_8raw_text, 5)  # for ' 01 >>' 6 chars (end of line)


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