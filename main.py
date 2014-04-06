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

from iPerfClasses import speedTest
import os, sys
import Tkinter as TK, tkFileDialog as TKFD


#cheat for not having to select the folder every time.
#change string in os.walk to be the absolute path to the data files
#In command line, use "python main.py -c"
# use "python main.py -cs" to only test on 3 files (one of each type)
if (len(sys.argv) > 1):
    if (sys.argv[1] == "-c"):
        for root, dirs, files in os.walk("/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/"):
            for aFile in files:
                print( speedTest.speedTest(os.path.join(root, aFile)) )
    elif (sys.argv[1] == "-cs"):
        file1 = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/10_17_2013/99000344556962-10172013151027.txt"
        file2 = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/10_17_2013/356420059231100-10172013094856.txt"
        file3 = "/Users/peterwalker/Documents/School/+ CSUMB Courses/CPUC/Raw Data/bb results/10_17_2013/WBBDTest2-10172013151943.txt"

        print(str( speedTest.speedTest(file1) ))
        print(str( speedTest.speedTest(file2) ))
        print(str( speedTest.speedTest(file3) ))
    else:
        print("I don't know that option. I'm just a silly computer. I know -c and -cs")
    #END IF/ELIF/ELSE
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
            print( speedTest.speedTest(os.path.join(root, aFile)) )

    """ Cool example code of os.walk()

    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    import os
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    """
#END IF/ELSE
