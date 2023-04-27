# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)

from __future__ import absolute_import, print_function, unicode_literals

from itertools import chain


from ableton.v2.base import const, depends, liveobj_valid


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


def _crossfade_toggle_value(self, value):
    if liveobj_valid(self.selected_track):
        self.selected_track.mixer_device.crossfade_assign = (self.selected_track.mixer_device.crossfade_assign - 1) % len(self.selected_track.mixer_device.crossfade_assignments.values)
