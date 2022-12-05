from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object

# import Live

from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components.view_control import ViewControlComponent
from ableton.v2.control_surface.components.target_track import TargetTrackComponent


class C4ViewControlComponent(ViewControlComponent):

    def __init__(self, num_tracks=0, num_returns=0, *a, **k):
        super(C4ViewControlComponent, self).__init__(*a, **k)
        self._session_width = num_tracks
        self._nbr_returns = num_returns
        self._offset_listeners = []
        self.track_offset = 0  # 'C4ViewControlComponent' object has no attribute 'track_offset'
        self._target_track = TargetTrackComponent(*a, **k)

    def add_offset_listener(self, other):
        pass

    def remove_offset_listener(self, other):
        pass

    def notify_offset_listener(self, value, other):
        pass

    def offset_has_listener(self, other):
        pass

    def offset_listener_count(self):
        return len(self._offset_listeners)

    @property
    def num_tracks(self):
        return self._session_width

    def _get_target_track(self):
        return [self._target_track.target_track]

    @property
    def tracks_to_use(self):
        return self._get_target_track
    #     return filter(lambda t: liveobj_valid(t) and t == self._target_track.target_track, self.song.tracks)
