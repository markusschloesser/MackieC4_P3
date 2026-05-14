

from .consts import *

def reassign_encoder_parameters(encoders, extended_device_list, update_vpot_leds_for_device_toggle, send_user_mode_display_strings):
    # need to rebuild the midi map for every encoder disconnected from all parameters
    for s in encoders:
        s.unlight_vpot_leds()
        s.set_v_pot_parameter(None, VPOT_DISPLAY_SINGLE_DOT)

    # don't actively listen for updates in USER mode
    for device in extended_device_list:
        device_encoder_index_in_row = extended_device_list.index(device)
        try:
            extended_device_list[device_encoder_index_in_row].remove_is_active_listener(update_vpot_leds_for_device_toggle)
        except RuntimeError:
            pass

    # display this text once only here because the Max sequencer handles its own display in C4M_USER mode
    # users see these instructions displayed when the Max sequencer is NOT connected,
    # (the text is never "redisplayed" when processing on_display_timer events),
    # and sometimes when the sequencer is connected but MIDI bandwidth is bottle-necked and slow
    send_user_mode_display_strings()  # this is the only exception to the "timer based updates" only policy (when no Split LEDs are lit)