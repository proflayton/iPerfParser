

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



# Each subset of pings within each subset (represented by a numbered thread)
# ------------------------------------------------------------------------
# SPEEDPINGS.PY
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
from .Pings import Ping
class SpeedPings():
    localHost = "UNKNOWN"
    localPort = 0
    serverHost = "UNKNWON"
    serverPort = 0

    #some tests are numbered 3, 4, 5, etc. There is also a test numbered SUM
    numTest = 0

    pings = []

    def __init__(self):
        pass
    #END DEF
#END CLASS

