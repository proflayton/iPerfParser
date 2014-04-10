
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

from .utils import readToAndGetLine, monthAbbrToNum
from .utils import global_str_padding as pad
pad = pad*1
from .IndividualSpeedTest import SpeedTest
class SpeedTestFile():

    # -------------------
    # Initializing some class attributes
    FileName = "UNKNOWN"
    FileStreamLoc = 0

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
    Latitude = 0
    Longitude = 0

    this_speedTests = []
    # -------------------

    # init functions calls load using the given file path
    def __init__(self,filePath):
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

        #open the file and read through the first line (which is "CPUC Beta .....")
        # save byte location to self.FileStreamLoc
        f = open(filePath,'r')
        f.readline()
        self.FileStreamLoc = f.tell()

        #Reading in the DateTime of the test
        f.seek(self.FileStreamLoc)
        datetime = f.readline()
        self.FileStreamLoc = f.tell()
        if (self.FileName[:8] == "WBBDTest"):
            self.DateTime = datetime[:-1]
        else:
            #Formatting the datetime as "mm/dd/yyyy hh:mm:ss" when not in this format
            datetime = datetime.split("at ")[1][4:-1]
            month = str(monthAbbrToNum(datetime[:3]))
            day = str(datetime[4:6])
            year = str(datetime[-5:-1])
            time = str(datetime[7:9]) + ":" + str(datetime[10:12]) + ":" + str(datetime[13:15])
            self.DateTime = month + "/" + day + "/" + year + " " + time
        f.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Read in Operating System Header Information
        temp = readToAndGetLine(f,"OS: ")
        if temp:
            self.OSName = temp.split("Name = ")[1].split(",")[0]
            self.OSArchitectue = temp.split("Architecture = ")[1].split(",")[0]
            self.OSVersion = temp.split("Version = ")[1][:-1]
            # After parsing text, we need to check that there are no empty values
            if self.OSName == "": self.OSName = "N/A"
            if self.OSArchitectue == "": self.OSArchitectue = "N/A"
            if self.OSVersion == "": self.OSVersion = "N/A"
        else:
            self.OSName = "N/A"
            self.OSArchitectue = "N/A"
            self.OSVersion = "N/A"
        f.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Read in Java Header Information
        temp = readToAndGetLine(f,"Java: ")
        if temp:
            self.JavaVersion = temp.split("Version = ")[1].split(",")[0];
            self.JavaVender  = temp.split("Vendor = ")[1][:-1]
            if self.JavaVersion == "": self.JavaVersion = "N/A"
            if self.JavaVender == "": self.JavaVender = "N/A"
        else:
            self.JavaVersion = "N/A"
            self.JavaVender = "N/A"
        f.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Set the Network Type Information
        if (self.FileName[:8] == "WBBDTest"):
            self.NetworkType = "netbook"
        else:
            self.NetworkType = "mobile"
        #END IF/ELSE

        #Read in Server Header Information
        try:
            self.Server = readToAndGetLine(f,"Server: ").split("Server: ")[1][:-1]
            if self.Server == "": self.Server = "N/A"
        except:
            self.Server = "N/A"
        f.seek(self.FileStreamLoc)
        #Read in Host Header Information
        try:
            self.Host = readToAndGetLine(f,"Host: ").split("Host: ")[1][:-1]
            if self.Host == "": self.Host = "N/A"
        except:
            self.Host = "N/A"
        f.seek(self.FileStreamLoc)
        #END TRY/EXCEPT

        #Get Network Provider
        try:
            self.NetworkProvider = readToAndGetLine(f,"NetworkProvider: ").split("NetworkProvider: ")[1][:-1]
            if self.NetworkProvider == "": self.NetworkProvider = "N/A"
        except:
            f.seek(self.FileStreamLoc)
            try:
                self.NetworkProvider = readToAndGetLine(f,"Network Provider: ").split("Network Provider: ")[1][:-1]
                if self.NetworkProvider == "": self.NetworkProvider = "N/A"
            except:
                self.NetworkProvider = "N/A"
        f.seek(self.FileStreamLoc)
        #END TRY/EXCEPT

        #Get Network Operator
        try:
            self.NetworkOperator = readToAndGetLine(f,"NetworkOperator: ").split("NetworkOperator: ")[1][:-1]
            if self.NetworkOperator == "": self.NetworkOperator = "N/A"
        except:
            self.NetworkOperator = "N/A"
        f.seek(self.FileStreamLoc)
        #Get Device ID
        try:
            self.DeviceID = readToAndGetLine(f,"Device ID: ").split("Device ID: ")[1][:-1]
            if self.DeviceID == "": self.DeviceID = "N/A"
        except:
            self.DeviceID = "N/A"
        f.seek(self.FileStreamLoc)
        #Get Device ConnectionType
        try:
            self.ConnectionType = readToAndGetLine(f,"ConnectionType: ").split("ConnectionType: ")[1][:-1]
            if self.ConnectionType == "": self.ConnectionType = "N/A"
        except:
            self.ConnectionType = "N/A"
        f.seek(self.FileStreamLoc)
        #END TRY/EXCEPTs

        #Get the Location ID
        try:
            self.LocationID = readToAndGetLine(f,"Location ID: ").split("Location ID: ")[1][:-1]
            if self.LocationID == "": self.LocationID = "N/A"
        except:
            f.seek(self.FileStreamLoc)
            try:
                self.LocationID = readToAndGetLine(f,"Location: ").split("Location: ")[1][:-1]
                if self.LocationID == "": self.LocationID = "N/A"
            except:
                self.LocationID = "N/A"
        f.seek(self.FileStreamLoc)
        #END TRY/EXCEPT

        #Get the Latitude and Longitude, if it is available
        try:
            temp = readToAndGetLine(f, "Latitude:")
            while temp:
                temp = temp.split("Latitude:")[1][:-1]
                if temp != "0.0":
                    self.Latitude = temp
                temp = readToAndGetLine(f, "Longitude:")
                temp = temp.split("Longitude:")[1][:-1]
                if temp != "0.0":
                    self.Longitude = temp
                temp = readToAndGetLine(f, "Latitude:")
        except:
            not_doing_anything = True
        f.seek(self.FileStreamLoc)

        #Set the file stream to the line after "Checking Connectivity"
        readToAndGetLine(f, "Checking Connectivity..")
        self.FileStreamLoc = f.tell()

        # Loop through the rest of the file, creating individual
        # Speed Test objects, which will hold an array of all of the actual data
        continueLoop = True
        while continueLoop:
            f.seek(self.FileStreamLoc)
            SpeedTestData = readToAndGetLine(f, "Iperf command line:")
            if not SpeedTestData:
                continueLoop = False
            else:
                temp = f.readline()
                while (temp[:-2] != ''):
                    SpeedTestData += temp[:-2] + "\n"
                    temp = f.readline()
                #END WHILE
                createdSpeedTest = SpeedTest(SpeedTestData)
                self.this_speedTests.append(createdSpeedTest)
                self.FileStreamLoc = f.tell()
            #END IF/ELSE
        #END WHILE
    #END DEF


    # DESC: Returns all of the sub tests for this file as a string
    # PARAMS:   self- reference to object (THIS)
    # RETURN:   text - String all text for individual tests
    def printSpeedTests(self):
        text = ""
        for obj in self.this_speedTests:
            text += pad*2 + "Speed Test #" + str(self.this_speedTests.index(obj)+1) + "\n" + str(obj)
        return text
    #END DEF


    # DESC: Returns a string representation of the object
    # PARAMS:   self- reference to object (THIS)
    # RETURN:   String, contains all object data in an easy-to-print-and-read string
    def __str__(self):
        return (pad + "Filename: " + self.FileName + "\n" +
                pad + " DateTime of Speed Test - " + self.DateTime + "\n" +
                pad + " OS: " + self.OSName + ", " + self.OSArchitectue + ", " + self.OSVersion + "\n" +
                pad + " Java: " + self.JavaVersion + ", " + self.JavaVender + "\n" +
                pad + " Network Type: " + self.NetworkType + "\n" +
                pad + " Connection: Server = " + self.Server + ", Host = " + self.Host + "\n" +
                pad + " Network: Operator = " + self.NetworkOperator +
                      ", Provider = " + self.NetworkProvider + "\n" +
                pad + " Device: ID = " + self.DeviceID +
                      ", Connection Type = " + self.ConnectionType + "\n" +
                pad + " Location ID: " + self.LocationID + "\n" +
                pad + " Latitude:" + str(self.Latitude) +
                      " Longitude:" + str(self.Longitude) + "\n" +
                self.printSpeedTests() +
                "\n"
                )
    #END DEF
#END CLASS
