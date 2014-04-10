
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
    ## !!!!
    ## Some tests (like in WBBD) do not specifiy TCP West,TCP East,UDP West, etc.
    ## It would be better to just compare the IP address the test is connecting to
    ##  and then assign TCP/UDP West/East based on that value
    ##
    ## 184.72.222.65 = East TCP/UDP
    ## 184.72.63.139 = West TCP/UDP
    """
        Here's what I've found in my analysis of the iperf commands.
            read line is always "Iperf command line:___"
            where ___ is the start of the command.
            there is always a space between the command in the options

        OPTIONS----
        ALL
        -c ____ = client IP (East or West)
        -p ____ = port
        -i 1 = why always 1?
        -f ____ = ?????
        -t ____ = time????

        TCP:
        -e = use TCP?
        -P ____ = # of channels (local ports connected with client IP:port)
        -w ____ = window size
           -t 10 != 10 second long tests!!!
           -t 10 results in a 10 second long test and then a longer test (arbitrary length, 35sec -> 50sec long)

        UDP:
        -u = use UDP?
        -l ____ = datagram size in bytes
        -t 1 == 1 second test
        -t 5 == 5 second test
        -b ____ = transmit speed in Kbits/sec
    """
    ## !!!!!

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

    def __init__(self, data):
        self.loadHeaderInfo(data)
        self.createPingThreads(data)
        #self.allText = None
    #END DEF


    def loadHeaderInfo(self, data):
        #splitting the first line from the rest of the data
        iPerfCommand = data.split("\n", 1)[0]

        #We have a string, but we want to treat it as a stream so 
        #that we can use our other functions 
        dataStream = io.StringIO(data)

        #dataIO = io.StringIO(data)

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

        if self.ConnectionType == "TCP":
            create_multiple_ping_threads = True
            pingLine = readToAndGetLine(dataStream,"[")
            while(pingLine != None):
                threadNumber  = pingLine[pingLine.find("[")+1 : pingLine.find("]")].replace(" ","")
                if "local " in pingLine:
                    print(pingLine)
                else:
                    intervalStart = pingLine[pingLine.find("]")+1 : pingLine.find("-")].replace(" ","")
                    intervalEnd   = pingLine[pingLine.find("-")+1 : pingLine.find("s")].replace(" ","")
                    speed = pingLine[pingLine.find("KBytes")+6:pingLine.find("Kbites/sec")-9].replace(" ","")
                    
                    if intervalStart == "SUM": 
                        pass
                    else:
                        pass

                    #print(speed)
                    #import sys
                    #sys.exit()
                pingLine = readToAndGetLine(dataStream,"[")
        else:
            create_one_ping_thread = True



        #END IF/ELSE
    #END DEF


    def createPingThreads(self, data):
        a = False
    #END DEF


    def __str__(self):
        this_str = (pad + " Connection Type: " + self.ConnectionType + "\n" +
                    pad + " Connection Location: " + self.ConnectionLoc + "\n" +
                    pad + " Reciever IP:" + self.RecieverIP + " port:" + str(self.Port) + "\n" +
                    pad + " Test Interval:" + self.TestInterval + "\n"
                   )
        for elem in self.this_PingThreads:
            this_str += pad + str(elem, add_pad+pad) + "\n"
        return ""
        return this_str
    #END DEF
#END CLASS
