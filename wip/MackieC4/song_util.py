from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain

import sys
from ableton.v2.base import const, compose, depends, find_if, liveobj_valid, listens
from ableton.v2.control_surface import Component, find_instrument_devices
from ableton.v2.control_surface.control import ToggleButtonControl
import ableton.v2.control_surface.components as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

if sys.version_info[0] >= 3:  # Live 11
    from ableton.v2.base import old_hasattr

import Live


class ViewToggleComponent(Component):
    detail_view_toggle_button = ToggleButtonControl(untoggled_color='View.DetailOff',
      toggled_color='View.DetailOn')
    main_view_toggle_button = ToggleButtonControl(untoggled_color='View.MainOff',
      toggled_color='View.MainOn')
    clip_view_toggle_button = ToggleButtonControl(untoggled_color='View.ClipOff',
      toggled_color='View.ClipOn')
    browser_view_toggle_button = ToggleButtonControl(untoggled_color='View.BrowserOff',
      toggled_color='View.BrowserOn')

    def __init__(self, *a, **k):
        (super(ViewToggleComponent, self).__init__)(*a, **k)
        self._ViewToggleComponent__on_detail_view_visibility_changed.subject = self.application.view
        self._ViewToggleComponent__on_main_view_visibility_changed.subject = self.application.view
        self._ViewToggleComponent__on_clip_view_visibility_changed.subject = self.application.view
        self._ViewToggleComponent__on_browser_view_visibility_changed.subject = self.application.view
        self._ViewToggleComponent__on_detail_view_visibility_changed()
        self._ViewToggleComponent__on_main_view_visibility_changed()
        self._ViewToggleComponent__on_clip_view_visibility_changed()
        self._ViewToggleComponent__on_browser_view_visibility_changed()

    @detail_view_toggle_button.toggled
    def detail_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail')

    @main_view_toggle_button.toggled
    def main_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Session')

    @clip_view_toggle_button.toggled
    def clip_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail/Clip')

    @browser_view_toggle_button.toggled
    def browser_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Browser')

    def _show_or_hide_view(self, show_view, view_name):
        if show_view:
            self.application.view.show_view(view_name)
        else:
            self.application.view.hide_view(view_name)

    @listens('is_view_visible', 'Detail')
    def __on_detail_view_visibility_changed(self):
        self.detail_view_toggle_button.is_toggled = self.application.view.is_view_visible('Detail')

    @listens('is_view_visible', 'Session')
    def __on_main_view_visibility_changed(self):
        self.main_view_toggle_button.is_toggled = self.application.view.is_view_visible('Session')

    @listens('is_view_visible', 'Detail/Clip')
    def __on_clip_view_visibility_changed(self):
        self.clip_view_toggle_button.is_toggled = self.application.view.is_view_visible('Detail/Clip')

    @listens('is_view_visible', 'Browser')
    def __on_browser_view_visibility_changed(self):
        self.browser_view_toggle_button.is_toggled = self.application.view.is_view_visible('Browser')


# loop on/off
def toggle_loop(self):
    self.song().loop = not self.song().loop


# toggle arrange/session mode
def toggle_session_arranger_is_visible(self):
    if self.application().view.is_view_visible('Session'):
        self.application().view.focus_view('Arranger')
    else:
        self.application().view.hide_view('Arranger')


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
