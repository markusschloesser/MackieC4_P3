Disclaimer:
This is fully functional, but as all other Midi Remote Scripts done without proper documentation! We have been using it for over 2 years in daily studio projects. Nevertheless there might be errors and as new features are constantly being added, Live might be slower or even unstable. Please take this under consideration.
I suggest to open the Live logfile every once in a while to monitor what's going on. We do not take responsibility for lost tracks etc, make backups!


What is it:
A midi remote script for Ableton Live 10 and 11 for the Mackie C4 controller in Python 3 with backwards compatibility to Py2.7 for Live 10.

How to install it:
Copy 'wip/MackieC4' folder to your 'MIDI Remote Scripts'. Make sure Live is not open or if it was, please restart Live.
Ports: in Live midi settings select the script "MackieC4" and set both in and out ports to Midi in/out ports. and activate 'Track' and 'Remote' for both ports. Further info @https://github.com/markusschloesser/MackieC4_P3/wiki/How-To-download-and-use-this-Mackie-C4-Remote-Script-in-Ableton-Live

How to use it?
See the Manual/Wiki with lots of picture https://github.com/markusschloesser/MackieC4_P3/wiki
showing ChannelStrip, Devices and Function mode

What can you do with it:

	1. Script works in Live 10 and 11, not tested under Live 9
	2. C4 is fully usable and shows parameter names, encoders can be used and pushing them sets default value (where existant). Where there are quantized parameters, clicking the encoder steps between values, turning does the same.
	3. Track switching, also parameter bank switching and device switching for device mode (works also for grouped/chained device). 
	4. Parameter names get properly shortened.  
	5. "Sends" etc also work in track mode
	6. Grouptrack folding/unfolding
	7. "Function mode" offers lots and lots of standard Live functionality like clip/detail view switching, unarm all, unsolo all, unmute all, follow/unfollow
	8. lots more, see Project Board https://github.com/markusschloesser/MackieC4_P3/projects and 
	9. current ssues https://github.com/markusschloesser/MackieC4_P3/issues	
 

What doesn't work / ToDo:

    1. see "Issues" here
    2. next steps: migrate to v2/v3 framework utilizing (ControlSurface): If anyone has ANY documentation (besides the old docstrings) about the v2/v3 framework, I'd be most appreciative!
   

Any help is welcome! Suggestions, Ideas for enhancement, bug reports, especially code contributions. Please check, if we already thought about it, and if it's in issues https://github.com/markusschloesser/MackieC4_P3/issues 😉 
I also uploaded the decompiled Ableton Live 9-11 remote scripts in a separate repository. If you want access to those, write me



History of the code:
Old Status:
1. Only had a compiled script from Leigh Hunt (massive credits to him!)
2. Script was written for Live 8 (LOM)
3. Was written in Python 2
 
 
What we did 2020:
  1. First I decompiled the scripts using an online converter, with mixed results.
  2. Jon did lots of work to that, fixed, commented, streamlined, adapted. 
  3. I then decompiled using a better online decompiler.

What we did in 2021:

  1. using Pycharm with proper syntax checking.
  2. Got rid of LiveUtils
  3. By hand did the Py2 -> Py3 conversion by looking at what was in the code that looked like Py2 and converted that the Py3 (stuff like utf, long int, xrange > range etc)
  4. Managed to decompile the new Live11/Py3 scripts by using uncomyple6 and using the resulting code as a reference. Not everything was decompiled successfully but most of it
  5. Worked and commented a lot in the code
  6. Opened a repository here
  7. fixed a tremendous amount of ugly errors
  8. Integrated liveobj_valid and liveobj_changed
  9. introduced lots of new functionality 

2022/2023:
a lot more functionality, less bugs, shorter code, etc
