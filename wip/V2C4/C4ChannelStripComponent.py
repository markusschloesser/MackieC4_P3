
from .V2C4Component import *

from _Framework.MixerComponent import ChannelStripComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.ButtonElement import ButtonElement


class C4ChannelStripComponent(ChannelStripComponent, V2C4Component):
    """
    combination of Axiom Displaying and Notifying Mixer Component code
    except just for the selected track
    This class handles Track Mute and Solo as well as notifying observers when parameters are reassigned """
    __module__ = __name__

    def __init__(self):
        V2C4Component.__init__(self)
        self._mixer = None
        self.selected_track = None
        self.selected_strip = None
        self._update_callback = None
        self._data_display = None
        self._static_display = None

        self._track_name_label = 'Track Name'.center(LCD_BOTTOM_ROW_OFFSET/2)
        self._device_name_label = 'Device Name'.center(LCD_BOTTOM_ROW_OFFSET/2)

        self._track_name_static_ds = DisplayDataSource(separator='|')
        self._device_name_static_ds = DisplayDataSource()
        self._track_name_static_ds.set_display_string(self._track_name_label)
        self._device_name_static_ds.set_display_string(self._device_name_label)
        self.static_data_sources = [self._track_name_static_ds, self._device_name_static_ds]

        ChannelStripComponent.__init__(self)
        # self._register_timer_callback(self._on_timer)
        return

    def disconnect(self):
        ChannelStripComponent.disconnect(self)
        self._update_callback = None
        # self._unregister_timer_callback(self._on_timer)
        self._data_display = None
        self._static_display = None
        self._mixer = None
        self.selected_track = None
        self.selected_strip = None
        return

    def set_script_handle(self, main_script):
        """ to log in Live's log from this class, for example, need to set this script """
        self._set_script_handle(main_script)

    def on_selected_track_changed(self):
        super(C4ChannelStripComponent, self).on_selected_track_changed()

        if self.selected_track != self.song().view.selected_track:
            # this C4 Channel Strip is not "known" to the mixer component
            self.selected_track = self.song().view.selected_track
            self.set_track(self.selected_track)
            self.selected_strip = self._mixer.selected_strip
            #
        return

    def set_mixer(self, mixer):
        assert isinstance(mixer, MixerComponent)
        self._mixer = mixer

    def set_update_callback(self, callback):
        # pops if callback function arg does NOT contain an attribute named im_func
        # How is this different from using assert callable(callback)?
        # classes are callable as are instances implementing a __call__() method
        assert callback is None or dir(callback).count('im_func') is 1
        self._update_callback = callback
        return

    def update(self):
        # self._log_message("updating ChannelStripComponent")
        super(C4ChannelStripComponent, self).update()
        if self._update_callback is not None:
            self._log_message("running _update_callback()")
            self._update_callback()
        return

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
        assert display.keys()[0] == LCD_ANGLED_ADDRESS
        assert isinstance(display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET], PhysicalDisplayElement)

        self._static_display = display[LCD_ANGLED_ADDRESS][LCD_TOP_ROW_OFFSET]
        self._static_display.set_data_sources(self.static_data_sources)

        self._data_display = display[LCD_ANGLED_ADDRESS][LCD_BOTTOM_ROW_OFFSET]
        data_sources = [self._track_name_data_source, device_name_data_source]
        self._data_display.set_data_sources(data_sources)
        return

    def _on_timer(self):

        # if self.track is not None:
        #     found_recording_clip = False
        #     song = self.song()
        #     tracks = song.tracks
        #     check_arrangement = song.is_playing and song.record_mode
        #     for track in tracks:
        #         if track.can_be_armed and track.arm:
        #             if check_arrangement:
        #                 found_recording_clip = True
        #                 break
        #             else:
        #                 playing_slot_index = track.playing_slot_index
        #                 if playing_slot_index in range(len(track.clip_slots)):
        #                     slot = track.clip_slots[playing_slot_index]
        #                     if slot.has_clip and slot.clip.is_recording:
        #                         found_recording_clip = True
        #                         break

            #  WTF1? disarm every unselected track every time the timer strobes
            # if not found_recording_clip:
            #     if song.exclusive_arm:
            #         for track in tracks:
            #             if track.can_be_armed and track.arm and track != self.track:
            #                 track.arm = False

                # WTF2? arm the selected track and show the instrument view every time the timer strobes?
                # self.track.arm = True
                # self.track.view.select_instrument()
        # WTF Notes: maybe this behavior could implement an alternative channel strip "arm takeover" mode
        return
