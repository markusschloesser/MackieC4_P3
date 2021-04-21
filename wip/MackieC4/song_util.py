from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain

import sys
from ableton.v2.base import const, compose, depends, find_if, liveobj_valid

if sys.version_info[0] >= 3:  # Live 11
    from ableton.v2.base import old_hasattr

from ableton.v2.control_surface import Component, find_instrument_devices
import Live


# toggle follow song
def toggle_follow(self):
    self.song().view.follow_song = not self.song().view.follow_song


# loop on/off
def toggle_loop(self):  # works
    self.song().loop = not self.song().loop


# toggle arrange/session mode
def toggle_session_arranger_is_visible(self):  # works
    if self.application().view.is_view_visible('Session'):
        self.application().view.focus_view('Arranger')
    else:
        self.application().view.hide_view('Arranger')


# toggle clip / Device view
def toggle_detail_sub_view(self):  # works
    if self.application().view.is_view_visible('Detail/Clip'):
        self.application().view.show_view('Detail/DeviceChain')
    else:
        self.application().view.show_view('Detail/Clip')


# show / hide browser
def toggle_browser_is_visible(self):  # works
    if self.application().view.is_view_visible('Browser'):
        self.application().view.hide_view('Browser')
    else:
        self.application().view.show_view('Browser')


# back to arrangement / BTA
def toggle_back_to_arranger(self, name='BTA'):
    self.song().back_to_arranger = not self.song().back_to_arranger
    
    
# unsolo all
def unsolo_all(self):  # works
    for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
        if track.solo:
            track.solo = False


def any_muted_track(self):
    tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    exists = next((x for x in tracks if x.mute), None)
    if exists is not None:
        return True
    return False

# unmute all
def unmute_all(self):  # works
    for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
        if track.mute:
            track.mute = False


def redo(self):
    if self.song().can_redo:
        self.song().redo()


def undo(self):
    if self.song().can_undo:
        self.song().undo()
