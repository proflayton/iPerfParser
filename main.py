# ------------------------------------------------------------------------
# MAIN.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  This program will initially ask the user to choose the folder
#           that houses the raw data files from iPerf speed tests. It then
#           constructs an object that will house the raw data parsed into
#           useable objects for analysis
#
# INPUTS-   This program initially asks the user for the location of the
#           raw data files.
#           !!NOTE!! All of the data files should be in the same locaiton!!
#           After parsing the data, the program will ask the user
#           what type of analysis they wish to perform.
#
# OUTPUTS-  The program, upon parsing the data and recieving a command
#           for a specific analysis, will generate _______
#
# ------------------------------------------------------------------------

from Tests import *
import os
import Tkinter as TK, tkFileDialog as TKFD

"""
path = tkFileDialog.askopenfilename()
path2 = os.path.abspath("F:\\CPUC\\BB_results\\10_17_2013\\99000344556962-10172013151027.txt")
print (path)

#This version of substringing is for Windows OS? the 2 backlashes are how windows delimits file path, right?
print (path2[:path2.rfind("\\")] )
#This version is for Unix. Maybe I can get the OS type at the beginning of the script
print (path[:path.rfind("/")] )

#t = Test(path)
#print(t)
"""

#apparently, after calling this, Mac is "Darwin", Linux is "linux____", and Windows is "win____"
# so, basically, if we want to check for windows, check for "win", otherwise, it's Unix based, and "/" is used'

#print(os.name)

#This is another tKinter function in the TkFileDialog (or tkinter.filedialog) module
rootOfFiles = TKFD.askdirectory()
for root, dirs, files in os.walk(rootOfFiles):
    for aFile in files:
        print( Test(os.path.join(root, aFile)) )
        #print( Test(os.path.join(root, aFile)) )


""" Cool example code

# Delete everything reachable from the directory named in "top",
# assuming there are no symbolic links.
# CAUTION:  This is dangerous!  For example, if top == '/', it
# could delete all your disk files.
import os
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

"""
