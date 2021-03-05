This is a work in progress and NOT fully functioning! 
I am not a developer and just started diving into Python.

What is it?
A midi remote script for Ableton Live 11 (!) for the Mackie C4 controller in PYthon 3.

Old Status:
1. Only had a compiled script from Leigh Hunt
2. Script was written for Live 8 (LOM)
3. Was obviously written in Py2
 

What we (a very friendly and helpful person which shall remain anonymous until he tells me otherwise) did last year:
  1. First I decompiled the scripts using an online converter, with mixed results.
  2. Jon did lots of stuff to that, fixed, commented, streamlined, adapted. 
  3. I then decompiled using a better online decompiler.
 

What I did in the last weeks:

  4. I’ve been using Pycharm with proper syntax checking.
  5. Got a new LiveUtils version from the touchable guys, which seems to introduce lots of redundant stuff, but kind of works for now
  6. By hand did the Py2 -> Py3 conversion by looking at what was in the code that looked like Py2 and converted that the Py3 (stuff like utf, long int etc)
  7. Managed to decompile the new Live11/Py3 scripts by using uncomyple6 and using the resulting code as a reference (mainly the Mackie stuff). Not everything was decompiled successfully but most of it
	8. Worked and commented a lot in the code
 


New status:

What works:

			1. Script get detected in Live 11
			2. C4 is usable and shows parameter names, encoders can be used and pushing them defaults value
			3. track switching works, also parameter bank switching and device switching for device mode (err just broke that). Sends etc also work in track mode
			4. (solved, works now) Parameter names do not get properly shortened.  
 

What doesn't work:

    1. when the last device of a track is deleted, the script goes crazy with an index error and I THINK the main problem is this:
			RemoteScriptError: s.build_midi_map(midi_map_handle)
			RemoteScriptError:   File "C:\ProgramData\Ableton\Live 11 Beta\Resources\MIDI Remote Scripts\MackieC4\Encoders.py", line 74, in build_midi_map
			RemoteScriptError: Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, param, 0, encoder, Live.MidiMap.MapMode.relative_signed_bit, feeback_rule, needs_takeover)
			RemoteScriptError: Boost.Python
			RemoteScriptError: ArgumentError
			RemoteScriptError: Python argument types in
			    MidiMap.map_midi_cc_with_feedback_map(int, DeviceParameter, int, int, MapMode, CCFeedbackRule, bool)
			did not match C++ signature:
			    map_midi_cc_with_feedback_map(unsigned int midi_map_handle, class TPyHandle<class ATimeableValue> parameter, int midi_channel, int controller_number, enum NRemoteMapperTypes::TControllerMapMode map_mode, class NPythonMidiMap::TCCFeedbackRule feedback_rule, bool avoid_takeover, float sensitivity=1.0)
		Unfortunately I do not know how to fix this currently (even though I probably spent 4 hrs looking into this already) and I think it's due to LOM changes (Live 8 => Live11)
		Update: adding the "sensitivy" to the midi map signature thing improves things, see commit notes. Careful! If you delete the last device and then select the device again on the C4, the log file will fill up VERY quickly.

    2. Parameter values are not shown (which I know is possible because it works on the Mackie Control Pro, again see the 2 Photos in Google Photos for comparison https://photos.app.goo.gl/m3NXgJcQeLvtHaZZA~~), also the encoders light ring shows "values", so it's gotta be somewhere. 
       What I don't understand is, everywhere in the Ableton scripts parameters and values are clearly derived from the LOM, so the "Live.DeviceParameter.DeviceParameter.value" should give me what I want. And in all original LIVE scripts 
       exactly that is called/accessed, BUT NOT in the Mackie scripts. There everywhere where there should be that, instead vpot_parameter is used and I can't find ANY reference to deviceParameter


I am currently not able to fix more, because I don't know how :-). So any help is welcome! Also I just started getting into Git / GitHub and Pycharm as well, so bear (🐻) with me, if I do something stupid and please correct me (constructively cos I'm sensitive ;-) )
I will also upload the decompiled Ableton Live 11 / Python 3 remote scripts in a separate repository.
