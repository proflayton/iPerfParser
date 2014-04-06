
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
#   ReadToAndGetLine - Given a file stream, reads the stream until the delimiter is found
#       INPUTS-   ..
#       OUTPUTS-  ..
#
# ------------------------------------------------------------------------

#Keeps reading until it finds a line with the deliminator, then returns that line
def ReadToAndGetLine(fileStream, delimiter):
    temp = fileStream.readline()
    while delimiter not in temp:
        temp = fileStream.readline()
        if not temp: break
    return temp

class speedTest():

    Time = "UNKNOWN"

    OSName = "UNKNOWN"
    OSArchitectue ="UNKNOWN"
    OSVersion = "UNKNOWN"

    JavaVersion = "UNKNOWN"
    JavaVender = "UNKNOWN"

    Networktype = "UNKNWON"

    Server = "UNKNOWN"
    Host = "UNKNOWN"

    NetworkProvider = "UNKNOWN"
    NetworkOperator = "UNKNOWN"
    DeviceID = "UNKNOWN"
    ConnectionType = "UNKNOWN"

    subtests = []

    def __init__(self,filePath):
        self.load(filePath)

    def load(self,filePath):
        self.subtests = []
        print("Loading in " + str(filePath));
        f = open(filePath,'r')
        f.readline() #CPUC Tester Beta v2.0
        time = f.readline()
        time = time.split("at ")[1]
        print(time)
        self.Time = time

        #Read in Operating System Header Information
        temp = ReadToAndGetLine(f,"OS: ")
        try:
            self.OSName = temp.split("Name = ")[1].split(",")[0]
            self.OSArchitectue = temp.split("Architecture = ")[1].split(",")[0]
            self.OSVersion = temp.split("Version = ")[1].replace("\n","")
        except:
            print("ERROR LOADING OS DATA")
            return

        #Read in Java Header Information
        temp = ReadToAndGetLine(f,"Java: ")
        try:
            self.JavaVersion = temp.split("Version = ")[1].split(",")[0];
            self.JavaVender  = temp.split("Vendor = ")[1].replace("\n","")
        except:
            print("ERROR LOADING JAVA DATA")
            return

        #Read in Server Header Information
        temp = ReadToAndGetLine(f,"Server: ")
        try:
            self.Server = temp.split("Server: ")[1].replace("\n","")
        except:
            print("ERROR LOADING SERVER DATA")
            return
        #Read in Host Header Information
        temp = ReadToAndGetLine(f,"Host: ")
        try:
            self.Server = temp.split("Host: ")[1].replace("\n","")
        except:
            print("ERROR LOADING HOST DATA")
            return

        #Get Network Provider
        try:
            self.NetworkProvider = ReadToAndGetLine(f,"NetworkProvider: ")\
                                    .split("NetworkProvider: ")[1].replace("\n","")
        except:
            print("ERROR LOADING NetworkProvider DATA")
            return
        #Get Network Operator
        try:
            self.NetworkOperator = ReadToAndGetLine(f,"NetworkOperator: ")\
                                    .split("NetworkOperator: ")[1].replace("\n","")
        except:
            print("ERROR LOADING NetworkOperator DATA")
            return

        #Get Device ID
        try:
            self.DeviceID = ReadToAndGetLine(f,"Device ID: ")\
                                    .split("Device ID: ")[1].replace("\n","")
        except:
            print("ERROR LOADING Device ID DATA")
            return
        #Get Device ConnectionType
        try:
            self.ConnectionType = ReadToAndGetLine(f,"ConnectionType: ")\
                                    .split("ConnectionType: ")[1].replace("\n","")
        except:
            print("ERROR LOADING Device ID DATA")
            return

        tempSubTest = self.findSubTest(f)
        while not tempSubTest is None:
            self.subtests.append(tempSubTest)
            tempSubTest = self.findSubTest(f)
        f.close()


    def findSubTest(self,fileStream):
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

            temp = ReadToAndGetLine(fileStream,"Client connecting to ").split("Client connecting to ")[1]
            ip = temp.split(",")[0]
            port = temp.split("port ")[1].replace("\n","")
            subtest.IP = ip
            subtest.Port = port

            print("%s\n%s:%s"%(testType,ip,port))

        return subtest

    def __repr__(self):
        return ("Test @ " + str(self.Time) + "" +
                "       OS: " + str(self.OSName) + ", " + self.OSArchitectue + ", " + self.OSVersion + "\n" +
                "       Java: " + str(self.JavaVersion) + ", " + str(self.JavaVender) + "\n" +
                "       Network: Provider = " + str(self.NetworkProvider) + ", Operator = " + str(self.NetworkOperator) + "\n" +
                "       Device: " + str(self.DeviceID) + ", " + str(self.ConnectionType) + "\n" +
                "       "
                )

#Small tests within each Test file
class SubTest():

    Latitude = 0.0
    Longitude= 0.0

    #Example: Iperf TCP West
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
