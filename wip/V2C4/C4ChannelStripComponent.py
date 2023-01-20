
from .V2C4Component import *

from _Framework.MixerComponent import ChannelStripComponent, release_control
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ButtonElement import ButtonElement
from _Framework.Util import nop


class C4ChannelStripComponent(ChannelStripComponent, V2C4Component):
    """
        ChannelStrip customization for displaying data on LCD screen
    """
    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)
        # self._update_callback = None
        self._data_display = None
        self._static_display = None

        self._track_name_label = 'Track Name'.center(int(LCD_BOTTOM_ROW_OFFSET/2))
        self._device_name_label = 'Device Name'.center(int(LCD_BOTTOM_ROW_OFFSET/2))

        self._track_name_static_ds = DisplayDataSource(separator='|')
        self._device_name_static_ds = DisplayDataSource()
        self._track_name_static_ds.set_display_string(self._track_name_label)
        self._device_name_static_ds.set_display_string(self._device_name_label)
        self.static_data_sources = [self._track_name_static_ds, self._device_name_static_ds]

        ChannelStripComponent.__init__(self)
        return

    def disconnect(self):
        ChannelStripComponent.disconnect(self)
        # self._update_callback = None
        self._data_display = None
        self._static_display = None
        return

    def set_script_handle(self, main_script):
        self._set_script_handle(main_script)

    #
    # def set_update_callback(self, callback):
    #     # pops if callback function arg does NOT contain an attribute named im_func
    #     # How is this different from using assert callable(callback)?
    #     # classes are callable as are instances implementing a __call__() method
    #     assert callback is None or dir(callback).count('im_func') is 1
    #     self._update_callback = callback
    #     return

    # def update(self):
    #     # self._log_message("updating ChannelStripComponent")
    #     super(C4ChannelStripComponent, self).update()
    #     if self._update_callback is not None:
    #         self._log_message("running _update_callback()")
    #         self._update_callback()
    #     return

    def set_pan_control(self, control):
        if control != self._pan_control:
            release_control(self._pan_control)
            self._pan_control = control
            self.update()

    def set_volume_control(self, control):
        if control != self._volume_control:
            # self._log_message("releasing volume control<{}>".format(self._volume_control.name))
            release_control(self._volume_control)
            self._volume_control = control
            # self._log_message("setting volume control<{}>".format(self._volume_control.name))
            self.update()
            # self._log_message("strip updated")

    def _update_track_name_data_source(self):
        # see super(C4ChannelStripComponent, self)._update_track_name_data_source()
        self._track_name_data_source.set_display_string(
            self._track.name if self._track is not None else ' None Track ')
        self._track_name_static_ds.set_display_string(
            self._track_name_label if self._track is not None else ' Track label ')
        self._device_name_static_ds.set_display_string(
            self._device_name_label if self._track is not None and
                                       self._track.view is not None and
                                       self._track.view.selected_device is not None else ' Device Label ')

        return

    def set_displays(self, display, device_name_data_source):
        assert isinstance(display, dict)
        assert list(display.keys())[0] == LCD_ANGLED_ADDRESS
        assert isinstance(display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement)

        self._static_display = display[LCD_ANGLED_ADDRESS][LCD_TOP_ROW_OFFSET]
        self._static_display.set_data_sources(self.static_data_sources)

        self._data_display = display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET]
        data_sources = [self._track_name_data_source, device_name_data_source]
        self._data_display.set_data_sources(data_sources)
        self.update()
        return

