
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
#   TestNumber          Integer, the number of this test from the original raw data file
#   ConnectionLoc       String, represents where this test is connected to (East or West)
#   RecieverIP          String, IP of the server this test is connected to
#   short_str_method           Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                           Default is False
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
from .utils import global_str_padding as pad; pad = pad*2

class PingTest():
    # ------------------------
    # Class variables
    TestNumber = 0
    RecieverIP = "UNKNOWN"
    ConnectionLoc = "UNKNOWN"

    PacketsSent = 0
    PacketsLost = 0

    RTTMin = 0
    RTTMax = 0
    RTTAverage = 0

    isMobile = True
    ERROR = False
    ErrorMessage = ""
    short_str_method = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString, testNum=0, isMobile=True, short=False):
        self.text = dataString
        self.isMobile = isMobile
        self.TestNumber = testNum
        self.short_str_method = short

        #These are the two error cases I've noticed for Ping Tests
        if "Network is unreachable" in dataString:
            self.ERROR = True
            self.ErrorMessage = "Connection Error: Network is unreachable"
            return
        elif "bad exit value" in dataString:
            self.ERROR = True
            self.ErrorMessage = "Connection Error: Ping Timed Out"
            return
        #END IF/ELIF
        self.text = dataString.split('\n')

        #This block will copy the command line call into the iPerfCommand variable,
        # as well as declare this objects TestNumber
        for line in self.text:
            if ("Starting Test" in line) and (self.TestNumber == 0):
                self.TestNumber = line.split(" ")[2].split(":")[0].split("..")[0]
                break
        #END FOR

        #Getting the Reciever IP address
        index = 0
        searchText = "ping statistics" if self.isMobile else "Ping statistics"
        for line in self.text:
            if searchText in line:
                splitText = line.split(" ")
                for elem in splitText:
                    if "184.72" in elem:
                        self.RecieverIP = elem.strip()
                        self.RecieverIP = self.RecieverIP[:-1] if not self.isMobile else self.RecieverIP
                        break
                #END FOR
                index = self.text.index(line)
                break
        #END FOR

        #Determining the Connection Location
        if self.RecieverIP == "184.72.222.65":
            self.ConnectionLoc = "East"
        if self.RecieverIP == "184.72.63.139":
            self.ConnectionLoc = "West"

        statsArr = self.text[index+1:]
        if self.isMobile:
            packetsLine = statsArr[0]
            packetsLine = packetsLine.split(",")
            self.PacketsSent = int(packetsLine[0].split(" ")[0])
            tempPacketsReceived = int(packetsLine[1].strip().split(" ")[0])
            self.PacketsLost = self.PacketsSent - tempPacketsReceived
            RTTLine = statsArr[1]
            RTTNums = RTTLine.split("=")[1][:-2].strip().split("/")
            self.RTTMin = float(RTTNums[0])
            self.RTTAverage = float(RTTNums[1])
            self.RTTMax = float(RTTNums[2])
        else:
            packetsLine = statsArr[0]
            packetsLine = packetsLine.split(",")
            self.PacketsSent = int(packetsLine[0].split("=")[1].strip())
            self.PacketsLost = int(packetsLine[2].split("=")[1].strip().split(" ")[0])
            RTTLine = statsArr[2]
            RTTLine = RTTLine.split(",")
            self.RTTMin = RTTLine[0].split("=")[1][:-2].strip()
            self.RTTMax = RTTLine[1].split("=")[1][:-2].strip()
            self.RTTAverage = RTTLine[2].split("=")[1][:-2].strip()
        #END IF/ELSE
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                    pad + "Connection Location: " + str(self.ConnectionLoc) + "\n"
                   )
        if self.ERROR:
            this_str += pad + "  ERROR: " + str(self.ErrorMessage) + "\n"
        else:
            if not self.short_str_method:
                this_str += (pad + "Packets Sent: " + str(self.PacketsSent) + "\n" +
                             pad + "Packets Lost: " + str(self.PacketsLost) + "\n" +
                             pad + "Round Trip Time Minimum: " + str(self.RTTMin) + "\n" +
                             pad + "Round Trip Time Maximum: " + str(self.RTTMax) + "\n" +
                             pad + "Round Trip Time Average: " + str(self.RTTAverage) + "\n"
                            )
            else:
                this_str += (pad + "Packet Loss Percentage: " + str(self.PacketsLost/self.PacketsSent) + "\n" +
                             pad + "Round Trip Time Average: " + str(self.RTTAverage) + "\n"
                            )
            #END IF/ELSE
        #END IF/ELSE
        return this_str
    #END DEF
#END CLASS
