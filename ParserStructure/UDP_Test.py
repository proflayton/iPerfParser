
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
#   DatagramzSent       Integer, parsed from status line in test
#   ServerReport        Dictionary, holds the server report ping, time, and number of datagrams out of order
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
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import global_str_padding as pad; pad = pad*2
from .IndividualSpeedTest import SpeedTest
from .PingThread import PingThread
from .Pings import Ping

class UDPTest(SpeedTest):
    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "UDP"
    DatagramSize = 0
    TargetBandwidth = None  #n[KM]

    DatagramzSent = 0
    ServerReport = None

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
        iPerfCommand = SpeedTest.__init__(self, dataString, testNum, short)
        if not self.ERROR:
            #Getting the datagram size
            self.DatagramSize = self.iPerfCommand[self.iPerfCommand.find("-l"):].split(" ")[1].strip()
            #Getting the datagram size
            self.TargetBandwidth = self.iPerfCommand[self.iPerfCommand.find("-b"):].split(" ")[1].strip()
            #Declaring and creating the Ping Threads for this test
            self.myPingThreads = []
            self.createPingThread()
            self.text = None
    #END DEF


    # DESC: Given the data stream, parses the Speed Test streams into individual Ping Threads
    def createPingThread(self):
        dataArray = []
        for line in self.text:
            if ("[" in line):
                if ("datagrams" in line):
                    break
                dataArray.append(line)
        #END FOR
        self.myPingThreads.append( PingThread(dataArray, 3, "Up", \
                                              self.MeasuringFmt["Size"], self.MeasuringFmt["Speed"], \
                                              self.short_str_method) )
        for line in self.text:
            #These two lines check that the correct line is gotten.
            # First initialize an array of strings (which will be used as refernece).
            # Next, for each elem in the array, check if it is in the line we are checking.
            #   (this is everything in the parenthesis)
            # Then, use all of the returned array. The code in the parenthesis returns an array of
            #  booleans, and all() makes sure that they are all True.
            # If the conditions are met, this line is the line we are looking for.
            #
            # Sadly, it means that these are not the droids we are looking for
            #
            strCheck = ["datagrams", "Sent"]
            if all(text in line for text in strCheck):
                self.DatagramzSent = line.split("Sent ")[1].split(" ")[0]
            # If "Server Report" is in the line, we need the next line
            elif "Server Report" in line:
                self.ServerReport = { "Ping": None, "Time": None,
                                      "Datagrams_OutofOrder": None
                                    }
                text = self.text[self.text.index(line)+1]
                self.ServerReport["Ping"] = Ping(text, self.MeasuringFmt["Size"], self.MeasuringFmt["Speed"])
                self.ServerReport["Time"] = text.split("/sec")[1].split("ms")[0].strip() + " ms"
                self.ServerReport["Datagrams_OutofOrder"] = text.split("ms")[1].strip().replace("  ","")
            #END IF/ELIF
        #END FOR
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
                for pingThread in self.myPingThreads:
                    this_str += str(pingThread)
                this_str += str(self.ServerReport["Ping"]) + "   " + str(self.ServerReport["Time"]) + "   " + \
                            str(self.ServerReport["Datagrams_OutofOrder"]) + "\n"
                #END FOR
            else:
                this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                            pad + "Connection Type: " + str(self.ConnectionType) + "\n" +
                            pad + "Connection Location: " + str(self.ConnectionLoc) + "\n" +
                            pad + "Reciever IP:" + str(self.RecieverIP) + " port:" + str(self.Port) + "\n" +
                            pad + "Test Interval:" + str(self.TestInterval) +\
                                "  Datagram Size:" + str(self.DatagramSize) + "\n" +\
                            pad + "Target Bandwidth:" + str(self.TargetBandwidth) +\
                                "  Measurement Format:" + str(self.MeasuringFmt["Size"]) +\
                                ", " + str(self.MeasuringFmt["Speed"]) + "\n"
                           )
                for pingThread in self.myPingThreads:
                    this_str += str(pingThread)
                this_str += str(self.ServerReport["Ping"]) + "   " + str(self.ServerReport["Time"]) + "   " + \
                            str(self.ServerReport["Datagrams_OutofOrder"]) + "\n"
                #END FOR
            #END IF/ELSE
            return this_str
        #END IF/ELSE
    #END DEF
#END CLASS
