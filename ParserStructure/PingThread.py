
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
# PINGTHREAD.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This object will represent a single thread, or pipe, in a network
#           speed test. It will hold an array of
#
# VARIABLES:
#   PipeNumber          Integer, the number thread this is (is between 3 and 6
#   DataDirection       String, is either Up or Down (depending on the order of the thread's read
#   LocalIP             The IP of this test's local machine
#   LocalPort           The port of this test's local machine
#   ServerIP            The IP of the server this thread was connected to
#   ServerPort          The port of the server this thread was connected to
#   myPings             List, holding all of the Pings in this specific thread
#   myfinalPing         Ping object, holding the final summation ping in the list
#   short_str_method    Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                           Default is False
#   ERROR               Boolean, is True if there was a in the UDP test
#
# FUNCTIONS:
#   __init__ - Used to initialize an object of this class
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   array_itize - Returns an array of this thread's pings. Used when converting
#                 STDs structure to a 2D array
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   totalLength:    The number of "rows", or elements, that the returned array needs to be,
#                                   as there are threads of different length, and we need spacers
#       OUTPUTS-    arrayed:        List, holding the necessary information for the 2D representation of this object
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import global_str_padding as pad; pad = pad*3
from .Pings import Ping

class PingThread(object):
    # ----------------
    # Initializing some class attributes
    PipeNumber    = 0
    DataDirection = ""

    LocalIP    = 0
    LocalPort  = 0
    ServerIP   = 0
    ServerPort = 0

    myPings     = []
    myfinalPing = None

    short_str_method = False
    # ----------------

    # DESC: Initializing class
    def __init__(self, dataArr, pipeNum, direction, size, speed, short=False):
        self.short_str_method = short
        self.myPings = []
        self.PipeNumber = pipeNum
        self.DataDirection = direction
        #This takes the given data String and parses the object information
        for line in dataArr:
            if "connected with" in line:
                line            = line.split("local", 1)[1].strip()
                self.LocalIP    = line.split("port")[0].strip()
                line            = line.split("port", 1)[1].strip()
                self.LocalPort  = line.split("connected")[0].strip()
                line            = line.split("connected with", 1)[1].strip()
                self.ServerIP   = line.split("port", 1)[0].strip()
                line            = line.split("port", 1)[1].strip()
                self.ServerPort = line.split("\n")[0].strip()
                break
            #END IF
        #END FOR
        #Removing the line from the array of pings that contains the connection info
        # and then creating all of the pings from the remaining strings
        dataArray = [line for line in dataArr if "connected with" not in line]
        for line in dataArray:
            newPing = Ping(line, size, speed)
            if (newPing.secIntervalStart == newPing.secIntervalEnd-1):
                if (newPing.secIntervalStart == 0) and (len(self.myPings) == 1):
                    self.myfinalPing = newPing
                    break
                else:
                    self.myPings.insert(int(newPing.secIntervalStart), newPing)
                #END IF/ELSE
            else:
                self.myfinalPing = newPing
                break
            #END IF/ELSE
        #END FOR
    #END DEF


    # DESC: Returns the Thread as an array of values. Spacers are added
    #       between the 1 second intervals and the END such that the given
    #       length is achieved
    def array_itize(self, totalLength):
        #Initialize the array with the thread num and direction
        arrayed = [self.PipeNumber, self.DataDirection]
        #For each ping, minus the last one, add the size and speed
        # to the array above
        for ping in self.myPings:
            arrayed.append(ping.size)
            arrayed.append(ping.speed)
        #END FOR
        #Adding empty values to array to pad the values such that the
        # last two values are the END values (0.0 -> XX.Y)
        for iter in range(totalLength - len(arrayed) - 2):
            arrayed.append("")
        #END FOR
        #Add the last two values, and return
        arrayed.append(self.myfinalPing.size)
        arrayed.append(self.myfinalPing.speed)
        return arrayed
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = ""
        if self.short_str_method:
            this_str = (pad + "Pipe Number: " + str(self.PipeNumber) + "\n" +
                        pad + "Data Direction: " + str(self.DataDirection) + "\n" +
                        pad + " Number of Pings: " + str(len(self.myPings)) + "\n" +
                        pad + " Final Ping: " + str(self.myfinalPing).strip() + "\n"
                       )
        else:
            this_str = (pad + "Pipe Number: " + str(self.PipeNumber) + "\n" +
                        pad + "Data Direction: " + str(self.DataDirection) + "\n" +
                        pad + "Local: " + str(self.LocalIP) + ":" + str(self.LocalPort) + "\n" +
                        pad + "Server: " + str(self.ServerIP) + ":" + str(self.ServerPort) + "\n"
                       )
            for ping in self.myPings:
                this_str += str(ping) + "\n"
            this_str += str(self.myfinalPing) + "\n"
            #END FOR
        return this_str
    #END DEF
#END CLASS
