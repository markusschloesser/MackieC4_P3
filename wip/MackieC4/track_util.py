# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\track_util.py
# Compiled at: 2021-01-27 15:20:47
# Size of source mod 2**32: 6989 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import chain

import sys

from Push2.decoration import TrackDecoratorFactory
from ableton.v2.base import const, compose, depends, find_if, liveobj_valid, EventObject, listens, listenable_property, \
    liveobj_changed, nop, listens_group, flatten
from ableton.v2.control_surface.components.item_lister import ItemProvider
from ableton.v2.control_surface.components.mixer import RightAlignTracksTrackAssigner
from ableton.v2.control_surface.components.session_ring import SessionRingComponent

if sys.version_info[0] >= 3:  # Live 11
    from ableton.v2.base import old_hasattr

from ableton.v2.control_surface import Component, find_instrument_devices
import Live


def is_group_track(track):
    if liveobj_valid(track):
        return track.is_foldable


def is_grouped(track):
    if liveobj_valid(track):
        return track.is_grouped


def group_track(track):
    if is_grouped(track):
        return track.group_track


def flatten_tracks(tracks):
    return chain(*((grouped_tracks(t) if is_group_track(t) else [t]) for t in tracks))


@depends(song=(const(None)))
def grouped_tracks(track, song=None):
    if not is_group_track(track):
        return []
    return flatten_tracks(filter(lambda t: group_track(t) == track, song.tracks))


def toggle_fold(track):
    if is_group_track(track):
        track.fold_state = not track.fold_state
        return True
    elif is_grouped(track):
        toggle_fold(track.group_track)
    else:
        track.view.is_collapsed = not track.view.is_collapsed  # for collapsing tracks in Arrange view
    return False


def is_folded(track):
    if is_group_track(track):
        return track.fold_state
    return False


def can_be_armed(track):
    if liveobj_valid(track):
        return track.can_be_armed


def arm(track):
    if can_be_armed(track):
        track.arm = True
        return True
    return False


def unarm(track):
    if can_be_armed(track):
        track.arm = False
        return True
    return False


def unarm_tracks(tracks):
    for track in tracks:
        unarm(track)


def tracks(song):
    return filter(liveobj_valid, song.tracks)


def visible_tracks(song):
    return filter(liveobj_valid, song.visible_tracks)


def toggle_track_fold(self, track):
    if old_hasattr(track, 'is_foldable') and track.is_foldable:
        track.fold_state = not track.fold_state
    else:
        if old_hasattr(track, 'is_showing_chains') and track.can_show_chains:
            track.is_showing_chains = not track.is_showing_chains
        else:
            instruments = list(find_instrument_devices(track))
            if instruments:
                instrument = instruments[0]
                if old_hasattr(instrument, 'is_showing_chains'):
                    if instrument.can_show_chains:
                        instrument.is_showing_chains = not instrument.is_showing_chains


def find_parent_track(live_object):
    track = live_object
    while liveobj_valid(track):
        track = isinstance(track, Live.Track.Track) or getattr(track, 'canonical_parent', None)

    return track


def get_chains_recursive(track_or_chain):
    instruments = list(find_instrument_devices(track_or_chain))
    chains = []
    if instruments:
        if old_hasattr(instruments[0], 'chains'):
            for chain in instruments[0].chains:
                chains.append(chain)
                instruments = list(find_instrument_devices(chain))
                if instruments and old_hasattr(instruments[0], 'chains') and instruments[0].is_showing_chains:
                    nested_chains = get_chains_recursive(chain)
                    chains.extend(nested_chains)

    return chains


def get_racks_recursive(track_or_chain):
    instruments = list(find_instrument_devices(track_or_chain))
    racks = []
    if instruments:
        if old_hasattr(instruments[0], 'chains'):
            racks.append(instruments[0])
            for chain in instruments[0].chains:
                instruments = list(find_instrument_devices(chain))
                if instruments and old_hasattr(instruments[0], 'chains') and instruments[0].can_have_chains:
                    nested_racks = get_racks_recursive(chain)
                    racks.extend(nested_racks)

    return racks


def get_flattened_track(track):
    flat_track = [
     track]
    if track.can_show_chains:
        if track.is_showing_chains:
            all_chains = get_chains_recursive(track)
            flat_track.extend(all_chains)
    return flat_track


def get_all_mixer_tracks(song):
    tracks = []
    for track in song.visible_tracks:
        tracks.extend(get_flattened_track(track))

    return tracks + list(song.return_tracks)


class SelectedMixerTrackProvider(EventObject):

    @depends(song=None)
    def __init__(self, song=None, *a, **k):
        (super(SelectedMixerTrackProvider, self).__init__)(*a, **k)
        self._view = song.view
        self._selected_mixer_track = None
        self._on_selected_track_changed.subject = self._view
        self._on_selected_chain_changed.subject = self._view
        self._on_selected_track_changed()

    @listens('selected_track')
    def _on_selected_track_changed(self):
        self._on_selected_mixer_track_changed()

    @listens('selected_chain')
    def _on_selected_chain_changed(self):
        self._on_selected_mixer_track_changed()

    @listenable_property
    def selected_mixer_track(self):
        return self._get_selected_chain_or_track()

    @selected_mixer_track.setter
    def selected_mixer_track(self, track_or_chain):
        unwrapped_track = getattr(track_or_chain, 'proxied_object', track_or_chain)
        if liveobj_changed(self._selected_mixer_track, unwrapped_track):
            if isinstance(unwrapped_track, Live.Chain.Chain):
                self._view.selected_chain = unwrapped_track
                unwrapped_track.canonical_parent.view.selected_chain = unwrapped_track
            else:
                self._view.selected_track = unwrapped_track

    def _on_selected_mixer_track_changed(self):
        selected_mixer_track = self._get_selected_chain_or_track()
        if liveobj_changed(self._selected_mixer_track, selected_mixer_track):
            self._selected_mixer_track = selected_mixer_track
            self.notify_selected_mixer_track(self.selected_mixer_track)

    def _get_selected_chain_or_track(self):
        selected_chain = self._view.selected_chain
        if selected_chain:
            return selected_chain
        return self._view.selected_track


class SessionRingTrackProvider(SessionRingComponent, ItemProvider):

    @depends(set_session_highlight=(const(nop)))
    def __init__(self, set_session_highlight=nop, *a, **k):
        self._decorator_factory = TrackDecoratorFactory()
        (super(SessionRingTrackProvider, self).__init__)(a, set_session_highlight=partial(set_session_highlight, include_rack_chains=True), tracks_to_use=self._decorated_tracks_to_use, **k)
        self._artificially_selected_item = None
        self._selected_item_when_item_artificially_selected = None
        self._update_listeners()
        self._selected_track = self.register_disconnectable(SelectedMixerTrackProvider())
        self._on_selected_item_changed.subject = self._selected_track
        self._track_assigner = RightAlignTracksTrackAssigner(song=(self.song))

    def scroll_into_view(self, mixable):
        mixable_index = self.tracks_to_use().index(mixable)
        new_offset = self.track_offset
        if mixable_index >= self.track_offset + self.num_tracks:
            new_offset = mixable_index - self.num_tracks + 1
        else:
            if mixable_index < self.track_offset:
                new_offset = mixable_index
        self.track_offset = new_offset

    def _get_selected_item(self):
        track_or_chain = self._selected_track.selected_mixer_track
        if liveobj_valid(self._artificially_selected_item):
            track_or_chain = self._artificially_selected_item
        return self._decorator_factory.decorated_objects.get(track_or_chain, track_or_chain)

    def _set_selected_item(self, item):
        self._artificially_selected_item = None
        self._selected_track.selected_mixer_track = item
        self.notify_selected_item()

    selected_item = property(_get_selected_item, _set_selected_item)

    @property
    def items(self):
        return self._track_assigner.tracks(self)

    def move(self, tracks, scenes):
        super(SessionRingTrackProvider, self).move(tracks, scenes)
        if tracks != 0:
            self._ensure_valid_track_offset()
            self.notify_items()

    def _update_track_list(self):
        super(SessionRingTrackProvider, self)._update_track_list()
        self._ensure_valid_track_offset()
        self.notify_items()
        self._update_listeners()

    def _decorated_tracks_to_use(self):
        return self._decorator_factory.decorate_all_mixer_tracks(get_all_mixer_tracks(self.song))

    def controlled_tracks(self):
        return [getattr(track, 'proxied_object', track) for track in self.items]

    def set_selected_item_without_updating_view(self, item):
        all_tracks = get_all_mixer_tracks(self.song)
        if item in all_tracks:
            self._artificially_selected_item = item
            self._selected_item_when_item_artificially_selected = self.song.view.selected_track
            self.notify_selected_item()

    def synchronize_selection_with_live_view(self):
        if self._artificially_selected_item:
            self.selected_item = self._artificially_selected_item

    @listens_group('is_showing_chains')
    def _on_is_showing_chains_changed(self, _):
        self._update_track_list()

    @listens_group('chains')
    def _on_chains_changed(self, _):
        if not self.song.view.selected_track.can_show_chains:
            self.selected_item = self.song.view.selected_track
        self._update_track_list()

    @listens_group('devices')
    def _on_devices_changed(self, _):
        self._update_track_list()

    def _update_listeners(self):

        def flattened_list_of_instruments(instruments):
            return list(flatten(instruments))

        tracks = self.song.tracks
        self._on_devices_changed.replace_subjects(tracks)
        chain_listenable_tracks = [track for track in tracks if isinstance(track, Live.Track.Track) if track]
        instruments_with_chains = flattened_list_of_instruments([get_racks_recursive(track) for track in chain_listenable_tracks if track])
        tracks_and_chains = chain_listenable_tracks + instruments_with_chains
        self._on_is_showing_chains_changed.replace_subjects(tracks_and_chains)
        self._on_chains_changed.replace_subjects(instruments_with_chains)
        self._on_instrument_return_chains_changed.replace_subjects(instruments_with_chains)

    def _ensure_valid_track_offset(self):
        max_index = len(self.tracks_to_use()) - 1
        clamped_offset = min(self.track_offset, max_index)
        if clamped_offset != self.track_offset:
            self.track_offset = clamped_offset

    @listens_group('return_chains')
    def _on_instrument_return_chains_changed(self, _):
        self._update_track_list()

    @listens('selected_mixer_track')
    def _on_selected_item_changed(self, _):
        if liveobj_changed(self._selected_item_when_item_artificially_selected, self.song.view.selected_track):
            self._artificially_selected_item = None
        self.notify_selected_item()
