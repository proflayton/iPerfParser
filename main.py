
# ------------------------------------------------------------------------
# Making sure that the version of python being used is at least 3.0
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


#Here's where main actually starts
# creating a Speed Test Data Structure
recusivlyPrintFiles = True
printShortString = True
so_many_STDs = STDs(recusivlyPrintFiles, printShortString)
#Loading in the raw data, and passing in the system arguements
# The two Trues are for the STDs recursive print and quick print options
so_many_STDs.loadRawData(sys.argv)
#print(str(so_many_STDs))

"""
# Converting the structure of parsed raw data into a 2 dimensional array
print("Structure")
csvReady = so_many_STDs.convertTo_Structure_To_2D()
"""

"""
# Converting the structure of parsed raw data into a 2 dimensional array
print("SD")
csvOfTCP = so_many_STDs.convertTo_Object_To_TCPStDev(20, 8000)
rootOfFiles = os.path.expanduser("~") + "/Desktop"
utils.csvExport(csvOfTCP, rootOfFiles + "/StandardDeviationofTCPSumThreads.csv")
"""

"""
# Adding the StDev and Median values to the csv of file information
print("Full File")
originalCSV = utils.csvImport(DATA_PATH)
so_many_STDs.add_StDev_and_Median_to_Master(originalCSV)
utils.csvExport(originalCSV, rootOfFiles + "/CPUC_FieldTestResults_Q42013_Data_with_StDev_and_Median.csv")
"""


#END MAIN