
import time
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.elements.display_data_source import adjust_string

from . import script_utils
from .script_utils import EncoderDisplaySegment
from .script_utils import make_interpolater
from .consts import *


def handle_pressed_v_pot(pressed_encoder_button_id, encoders, song, app_view, btn_ctlr, unsolo_all_functionality, update_undo_info, update_redo_info,
                         beat_pointer, nav_directions):
    encoder_01_index = 0  # follow
    encoder_02_index = 1  # loop
    encoder_03_index = 2  # Detail / Clip
    encoder_04_index = 3  # Session / Arrange mode
    encoder_05_index = 4  # browser visible on/off
    encoder_06_index = 5  # unsolo all
    encoder_07_index = 6  # unmute all
    encoder_08_index = 7  # BTA
    encoder_09_index = 8  # Undo
    encoder_10_index = 9  # Redo
    encoder_11_index = 10  # unarm all
    encoder_12_index = 11  # SPP
    # encoder_13_index is covered / occupied by SPP from 12
    encoder_14_index = 13
    encoder_16_index = 15  # Scroll / Zoom
    encoder_17_index = 16  # Metronome
    encoder_18_index = 17  # re-enable automation
    encoder_19_index = 18  # stop scrub
    encoder_25_index = 24  # Stop
    encoder_26_index = 25  # Play
    encoder_27_index = 26  # continue play
    encoder_28_index = 27  # overdub

    encoder_index = pressed_encoder_button_id - C4SID_VPOT_PUSH_BASE
    s = next(x for x in encoders if x.vpot_index() == encoder_index)

    if encoder_index == encoder_01_index:
        script_utils.toggle_follow(song_view=song.view)
        if song.view.follow_song:
            s.show_full_enlighted_poti()
        else:
            s.unlight_vpot_leds()
    elif encoder_index == encoder_02_index:
        if song.loop:
            script_utils.toggle_loop(song=song)
            s.unlight_vpot_leds()
        else:
            script_utils.toggle_loop(song=song)
            s.show_full_enlighted_poti()

    elif encoder_index == encoder_03_index:
        script_utils.toggle_detail_sub_view(app_view=app_view, modifier_pressed=btn_ctlr.only_shift_is_pressed)
        if app_view.is_view_visible('Detail/Clip'):
            s.show_full_enlighted_poti()
        else:
            s.unlight_vpot_leds()
    elif encoder_index == encoder_04_index:
        script_utils.toggle_session_arranger_is_visible(app_view=app_view, modifier_pressed=btn_ctlr.only_shift_is_pressed)
        if script_utils.is_arranger_visible(app_view=app_view):
            s.show_full_enlighted_poti()
        else:
            s.unlight_vpot_leds()
    elif encoder_index == encoder_05_index:
        script_utils.toggle_browser_is_visible(app_view=app_view, modifier_pressed=btn_ctlr.only_shift_is_pressed)
        if script_utils.is_browser_visible(app_view=app_view):
            s.show_full_enlighted_poti()
        else:
            s.unlight_vpot_leds()
    elif encoder_index == encoder_06_index:
        unsolo_all_functionality("handle_pressed_v_pot", encoder_index)

    elif encoder_index == encoder_07_index:
        tracks = tuple(song.tracks) + tuple(song.return_tracks)
        script_utils.unmute_all(tracks)

    elif encoder_index == encoder_08_index:
        script_utils.toggle_back_to_arranger(song=song)

    elif encoder_index == encoder_09_index:  # Undo
        if song.can_undo:
            result = song.undo()
            clean = result.removeprefix("Undo ").strip() if result else ""
            update_undo_info(clean)
        else:
            s.unlight_vpot_leds()

    elif encoder_index == encoder_10_index:  # Redo
        if song.can_redo:
            result = song.redo()
            clean = result.removeprefix("Redo ").strip() if result else ""
            update_redo_info(clean)

    elif encoder_index == encoder_11_index:
        script_utils.unarm_all_button(song.tracks)

    # toggle between BEAT and SMPTE mode for SPP
    elif encoder_index == encoder_12_index:
        beat_pointer("handle_pressed_v_pot", encoder_index)

    elif encoder_index == encoder_16_index:
        if app_view.is_view_visible('Arranger'):
            app_view.zoom_view(nav_directions.left, '', btn_ctlr.only_alt_is_pressed)

    elif encoder_index == encoder_17_index:
        song.metronome = not song.metronome

    elif s.vpot_index() == encoder_18_index:
        if song.re_enable_automation_enabled:
            """Returns true if some automated parameter has been overridden"""
            song.re_enable_automation()

    elif s.vpot_index() == encoder_19_index:
        if song.view.detail_clip:
            song.view.detail_clip.stop_scrub()

    #  capture_midi placeholder

    elif encoder_index == encoder_25_index:
        song.stop_playing()
        encoders[encoder_26_index].unlight_vpot_leds()
        encoders[encoder_27_index].unlight_vpot_leds()
    elif encoder_index == encoder_26_index:
        if btn_ctlr.only_shift_is_pressed:
            if not song.is_playing:
                song.continue_playing()
            else:
                song.stop_playing()
        elif btn_ctlr.only_control_is_pressed:
            song.play_selection()
        else:
            song.start_playing()
        s.show_full_enlighted_poti()
    elif encoder_index == encoder_27_index:
        song.continue_playing()
        s.show_full_enlighted_poti()
    elif encoder_index == encoder_28_index:
        if song.overdub:
            s.unlight_vpot_leds()  # if lit (because overdub), turn off
        else:
            s.show_full_enlighted_poti()
        song.overdub = not song.overdub

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