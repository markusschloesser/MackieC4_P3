# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\track_util.py
# Compiled at: 2021-01-27 15:20:47
# Size of source mod 2**32: 6989 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from ableton.v2.base import const, compose, depends, find_if, liveobj_valid
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
        # track.view.is_collapsed = not track.view.is_collapsed  # MS for later. for collapsing tracks in Arrange view
        return True
    elif is_grouped(track):
        toggle_fold(track.group_track)
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


def find_parent_track(live_object):
    track = live_object
    while liveobj_valid(track):
        track = isinstance(track, Live.Track.Track) or getattr(track, 'canonical_parent', None)

    return track
