
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
# UDP.PY
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
#   DatagramSize        The size of datagrams that will be sent
#   TargetBandwidth     String, the targetted bandwidth to be used in this test
#   ConnectionLoc       String, represents where this test is connected to (East or West)
#   myPingThreads       list, holding all of the PingThreads in this test
#   RecieverIP          String, IP of the server this test is connected to
#   Port                Integer, the port this test is connected to
#   TestInterval        Integer, the length of time that the test will be run
#   MeasurementFormat   String, the format (Kbytes, Kbits, etc.) that the data has been stored in
#   short_str           Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
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
#   getPingThreadWithNum - This returns the PingThread object with the thread number given
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   threadNumber:   Integer, representing the ping thread's pipe/thread number
#       OUTPUTS-    realPingThread: A Ping thread object, which was the last thread whose thread number
#                                   was given to the function
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
import io
from .utils import global_str_padding as pad; pad = pad*2
from .PingThread import PingThread
from .Pings import Ping

from .IndividualSpeedTest import SpeedTest
class UDPTest(SpeedTest):

    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "UDP"
    DatagramSize = 0
    TargetBandwidth = None  #n[KM]

    ERROR = False
    ErrorMessage = None
    #---- Inherited Variables ----
    # ConnectionLoc = "UNKNOWN"
    # myPingThreads = []
    # RecieverIP = "UNKNOWN"
    # Port = 0000
    # TestInterval = 0
    # MeasurementFormat = None
    # short_str = False
    # ------------------------

"""
    # DESC: Initializing class
    def __init__(self, dataString, short=False):
        self.short_str = short
        self.myPingThreads = []
        self.loadHeaderInfo(dataString)
        self.createPingThreads(dataString)
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
                        if len(self.myPingThreads) < 4:
                            self.myPingThreads.append(PingThread(threadNumber, "Up", temp, self.short_str))
                        else:
                            self.myPingThreads.append(PingThread(threadNumber, "Down", temp, self.short_str))
                    #Otherwise, we are adding a new ping to our ping thread
                    else:
                        currPingThread = self.getPingThreadWithNum(threadNumber)
                        currPingThread.addPing(Ping(temp))
                    #END IF/ELIF/ELSE
                elif self.ConnectionType == "UDP":
                    temp = dataLine.split("[")[1]
                    threadNumber = temp.split("]")[0].strip()
                    currPingThread = self.getPingThreadWithNum(threadNumber)
                    temp = temp.split("]")[1]
                    if "WARNING" in temp:
                        #An error with UDP happens here. Don't know how to handle yet
                        currPingThread.ERROR = True
                    elif "local" in temp:
                        #new UDP pingThread
                        self.myPingThreads.append(PingThread(threadNumber, "Up", temp, self.short_str))
                        #print("Local")
                    elif "-" in temp:
                        #Some actual Data we can use, as long as there is no error
                        if "datagrams" in temp:
                            #error with the test (datagrams received out-of-order)
                            #
                            # NOTE! This will probably need to be handled correctly later
                            # for new kinds of analysis. i.e., they may want to know
                            # how many datagrams were lost
                            #
                            dataLine = dataStream.readline()
                            continue

                        #if no error, go ahead and add the ping
                        currPingThread.addPing(Ping(temp))
                    elif "datagrams" in temp:
                        #End of the test, just getting more info about what happened
                        datagrams = temp.split("Sent")[1].split("datagrams")[0].replace(" ","")
                        currPingThread.datagrams = datagrams
                    elif "Server Report" in temp:
                        #the report is actually a line down
                        temp = dataStream.readline()
                        #Here we need to go ahead and parse the report
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

        #Checking for empty or 1 Ping TCP threads
        for thread in self.myPingThreads:
            if self.ConnectionType == "TCP":
                if len(thread.myPings) < 2:
                    index = self.myPingThreads.index(thread)
                    self.myPingThreads[index] = None
                else:
                    final_ping = thread.myPings.pop()
                    thread.final_secIntervalStart = final_ping.secIntervalStart
                    thread.final_secIntervalEnd   = final_ping.secIntervalEnd
                    thread.final_size             = final_ping.size
                    thread.final_speed            = final_ping.speed
                #END IF/ELSE
            #END IF
        #END FOR
        #This needs to be outside of the FOR loop so that the element
        # after the removed one is not skipped
        while None in self.myPingThreads:
            self.myPingThreads.remove(None)
    #END DEF

    # DESC: Searches for the ping thread with the threadNumber provided.
    #       Gets the LATTER one so that when new ones are created, we add to that one
    def getPingThreadWithNum(self, threadNumber):
        realPingThread = None
        for pingThread in self.myPingThreads:
            if (pingThread.PipeNumber == threadNumber):
                realPingThread = pingThread
        return realPingThread
    #END DEF


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
        if self.short_str:
            this_str = (pad + "Connection Type: " + self.ConnectionType + "\n" +
                        pad + "Connection Location: " + self.ConnectionLoc + "\n"
                       )
            for pingThread in self.myPingThreads:
                this_str += str(pingThread)
        else:
            this_str = (pad + "Connection Type: " + self.ConnectionType + "\n" +
                        pad + "Connection Location: " + self.ConnectionLoc + "\n" +
                        pad + "Reciever IP:" + self.RecieverIP + " port:" + str(self.Port) + "\n" +
                        pad + "Test Interval:" + self.TestInterval + "\n"
                       )
            for pingThread in self.myPingThreads:
                this_str += str(pingThread)
            #END FOR
        return this_str
    #END DEF
"""
#END CLASS
