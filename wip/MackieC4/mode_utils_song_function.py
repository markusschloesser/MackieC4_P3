
import time
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

from . import script_utils
from .script_utils import EncoderDisplaySegment
from .consts import *
from .MackieC4Component import make_interpolater


def reassign_encoder_parameters(encoders, song, display_parameters):
    encoder_01_index = 0
    encoder_02_index = 1
    encoder_03_index = 2
    encoder_04_index = 3
    encoder_05_index = 4
    encoder_06_index = 5
    encoder_07_index = 6
    encoder_08_index = 7
    encoder_09_index = 8
    encoder_10_index = 9
    encoder_11_index = 10
    encoder_17_index = 16  # Metronome in Function mode
    encoder_18_index = 17
    encoder_19_index = 18
    encoder_22_index = 21
    encoder_25_index = 24
    encoder_26_index = 25
    encoder_27_index = 26
    encoder_28_index = 27

    encoders_to_display_text = {
        encoder_01_index: ('unfllw', 'follow'),
        encoder_02_index: ('on/off', 'Loop'),
        encoder_03_index: ('Detail', 'Clip/'),
        encoder_04_index: ('Arrang', 'Sessn'),
        encoder_05_index: ('on/off', 'Browsr'),
        encoder_06_index: ('all', 'unsolo'),
        encoder_07_index: ('all', 'unmute'),
        encoder_08_index: ('Arrang', 'Back 2'),
        encoder_11_index: ('all', 'unarm'),
        encoder_17_index: ('nome  ', 'Metro '),
        encoder_18_index: ('Autmtn', 'Renabl'),
        encoder_19_index: ('Clip  ', 'Scrub '),
        encoder_22_index: (None, 'BPM   '),
        encoder_28_index: ('on/off', 'Ovrdub'),
    }

    for s in encoders:
        s_index = s.vpot_index()
        vpot_display_text = EncoderDisplaySegment(s_index)

        vpot_param = (None, VPOT_DISPLAY_SINGLE_DOT)

        if s_index in encoders_to_display_text:
            display_text = encoders_to_display_text[s_index]
            if display_text[0] is not None:
                vpot_display_text.set_text(display_text[0], display_text[1])
            else:
                vpot_display_text.set_upper_text(display_text[1])
        elif s.vpot_index() == encoder_09_index:
            vpot_display_text.set_upper_text_and_alt('NoUndo', 'Undo  ')
        elif s.vpot_index() == encoder_10_index:
            vpot_display_text.set_upper_text_and_alt('NoRedo', 'Redo  ')

        #  capture_midi

        elif s.vpot_index() == encoder_25_index:
            if song.is_playing:
                vpot_display_text.set_text(' Stop ', ' Song ')
            else:
                vpot_display_text.set_text(' Stop ', ' Song ')
        elif s.vpot_index() == encoder_26_index:
            if not song.is_playing:
                vpot_display_text.set_text(' Play ', ' Song ')
            else:
                vpot_display_text.set_text(' Play ', ' Song ')
        elif s.vpot_index() == encoder_27_index:
            if not song.is_playing:
                vpot_display_text.set_text('contin', ' Song ')
            else:
                vpot_display_text.set_text('contin', ' Song ')

        s.set_v_pot_parameter(vpot_param[0], vpot_param[1])
        display_parameters.append(vpot_display_text)


def do_display_update(app_view, song, selected_track, encoders, display_parameters, unsolo_all_functionality,
                      btn_ctlr, last_undo_label_time, last_undo_label, scrolling_display_text, last_redo_label_time, last_redo_label, beat_pointer, loop_length):

    log_id = "mode_utils_sf.do_display_update: "
    upper_string1 = ''
    lower_string1 = ''
    upper_string2 = ''
    lower_string2 = ''
    upper_string3 = ''
    lower_string3 = ''
    upper_string4 = ''
    lower_string4 = ''

    encoder_06_index = 5  # unsolo all
    encoder_07_index = 6  # unmute all
    encoder_08_index = 7  # BTA
    encoder_09_index = 8
    encoder_10_index = 9
    encoder_11_index = 10
    encoder_12_index = 11
    # encoder_13_index is covered / occupied by SPP from 12
    encoder_14_index = 12  # because 12 is occupied, we still need 12 otherwise everything be shifted over
    encoder_15_index = 13
    encoder_16_index = 14
    encoder_17_index = 16  # Metronome
    encoder_18_index = 17  # re-enable automation
    encoder_19_index = 18  # scrub clip
    encoder_20_index = 19  # scroll clip
    encoder_21_index = 20  # zoom clip
    encoder_22_index = 21  # BPM
    encoder_25_index = 24
    encoder_26_index = 25
    encoder_27_index = 26
    for e in encoders:
        try:
            dspl_sgmt = next(x for x in display_parameters if x.display_segment_index == e.vpot_index())
        except StopIteration:
            break  # nothing to display (coming out of USER mode: no parameters are mapped to encoders in USER mode, so no display parameters either (yet))

        if e.vpot_index() in row_00_encoders:
            if e.vpot_index() == encoder_06_index:
                unsolo_all_functionality("on_update_display_timer", e.vpot_index())

            upper_string1 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
            lower_string1 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
        elif e.vpot_index() in row_01_encoders:
            if e.vpot_index() == encoder_09_index:
                upper_string2 += adjust_string(dspl_sgmt.alter_upper_text(song.can_undo), 6) + ' '
                # NEW: lower row = last undo label (from redo), scroll if available
                if btn_ctlr.spot_erase_led_state > 0:
                    if time.time() - last_undo_label_time < 15.0 and last_undo_label:
                        lower_string2 += scrolling_display_text(last_undo_label, e.vpot_index()) + ' '
                    else:
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                else:
                    lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                if song.can_undo:
                    e.show_full_enlighted_poti()
                else:
                    e.unlight_vpot_leds()

            elif e.vpot_index() == encoder_10_index:
                upper_string2 += adjust_string(dspl_sgmt.alter_upper_text(song.can_redo), 6) + ' '
                # NEW: lower row = last redo label (from undo), scroll if available
                if btn_ctlr.spot_erase_led_state > 0:
                    if time.time() - last_redo_label_time < 15.0 and last_redo_label:
                        lower_string2 += scrolling_display_text(last_redo_label, e.vpot_index()) + ' '
                    else:
                        lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                else:
                    lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                if song.can_redo:
                    e.show_full_enlighted_poti()
                else:
                    e.unlight_vpot_leds()

            elif e.vpot_index() == encoder_11_index:
                upper_string2 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
                if script_utils.any_armed_track(song.tracks):
                    e.show_full_enlighted_poti()
                else:
                    e.unlight_vpot_leds()

            elif e.vpot_index() == encoder_12_index:
                # show beat position pointer or SPP at encoder 12 AND encoder 13 position in second row
                upper, lower = beat_pointer("on_update_display_timer", e.vpot_index())
                upper_string2 += upper
                lower_string2 += lower

            # show loop length
            elif e.vpot_index() == encoder_14_index:
                upper, lower = loop_length("on_update_display_timer", e.vpot_index())
                if btn_ctlr.spot_erase_led_state > 0:
                    upper_string2 += scrolling_display_text(upper, e.vpot_index()) + ' '
                else:
                    upper_string2 += upper
                lower_string2 += lower

            # show loop start
            elif e.vpot_index() == encoder_15_index:
                get_loop_start = str(song.loop_start / 4)
                if btn_ctlr.spot_erase_led_state > 0:
                    upper_string2 += scrolling_display_text('LoopStart', e.vpot_index()) + ' '
                else:
                    upper_string2 += 'LoopStart'
                lower_string2 += adjust_string(get_loop_start, 6) + ' '

                # vpot ring light
                display_mode_cc_first = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_WRAP][0]
                display_mode_cc_last = encoder_ring_led_mode_cc_values[VPOT_DISPLAY_WRAP][1]

                scaler = make_interpolater(0, song.last_event_time, display_mode_cc_first, display_mode_cc_last)
                loop_start = int(song.loop_start)
                led_ring_val = int(scaler(loop_start))
                spp_vpot_index = 14
                spp_vpot = encoders[spp_vpot_index]
                spp_vpot.update_led_ring(led_ring_val)

            elif e.vpot_index() == encoder_16_index:
                # show if we are in Session or Arrange view in upper row and selected track name in lower row
                upper_string2 += ('Scroll' if app_view.is_view_visible('Session') else 'Zoom  ')
                if liveobj_valid(selected_track):
                    if btn_ctlr.spot_erase_led_state > 0:
                        lower_string2 += scrolling_display_text(selected_track.name, e.vpot_index())
                    else:
                        lower_string2 += selected_track.name
                else:
                    lower_string2 += '      '

            else:
                upper_string2 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                lower_string2 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
        elif e.vpot_index() in row_02_encoders:
            if e.vpot_index() == encoder_22_index:
                upper_string3 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                lower_string3 += adjust_string(('%3.2f' % song.tempo), 6) + ' '

            else:
                upper_string3 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
                lower_string3 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
        elif e.vpot_index() in row_03_encoders:
            upper_string4 += adjust_string(dspl_sgmt.get_upper_text(), 6) + ' '
            lower_string4 += adjust_string(dspl_sgmt.get_lower_text(), 6) + ' '
            if e.vpot_index() == encoder_25_index:  # Song STOP
                if song.is_playing:
                    e.unlight_vpot_leds()
                else:
                    e.show_full_enlighted_poti()
            elif e.vpot_index() == encoder_26_index:  # Song PLAY
                if song.is_playing:
                    e.show_full_enlighted_poti()
                else:
                    e.unlight_vpot_leds()

    unmute_all_encoder = encoders[encoder_07_index]
    tracks = tuple(song.tracks) + tuple(song.return_tracks)
    if script_utils.any_muted_track(tracks):
        unmute_all_encoder.show_full_enlighted_poti()  # some track is muted (unmute has something to do)
    else:
        unmute_all_encoder.unlight_vpot_leds()  # no tracks are muted

    back_to_arranger_encoder = encoders[encoder_08_index]
    if song.back_to_arranger:
        back_to_arranger_encoder.show_full_enlighted_poti()
    else:
        back_to_arranger_encoder.unlight_vpot_leds()

    metronome_encoder = encoders[encoder_17_index]
    if song.metronome:
        metronome_encoder.show_full_enlighted_poti()
    else:
        metronome_encoder.unlight_vpot_leds()

    re_enable_automation_encoder = encoders[encoder_18_index]
    if song.re_enable_automation_enabled:
        re_enable_automation_encoder.show_full_enlighted_poti()
    else:
        re_enable_automation_encoder.unlight_vpot_leds()

    return upper_string1, lower_string1, upper_string2, lower_string2, upper_string3, lower_string3, upper_string4, lower_string4