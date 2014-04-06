
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
    sys.exit(0)
#END __name__=='__main__'





# ------------------------------------------------------------------------
# SPEEDTEST.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  ..
#
# FUNCTIONS:
#   __init__ - initializes the object by parsing the data in the given file path. calls load()
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   filePath:   String, containing absolute path to raw data file
#       OUTPUTS-    none
#
#   load - initializes the object by parsing the data in the given file path.
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   filePath:   String, containing absolute path to raw data file
#       OUTPUTS-    none
#
#   findSubTest - ..
#       INPUTS-     ..
#       OUTPUTS-    ..
#
#   __repr__ - returns a String representation of the object
#       INPUTS-     none
#       OUTPUTS-    String, representing the attributes of the object (THIS)
#
# ------------------------------------------------------------------------

from readTo import readToAndGetLine

class speedTest():

    # -------------------
    # Initializing some class attributes
    Time = "UNKNOWN"

    OSName = "UNKNOWN"
    OSArchitectue ="UNKNOWN"
    OSVersion = "UNKNOWN"

    JavaVersion = "UNKNOWN"
    JavaVender = "UNKNOWN"

    NetworkType = "UNKNOWN"

    Server = "UNKNOWN"
    Host = "UNKNOWN"

    NetworkProvider = "UNKNOWN"
    NetworkOperator = "UNKNOWN"
    DeviceID = "UNKNOWN"
    ConnectionType = "UNKNOWN"

    LocationID = "UNKNOWN"

    subtests = []
    isWBBD = False #These stupid WBBD files :)
    # -------------------

    # init functions calls load using the given file path
    def __init__(self,filePath):
        # !!!
        # Look at the line below! In one line, I am splitting
        #  the file path string based on "/", then getting
        #  the last element, and then the first 8 characters of that element.
        # HOW COOL IS THAT!?!
        # !!!
        if (filePath.split("/")[-1][:8] == "WBBDTest"):
            self.isWBBD = True
        self.load(filePath)
    #END INIT


    # DESC: parses data and info in given file (location is filePath)
    #       and stores it in the object's attributes
    # PARAMS:   self- reference to object (THIS)
    #           filePath- String, absolute path of raw data file
    # RETURN:   none
    def load(self, filePath):

        print("Loading in data @ " + "\"/" + "/".join(filePath.split("/")[-3:]) + "\"" );
        f = open(filePath,'r')

        #Seeing if the file given is, in fact, a data file
        #If not, the script will exit and display the message below
        isItCPUC = f.readline()
        if ("CPUC Tester Beta v2.0" not in isItCPUC):
            print("The file given to me was not a CPUC Network Speed Test.")
            print("Here is the first line:")
            print(isItCPUC)
            print("File Name: "+filePath)
            raise SystemExit

        #Reading in the Time of the test
        try:
            if not self.isWBBD:
                time = f.readline().split("at ")[1]
                self.Time = time[:-1]
            else:
                self.Time = f.readline()[:-1]
        except:
            print("ERROR LOADING Time DATA")
            return

        #Read in Operating System Header Information
        if not self.isWBBD:
            temp = readToAndGetLine(f,"OS: ")
            try:
                self.OSName = temp.split("Name = ")[1].split(",")[0]
                self.OSArchitectue = temp.split("Architecture = ")[1].split(",")[0]
                ## !!!!!
                ## [:-2] is used because there is a \r and \n character left on the end of the read line
                ## !!!!!
                self.OSVersion = temp.split("Version = ")[1][:-2]
                # After parsing text, we need to check that there are no empty values
                if self.OSName == "": self.OSName = "N/A"
                if self.OSArchitectue == "": self.OSArchitectue = "N/A"
                if self.OSVersion == "": self.OSVersion = "N/A"
            except:
                print("ERROR LOADING OS Name/Architecture/Version DATA")
                return
        #END IF

        #Read in Java Header Information
        if not self.isWBBD:
            temp = readToAndGetLine(f,"Java: ")
            try:
                self.JavaVersion = temp.split("Version = ")[1].split(",")[0];
                self.JavaVender  = temp.split("Vendor = ")[1][:-2]
                if self.JavaVersion == "": self.JavaVersion = "N/A"
                if self.JavaVender == "": self.JavaVender = "N/A"
            except:
                print("ERROR LOADING Java Version/Vendor DATA")
                return
        #END IF

        #Read in Network Type Information
        if not self.isWBBD:
            try:
                self.NetworkType = readToAndGetLine(f,"NetworkType: ").split("NetworkType: ")[1][:-2]
                if self.NetworkType == "": self.NetworkType = "N/A"
            except:
                print("ERROR LOADING NetworkType DATA")
                return
        else:
            self.NetworkType = "netbook"
        #END IF/ELSE

        #Read in Connection Information
        if not self.isWBBD:
            #Read in Server Header Information
            try:
                self.Server = readToAndGetLine(f,"Server: ").split("Server: ")[1][:-2]
                if self.Server == "": self.Server = "N/A"
            except:
                print("ERROR LOADING Server DATA")
                return
            #Read in Host Header Information
            try:
                self.Host = readToAndGetLine(f,"Host: ").split("Host: ")[1][:-2]
                if self.Host == "": self.Host = "N/A"
            except:
                print("ERROR LOADING Host DATA")
                return
        #END IF

        #Get Network Provider
        try:
            if not self.isWBBD:
                self.NetworkProvider = readToAndGetLine(f,"NetworkProvider: ").split("NetworkProvider: ")[1][:-2]
            else:
                # !!!
                #Location ID must be read first, otherwise is just read over and cannot be retrieved
                # !!!
                self.LocationID = readToAndGetLine(f,"Location: ").split("Location: ")[1][:-2]
                self.NetworkProvider = readToAndGetLine(f,"Network Provider: ").split("Network Provider: ")[1][:-2]
            if self.NetworkProvider == "": self.NetworkProvider = "N/A"
        except:
            print("ERROR LOADING NetworkProvider DATA")
            return

        #Get other Network information
        if not self.isWBBD:
            #Get Network Operator
            try:
                self.NetworkOperator = readToAndGetLine(f,"NetworkOperator: ").split("NetworkOperator: ")[1][:-2]
                if self.NetworkOperator == "": self.NetworkOperator = "N/A"
            except:
                print("ERROR LOADING NetworkOperator DATA")
                return
            #Get Device ID
            try:
                self.DeviceID = readToAndGetLine(f,"Device ID: ").split("Device ID: ")[1][:-2]
                if self.DeviceID == "": self.DeviceID = "N/A"
            except:
                print("ERROR LOADING Device ID DATA")
                return
            #Get Device ConnectionType
            try:
                self.ConnectionType = readToAndGetLine(f,"ConnectionType: ").split("ConnectionType: ")[1][:-2]
                if self.ConnectionType == "": self.ConnectionType = "N/A"
            except:
                print("ERROR LOADING Device Connection Type DATA")
                return
        #END IF

        #Get the Location ID
        if not self.isWBBD:
            try:
                self.LocationID = readToAndGetLine(f,"Location ID: ").split("Location ID: ")[1][:-2]
                if self.LocationID == "": self.LocationID = "N/A"
            except:
                print("ERROR LOADING Location ID DATA")
                return
        #END IF

        """
        tempSubTest = self.findSubTest(f)
        while not tempSubTest is None:
            self.subtests.append(tempSubTest)
            tempSubTest = self.findSubTest(f)
        """
        f.close()
    #END DEF


    # DESC: Finds all of the sub-tests in the given file stream
    # PARAMS:   self- reference to object (THIS)
    #           fileStream- FileStream object, read stream of the file
    # RETURN:   subtest - SubTest object holding parsed data for sub-test (e.g. TCP West)
    def findSubTest(self, fileStream):
        subtest = None
        temp = fileStream.readline()
        while "Starting Test " not in temp:
            temp = fileStream.readline()
            if not temp: break
        if not temp or temp is None:
            return None
        else:
            subtest = SubTest()
            #Start parsing the subtest

            #Split from the colon and remove the ....'s on the right
            testType = temp.split(": ")[1].split(".")[0]
            subtest.Type = testType

            temp = readToAndGetLine(fileStream,"Client connecting to ").split("Client connecting to ")[1]
            ip = temp.split(",")[0]
            port = temp.split("port ")[1].replace("\n","")
            subtest.IP = ip
            subtest.Port = port

            print("%s\n%s:%s"%(testType,ip,port))

        return subtest
    #END DEF


    # DESC: Returns a string representation of the object
    # PARAMS:   self- reference to object (THIS)
    # RETURN:   String, contains all object data in an easy-to-print-and-read string
    def __str__(self):
        if self.isWBBD:
            return ("Speed Test taken - " + self.Time + "\n" +
                    "    Network Type: " + self.NetworkType + "\n" +
                    "    Network: Provider = " + self.NetworkProvider + "\n" +
                    "    Location ID: " + self.LocationID + "\n" +
                    "    "
                    )
        return ("Speed Test taken - " + self.Time + "\n" +
                "    OS: " + self.OSName + ", " + self.OSArchitectue + ", " + self.OSVersion + "\n" +
                "    Java: " + self.JavaVersion + ", " + self.JavaVender + "\n" +
                "    Network Type: " + self.NetworkType + "\n" +
                "    Connection: Server = " + self.Server + ", Host = " + self.Host + "\n" +
                "    Network: Provider = " + self.NetworkProvider + ", Operator = " + self.NetworkOperator + "\n" +
                "    Device: ID = " + self.DeviceID + ", Connection Type = " + self.ConnectionType + "\n" +
                "    Location ID: " + self.LocationID + "\n" +
                "    "
                )
    #END DEF



#Small tests within each Test file
class SubTest():

    Latitude = 0.0
    Longitude= 0.0

    #Example: Iperf TCP West
    ## !!!!
    ## Some tests (like in WBBD) do not specifiy TCP West,TCP East,UDP West, etc.
    ## It would be better to just compare the IP address the test is connecting to
    ##  and then assign TCP/UDP West/East based on that value
    ##
    ## 184.72.222.65 = East TCP/UDP
    ## 184.72.63.139 = West TCP/UDP
    ## !!!!!
    Type     = "UNKNOWN"

    IP       = "UNKNOWN"
    Port     = 0000

    WindowSz = 0 #In KByte

    pings = []

    def __init__(self):
        pass

#Each subset of pings within each subset (represented by a numbered thread)
class Pings():
    localHost = "UNKNOWN"
    localPort = 0
    serverHost= "UNKNWON"
    serverPort= 0

    pings = []

    def __init__(self):
        pass

#Each ping within a subset of pings
class Ping():
    #second started to second ended
    secIntervalStart = 0
    secIntervalEnd   = 0

    size             = 0
    speed            = 0

    def __init__(self):
        pass
