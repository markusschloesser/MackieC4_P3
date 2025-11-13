
from ableton.v2.control_surface.device_provider import DeviceProvider


class C4DeviceProvider(DeviceProvider):

    def __init__(self, song=None, *a, **k):
        super(C4DeviceProvider, self).__init__(song, *a, **k)

    def on_update_display_timer(self):
        pass

    def destroy(self):
        self._device = None
        self._locked_to_device = False