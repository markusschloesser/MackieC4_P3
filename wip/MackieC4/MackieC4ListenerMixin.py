
import logging

from ableton.v2.base import liveobj_valid, depends
from .consts import *  # importing sys from the import in .consts via the * (everything)


if sys.version_info[0] >= 3:  # Python 3.x+ (Live 11+)
    from builtins import range

logger = logging.getLogger(__name__)

class MackieC4ListenerMixin(object):
    """This Mackie C4 Mixin class implements all dictionary based Listener mapping behavior"""
    
    __module__ = __name__

    @depends(encoder_controller=None)
    def __init__(self, encoder_controller=None):
                
        self._lm = {}   # lm == listener mappings
        # needed because self.__encoder_controller resolves here, MackieC4ListenerMixin, not MackieC4 where "public" methods like self.song() resolve
        self.__my_ec_ref = encoder_controller

        self._mixer_master_keys = ('volume', 'panning', 'crossfader')
        self._mixer_normal_track_keys_all = ('arm', 'solo', 'mute', 'is_frozen', 'current_monitoring_state', 'available_input_routing_channels',
                                         'available_input_routing_types', 'available_output_routing_channels',
                                         'available_output_routing_types', 'input_routing_channel', 'input_routing_type',
                                         'output_routing_channel', 'output_routing_type')
        self._mixer_normal_track_keys_in_use = ('arm', 'solo', 'mute', 'is_frozen')
        self._mixer_normal_strip_keys_in_use = ('volume', 'panning')
        self._mixer_return_track_keys_all = ('solo', 'mute', 'available_output_routing_channels', 'available_output_routing_types', 
                                        'output_routing_channel', 'output_routing_type')
        self._mixer_return_track_keys_in_use = ('solo', 'mute')
        self._mixer_return_strip_keys_in_use = ('volume', 'panning')
        self._initialize_listener_setup()


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
                if liveobj_valid(tr):
                    cb = self._lm["masterlisten"][type][tr]
                    cmd_pfx = f"tr.mixer_device.{type}"
                    test = eval(cmd_pfx + '.value_has_listener(cb)')
                    if test:
                        eval(cmd_pfx + '.remove_value_listener(cb)')

        # Normal Tracks
        for type in self._mixer_normal_track_keys_all:
            for tr in self._lm["mlisten"][type]:

                if liveobj_valid(tr):
                    cb = self._lm["mlisten"][type][tr]
                    if type == 'arm':
                        if tr.can_be_armed:
                            if tr.arm_has_listener(cb):
                                tr.remove_arm_listener(cb)

                    elif type == 'current_monitoring_state':
                        if tr.can_be_armed:
                            if tr.current_monitoring_state_has_listener(cb):
                                tr.remove_current_monitoring_state_listener(cb)
                    else:
                        cmd_hdr = f"tr.{type}"
                        cmd_tail = "_has_listener(cb)"
                        test = eval(cmd_hdr + cmd_tail)
                        if test:
                            cmd_hdr = f"tr.remove_{type}"
                            cmd_tail = "_listener(cb)"
                            eval(cmd_hdr + cmd_tail)

        for type in self._mixer_normal_strip_keys_in_use:
            for tr in self._lm["mlisten"][type]:
                if liveobj_valid(tr):
                    cb = self._lm["mlisten"][type][tr]
                    cmd_hdr = f"tr.mixer_device.{type}"
                    cmd_tail = ".value_has_listener(cb)"
                    test = eval(cmd_hdr + cmd_tail)
                    if test:
                        cmd_tail = ".remove_value_listener(cb)"
                        eval(cmd_hdr + cmd_tail)

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
                    cmd_hdr = f"tr.{type}"
                    cmd_tail = "_has_listener(cb)"
                    test = eval(cmd_hdr + cmd_tail)
                    if test:
                        cmd_hdr = f"tr.remove_{type}"
                        cmd_tail = "_listener(cb)"
                        eval(cmd_hdr + cmd_tail)

        for type in self._mixer_return_strip_keys_in_use:
            for tr in self._lm["rlisten"][type]:
                if liveobj_valid(tr):
                    cb = self._lm["rlisten"][type][tr]
                    cmd_hdr = f"tr.mixer_device.{type}"
                    cmd_tail = ".value_has_listener(cb)"
                    test = eval(cmd_hdr + cmd_tail)
                    if test:
                        cmd_tail = ".remove_value_listener(cb)"
                        eval(cmd_hdr + cmd_tail)

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
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 0)
            for type in self._mixer_normal_track_keys_in_use:
                if type == 'is_frozen':
                    if tr.can_be_frozen:
                        if tr.is_frozen_has_listener(self.on_is_frozen_changed):
                            tr.remove_is_frozen_listener(self.on_is_frozen_changed)
                        tr.add_is_frozen_listener(self.on_is_frozen_changed)
                if type == 'arm':
                    if tr.can_be_armed:
                        self.add_mixert_listener(track, type, tr)
                else:
                    self.add_mixert_listener(track, type, tr)

            for type in self._mixer_normal_strip_keys_in_use:
                self.add_mixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_send_listener(track, tr, sid, tr.mixer_device.sends[sid])

        tracks = self.song().return_tracks
        for track in range(len(tracks)):
            tr = tracks[track]
            self.add_trname_listener(track, tr, 1)
            for type in self._mixer_return_track_keys_in_use:
                self.add_retmixert_listener(track, type, tr)

            for type in self._mixer_return_strip_keys_in_use:
                self.add_retmixerv_listener(track, type, tr)

            for sid in range(len(tr.mixer_device.sends)):
                self.add_retsend_listener(track, tr, sid, tr.mixer_device.sends[sid])
                

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
            self._lm["mlisten"][type][track] = cb
            eval('track.add_' + type + '_listener(cb)')

    def add_mixerv_listener(self, tid, type, track):
        if not (track in self._lm["mlisten"][type]):
            cb = lambda: self.mixerv_changestate(type, tid, track)
            self._lm["mlisten"][type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

    def add_master_listener(self, tid, type, track):
        if not (track in self._lm["masterlisten"][type]):
            cb = lambda: self.mixerv_changestate(type, tid, track, 2)
            self._lm["masterlisten"][type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

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
            eval('track.add_' + type + '_listener(cb)')

    def add_retmixerv_listener(self, tid, type, track):
        if not (track in self._lm["rlisten"][type]):
            cb = lambda: self.mixerv_changestate(type, tid, track, 1)
            self._lm["rlisten"][type][track] = cb
            eval('track.mixer_device.' + type + '.add_value_listener(cb)')

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
        try:
            self.do_add_device_listeners(self.song().tracks, 0)
            self.do_add_device_listeners(self.song().return_tracks, 1)
            self.do_add_device_listeners([self.song().master_track], 2)
            # self.log_message(logging.DEBUG, "LM.add_device_listeners: added all track device_listeners types 0, 1, 2")
        except RuntimeError as re:
            # "Can't obtain live set at this time" for example, thrown from deep in the M4L_core scripting code, while "reloading" a recent session
            # _MxDCore\LomTypes.py", line 1073, in <lambda>
            msg = "LM.add_device_listeners: can't add any track device_listeners due to runtime exception: "
            if liveobj_valid(re.args):
                msg += str(re.args)
            else:
                msg += "unknown"
            self.log_message(logging.WARNING, msg)
            pass

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
            tt = "regular" if type == 0 else f"unknown type {type} "
            tt = "return" if type == 1 else tt
            tt = "master" if type == 2 else tt
            # self.log_message(logging.DEBUG, f"{log_id}added device listener (device_changestate) for <{tt}> track type {track.name}")
            if len(track.devices) >= 1:
                self.do_add_parameters_listeners(track, i, type)

    def do_add_parameters_listeners(self, track, tid=0, type=0):
        # log_id = "LM.do_add_parameters_listeners: "
        track_devices = track.devices
        extended_device_list = self.__my_ec_ref.get_device_list(track_devices)
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
        """for each track input, tid value is relative to the type value. 
           for type 0: tid == self.song().tracks.index
           for type 1: tid == self.song().return_tracks.index
           for type 2: tid == self.song().master_track.index (always 0)"""
        # dtls = f"track <{track.name}> tidx <{tid}> type <{type}>"
        if self.has_track_device_listener(track):
            self.remove_track_device_listener(track)
        cb = lambda: self.device_changestate(track, tid, type)
        # self.log_message(logging.DEBUG, "LM.add_track_device_listener: input" + dtls)
        if track.devices_has_listener(cb):
            track.remove_devices_listener(cb)
        if track.view.selected_device_has_listener(cb):
            track.view.remove_selected_device_listener(cb)

        track.add_devices_listener(cb)
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
        """for each parameter input, tid value is relative to the type value (as above) 
           for type 0: tid == self.song().tracks.index
           for type 1: tid == self.song().return_tracks.index
           for type 2: tid == self.song().master_track.index (always 0)
           the did value is relative to the tid, and pid is relative to did"""
        if self.has_param_value_listener(param):
            self.remove_param_value_listener(param)
        cb = lambda: self.param_changestate(param, tid, did, pid, type)
        if param.value_has_listener(cb):
            param.remove_value_listener(cb)

        param.add_value_listener(cb)
        self._lm["prlisten"][param] = cb

    def has_param_value_listener(self, param):
        return True if param in self._lm["prlisten"] else False