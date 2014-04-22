
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
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This is the parent object, which will hold all of the parsed data files in
#           Speed Test File objects. The class will also be capable of creating and
#           returning analyses of the parsed data in .csv files
#
# FUNCTIONS:
#   __init__ - Used to initialize an object of this class
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   loadRawData - Given an array of system arguements, take appropiate actions to load
#                 the raw data from text files, parse into Speed Test File objects, and
#                 add to the Data Structure's internal array
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   addToStructure - Takes the given Speed Test File object and adds it to the correct internal array
#                    based on the STFileObj's Network Provider and Network Type
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   STFileObj:  SpeedTestFile object, holds the raw data that has been parsed
#       OUTPUTS-    none
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
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

    this_SpeedTestFiles = {}
    # ---------------------

    # DESC: Initializing class
    def __init__(self):
        self.meaningOfLife = "bacon"
        #This bit creates the SpeedTest Files array. For each type of connection
        # (i.e., mobile or netbook), it will instantiate another dictionary, where
        # each key is the carrier name, and points to an array
        self.this_SpeedTestFiles = {
                                    "mobile"  : {},
                                    "netbook" : {}
                                   }
        for key in self.this_SpeedTestFiles:
            for elem in self.Carriers:
                self.this_SpeedTestFiles[key][elem] = []
        #END FORS
    #END DEF


    # DESC: Given the system arguements from main.py, load in the raw data files
    def loadRawData(self, sysArgv):
        #cheat for not having to select the folder every time.
        #change string in DataRoot to be the absolute path to the data files
        #In command line, use "python main.py -c"
        # use "python main.py -cs" to only test on 3 files (one of each type)
        # use "python main.py -css" to only test on 1 file
        if (len(sysArgv) > 1):
            #This little boolean is so that our output are not a long
            short_str_method = True
            #Alter this string to be the parent directory holding all of the data
            DataRootPeter = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/"
            DataRootBrandon = "D:/CPUC/BB_results/"
            if (sysArgv[1] == "-tf"):
                file1 = DataRootBrandon + "10_18_2013/WBBDTest2-10182013113755.txt"
                test_SpeedTest = SpeedTestFile(file1, short_str_method)
                self.addToStructure(test_SpeedTest)
            elif (sysArgv[1] == "-c"):
                for root, dirs, files in os.walk(DataRootPeter+"10_18_2013/"):
                    for aFile in files:
                        #Seeing if the file given is, in fact, a data file
                        #If not, the script will exit and display the message below
                        f = open(os.path.join(root, aFile),'r')
                        isItCPUC = f.readline()
                        if ("CPUC Tester Beta v2.0" in isItCPUC):
                            test_STFile = SpeedTestFile(os.path.join(root, aFile), short_str_method)
                            #print(str(test_STFile))
                            self.addToStructure(test_STFile)
                        #END IF
                    #END FOR files
                #END FOR os.walk
            #END IF

            elif (sysArgv[1] == "-cs"):
                #Alter these strings to be individual data files
                file1 = DataRootPeter + "10_17_2013/99000344556962-10172013151027.txt"
                file2 = DataRootPeter + "10_17_2013/356420059231100-10172013094856.txt"
                file3 = DataRootPeter + "10_17_2013/WBBDTest2-10172013151943.txt"
                stfile1 = SpeedTestFile(file1, short_str_method)
                stfile2 = SpeedTestFile(file2, short_str_method)
                stfile3 = SpeedTestFile(file3, short_str_method)
                self.addToStructure(stfile1)
                self.addToStructure(stfile2)
                self.addToStructure(stfile3)
                #print(str(stfile1))
                #print(str(stfile2))
                #print(str(stfile3))

            elif (sysArgv[1] == "-css"):
                #Alter this string to be an individual data file
                file1 = DataRootPeter + "10_17_2013/99000344556962-10172013151027.txt"
                test_SpeedTest = SpeedTestFile(file1, short_str_method)
                self.addToStructure(test_SpeedTest)
                #print( str(test_SpeedTest) )
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
        #END IF/ELSE
    #END DEF


    # DESC: Add the created Speed Test File object to the correct dictionaries
    def addToStructure(self, STFileObj):
        #Checking to see if the passed object's Network Provider
        # is in our list of Carriers. If it is, use the STFile's
        # network type and provider to add it to the correct dictionary
        if STFileObj.NetworkProvider in self.Carriers:
            (self.this_SpeedTestFiles[STFileObj.NetworkType]
                                     [STFileObj.NetworkProvider]
                                     .append(STFileObj) )
        #If the Network Provider was not in the list of carriers, try
        # using the Network Operator. If that variable is in the list of
        # carriers, use it and the network type to add it to the correct dict
        elif STFileObj.NetworkOperator in self.Carriers:
            (self.this_SpeedTestFiles[STFileObj.NetworkType]
                                     [STFileObj.NetworkOperator]
                                     .append(STFileObj) )
        #Otherwise, the File parsed does not have any useful information for us.
        # As long as it's Network Provider and Network Operator are not "N/A", add
        # the value to the list of ignored carriers. Also, add the object's filename
        # to the list of ignored files, for use later
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


    # DESC: Creating a csv file of the data structure. Starts by converting
    #       the structure into a 2-dimensional array, then passes it to the
    #       csv converter class, which returns the file
    def convertTo_StructureTo2D(self):
        #Start by creating an empty dictionary. then copy the structure's
        # dictionary into it, so that when the function is done editting things,
        # the original is not lost
        toBeReturned = {
                        "mobile"  : {},
                        "netbook" : {}
                       }
        for key in toBeReturned:
            for elem in self.Carriers:
                toBeReturned[key][elem] = []

        for devType in self.this_SpeedTestFiles:
            for carrier in self.this_SpeedTestFiles[devType]:
                for speedTest in self.this_SpeedTestFiles[devType][carrier]:
                    toBeReturned[devType][carrier].append(speedTest.convertTo2D())
            #END FOR
        #END FOR
        return toBeReturned
    #END DEF


    # DESC: This will take the object's structure of parsed data and return
    #       an array of 2-dimensional arrays that can be passed into the
    #       CSV converter class. Each 2-D array will be placed into a specific
    #       type, carrier, and direction.
    def convertTo_ObjectToTCP(self, numRangeCols=3): #pingData="speed"
        #Start by creating an empty dictionary. then copy the structure's
        # dictionary into it, so that when the function is done editting things,
        # the original is not lost
        toBeReturned = {
                        "mobile"  : {},
                        "netbook" : {}
                       }
        for key in toBeReturned:
            for elem in self.Carriers:
                toBeReturned[key][elem] = {
                                            "Up" : [] ,
                                            "Down" : []
                                          }
            #END FOR
        #END FOR

        for devType in self.this_SpeedTestFiles:
            for carrier in self.this_SpeedTestFiles[devType]:
                for speedTest in self.this_SpeedTestFiles[devType][carrier]:
                    speedTest.calc_TestTCP_StDev(toBeReturned)
                #END FOR
            #END FOR
        #END FOR
        #After the FOR loops above, the structure toBeReturned should have Up and Down
        # in each carrier populated with standard deviation values. A reference to this
        # structure is then passed to the function that converts the Up and Down dictionaries
        # into 2D arrays
        realReturn = self.convertTo_TCP_to_2D(toBeReturned, numRangeCols)
        return realReturn
    #END DEF


    # DESC: This will take the object's structure of parsed data and return
    #       an array of 2-dimensional arrays that can be passed into the
    #       CSV converter class. Each 2-D array will be placed into a specific
    #       type, carrier, and direction.
    def convertTo_TCP_to_2D(self, structure, numRangeCols=3):
        if numRangeCols < 3:
            numRangeCols = 3
        #END IF
        new_structure = []

        #Gets the max amount of columns we will need in our CSV file
        StDevMax = 0
        for key in structure:
            for elem in structure[key]:
                for direction in structure[key][elem]:
                    try:
                        if (StDevMax < max(structure[key][elem][direction])):
                            StDevMax = max(structure[key][elem][direction])
                    except:
                        #empty sequence passed into max
                        pass;
                    #END IF
            #END FOR
        #END FOR
        val_ranges = []
        for i in range(numRangeCols):
            val_ranges.append(StDevMax*(float(i+1)/numRangeCols))
        #END FOR

        new_structure.append(["Standard Deviation Distribution"])
        new_structure.append(["Data: Sum of TCP thread speeds in 1.0 second intervals"])
        new_structure.append(["Separated by direction, carrier, and type"])
        new_structure.append(["",""])
        new_structure.append(["Network Type:", "Carrier & Direction:"])

        
        for key in structure:
            new_structure.append([key])
            for elem in structure[key]:
                for direction in structure[key][elem]:
                    line = ["", elem, "", "StDev Range:"]
                    line.extend(map(int, val_ranges))
                    new_structure.append(line)

                    range_totals = []
                    for i in range(numRangeCols):
                        range_totals.append(0)
                    #END FOR

                    for value in structure[key][elem][direction]:
                        for i in range(numRangeCols):
                            if value <= val_ranges[i]:
                                range_totals[i] += 1
                                break
                            #END IF
                        #END FOR
                    #END FOR

                    line = ["", direction, "", "Totals:"]
                    line.extend(range_totals)
                    new_structure.append(line)
                    new_structure.append(["",""])
                #END FOR
            #END FOR
            new_structure.append(["",""])
        #END FOR
        return new_structure
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        returnedString = ""
        #For each type of carrier in each device type, print the number of object
        for deviceType in self.this_SpeedTestFiles:
            returnedString += deviceType + "\n"
            for carrier in self.this_SpeedTestFiles[deviceType]:
                returnedString += ("   "+ carrier + ": " +
                                   str(len(self.this_SpeedTestFiles[deviceType][carrier])) + "\n")
            #END FOR
        #END FOR
        #Also, print the carriers that were ignored
        for elem in self.ignored_Carriers:
            returnedString += elem + "; "
        #END FOR

        #Also, print the number of files that were ignored because of bad
        # carrier information
        returnedString += "\nNum ignore files: " + str(len(self.ignored_Files)) + "\n"

        #Use this commented out section to print the file names of all of the
        # ignored files
        """
        for elem in self.ignored_Files:
            returnedString += "\n" + elem
        """
        return returnedString
    #END DEF
#END CLASS
