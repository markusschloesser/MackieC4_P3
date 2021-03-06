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
			2. C4 is usable and shows parameter names, encoders can be used and pushing them sets default value (where existant)
			3. Track switching works, also parameter bank switching and device switching for device mode (err just broke that). 
			4. (solved, works now) Parameter names do not get properly shortened.  
			5. "Sends" etc also work in track mode, BUT always shows 11 "Sends" event if there are less	
 

What doesn't work / ToDo:

    1. last device deletion causes error #1 https://github.com/markusschloesser/MackieC4_P3/issues/1
    2. Parameter values are not shown #3 https://github.com/markusschloesser/MackieC4_P3/issues/3
    3. When devices are unfolded, the "new" parameters are not shown, needs some listener to device update or so
    4. device switching (when multiple devices on one track) SOMETIMES works, haven't found out yet why. Seems it doesn't work when a device is grouped
    5. need a way to only show existing "Sends" in Track mode
    6. "Marker" and "Function" mode currently have no functionality implemented, let's figure out something to do with them
	7. expand Grouptrack would be helpful in track mode


I am currently not able to fix more, because I don't know how :-). So any help is welcome! Also, I just started getting into Git / GitHub and Pycharm as well, so bear (🐻) with me, if I do something stupid and please correct me (constructively cos I'm sensitive ;-) )
I also uploaded the decompiled Ableton Live 11 / Python 3 remote scripts in a separate repository.

Other stuff that can be done or needs to be discussed at least:
1. Do we actually need code related to clips, clip_name, scenes, tempo etc? imho there is no need and could be removed.
2. Lots of stuff in "LiveUtils" can probably be replaced by proper calls to Live stuff
