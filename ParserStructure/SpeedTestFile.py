
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
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This object will hold a raw data file's header information (see list of variables)
#           and then parse individual test from the remaining text, storing them as a series of
#           related objects
#
# VARIABLES:
#   FileName        String, holding file name that is being parsed
#   FileStreamLoc   Integer, representing byte location that the script is at in file stream
#   DateTime        String, holding date and time test was taken
#   OSName          String, holding OS name that this test was conducted with
#   OSArchitecture  String, holding OS architecture that this test was conducted with
#   OSVersion       String, holding OS version that this test was conducted with
#   JavaVersion     String, holding Java version that this test was conducted with
#   JavaVendor      String, holding Java vendor that this test was conducted with
#   NetworkType     String, holding Network Type that this test was conducted with
#   Server          String, holding Server that this test was conducted with
#   Host            String, holding Host that this test was conducted with
#   NetworkProvider String, holding Network Provider that this test was conducted with (i.e. the Carrier)
#   NetworkOperator String, holding Network Operator that this test was conducted with (i.e. the Carrier)
#           note: Sometimes, the carrier name is in Network Provider, other times it is in Network Operator
#   DeviceID        String, the Device ID number
#   ConnectionType  String, holding Connection type that this test was conducted with
#   LocationID      Integer, the ID number of the location that this test was conducted at
#   Latitude        Integer, the latitude given by the GPS that this test was conducted at.
#                           Is 0 if no GPS data was available
#   Longitude       Integer, the latitude given by the GPS that this test was conducted at.
#                           Is 0 if no GPS data was available
#   this_SpeedTests List, holding all of the Individual Speed tests that are contained in the given file being parsed
#   short_str       Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                           Default is False
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
#   convertTo2D - Converts this SpeedTestFile object into a 2D array, and returns the result
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    tobeReturned:   the 2D array that will be returned
#
#   calc_TestTCP_StDev - For each test in this object, if the test is a TCP test, calculate the
#                        standard deviation of the sum of thread speeds at each 1 second interval.
#                        The IndivSpeedTest object will handle putting the value into the structure
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   structRef:  reference to the structure created in STDs.convertTo_ObjectToTCP()
#       OUTPUTS-    none
#
#   printSpeedTests - Return a string that has the information of each speed test in the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    text:   String, a representation of the IndividualSpeedTests held in
#                           this objects this_SpeedTests
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
#
# ------------------------------------------------------------------------

from .utils import readToAndGetLine, monthAbbrToNum, isLessThanVersion
from .utils import global_str_padding as pad
pad = pad*1
from .IndividualSpeedTest import SpeedTest
class SpeedTestFile(object):

    # -------------------
    # Initializing some class attributes
    FileName = "UNKNOWN"
    FileStreamLoc = 0

    DateTime = "UNKNOWN"

    OSName = "UNKNOWN"
    OSArchitecture = "UNKNOWN"
    OSVersion = "UNKNOWN"

    JavaVersion = "UNKNOWN"
    JavaVendor = "UNKNOWN"

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

    this_SpeedTests = []

    short_str = False
    # -------------------

    # DESC: init functions calls load using the given file path
    def __init__(self, filePath, short=False):
        self.short_str = short
        self.this_SpeedTests = []
        self.FileName = filePath.split("/")[-1]
        self.load(filePath)
    #END INIT


    # DESC: parses data and info in given file (location is filePath)
    #       and stores it in the object's attributes
    def load(self, filePath):
        #Open the file and read through the first line (which is "CPUC Beta .....")
        # save byte location to self.FileStreamLoc
        fs = open(filePath,'r')
        fs.readline()
        self.FileStreamLoc = fs.tell()

        #Reading in the DateTime of the test
        #Also setting the network type, as this is where the file types start to differ
        fs.seek(self.FileStreamLoc)
        datetime = fs.readline()
        self.FileStreamLoc = fs.tell()
        if ("Testing started" not in datetime):
            self.NetworkType = "netbook"
            self.DateTime = datetime[:-1]
        else:
            self.NetworkType = "mobile"
            #Formatting the datetime as "mm/dd/yyyy hh:mm:ss" when not in this format
            datetime = datetime.split("at ")[1][4:-1]
            month = str(monthAbbrToNum(datetime[:3]))
            day = str(datetime[4:6])
            year = str(datetime[-5:-1])
            time = str(datetime[7:9]) + ":" + str(datetime[10:12]) + ":" + str(datetime[13:15])
            self.DateTime = month + "/" + day + "/" + year + " " + time
        fs.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Read in Operating System Header Information
        temp = readToAndGetLine(fs,"OS: ")
        if temp:
            self.OSName = temp.split("Name = ")[1].split(",")[0]
            self.OSArchitecture = temp.split("Architecture = ")[1].split(",")[0]
            self.OSVersion = temp.split("Version = ")[1][:-1]
            # After parsing text, we need to check that there are no empty values
            if self.OSName == "": self.OSName = "N/A"
            if self.OSArchitecture == "": self.OSArchitecture = "N/A"
            if self.OSVersion == "": self.OSVersion = "N/A"
        else:
            self.OSName = "N/A"
            self.OSArchitecture = "N/A"
            self.OSVersion = "N/A"
        fs.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Read in Java Header Information
        temp = readToAndGetLine(fs,"Java: ")
        if temp:
            self.JavaVersion = temp.split("Version = ")[1].split(",")[0];
            self.JavaVendor  = temp.split("Vendor = ")[1][:-1]
            if self.JavaVersion == "": self.JavaVersion = "N/A"
            if self.JavaVendor == "": self.JavaVendor = "N/A"
        else:
            self.JavaVersion = "N/A"
            self.JavaVendor = "N/A"
        fs.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Read in Server Header Information
        try:
            self.Server = readToAndGetLine(fs,"Server: ").split("Server: ")[1][:-1]
            if self.Server == "": self.Server = "N/A"
        except:
            self.Server = "N/A"
        fs.seek(self.FileStreamLoc)
        #Read in Host Header Information
        try:
            self.Host = readToAndGetLine(fs,"Host: ").split("Host: ")[1][:-1]
            if self.Host == "": self.Host = "N/A"
        except:
            self.Host = "N/A"
        fs.seek(self.FileStreamLoc)
        #END TRY/EXCEPT

        #Get Network Provider
        try:
            self.NetworkProvider = readToAndGetLine(fs,"NetworkProvider: ").split("NetworkProvider: ")[1][:-1]
            if self.NetworkProvider == "": self.NetworkProvider = "N/A"
        except:
            fs.seek(self.FileStreamLoc)
            try:
                self.NetworkProvider = readToAndGetLine(fs,"Network Provider: ").split("Network Provider: ")[1][:-1]
                if self.NetworkProvider == "": self.NetworkProvider = "N/A"
            except:
                self.NetworkProvider = "N/A"
        fs.seek(self.FileStreamLoc)
        #END TRY/EXCEPT

        #Get Network Operator
        try:
            self.NetworkOperator = readToAndGetLine(fs,"NetworkOperator: ").split("NetworkOperator: ")[1][:-1]
            if self.NetworkOperator == "": self.NetworkOperator = "N/A"
        except:
            self.NetworkOperator = "N/A"
        fs.seek(self.FileStreamLoc)
        #Get Device ID
        try:
            self.DeviceID = readToAndGetLine(fs,"Device ID: ").split("Device ID: ")[1][:-1]
            if self.DeviceID == "": self.DeviceID = "N/A"
        except:
            self.DeviceID = "N/A"
        fs.seek(self.FileStreamLoc)
        #Get Device ConnectionType
        try:
            self.ConnectionType = readToAndGetLine(fs,"ConnectionType: ").split("ConnectionType: ")[1][:-1]
            if self.ConnectionType == "": self.ConnectionType = "N/A"
        except:
            self.ConnectionType = "N/A"
        fs.seek(self.FileStreamLoc)
        #END TRY/EXCEPTs

        #Get the Location ID
        try:
            self.LocationID = readToAndGetLine(fs,"Location ID: ").split("Location ID: ")[1][:-1]
            if self.LocationID == "": self.LocationID = "N/A"
        except:
            fs.seek(self.FileStreamLoc)
            try:
                self.LocationID = readToAndGetLine(fs,"Location: ").split("Location: ")[1][:-1]
                if self.LocationID == "": self.LocationID = "N/A"
            except:
                self.LocationID = "N/A"
        fs.seek(self.FileStreamLoc)
        #END TRY/EXCEPT

        #Get the Latitude and Longitude, if it is available
        try:
            temp = readToAndGetLine(fs, "Latitude:")
            while temp:
                temp = temp.split("Latitude:")[1][:-1]
                if temp != "0.0":
                    self.Latitude = temp
                temp = readToAndGetLine(fs, "Longitude:")
                temp = temp.split("Longitude:")[1][:-1]
                if temp != "0.0":
                    self.Longitude = temp
                temp = readToAndGetLine(fs, "Latitude:")
        except:
            not_doing_anything = True
        fs.seek(self.FileStreamLoc)

        #Set the file stream to the line after "Checking Connectivity"
        readToAndGetLine(fs, "Checking Connectivity..")
        self.FileStreamLoc = fs.tell()

        # Loop through the rest of the file, creating individual
        # Speed Test objects, which will hold an array of all of the actual data
        continueLoop = True
        while continueLoop:
            fs.seek(self.FileStreamLoc)
            iPerfLine = readToAndGetLine(fs, "Iperf command line:")
            self.FileStreamLoc = fs.tell()
            if not iPerfLine:
                continueLoop = False
            else:
                fs.seek(self.FileStreamLoc - len(iPerfLine)-1)
                aSpeedTest = SpeedTest(fs, self.short_str)
                self.this_SpeedTests.append(aSpeedTest)
            #END IF/ELSE
        #END WHILE

        # !!!!
        # SUPER IMPORTANT!! Otherwise, problems galore
        # !!!!
        # Don't want open streams o_O
        fs.close()
    #END DEF


    # DESC: Converts all of the individual test and ping threads and such
    #       in this object and returns a 2D array of it all
    def convertTo2D(self):
        toBeReturned = []
        #Setting up the basic information at the top of the 2D array/.csv file
        toBeReturned.append(["Filename", self.FileName])
        toBeReturned.append(["DateTime", self.DateTime])
        toBeReturned.append(["Location ID", self.LocationID])
        toBeReturned.append(["Network Type", self.NetworkType])
        toBeReturned.append(["Provider", (self.NetworkProvider
                                        if (self.NetworkProvider != "N/A")
                                        else self.NetworkOperator)])
        counter = 5
        testnum = 1
        for test in self.this_SpeedTests:
            #This section sets up the column headers for the test. Each
            # test will have column headers. The timing headers need
            # to account for different length threads, hence getLongest

            test_length = int(test.getLongestThreadTime())
            toBeReturned.append(["","","","Thread Num","Data Direction"])
            for t in range(test_length):
                toBeReturned[counter].append(str(float(t)) + "-" + str(float(t+1)))
                toBeReturned[counter].append("")
            #END FOR
            toBeReturned[counter].append("END")
            counter += 1

            #These three lines set up the Test information in the array
            toBeReturned.append(["","","Test #" + str(testnum)])
            testnum += 1
            toBeReturned.append(["","",test.ConnectionType])
            toBeReturned.append(["","",test.ConnectionLoc])

            #Append the threads to the array. If the array is not nothing,
            # it must then be holding the Test Header information, and so
            # we don't need any padding
            for thread in test.this_PingThreads:
                try:
                    toBeReturned[counter].extend(thread.array_itize((test_length*2)+4))
                except:
                    toBeReturned.append(["","",""])
                    toBeReturned[counter].extend(thread.array_itize((test_length*2)+4))
                counter += 1
            #END FOR

            #Incrementing the counter so that the next IndivTest that is converted is put below
            # the previous one (sometimes, there is one thread per test, and just moving to the next
            # iteration messed up the spacing)
            nextLine = True
            while nextLine:
                try:
                    aThing = toBeReturned[counter][2]
                    counter +=1
                except:
                    nextLine = False
            toBeReturned.append(["",""])
            counter += 1
        #END FOR
        return toBeReturned
    #END DEF


    # DESC: Looping through each Test, if the test if of type TCP, then
    #       call it's thread sum standard deviation function.
    def calc_TestTCP_StDev(self, structRef):
        list_carriers = list(structRef[self.NetworkType])

        #Calculate all of the threads' sums of pings if the thread is TCP
        for indivTest in self.this_SpeedTests:
            if (indivTest.ConnectionType == "TCP"):
                if (self.NetworkOperator in list_carriers):
                    indivTest.calc_StDev_ofTCPThreadSumsByDirection\
                        (structRef, self.NetworkType, self.NetworkOperator)
                elif (self.NetworkProvider in list_carriers):
                    indivTest.calc_StDev_ofTCPThreadSumsByDirection\
                        (structRef, self.NetworkType, self.NetworkProvider)
                #END IF/ELIF
            #END IF
        #END FOR
    #END DEF


    # DESC: Returns all of the sub tests for this file as a string
    def printSpeedTests(self):
        text = ""
        for obj in self.this_SpeedTests:
            text += pad*2 + "Speed Test #" + str(self.this_SpeedTests.index(obj)+1) + "\n" + str(obj)
        return text
    #END DEF


    # DESC: Returns a string representation of the object
    def __str__(self):
        if self.short_str:
            return (pad + "Filename: " + self.FileName + "\n" +
                    pad + "DateTime of Speed Test - " + self.DateTime + "\n" +
                    pad + "Network Type: " + self.NetworkType + "\n" +
                    pad + "Network: Provider = " + self.NetworkProvider +
                          ", Operator = " + self.NetworkOperator + "\n" +
                    pad + "Location ID: " + self.LocationID + "\n" +
                    self.printSpeedTests() +
                    "\n"
                    )
        else:
            return (pad + "Filename: " + self.FileName + "\n" +
                    pad + "DateTime of Speed Test - " + self.DateTime + "\n" +
                    pad + "OS: " + self.OSName + ", " + self.OSArchitecture + ", " + self.OSVersion + "\n" +
                    pad + "Java: " + self.JavaVersion + ", " + self.JavaVendor + "\n" +
                    pad + "Network Type: " + self.NetworkType + "\n" +
                    pad + "Connection: Server = " + self.Server + ", Host = " + self.Host + "\n" +
                    pad + "Network: Provider = " + self.NetworkProvider +
                          ", Operator = " + self.NetworkOperator + "\n" +
                    pad + "Device: ID = " + self.DeviceID +
                          ", Connection Type = " + self.ConnectionType + "\n" +
                    pad + "Location ID: " + self.LocationID + "\n" +
                    pad + "Latitude:" + str(self.Latitude) +
                          " Longitude:" + str(self.Longitude) + "\n" +
                    self.printSpeedTests() +
                    "\n"
                    )
    #END DEF
#END CLASS
