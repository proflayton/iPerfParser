

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
# UTILS.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  Provide a few functions that will be used in multiple modules
#
# FUNCTIONS:
#   readToAndGetLine -  Given a file stream, reads the stream until the delimiter is found
#       INPUTS-     fileStream:         FileStream object, called with open(FILEPATH, 'r')
#                   delimiter:          String, the text that you are looking for
#       OUTPUTS-    line:               String, containing the fully read line that contained the delimiter
#
#   isLessThanVersion -  This version will check the current python build's version number
#                       against 2.7. If the version is left, exit the module
#       INPUTS-     none
#       OUTPUTS-    SystemExit:     Upon conditons being met, the program will terminiate
#
#   monthAbbrToNum -  This function takes an abbreviation for a month name and returns the number index
#       INPUTS-     date:   String, abbreviation for a month (e.g. Jun, Oct, etc.)
#       OUTPUTS-    ..:     Integer, representing the month index (from 1 to 12)
#
#   monthAbbrToNum -  This function takes a number index for a month and returns the name abbreviation
#       INPUTS-     num:    Integer, representing the month index (from 1 to 12)
#       OUTPUTS-    ..:     String, abbreviation for a month (e.g. Jun, Oct, etc.)
#
# ------------------------------------------------------------------------

#This is going to be a global variable used in the __str__ methods of all other modules
# This way, when objects are outputted, they can be indented to create a tree looking output
global_str_padding = "   "
#END GLOBAL VARS


def readToAndGetLine(fileStream, delimiter):
    line = fileStream.readline()
    while delimiter not in line:
        line = fileStream.readline()
        if not line: break
    if line and (not isLessThanVersion((3,0,0))):
        line = line[:-2] + "\n"
    return line
#END DEF

def isLessThanVersion(minVer):
    if type(minVer) is tuple:
        import sys
        # Comparing the version info in the sys module to the version 2.7
        if sys.version_info < minVer:
            return False
        return True
    raise ValueError("You need to pass in a tuple the compare the current version to.")
#END DEF

# Found on http://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
# Code written by user Gi0rgi0s
def monthAbbrToNum(date):
    return{ 'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9,
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
            }[date]
#END DEF
def monthNumToAbbr(num):
    return{ 1 : 'Jan',
            2 : 'Feb',
            3 : 'Mar',
            4 : 'Apr',
            5 : 'May',
            6 : 'Jun',
            7 : 'Jul',
            8 : 'Aug',
            9 : 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
            }[num]
#END DEF
