
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
    sys.exit(0)
#END __name__=='__main__'


# Small tests within each Test file
# ------------------------------------------------------------------------
# INDIVIDUALSPEEDTEST.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  ..
#
# FUNCTIONS:
#   __init__ - ..
#       INPUTS-     ..:     ..
#       OUTPUTS-    ..
#
# ------------------------------------------------------------------------
from .readTo import readToAndGetLine
from SpeedPings import SpeedPings
class SpeedTest():

    Latitude = 0.0
    Longitude = 0.0

    ## !!!!
    ## Some tests (like in WBBD) do not specifiy TCP West,TCP East,UDP West, etc.
    ## It would be better to just compare the IP address the test is connecting to
    ##  and then assign TCP/UDP West/East based on that value
    ##
    ## 184.72.222.65 = East TCP/UDP
    ## 184.72.63.139 = West TCP/UDP
    ## !!!!!
    #e.g. TCP, UDP, Ping
    ConnectionType = "UNKNOWN"
    #e.g. West, East, None
    ConnectionLoc = "UNKNOWN"

    IP = "UNKNOWN"
    Port = 0000

    WindowSz = 0 #In KByte

    pings = []

    def __init__(self):
        pass
    #END DEF
#END CLASS

