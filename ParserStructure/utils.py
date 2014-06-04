
# ------------------------------------------------------------------------
# UTILS.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  Provide a few functions that will be used in multiple modules
#
# VARIABLES:
#   global_str_padding: A string with a set number of spaces. Used in the __str__
#                       methods of all classes.
#
# FUNCTIONS:
#   testForMain - This tests if the file being run is being run as main. This is a problem (kind of) for
#               the class files like Ping_Test or TCP_Test. This function will, if __name__ is __main__, exit
#               the program, and give the user a list of file locations where main.py might be
#       INPUTS-     name:   String, the value of the programs __name__ variable
#       OUTPUTS-    none:   Exits program if conditions are met. Otherwise, nothing is returned
#
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
#       OUTPUTS-    return: Integer, representing the month index (from 1 to 12)
#
#   monthAbbrToNum -  This function takes a number index for a month and returns the name abbreviation
#       INPUTS-     num:    Integer, representing the month index (from 1 to 12)
#       OUTPUTS-    retrn:  String, abbreviation for a month (e.g. Jun, Oct, etc.)
#
#   calcStDevP - Calculates the population standard deviation of the given array
#       INPUTS-     array:  list of values that will be used in calculated StDev
#       OUTPUTS-    dev:    Integer, the StDev of the given array
#
#   calcMean - Calculates the mean of the given array of values
#       INPUTS-     array:  list of values that will be used in calculated StDev
#       OUTPUTS-    dev:    Integer, the StDev of the given array
#
#   calcTCPThroughput - Calculates the theoretical TCP Throughput of the connection whose RTT has been given
#       INPUTS-     RTT     Integer/Float, the round trip time it took to send a packet on a connection.
#                           cannot be a string, None, or 0
#                   MSS     Integer/Float, default 1024, the maximum segment size that can be sent in the TCP connection
#                           cannot be a string, None, or 0
#                   Loss    Integer/Float, default 0.01, the percentage of packets that will be lost in the connection
#                           cannot be a string, None, or 0
#       OUTPUTS-    Integer/None    Returns None if wrong type of value was given, otherwise an Integer
#
#   csvExport - Used to initialize an object of this class
#       INPUTS-     a_2D_Array:     A 2-dimensional array with each sub array representing
#                                   a line in the end csv file
#                   fileNameToSave: The full path of the resulting csv file
#       OUTPUTS-    csv file saved at given path
#
#   csvImport - Used to initialize an object of this class
#       INPUTS-     fileNameToSave: The full path of the csv file to import
#       OUTPUTS-    a_2D_Array:     A 2-dimensional array with each sub array representing
#                                   a line in the csv file
#
# ------------------------------------------------------------------------


# DESC: This section checks to see if the script is being run directly,
#       i.e. through the command line. If it is, then it stops and exits the
#       program, asking the user to use these files by running the main.py
def testForMain(name):
    if name == '__main__':
        print("Please run main.py.")

        #Changing Current Working Directory to 3 levels up
        import os
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
#END DEF
#Now I check for main (from this file, utils)
#testForMain(__name__)


#This is going to be a global variable used in the __str__ methods of all other modules
# This way, when objects are outputted, they can be indented to create a tree looking output
global_str_padding = "   "
#END GLOBAL VARS


# DESC: ..
def readToAndGetLine(fileStream, delimiter):
    line = fileStream.readline()
    while delimiter not in line:
        line = fileStream.readline()
        if not line: break
    if line and (not isLessThanVersion((3,0,0))):
        line = line[:-2] + "\n"
    return line
#END DEF

# DESC: ..
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



# DESC: Returns the population standard deviation of the given array of values.
#       If an empty array is given, it returns None, which should be ignored
def calcStDevP(array):
    if not array:
        return None
    avg = calcMean(array)
    dev = float(0)
    for elem in array:
        dev += (elem - avg)**2
    dev = (dev / len(array))**(1.0/2.0)
    return dev
#END DEF

# DESC: Returns the mean of the given array of values.
#       If an empty array is given, it returns None, which should be ignored
def calcMean(array):
    if not array:
        return None
    avg = float(0)
    for elem in array:
        avg += elem
    return (avg / len(array))
#END DEF

# DESC: This function takes in an array
#       And returns the median of the array
def getMedian(vals):
    if not vals:
        return None
    sortedVals = sorted(vals)
    if (len(sortedVals)%2 == 1):
        return sortedVals[int(len(sortedVals)/2)]
    else:
        return (sortedVals[int(len(sortedVals)/2)] + sortedVals[int(len(sortedVals)/2)-1])/2.0
#END DEF

# DESC: Given a few values (RTT is required), this function will return
#       the theoretical TCP Throughput on the connection from which the RTT was obtained.
#       RTT must be in milliseconds
#       MSS must be in bytes
#       Loss must be in percent
#       Returns the theoretical throughput in bits/sec.
def calcTCPThroughput(RTT, MSS=1024, Loss=0.000001):
    for value in [RTT, MSS, Loss]:
        if (value is None) or (isinstance(value, str)):
            return None
    #END FOR
    for value in [RTT, MSS, Loss]:
        if (value == 0):
            return 0
    #END FOR
    RTT_calc = RTT / 1000.0
    MSS_calc = MSS * 8.0 / 1024.0
    Loss_calc = Loss / 100.0
    from math import sqrt
    return ( (MSS_calc / RTT_calc) / sqrt(Loss_calc) )
#END DEF



# DESC: This fuction takes in two values:
#       The 2D representing the rows and columns in the CSV
#       The fileName in which the CSV will be saved to
def csvExport(a_2D_Array, fileNameToSave):
    f = open(fileNameToSave,"w")
    for row in a_2D_Array:
        rowOfText = ''
        for col in row:
            rowOfText += ('"' + str(col) + '",')
        f.write(rowOfText[:-1]+"\n")
    f.close()
#END DEF

# DESC: This function takes the path to a .csv file
#       and imports it as a 2-D array
def csvImport(fileNameToImport):
    a_2D_Array = []
    f = open(fileNameToImport,"r")
    line = f.readline()
    while line:
        a_1D_Array = []
        cols = line.split(",")
        for c in cols:
            a_1D_Array.append(c.replace("\n","").replace("\n\r",""))
        #END FOR
        a_2D_Array.append(a_1D_Array)
        line = f.readline().replace("\n","").replace("\n\r","")
    #END WHILE
    return a_2D_Array
#END DEF



#  ------------------------------------------
# In case you every need to have a one line method to print out elements in
# an array, use list comprehension.
# e.g.
#     [print(line) for line in dataArr]
#    
# The basic structure is as such...
#
# new_list = [expression(i) for i in old_list if filter(i)]
#    [ expression for item in list if conditional ]
#  ------------------------------------------


