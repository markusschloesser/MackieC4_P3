import os
from os.path import join
import subprocess

src_rel_path = r'../../Live11Scripts/MIDI Remote Scripts'
dest_rel_path = r'../MRS11'
"""    
    ##### To run this script in this project's PyCharm Terminal (cmd.exe) #####
    NOTE 2025: a project specific virtual environment Python Interpreter will have uncompyle6.exe in the
        venv/scripts folder.  
        ** in Feb. 2025, uncompyle6 only successfully decompiles code compiled by Python 3.8 or below and Live 12 midi remote 
        scripts seem to have been compiled under Python 3.11.  So, error city, "what is this 3.11 code you speak in?"
        
    * In File>Settings>Project:MackieC4Pro*>Python Interpreter (*any local repository folder name)
        * install/update uncompyle6 in the Project's current Python Interpreter (Python 3.11 for example)
    * If using the system Python Interpreter, add installed uncompyle6.exe location to Windows PATH environment variable (or Confirm PATH entry exists)
        C:\Program Files\Python311\Scripts
    * In File>Settings>Tools>Terminal
        * Shell Path: C:\Windows\system32\cmd.exe
        * Start Directory: "z_utility" folder where chuckNorris.py lives (because Details*)
    * Reboot
    * Reopen this project
    * In Terminal: "Local-cmd" Tab, run
        (venv?) G:MackieC4Pro/z_utility>  python ./chuckNorris.py
    Finally: 
    * In File>Settings>Project:MackieC4Pro*>Project Structure (*any local repository folder name)
        * If MackieC4Pro* is already the Project "Content Root", delete the entry, then
        * Add the (new) MRS11 folder as Content Root
        * And the wip/MackieC4 folder as Content Root
        ** This Project reference structure mirrors the runtime reference structure inside Live's MIDI Remote Scripts folder
        ** meaning the python import paths in every file resolve in this project exactly like they do at runtime in Live
        * Content Root Structure settings only need to be set once (unless the Structure actually changes)
        
    NOTE: You only need to have Chuck walk the range of folders (i.e. run this script) if/when new or updated .pyc files appear in the (recursive) source path
        (OR - whenever uncompyle6 is updated)
    Details*
            ** ../../ Relative (source) path means "Live11Scripts" folder sits outside this repository (two levels up from inside "z_utility" folder)
            ** ../ Relative (dest) path means "MRS11" folder sits inside this repository next to the wip folder (one level up from inside "z_utility" folder)
            ** the subprocess.call() routine below might always use the system Python Interpreter to execute the called command
            ** OR - the fact that no code compiled under Python 3.9 or higher is ever successfully decompiled by uncompyle6 these days was difficult to
               discern from the error messages alone and that fact was certainly difficult to accept on first through tenth (or so) encounters.
            
            **** (Assumed repo-relative folder structure) ****
            commonRoot/Live11Scripts/Midi Remote Scripts (.pyc source files)
            commonRoot/MackieC4Pro
                /.git
                /.idea                      <--- gitignore .idea/
                /MRS11 (.py dest files)     <--- gitignore MRS*/
                /release
                    /MackieC4
                /wip
                    /MackieC4
                        ...
                /z_utility
"""


def walker_folder_ranger():

    for root, _, files in os.walk(src_rel_path):
        for name in files:
            file_path = join(root, name)
            rel_file_path = os.path.join(dest_rel_path, os.path.dirname(os.path.relpath(file_path, src_rel_path)))
            if not os.path.isdir(rel_file_path):
                os.makedirs(rel_file_path)

            rfp = rel_file_path
            fp = file_path
            subprocess.call(['uncompyle6','-o', rfp, fp])


if __name__ == "__main__":
    # execute only if run as a script
    walker_folder_ranger()
