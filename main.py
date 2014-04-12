
# ------------------------------------------------------------------------
# Making sure that the version of python being used is at least 2.7
# ------------------------------------------------------------------------
from iPerfClasses.utils import isLessThanVersion
if not isLessThanVersion((2,6)):
    raise SystemExit


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

from iPerfClasses.SpeedTestDataStructure import SpeedTestDS as STDs
import os
import sys

# Here's where main actually starts
# creating a Speed Test Data Structure
MainSpeedTestDS = STDs()
# Loading in the raw data, and passing in the system arguements
MainSpeedTestDS.loadRawData(sys.argv)

print(str(MainSpeedTestDS))
