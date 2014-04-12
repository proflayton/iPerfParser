
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
from .utils import isLessThanVersion
if not isLessThanVersion((3,0)):
    import Tkinter as TK, tkFileDialog as TKFD
else:
    import tkinter as TK, tkinter.filedialog as TKFD
class SpeedTestDS():

    # ---------------------
    # Initializing some class attributes

    Carriers = ["AT&T", "Verizon", "Sprint", "T-Mobile"]
    ignored_Carriers = []
    ignored_Files = []

    this_SpeedTestFiles = {
                            "mobile"  : {},
                            "netbook" : {}
                          }

    for key in this_SpeedTestFiles:
        for elem in Carriers:
            this_SpeedTestFiles[key][elem] = []
    #END FORS

    # ---------------------
    def __init__(self):
        self.meaningOfLife = "bacon"
    #END DEF


    def loadRawData(self, sysArgv):
        #cheat for not having to select the folder every time.
        #change string in DataRoot to be the absolute path to the data files
        #In command line, use "python main.py -c"
        # use "python main.py -cs" to only test on 3 files (one of each type)
        # use "python main.py -css" to only test on 1 file
        if (len(sysArgv) > 1):
            #Alter this string to be the parent directory holding all of the data
            DataRoot = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/"
            if (sysArgv[1] == "-c"):
                for root, dirs, files in os.walk(DataRoot+"10_18_2013/"):
                    for aFile in files:
                        #Seeing if the file given is, in fact, a data file
                        #If not, the script will exit and display the message below
                        f = open(os.path.join(root, aFile),'r')
                        isItCPUC = f.readline()
                        if ("CPUC Tester Beta v2.0" in isItCPUC):
                            test_STFile = SpeedTestFile(os.path.join(root, aFile))
                            print(str(test_STFile))
                            self.addToStructure(test_STFile)
                        #END IF
                    #END FOR files
                #END FOR os.walk
            #END IF

            elif (sysArgv[1] == "-cs"):
                #Alter these strings to be individual data files
                file1 = DataRoot + "10_17_2013/99000344556962-10172013151027.txt"
                file2 = DataRoot + "10_17_2013/356420059231100-10172013094856.txt"
                file3 = DataRoot + "10_17_2013/WBBDTest2-10172013151943.txt"
                stfile1 = SpeedTestFile(file1)
                stfile2 = SpeedTestFile(file2)
                stfile3 = SpeedTestFile(file3)
                self.addToStructure(stfile1)
                self.addToStructure(stfile2)
                self.addToStructure(stfile3)
                print(str(stfile1))
                print(str(stfile2))
                print(str(stfile3))

            elif (sysArgv[1] == "-css"):
                #Alter this strings to be an individual data file
                file1 = DataRoot + "10_17_2013/99000344556962-10172013151027.txt"
                test_SpeedTest = SpeedTestFile(file1)
                print( str(test_SpeedTest) )
            else:
                print("I don't know that option. I'm just a silly computer. I know -c, -cs, and -css")
            #END IF/ELIF/ELIF/ELSE

        # ----------------------------------------------------------
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
                    if ("CPUC Tester Beta v2.0" in isItCPUC):
                        test_STFile = SpeedTestFile(os.path.join(root, aFile))
                        self.addToStructure(test_STFile)
                    #END IF
                #END FOR files
            #END FOR os.walk
            print("Parsing completed. The data structure has been built.\nWhat analysis would you like to perform?")
        #END IF/ELSE
    #END DEF






    # NEED TO COMMENT BELOW

    def addToStructure(self, STFileObj):
        if STFileObj.NetworkProvider in self.Carriers:
            (self.this_SpeedTestFiles[STFileObj.NetworkType]
                                     [STFileObj.NetworkProvider]
                                     .append(STFileObj) )
        elif STFileObj.NetworkOperator in self.Carriers:
            (self.this_SpeedTestFiles[STFileObj.NetworkType]
                                     [STFileObj.NetworkOperator]
                                     .append(STFileObj) )
        else:
            if STFileObj.NetworkProvider != "N/A":
                if not(STFileObj.NetworkProvider in self.ignored_Carriers):
                    self.ignored_Carriers.append(STFileObj.NetworkProvider)
            elif STFileObj.NetworkOperator != "N/A":
                if not(STFileObj.NetworkOperator in self.ignored_Carriers):
                    self.ignored_Carriers.append(STFileObj.NetworkOperator)
            #END IF/ELIF
            self.ignored_Files.append(STFileObj.FileName)
        #END IF/ELIF/ELSE
    #END DEF


    def __str__(self):
        returnedString = ""
        for deviceType in self.this_SpeedTestFiles:
            returnedString += deviceType + "\n"
            for carrier in self.this_SpeedTestFiles[deviceType]:
                returnedString += ("   "+ carrier + ": " +
                                   str(len(self.this_SpeedTestFiles[deviceType][carrier])) + "\n")
        for elem in self.ignored_Carriers:
            returnedString += elem + "; "

        returnedString += "\nNum ignore files: " + str(len(self.ignored_Files)) + "\n"

        """
        for elem in self.ignored_Files:
            returnedString += "\n" + elem
        """
        return returnedString
#END CLASS
