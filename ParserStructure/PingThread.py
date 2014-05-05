
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
# PINGTHREAD.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This object will represent a single thread, or pipe, in a network
#           speed test. It will hold an array of
#
# VARIABLES:
#   PipeNumber              Integer, the number thread this is (is between 3 and 6
#   DataDirection           String, is either Up or Down (depending on the order of the thread's read
#   LocalIP                 The IP of this test's local machine
#   LocalPort               The port of this test's local machine
#   ServerIP                The IP of the server this thread was connected to
#   ServerPort              The port of the server this thread was connected to
#   final_secIntervalStart  The summation Ping start time. This should always be 0.0
#   final_secIntervalEnd    The summation Ping end time. This should always be more than 1.0
#   final_size              The summation Ping size (data sent).
#   final_speed             The summation Ping speed (KB/s)
#   Datagrams               String? Integer? holding some UDP information we don't understand yet
#   myPings                 List, holding all of the Pings in this specific thread
#   short_str               Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                               Default is False
#   ERROR                   Boolean, is True if there was a in the UDP test
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
from .utils import readToAndGetLine
from .utils import global_str_padding as pad; pad = pad*3
from .Pings import Ping
class PingThread():

    # ----------------
    # Initializing some class attributes
    PipeNumber    = 0
    DataDirection = ""

    LocalIP       = 0
    LocalPort     = 0
    ServerIP      = 0
    ServerPort    = 0

    final_secIntervalStart = 0
    final_secIntervalEnd   = 0
    final_size             = 0
    final_speed            = 0

    Datagrams     = None
    myPings    = []

    short_str     = False

    ERROR         = False
    # ----------------

    # DESC: Initializing class
    def __init__(self, threadNum, direction, data, short=False):
        #This takes the given data String and parses the object information
        self.short_str = short
        data            = data.split("local", 1)[1].strip()
        data_localIP    = data.split("port")[0].strip()
        data            = data.split("port", 1)[1].strip()
        data_localPort  = data.split("connected")[0].strip()
        data            = data.split("connected with", 1)[1].strip()
        data_serverIP   = data.split("port", 1)[0].strip()
        data            = data.split("port", 1)[1].strip()
        data_serverPort = data.split("\n")[0].strip()
        self.myPings    = []
        self.PipeNumber    = threadNum
        self.DataDirection = direction
        self.LocalIP       = data_localIP
        self.LocalPort     = data_localPort
        self.ServerIP      = data_serverIP
        self.ServerPort    = data_serverPort
    #END DEF


    # DESC: Adding a Ping object to this class' array of Ping objects
    def addPing(self,ping):
        self.myPings.append(ping)
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
            if (int(ping.secIntervalEnd - ping.secIntervalStart) == 1):
                arrayed.append(ping.size)
                arrayed.append(ping.speed)
            #END IF
        #END FOR
        #Adding empty values to array to pad the values such that the
        # last two values are the END values (0.0 -> XX.Y)
        for iter in range(totalLength - len(arrayed) - 2):
            arrayed.append("")
        #END FOR
        #Add the last two values, and return
        if (self.final_secIntervalStart == 0
            and self.final_secIntervalEnd == 0
            and self.final_size == 0
            and self.final_speed == 0):
            arrayed.append(self.myPings[-1].size)
            arrayed.append(self.myPings[-1].speed)
        else:
            arrayed.append(self.final_size)
            arrayed.append(self.final_speed)
        return arrayed
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = ""
        if self.short_str:
            this_str = (pad + "Pipe Number: " + str(self.PipeNumber) + "\n" +
                        pad + "Data Direction: " + self.DataDirection + "\n" +
                        pad + "Final Ping: " + str(self.final_secIntervalStart) + "-" +
                                               str(self.final_secIntervalEnd) + " " +
                                               str(self.final_size) + "KBytes " +
                                               str(self.final_speed) + "Kbits/sec" + "\n"
                       )
            this_str += pad + "Number of Pings: " + str(len(self.myPings)) + "\n"
        else:
            this_str = (pad + "Pipe Number: " + str(self.PipeNumber) + "\n" +
                        pad + "Data Direction: " + self.DataDirection + "\n" +
                        pad + "Local: " + str(self.LocalIP) + ":" + str(self.LocalPort) + "\n" +
                        pad + "Server: " + str(self.ServerIP) + ":" + str(self.ServerPort) + "\n"
                       )
            for ping in self.myPings:
                this_str += str(ping) + "\n"
            this_str += (pad + "Final Ping: " + str(self.final_secIntervalStart) + "-" +
                                                str(self.final_secIntervalEnd) + " " +
                                                str(self.final_size) + "KBytes " +
                                                str(self.final_speed) + "Kbits/sec" + "\n"
                        )
            #END FOR
        return this_str

#END CLASS
