from __future__ import absolute_import, print_function, unicode_literals


def toggle_follow(self):
    self.song().view.follow_song = not self.song().view.follow_song


def toggle_loop(self):
    self.song().loop = not self.song().loop


# toggle arrange/session mode
def toggle_session_arranger_is_visible(self):
    if self.application().view.is_view_visible('Session'):
        if self.shift_is_pressed():
            self.application().view.focus_view('Session')
        else:
            self.application().view.hide_view('Session')
    elif self.shift_is_pressed():
        self.application().view.focus_view('Arranger')
    else:
        self.application().view.hide_view('Arranger')


def is_arranger_visible(self):
    return self.application().view.is_view_visible('Arranger')


# toggle clip / Device view
def toggle_detail_sub_view(self):
    if self.application().view.is_view_visible('Detail/Clip'):
        if self.shift_is_pressed():
            self.application().view.focus_view('Detail/Clip')
        else:
            self.application().view.show_view('Detail/DeviceChain')
    elif self.shift_is_pressed():
        self.application().view.focus_view('Detail/DeviceChain')
    else:
        self.application().view.show_view('Detail/Clip')


def toggle_browser_is_visible(self):
    if self.application().view.is_view_visible('Browser'):
        if self.shift_is_pressed():
            self.application().view.focus_view('Browser')
        else:
            self.application().view.hide_view('Browser')
    else:
        self.application().view.show_view('Browser')


def is_browser_visible(self):
    return self.application().view.is_view_visible('Browser')


# back to arrangement / BTA
def toggle_back_to_arranger(self, name='BTA'):
    self.song().back_to_arranger = not self.song().back_to_arranger


def any_soloed_track(self):
    tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    return bool(any(t.solo for t in tracks))


def unsolo_all(self):
    tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    for track in tracks:
        if track.solo:
            track.solo = False


def any_muted_track(self):
    tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    return bool(any(t.mute for t in tracks))


def unmute_all(self):
    tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    for track in tracks:
        if track.mute:
            track.mute = False


def redo(self):
    if self.song().can_redo:
        self.song().redo()


def undo(self):
    if self.song().can_undo:
        self.song().undo()


def any_armed_track(self):
    tracks = self.song().tracks
    return bool(any(track.can_be_armed and track.arm for track in tracks))


def unarm_all_button(self):
    tracks = self.song().tracks
    for track in tracks:
        if track.can_be_armed and (track.arm or track.implicit_arm):
            track.arm = False
