import os
from fnmatch import fnmatch
import subprocess
root = "/Users/bernardahn/Desktop/MIDI Remote Scripts"
pattern="*.pyc"
for path, subdirs,files in os.walk(root):
	for name in files:
		if fnmatch(name,pattern):
			index=os.path.splitext(name)[0]
			newfile=index+".py"
			newfile=os.path.join(path,newfile)
			subprocess.call(["touch",newfile])
			subprocess.call(["uncompyle6","-o",newfile,os.path.join(path,name)])