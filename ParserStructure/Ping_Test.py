
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
#   ConnectionType      String, represents the type of connection
#   TestNumber          Integer, the number of this test from the original raw data file
#   RecieverIP          String, IP of the server this test is connected to
#   ConnectionLoc       String, represents where this test is connected to (East or West)
#   Times               List, holds all of the individual ping times in the test
#   PacketsSent         Integer, number of packets sent during the test
#   PacketsLost         Integer, number of packets not received by the recipient
#   RTTMin              Integer, RTT min recorded by the test
#   RTTMax              Integer, RTT max recorded by the test
#   RTTAverage          Integer, RTT average recorded by the test
#   isMobile            Boolean, if the test was on a mobile device, the format is different
#   ERROR               Boolean, if there was an error in the test, then this is True
#   ErrorMessage        String, the message that will be output when str is called
#   short_str_method           Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                           Default is False
#
# FUNCTIONS:
#   __init__ - Used to initialize an object of this class
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   convert_Obj_To_2D - Converts this SpeedTestFile object into a 2D array, and returns the result
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    objectAs2D:   the 2D array that will be returned
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import global_str_padding as pad; pad = pad*2

class PingTest():
    # ------------------------
    # Class variables
    ConnectionType = "PING"
    TestNumber = 0
    RecieverIP = "UNKNOWN"
    ConnectionLoc = "UNKNOWN"
    Times = {}

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
        self.Times = {}
        self.text = dataString
        self.isMobile = isMobile
        self.TestNumber = testNum
        self.short_str_method = short

        #These are the two error cases I've noticed for Ping Tests
        if "Network is unreachable" in dataString:
            self.ERROR = True
            self.ErrorMessage = "Connection Error: Network is unreachable"
            return
        elif "Ping timed out" in dataString:
            self.ERROR = True
            self.ErrorMessage = "Connection Error: Ping Timed Out"
            return
        elif ("Quitting operations" in dataString) or ("Quitting Operations" in dataString):
            self.ERROR = True
            self.ErrorMessage = "Test quit by User."
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
        pingCounter = 0
        statsText = "ping statistics" if self.isMobile else "Ping statistics"
        pingText = "bytes from" if self.isMobile else "Reply from"
        pingErrors = ["Request timed out",
                      "General failure",
                      "host unreachable",
                      "net unreachable" ]
        for line in self.text:
            #This test comes first so that, when we reach the statistics at the bottom, we read it,
            # parse it, and then break out of the loop before the other conditional are run
            if statsText in line:
                splitText = line.split(" ")
                for elem in splitText:
                    if "184.72" in elem:
                        self.RecieverIP = elem.strip()
                        self.RecieverIP = self.RecieverIP[:-1] if not self.isMobile else self.RecieverIP
                        break
                #END FOR
                index = self.text.index(line)
                break
            #Parse the individual ping times from the test
            else:
                pingCounter += 1
                isErrorPresent = False
                for error in pingErrors:
                    if error in line:
                        self.Times[pingCounter] = 0
                        isErrorPresent = True
                        break
                if isErrorPresent:
                    continue
                #END FOR
                if pingText in line:
                    self.Times[pingCounter] = line.split("time=")[1].split("ms")[0].strip();
                #END IF
            #END IF/ELSE
        #END FOR

        #Determining the Connection Location
        if self.RecieverIP == "184.72.222.65":
            self.ConnectionLoc = "East"
        if self.RecieverIP == "184.72.63.139":
            self.ConnectionLoc = "West"

        statsArr = self.text[index+1:]
        if self.isMobile:
            #First declare packetsLine to be the first element, and then split it by ",".
            # Then parse the packets sent and received, and deduce the packets lost
            packetsLine = statsArr[0]
            packetsLine = packetsLine.split(",")
            self.PacketsSent = float(packetsLine[0].split(" ")[0])
            tempPacketsReceived = float(packetsLine[1].strip().split(" ")[0])
            self.PacketsLost = self.PacketsSent - tempPacketsReceived
            #This try/except block is needed, as sometimes the min/avg/max numbers
            # are not printed out by iPerf. This happens in the case of 100% packet loss
            try:
                RTTLine = statsArr[1]
                RTTNums = RTTLine.split("=")[1][:-2].strip().split("/")
                self.RTTMin = float(RTTNums[0])
                self.RTTAverage = float(RTTNums[1])
                self.RTTMax = float(RTTNums[2])
            except:
                using_defaults_of_0 = True
        else:
            #First declare packetsLine to tbe the first element, and then split it by ",".
            # Then parse the packets sent and lost
            packetsLine = statsArr[0]
            packetsLine = packetsLine.split(",")
            self.PacketsSent = float(packetsLine[0].split("=")[1].strip())
            self.PacketsLost = float(packetsLine[2].split("=")[1].strip().split(" ")[0])
            #This try/except block is needed, as sometimes the min/avg/max numbers
            # are not printed out by iPerf. This happens in the case of 100% packet loss
            try:
                RTTLine = statsArr[2]
                RTTLine = RTTLine.split(",")
                self.RTTMin = float(RTTLine[0].split("=")[1][:-2].strip())
                self.RTTMax = float(RTTLine[1].split("=")[1][:-2].strip())
                self.RTTAverage = float(RTTLine[2].split("=")[1][:-2].strip())
            except:
                using_defaults_of_0 = True
        #END IF/ELSE
    #END DEF


    # DESC: This converts the object into a 2D representation of itself. Will return a 2D array
    #       that will be used in the SpeedTestFile class.
    def convert_Obj_To_2D(self):
        objectAs2D = []
        index = 0
        objectAs2D.append(["","","Ping Sequence Num"])
        #Adding the sequence numbers to correspong with the 
        for t in range(10):
            objectAs2D[index].append(str(t+1))
        #END FOR
        #These two lines set up the Test information in the array
        objectAs2D.append(["","","Test #" + self.TestNumber])
        objectAs2D.append(["","","Ping " + self.ConnectionLoc])
        objectAs2D.append(["","",""])
        index +=1
        #If the test has an error, then we print error. Otherwise, we array-itize the
        # threads and add then to the 2D array
        if (self.ERROR):
            objectAs2D[index].extend(["ERROR","ERROR","ERROR"])
            return objectAs2D
        else:
            #Appending the ping Times
            for tIndex in self.Times:
                objectAs2D[index].append(self.Times[tIndex])
            index += 1
            #Appending the Packet information, and the RTT information
            objectAs2D[index].extend(["Packets Sent", self.PacketsSent, "Packets Lost", self.PacketsLost])
            index += 1
            objectAs2D[index].extend(["RTT Min", self.RTTMin, "RTT Avg", self.RTTAverage, "RTT Max", self.RTTMax])
        #END IF/ELSE
        #Adding a little spacer between the tests.
        objectAs2D.append(["",""])
        return objectAs2D
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                    pad + "Connection Type: " + str(self.ConnectionType) + "\n" +
                    pad + "Connection Location: " + str(self.ConnectionLoc) + "\n"
                   )
        if self.ERROR:
            this_str += pad + "  ERROR: " + str(self.ErrorMessage) + "\n"
        else:
            if not self.short_str_method:
                #Printing the individual pings in the ping test
                this_str += pad + "Ping Times: "
                for index in self.Times:
                    this_str += (str(index) + "=" + str(self.Times[index]) + "ms, ")
                this_str = this_str[:-2] + "\n"
                #Printing the rest of the information
                this_str += (pad + "Packets Sent: " + str(self.PacketsSent) + "\n" +
                             pad + "Packets Lost: " + str(self.PacketsLost) + "\n" +
                             pad + "Round Trip Time Minimum: " + str(self.RTTMin) + "\n" +
                             pad + "Round Trip Time Maximum: " + str(self.RTTMax) + "\n" +
                             pad + "Round Trip Time Average: " + str(self.RTTAverage) + "\n"
                            )
            else:
                this_str += (pad + "Packet Loss Percentage: " + str(self.PacketsLost/self.PacketsSent) + "%\n" +
                             pad + "Round Trip Time Average: " + str(self.RTTAverage) + "\n"
                            )
            #END IF/ELSE
        #END IF/ELSE
        return this_str
    #END DEF
#END CLASS
