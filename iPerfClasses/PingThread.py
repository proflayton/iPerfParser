
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
    PipeNumber    = 0
    DataDirection = ""

    LocalIP       = 0
    LocalPort     = 0
    ServerIP      = 0
    ServerPort    = 0

    Datagrams     = None
    this_Pings    = []

    short_str     = False
    # ----------------

    # DESC: Initializing class
    def __init__(self, threadNum, direction, data, short=False):
        #This takes the given data String and parses the object information
        self.short_str = short
        data            = data.split("local", 1)[1].strip()
        data_localIP    = data.split("port")[0].strip()
        data            = data.split("port", 1)[1].strip()
        data_localPort  = data.split("connected")[0].strip()
        data            = data.split("connected with", 1)[1].strip()
        data_serverIP   = data.split("port", 1)[0].strip()
        data            = data.split("port", 1)[1].strip()
        data_serverPort = data.split("\n")[0].strip()
        self.this_Pings    = []
        self.PipeNumber    = threadNum
        self.DataDirection = direction
        self.LocalIP       = data_localIP
        self.LocalPort     = data_localPort
        self.ServerIP      = data_serverIP
        self.ServerPort    = data_serverPort
    #END DEF

    # DESC: Adding a Ping object to this class' array of Ping objects
    def addPing(self,ping):
        self.this_Pings.append(ping)
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = (pad + "Pipe Number: " + str(self.PipeNumber) + "\n" +
                    pad + "Data Direction: " + self.DataDirection + "\n" +
                    pad + "Local: " + str(self.LocalIP) + ":" + str(self.LocalPort) + "\n" +
                    pad + "Server: " + str(self.ServerIP) + ":" + str(self.ServerPort) + "\n"
                   )
        if self.short_str:
            this_str += pad + "Number of Pings: " + str(len(self.this_Pings)) + "\n"
        else:
            for ping in self.this_Pings:
                this_str += str(ping) + "\n"
            #END FOR
        return this_str

#END CLASS
