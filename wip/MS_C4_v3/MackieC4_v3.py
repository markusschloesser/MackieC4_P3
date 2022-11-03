
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import time
from ableton.v2.base import const, inject, listens, task
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_PB_TYPE, ControlSurface, Layer
from ableton.v2.control_surface.components import MixerComponent, SessionNavigationComponent, SessionRingComponent, \
    SessionComponent, SessionOverviewComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement, EncoderElement, SysexElement, ButtonElement
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE
from .hw_elements import HW_Elements, SESSION_WIDTH, SESSION_HEIGHT

IS_MOMENTARY = True
CHANNEL = 0


class MackieC4_v3(ControlSurface):
    def __init__(self, *a, **k):
        (super(MackieC4_v3, self).__init__)(*a, **k)

        with self.component_guard():

            self._create_controls()
            self._create_session()

        # self.log_message(time.strftime("%d.%m.%Y %H:%M:%S",time.localtime()) + "--------------= ProjectX log opened =--------------")  # Writes message into Live's main log file. This is a ControlSurface method.


def make_button(identifier, name, **k):
    return ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, CHANNEL, identifier, name=name, **k)

def _create_session(self):
    self._session_ring = SessionRingComponent(name=u'Session_Ring', num_tracks=SESSION_WIDTH, num_scenes=SESSION_HEIGHT)
    self._session = SessionComponent(name=u'Session', session_ring=self._session_ring)
    self._session_navigation = SessionNavigationComponent(name=u'Session_Navigation', is_enabled=False, session_ring=self._session_ring, layer=Layer(left_button=u'left_button', right_button=u'right_button'))
    self._session_navigation.set_enabled(True)
        self._session_overview = SessionOverviewComponent(name=u'Session_Overview', is_enabled=False, session_ring=self._session_ring, enable_skinning=True, layer=Layer(button_matrix=u'pads_with_zoom'))