
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
import io
from .utils import readToAndGetLine
from .utils import global_str_padding as pad
pad = pad*2
from .PingThread import PingThread

class SpeedTest():

    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "UNKNOWN"
    #e.g. West, East
    ConnectionLoc = "UNKNOWN"

    RecieverIP = "UNKNOWN"
    Port = 0000

    TestInterval = 0

    this_PingThreads = []

    # ------------------------

    def __init__(self, dataStream):
        self.loadHeaderInfo(readToAndGetLine(dataStream, "Iperf command line:"))
        self.createPingThreads(dataStream)
    #END DEF


    def loadHeaderInfo(self, data):
        #splitting the first line from the rest of the data
        iPerfCommand = data.split("\n", 1)[0]

        #Finding the connection type
        if iPerfCommand.find("-e")>0:
            self.ConnectionType = "TCP"
        if iPerfCommand.find("-u")>0:
            self.ConnectionType = "UDP"

        #Getting the Reciever IP address
        c_opt_strt = iPerfCommand.find("-c")+3
        c_opt_end = iPerfCommand.find(" ", c_opt_strt)+1
        if (c_opt_end != 0):
            self.RecieverIP = iPerfCommand[c_opt_strt:c_opt_end]
        else:
            self.RecieverIP = iPerfCommand[c_opt_strt:]

        #Determining the Connection Location
        if self.RecieverIP == "184.72.222.65":
            self.ConnectionLoc = "East"
        if self.RecieverIP == "184.72.63.139":
            self.ConnectionLoc = "West"

        #Getting port number
        p_opt_strt = iPerfCommand.find("-p")+3
        p_opt_end = iPerfCommand.find(" ", p_opt_strt)+1
        if (p_opt_end != 0):
            self.Port = iPerfCommand[p_opt_strt:p_opt_end]
        else:
            self.Port = iPerfCommand[p_opt_strt:]

        #Getting test time interval number
        t_opt_strt = iPerfCommand.find("-t")+3
        t_opt_end = iPerfCommand.find(" ", t_opt_strt)+1
        if (t_opt_end != 0):
            self.TestInterval = iPerfCommand[t_opt_strt:t_opt_end]
        else:
            self.TestInterval = iPerfCommand[t_opt_strt:]
        #END IF/ELSE
    #END DEF


    def createPingThreads(self, dataStream):
        a = True
        while a:
            a = dataStream.readline()
            if a == b"\n":
                a = False
    #END DEF


    def __str__(self):
        this_str = (pad + " Connection Type: " + self.ConnectionType + "\n" +
                    pad + " Connection Location: " + self.ConnectionLoc + "\n" +
                    pad + " Reciever IP:" + self.RecieverIP + " port:" + str(self.Port) + "\n" +
                    pad + " Test Interval:" + self.TestInterval + "\n"
                   )
        return this_str
    #END DEF
#END CLASS
