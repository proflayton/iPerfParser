
# ------------------------------------------------------------------------
# Making sure that the version of python being used is at least 2.7
# ------------------------------------------------------------------------
from ParserStructure.utils import isLessThanVersion
if not isLessThanVersion((3,0)):
    raise SystemExit


# ------------------------------------------------------------------------
# MAIN.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
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

#Importing the necessary classes in the sub-directory
from ParserStructure.SpeedTestDataStructure import SpeedTestDS as STDs
import ParserStructure.utils as utils
import os, sys, datetime
import tkinter as TK, tkinter.filedialog as TKFD
#Setting up some files to use for checking data.
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "ReferenceData", "CPUC_FieldTestResults_Q42013_Data.csv")


# Here's where main actually starts
# creating a Speed Test Data Structure
so_many_STDs = STDs()
# Loading in the raw data, and passing in the system arguements
so_many_STDs.loadRawData(sys.argv)

# Converting the structure of parsed raw data into a 2 dimensional array
csvReady = so_many_STDs.convertTo_Structure_To_2D()
"""
print("Please select the folder you wish to hold the csv files that will be created")
rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                 title = "Select the Folder You Wish To Hold the CSV Files",
                                 mustexist = True)
""
rootOfFiles = os.path.expanduser("~") + "/Desktop"
""
for devType in csvReady:
    for carrier in csvReady[devType]:
        for array in csvReady[devType][carrier]:
            try: os.mkdir(rootOfFiles + "/" + "StructureToCSV")
            except: pass
            try: os.mkdir(rootOfFiles + "/" + "StructureToCSV" + "/" + devType)
            except: pass
            try: os.mkdir(rootOfFiles + "/" + "StructureToCSV" + "/" + devType + "/" + carrier)
            except: pass

            index = csvReady[devType][carrier].index(array)
            csvExport(array, rootOfFiles + "/" + "StructureToCSV" + "/" +
                             devType + "/" +
                             carrier + "/" +
                             so_many_STDs.this_SpeedTestFiles[devType][carrier][index].FileName[:-4] + ".csv")
        #END FOR
    #END FOR
#END FOR
"""

print("SD")
# Converting the structure of parsed raw data into a 2 dimensional array
csvOfTCP = so_many_STDs.convertTo_Object_To_TCPStDev(20)
rootOfFiles = os.path.expanduser("~") + "/Desktop"
utils.csvExport(csvOfTCP, rootOfFiles + "/StandardDeviationofTCPSumThreads.csv")

print("Full File")
# Adding the StDev and Median values to the csv of file information
originalCSV = utils.csvImport(DATA_PATH)
so_many_STDs.add_StDev_and_Median_to_Master(originalCSV)
utils.csvExport(originalCSV, rootOfFiles + "/CPUC_FieldTestResults_Q42013_Data_with_StDev_and_Median.csv")



#END MAIN