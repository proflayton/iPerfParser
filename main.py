
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
#           !!NOTE!! All of the data files should be in the same location!!
#           After parsing the data, the program will ask the user
#           what type of analysis they wish to perform.
#
# OUTPUTS-  The program, upon parsing the data and recieving a command
#           for a specific analysis, will generate CSV files of the data, 
#           or some other file type we have not implemented yet
#
# ------------------------------------------------------------------------

#Importing the necessary classes in the sub-directory
from ParserStructure.SpeedTestDataStructure import SpeedTestDS as STDs
import ParserStructure.utils as utils
import os, sys

#Here's where main actually starts
# creating a Speed Test Data Structure
recusivlyPrintFiles = True
printShortString = False
so_many_STDs = STDs(recusivlyPrintFiles, printShortString)
#Loading in the raw data, and passing in the system arguements
# The two Trues are for the STDs recursive print and quick print options
so_many_STDs.loadRawData(sys.argv)

command = True
while command:
    print("============================================\n" +
          "Please input the number/letter of the function you wish to perform:\n" +
          "  -0-  Print the structure\n" +
          "  -1-  Convert all parsed Files into CSV files\n" +
          "  -2-  Create a distribution of the standard deviations of TCP network speeds\n" +
          "       (based off the sum of speeds of all four TCP threads per Test, per File\n" +
          "  -3-  Append the standard deviation and median of the Sum threads of the TCP tests\n" +
          "       to the master CSV file included in the package\n" +
          "  -4-  Append the rValue and MOS to the CSV file\n" +
          " -q/Q- Quit")
    choice = input("--> ")
    print("============================================")
    if "0" in choice:
        print(str(so_many_STDs))
    elif "1" in choice:
        #Converting the structure of parsed raw data into a 2 dimensional array
        csvReady = so_many_STDs.convertTo_Structure_To_2D()
    elif "2" in choice:
        #Converting the structure of parsed raw data into a single 2 dimensional
        # array, which is a histogram of the standard deviation of all network speeds,
        # separated by carrier, direction, and location connected to (e.g. Verizon, Up, West)
        print("Please provide a few numbers...")
        buckets = int(input("Number of buckets in histogram: "))
        maxValue = int(input("Max Standard Deviation value allowed: "))
        so_many_STDs.convertTo_Object_To_TCPStDev(buckets, maxValue)
    elif "3" in choice:
        #Adding the StDev and Median values to the csv of file information
        #The first 3 lines declare the string of the path to the original CSV file. It
        # is then imported as a 2D array, and a reference to it is passed to the appropiate function
        this_dir, this_filename = os.path.split(__file__)
        DATA_PATH = os.path.join(this_dir, "ReferenceData", "CPUC_FieldTestResults_Q42013_Data.csv")
        originalCSV = utils.csvImport(DATA_PATH)
        so_many_STDs.add_StDev_and_Median_to_Master(originalCSV)
    elif "4" in choice:
        this_dir, this_filename = os.path.split(__file__)
        DATA_PATH = os.path.join(this_dir, "ReferenceData", "CPUC_FieldTestResults_Q42013_Data.csv")
        originalCSV = utils.csvImport(DATA_PATH)
        so_many_STDs.rValAndMosCalc(originalCSV,150)
    elif "q" in choice or "Q" in choice:
        #Ending the program
        print("Quitting operations")
        command = False
    else:
        print("This option is unknown. Please try again...")
    #END IF/ELIF/ELSE
#END WHILe


#END MAIN