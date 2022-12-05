from __future__ import absolute_import, print_function, unicode_literals

# import Live
import time
from ableton.v2.base import const, inject, listens, task
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, ControlSurface, Layer
from ableton.v2.control_surface.components import MixerComponent, SessionNavigationComponent, SessionRingComponent
from ableton.v2.control_surface.components import SessionComponent, SessionOverviewComponent, SimpleTrackAssigner
from ableton.v2.control_surface.components import BasicTrackScroller
from ableton.v2.control_surface.elements import ButtonMatrixElement, EncoderElement, SysexElement, ButtonElement
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent

import sys
if sys.version_info[0] >= 3:  # Live 11
    from builtins import str
    from builtins import range
    from builtins import object

from .hwelements import create_encoder, SESSION_WIDTH, SESSION_HEIGHT
from .C4ViewControlComponent import C4ViewControlComponent

import logging
logger = logging.getLogger(__name__)

IS_MOMENTARY = True
CHANNEL = 0


class MackieC4_v3(ControlSurface):

    def __init__(self, c_inst, *a, **k):
        super(MackieC4_v3, self).__init__(c_instance=c_inst, *a, **k)

        with self.component_guard():
            name = 'Encoder32'  # C4SID_VPOT_CC_ADDRESS_32 = 0x3F
            self._prehear_volume_control = create_encoder(0x3f, name)
            self._view_control = C4ViewControlComponent(*a, **k)
            self._mixer = MixerComponent(tracks_provider=self._view_control)
            self._set_controls()
            # self._create_session()

        # noinspection PyTypeChecker
        fmt = str('%d.%m.%Y %H:%M:%S')
        timestamp = time.strftime(fmt, time.localtime())
        banner = "--------------= C4 v3 Project log opened =--------------"
        # Writes message into Live's main log file. logger.info() is a ControlSurface method.
        logger.info(timestamp + banner)

    # def make_button(identifier, name, **k):
    #     return ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, CHANNEL, identifier, name=name, **k)

    # def _create_session(self):
    #     self._session_ring = SessionRingComponent(name=u'Session_Ring',
    #                                               num_tracks=SESSION_WIDTH, num_scenes=SESSION_HEIGHT)
    #     self._session = SessionComponent(name=u'Session', session_ring=self._session_ring)
    #     self._session_navigation = SessionNavigationComponent(name=u'Session_Navigation', is_enabled=False,
    #                                                           session_ring=self._session_ring,
    #                                                           layer=Layer(left_button=u'left_button',
    #                                                                       right_button=u'right_button'))
    #     self._session_navigation.set_enabled(True)
    #     self._session_overview = SessionOverviewComponent(name=u'Session_Overview', is_enabled=False,
    #                                                       session_ring=self._session_ring, enable_skinning=True,
    #                                                       layer=Layer(button_matrix=u'pads_with_zoom'))

    def _set_controls(self):
        self._mixer.set_prehear_volume_control(self._prehear_volume_control)

