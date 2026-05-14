
import logging

from ableton.v2.base import liveobj_valid, depends
from .consts import * 


logger = logging.getLogger(__name__)

class MackieC4ListenerMixin(object):
    """This Mackie C4 Mixin class implements all dictionary based Listener mapping behavior"""
    
    __module__ = __name__

    @depends(log_levels=None)
    def __init__(self, log_levels=None):
                
        self._lm = {}   # lm == listener mappings

        self.__my_log_levels = log_levels

        self._mixer_master_keys = ('volume', 'panning', 'crossfader')
        self._mixer_normal_track_keys_all = ('arm', 'solo', 'mute', 'is_frozen', 'current_monitoring_state', 'available_input_routing_channels',
                                         'available_input_routing_types', 'available_output_routing_channels', 'available_output_routing_types',
                                         'input_routing_channel', 'input_routing_type', 'output_routing_channel', 'output_routing_type')
        self._mixer_normal_track_keys_in_use = ('arm', 'solo', 'mute', 'is_frozen')
        self._mixer_normal_strip_keys_in_use = ('volume', 'panning')
        self._mixer_return_track_keys_all = ('solo', 'mute', 'available_output_routing_channels', 'available_output_routing_types',
                                        'output_routing_channel', 'output_routing_type')
        self._mixer_return_track_keys_in_use = ('solo', 'mute')
        self._mixer_return_strip_keys_in_use = ('volume', 'panning')
        self._initialize_listener_setup()

    # LOM reference to the current song() all remote scripts inherit
    def song(self):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")

    # necessary utility methods
    def get_device_list(self, container, expand_chains=False, report=True):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def log_message(self, level=logging.ERROR, *message):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")

    # listener callback implementation methods
    # Note that typically, only one, if any, input parameter is provided by Live when a registered listener receives a call back notification.
    # Valid input values provided at the time a callback method gets registered as a listener (like r=0 or type below) do NOT
    # get saved in the LOM and passed back later when listener subjects fire actual event notifications. If Live passes an input value to a
    # callback method with a notification, it's because that's how Ableton designed Live's "event observer" system, not because of how
    # this Mixin (and inheritors) implements Live's "event observer" system. (For example, the C4 script is generally only concerned with "visible tracks"
    # while Live's callbacks are generally associated with "(all) tracks" in a song session, so the 'tid' ((all tracks)track index) passed to a listener
    # is quite often different from the index of the same track in Live's "visible tracks" collection.)
    def on_is_frozen_changed(self):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def send_changestate(self, tid, track, sid, send, r=0):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def mixert_changestate(self, type, tid, track):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def mixerv_changestate(self, type, tid, track):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def trname_changestate(self, tid, track, ret):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def selected_device_change_state(self, track, tid, type):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def devpm_change(self, device):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def param_changestate(self, param, tid, did, pid, type):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def scene_change(self):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def track_change(self):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def tracks_change(self, caller=None):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def overdub_change(self):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")
    def transport_change(self):
        raise NotImplementedError("method must be implemented in classes that inherit from this Mixin class")

    def _initialize_listener_setup(self):
        self.setup_device_listener_keys()
        self.setup_normal_track_listener_keys()
        self.setup_return_track_listener_keys()
        self.setup_master_track_listener_keys()

    def setup_device_listener_keys(self):
        self.clear_device_listener_keys()

    def clear_device_listener_keys(self):
        """'Parameter Value', 'Device Parameters', and 'Track Device' Listener key names"""
        self._lm["prlisten"] = {} # parameter.value_has_listener(), for example
        self._lm["plisten"] = {} # device.parameters_has_listener()
        self._lm["dlisten"] = {} # track.view.selected_device_has_listener()
        
    def setup_normal_track_listener_keys(self):
        """(type 0) regular Track "Mixer" Listener key names"""
        self._lm["mlisten"] = {}
        self.clear_normal_track_listener_key_values()
        
    def clear_normal_track_listener_key_values(self):
        self._lm["mlisten"]["solo"] = {}
        self._lm["mlisten"]["mute"] = {}
        self._lm["mlisten"]["arm"] = {}
        self._lm["mlisten"]["is_frozen"] = {}
        self._lm["mlisten"]["current_monitoring_state"] = {}
        self._lm["mlisten"]["panning"] = {}
        self._lm["mlisten"]["volume"] = {}
        self._lm["mlisten"]["sends"] = {}
        self._lm["mlisten"]["name"] = {}
        self._lm["mlisten"]["available_input_routing_channels"] = {}
        self._lm["mlisten"]["available_input_routing_types"] = {}
        self._lm["mlisten"]["available_output_routing_channels"] = {}
        self._lm["mlisten"]["available_output_routing_types"] = {}
        self._lm["mlisten"]["input_routing_type"] = {}
        self._lm["mlisten"]["input_routing_channel"] = {}
        self._lm["mlisten"]["output_routing_channel"] = {}
        self._lm["mlisten"]["output_routing_type"] = {}
        
    def setup_return_track_listener_keys(self):
        """(type 1) Return Track "Mixer" Listener key names"""
        self._lm["rlisten"] = {}
        self.clear_return_track_listener_key_values()
        
    def clear_return_track_listener_key_values(self):
        self._lm["rlisten"]["solo"] = {}
        self._lm["rlisten"]["mute"] = {}
        self._lm["rlisten"]["panning"] = {}
        self._lm["rlisten"]["volume"] = {}
        self._lm["rlisten"]["sends"] = {}
        self._lm["rlisten"]["name"] = {}
        self._lm["rlisten"]["available_output_routing_channels"] = {}
        self._lm["rlisten"]["available_output_routing_types"] = {}
        self._lm["rlisten"]["output_routing_channel"] = {}
        self._lm["rlisten"]["output_routing_type"] = {}

    def setup_master_track_listener_keys(self):
        """(type 2) Master Track "Mixer" Listener key names"""
        self._lm["masterlisten"] = {}
        self.clear_master_track_listener_key_values()
        
    def clear_master_track_listener_key_values(self):
        self._lm["masterlisten"]["panning"] = {}
        self._lm["masterlisten"]["volume"] = {}
        self._lm["masterlisten"]["crossfader"] = {}



    def destroy_mixer_listeners(self):
        # Master Track
        for type in self._mixer_master_keys:
            for tr in self._lm["masterlisten"][type]:
                if liveobj_valid(tr) and liveobj_valid(tr.mixer_device):
                    m_d = tr.mixer_device
                    cb = self._lm["masterlisten"][type][tr]
                    # ('volume', 'panning', 'crossfader')
                    if type == "volume":
                        if m_d.volume.value_has_listener(cb):
                            m_d.volume.remove_value_listener(cb)
                    elif type == 'panning':
                        if m_d.panning.value_has_listener(cb):
                            m_d.panning.remove_value_listener(cb)
                    elif type == 'crossfader':
                        if m_d.crossfader.value_has_listener(cb):
                            m_d.crossfader.remove_value_listener(cb)

        # Normal Tracks
        for type in self._mixer_normal_track_keys_all:
            for tr in self._lm["mlisten"][type]:

                if liveobj_valid(tr):
                    cb = self._lm["mlisten"][type][tr]
                    # ('arm', 'solo', 'mute', 'is_frozen', 'current_monitoring_state', 'available_input_routing_channels',
                    # 'available_input_routing_types', 'available_output_routing_channels', 'available_output_routing_types',
                    # 'input_routing_channel', 'input_routing_type', 'output_routing_channel', 'output_routing_type')
                    if type == 'arm':
                        if tr.can_be_armed:
                            if tr.arm_has_listener(cb):
                                tr.remove_arm_listener(cb)
                    elif type == 'current_monitoring_state':
                        if tr.can_be_armed:
                            if tr.current_monitoring_state_has_listener(cb):
                                tr.remove_current_monitoring_state_listener(cb)
                    elif type == 'solo':
                        if tr.solo_has_listener(cb):
                            tr.remove_solo_listener(cb)
                    elif type == 'mute':
                        if tr.mute_has_listener(cb):
                            tr.remove_mute_listener(cb)
                    elif type == 'is_frozen':
                        if tr.is_frozen_has_listener(cb):
                            tr.remove_is_frozen_listener(cb)
                    elif type == 'available_input_routing_channels':
                        if tr.available_input_routing_channels_has_listener(cb):
                            tr.remove_available_input_routing_channels_listener(cb)
                    elif type == 'available_input_routing_types':
                        if tr.available_input_routing_types_has_listener(cb):
                            tr.remove_available_input_routing_types_listener(cb)
                    elif type == 'available_output_routing_channels':
                        if tr.available_output_routing_channels_has_listener(cb):
                            tr.remove_available_output_routing_channels_listener(cb)
                    elif type == 'available_output_routing_types':
                        if tr.available_output_routing_types_has_listener(cb):
                            tr.remove_available_output_routing_types_listener(cb)
                    elif type == 'input_routing_channel':
                        if tr.input_routing_channel_has_listener(cb):
                            tr.remove_input_routing_channel_listener(cb)
                    elif type == 'input_routing_type':
                        if tr.input_routing_type_has_listener(cb):
                            tr.remove_input_routing_type_listener(cb)
                    elif type == 'output_routing_channel':
                        if tr.output_routing_channel_has_listener(cb):
                            tr.remove_output_routing_channel_listener(cb)
                    elif type == 'output_routing_type':
                        if tr.output_routing_type_has_listener(cb):
                            tr.remove_output_routing_type_listener(cb)

        for type in self._mixer_normal_strip_keys_in_use:
            for tr in self._lm["mlisten"][type]:
                if liveobj_valid(tr)and liveobj_valid(tr.mixer_device):
                    m_d = tr.mixer_device
                    cb = self._lm["mlisten"][type][tr]
                    # ('volume', 'panning')
                    if type == "volume":
                        if m_d.volume.value_has_listener(cb):
                            m_d.volume.remove_value_listener(cb)
                    elif type == 'panning':
                        if m_d.panning.value_has_listener(cb):
                            m_d.panning.remove_value_listener(cb)

        for tr in self._lm["mlisten"]['sends']:
            if liveobj_valid(tr):
                for send in self._lm["mlisten"]['sends'][tr]:
                    if liveobj_valid(send):
                        cb = self._lm["mlisten"]['sends'][tr][send]
                        if send.value_has_listener(cb):
                            send.remove_value_listener(cb)

        for tr in self._lm["mlisten"]['name']:
            if liveobj_valid(tr):
                cb = self._lm["mlisten"]['name'][tr]
                if tr.name_has_listener(cb):
                    tr.remove_name_listener(cb)

        # Return Tracks
        for type in self._mixer_return_track_keys_in_use:
            for tr in self._lm["rlisten"][type]:
                if liveobj_valid(tr):
                    cb = self._lm["rlisten"][type][tr]
                    # ('solo', 'mute')
                    if type == 'solo':
                        if tr.solo_has_listener(cb):
                            tr.remove_solo_listener(cb)
                    elif type == 'mute':
                        if tr.mute_has_listener(cb):
                            tr.remove_mute_listener(cb)

        for type in self._mixer_return_strip_keys_in_use:
            for tr in self._lm["rlisten"][type]:
                if liveobj_valid(tr)and liveobj_valid(tr.mixer_device):
                    m_d = tr.mixer_device
                    cb = self._lm["rlisten"][type][tr]
                    # ('volume', 'panning')
                    if type == "volume":
                        if m_d.volume.value_has_listener(cb):
                            m_d.volume.remove_value_listener(cb)
                    elif type == 'panning':
                        if m_d.panning.value_has_listener(cb):
                            m_d.panning.remove_value_listener(cb)

        for tr in self._lm["rlisten"]['sends']:
            if liveobj_valid(tr):
                for send in self._lm["rlisten"]['sends'][tr]:
                    if liveobj_valid(send):
                        cb = self._lm["rlisten"]['sends'][tr][send]
                        if send.value_has_listener(cb):
                            send.remove_value_listener(cb)

        for tr in self._lm["rlisten"]['name']:
            if liveobj_valid(tr):
                cb = self._lm["rlisten"]['name'][tr]
                if tr.name_has_listener(cb):
                    tr.remove_name_listener(cb)

        self.clear_normal_track_listener_key_values()
        self.clear_return_track_listener_key_values()
        self.clear_master_track_listener_key_values()
        return
    
    def set_mixer_listeners(self):
        self.destroy_mixer_listeners()
        
        for type in self._mixer_master_keys:
            self.add_master_listener(0, type, self.song().master_track)

        tracks = self.song().visible_tracks
        for track_index in range(len(tracks)):
            track_obj = tracks[track_index]
            self.add_trname_listener(track_index, track_obj, 0)
            for type in self._mixer_normal_track_keys_in_use:
                if type == 'is_frozen':
                    if track_obj.can_be_frozen:
                        if track_obj.is_frozen_has_listener(self.on_is_frozen_changed):
                            track_obj.remove_is_frozen_listener(self.on_is_frozen_changed)
                        track_obj.add_is_frozen_listener(self.on_is_frozen_changed)
                if type == 'arm':
                    if track_obj.can_be_armed:
                        self.add_mixert_listener(track_index, type, track_obj)
                else:
                    self.add_mixert_listener(track_index, type, track_obj)

            for type in self._mixer_normal_strip_keys_in_use:
                self.add_mixerv_listener(track_index, type, track_obj)

            for sid in range(len(track_obj.mixer_device.sends)):
                self.add_send_listener(track_index, track_obj, sid, track_obj.mixer_device.sends[sid])

        tracks = self.song().return_tracks
        for track_index in range(len(tracks)):
            track_obj = tracks[track_index]
            self.add_trname_listener(track_index, track_obj, 1)
            for type in self._mixer_return_track_keys_in_use:
                self.add_retmixert_listener(track_index, type, track_obj)

            for type in self._mixer_return_strip_keys_in_use:
                self.add_retmixerv_listener(track_index, type, track_obj)

            for sid in range(len(track_obj.mixer_device.sends)):
                self.add_retsend_listener(track_index, track_obj, sid, track_obj.mixer_device.sends[sid])
                

    def add_send_listener(self, tid, track, sid, send):
        if not (track in self._lm["mlisten"]['sends']):
            self._lm["mlisten"]['sends'][track] = {}
            
        if not (send in self._lm["mlisten"]['sends'][track]):
            cb = lambda: self.send_changestate(tid, track, sid, send)
            self._lm["mlisten"]['sends'][track][send] = cb
            send.add_value_listener(cb)

    def add_mixert_listener(self, tid, type, track):
        if not (track in self._lm["mlisten"][type]):
            cb = lambda: self.mixert_changestate(type, tid, track)
            # ('arm', 'solo', 'mute', 'is_frozen')
            # arm case already handled
            self._lm["mlisten"][type][track] = cb
            try:
                if type == 'solo':
                    track.add_solo_listener(cb)
                elif type =='mute':
                    track.add_mute_listener(cb)
                elif type == 'is_frozen':
                    track.add_is_frozen_listener(cb)
            except AttributeError as e:
                self.log_message(logging.ERROR, f"MCLM.add_mixert_listener: unable to add track {type} listener {cb}")

    def add_mixerv_listener(self, tid, type, track):
        if not (track in self._lm["mlisten"][type]):
            cb = lambda: self.mixerv_changestate(type, tid, track)
            # ('volume', 'panning')
            self._lm["mlisten"][type][track] = cb
            try:
                if type == 'volume':
                    track.mixer_device.volume.add_value_listener(cb)
                elif type == 'panning':
                    track.mixer_device.panning.add_value_listener(cb)
            except AttributeError as e:
                self.log_message(logging.ERROR, f"MCLM.add_mixerv_listener: unable to add track mixer {type} listener {cb}")

    def add_master_listener(self, tid, type, track):
        if not (track in self._lm["masterlisten"][type]):
            cb = lambda: self.mixerv_changestate(type, tid, track, 2)
            # ('volume', 'panning', 'crossfader')
            self._lm["masterlisten"][type][track] = cb
            try:
                if type == 'volume':
                    track.mixer_device.volume.add_value_listener(cb)
                elif type == 'panning':
                    track.mixer_device.panning.add_value_listener(cb)
                elif type == 'crossfader':
                    track.mixer_device.crossfader.add_value_listener(cb)
            except AttributeError as e:
                self.log_message(logging.ERROR, f"MCLM.add_master_listener: unable to add track mixer {type} listener {cb}")

    def add_retsend_listener(self, tid, track, sid, send):
        if not (track in self._lm["rlisten"]['sends']):
            self._lm["rlisten"]['sends'][track] = {}
        if not (send in self._lm["rlisten"]['sends'][track]):
            cb = lambda: self.send_changestate(tid, track, sid, send, 1)
            self._lm["rlisten"]['sends'][track][send] = cb
            send.add_value_listener(cb)

    def add_retmixert_listener(self, tid, type, track):
        if not (track in self._lm["rlisten"][type]):
            cb = lambda: self.mixert_changestate(type, tid, track, 1)
            self._lm["rlisten"][type][track] = cb
            # ('solo', 'mute')
            try:
                if type == 'solo':
                    track.add_solo_listener(cb)
                elif type =='mute':
                    track.add_mute_listener(cb)
            except AttributeError as e:
                self.log_message(logging.ERROR, f"MCLM.add_retmixert_listener: unable to add track {type} listener {cb}")

    def add_retmixerv_listener(self, tid, type, track):
        if not (track in self._lm["rlisten"][type]):
            cb = lambda: self.mixerv_changestate(type, tid, track, 1)
            self._lm["rlisten"][type][track] = cb
            # ('volume', 'panning')
            try:
                if type == 'volume':
                    track.mixer_device.volume.add_value_listener(cb)
                elif type == 'panning':
                    track.mixer_device.panning.add_value_listener(cb)
            except AttributeError as e:
                self.log_message(logging.ERROR, f"MCLM.add_retmixerv_listener: unable to add track mixer {type} listener {cb}")

    # Track name listener
    def add_trname_listener(self, tid, track, ret=0):
        cb = lambda: self.trname_changestate(tid, track, ret)
        if ret == 1:
            if not (track in self._lm["rlisten"]['name']):
                self._lm["rlisten"]['name'][track] = cb
        elif not (track in self._lm["mlisten"]['name']):
            self._lm["mlisten"]['name'][track] = cb
        track.add_name_listener(cb)

    def add_device_listeners(self):
        self.remove_device_listeners()
        # self.log_message(logging.DEBUG, "C4.add_device_listeners: removed any existing device_listeners")
        # self.do_add_device_listeners(self.song().tracks, 0)
        self.do_add_device_listeners(self.song().visible_tracks, 0)
        self.do_add_device_listeners(self.song().return_tracks, 1)
        self.do_add_device_listeners([self.song().master_track], 2)
        # self.log_message(logging.DEBUG, "LM.add_device_listeners: added all track device_listeners types 0, 1, 2")

    def remove_device_listeners(self):
        for pr in self._lm["prlisten"]:
            self.remove_param_value_listener(pr)

        for tr in self._lm["dlisten"]:
            self.remove_track_device_listener(tr)

        for de in self._lm["plisten"]:
            self.remove_device_params_listener(de)

        self.clear_device_listener_keys()
        return
    
    def remove_param_value_listener(self, pr):
        if liveobj_valid(pr) and self.has_param_value_listener(pr):
            ocb = self._lm["prlisten"][pr] # ocb == old callback (function reference)
            # self.log_message(logging.DEBUG, f"LM.remove_param_value_listener: removing parameter {pr.name} value listener")
            if pr.value_has_listener(ocb):
                pr.remove_value_listener(ocb)

    def remove_device_params_listener(self, de):
        if liveobj_valid(de) and self.has_device_parameters_listener(de):
            ocb = self._lm["plisten"][de]
            # self.log_message(logging.DEBUG, f"LM.remove_device_params_listener: removing device {de.name} parameters listener")
            if de.parameters_has_listener(ocb):
                de.remove_parameters_listener(ocb)

    def remove_track_device_listener(self, tr):
        if liveobj_valid(tr) and self.has_track_device_listener(tr):
            ocb = self._lm["dlisten"][tr]
            # self.log_message(logging.DEBUG, f"LM.remove_track_device_listener: removing track {tr.name} device listener)
            if tr.view.selected_device_has_listener(ocb):
                tr.view.remove_selected_device_listener(ocb)
            if tr.devices_has_listener(ocb):
                tr.remove_devices_listener(ocb)

    def do_add_device_listeners(self, tracks, type=0):
        # log_id = "LM.do_add_device_listeners: "
        for i in range(len(tracks)):
            track = tracks[i]
            self.add_track_device_listener(track, i, type)
            # tt = "regular" if type == 0 else f"unknown type {type} "
            # tt = "return" if type == 1 else tt
            # tt = "master" if type == 2 else tt
            # self.log_message(logging.DEBUG, f"{log_id}added device listener (device_changestate) for <{tt}> track type {track.name}")
            # "last changed parameter inc/dec" behavior only needs listeners on the current selected device, not all devices on all visible tracks
            # if len(track.devices) >= 1:
            #     self.do_add_parameters_listeners(track, i, type)

    def do_add_parameters_listeners(self, track, tid=0, type=0):
        # log_id = "LM.do_add_parameters_listeners: "
        track_devices = track.devices
        extended_device_list = self.get_device_list(track_devices)
        # self.log_message(logging.DEBUG, f"{log_id}standard device count {len(track_devices)} extended device count <{len(extended_device_list)}>")
        self.do_add_track_devices_listeners(extended_device_list, tid, type, track.name)

    def do_add_track_devices_listeners(self, device_list, tid=0, type=0, track_name=""):
        for j in range(len(device_list)):
            device = device_list[j]
            self.do_add_one_devices_listeners(device, j, tid, type, track_name)

    def do_add_one_devices_listeners(self, device, did=0, tid=0, type=0, track_name=""):
        # log_id = "LM.do_add_one_devices_listeners: "
        self.add_device_parameters_listener(device)
        dtls = f"listener for track {track_name} device {device.name}"
        # self.log_message(logging.DEBUG, f"{log_id}added device parameters {dtls} devpm_change")
        self.do_add_parameter_value_listeners(device, tid, did, type, dtls)

    def do_add_parameter_value_listeners(self, device, tid=0, did=0, type=0, log_dtls=""):
        # log_id = "LM.do_add_parameter_value_listeners: "
        param_count = len(device.parameters)
        if param_count >= 1:
            for k in range(param_count):
                par = device.parameters[k]
                self.add_param_value_listener(par, tid, did, k, type)
                # self.log_message(logging.DEBUG, f"{log_id}added device parameter {log_dtls} parameter {par.name} param_changestate")

    def add_track_device_listener(self, track, tid=0, type=0):
        """Although the last 2 optional input values here get populated (have meaning) when this add method is called, see chain of """ \
        """do_add_track_device_listener methods above, The lambda callback method selected_device_change_state is only ever called back with the one """ \
        """required input param, never any of the optional parameters"""
        # """for each track input, tid value is relative to the type value.
        #    for type 0: tid == self.song().tracks.index
        #    for type 1: tid == self.song().return_tracks.index
        #    for type 2: tid == self.song().master_track.index (always 0)"""
        dtls = f"track <{track.name}> tidx <{tid}> type <{type}>"
        # if self.has_track_device_listener(track):
        #     self.remove_track_device_listener(track)
        cb = lambda: self.selected_device_change_state(track, tid, type)
        self.log_message(self.__my_log_levels["TRACE"], "LM.add_track_device_listener: input " + dtls)
        if track.view.selected_device_has_listener(cb):
            track.view.remove_selected_device_listener(cb)

        # track.add_devices_listener(cb)
        track.view.add_selected_device_listener(cb)
        self._lm["dlisten"][track] = cb
        # self.log_message(logging.DEBUG, "LM.add_track_device_listener: callback added for selected_device_listener with details: " + dtls)

    def has_track_device_listener(self, track):
        return True if track in self._lm["dlisten"] else False

    def add_device_parameters_listener(self, device):
        if self.has_device_parameters_listener(device):
            self.remove_device_params_listener(device)
        cb = lambda: self.devpm_change(device)
        if device.parameters_has_listener(cb):
            device.remove_parameters_listener(cb)

        device.add_parameters_listener(cb)
        self._lm["plisten"][device] = cb

    def has_device_parameters_listener(self, device):
        return True if device in self._lm["plisten"] else False

    def add_param_value_listener(self, param, tid=0, did=0, pid=0, type=0):
        """Although the last 4 optional input values here get populated (have meaning) when this add method is called, see chain of """ \
        """do_add_param_value_listener methods above, The lambda callback method param_changestate is only ever called back with the one """ \
        """required input param, never any of the optional parameters"""
        # for each parameter input, tid value is relative to the type value (as above)
        #    for type 0: tid == self.song().tracks.index
        #    for type 1: tid == self.song().return_tracks.index
        #    for type 2: tid == self.song().master_track.index (always 0)
        #    the did value is relative to the tid, and pid is relative to did
        if self.has_param_value_listener(param):
            self.remove_param_value_listener(param)
        cb = lambda: self.param_changestate(param, tid, did, pid, type)
        if param.value_has_listener(cb):
            param.remove_value_listener(cb)

        param.add_value_listener(cb)
        self._lm["prlisten"][param] = cb

    def has_param_value_listener(self, param):
        return True if param in self._lm["prlisten"] else False


    def add_tracks_listener(self):
        try:
            self.song().add_tracks_listener(self.tracks_change)
        except RuntimeError:
            pass

    def rem_tracks_listener(self):
        try:
            self.song().remove_tracks_listener(self.tracks_change)
        except RuntimeError:
            pass

    def add_overdub_listener(self):
        try:
            self.song().add_overdub_listener(self.overdub_change)
        except RuntimeError:
            pass

    def rem_overdub_listener(self):
        try:
            self.song().remove_overdub_listener(self.overdub_change)
        except RuntimeError:
            pass

    def add_transport_listener(self):
        # try-except blocks handle the cases when the song.is_playing_listener callback method self.transport_change is already present.
        try:
            self.song().add_is_playing_listener(self.transport_change)
        except RuntimeError:
            pass

    def rem_transport_listener(self):
        # try-except blocks handle the cases when the song.is_playing_listener callback method self.transport_change is already not present.
        try:
            self.song().remove_is_playing_listener(self.transport_change)
        except RuntimeError:
            pass

    def add_scene_listeners(self):
        # try-except blocks handle the cases when the song-view-listener callback method self.scene_change, for example, is already present. This reduces
        # the number of function calls at the expense of using exception handling semantics for relatively normal program event handling.
        try:
            self.song().view.add_selected_scene_listener(self.scene_change)
        except RuntimeError:
            pass

        try:
            self.song().view.add_selected_track_listener(self.track_change)
        except RuntimeError:
            pass

    def has_scene_listeners(self):
        return self.song().view.has_selected_scene_listener(self.scene_change) and self.song().view.has_selected_track_listener(self.track_change)

    def rem_scene_listeners(self):
        # try-except blocks handle the cases when the song-view-listener (callback method self.scene_change, for example) is already not present.
        try:
            self.song().view.remove_selected_scene_listener(self.scene_change)
        except RuntimeError:
            pass

        try:
            self.song().view.remove_selected_track_listener(self.track_change)
        except RuntimeError:
            pass