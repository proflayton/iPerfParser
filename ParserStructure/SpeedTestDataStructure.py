
# ------------------------------------------------------------------------
# This block checks to see if the script is being run directly,
# i.e. through the command line. If it is, then it stops and exits the
# program, asking the user to use these files by running the main.py
# ------------------------------------------------------------------------
try:
    from .utils import testForMain
except:
    from utils import testForMain
testForMain(__name__)

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
# VARIABLES:
#   Carriers:            List, all of the carriers that we wish to keep track of
#   ignored_Carriers:    List, will be dynamically added to, if a file has a carrier that we are not tracking
#   ignored_Files:       List, Strings that hold the file name of an ignored file (bad carrier, no carrier, etc.
#   mySpeedTestFiles:    Structure, created in __init__, will hold parsed files, categorized by
#                        Network Type and Carrier
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
#   convertTo_Structure_To_2D - Returns a structure that has converted each SpeedTestFile into a 2-dimensional
#                               array. Each array can be converted to a .csv file. Each array holds all of the
#                               SpeedTestFile information, down to the Ping level
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    None:   The structure created (containing a 2-D array representation of each file)
#                           is passed to the CSV exporter..
#
#   convertTo_Object_To_TCPStDev - Returns a 2D array that can be converted into a 2D array. The information
#                           inside represents a distribution of the standard deviation of each SpeedTestFile's
#                           TCP tests. The values used to calculate each StDev is the sum of all TCP threads' speed
#                           in a specific direction (Up or Down)
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   numRangeCols:   Integer, the number of columns that the user would like in their distribution
#                                   default is 3
#                   maxRange:       The largest value the StDev is allowed that will be organized into the buckets
#       OUTPUTS-    None:           The structure created (containing the StDevs of each test,
#                                   categorized by Direction and Location) is passed to the CSV exporter..
#
#   convertTo_TCP_to_2D - Takes a STDs like structure, and returns it converted into a 2D array.
#                         What was given was a structure like so:
#                         { mobile:
#                               { carrier1:
#                                   { Up: [], Down: [] },
#                                 carrier2:
#                                   { Up: [], Down: [] },
#                                 ..
#                               }
#                           netbook : { .. }
#                         }
#                         Each Up and Down array is a list of standard deviation values
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   structure:      a reference to the structure created in convert_objectToTCP
#                   numRangeCols:   Integer, the number of columns that the user would like in their distribution
#       OUTPUTS-    new_structure:  2D array, that will be converted into a .csv file
#
# * add_StDev_and_Median_to_Master - ...
# *     INPUTS-     ..
#       OUTPUTS-    ..
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    returnedString: String, prints out the number of tests in each nettype and carrier,
#                                   as well as any ignored carriers and the number of ignored files (or their name)
#
# ------------------------------------------------------------------------

from .SpeedTestFile import SpeedTestFile
from .utils import csvExport
import os, sys, datetime
import tkinter as TK, tkinter.filedialog as TKFD

class SpeedTestDS(object):
    # ---------------------
    # Initializing some class attributes
    Carriers = ["AT&T", "Verizon", "Sprint", "T-Mobile"]
    bad_info_Files = []
    ignored_Carriers = []
    ignored_Files = []

    mySpeedTestFiles = {}

    recursively_print = False
    short_str_method = True
    # ---------------------

    # DESC: Initializing class
    def __init__(self, recurPrint=False, quickPrint=True):
        self.meaningOfLife = "bacon"
        self.recursively_print = recurPrint
        self.short_str_method = quickPrint
        #Initializing the arrays in this object. There shouldn't be any conflicts
        # with other objects of the same type, but better to be safe than sorry
        self.ignored_Carriers = []
        self.ignored_Files = []
        self.bad_info_Files = []
        #This bit creates the SpeedTest Files array. For each type of connection
        # (i.e., mobile or netbook), it will instantiate another dictionary, where
        # each key is the carrier name, and points to an array
        self.mySpeedTestFiles = {
                                  "mobile"  : {},
                                  "netbook" : {}
                                }
        for key in self.mySpeedTestFiles:
            for elem in self.Carriers:
                self.mySpeedTestFiles[key][elem] = []
        #END FORS
    #END DEF


    # DESC: Given the system arguements from main.py, load in the raw data files
    def loadRawData(self, sysArgv):
        #cheat for not having to select the folder every time.
        #change string in DataRoot to be the absolute path to the data files
        #In command line:
        # use "main.py -b" if your files are located in the folders specified in the variables
        #   DataRoot, BBResults, and Samples
        # use "main.py -p" if your files are located in the folders specified in the variables
        if (len(sysArgv) > 1):
            if (sysArgv[1] == "-h") or ("help" in sysArgv[1]):
                print(  "Syntax:\n" +
                        "    main.py [fileLocation] [filesToUse]\n" +
                        "Options:\n" +
                        "  -b   Brandon's file location paths\n" +
                        "  -p   Peter's file location paths\n" +
                        "    -c     uses a folder of data files (i.e. 10_17_2013)\n" +
                        "    -cs    uses a file of each type (netbook and mobile)\n" +
                        "    -s     uses sample data files provided (2 w/o errors, 3 w/)\n" +
                        "       OPT: 2 arguements of 'False' or 'True' (sets recurPrint and short_str_method in STDs\n" +
                        "    -ss    uses sample test file 1 (i.e. sample_test_1.txt)\n" +
                        "       OPT: number of text file to use. If file doesn't exist, uses sample_test_1.txt"
                     )
                raise SystemExit
            else:
                if (sysArgv[1] == "-b"):
                    DataRoot = "D:/CPUC/"
                    BBresults = "BB_results/"
                    Samples = ""   #see if statements at the bottom (-s and -ss)
                elif (sysArgv[1] == "-p"):
                    DataRoot = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/"
                    BBresults = "bb results/"
                    Samples = "sampleTests/"
                #END DECLARING STRINGS

                #Below are the actual sys arg options
                if (sysArgv[2] == "-cs"):
                    #Alter these strings to be individual data files
                    file1 = DataRoot + BBresults + "10_17_2013/99000344556962-10172013151027.txt"
                    file2 = DataRoot + BBresults + "10_17_2013/WBBDTest2-10172013151943.txt"
                    stfile1 = SpeedTestFile(file1, self.short_str_method)
                    stfile2 = SpeedTestFile(file2, self.short_str_method)
                    self.addToStructure(stfile1)
                    self.addToStructure(stfile2)
                elif (sysArgv[2] == "-c"):
                    for root, dirs, files in os.walk(DataRoot + BBresults + "10_17_2013/"):
                        for aFile in files:
                            #Seeing if the file given is, in fact, a data file
                            #If not, the script will exit and display the message below
                            f = open(os.path.join(root, aFile),'r')
                            try:
                                isItCPUC = f.readline()
                                if ("CPUC Tester Beta v2.0" in isItCPUC):
                                    test_STFile = SpeedTestFile(os.path.join(root, aFile), self.short_str_method)
                                    self.addToStructure(test_STFile)
                                #END IF
                            except:
                                pass
                        #END FOR files
                    #END FOR os.walk
                #------------------------------------------------
                elif (sysArgv[2] == "-s"):
                    try:
                        self.recursively_print = False if sysArgv[3] == "False" else True
                        self.short_str_method = False if sysArgv[4] == "False" else True
                    except:
                        pass
                    #END TRY/EXCEPT
                    for root, dirs, files in os.walk(DataRoot + Samples):
                        for aFile in files:
                            #Seeing if the file given is, in fact, a data file
                            #If not, the script will exit and display the message below
                            f = open(os.path.join(root, aFile),'r')
                            try:
                                isItCPUC = f.readline()
                                if ("CPUC Tester Beta v2.0" in isItCPUC):
                                    test_STFile = SpeedTestFile(os.path.join(root, aFile), self.short_str_method)
                                    self.addToStructure(test_STFile)
                            except:
                                pass
                            #END TRY/EXCEPT
                        #END FOR files
                    #END FOR os.walk
                elif (sysArgv[2] == "-ss"):
                    try:
                        num = sysArgv[3]
                    except:
                        num = 1
                    #END TRY/EXCEPT
                    file1 = DataRoot + Samples + "sample_test_" + str(num) + ".txt"
                    if not os.path.isfile(file1):
                        file1 = DataRoot + Samples + "sample_test_1.txt"
                    test_SpeedTest = SpeedTestFile(file1, self.short_str_method)
                    self.addToStructure(test_SpeedTest)
                else:
                    print("I don't know that option.")
                #END IF/ELIF/ELSE
            #END IF/ELSE
        # ----------------------------------------------------------
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
                #These are used to keep track of what file we are currently at, and the total number of files
                # in the folder we are currently in
                counter = 0
                total = len(files)
                for aFile in files:
                    #This is the progress bar that is printed out
                    print("FOLDER: "+root.split("/")[-1]+' -- FILES: '+str(counter)+'/'+str(total), end='\r')
                    counter+=1
                    #Seeing if the file given is, in fact, a data file
                    #If not, the script will exit and display the message below
                    f = open(os.path.join(root, aFile),'r')
                    try:
                        isItCPUC = f.readline()
                        if ("CPUC Tester Beta v2.0" in isItCPUC):
                            test_STFile = SpeedTestFile(os.path.join(root, aFile), self.short_str_method)
                            self.addToStructure(test_STFile)
                        #END IF
                    except:
                        pass
                #END FOR files
                #Printing an empty line after all of the files have been read, so to clear the text
                print(" "*80, end='\r')
            #END FOR os.walk
        #END IF/ELSE
    #END DEF


    # DESC: Add the created Speed Test File object to the correct dictionaries
    def addToStructure(self, STFileObj):
        #Checking to see if the passed object's Network Provider
        # is in our list of Carriers. If it is, use the STFile's
        # network type and provider to add it to the correct dictionary
        if STFileObj.NetworkProvider in self.Carriers:
            (self.mySpeedTestFiles[STFileObj.NetworkType]
                                     [STFileObj.NetworkProvider]
                                     .append(STFileObj) )
        #If the Network Provider was not in the list of carriers, try
        # using the Network Operator. If that variable is in the list of
        # carriers, use it and the network type to add it to the correct dict
        elif STFileObj.NetworkOperator in self.Carriers:
            (self.mySpeedTestFiles[STFileObj.NetworkType]
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
            #If both the NetworkProvider and NetworkOperator are empty or have a weird 
            # value, then something went wrong when the test was taken and we don't know
            # which carrier this test belongs to. But we will still use the test
            # when adding to the CPUC_Results CSV.
            self.bad_info_Files.append(STFileObj)
            #END IF/ELIF/ELSE
        #END IF/ELIF/ELSE
    #END DEF


    # DESC: Creating a csv file of the data structure. Starts by converting
    #       the structure into a 2-dimensional array, then passes it to the
    #       CSV converter function, which returns the file
    def convertTo_Structure_To_2D(self):
        #Start by creating an empty dictionary. then copy the structure's
        # dictionary into it, so that when the function is done editting things,
        # the original is not lost
        csvReady = {
                        "mobile"  : {},
                        "netbook" : {}
                       }
        for key in csvReady:
            for elem in self.Carriers:
                csvReady[key][elem] = []

        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    csvReady[devType][carrier].append(speedTest.convertTo2D())
            #END FOR
        #END FOR
        print("Please select the folder you wish to hold the csv files that will be created")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV Files",
                                         mustexist = True)
        for devType in csvReady:
            for carrier in csvReady[devType]:
                for array in csvReady[devType][carrier]:
                    try: os.mkdir(rootOfFiles + "/" + "StructureToCSV")
                    except: pass
                    try: os.mkdir(rootOfFiles + "/" + "StructureToCSV" + "/" + devType)
                    except: pass
                    try: os.mkdir(rootOfFiles + "/" + "StructureToCSV" + "/" + devType + "/" + carrier)
                    except: pass
                    #This section exports the 2D array, using the file name stored in the 
                    # 2nd box of the first array
                    csvExport(array, rootOfFiles + "/" + "StructureToCSV" + "/" +
                                     devType + "/" +
                                     carrier + "/" +
                                     array[0][1][:-4] + ".csv")
                #END FOR
            #END FOR
        #END FOR
        return True
    #END DEF


    # DESC: This will take the object's structure of parsed data and return
    #       an array of 2-dimensional arrays that will be passed into the
    #       CSV converter function. Each 2-D array will be placed into a specific
    #       type, carrier, and direction.
    def convertTo_Object_To_TCPStDev(self, numRangeCols=3, maxRange=1000): #pingData="speed"
        #Start by creating an empty dictionary. then copy the structure's
        # dictionary into it, so that when the function is done editting things,
        # the original is not lost
        TCPStDevStruct = {
                          "mobile"  : {},
                          "netbook" : {}
                         }
        for key in TCPStDevStruct:
            for elem in self.Carriers:
                TCPStDevStruct[key][elem] = {
                                              "East" : {  "Up" : [], "Down" : []  },
                                              "West" : {  "Up" : [], "Down" : []  }
                                            }
            #END FOR
        #END FOR
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                counter = 0
                total = len(self.mySpeedTestFiles[devType][carrier])
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    print(" "+devType+"-"+carrier+' -- '+str(counter)+'/'+str(total), end='\r')
                    counter+=1
                    speedTest.calc_TCP_StDev_and_append_to_Distribution(TCPStDevStruct, self.Carriers)
                #END FOR
                print(" "*80, end='\r')
            #END FOR
        #END FOR
        #After the FOR loops above, the structure TCPStDevStruct should have Up and Down
        # in each carrier populated with standard deviation values. A reference to this
        # structure is then passed to the function that converts the Up and Down dictionaries
        # into 2D arrays
        csvStruct_TCPStDev = self.convertTo_TCP_to_2D(TCPStDevStruct, numRangeCols, maxRange)

        print("Please select the folder you wish to hold the csv file that will be created")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV Files",
                                         mustexist = True)
        from datetime import datetime
        now = datetime.now().strftime('%Y%m%d-%I%M%S')
        csvExport(csvStruct_TCPStDev, rootOfFiles + "/StandardDeviationofTCPSumThreads_"+now+".csv")
        return True
    #END DEF


    # DESC: This will take the object's structure of parsed data and return
    #       an array of 2-dimensional arrays that will be passed into the
    #       CSV converter function. Each 2-D array will be placed into a specific
    #       type, carrier, and direction.
    def convertTo_TCP_to_2D(self, structure, numRangeCols, maxRange):
        if numRangeCols < 3:
            numRangeCols = 3
        if maxRange < 1:
            maxRange = 1000
        #END IF
        new_structure = []
        #Creating the arrays of the upper and lower ranges of StDevs.
        # index 2 with in val_ranges_lower is the lower bound of the column, and
        # index 2 of val_ranges_upper is the upper bound
        val_ranges_lower = []
        val_ranges_upper = []
        for i in range(numRangeCols):
            val_ranges_lower.append(maxRange*(float(i)/numRangeCols))
            val_ranges_upper.append(maxRange*(float(i+1)/numRangeCols))
        #END FOR
        true_val_ranges = []
        for i in range(numRangeCols):
            true_val_ranges.append(str(int(val_ranges_lower[i])) + "-" + str(int(val_ranges_upper[i])))
        true_val_ranges.append(str(maxRange)+"+")
        #END FOR

        #Setting up the first 4 lines of the csv (always the same)
        new_structure.append(["Standard Deviation Distribution"])
        new_structure.append(["Data: Sum of TCP thread speeds in 1.0 second intervals"])
        new_structure.append(["Separated by direction, carrier, and type"])
        new_structure.append(["",""])
        new_structure.append(["Network Type:", "Carrier, Server, & Direction:"])

        for key in structure:
            new_structure.append([key])
            for elem in structure[key]:
                #Creating an array of the first four cells (doesn't change between section).
                # Then extend the array with the value ranges, and append to our final 2D array
                line = ["", elem, "StDev Range:"]
                line.extend(true_val_ranges)
                new_structure.append(line)
                for server in structure[key][elem]:
                    for direction in structure[key][elem][server]:
                        #Creating an empty array. Will hold the number of StDevs that fall within a range
                        range_totals = []
                        for i in range(numRangeCols+1):
                            range_totals.append(0)
                        #END FOR

                        #This goes through each value in the specific nettype,carrier,direction that we
                        # are currently looping through, and compares the value to the upper and lower
                        # ranges at each step
                        for value in structure[key][elem][server][direction]:
                            if value > maxRange:
                                range_totals[-1] += 1
                            for i in range(numRangeCols): # numRangeCols-1
                                if (value > val_ranges_lower[i]) and (value <= val_ranges_upper[i]):
                                    range_totals[i] += 1
                                    break
                                #END IF
                            #END FOR
                        #END FOR

                        #Creating an array of the first four cells (doesn't change between section).
                        # Then extend the array with the range totals, and append to our final 2D array
                        line = ["", server+" "+direction, "Totals:"]
                        line.extend(range_totals)
                        new_structure.append(line)
                    #END FOR
                #END FOR
                new_structure.append(["",""])
            #END FOR
            new_structure.append(["",""])
        #END FOR
        return new_structure
    #END DEF


    # DESC: This starts with a reference to a 2-D array (converted from the provided CSV file)
    #       and appends the TCP StDev and Median to the appropiate row (each row is a file)
    def add_StDev_and_Median_to_Master(self, origRef):
        if (origRef[0][-1] != "eTCP_DOWN2_MEDIAN"):
            newHeaders = ["wTCP_UP1_STDEV","wTCP_UP1_MEDIAN",
                          "wTCP_DOWN1_STDEV","wTCP_DOWN1_MEDIAN",
                          "eTCP_UP1_STDEV","eTCP_UP1_MEDIAN",
                          "eTCP_DOWN1_STDEV","eTCP_DOWN1_MEDIAN",
                          "wTCP_UP2_STDEV","wTCP_UP2_MEDIAN",
                          "wTCP_DOWN2_STDEV","wTCP_DOWN2_MEDIAN",
                          "eTCP_UP2_STDEV","eTCP_UP2_MEDIAN",
                          "eTCP_DOWN2_STDEV","eTCP_DOWN2_MEDIAN"
                         ]
            origRef[0].extend(newHeaders)
        #END IF
        #This section goes through all of the tests stored in this structure and runs
        # the SpeedTestFile object's StDev and Median appending function
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                counter = 0
                total = len(self.mySpeedTestFiles[devType][carrier])
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    #This is the progress bar/output for this function
                    print(" "+devType+"-"+carrier+' -- '+str(counter)+'/'+str(total), end='\r')
                    counter+=1
                    speedTest.calc_StDev_and_Median_and_append_to_MasterCSV( origRef )
                #END FOR
                #After printing out the progress for one carrier, it clears the line
                print(" "*80, end='\r')
            #END FOR
        #END FOR
        #This section does the same thing as above, but it runs through the files 
        # that had no carrier information.
        counter = 0
        total = len(self.bad_info_Files)
        for speedTest in self.bad_info_Files:
            print(" Files w/o carrier info -- "+str(counter)+"/"+str(total), end='\r')
            counter+=1
            speedTest.calc_StDev_and_Median_and_append_to_MasterCSV( origRef )
        #END FOR
        print(" "*80, end='\r')

        #If there are any rows that still don't have any information for the TCP StDev and Median,
        # we'll put in a value that says there was no such file in the folders of raw data
        lastIndex = origRef[0].index("eTCP_DOWN2_MEDIAN")
        for row in origRef:
            are_there_values_here = row[lastIndex-15:lastIndex+1]
            if not are_there_values_here:
                row.extend(["FileMissingError"]*16)
        #END FOR

        print("Please select the folder you wish to hold the csv file that will be created")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV File",
                                         mustexist = True)
        csvExport(origRef, rootOfFiles + "/CPUC_FieldTestResults_Q42013Data_with_StDev_Median.csv")
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        returnedString = ""
        #For each type of carrier in each device type, print the number of object
        for deviceType in self.mySpeedTestFiles:
            returnedString += deviceType.upper() + "\n"
            for carrier in self.mySpeedTestFiles[deviceType]:
                returnedString += ("   "+ carrier + ": " +
                                   str(len(self.mySpeedTestFiles[deviceType][carrier])) + "\n")
            #END FOR
        #END FOR

        returnedString += "------------------------------------------\n"

        #Also, print the carriers that were ignored
        for elem in self.ignored_Carriers:
            returnedString += elem + "; "
        #END FOR
        if len(self.ignored_Carriers) > 0:
            returnedString += "\n"

        if self.short_str_method:
            #Print the number of files that were ignored because of bad carrier information
            returnedString += "Num ignore files: " + str(len(self.ignored_Files)) + "\n"
        else:
            #This loop prints the file names of all of the ignored files
            for itir in range( int(len(self.ignored_Files)/2) ):
                try: returnedString += self.ignored_Files[itir*2] + ", " + self.ignored_Files[(itir*2)+1] + "\n"
                except: returnedString += self.ignored_Files[itir*2] + "\n"
            #END FOR
        #END IF/ELSE

        #Print the number of files that were ignored because of bad carrier information
        returnedString += "Num files w/o Carrier Info: " + str(len(self.bad_info_Files)) + "\n"
        #This loop prints the files that had no carrier info
        if self.recursively_print:
            for aFile in self.bad_info_Files:
                returnedString += str(aFile) + "\n"
        #END IF

        returnedString += "------------------------------------------\n"
        returnedString += "------------------------------------------\n"

        #This section will print out all of the parsed files if the quickPrint option is False
        if self.recursively_print:
            for deviceType in self.mySpeedTestFiles:
                for carrier in self.mySpeedTestFiles[deviceType]:
                    for aFile in self.mySpeedTestFiles[deviceType][carrier]:
                        returnedString += str(aFile) + "\n"
                    #END FOR
                #END FOR
            #END FOR
        #END IF

        return returnedString
    #END DEF
#END CLASS
