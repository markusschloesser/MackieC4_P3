# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\session_ring.py
# Compiled at: 2021-01-27 15:20:55
# Size of source mod 2**32: 967 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import SessionRingComponent


class SelectedTrackFollowingSessionRingComponent(SessionRingComponent):

    def __init__(self, *a, **k):
        (super(SelectedTrackFollowingSessionRingComponent, self).__init__)(*a, **k)
        self._SelectedTrackFollowingSessionRingComponent__on_selected_track_changed.subject = self.song.view
        self._SelectedTrackFollowingSessionRingComponent__on_selected_track_changed()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        tracks_to_use = self.tracks_to_use()
        selected_track = self.song.view.selected_track
        if selected_track in tracks_to_use:
            track_index = list(tracks_to_use).index(selected_track)
            new_offset = track_index - track_index % self.num_tracks
            self.track_offset = new_offset
            