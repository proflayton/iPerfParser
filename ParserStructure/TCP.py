
# ------------------------------------------------------------------------
# This section checks to see if the script is being run directly,
# i.e. through the command line. If it is, then it stops and exits the
# program, asking the user to use these files by running the main.py
# ------------------------------------------------------------------------
if __name__ == '__main__':
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
#   MeasurementFormat   String, the format (Kbytes, Kbits, etc.) that the data has been stored in
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
#   calc_StDev_ofTCPThreadSumsByDirection
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   structRef:  reference to the structure that will hold the standard deviation values
#                   netType:    String, the network type (mobile or netbook) that this test falls under
#                   carrier:    String, the carrier (AT&T, Verizon, etc.) that this test falls under
#       OUTPUTS-    none
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import global_str_padding as pad; pad = pad*2
from .PingThread import PingThread
from .Pings import Ping

from .IndividualSpeedTest import SpeedTest
class TCPTest(SpeedTest):

    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "TCP"
    WindowSize = 0

    ERROR = False
    ErrorMessage = None
    #---- Inherited Variables ----
    # ConnectionLoc = "UNKNOWN"
    # myPingThreads = []
    # TestNumber = 0
    # RecieverIP = "UNKNOWN"
    # Port = 0000
    # TestInterval = 0
    # MeasurementFormat = None
    # short_str_method = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString, short=False):
        self.text = dataString
        if ("Test Timed Out" in dataString) or ("timed out" in dataString):
            self.ERROR = True
            self.ErrorMessage = "Test Timed Out"
            return
        elif "Quitting operations" in dataString:
            self.ERROR = True
            self.ErrorMessage = "Test quit by User"
            return
        elif "failed:" in dataString:
            self.ERROR = True
            self.ErrorMessage = "There was an error of some kind. Please investigate"
            return
        #END IF/ELIF
        self.short_str_method = short
        self.myPingThreads = { "Up" : [], "Down" : [] }
        self.MeasurementFormat = { "Speed" : None, "Size" : None}
        #Calling the other initialization functions
        self.text = dataString.split('\n')
        self.loadHeaderInfo()
        self.createPingThreads()
        self.text = None
    #END DEF


    # DESC: ..
    def loadHeaderInfo(self):
        #This block will copy the command line call into the iPerfCommand variable,
        # as well as declare this objects TestNumber
        iPerfCommand = ""
        for line in self.text:
            if "Starting Test" in line:
                self.TestNumber = line.split(":")[0][-1]
            if "Iperf command line" in line:
                iPerfCommand = line
            if iPerfCommand != "" and self.TestNumber != 0:
                break
        #END FOR

        #Getting the Reciever IP address
        self.RecieverIP = iPerfCommand[iPerfCommand.find("-c"): ].split(" ")[1].strip()

        #Determining the Connection Location
        if self.RecieverIP == "184.72.222.65":
            self.ConnectionLoc = "East"
        if self.RecieverIP == "184.72.63.139":
            self.ConnectionLoc = "West"

        #Getting port number
        self.Port = iPerfCommand[iPerfCommand.find("-p"): ].split(" ")[1].strip()

        #Getting test time interval number
        self.TestInterval = iPerfCommand[iPerfCommand.find("-t"): ].split(" ")[1].strip()

        #Getting the window size
        self.WindowSize = iPerfCommand[iPerfCommand.find("-w"): ].split(" ")[1].strip()

        #Getting measurement format
        mform = iPerfCommand[iPerfCommand.find("-f"): ].split(" ")[1].strip()
        if mform == "k":
            self.MeasurementFormat["Speed"] = "Kbits/sec"
            self.MeasurementFormat["Size"] = "KBytes"
        elif mform == "K":
            self.MeasurementFormat["Speed"] = "KBytes/sec"
            self.MeasurementFormat["Size"] = "KBytes"
        elif mform == "m":
            self.MeasurementFormat["Speed"] = "Mbits/sec"
            self.MeasurementFormat["Size"] = "MBytes"
        elif mform == "M":
            self.MeasurementFormat["Speed"] = "MBytes/sec"
            self.MeasurementFormat["Size"] = "MBytes"
        #END IF/ELIF
    #END DEF


    # DESC: Given the data stream, parses the Speed Test streams into individual Ping Threads
    def createPingThreads(self):
        #This block does the initial organization, going through each line and
        # putting them into the array whose key corresponds with their thread number.
        tempThreads = {}
        for line in self.text:
            if "[" in line:
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
            dirSplitTempThreads["Up"][key] = []
            if key != "SUM":
                dirSplitTempThreads["Down"][key] = []
        #END FOR
        #This block goes through each thread in the first structure, and essentially
        # divides the array of strings in half, putting the Upload streams into their
        # appropiate array, and the Downloads in their's.
        for thread in tempThreads:
            #The SUM thread is only for the Upload stream, so we always know where it goes,
            # and there is no SUM thread for the Download stream
            if thread != "SUM":
                direction = ["Up", "Down"]
                dircInd = -1
                for line in tempThreads[thread]:
                    if "connected with" in line:
                        dircInd += 1
                    dirSplitTempThreads[direction[dircInd]][thread].append(line)
                #END FOR
            else:
                for line in tempThreads[thread]:
                    dirSplitTempThreads["Up"][thread].append(line)
                #END FOR
            #END IF/ELSE
        #END FOR
        #
        #
        for direction in dirSplitTempThreads:
            for thread in dirSplitTempThreads[direction]:
                self.myPingThreads[direction].append( 
                    PingThread(dirSplitTempThreads[direction][thread],\
                               thread, direction,\
                               self.MeasurementFormat["Size"], self.MeasurementFormat["Speed"],\
                               self.short_str_method) )
        #END FOR
    #END DEF

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

    # DESC: In this test, find the longest thread time among all of the threads
    def getLongestThreadTime(self):
        time = 0
        for thread in self.myPingThreads:
            for ping in thread.myPings:
                new_time = ping.secIntervalEnd
                time = new_time if new_time > time else time
        return time
    #END DEF


    # DESC: This returns the sum of the Up threads in this test
    def sum_UpThreads(self):
        Up_threads = []; Up_threads_sum = []
        for thread in self.myPingThreads:
            if (thread.DataDirection == "Up"):
                Up_threads.append(thread)
            #END IF
        #END FOR
        #Calculating max thread length by direction
        max_up_length = 0
        for thread in Up_threads:
            for ping in thread.myPings:
                new_max = ping.secIntervalEnd
                max_up_length = new_max if new_max > max_up_length else max_up_length
            #END FOR
        #END FOR
        #Get the sums of the Up and Down threads
        for step in range(int(max_up_length)):
            temp = 0
            for itr in range(len(Up_threads)):
                try: temp += Up_threads[itr].myPings[step].speed
                except: pass
            #END FOR
            Up_threads_sum.append(temp)
        #END FOR
        return Up_threads_sum
    #END DEF


    # DESC: This returns the sum of the Down threads in this test
    def sum_DownThreads(self):
        Down_threads = []; Down_threads_sum = []
        for thread in self.myPingThreads:
            if (thread.DataDirection == "Down"):
                Down_threads.append(thread)
            #END IF
        #END FOR
        #Calculating max thread length by direction
        max_down_length = 0
        for thread in Down_threads:
            for ping in thread.myPings:
                new_max = ping.secIntervalEnd
                max_down_length = new_max if new_max > max_down_length else max_down_length
            #END FOR
        #END FOR
        #Get the sums of the Up and Down threads
        for step in range(int(max_down_length)):
            temp = 0
            for itr in range(len(Down_threads)):
                try: temp += Down_threads[itr].myPings[step].speed
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
                                "  Measurement Format:" + self.MeasurementFormat["Size"] +\
                                    ", " + self.MeasurementFormat["Speed"] + "\n"
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
