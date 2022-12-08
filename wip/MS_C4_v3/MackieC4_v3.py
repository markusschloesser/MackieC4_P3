from __future__ import absolute_import, print_function, unicode_literals

# import Live
import time
from ableton.v2.base import const, inject, listens, task
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, ControlSurface, Layer
from ableton.v2.control_surface.input_control_element import InputControlElement, MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.input_control_element import MIDI_PB_TYPE, MIDI_SYSEX_TYPE, ScriptForwarding
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

from .hw_elements import create_encoder, SESSION_WIDTH, SESSION_HEIGHT
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
            # uncomment to produce Control registered twice assertion error
            # self._register_control(self._prehear_volume_control)

            self._view_control_stub = C4ViewControlComponent(*a, **k)
            self._mixer = MixerComponent(tracks_provider=self._view_control_stub)

            self._set_controls()
            # self._create_session()

        # noinspection PyTypeChecker
        fmt = str('%d.%m.%Y %H:%M:%S')
        timestamp = time.strftime(fmt, time.localtime())
        banner = "--------------= C4 v3 Project log opened =--------------"
        # Writes message into Live's main log file. logger.info() is a ControlSurface method.
        logger.info(timestamp + banner)
        for key in self._forwarding_registry.keys():
            logger.info("forwarding key<{}> value<{}>".format(key, self._forwarding_registry[key]))
        for key in self._forwarding_long_identifier_registry.keys():
            logger.info("forwarding long key<{}> value<{}>".format(key, self._forwarding_long_identifier_registry[key]))

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

    def _do_receive_midi(self, midi_bytes):
        logger.info("do received midi bytes <{}>".format(midi_bytes))
        self.notify_received_midi(*midi_bytes)
        logger.info("'received_midi' listeners notified")
        self.mxd_midi_scheduler.handle_message(midi_bytes)
        logger.info("'midi scheduler' handle_message called")
        self.process_midi_bytes(midi_bytes, self._receive_midi_data)
        logger.info("'process_midi_bytes' called")

    def receive_midi(self, midi_bytes):
        logger.info("receive_midi received midi bytes <{}>".format(midi_bytes))
        super(MackieC4_v3, self).receive_midi(midi_bytes)

    def _install_mapping(self, midi_map_handle, control, parameter, feedback_delay, feedback_map):
        if isinstance(control, EncoderElement):
            logger.info("Encoder<{}> in _install_mapping".format(control.name))

        super(MackieC4_v3, self)._install_mapping(midi_map_handle, control, parameter, feedback_delay, feedback_map)

    def _install_forwarding(self, midi_map_handle, control, forwarding_type=ScriptForwarding.exclusive):
        if isinstance(control, EncoderElement):
            logger.info("Encoder<{}> ScriptForwarding was <{}> now is 2".format(control.name, forwarding_type))
            non_consuming = 2
            forwarding_type = ScriptForwarding(non_consuming)

        super(MackieC4_v3, self)._install_forwarding(midi_map_handle, control, forwarding_type)

    def _set_controls(self):
        logger.info("bingo <{}>".format(self._prehear_volume_control.value_listener_count()))
        for key in self._forwarding_registry.keys():
            logger.info("forwarding key<{}> value<{}>".format(key, self._forwarding_registry[key]))
        for key in self._forwarding_long_identifier_registry.keys():
            logger.info("forwarding long key<{}> value<{}>".format(key, self._forwarding_long_identifier_registry[key]))

        if self._prehear_volume_control.value_listener_count() == 0:
            self._prehear_volume_control.add_value_listener(self._encoder_value_listener)
            logger.info("bango <{}>".format(self._prehear_volume_control.value_listener_count()))
            for key in self._forwarding_registry.keys():
                logger.info("forwarding key<{}> value<{}>".format(key, self._forwarding_registry[key]))
            for key in self._forwarding_long_identifier_registry.keys():
                logger.info(
                    "forwarding long key<{}> value<{}>".format(key, self._forwarding_long_identifier_registry[key]))

        self._mixer.set_prehear_volume_control(self._prehear_volume_control)

    def _encoder_value_listener(self, value, *a, **k):
        logger.info("bongo <{}>".format(value))
