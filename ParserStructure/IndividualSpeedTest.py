
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
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This class is the bare bones for the TCP and UDP classes, as both test have different
#           formats for their information, and different things that we want to track
#
# VARIABLES:    The variables below are common to both TCP and UDP tests
#   ConnectionType      String, represents the type of connection (TCP or UDP)
#   ConnectionLoc       String, represents where this test is connected to (East or West)
#   myPingThreads       list, holding all of the PingThreads in this test
#   RecieverIP          String, IP of the server this test is connected to
#   Port                Integer, the port this test is connected to
#   TestInterval        Integer, the length of time that the test will be run
#   MeasurementFormat   String, the format (Kbytes, Kbits, etc.) that the data has been stored in
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
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
class SpeedTest():

    # ------------------------
    # Class variables.
    #e.g. TCP, UDP
    ConnectionType = "UNKNOWN"
    #e.g. West, East
    ConnectionLoc = "UNKNOWN"

    myPingThreads = []
    TestNumber = 0

    RecieverIP = "UNKNOWN"
    Port = 0000

    TestInterval = 0
    MeasurementFormat = None  #[kmKM] (Kbits, Mbits, KBytes, MBytes)

    iPerfCommand = ""
    ERROR = False
    ErrorMessage = None

    short_str_method = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString, testNum=0, short_str=False):
        self.text = dataString
        self.TestNumber = testNum
        if ("Test Timed Out" in dataString) or ("timed out" in dataString):
            self.ERROR = True
            self.ErrorMessage = "Test Timed Out."
            return
        elif "Quitting operations" in dataString:
            self.ERROR = True
            self.ErrorMessage = "Test quit by User."
            return
        elif "failed:" in dataString:
            self.ERROR = True
            self.ErrorMessage = "There was an error of some kind. Please investigate"
            return
        elif "WARNING: did not recieve" in dataString:
            self.ERROR = True
            self.ErrorMessage = "WARNING: did not receive ack of last datagram after 10 tries."
            return
        #END IF/ELIF
        self.short_str_method = short_str
        self.MeasurementFormat = { "Speed" : None, "Size" : None}
        self.text = dataString.split('\n')

        #This block will copy the command line call into the iPerfCommand variable,
        # as well as declare this objects TestNumber
        for line in self.text:
            if ("Starting Test" in line) and (self.TestNumber == 0):
                self.TestNumber = line.split(" ")[2].split(":")[0].split("..")[0]
            if "Iperf command line" in line:
                self.iPerfCommand = line
            if self.iPerfCommand != "" and self.TestNumber != 0:
                break
        #END FOR

        #Getting the Reciever IP address
        self.RecieverIP = self.iPerfCommand[self.iPerfCommand.find("-c"): ].split(" ")[1].strip()

        #Determining the Connection Location
        if self.RecieverIP == "184.72.222.65":
            self.ConnectionLoc = "East"
        if self.RecieverIP == "184.72.63.139":
            self.ConnectionLoc = "West"

        #Getting port number
        self.Port = self.iPerfCommand[self.iPerfCommand.find("-p"): ].split(" ")[1].strip()

        #Getting test time interval number
        self.TestInterval = self.iPerfCommand[self.iPerfCommand.find("-t"): ].split(" ")[1].strip()

        #Getting measurement format
        mform = self.iPerfCommand[self.iPerfCommand.find("-f"): ].split(" ")[1].strip()
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


    # DESC: Creating a string representation of our object
    def __str__(self):
        return self.text
    #END DEF
#END CLASS
