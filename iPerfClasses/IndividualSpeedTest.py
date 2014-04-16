
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
# INDIVIDUALSPEEDTEST.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  This class will hold just an individual speed test (be it either a TCP or UDP test).
#           This will be where we have functions that do a lot of data analysis functions (like
#           standard deviation of TCP upload and download speed tests).
#
# FUNCTIONS:
#   __init__ - Used to initialize an object of this class
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   loadHeaderInfo - Given a string (in most cases, a line read from the file stream starting
#                    with "Iperf command line:"), this section will use the string to determine
#                    the basic information about this test
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#                   data:   a String, holding the command used to run this iPerf test, which
#                           also has all of the information we need
#       OUTPUTS-    none
#
#   createPingThreads - Given the data stream, parses the Speed Test streams into
#                       individual Ping Threads
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   dataStream: a data stream, with the rest of the Speed Test information
#       OUTPUTS-    none
#
#   getPingThreadWithNumber - This returns the PingThread object with the thread number given
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   threadNumber:   Integer, representing the ping thread's pipe/thread number
#       OUTPUTS-    realPing:       ...
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
import io
from .utils import readToAndGetLine
from .utils import global_str_padding as pad
pad = pad*2
from .PingThread import PingThread
from .Pings import Ping

class SpeedTest():

    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "UNKNOWN"
    #e.g. West, East
    ConnectionLoc = "UNKNOWN"

    RecieverIP = "UNKNOWN"
    Port = 0000

    short_str = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataStream, short=False):
        self.short_str = short
        self.this_PingThreads = []
        self.loadHeaderInfo(readToAndGetLine(dataStream, "Iperf command line:"))
        self.createPingThreads(dataStream)
    #END DEF


    # DESC:
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


    # DESC: Given the data stream, parses the Speed Test streams into individual Ping Threads
    def createPingThreads(self, dataStream):
        dataLine = readToAndGetLine(dataStream,"[")
        while dataLine:
            if dataLine.strip() == '':
                break
            else:
                #If the connection type was determined to be TCP (from the
                # loadHeaderInfo function), then parse
                if self.ConnectionType == "TCP":
                    #This section determines the pipe/thread number (i.e. 3, 4, 5, or 6)
                    temp = dataLine.split("[")[1]
                    threadNumber = temp.split("]")[0].strip()
                    temp = temp.split("]")[1]
                    #If the threadNumber is SUM, we ignore it (i.e. pass)
                    if threadNumber == "SUM":
                        pass
                    #If local is in the rest of the line, then we are starting a new thread
                    elif "local" in temp:
                        if len(self.this_PingThreads) < 4:
                            self.this_PingThreads.append(PingThread(threadNumber, "Up", temp, self.short_str))
                        else:
                            self.this_PingThreads.append(PingThread(threadNumber, "Down", temp, self.short_str))
                    #Otherwise, we are adding a new ping to our ping thread
                    else:
                        currPingThread = self.getPingThreadWithNumber(threadNumber)
                        currPingThread.addPing(Ping(temp))
                    #END IF/ELIF/ELSE
                elif self.ConnectionType == "UDP":
                    temp = dataLine.split("[")[1]
                    threadNumber = temp.split("]")[0].strip()
                    temp = temp.split("]")[1]
                    if "local" in temp:
                        self.this_PingThreads.append(PingThread(threadNumber, "Up", temp, self.short_str))
                        #print("Local")
                    elif "-" in temp:
                        if "datagrams" in temp:
                            #error with the test (datagrams received out-of-order)
                            #
                            # NOTE! This will probably need to be handled correctly later
                            # for new kinds of analysis. i.e., they may want to know
                            # how many datagrams were lost
                            #
                            dataLine = dataStream.readline()
                            continue
                        self.this_PingThreads[0].addPing(Ping(temp))
                    elif "datagrams" in temp:
                        datagrams = temp.split("Sent")[1].split("datagrams")[0].replace(" ","")
                        self.this_PingThreads[0].datagrams = datagrams
                    elif "Server Report" in temp:
                        #the report is actually a line down
                        temp = dataStream.readline()
                    #END IF/ELIFx3
                else:
                    print("ERROR! NO CONNECTION TYPE")
                    return
                #END IF/ELIF/ELSE
            #END IF/ELSE
            #This one line continues to the next line in the Test.
            # If this is deleted, Brandon and I will find who deleted it
            # and format their computer manually with a very large magnet.
            dataLine = dataStream.readline()
        #END LOOP
    #END DEF

    # DESC: Searches for the ping thread with the threadNumber provided.
    #       Gets the LATTER one so that when new ones are created, we add to that one
    def getPingThreadWithNumber(self,threadNumber):
        realPing = None
        for pingThread in self.this_PingThreads:
            if pingThread.PipeNumber == threadNumber:
                realPing = pingThread
        return realPing
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = (pad + "Connection Type: " + self.ConnectionType + "\n" +
                    pad + "Connection Location: " + self.ConnectionLoc + "\n" +
                    pad + "Reciever IP:" + self.RecieverIP + " port:" + str(self.Port) + "\n" +
                    pad + "Test Interval:" + self.TestInterval + "\n"
                   )
        for pingThread in self.this_PingThreads:
            this_str += str(pingThread)
        #END FOR
        return this_str
    #END DEF
#END CLASS
