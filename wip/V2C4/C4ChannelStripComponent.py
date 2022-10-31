
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from _Framework.MixerComponent import ChannelStripComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.ButtonElement import ButtonElement


from .C4_DEFINES import *


class C4ChannelStripComponent(ChannelStripComponent):
    """
    combination of Axiom Displaying and Notifying Mixer Component code
    except just for the selected track
    This class handles Track Mute and Solo as well as notifying observers when parameters are reassigned"""
    __module__ = __name__

    def __init__(self, mixer):
        ChannelStripComponent.__init__(self)
        assert isinstance(mixer, MixerComponent)
        self._mixer = mixer
        self._update_callback = None
        self._display = None
        self._register_timer_callback(self._on_timer)
        return

    def disconnect(self):
        ChannelStripComponent.disconnect(self)
        self._update_callback = None
        self._unregister_timer_callback(self._on_timer)
        self._display = None
        return

    def on_selected_track_changed(self):
        if self.song().view.selected_track != self._track:
            self.set_track(self.song().view.selected_track)
            ChannelStripComponent.on_selected_track_changed(self)

    def set_update_callback(self, callback):
        assert callback is None or dir(callback).count('im_func') is 1
        self._update_callback = callback
        return

    def update(self):
        super(C4ChannelStripComponent, self).update()
        if self._update_callback is not None:
            self._update_callback()
        return

    def set_display(self, display):
        assert isinstance(display, PhysicalDisplayElement)
        self._display = display

    def _on_timer(self):

        if self.track is not None:
            found_recording_clip = False
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            for track in tracks:
                if track.can_be_armed and track.arm:
                    if check_arrangement:
                        found_recording_clip = True
                        break
                    else:
                        playing_slot_index = track.playing_slot_index
                        if playing_slot_index in range(len(track.clip_slots)):
                            slot = track.clip_slots[playing_slot_index]
                            if slot.has_clip and slot.clip.is_recording:
                                found_recording_clip = True
                                break

            if not found_recording_clip:
                if song.exclusive_arm:
                    for track in tracks:
                        if track.can_be_armed and track.arm and track != self.track:
                            track.arm = False

                self.track.arm = True
                self.track.view.select_instrument()
        return
