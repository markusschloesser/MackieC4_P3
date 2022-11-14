from .V2C4Component import *

from _Framework.MixerComponent import ChannelStripComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ButtonElement import ButtonElement

from .C4ChannelStripComponent import C4ChannelStripComponent

class C4MixerComponent(MixerComponent, V2C4Component):
    """
        Mixer customization making use of C4ChannelStripComponent for displaying data on LCD screen
    """
    __module__ = __name__

    def __init__(self, *a, **k):
        V2C4Component.__init__(self)
        self._displays = {LCD_ANGLED_ADDRESS: {LCD_BOTTOM_ROW_OFFSET: None}}
        self._device_name_data_source = None

        MixerComponent.__init__(self, num_tracks=1, *a, **k)

    def disconnect(self):
        MixerComponent.disconnect(self)
        self._displays = None
        self._device_name_data_source = None

    def _create_strip(self):
        return C4ChannelStripComponent()

    def set_displays(self, display_rows, device_name_data_source):
        assert isinstance(display_rows, dict)
        assert display_rows.keys()[0] == LCD_ANGLED_ADDRESS
        assert isinstance(display_rows[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement)

        self._displays = display_rows
        self._device_name_data_source = device_name_data_source

    def on_selected_track_changed(self):
        MixerComponent.on_selected_track_changed(self)
        if isinstance(self._displays[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement):
            self.selected_strip().set_displays(self._displays, self._device_name_data_source)

    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)
