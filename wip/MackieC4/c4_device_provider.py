
import Live

from ableton.v2.base import liveobj_valid, listens
from ableton.v2.control_surface.device_provider import DeviceProvider, device_to_appoint


class C4DeviceProvider(DeviceProvider):

    def __init__(self, song=None, *a, **k):
        super(C4DeviceProvider, self).__init__(song, *a, **k)
        self._last_change_details = {}
        self.clear_last_param_details()
        self._selected_track = None

    def set_last_param_value_change_details(self, param, tid=0, did=0, pid=0):
        if liveobj_valid(param):
            self.clear_last_param_details()
            self._last_change_details["parameter"] = param
            # self.canonical_parent.log_message(f"C4DeviceProvider.set_last_param_value_change_details: name <{param.name}> orig <{param.original_name}> val <{param.value}")
            self._last_change_details["parameterName"] = param.original_name # param.name if param.original_name.starts_with("Macro") else
            self._last_change_details["trackId"] = tid
            self._last_change_details["deviceId"] = did
            self._last_change_details["parameterId"] = pid

    def clear_last_param_details(self):
        self._last_change_details["parameter"] = {}
        self._last_change_details["parameterName"] = {}
        self._last_change_details["trackId"] = {}
        self._last_change_details["deviceId"] = {}
        self._last_change_details["parameterId"] = {}

    def get_last_param_value_change_details(self):
        return self._last_change_details

    def get_last_param_value_change_name(self):
        return self._last_change_details["parameterName"]

    @property
    def provided_device(self):
        return self._device

    @property
    def surface_is_locked(self):
        return self._locked_to_device

    @property
    def device_track(self):
        return self._selected_track

    def on_update_display_timer(self):
        pass

    def destroy(self):
        self._device = None
        self._locked_to_device = False
        self._last_change_details = None

    def _update_appointed_device(self):
        super()._update_appointed_device()
        self.clear_last_param_details()
        # self.canonical_parent.log_message("C4DeviceProvider._update_appointed_device: invoked super")

    def update_device_selection(self):
        super().update_device_selection()
        self.canonical_parent.log_message("C4DeviceProvider.update_device_selection: clearing last param details")
        self.clear_last_param_details()

        view = self.song.view
        track_or_chain = view.selected_chain if view.selected_chain else view.selected_track
        if isinstance(track_or_chain, Live.Track.Track):
            self._selected_track = track_or_chain
            self.canonical_parent.log_message(f"C4DeviceProvider.update_device_selection: updating self._selected_track to {track_or_chain.name}")
