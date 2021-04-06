This is a work in progress and NOT fully functioning! I suggest to open the Live log file to monitor what's going as there's still some errors which fill that up quickly. If you don't know where that log file is, this script is NOT for you 😉
I am not a developer and just started diving into Python.

What is it?
A midi remote script for Ableton Live 11 (!) for the Mackie C4 controller in PYthon 3.

Old Status:
1. Only had a compiled script from Leigh Hunt
2. Script was written for Live 8 (LOM)
3. Was obviously written in Py2
 
 
What we did last year:
  1. First I decompiled the scripts using an online converter, with mixed results.
  2. Jon did lots of work to that, fixed, commented, streamlined, adapted. 
  3. I then decompiled using a better online decompiler.

What we did in the last weeks:

  4. Been using Pycharm with proper syntax checking.
  5. Got rid of LiveUtils
  6. By hand did the Py2 -> Py3 conversion by looking at what was in the code that looked like Py2 and converted that the Py3 (stuff like utf, long int, xrange > range etc)
  7. Managed to decompile the new Live11/Py3 scripts by using uncomyple6 and using the resulting code as a reference (mainly the Mackie stuff). Not everything was decompiled successfully but most of it
	8. Worked and commented a lot in the code
 


New status:

What works:

			1. Script get detected in Live 11
			2. C4 is usable and shows parameter names, encoders can be used and pushing them sets default value (where existant)
			3. Track switching works, also parameter bank switching and device switching for device mode (works if not a grouped device). 
			4. (solved, works now) Parameter names do not get properly shortened.  
			5. "Sends" etc also work in track mode, BUT always shows 12 "Sends", even if there are less
			6. Grouptrack folding/unfolding
			7. lots more, see Project Board and Issues	
 

What doesn't work / ToDo:

    1. last device deletion causes error #1 https://github.com/markusschloesser/MackieC4_P3/issues/1
    3. for the other stuff, see "Issues" here
   
How to use it?
See Jon's Wiki entry https://github.com/markusschloesser/MackieC4_P3/wiki/How-To-download-and-use-this-Mackie-C4-Remote-Script-in-Ableton-Live

Any help is welcome! 
I also uploaded the decompiled Ableton Live 11 / Python 3 remote scripts in a separate repository. If you want access to those, write me

