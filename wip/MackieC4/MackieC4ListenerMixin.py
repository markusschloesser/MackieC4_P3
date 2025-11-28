
import logging

from ableton.v2.base import liveobj_valid
from .consts import *  # importing sys from the import in .consts via the * (everything)


if sys.version_info[0] >= 3:  # Python 3.x+ (Live 11+)
    from builtins import str
    from builtins import range

logger = logging.getLogger(__name__)

class MackieC4ListenerMixin(object):
    """This Mackie C4 Mixin class implements all dictionary based Listener mapping behavior"""
    
    __module__ = __name__

    def __init__(self):
        super().__init__()
        
        self._lm = {}   # lm == listener mappings

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
        # self.log_message("C4.add_device_listeners: removed any existing device_listeners")
        self.do_add_device_listeners(self.song().tracks, 0)
        self.do_add_device_listeners(self.song().return_tracks, 1)
        self.do_add_device_listeners([self.song().master_track], 2)
        # self.log_message("LM.add_device_listeners: added all track device_listeners types 0, 1, 2")

    def do_add_device_listeners(self, tracks, type):
        for i in range(len(tracks)):
            self.add_device_listener(tracks[i], i, type)
            # self.log_message("LM.do_add_device_listeners: for track type <{0}>".format(type))
            if len(tracks[i].devices) >= 1:
                for j in range(len(tracks[i].devices)):
                    self.add_devpmlistener(tracks[i].devices[j])
                    param_count = len(tracks[i].devices[j].parameters)
                    # self.log_message("LM.do_add_device_listeners: adding <{0}> device parameter listeners".format(param_count))
                    if param_count >= 1:
                        for k in range(len(tracks[i].devices[j].parameters)):
                            par = tracks[i].devices[j].parameters[k]
                            self.add_paramlistener(par, i, j, k, type)

    def add_device_listener(self, track, tid, type):
        dtls = f"track <{track.name}> tidx <{tid}> type <{type}>"
        cb = lambda: self.device_changestate(track, tid, type)
        # self.log_message("LM.add_device_listener: input" + dtls)
        if not (track in self._lm["dlisten"]):
            track.add_devices_listener(cb)
            track.view.add_selected_device_listener(cb)
            # self.log_message("LM.add_device_listener: callback added for selected_device_listener with details: " + dtls)
            self._lm["dlisten"][track] = cb


    def remove_device_listeners(self):
        for pr in self._lm["prlisten"]:
            if liveobj_valid(pr):
                ocb = self._lm["prlisten"][pr]
                # self.log_message("LM.remove_device_listeners: removing parameter value listeners")
                if pr.value_has_listener(ocb):
                    pr.remove_value_listener(ocb)

        for tr in self._lm["dlisten"]:
            if liveobj_valid(tr):
                ocb = self._lm["dlisten"][tr]
                # self.log_message("LM.remove_device_listeners: removing track device listeners)
                if tr.view.selected_device_has_listener(ocb):
                    tr.view.remove_selected_device_listener(ocb)

        for de in self._lm["plisten"]:
            if liveobj_valid(de):
                ocb = self._lm["plisten"][de]
                # self.log_message("LM.remove_device_listeners: removing device parameters listener")
                if de.parameters_has_listener(ocb):
                    de.remove_parameters_listener(ocb)

        self.clear_device_listener_keys()
        return


    def add_devpmlistener(self, device):  # devpmlistener is device parameters listener
        cb = lambda: self.devpm_change()
        if not (device in self._lm["plisten"]):
            device.add_parameters_listener(cb)
            self._lm["plisten"][device] = cb

    def devpm_change(self):
        self.refresh_state()

    def add_paramlistener(self, param, tid, did, pid, type):
        cb = lambda: self.param_changestate(param, tid, did, pid, type)
        if not (param in self._lm["prlisten"]):
            param.add_value_listener(cb)
            self._lm["prlisten"][param] = cb
