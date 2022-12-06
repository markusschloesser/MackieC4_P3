# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\VCM600.py
# Compiled at: 2021-03-17 12:36:39
# Size of source mod 2**32: 8821 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live


from ableton.v2.control_surface import ControlSurface, MIDI_CC_TYPE, Layer
from ableton.v2.control_surface.elements import EncoderElement
from ableton.v2.control_surface.components import MixerComponent, SessionRingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement

from .element_utils import make_button, make_encoder, make_slider
from .mixer_navigation import MixerNavigationComponent

NUM_TRACKS = 12


class C4_framework(ControlSurface):
    mixer_navigation_type = MixerNavigationComponent

    def __init__(self, *a, **k):
        super(C4_framework, self).__init__(*a, **k)
        with self.component_guard():
            self._create_mixer()

    def _create_mixer(self):
        is_momentary = True
        self._session_ring = SessionRingComponent(name='Session_Navigation',
                                                  num_tracks=8,
                                                  num_scenes=0,
                                                  is_enabled=False)
        self._mixer = MixerComponent(name='Mixer', is_enabled=False, tracks_provider=(self._session_ring),
                                     invert_mute_feedback=True,
                                     layer=Layer(volume_controls=(self.EncoderElement)))



