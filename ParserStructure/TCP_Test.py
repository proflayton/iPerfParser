
# ------------------------------------------------------------------------
# This block checks to see if the script is being run directly,
# i.e. through the command line. If it is, then it stops and exits the
# program, asking the user to use these files by running the main.py
# ------------------------------------------------------------------------
try:
    from .utils import testForMain
except:
    from utils import testForMain
testForMain(__name__)


# ------------------------------------------------------------------------
# TCP.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This class will hold just an individual speed test (be it either a TCP or UDP test).
#           This will be where we have functions that do a lot of data analysis functions (like
#           standard deviation of TCP upload and download speed tests).
#
# VARIABLES:
#   ConnectionType      String, represents the type of connection (TCP or UDP)
#   WindowSize          Integer, the size of TCP window to be used in this test
#   ConnectionLoc       String, represents where this test is connected to (East or West)
#   myPingThreads       list, holding all of the PingThreads in this test
#   RecieverIP          String, IP of the server this test is connected to
#   Port                Integer, the port this test is connected to
#   TestInterval        Integer, the length of time that the test will be run
#   MeasuringFmt        String, the format (Kbytes, Kbits, etc.) that the data has been stored in
#   short_str_method           Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                           Default is False
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
#   getLongestThreadTime - The looks through all of the threads in this function and
#                          returns the longest thread time in seconds
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    time:   Integer, representing the longest thread time
#
#   sumSpeed_UpThreads - Creating an array of the sum of each 1 second interval of all 4 thread's speed
#       INPUTS-     self:               reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    Up_Threads_sum:     an array containing values representing the sum of each 4 threads' speed
#
#   sumSpeed_DownThreads - Creating an array of the sum of each 1 second interval of all 4 thread's speed
#       INPUTS-     self:               reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    Down_Threads_sum:   an array containing values representing the sum of each 4 threads' speed
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import global_str_padding as pad; pad = pad*2
from .IndividualSpeedTest import SpeedTest
from .PingThread import PingThread
from .Pings import Ping

class TCPTest(SpeedTest):
    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "TCP"
    WindowSize = 0

    #---- Inherited Variables ----
    # ConnectionLoc = "UNKNOWN"
    # myPingThreads = []
    # TestNumber = 0
    # RecieverIP = "UNKNOWN"
    # Port = 0000
    # TestInterval = 0
    # MeasuringFmt = None
    # iPerfCommand = ""
    # ERROR = False
    # ErrorMessage = None
    # short_str_method = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString, testNum=0, short=False):
        #Call the parent class' __init__
        SpeedTest.__init__(self, dataString, testNum, short)
        if not self.ERROR:
            #Getting the window size
            self.WindowSize = self.iPerfCommand[self.iPerfCommand.find("-w"):].split(" ")[1].strip()
            #Declaring and creating the Ping Threads for this test
            self.myPingThreads = { "Up" : [], "Down" : [] }
            self.SumThread = None
            self.createPingThreads()
            self.text = None
    #END DEF


    # DESC: Given the data stream, parses the Speed Test streams into individual Ping Threads
    def createPingThreads(self):
        #This block does the initial organization, going through each line and
        # putting them into the array whose key corresponds with their thread number.
        tempThreads = {}
        for line in self.text:
            if ("[" in line) and ("SUM" not in line):
                newKey = line.split("]")[0][1:].strip()
                if newKey not in tempThreads.keys():
                    tempThreads[newKey] = []
                #END IF
                tempThreads[newKey].append(line)
            #END IF
        #END FOR
        #This block does the initial declaration of further organization, setting up
        # the structure to separate the Upload threads from the Download threads.
        dirSplitTempThreads = {"Up":{},"Down":{}}
        for key in list(tempThreads):
            dirSplitTempThreads["Down"][key] = []
            dirSplitTempThreads["Up"][key] = []
        #END FOR
        #This block goes through each thread in the first structure, and essentially
        # divides the array of strings in half, putting the Upload streams into their
        # appropiate array, and the Downloads in their's.
        for thread in tempThreads:
            direction = ["Up", "Down"]
            dircInd = -1
            for line in tempThreads[thread]:
                if "connected with" in line:
                    dircInd += 1
                dirSplitTempThreads[direction[dircInd]][thread].append(line)
            #END FOR
        #END FOR
        #Sorting the arrays of threads, as they are now organized by thread and direction
        for direction in dirSplitTempThreads:
            for thread in dirSplitTempThreads[direction]:
                temp = sorted(dirSplitTempThreads[direction][thread])
                start = temp.pop(-1); end = temp.pop(1)
                dirSplitTempThreads[direction][thread] = [start]
                dirSplitTempThreads[direction][thread].extend(temp)
                dirSplitTempThreads[direction][thread].append(end)
        #END FOR
        #Now pass each array of Pings (as Strings) to the PingThread constructor
        for direction in dirSplitTempThreads:
            for thread in dirSplitTempThreads[direction]:
                self.myPingThreads[direction].append( 
                    PingThread(dirSplitTempThreads[direction][thread],\
                               thread, direction,\
                               self.MeasuringFmt["Size"],\
                               self.MeasuringFmt["Speed"],\
                               self.short_str_method) )
        #END FOR
    #END DEF


    # DESC: In this test, find the longest thread time among all of the threads
    def getLongestThreadTime(self):
        time = 0
        for direction in self.myPingThreads:
            for thread in self.myPingThreads[direction]:
                new_time = thread.myPings[-1].secIntervalEnd
                time = new_time if new_time > time else time
        #END FOR
        return time
    #END DEF


    # DESC: This returns the sum of the Up threads in this test
    def sumSpeed_UpThreads(self):
        Up_threads_sum = []
        #Calculating max thread length
        max_up_length = 0
        for thread in self.myPingThreads["Up"]:
            new_max = int(thread.myPings[-1].secIntervalEnd)
            max_up_length = new_max if new_max > max_up_length else max_up_length
        #END FOR
        #Get the sums of the Up and Down threads
        for step in range(max_up_length):
            temp = 0
            for itr in range(len(self.myPingThreads["Up"])):
                try: temp += self.myPingThreads["Up"][itr].myPings[step].speed
                except: pass
            #END FOR
            Up_threads_sum.append(temp)
        #END FOR
        return Up_threads_sum
    #END DEF


    # DESC: This returns the sum of the Down threads in this test
    def sumSpeed_DownThreads(self):
        Down_threads_sum = []
        #Calculating max thread length by direction
        max_down_length = 0
        for thread in self.myPingThreads["Down"]:
            new_max = int(thread.myPings[-1].secIntervalEnd)
            max_down_length = new_max if new_max > max_down_length else max_down_length
        #END FOR
        #Get the sums of the Up and Down threads
        for step in range(max_down_length):
            temp = 0
            for itr in range(len(self.myPingThreads["Down"])):
                try: temp += self.myPingThreads["Down"][itr].myPings[step].speed
                except: pass
            #END FOR
            Down_threads_sum.append(temp)
        #END FOR
        return Down_threads_sum
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        if self.ERROR:
            return self.text.strip('\n\n')
        else:
            if self.short_str_method:
                this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                            pad + "Connection Type: " + self.ConnectionType + "\n" +
                            pad + "Connection Location: " + self.ConnectionLoc + "\n"
                           )
                for direction in self.myPingThreads:
                    for pingThread in self.myPingThreads[direction]:
                        this_str += str(pingThread)
                #END FOR
            else:
                this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                            pad + "Connection Type: " + self.ConnectionType + "\n" +
                            pad + "Connection Location: " + self.ConnectionLoc + "\n" +
                            pad + "Reciever IP:" + self.RecieverIP + " port:" + str(self.Port) + "\n" +
                            pad + "Test Interval:" + self.TestInterval +\
                                "  Window Size:" + self.WindowSize +\
                                "  Measurement Format:" + self.MeasuringFmt["Size"] +\
                                    ", " + self.MeasuringFmt["Speed"] + "\n"
                           )
                for direction in self.myPingThreads:
                    for pingThread in self.myPingThreads[direction]:
                        this_str += str(pingThread)
                #END FOR
            #END IF/ELSE
            return this_str
        #END IF/ELSE
    #END DEF
#END CLASS
