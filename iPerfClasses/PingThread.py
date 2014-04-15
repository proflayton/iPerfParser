
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
# PINGTHREAD.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  This object will represent a single thread, or pipe, in a network
#           speed test. It will hold an array of
#
# FUNCTIONS:
#   __init__ - Used to initialize an object of this class
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import readToAndGetLine
from .utils import global_str_padding as pad
pad = pad*3
from .Pings import Ping
class PingThread():

    # ----------------
    # Initializing some class attributes
    testNum    = 0
    localIP    = 0
    localPort  = 0
    serverIP   = 0
    serverPort = 0
    datagrams  = None
    # ----------------

    # DESC: Initializing class
    def __init__(self, testNum, data):
        #This takes the given data String and parses the object information
        data       = data.split("local")[1]
        localIP    = data.split("port")[0].replace(" ","")
        data       = data.split(localIP + " port")[1]
        localPort  = data.split("connected")[0]
        data       = data.split("connected with")[1]
        serverIP   = data.split("port")[0]
        data       = data.split("port")[1]
        serverPort = data.split("\n")[0]
        self.this_Pings = []
        self.testNum    = testNum
        self.localIP    = localIP
        self.localPort  = localPort
        self.serverIP   = serverIP
        self.serverPort = serverPort
    #END DEF

    # DESC: Adding a Ping object to this class' array of Ping objects
    def addPing(self,ping):
        self.this_Pings.append(ping)
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        return (pad + "PingThread: " + str(self.testNum)
                    + "   Pings: " + str(len(self.this_Pings))
               )

#END CLASS
