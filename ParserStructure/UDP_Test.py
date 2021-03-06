
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
#   iPerfCommand        String, the command line string used to run iPerf for this test
#   ERROR               Boolean, True if test contained an error, False otherwise
#   ErrorMessage        String, the message that will be displayed if the test contained an error
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
#   convert_Obj_To_2D - Converts this SpeedTestFile object into a 2D array, and returns the result
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    objectAs2D:   the 2D array that will be returned
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
        SpeedTest.__init__(self, dataString, testNum, short)
        if not self.iPerfCommand: return
        #Getting the datagram size
        self.DatagramSize = self.iPerfCommand[self.iPerfCommand.find("-l"):].split(" ")[1].strip()
        #Getting the datagram size
        self.TargetBandwidth = self.iPerfCommand[self.iPerfCommand.find("-b"):].split(" ")[1].strip()
        if not self.ERROR:
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
            #These two lines below check that the correct line is gotten.
            # First initialize an array of strings (which will be used as reference).
            # Next, for each elem in the array, check if it is in the line we are checking.
            #   (this is everything in the parenthesis)
            # Then, use all() on the returned array. The code in the parenthesis returns an array of
            #  booleans, and all() makes sure that they are all True.
            # If the conditions are met, this line is the line we are looking for.
            # If one of the strings was not found, then sadly, it means
            #  that these are not the droids we are looking for...
            # This was implemented because datagrams is in a few other lines, but not the ones we want
            strCheck = ["datagrams", "Sent"]
            if all(text in line for text in strCheck):
                self.DatagramzSent = line.split("Sent ")[1].split(" ")[0]
            # If "Server Report" is in the line, we need the next line
            elif "Server Report" in line:
                self.ServerReport = { "Ping": None, "Time": None,
                                      "Datagrams_OutofOrder": []
                                    }
                text = self.text[self.text.index(line)+1]
                self.ServerReport["Ping"] = Ping(text, self.MeasuringFmt["Size"], self.MeasuringFmt["Speed"])
                self.ServerReport["Time"] = text.split("/sec")[1].split("ms")[0].strip() + " ms"
                #Calculating the percentage at the end of this server report string
                fraction = text.split("ms")[1]
                lost = int(fraction.split("/")[0].strip())
                total = int(fraction.split("/")[1].split("(")[0].strip())
                self.ServerReport["Datagrams_OutofOrder"].append(lost)
                self.ServerReport["Datagrams_OutofOrder"].append(total)
                self.ServerReport["Datagrams_OutofOrder"].append((float(lost)/float(total))*100)
            #END IF/ELIF
        #END FOR
    #END DEF


    # DESC: This converts the object into a 2D representation of itself. Will return a 2D array
    #       that will be used in the SpeedTestFile class.
    def convert_Obj_To_2D(self):
        objectAs2D = []
        index = 0
        #This section sets up the column headers for the test. Each
        # test will have column headers. The timing headers need
        # to account for different length threads, hence getLongest
        objectAs2D.append(["","","","Thread Num","Data Direction"])
        for t in range(int(self.TestInterval)):
            objectAs2D[index].append(str(float(t)) + "-" + str(float(t+1)))
            objectAs2D[index].append("")
        #END FOR
        objectAs2D[index].append("END")
        index += 1
        #These two lines set up the Test information in the array
        objectAs2D.append(["","","Test #" + self.TestNumber])
        objectAs2D.append(["","",self.ConnectionType+" "+self.ConnectionLoc])

        if (self.ERROR):
            objectAs2D[index].extend(["ERROR", "ERROR"])
            index += 1
        else:
            #Append the threads to the array. If the array is not nothing,
            # it must then be holding the Test Header information, and so
            # we don't need any padding
            for thread in self.myPingThreads:
                objectAs2D[index].extend(thread.array_itize((int(self.TestInterval)*2)+2))
                index += 1
            #END FOR
        #END IF/ELSE

        #Now appending the Server Report information
        if not self.ERROR:
            objectAs2D[index].extend(["","Server Report",
                                      str(self.ServerReport["Ping"].size) + " " + 
                                      str(self.ServerReport["Ping"].size_units),
                                      str(self.ServerReport["Ping"].speed) + " " + 
                                      str(self.ServerReport["Ping"].speed_units),
                                      str(self.ServerReport["Time"]),
                                      str(self.ServerReport["Datagrams_OutofOrder"][0]) + "/ " +
                                      str(self.ServerReport["Datagrams_OutofOrder"][1])
                                    ])
        #END IF
        objectAs2D.append(["",""])
        return objectAs2D
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                    pad + "Connection Type: " + str(self.ConnectionType) + "\n" +
                    pad + "Connection Location: " + str(self.ConnectionLoc) + "\n"
                   )
        if not self.short_str_method:
            this_str += (pad + "Reciever IP:" + str(self.RecieverIP) + " port:" + str(self.Port) + "\n" +
                         pad + "Test Interval:" + str(self.TestInterval) +
                               "  Datagram Size:" + str(self.DatagramSize) + "\n" +
                         pad + "Target Bandwidth:" + str(self.TargetBandwidth) +
                               "  Measurement Format:" + str(self.MeasuringFmt["Size"]) +
                                                 ", " + str(self.MeasuringFmt["Speed"]) + "\n"
                        )
        if self.ERROR:
            this_str += pad + "  ERROR: " + str(self.ErrorMessage) + "\n"
        else:
            for pingThread in self.myPingThreads:
                this_str += str(pingThread)
            #Now append the Server Report information
            this_str += ( pad + "  Server Report: " +
                          str(self.ServerReport["Ping"]).strip() + "   " +
                          str(self.ServerReport["Time"]) + "   " +
                          str(self.ServerReport["Datagrams_OutofOrder"][0]) + "/ " +
                          str(self.ServerReport["Datagrams_OutofOrder"][1]) + " (" +
                          str( int(round(self.ServerReport["Datagrams_OutofOrder"][2])) ) + "%)\n"
                        )
            #END APPEND PING THREADS
        #END IF/ELSE
        return this_str
    #END DEF
#END CLASS
