from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain

import sys
from ableton.v2.base import const, compose, depends, find_if, liveobj_valid, listens
from ableton.v2.control_surface import Component, find_instrument_devices
import ableton.v2.control_surface.components as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

if sys.version_info[0] >= 3:  # Live 11
    from ableton.v2.base import old_hasattr

import Live


def toggle_follow(self):
    self.song().view.follow_song = not self.song().view.follow_song


# loop on/off
def toggle_loop(self):
    self.song().loop = not self.song().loop


# toggle arrange/session mode
def toggle_session_arranger_is_visible(self):
    if self.application().view.is_view_visible('Session'):
        self.application().view.focus_view('Arranger')
    else:
        self.application().view.hide_view('Arranger')


# toggle clip / Device view
def toggle_detail_sub_view(self):
    if self.application().view.is_view_visible('Detail/Clip'):
        self.application().view.show_view('Detail/DeviceChain')
    else:
        self.application().view.show_view('Detail/Clip')


def toggle_browser_is_visible(self):
    if self.application().view.is_view_visible('Browser'):
        self.application().view.hide_view('Browser')
    else:
        self.application().view.show_view('Browser')


# back to arrangement / BTA
def toggle_back_to_arranger(self, name='BTA'):
    self.song().back_to_arranger = not self.song().back_to_arranger
    

def unsolo_all(self):
    for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
        if track.solo:
            track.solo = False


def any_muted_track(self):
    tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    exists = next((x for x in tracks if x.mute), None)
    if liveobj_valid(exists):
        return True
    return False


def unmute_all(self):
    for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
        if track.mute:
            track.mute = False


def redo(self):
    if self.song().can_redo:
        self.song().redo()
        return True
    return False


def undo(self):
    if self.song().can_undo:
        self.song().undo()
        return True
    return False


def metronome_button(self, toggled):
    self.song.metronome = toggled


def unarm_all_button(self):
    for track in self.song().tracks:
        if track.can_be_armed and track.arm:
            track.arm = False

#
# class TransportComponent(TransportComponentBase):
#     capture_midi_button = ButtonControl(EncoderControl.vpot_pressed)
#
#     @capture_midi_button.pressed
#     def capture_midi_button(self, _):
#         try:
#             if self.song.can_capture_midi:
#                 self.song.capture_midi()
#         except RuntimeError:
#             pass
#
#     @listens('can_capture_midi')
#     def __on_can_capture_midi_changed(self):
#         self.capture_midi_button.enabled = self.song.can_capture_midi
