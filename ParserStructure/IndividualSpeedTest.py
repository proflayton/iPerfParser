
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
#   short_str           Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
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

    RecieverIP = "UNKNOWN"
    Port = 0000

    TestInterval = 0
    MeasurementFormat = None  #[kmKM] (Kbits, Mbits, KBytes, MBytes)

    short_str = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString, short=False):
        self.text = dataString
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        return self.text
    #END DEF
#END CLASS
