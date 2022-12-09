# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\irig_keys_io.py
# Compiled at: 2021-03-17 12:36:40
# Size of source mod 2**32: 4032 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from ableton.v2.control_surface import ControlSurface, Layer, MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.components import TransportComponent
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
from .mixer import MixerComponent
from .session_recording import SessionRecordingComponent
from .session_ring import SelectedTrackFollowingSessionRingComponent
from .skin import skin
PAD_IDS = (36, 38, 40, 42, 46, 43, 47, 49)
PAD_CHANNEL = 9


class IRigKeysIO(ControlSurface):

    def __init__(self, *a, **k):
        (super(IRigKeysIO, self).__init__)(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_mixer()

    def _create_controls(self):
        self._encoders = ButtonMatrixElement(rows=[
         [EncoderElement(MIDI_CC_TYPE, 0, identifier, map_mode=(Live.MidiMap.MapMode.relative_signed_bit), name=('Volume_Encoder_{}'.format(index))) for index, identifier in enumerate(range(0x29, 0x2A))]],
          name='Volume_Encoders')
        self._data_encoder = EncoderElement(MIDI_CC_TYPE,
          0,
          0x3C,
          map_mode=(Live.MidiMap.MapMode.relative_signed_bit),
          name='Data_Encoder')
        self._data_encoder_button = ButtonElement(True,
          MIDI_CC_TYPE, 0, 23, name='Data_Encoder_Button', skin=skin)
        self._play_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 118, name='Play_Button', skin=skin)
        self._record_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 119, name='Record_Button', skin=skin)
        self._record_stop_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 116, name='Record_Stop_Button', skin=skin)
        self._stop_button = ButtonElement(False,
          MIDI_CC_TYPE, 0, 117, name='Stop_Button', skin=skin)

    def _create_mixer(self):
        self._session_ring = SelectedTrackFollowingSessionRingComponent(is_enabled=False,
          num_tracks=(self._encoders.width()),
          num_scenes=(self._encoders.height()),
          name='Session_Ring')
        self._mixer = MixerComponent(tracks_provider=(self._session_ring), name='Mixer')
        self._mixer.layer = Layer(volume_controls=(self._encoders),
          track_scroll_encoder=(self._data_encoder),
          selected_track_arm_button=(self._data_encoder_button),
          )
