from .V2C4Component import *

from _Framework.MixerComponent import MixerComponent, izip_longest, turn_button_on_off
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ButtonElement import ButtonElement

from .C4ChannelStripComponent import C4ChannelStripComponent

if sys.version_info[0] >= 3:  # Live 11
    from itertools import zip_longest


class C4MixerComponent(MixerComponent, V2C4Component):
    """
        Mixer customization making use of C4ChannelStripComponent for displaying data on LCD screen.
        This mixer component follows the self.song().view.selected_track around, one "set" of
        track control elements always connects to the mixer's "selected channel strip" or None.
    """
    __module__ = __name__

    # need to declare listener methods to the "button event subjects" so we can send appropriate
    # button feedback LED ON or OFF signals.  Currently, each button press toggles the LED state more
    # or less independently of the button's associated parameter's state in Live.  We should just listen for
    # changes to the subject and "feedback" that change value to the LED.  If "track mute status" changed
    # for example, and now that "device parameter" is OFF, then send the OFF feedback value to the LED.

    def __init__(self, *a, **k):
        V2C4Component.__init__(self)
        self._selected_strip_volume_control = None
        self._selected_strip_pan_control = None
        self._selected_strip_send_controls = (None, )
        self._selected_strip_track_buttons = {'arm': None, 'solo': None, 'mute': None, 'activate': None}
        self._selected_track = None
        self._displays = {LCD_ANGLED_ADDRESS: {LCD_BOTTOM_ROW_OFFSET: None}}
        self._device_name_data_source = None

        MixerComponent.__init__(self, num_tracks=0, num_returns=0, auto_name=True, *a, **k)

    def disconnect(self):
        self._disconnect_selected_strip_controls()
        MixerComponent.disconnect(self)
        self._selected_strip_track_buttons['arm'] = None
        self._selected_strip_track_buttons['solo'] = None
        self._selected_strip_track_buttons['mute'] = None
        self._selected_strip_track_buttons['activate'] = None
        self._selected_strip_volume_control = None
        self._selected_strip_pan_control = None
        self._selected_strip_send_controls = (None, )
        self._selected_track = None
        self._displays = None 
        self._device_name_data_source = None

    def _create_strip(self):
        if self._script_backdoor_handle is not None:
            return C4ChannelStripComponent().set_script_handle(self._script_backdoor_handle)
        else:
            return C4ChannelStripComponent()

    def set_displays(self, display_rows, device_name_data_source):
        assert isinstance(display_rows, dict)
        assert list(display_rows.keys())[0] == LCD_ANGLED_ADDRESS
        assert isinstance(display_rows[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement)

        self._displays = display_rows
        self._device_name_data_source = device_name_data_source

    def on_selected_track_changed(self):
        self._disconnect_selected_strip_controls()
        MixerComponent.on_selected_track_changed(self)
        self._connect_selected_strip_controls()
        # self._selected_track != self.song().master_track
        # self._selected_track = self.song().view.selected_track

        if isinstance(self._displays[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement):
            self.selected_strip().set_displays(self._displays, self._device_name_data_source)
    
    def set_selected_strip_volume_control(self, control):
        name = control.name if control is not None else 'None'
        self._log_message("setting volume control<{}> on selected strip<{}>".format(name, self.selected_strip().name))
        self._selected_strip_volume_control = control
        self._set_selected_strip_volume_control()

    def _set_selected_strip_volume_control(self):
        self.selected_strip().set_volume_control(self._selected_strip_volume_control)

    def set_selected_strip_pan_control(self, control):
        name = control.name if control is not None else 'None'
        self._log_message("setting pan control<{}> on selected strip<{}>".format(name, self.selected_strip().name))
        self._selected_strip_pan_control = control
        self._set_selected_strip_pan_control()

    def _set_selected_strip_pan_control(self):
        self.selected_strip().set_pan_control(self._selected_strip_pan_control)

    def set_selected_strip_send_controls(self, controls):
        self._send_controls = controls
        if sys.version_info[0] >= 3:  # Live 11
            for control in zip_longest(controls or []):
                if self._send_index is None:
                    self._selected_strip_send_controls = (None,)
                else:
                    self._selected_strip_send_controls = (None,) * self._send_index + (control,)
        else:  # Live 10
            for control in izip_longest(controls or []):
                if self._send_index is None:
                    self._selected_strip_send_controls = (None, )
                else:
                    self._selected_strip_send_controls = (None, ) * self._send_index + (control,)

        self._set_selected_strip_send_controls()

    def _set_selected_strip_send_controls(self):
        if len(self._selected_strip_send_controls) > 0 and self._selected_strip_send_controls[0] is None:
            self.selected_strip().set_send_controls(None)
        else:
            self.selected_strip().set_send_controls(self._selected_strip_send_controls)

    def set_selected_strip_arm_button(self, button):
        if self._selected_strip_track_buttons['arm'] is None or self._selected_strip_track_buttons['arm'] != button:
            self._selected_strip_track_buttons['arm'] = button 
            self._set_selected_strip_arm_button()

    def _set_selected_strip_arm_button(self):
        if self.selected_strip().track == \
                self.song().view.selected_track and self.song().view.selected_track.can_be_armed:
            self.selected_strip().set_arm_button(self._selected_strip_track_buttons['arm'])
        else:
            self.selected_strip().set_arm_button(None)

    def set_selected_strip_solo_button(self, button):
        if self._selected_strip_track_buttons['solo'] is None or self._selected_strip_track_buttons['solo'] != button:
            self._selected_strip_track_buttons['solo'] = button 
            self._set_selected_strip_solo_button()

    def _set_selected_strip_solo_button(self):
        if self.selected_strip() != self.master_strip():
            self.selected_strip().set_solo_button(self._selected_strip_track_buttons['solo'])
        else:
            self.selected_strip().set_solo_button(None)

    def set_selected_strip_mute_button(self, button):
        if self._selected_strip_track_buttons['mute'] is None or self._selected_strip_track_buttons['mute'] != button:
            self._selected_strip_track_buttons['mute'] = button 
            self._set_selected_strip_mute_button()

    def _set_selected_strip_mute_button(self):
        if self.selected_strip() != self.master_strip():
            self.selected_strip().set_mute_button(self._selected_strip_track_buttons['mute'])
        else:
            self.selected_strip().set_mute_button(None)

    def set_selected_strip_activate_button(self, button):
        if self._selected_strip_track_buttons['activate'] is None or self._selected_strip_track_buttons['activate'] != button:
            self._selected_strip_track_buttons['activate'] = button 
            self._set_selected_strip_activate_button()

    def _set_selected_strip_activate_button(self):
        if self.selected_strip() != self.master_strip():
            self.selected_strip().set_select_button(self._selected_strip_track_buttons['activate'])
        else:
            self.selected_strip().set_select_button(None)

    def update(self):
        super(MixerComponent, self).update()
        if self._allow_updates:
            if self.is_enabled():
                self.selected_strip().update()
            else:
                map(lambda x: turn_button_on_off(x, on=False), [
                 self._selected_strip_track_buttons['arm'],
                 self._selected_strip_track_buttons['solo'],
                 self._selected_strip_track_buttons['mute'],
                 self._selected_strip_track_buttons['activate']])
        else:
            self._update_requests += 1
    
    def _connect_selected_strip_controls(self):
        self.selected_strip().set_script_handle(self._script_backdoor_handle)
        self._set_selected_strip_volume_control()
        self._set_selected_strip_pan_control()
        self._set_selected_strip_send_controls()
        self._set_selected_strip_arm_button()
        self._set_selected_strip_solo_button()
        self._set_selected_strip_mute_button()
        self._set_selected_strip_activate_button()

    def _disconnect_selected_strip_controls(self):
        self.selected_strip().set_volume_control(None)
        self.selected_strip().set_pan_control(None)
        self.selected_strip().set_send_controls(None)
        self.selected_strip().set_arm_button(None)
        self.selected_strip().set_solo_button(None)
        self.selected_strip().set_mute_button(None)
        self.selected_strip().set_select_button(None)

    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)
