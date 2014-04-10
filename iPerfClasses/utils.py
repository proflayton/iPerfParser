
# ------------------------------------------------------------------------
# UTILS.PY
#
# AUTHOR(S):    Brandon Layton, Peter Walker
#
# PURPOSE-  Provide a few functions that will be used in multiple modules
#
# FUNCTIONS:
#   readToAndGetLine -  Given a file stream, reads the stream until the delimiter is found
#       INPUTS-     fileStream:         FileStream object, called with open(FILEPATH, 'r')
#                   delimiter:          String, the text that you are looking for
#       OUTPUTS-    line:               String, containing the fully read line that contained the delimiter
#
#   checkMinVersion -  This version will check the current python build's version number
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
global_str_padding = "   "
#END GLOBAL VARS


def readToAndGetLine(fileStream, delimiter):
    line = fileStream.readline()
    while delimiter not in line:
        line = fileStream.readline()
        if not line: break
    if line and (not checkVersion((3,0,0))):
        line = line[:-2] + "\n"
    return line
#END DEF

def checkVersion(minVer):
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
