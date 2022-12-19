Disclaimer:
This is still a work in progress, but mostly fully functioning! We already use it a lot in daily projects.
I suggest though to open the Live logfile to monitor what's going on, as there's still some errors. 


What is it?
A midi remote script for Ableton Live 10 and 11 for the Mackie C4 controller in Python 3 with backwards compatibility to Py2.7 for Live 10.

How to use it?
See the Wiki https://github.com/markusschloesser/MackieC4_P3/wiki
With pictures showing ChannelStrip, Devices and Function mode

What works:

			1. Script gets detected in Live 10 and 11
			2. C4 is usable and shows parameter names, encoders can be used and pushing them sets default value (where existant). Where there are quantized parameters, clicking the encoder steps between values, turning does the same.
			3. Track switching works, also parameter bank switching and device switching for device mode (only works if not a grouped/chained device). 
			4. Parameter names get properly shortened.  
			5. "Sends" etc also work in track mode
			6. Grouptrack folding/unfolding
			7. "Function mode" offers lots of standard Live functionality like clip/detail view switching, unarm all, unsolo all, unmute all, follow/unfollow
			8. lots more, see Project Board https://github.com/markusschloesser/MackieC4_P3/projects and 
			9. current ssues https://github.com/markusschloesser/MackieC4_P3/issues	
 

What doesn't work / ToDo:

    1. undoing certain things can cause errors see #1 https://github.com/markusschloesser/MackieC4_P3/issues/1
    2. for the other stuff, see "Issues" here
    3. next steps: migrate to v2/v3 framework utilizing (ControlSurface): If anyone has ANY documentation (besides the old docstrings) about the v2/v3 framework, I'd be most appreciative!
   

Any help is welcome! Suggestions, Ideas for enhancement, bug reports, especially code contributions. Please check, if we already thought about it, and if it's in issues https://github.com/markusschloesser/MackieC4_P3/issues 😉 
I also uploaded the decompiled Ableton Live 11 / Python 3 remote scripts in a separate repository. If you want access to those, write me



History of the code:
Old Status:
1. Only had a compiled script from Leigh Hunt (massive credits to him!)
2. Script was written for Live 8 (LOM)
3. Was obviously written in Py2
 
 
What we did 2020:
  1. First I decompiled the scripts using an online converter, with mixed results.
  2. Jon did lots of work to that, fixed, commented, streamlined, adapted. 
  3. I then decompiled using a better online decompiler.

What we did in 2021:

  1. using Pycharm with proper syntax checking.
  2. Got rid of LiveUtils
  3. By hand did the Py2 -> Py3 conversion by looking at what was in the code that looked like Py2 and converted that the Py3 (stuff like utf, long int, xrange > range etc)
  4. Managed to decompile the new Live11/Py3 scripts by using uncomyple6 and using the resulting code as a reference. Not everything was decompiled successfully but most of it
  5- Worked and commented a lot in the code
  6. Opened a repository here
  7. fixed a tremendous amount of ugly errors
  8. Integrated liveobj_valid and liveobj_changed
  9. introduced lots of new functionality 

2022:
more functionality, less bugs, shorter code, etc
