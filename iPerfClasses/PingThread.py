
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




# Each subset of pings within each subset (represented by a numbered thread)
# ------------------------------------------------------------------------
# PINGTHREAD.PY
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
from .utils import readToAndGetLine
from .Pings import Ping
class PingThread():

    # ----------------
    #some tests are numbered 3, 4, 5, etc. There is also a test numbered SUM
    testNum   = 0
    localIP   = 0
    localPort = 0
    serverIP  = 0
    serverPort= 0
    datagrams = None
    # ----------------

    def __init__(self,testNum,localIP,localPort,serverIP,serverPort):
        self.this_Pings= []
        self.testNum   = testNum
        self.localIP   = localIP
        self.localPort = localPort
        self.serverIP  = serverIP
        self.serverPort= serverPort
    #END DEF

    def addPing(self,ping):
        self.this_Pings.append(ping)
    #END DEF


    def __str__(self):
        return (
               "PingThread: " + str(self.testNum) + 
               "     Pings: " + str(len(self.this_Pings))
               )

#END CLASS
