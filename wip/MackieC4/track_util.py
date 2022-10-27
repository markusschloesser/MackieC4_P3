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
    flat_track = [track]
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


def _crossfade_toggle_value(self, value):
    if liveobj_valid(self._track):
        self._track.mixer_device.crossfade_assign = value != 0 or self._crossfade_toggle.is_momentary() or (self._track.mixer_device.crossfade_assign - 1) % len(self._track.mixer_device.crossfade_assignments.values)
