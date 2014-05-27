
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
#   Carriers:           List, all of the carriers that we wish to keep track of
#   bad_info_Files      List, parse File objects that don't have the necessary information for sorting
#   ignored_Carriers:   List, will be dynamically added to, if a file has a carrier that we are not tracking
#   ignored_Files:      List, Strings that hold the file name of an ignored file (bad carrier, no carrier, etc.
#   mySpeedTestFiles:   Structure, created in __init__, will hold parsed files, categorized by
#                        Network Type and Carrier
#   recursively_print   Boolean, if true, prints all object in mySpeedTestFiles and bad_info_Files
#   short_str_method    Boolean, if true, prints objects in shorter version. Is passed to objects in structure
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
#   convert_Structure_To_2D - Returns a structure that has converted each SpeedTestFile into a 2-dimensional
#                       array. Each array can be converted to a .csv file. Each array holds all of the
#                       SpeedTestFile information, down to the Ping level
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    None:   The structure created (containing a 2-D array representation of each file)
#                           is passed to the CSV exporter..
#
#   create_TCP_StDev_Distribution - Returns a 2D array that can be converted into a 2D array. The information
#                       inside represents a distribution of the standard deviation of each SpeedTestFile's
#                       TCP tests. The values used to calculate each StDev is the sum of all TCP threads' speed
#                       in a specific direction (Up or Down)
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   numRangeCols:   Integer, the number of columns that the user would like in their distribution
#                                   default is 3
#                   maxRange:       The largest value the StDev is allowed that will be organized into the buckets
#       OUTPUTS-    None:           The structure created (containing the StDevs of each test,
#                                   categorized by Direction and Location) is passed to the CSV exporter..
#
#   convert_TCPStDevStruct_to_2D - Takes a STDs like structure, and returns it converted into a 2D array.
#                       What was given was a structure like so:
#                       { mobile:
#                           { carrier1:
#                               { Up: [], Down: [] },
#                             carrier2:
#                               { Up: [], Down: [] },
#                             ..
#                           }
#                         netbook : { .. }
#                       }
#                       Each Up and Down array is a list of standard deviation values
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   structure:      a reference to the structure created in convert_objectToTCP
#                   numRangeCols:   Integer, the number of columns that the user would like in their distribution
#       OUTPUTS-    new_structure:  2D array, that will be converted into a .csv file
#
#   add_StDev_and_Median_to_Given - This calculates the standard deviations of every SpeedTestFile object's
#                                    TCP tests (Up and Down separately), as well as the median of those tests
#                                    and appends the values to the imported CSV file, in the appropiate row
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   origRef:    reference to the 2D array of the imported CSV file
#       OUTPUTS-    None:       The function creates a 2D array of the imported CSV file, appends the necessary
#                               data, and then exports the file in the users chosen location
#
#   add_rVal_and_MOS_to_Given - This calculates the standard deviations of every SpeedTestFile object's
#                               TCP tests (Up and Down separately), as well as the median of those tests
#                                    and appends the values to the imported CSV file, in the appropiate row
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   origRef:    reference to the 2D array of the imported CSV file
#       OUTPUTS-    None:       The function creates a 2D array of the imported CSV file, appends the necessary
#                               data, and then exports the file in the users chosen location
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
                    Samples = ""   #used by if statements at the bottom (-s and -ss)
                elif (sysArgv[1] == "-p"):
                    DataRoot = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/iPerfParser/Raw Data/"
                    BBresults = "BB results/2013_4thField/"
                    #BBresults = "BB results/2013_3rdField/"
                    Samples = "sampleTests/"
                #END DECLARING STRINGS

                #Below are the actual sys arg options
                if (sysArgv[2] == "-cs"):
                    #Alter these strings to be individual data files. These two files are one of
                    # each kind, a mobile Test, and a netbook Test
                    file1 = DataRoot + BBresults + "10_17_2013/99000344556962-10172013151027.txt"
                    file2 = DataRoot + BBresults + "10_17_2013/WBBDTest2-10172013151943.txt"
                    stfile1 = SpeedTestFile(file1, self.short_str_method)
                    stfile2 = SpeedTestFile(file2, self.short_str_method)
                    self.addToStructure(stfile1)
                    self.addToStructure(stfile2)
                elif (sysArgv[2] == "-c"):
                    for root, dirs, files in os.walk(DataRoot + BBresults + "10_24_2013/"):
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
                # ------------------------------------------------------------
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
                # ------------------------------------------------------------
                elif (sysArgv[2] == "-qk"):
                    for root, dirs, files in os.walk(DataRoot + "/testthese/"):
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
                else:
                    print("I don't know that option.")
                #END IF/ELIF/ELSE
            #END IF/ELSE
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        else:
            #Asking for a directory from the user
            # initialdir sets the starting point as the user's home directory
            # title sets what to display in the title of the dialog box
            # mustexits means that the folder chosen must exist
            print("Please select the folder containing all of the raw data in the new dialog box...")
            rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                             title = "Select the Folder Containing the Raw Data",
                                             mustexist = True)

            #Loops through all files in given folder, and any subfolders.
            #This loop is to just get the count of files that will be read in, so that
            # we can print out a progress bar.
            print("Counting files...")
            totalFiles = 0
            for root, dirs, files in os.walk(rootOfFiles):
                for aFile in files:
                    f = open(os.path.join(root, aFile),'r')
                    try:
                        isItCPUC = f.readline()
                        if ("CPUC Tester Beta v2.0" in isItCPUC):
                            totalFiles += 1
                    except:
                        pass
                #END FOR files
            #END FOR os.walker
            print("Done counting files...")

            #Now we read in the files, and keep track of how many files have been read in and parsed
            fileCounter = 0
            counterCounter = 0
            for root, dirs, files in os.walk(rootOfFiles):
                for aFile in files:
                    #Seeing if the file given is, in fact, a data file
                    #If not, the script will exit and display the message below
                    f = open(os.path.join(root, aFile),'r')
                    try:
                        isItCPUC = f.readline()
                        if ("CPUC Tester Beta v2.0" in isItCPUC):
                            #This is the progress bar that is printed out
                            fileCounter += 1; counterCounter +=1
                            if counterCounter > (totalFiles/200):
                                counterCounter = 0
                                percent = float(fileCounter)/totalFiles
                                print("[" + "="*int(percent*13) + " "*int((1-percent)*13) + "] " + 
                                        str(int(percent*100)) + "%", end='\r')
                            #END IF
                            #This is where the file is actually created, and then added to the structure
                            test_STFile = SpeedTestFile(os.path.join(root, aFile), self.short_str_method)
                            self.addToStructure(test_STFile)
                        #END IF
                    except:
                        pass
                #END FOR files
            #END FOR os.walk
            #Printing an empty line after all of the files have been read, so to clear the text
            print(" "*80, end='\r')
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
    def convert_Structure_To_2D(self):
        #Start by creating an empty dictionary. then copy the structure's
        # dictionary into it, so that when the function is done editting things,
        # the original is not lost
        csvReady = {  "mobile"  : {},
                      "netbook" : {},
                      "bad_info_Files": []
                    }
        for key in csvReady:
            if key != "bad_info_Files":
                for elem in self.Carriers:
                    csvReady[key][elem] = []
        #END FORs
        #This is where the actual function call is made. Looping through the structure, we call
        # the SpeedTestFile's convertTo2D function, and append the result (a 2D array) to our new
        # temporary structure (csvReady)
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    csvReady[devType][carrier].append(speedTest.convert_Obj_To_2D())
            #END FOR
        #END FOR
        for speedTest in self.bad_info_Files:
            csvReady["bad_info_Files"].append(speedTest.convert_Obj_To_2D())
        #END FOR
        #We ask where the user wants the files put
        print("Please select the folder you wish to hold the csv files that will be created:")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV Files",
                                         mustexist = True)
        #Looping through the structure, we check to see if the necessary folders have been created.
        # There will be folders that separate the CSVs by device type and carrier, and they all go into a
        # "StructureToCSV" folder. If the folder has already been created, we go to except, which passed, and then
        # continues until we reach the actual csvExporter. This exports the file with the filename of
        # the object, which happens to be stored in the first row, second cell
        for devType in csvReady:
            if devType != "bad_info_Files":
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
                                         array[0][1].split(".")[0] + ".csv")
                    #END FOR
                #END FOR
            else:
                for array in csvReady[devType]:
                    try: os.mkdir(rootOfFiles + "/" + "StructureToCSV")
                    except: pass
                    try: os.mkdir(rootOfFiles + "/" + "StructureToCSV" + "/" + devType)
                    except: pass
                    #This section exports the 2D array, using the file name stored in the 
                    # 2nd box of the first array
                    csvExport(array, rootOfFiles + "/" + "StructureToCSV" + "/" +
                                     devType + "/" +
                                     array[0][1].split(".")[0] + ".csv")
                #END FOR
            #END IF/ELSE
        #END FOR
        return True
    #END DEF



    # DESC: This will take the object's structure of parsed data and return
    #       an array of 2-dimensional arrays that will be passed into the
    #       CSV converter function. Each 2-D array will be placed into a specific
    #       type, carrier, and direction.
    def create_TCP_StDev_Distribution(self, numRangeCols=3, maxRange=1000):
        #Start by creating an empty dictionary. then copy the structure's
        # dictionary into it, so that when the function is done editting things,
        # the original is not lost
        TCPStDevStruct = {
                          "mobile"  : {},
                          "netbook" : {}
                         }
        #The structure is similar to the basic one, with each test being separated by device type
        # and carrier. But inside, we are totalling up the standard deviation for each connected location
        # (East and West), and each direction (Up and Down). Hence, we create another dictionary, and inside
        # a dictionary pointing to an array. This reference will be passed through to each SpeedTestFile
        # object, who will append valus to the correct array (based on dev type, carrier, location, and direction)
        for key in TCPStDevStruct:
            for elem in self.Carriers:
                TCPStDevStruct[key][elem] = {
                                              "East" : {  "Up" : [], "Down" : []  },
                                              "West" : {  "Up" : [], "Down" : []  }
                                            }
            #END FOR
        #END FOR
        #Counting the number of files in the object, not including the bad files
        filesInStruct = 0
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                filesInStruct += len(self.mySpeedTestFiles[devType][carrier])
        #END FORs
        #Variables used to track how many objects have been processed
        objCounter = 0
        counterCounter = 0
        
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    #Creating the progress bar
                    objCounter += 1
                    counterCounter += 1
                    if counterCounter > (filesInStruct/200):
                        counterCounter = 0
                        percent = float(objCounter)/filesInStruct
                        print("[" + "="*int(percent*13) + " "*int((1-percent)*13) + "] " + 
                                str(int(percent*100)) + "%", end='\r')
                    #Actually calling the function that calculate the StDev for the distribution. The list
                    # of carrier needs to be passed through because we don't know if the carrier name
                    # is in Network Provider or Operator. Hence, we need the array of allowed
                    # carriers, and so we pass in a reference
                    speedTest.calc_TCP_StDev_for_Distribution(TCPStDevStruct, self.Carriers)
                #END FOR
            #END FOR
        #END FOR
        #Line that clears the progress bar
        print(" "*80, end='\r')
        #After the FOR loops above, the structure TCPStDevStruct should have Up and Down
        # in each carrier populated with standard deviation values. A reference to this
        # structure is then passed to the function that converts the Up and Down dictionaries
        # into 2D arrays
        csvStruct_TCPStDev = self.convert_TCPStDevStruct_to_2D(TCPStDevStruct, numRangeCols, maxRange)

        print("Please select the folder you wish to hold the csv file that will be created")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV Files",
                                         mustexist = True)
        #Just to keep everything from conflicting/overwriting, we append the datetime onto the
        # end of the filename. Format is Year Month Day "-" Hour(12 hour clock) Minute Second
        from datetime import datetime
        now = datetime.now().strftime('%Y%m%d-%I%M%S')
        csvExport(csvStruct_TCPStDev, rootOfFiles + "/StandardDeviationofTCPSumThreads_"+now+".csv")
        return True
    #END DEF


    # DESC: This will take the object's structure of parsed data and return
    #       an array of 2-dimensional arrays that will be passed into the
    #       CSV converter function. Each 2-D array will be placed into a specific
    #       type, carrier, and direction.
    def convert_TCPStDevStruct_to_2D(self, structure, numRangeCols, maxRange):
        if numRangeCols < 3:
            numRangeCols = 3
        if maxRange < numRangeCols:
            maxRange = 1000
        #END IF
        new_structure = []
        #Creating the arrays of the upper and lower ranges of StDevs.
        # Two array are created as the output is easier, and the comparisons are also easier
        val_ranges_lower = []
        val_ranges_upper = []
        for i in range(numRangeCols):
            val_ranges_lower.append(maxRange*(float(i)/numRangeCols))
            val_ranges_upper.append(maxRange*(float(i+1)/numRangeCols))
        #END FOR
        #This array is just used for the output, as it will consist of strings of the upper and lower
        # ranges from the arrays above
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

        for devType in structure:
            #Appending the device type. This will be in the top left corner of all of it's data
            new_structure.append([devType])
            for carrier in structure[devType]:
                #Creating an array of the first four cells (doesn't change between section).
                # Then extend the array with the value ranges, and append to our final 2D array
                line = ["", carrier, "StDev Range:"]
                line.extend(true_val_ranges)
                new_structure.append(line)
                for server in structure[devType][carrier]:
                    for direction in structure[devType][carrier][server]:
                        #Creating an empty array. Will hold the number of StDevs that fall within a range
                        # The empty array is created this way rather than with [0]*numRangeCols because
                        # I want to make sure that each element is referencing an individual object
                        range_totals = []
                        for i in range(numRangeCols+1):
                            range_totals.append(0)
                        #END FOR
                        #This goes through each value in the specific nettype,carrier,direction that we
                        # are currently looping through, and compares the value to the upper and lower
                        # ranges at each step
                        for value in structure[devType][carrier][server][direction]:
                            if value > maxRange:
                                range_totals[-1] += 1
                            for i in range(numRangeCols):
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
    def add_StDev_and_Median_to_Given(self, origCSVRef, filename):
        #This appends the new column headers to the CPUC_Results CSV if they do not exist.
        # We check if they exist by seeing if the last header is "eTCP_DOWN2_MEDIAN"
        if (origCSVRef[0][-1] != "eTCP_DOWN2_MEDIAN"):
            newHeaders = ["wTCP_UP1_STDEV","wTCP_UP1_MEDIAN",
                          "wTCP_DOWN1_STDEV","wTCP_DOWN1_MEDIAN",
                          "eTCP_UP1_STDEV","eTCP_UP1_MEDIAN",
                          "eTCP_DOWN1_STDEV","eTCP_DOWN1_MEDIAN",
                          "wTCP_UP2_STDEV","wTCP_UP2_MEDIAN",
                          "wTCP_DOWN2_STDEV","wTCP_DOWN2_MEDIAN",
                          "eTCP_UP2_STDEV","eTCP_UP2_MEDIAN",
                          "eTCP_DOWN2_STDEV","eTCP_DOWN2_MEDIAN"
                         ]
            origCSVRef[0].extend(newHeaders)
        #END IF
        #Counting all of the files in this object, to be used for a progress bar
        filesInStruct = 0
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                filesInStruct += len(self.mySpeedTestFiles[devType][carrier])
        filesInStruct += len(self.bad_info_Files)
        #Variables used to track how many objects have been processed
        objCounter = 0
        counterCounter = 0

        #This section goes through all of the tests stored in this structure and runs
        # the SpeedTestFile object's StDev and Median appending function
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    #Creating the progress bar
                    objCounter += 1
                    counterCounter += 1
                    if counterCounter > (filesInStruct/200):
                        counterCounter = 0
                        percent = float(objCounter)/filesInStruct
                        print("[" + "="*int(percent*13) + " "*int((1-percent)*13) + "] " + 
                                str(int(percent*100)) + "%", end='\r')
                    #Actually calling the function
                    speedTest.calc_TCP_StDev_and_Median_then_Append( origCSVRef )
                #END FOR
            #END FOR
        #END FOR
        #This section does the same thing as above, but it runs through the files 
        # that had no carrier information.
        for speedTest in self.bad_info_Files:
            #Creating the progress bar
            objCounter += 1
            counterCounter += 1
            if counterCounter > (filesInStruct/200):
                counterCounter = 0
                percent = float(objCounter)/filesInStruct
                print("[" + "="*int(percent*13) + " "*int((1-percent)*13) + "] " + 
                        str(int(percent*100)) + "%", end='\r')
            #Actually calling the function
            speedTest.calc_TCP_StDev_and_Median_then_Append( origCSVRef )
        #END FOR
        print(" "*80, end='\r')

        #If there are any rows that still don't have any information for the TCP StDev and Median,
        # we'll put in a value that says there was no such file in the folders of raw data
        lastIndex = origCSVRef[0].index("eTCP_DOWN2_MEDIAN")
        for row in origCSVRef:
            #This creates a smaller array of the current row. If the array is empty, then
            # it means that there we no values in that row yet. We fill those cells
            # in with "FileMissingError"
            are_there_values_here = row[lastIndex-15:lastIndex+1]
            if not are_there_values_here:
                row.extend(["FileMissingError"]*16)
        #END FOR

        print("Please select the folder you wish to hold the csv file that will be created")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV File",
                                         mustexist = True)
        filename = filename.split("/")[-1].split(".")[0]
        csvExport(origCSVRef, rootOfFiles + "/" + filename + "_with_StDev_Median.csv")
    #END DEF


    # DESC: Calculates rVal and MOS for each given (test?/file?), which are values that
    #       describe the potential "Voice Over IP" (VoIP) quality of the link from the test's location
    def add_rVal_and_MOS_to_Given(self, origCSVRef, delayThresh, filename):
        #add the headers to the CSV if we need
        if (origCSVRef[0][-1] != "MOS"):
            newHeaders = ["rValue","MOS"]
            origCSVRef[0].extend(newHeaders)
        #END IF
        #This section goes through all of the tests stored in this structure and runs
        # the SpeedTestFile object's rval and MOS appending function
        for devType in self.mySpeedTestFiles:
            for carrier in self.mySpeedTestFiles[devType]:
                for speedTest in self.mySpeedTestFiles[devType][carrier]:
                    speedTest.calc_rVal_and_MOS_then_Append(origCSVRef, delayThresh)
                #END FOR
            #END FOR
        #END FOR
        #This section does the same thing as above, but it runs through the files 
        # that had no carrier information.
        for speedTest in self.bad_info_Files:
            speedTest.calc_rVal_and_MOS_then_Append(origCSVRef, delayThresh)
        #END FOR
        #If there are any rows that still don't have any information for the TCP StDev and Median,
        # we'll put in a value that says there was no such file in the folders of raw data
        lastIndex = origCSVRef[0].index("MOS")
        for row in origCSVRef:
            #This creates a smaller array of the current row. If the array is empty, then
            # it means that there we no values in that row yet. We fill those cells
            # in with "FileMissingError"
            are_there_values_here = row[lastIndex-1:lastIndex+1]
            if not are_there_values_here:
                row.extend(["FileMissingError"]*2)
        #END FOR
        print("Please select the folder you wish to hold the csv file that will be created")
        rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                         title = "Select the Folder You Wish To Hold the CSV File",
                                         mustexist = True)

        filename = filename.split("/")[-1].split(".")[0]
        csvExport(origCSVRef, rootOfFiles + "/" + filename + "_with_rVal_and_MOS.csv")
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
        #END IF
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
