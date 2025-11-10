# was originally Python bytecode 2.5
# Compiled at: 2011-01-12 12:23:43

from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import object

from .consts import *
import Live
import MidiRemoteScript


class MackieC4Component(object):
    """Baseclass for every 'subcomponent' of the Mackie Control. Just offers some """
    __module__ = __name__

    # main_script is the MackieC4 "main class instance" that interacts with Live
    # see the MackieC4 __init__ where it calls the EncoderController __init__
    # passing self and the list of initialized controllers, and then see inside
    # EncoderController __init__ where it names that second parameter main_script
    # then passes to this __init__.
    def __init__(self, main_script):
        self.__main_script = main_script

    def destroy(self):
        self.__main_script = None
        return

    def main_script(self):
        return self.__main_script

    def shift_is_pressed(self):
        return self.__main_script.shift_is_pressed()

    def set_shift_is_pressed(self, pressed):
        self.__main_script.shift_is_pressed = pressed

    def option_is_pressed(self):
        return self.__main_script.option_is_pressed()

    def set_option_is_pressed(self, pressed):
        self.__main_script.option_is_pressed = pressed

    def ctrl_is_pressed(self):
        return self.__main_script.ctrl_is_pressed()

    def set_ctrl_is_pressed(self, pressed):
        self.__main_script.set_pressed = pressed

    def alt_is_pressed(self):
        return self.__main_script.alt_is_pressed()

    def set_alt_is_pressed(self, pressed):
        self.__main_script.set_pressed = pressed

    def song(self):
        return self.__main_script.song()

    def script_handle(self):
        return self.__main_script.handle()

    def application(self):
        return self.__main_script.application()

    def send_midi(self, bytes):
        self.__main_script.send_midi(bytes)

    def request_rebuild_midi_map(self):
        self.__main_script.request_rebuild_midi_map()

    def refresh_state(self):
        self.__main_script.refresh_state()

    def get_device_list(self, container):
        """ add each device in order. If device is a rack / RackDevice / GroupDevice, process each chain recursively."""
        # device_list = track_util.get_racks_recursive(track)  # this refers to the method used by Ableton in track_selection (which didn't work, but I'll leave it in here for now)
        device_list = []
        for device in container:
            if len(device_list) < 127:  # now limited to 127 devices, because some drum racks have over 136 and that kind of breaks it
                device_list.append(device)
                if device.can_have_chains:  # is a rack and it's open
                    # if device.view.is_showing_chain_devices:  # this makes device list foldable, which wouldn't work with current script.
                    # So for now, everything is a flattened list
                    for ch in device.chains:
                        chain_devices = [d for ch in device.chains for d in self.get_device_list(ch.devices)]
                        for d in chain_devices:
                            if len(device_list) < 127:
                                device_list.append(d)
                            else:
                                break
            else:
                break
        return device_list


def make_interpolater(Live_value_min, Live_value_max, C4_min, C4_max):
    # Figure out how 'wide' each range is
    LiveSpan = Live_value_max - Live_value_min
    C4_Span = C4_max - C4_min

    # Compute the scale factor between left and right values
    scaleFactor = float(C4_Span) / float(LiveSpan)

    # create interpolation function using pre-calculated scaleFactor
    def interp_fn(value):
        return C4_min + (value - Live_value_min) * scaleFactor

    return interp_fn
