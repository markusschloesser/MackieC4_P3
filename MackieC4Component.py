# Python bytecode 2.5 (62131)
# Embedded file name: /Applications/Live 8.2.1 OS X/Live.app/Contents/App-Resources/MIDI Remote Scripts/MackieC4/MackieC4Component.py
# Compiled at: 2011-01-12 12:23:43
# Decompiled by https://python-decompiler.com
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object  # MS needed for new object at class
from .consts import *
import Live
import MidiRemoteScript
from _Framework.ControlSurface import ControlSurface


class MackieC4Component(object):  # MS lets try this, also in new Mackie control scripts
    """Baseclass for every 'sub component' of the Mackie Control. Just offers some """
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

    def control_is_pressed(self):
        return self.__main_script.control_is_pressed()

    def set_control_is_pressed(self, pressed):
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