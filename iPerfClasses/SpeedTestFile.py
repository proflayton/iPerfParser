
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

from .readTo import readToAndGetLine
from .IndividualSpeedTest import SpeedTest
class SpeedTestFile():

    # -------------------
    # Initializing some class attributes
    FileName = "UNKNOWN"

    DateTime = "UNKNOWN"

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

    speedTests = []
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
        self.FileName = filePath.split("/")[-1]
        self.load(filePath)
    #END INIT


    # DESC: parses data and info in given file (location is filePath)
    #       and stores it in the object's attributes
    # PARAMS:   self- reference to object (THIS)
    #           filePath- String, absolute path of raw data file
    # RETURN:   none
    def load(self, filePath):

        #Print will print out the bottom three levels of the path passed in
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

        #Reading in the DateTime of the test
        try:
            if not self.isWBBD:
                time = f.readline().split("at ")[1]
                self.DateTime = time[:-1]
            else:
                self.DateTime = f.readline()[:-1]
        except:
            #Raises an error (stops the script) and gives the file that caused the error
            raise StandardError("ERROR LOADING DateTime DATA: "
                                 + "/".join(filePath.split("/")[-2:]))

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
                raise StandardError("ERROR LOADING OS Name/Architecture/Version DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
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
                raise StandardError("ERROR LOADING Java Version/Vendor DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
        #END IF

        #Read in Network Type Information
        if not self.isWBBD:
            try:
                self.NetworkType = readToAndGetLine(f,"NetworkType: ").split("NetworkType: ")[1][:-2]
                if self.NetworkType == "": self.NetworkType = "N/A"
            except:
                raise StandardError("ERROR LOADING NetworkType DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
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
                raise StandardError("ERROR LOADING Server DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
            #Read in Host Header Information
            try:
                self.Host = readToAndGetLine(f,"Host: ").split("Host: ")[1][:-2]
                if self.Host == "": self.Host = "N/A"
            except:
                raise StandardError("ERROR LOADING Host DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
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
            raise StandardError("ERROR LOADING NetworkProvider DATA: "
                                 + "/".join(filePath.split("/")[-2:]))

        #Get other Network information
        if not self.isWBBD:
            #Get Network Operator
            try:
                self.NetworkOperator = readToAndGetLine(f,"NetworkOperator: ").split("NetworkOperator: ")[1][:-2]
                if self.NetworkOperator == "": self.NetworkOperator = "N/A"
            except:
                raise StandardError("ERROR LOADING NetworkOperator DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
            #Get Device ID
            try:
                self.DeviceID = readToAndGetLine(f,"Device ID: ").split("Device ID: ")[1][:-2]
                if self.DeviceID == "": self.DeviceID = "N/A"
            except:
                raise StandardError("ERROR LOADING Device ID DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
            #Get Device ConnectionType
            try:
                self.ConnectionType = readToAndGetLine(f,"ConnectionType: ").split("ConnectionType: ")[1][:-2]
                if self.ConnectionType == "": self.ConnectionType = "N/A"
            except:
                raise StandardError("ERROR LOADING Device Connection Type DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
        #END IF

        #Get the Location ID
        if not self.isWBBD:
            try:
                self.LocationID = readToAndGetLine(f,"Location ID: ").split("Location ID: ")[1][:-2]
                if self.LocationID == "": self.LocationID = "N/A"
            except:
                raise StandardError("ERROR LOADING Location ID DATA: "
                                     + "/".join(filePath.split("/")[-2:]))
        #END IF



        """
        tempSpeedTest = self.findSpeedTest(f)
        while not tempSpeedTest is None:
            self.subtests.append(tempSpeedTest)
            tempSpeedTest = self.findSpeedTest(f)
        """
        f.close()
    #END DEF


    # DESC: Finds all of the sub-tests in the given file stream
    # PARAMS:   self- reference to object (THIS)
    #           fileStream- FileStream object, read stream of the file
    # RETURN:   subtest - SubTest object holding parsed data for sub-test (e.g. TCP West)

    # !!!
    # I think we should instead look for the iperf command line. That function call
    # will likely hold all of the information that we need, and is always in the file above the test
    #
    # e.g. Iperf command line:/data/data/net.measurementlab.ndt/files/iperfT
    #               -c 184.72.63.139 -e -w 32k -P 4 -i 1 -t 10 -f k -p 5003
    # !!!
    def findSpeedTest(self, fileStream):
        speedtest = None
        temp = fileStream.readline()
        while "Starting Test " not in temp:
            temp = fileStream.readline()
            if not temp: break
        if not temp or temp is None:
            return None
        else:
            speedtest = SubTest()
            #Start parsing the subtest

            #Split from the colon and remove the ....'s on the right
            testType = temp.split(": ")[1].split(".")[0]
            speedtest.Type = testType

            temp = readToAndGetLine(fileStream,"Client connecting to ").split("Client connecting to ")[1]
            ip = temp.split(",")[0]
            port = temp.split("port ")[1].replace("\n","")
            speedtest.IP = ip
            speedtest.Port = port

            print("%s\n%s:%s"%(testType,ip,port))

        return speedtest
    #END DEF


    # DESC: Returns a string representation of the object
    # PARAMS:   self- reference to object (THIS)
    # RETURN:   String, contains all object data in an easy-to-print-and-read string
    def __str__(self):
        if self.isWBBD:
            return ("Filename: " + self.FileName + "\n" +
                    "    DateTime of Speed Test - " + self.DateTime + "\n" +
                    "    Network Type: " + self.NetworkType + "\n" +
                    "    Network: Provider = " + self.NetworkProvider + "\n" +
                    "    Location ID: " + self.LocationID + "\n" +
                    "    "
                    )
        return ("Filename: " + self.FileName + "\n" +
                "    DateTime of Speed Test - " + self.DateTime + "\n" +
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
#END CLASS
