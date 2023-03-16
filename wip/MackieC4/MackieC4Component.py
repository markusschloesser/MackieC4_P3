# was originally Python bytecode 2.5
# Compiled at: 2011-01-12 12:23:43

from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import object  # MS needed for new object at class

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
