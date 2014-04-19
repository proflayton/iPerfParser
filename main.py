
# ------------------------------------------------------------------------
# Making sure that the version of python being used is at least 2.7
# ------------------------------------------------------------------------
from iPerfClasses.utils import isLessThanVersion
if not isLessThanVersion((2,6)):
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

from iPerfClasses.SpeedTestDataStructure import SpeedTestDS as STDs
from iPerfClasses.CSVExporter import csvExport
import os
import sys
if not isLessThanVersion((3,0)):
    import Tkinter as TK, tkFileDialog as TKFD
else:
    import tkinter as TK, tkinter.filedialog as TKFD

# Here's where main actually starts
# creating a Speed Test Data Structure
so_many_STDs = STDs()
# Loading in the raw data, and passing in the system arguements
so_many_STDs.loadRawData(sys.argv)

#import pprint
#pprint.pprint(so_many_STDs.this_SpeedTestFiles, depth=4)

# Converting the structure of parsed raw data into a 2 dimensional array
csvReady = so_many_STDs.convertTo_StructureTo2D()

# Converting the structure of parsed raw data into a 2 dimensional array
csvOfTCP = so_many_STDs.convertTo_ObjectToTCP(10)
rootOfFiles = os.path.expanduser("~") + "/Desktop"
csvExport(csvOfTCP, rootOfFiles + "/Standard Deviation of TCP Sum Threads.csv")

#pprint.pprint(csvReady, depth=4)
#pprint.pprint(so_many_STDs.this_SpeedTestFiles, depth=4)

"""
print("Please select the folder you wish to hold the csv files that will be created")
rootOfFiles = TKFD.askdirectory( initialdir = os.path.expanduser("~"),
                                 title = "Select the Folder You Wish To Hold the CSV Files",
                                 mustexist = True)
"""
rootOfFiles = os.path.expanduser("~") + "/Desktop"

"""
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
            csvExport(array, rootOfFiles + "/" +
                             devType + "/" +
                             carrier + "/" +
                             so_many_STDs.this_SpeedTestFiles[devType][carrier][index].FileName[:-4] + ".csv")
        #END FOR
    #END FOR
#END FOR
"""



#Used this section to test that the conversion done in the
# STDs class was working correctly
"""
import random
x = {
     "mobile"  : {},
     "netbook" : {}
    }
for key in x:
    for elem in ["A", "B", "C", "D"]:
        x[key][elem] = {
                        "Up" : [random.randint(0, 30),random.randint(0, 30),random.randint(0, 30),
                                random.randint(0, 30),random.randint(0, 30),random.randint(0, 30),
                                random.randint(0, 30),random.randint(0, 30),random.randint(0, 30),
                                random.randint(0, 30),random.randint(0, 30),random.randint(0, 30)] ,
                        "Down" : [random.randint(0, 15),random.randint(0, 15),random.randint(0, 15),
                                  random.randint(0, 15),random.randint(0, 15),random.randint(0, 30),
                                  random.randint(0, 15),random.randint(0, 15),random.randint(0, 30),
                                  random.randint(0, 15),random.randint(0, 15),random.randint(0, 30)]
                       }
    #END FOR
#END FOR
x = so_many_STDs.convertTo_TCP_to_2D(x, 10)
csvExport(x, rootOfFiles + "/testing_convert.csv")
"""


#END MAIN