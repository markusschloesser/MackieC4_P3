
from .V2C4Component import *
if sys.version_info[0] >= 3:  # Live 11
    from builtins import range, str

from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.ButtonElement import ButtonElement

from .C4_DEFINES import *


class C4MixerComponent(MixerComponent):
    """combination of Axiom Displaying and notifying Mixer Component code
    This class handles Track Mute and Solo as well as notifying observers when parameters are reassigned"""
    __module__ = __name__

    def __init__(self, num_tracks):
        self._update_callback = None
        MixerComponent.__init__(self, num_tracks)
        self._bank_display = None
        self._selected_tracks = []
        self._display = None
        self._mute_button = None
        self._solo_button = None
        self._register_timer_callback(self._on_timer)
        return

    def disconnect(self):
        MixerComponent.disconnect(self)
        self._update_callback = None
        self._unregister_timer_callback(self._on_timer)
        self._selected_tracks = None
        return

    def set_update_callback(self, callback):
        assert callback == None or dir(callback).count('im_func') is 1
        self._update_callback = callback
        return

    def set_bank_display(self, display):
        assert isinstance(display, PhysicalDisplayElement)
        self._bank_display = display


    def on_selected_track_changed(self):
        MixerComponent.on_selected_track_changed(self)
        selected_track = self.song().view.selected_track
        num_strips = len(self._channel_strips)
        if selected_track in self._tracks_to_use():
            track_index = list(self._tracks_to_use()).index(selected_track)
            new_offset = track_index - track_index % num_strips
            assert new_offset / num_strips == int(new_offset / num_strips)
            self.set_track_offset(new_offset)

    def update(self):
        super(C4MixerComponent, self).update()
        if self._update_callback != None:
            self._update_callback()
        return

    def _tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _reassign_tracks(self):
        MixerComponent._reassign_tracks(self)
        if self._update_callback != None:
            self._update_callback()
        return

    def _bank_up_value(self, value):
        old_offset = int(self._track_offset)
        MixerComponent._bank_up_value(self, value)
        if self._bank_display != None:
            if value != 0 and old_offset != self._track_offset:
                min_track = self._track_offset + 1
                max_track = min(len(self._tracks_to_use()), min_track + len(self._channel_strips))
                self._bank_display.display_message("Tracks {} - {}".format(min_track, max_track))
            else:
                self._bank_display.update()
        return

    def _bank_down_value(self, value):
        old_offset = int(self._track_offset)
        MixerComponent._bank_down_value(self, value)
        if self._bank_display != None:
            if value != 0 and old_offset != self._track_offset:
                min_track = self._track_offset + 1
                max_track = min(len(self._tracks_to_use()), min_track + len(self._channel_strips))
                self._bank_display.display_message("Tracks {} - {}".format(min_track, max_track))
            else:
                self._bank_display.update()
        return

    def set_display(self, display):
        assert isinstance(display, PhysicalDisplayElement)
        self._display = display

    def set_solo_button(self, button):
        assert button == None or isinstance(button, ButtonElement) and button.is_momentary()
        self.selected_strip().set_solo_button(button)
        if self._solo_button != button:
            if self._solo_button != None:
                self._solo_button.remove_value_listener(self._solo_value)
            self._solo_button = button
            if self._solo_button != None:
                self._solo_button.add_value_listener(self._solo_value)
            self.update()
        return

    def set_mute_button(self, button):
        assert button == None or isinstance(button, ButtonElement) and button.is_momentary()
        self.selected_strip().set_mute_button(button)
        if self._mute_button != button:
            if self._mute_button != None:
                self._mute_button.remove_value_listener(self._mute_value)
            self._mute_button = button
            if self._mute_button != None:
                self._mute_button.add_value_listener(self._mute_value)
            self.update()
        return

    def _on_timer(self):
        sel_track = None
        while len(self._selected_tracks) > 0:
            track = self._selected_tracks[(-1)]
            if track != None and track.has_midi_input and track.can_be_armed and not track.arm:
                sel_track = track
                break
            del self._selected_tracks[-1]

        if sel_track != None:
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
                        if track.can_be_armed and track.arm and track != sel_track:
                            track.arm = False

                sel_track.arm = True
                sel_track.view.select_instrument()
        self._selected_tracks = []
        return

    def _solo_value(self, value):
        assert self._solo_button != None
        assert value in range(MIDI_DATA_LAST_VALID + 1)
        if self._display != None and self.song().view.selected_track not in (
         self.song().master_track,
         None):
            if value != 0:
                track = self.song().view.selected_track
                display_string = str(track.name) + ': Solo '
                if track.solo:
                    display_string += 'On'
                else:
                    display_string += 'Off'
                self._display.display_message(display_string)
            else:
                self._display.update()
        return

    def _mute_value(self, value):
        assert self._mute_button != None
        assert value in range(MIDI_DATA_LAST_VALID + 1)
        if self._display != None and self.song().view.selected_track not in (
         self.song().master_track,
         None):
            if value != 0:
                track = self.song().view.selected_track
                display_string = str(track.name) + ': Mute '
                if track.mute:
                    display_string += 'On'
                else:
                    display_string += 'Off'
                self._display.display_message(display_string)
            else:
                self._display.update()
        return

    def _next_track_value(self, value):
        MixerComponent._next_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)

    def _prev_track_value(self, value):
        MixerComponent._prev_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)