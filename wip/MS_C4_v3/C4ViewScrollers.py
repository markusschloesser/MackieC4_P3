from __future__ import absolute_import, print_function, unicode_literals
import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object

# import Live
from ableton.v2.control_surface.components.scroll import ScrollComponent
from ableton.v2.control_surface.components.view_control import TrackScroller, SceneScroller

"""
Comment Quote from: ableton.v2.base.Event.py

    def add_event(cls, event_name_or_event):
        Adds an event to a Disconnectable class. 
        [parameter] event_name_or_event must either be a string or an Event object.

    The class will get a number of new methods:
        * add_[event_name]_listener
        * remove_[event_name]_listener
        * notify_[event_name]_listener
        * [event_name]_has_listener()
        * [event_name]_listener_count
        
The logged error was:  missing "add" method for event: offset
    
So, adding 5 methods for event: offset
"""


# class C4ScrollComponent(ScrollComponent):
#
#     def __init__(self, num_tracks=0, num_returns=0, *a, **k):
#         super(C4ScrollComponent, self).__init__(*a, **k)
#         self._session_width = num_tracks
#         self._nbr_returns = num_returns
#         self._offset_listeners = []
#
#     def add_offset_listener(self, other):
#         pass
#
#     def remove_offset_listener(self, other):
#         pass
#
#     def notify_offset_listener(self, value, other):
#         pass
#
#     def offset_has_listener(self, other):
#         pass
#
#     def offset_listener_count(self):
#         return len(self._offset_listeners)
#
#     @property
#     def num_tracks(self):
#         return self._session_width


# class C4TrackScroller(TrackScroller):
#
#     def __init__(self, num_tracks=0, *a, **k):
#         super(C4TrackScroller, self).__init__(*a, **k)
#         self._session_width = num_tracks
#         self._offset_listeners = []
#
#     def add_offset_listener(self, other):
#         pass
#
#     def remove_offset_listener(self, other):
#         pass
#
#     def notify_offset_listener(self, value, other):
#         pass
#
#     def offset_has_listener(self, other):
#         pass
#
#     def offset_listener_count(self):
#         return len(self._offset_listeners)
#
#     def num_tracks(self):
#         return self._session_width
#
#
# class C4SceneScroller(SceneScroller):
#
#     def __init__(self, num_scenes=0, *a, **k):
#         super(C4SceneScroller, self).__init__(*a, **k)
#         self._session_height = num_scenes
#         self._offset_listeners = []
#
#     def add_offset_listener(self, other):
#         pass
#
#     def remove_offset_listener(self, other):
#         pass
#
#     def notify_offset_listener(self, value, other):
#         pass
#
#     def offset_has_listener(self, other):
#         pass
#
#     def offset_listener_count(self):
#         return len(self._offset_listeners)