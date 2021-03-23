from __future__ import with_statement
import Live # This allows us (and the Framework methods) to use the Live API on occasion

from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a button a the controller
from _Framework.ChannelStripComponent import * # Class attaching to the mixer of a given track
from _Framework.EncoderElement import EncoderElement
from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from _Framework.CompoundComponent import CompoundComponent


CHANNEL = 4
num_tracks = 4
mixer = None

class MM1(ControlSurface):

def __init__(self, c_instance):
ControlSurface.__init__(self, c_instance)
self._setup_mixer_control()

def _setup_mixer_control(self):
is_momentary = True
global mixer # We want to instantiate the global mixer as a MixerComponent object (it was a global "None" type up until now...)
mixer = MixerComponent(num_tracks, 0, with_eqs=False, with_filters=False) #(num_tracks, num_returns, with_eqs, with_filters)
mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
self.song().view.selected_track = mixer.channel_strip(0)._track

def _setup_mixer_control(self):
is_momentary = True
num_tracks = 4 #A mixer is one-dimensional; here we define the width in tracks - seven columns,
global mixer #We want to instantiate the global mixer as a MixerComponent object (it was a global "None" type up until now...)
mixer = MixerComponent(num_tracks, 0, with_eqs=False, with_filters=False) #(num_tracks, num_returns, with_eqs, with_filters)
mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
self.song().view.selected_track = mixer.channel_strip(0)._track #set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error
#"""set up the mixer buttons"""
#mixer.set_select_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 56),ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 54)) #left, right track select
#mixer.master_strip().set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 94)) #jump to the master track
#mixer.selected_strip().set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 42)) #sets the mute ("activate") button
#mixer.selected_strip().set_solo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 44)) #sets the solo button
#mixer.selected_strip().set_arm_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 46)) #sets the record arm button
#"""set up the mixer sliders"""
mixer.selected_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, 48)) #sets the continuous controller for volume
#"""note that we have split the mixer functions across two scripts, in order to have two session highlight boxes (one red, one yellow), so there are a few things which we are not doing here..."""











# this tells Live the filename in which to look for my code

import wfK1


# this is the standardized function with which Live loads
# any script. c_instance is the Control Surface slot in Live's
# prefs, as far as I can tell

def create_instance(c_instance):
    # this is what it should load
    # (the thing inside my file that's called 'K1')

    return wfK1.K1(c_instance)


# this lets me use Live's own generic Control Surface code
# to handle a bunch of background tasks in interfacing
# with the app, so I will only have to customize the behavior
# I want and not re-do all the plumbing

from _Framework.ControlSurface import ControlSurface


# this is the thing that'll be loaded in the __init__.py file.
# it's going to be based on the generic Control Surface
# (the slot that was called c_instance in __init__.py)

class K1(ControlSurface):

    # this defines the function to construct what code
    # ('self', i.e. this very thing I wrote below) the slot
    # ('instance') will be assigned

    def __init__(self, instance):
        # this tells the compiler (which turns the script into
        # instructions Live can actually execute) to start with
        # the generic Control Surface initial setup. Super
        # means that we're executing a command in there
        # instead of code in here.

        super(K1, self).__init__(instance, False)

        # this is, as far as I can tell, a protection against crashes,
        # everything I do will be encapsulated in this guard. I
        # found a bunch of sources and scripts that
        # recommended to import the 'with' command, which
        # wasn't available in older versions of the script language,
        # but that turned out to not be necessary in Live 10

        with self.component_guard():
            # now we can do things! The first line shows a message
            # in Live's own status bar, the second adds a line to Log.txt

            self.show_message("Hello World")
            self.log_message("wayfinder K1 remote script loaded")




# code snippet from The Rabbits at Ableton forum for RACKS
def get_device_list(self, container):
    # add each device in order. if device is a rack, process each chain recursively
    # don't add racks that are not showing devices.
    lst = []
    for dev in container:
        lst.append(dev)
        if dev.can_have_chains:  # is a rack and it's open
            if dev.view.is_showing_chain_devices:
                for ch in dev.chains:
                    lst += self.get_device_list(ch.devices)
    return lst

# Called this way.
device_list = self.get_device_list(current_track.devices)


# for foldable groups
if track.is_foldable:
    track.fold_state = not track.fold_state
else:
    track.view.is_collapsed = not track.view.is_collapsed

# fold_state refers to groups .is_foldable is true for Groups.
# .is_collapsed refers to tracks that are collapsed in Arrangement view.

# I combined the two because it means one less pad used and the two are never both true.