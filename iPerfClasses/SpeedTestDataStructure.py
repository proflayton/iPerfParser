
# ------------------------------------------------------------------------
# This section checks to see if the script is being run directly,
# i.e. through the command line. If it is, then it stops and exits the
# program, asking the user to use these files by running the main.py
# ------------------------------------------------------------------------
if __name__ == '__main__':
    print("Please run main.py.")

    #Changing Current Working Directory to 3 levels up
    import os, sys
    os.chdir("../../..")
    duhDir = os.getcwd()

    #Initialize array to hold locations of "main.py"
    #Using os.walk to look in all sub-directories
    search = []
    for root, dirs, files in os.walk(duhDir):
        for name in files:
            if name == "main.py":
                search.append(os.path.join(root, name))

    print("Your file seems to be located in one of these paths:")
    for link in search:
        print(link)

    #Telling the system to exit with no errors
    raise SystemExit
#END __name__=='__main__'




# ------------------------------------------------------------------------
# SPEEDTESTDATASTRUCTURE.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  ..
#
# FUNCTIONS:
#   __init__ - ...
#       INPUTS-     ...:    ...
#       OUTPUTS-    ...
#
# ------------------------------------------------------------------------

from .SpeedTestFile import SpeedTestFile
import os
import sys
from .utils import checkVersion
if not checkVersion((3,0)):
    import Tkinter as TK, tkFileDialog as TKFD
else:
    import tkinter as TK, tkinter.filedialog as TKFD
class SpeedTestDS():

    # ---------------------
    # Initializing some class attributes
    this_SpeedTestFiles = []
    # ---------------------
    def __init__(self):
        self.meaningOfLife = "bacon"
    #END DEF


    def loadRawData(self, sysArgv):
        #cheat for not having to select the folder every time.
        #change string in os.walk to be the absolute path to the data files
        #In command line, use "python main.py -c"
        # use "python main.py -cs" to only test on 3 files (one of each type)
        if (len(sysArgv) > 1):
            #Alter this string to be the parent directory holding all of the data
            DataRoot = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/"
            if (sysArgv[1] == "-c"):
                for root, dirs, files in os.walk(DataRoot+"10_17_2013/"):
                    for aFile in files:
                        self.this_SpeedTestFiles.append( SpeedTestFile(os.path.join(root, aFile)) )
                        print( self.this_SpeedTestFiles[-1] )
            elif (sysArgv[1] == "-cs"):
                #Alter these strings to be individual data files
                file1 = DataRoot + "10_17_2013/99000344556962-10172013151027.txt"
                file2 = DataRoot + "10_17_2013/356420059231100-10172013094856.txt"
                file3 = DataRoot + "10_17_2013/WBBDTest2-10172013151943.txt"
                self.this_SpeedTestFiles.append( SpeedTestFile(file1) )
                self.this_SpeedTestFiles.append( SpeedTestFile(file2) )
                self.this_SpeedTestFiles.append( SpeedTestFile(file3) )
                for elem in self.this_SpeedTestFiles:
                    print( str(elem) )
            elif (sysArgv[1] == "-css"):
                #Alter this strings to be an individual data file
                file1 = DataRoot + "10_17_2013/99000344556962-10172013151027.txt"
                test_SpeedTest = SpeedTestFile(file1)
                print( str(test_SpeedTest) )
            else:
                print("I don't know that option. I'm just a silly computer. I know -c, -cs, and -css")
            #END IF/ELIF/ELIF/ELSE
        else:
            #Asking for a directory from the user
            # initialdir sets the starting point as the user's home directory
            # title sets what to display in the title of the dialog box
            # mustexits means that the folder chosen must exist
            print("Please select the folder containing all of the raw data in the new dialog box...")
            rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                             title = "Select the Folder Containing the Raw Data",
                                             mustexist = True)

            #Loops through all files in given folder
            #You must use speedTest.speedTest as the left speedTest is
            # the module, and the right speedTest is the class. Maybe I should rename that?
            for root, dirs, files in os.walk(rootOfFiles):
                for aFile in files:
                    #Seeing if the file given is, in fact, a data file
                    #If not, the script will exit and display the message below
                    f = open(os.path.join(root, aFile),'r')
                    isItCPUC = f.readline()
                    # !!!!!!!!!
                    # The internal block of the IF statement will need
                    # to be elaborated on. It currently does nothing.
                    # It should build the array of SpeedTestFile objects and
                    # then allow the user to perform analysis on these objects
                    # !!!!!!!!1
                    if ("CPUC Tester Beta v2.0" in isItCPUC):
                        print( SpeedTestFile(os.path.join(root, aFile)) )
        #END IF/ELSE
    #END DEF
#END CLASS