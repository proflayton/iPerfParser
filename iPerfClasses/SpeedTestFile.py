
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
#   printSpeedTests - ..
#       INPUTS-     ..
#       OUTPUTS-    ..
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
        fs.seek(self.FileStreamLoc)
        datetime = fs.readline()
        self.FileStreamLoc = fs.tell()
        if ("Testing started" not in datetime):
            self.DateTime = datetime[:-1]
        else:
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
        fs.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Read in Java Header Information
        temp = readToAndGetLine(fs,"Java: ")
        if temp:
            self.JavaVersion = temp.split("Version = ")[1].split(",")[0];
            self.JavaVender  = temp.split("Vendor = ")[1][:-1]
            if self.JavaVersion == "": self.JavaVersion = "N/A"
            if self.JavaVender == "": self.JavaVender = "N/A"
        else:
            self.JavaVersion = "N/A"
            self.JavaVender = "N/A"
        fs.seek(self.FileStreamLoc)
        #END IF/ELSE

        #Set the Network Type Information
        if (self.FileName[:8] == "WBBDTest"):
            self.NetworkType = "netbook"
        else:
            self.NetworkType = "mobile"
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

            #
            #print(self.FileName)
            #

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
                    pad + "OS: " + self.OSName + ", " + self.OSArchitectue + ", " + self.OSVersion + "\n" +
                    pad + "Java: " + self.JavaVersion + ", " + self.JavaVender + "\n" +
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
