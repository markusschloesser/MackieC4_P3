from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from threading import Timer
import time
from functools import partial, wraps

from ableton.v2.base import liveobj_valid, find_if, const, depends

# methods taking song() input parameter
@depends(song_view=None)
def toggle_follow(song_view=None):
    song_view.follow_song = not song_view.follow_song


@depends(song=None)
def toggle_loop(song=None):
    song.loop = not song.loop

# back to arrangement / BTA
@depends(song=None)
def toggle_back_to_arranger(song=None):
    song.back_to_arranger = not song.back_to_arranger

@depends(song=None)
def redo(song=None):
    if song.can_redo:
        song.redo()

@depends(song=None)
def undo(song=None):
    if song.can_undo:
        song.undo()

def grouped_tracks(track, tracks=None):
    if not is_group_track(track):
        return []
    return flatten_tracks(filter(lambda t: group_track(t) == track, tracks))

def flatten_tracks(tracks):
    return chain(*((grouped_tracks(t) if is_group_track(t) else [t]) for t in tracks))

# methods taking track input
def any_armed_track(tracks):
    return bool(any(track.can_be_armed and track.arm for track in tracks))

def unarm_all_button(tracks):
    for track in tracks:
        if track.can_be_armed and (track.arm or track.implicit_arm):
            track.arm = False

def any_soloed_track(tracks):
    # tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    return bool(any(t.solo for t in tracks))

def unsolo_all(tracks):
    # tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    for track in tracks:
        if track.solo:
            track.solo = False

def any_muted_track(tracks):
    # tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    return bool(any(t.mute for t in tracks))

def unmute_all(tracks):
    # tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
    for track in tracks:
        if track.mute:
            track.mute = False

def is_group_track(track):
    if liveobj_valid(track):
        return track.is_foldable
    return False

def is_grouped(track):
    if liveobj_valid(track):
        return track.is_grouped
    return False

def group_track(track):
    if is_grouped(track):
        return track.group_track
    return False

def is_folded(track):
    if is_group_track(track):
        return track.fold_state
    return False

def toggle_fold(track):
    if is_group_track(track):
        track.fold_state = not track.fold_state
        return True
    elif is_grouped(track):
        toggle_fold(track.group_track)
    else:
        track.view.is_collapsed = not track.view.is_collapsed  # for collapsing tracks in Arrange view
    return False

def can_be_armed(track):
    if liveobj_valid(track):
        return track.can_be_armed
    return False

def arm(track):
    if can_be_armed(track):
        track.arm = True
        return True
    return False

def unarm(track):
    if can_be_armed(track):
        track.arm = False
        return True
    return False

def unarm_tracks(tracks):
    for track in tracks:
        unarm(track)

def tracks(tracks):
    return filter(liveobj_valid, tracks)

def visible_tracks(visible_tracks):
    return filter(liveobj_valid, visible_tracks)


def crossfade_toggle_value(selected_track, value='Mixer.Crossfade.Off'):
    if liveobj_valid(selected_track):
        nbr_choices = len(selected_track.mixer_device.crossfade_assignments.values)
        new_choice = nbr_choices - 1 if selected_track.mixer_device.crossfade_assign < 1 else selected_track.mixer_device.crossfade_assign - 1
        selected_track.mixer_device.crossfade_assign = new_choice % nbr_choices

# methods taking application.view input parameter (and a modifier value maybe)
def is_arranger_visible(app_view):
    return app_view.is_view_visible('Arranger')

def is_browser_visible(app_view):
    return app_view.is_view_visible('Browser')

# toggle arrange/session mode
def toggle_session_arranger_is_visible(app_view, modifier_pressed):
    if app_view.is_view_visible('Session'):
        if modifier_pressed:
            app_view.focus_view('Session')
        else:
            app_view.hide_view('Session')
    elif modifier_pressed:
        app_view.focus_view('Arranger')
    else:
        app_view.hide_view('Arranger')

# toggle clip / Device view
def toggle_detail_sub_view(app_view, modifier_pressed):
    if app_view.is_view_visible('Detail/Clip'):
        if modifier_pressed:
            app_view.focus_view('Detail/Clip')
        else:
            app_view.show_view('Detail/DeviceChain')
    elif modifier_pressed:
        app_view.focus_view('Detail/DeviceChain')
    else:
        app_view.show_view('Detail/Clip')

def toggle_browser_is_visible(app_view, modifier_pressed):
    if app_view.is_view_visible('Browser'):
        if modifier_pressed:
            app_view.focus_view('Browser')
        else:
            app_view.hide_view('Browser')
    else:
        app_view.show_view('Browser')


# methds taking device and paramater input
# method from ableton.v3.live.util.get_parameter_by_name()
# except matching on "current" names
def get_parameter_by_name(name, device):
    if liveobj_valid(device):
        return find_if((lambda p: p.name == name and liveobj_valid(p) and p.is_enabled), device.parameters)

def toggle_or_cycle_parameter_value(parameter):
    if liveobj_valid(parameter):
        if parameter.is_quantized:
            if parameter.value + 1 > parameter.max:
                parameter.value = parameter.min
            else:
                parameter.value = parameter.value + 1
        else:
            parameter.value = parameter.max if parameter.value == parameter.min else parameter.min

def update_or_cycle_parameter_value(parameter, increment_amount, option_is_pressed=False):
    """adds an incremental value to the input prarameter's current value, optionally wrapping around the min and max boundary values"""
    if liveobj_valid(parameter):
        new_value = parameter.value + increment_amount
        if new_value > parameter.max:
            if option_is_pressed:
                new_value = parameter.min
            else:
                new_value = parameter.max
        elif new_value < parameter.min:
            if option_is_pressed:
                new_value = parameter.max
            else:
                new_value = parameter.min
        parameter.value = new_value

# unicode of Python2 is equivalent to str in Python3, so you can also write: str(text, 'utf-8') to get ascii text
# Assuming that text is a bytes object, just use text.decode('utf-8')
class EncoderDisplaySegment(object):
    """ Represents the text to display on the LCD over ONE encoder of the Mackie C4 """
    __module__ = __name__

    def __init__(self, vpot_index):
        self.__vpot_index = vpot_index
        # self.__vpot_cc_nbr = vpot_index + C4SID_VPOT_CC_ADDRESS_BASE

        self.__upper_text = ''.join(' ' for x in range(7))  # '       '
        self.__lower_text = ''.join(' ' for x in range(7))  # '       '
        self.__upper_alt_text = ''.join('-' for x in range(6)) + '|'  # '------|'
        self.__lower_alt_text = ''.join('-' for x in range(6)) + '|'  # '------|'

        return

    @property
    def display_segment_index(self):
        """The zero based index (0 - 31) of the LCD screen space over the encoder at the same index"""
        return self.__vpot_index

    def is_index_match(self, test_index):
        if test_index == self.__vpot_index:
            return True
        else:
            return False

    def set_text(self, lower, upper):  # lower first in param list supports refactoring
        self.set_lower_text(lower)
        self.set_upper_text(upper)

    def clear_text(self):
        self.__upper_text = ''.join(' ' for x in range(7))  # '       '
        self.__lower_text = ''.join(' ' for x in range(7))  # '       '

    def set_lower_text(self, lower):
        self.__lower_text = lower

    def set_lower_text_and_alt(self, lower, alt_txt):
        self.set_lower_text(lower)
        self.__lower_alt_text = alt_txt

    def set_upper_text(self, upper):
        self.__upper_text = upper

    def set_upper_text_and_alt(self, upper, alt_txt):
        self.set_upper_text(upper)
        self.__upper_alt_text = alt_txt

    def get_upper_text(self):
        return self.__upper_text

    def alter_upper_text(self, alter_text=True):
        if alter_text:
            return self.__upper_alt_text
        else:
            return self.__upper_text

    def get_lower_text(self):
        if not liveobj_valid(self.__lower_text):
            return "xxXXxx"
        else:
            return str(self.__lower_text)

    def alter_lower_text(self, alter_text=True):
        if alter_text:
            return self.__lower_alt_text
        else:
            return self.get_lower_text()


class TimeDisplay(object):

    @depends(smpt_format=(const(None)))
    def __init__(self, smpt_format=None):
        self.__show_beat_time = False
        self.__smpt_format = smpt_format
        # self.__last_send_time = []
        self._show_beats()

    @property
    def show_beat_time(self):
        return self.__show_beat_time

    @property
    def smpt_format(self):
        return self.__smpt_format

    def toggle_mode(self):
        if self.show_beat_time:
            self._show_smpte(self.__smpt_format)
        else:
            self._show_beats()

    def _show_beats(self):
        self.__show_beat_time = True

    def _show_smpte(self, smpte_mode):
        self.__show_beat_time = False
        self.__smpt_format = smpte_mode

    # def refresh_state(self):
    #     self._show_beats()
    #     self.__last_send_time = []

    # @depends(song=(const(None)))
    # def on_update_display_timer(self, song=None):
    #     if self.show_beat_time:
    #         time_string = str(song().get_current_beats_song_time())
    #     else:
    #         time_string = str(song().get_current_smpte_song_time(self.__smpt_format))
    #     time_string = [c for c in time_string if c not in ('.', ':')]
    #     if self.__last_send_time != time_string:
    #         self.__last_send_time = time_string
    #         self.__send_time_string(time_string, show_points=True)
    #
    # @staticmethod
    # def __send_time_string(time_string, show_points):
    #     for c in range(0, 10):
    #         char = time_string[9 - c].upper()

class TooSoon(Exception):
    """Can't be called so soon"""
    pass

class CoolDownDecorator(object):
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval
        self.last_run = 0

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)

    def __call__(self, *args, **kwargs):
        now_nanos = time.process_time_ns()
        now_ms = now_nanos / 1e6
        if now_ms - self.last_run < self.interval:
            to_go = self.last_run + self.interval - now_ms
            raise TooSoon(f"Call after {to_go} milliseconds")
        else:
            self.last_run = now_ms
            return self.func(*args, **kwargs)

def CoolDown(interval):
    def applyDecorator(func):
        decorator = CoolDownDecorator(func=func, interval=interval)
        return wraps(func)(decorator)

    return applyDecorator

# original code found as answer at https://stackoverflow.com/questions/28767826/python-decorator-call-function-multiple-times
# changes based on the Max Uzi object that rapid-fire-outputs a set number of 'bangs' for every input 'bang'
# changes untested and only useful for rapid-fire bursts, no delay between decorated function calls
# def uzi_func(cache=None, bang_count=1, **func_args):
#     if cache is None:
#         cache = {}
#     if not func_args.keys().__contains__("bang_count"):
#         func_args["bang_count"] = bang_count
#
#     def decorator(func):
#         funcname = func.__name__
#         if funcname not in cache:
#             # save the original function
#             cache[funcname] = func
#         @functools.wraps(func)
#         def wrapped_function(**kwargs):
#             bang_count = func_args.pop("bang_count")
#             while bang_count > 0:
#                 if cache[funcname] != func:
#                     # if cached decorated func-value object with funcname key is != to the wrapped func object,
#                     # also call the cached func with same kwargs
#                     cache[funcname](**func_args)
#                 func(**func_args)
#                 bang_count -= 1
#                 # would need to wait here for any delays, time.sleep() or something?
#         return wrapped_function
#     return decorator

# Source - https://stackoverflow.com/a/38317060
# Posted by MestreLion
# Retrieved 2026-04-24, License - CC BY-SA 3.0
#
# This timer can be used to repeatedly run a (quick) function on a schedule while some long running task (function) runs
# for example, while parsing a set of possibly enormous XML files, this Timer could run the print(f"still parsing {time.time()}") function periodically
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# usage:
# from time import sleep
#
# def hello(name):
#     print "Hello %s!" % name
#
# print "starting..."
# rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
# try:
#     sleep(5) # your long-running job goes here...
# finally:
#     rt.stop() # better in a try/finally block to make sure the program ends!


