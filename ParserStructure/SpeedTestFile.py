
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
#   FileName            String, holding file name that is being parsed
#   FileStreamLoc       Integer, representing byte location that the script is at in file stream
# * DateTime            String, holding date and time test was taken
#   OSName              String, holding OS name that this test was conducted with
#   OSArchitecture      String, holding OS architecture that this test was conducted with
#   OSVersion           String, holding OS version that this test was conducted with
#   JavaVersion         String, holding Java version that this test was conducted with
#   JavaVendor          String, holding Java vendor that this test was conducted with
#   NetworkType         String, holding Network Type that this test was conducted with
#   Server              String, holding Server that this test was conducted with
#   Host                String, holding Host that this test was conducted with
#   NetworkProvider     String, holding Network Provider that this test was conducted with (i.e. the Carrier)
#   NetworkOperator     String, holding Network Operator that this test was conducted with (i.e. the Carrier)
#                           note: Sometimes, the carrier name is in Network Provider, other times it is in Network Operator
#   DeviceID            String, the Device ID number
#   ConnectionType      String, holding Connection type that this test was conducted with
#   LocationID          Integer, the ID number of the location that this test was conducted at
#   Latitude            Integer, the latitude given by the GPS that this test was conducted at.
#                           Is 0 if no GPS data was available
#   Longitude           Integer, the latitude given by the GPS that this test was conducted at.
#                           Is 0 if no GPS data was available
#   mySpeedTests        List, holding all of the Individual Speed tests that are contained in the given file being parsed
#   short_str_method    Boolean, used in SpeedTestDataStructure if the printout requested in short of long.
#                           Default is False
#
# FUNCTIONS:
#   __init__ - initializes the object by parsing the data in the given file path. calls load()
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   filePath:   String, containing absolute path to raw data file
#       OUTPUTS-    none
#
#   loadHeaderInfo - initializes the object by parsing the data in the given file path.
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   filePath:   String, containing absolute path to raw data file
#       OUTPUTS-    none
#
#   createIndivTests -   ..
#       INPUTS-     ..
#       OUTPUTS-    ..
#
# * convertTo2D - Converts this SpeedTestFile object into a 2D array, and returns the result
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    tobeReturned:   the 2D array that will be returned
#
# * calc_TestTCP_StDev - For each test in this object, if the test is a TCP test, calculate the
#                        standard deviation of the sum of thread speeds at each 1 second interval.
#                        The IndivSpeedTest object will handle putting the value into the structure
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   structRef:  reference to the structure created in STDs.convertTo_ObjectToTCP()
#       OUTPUTS-    none
#
#   printSpeedTests - Return a string that has the information of each speed test in the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    text:   String, a representation of the IndividualSpeedTests held in
#                           this objects mySpeedTests
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
#
# ------------------------------------------------------------------------

from .utils import readToAndGetLine, monthAbbrToNum
from .utils import StDevP, getMedian
from .utils import global_str_padding as pad; pad = pad*1
from .TCP_Test import TCPTest
from .UDP_Test import UDPTest

class SpeedTestFile(object):
    # -------------------
    # Initializing some class attributes
    #File information
    FileName = "UNKNOWN"

    Date = "UNKNOWN"
    Time = "UNKNOWN"

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

    mySpeedTests = {}

    #Variables for tracking errors, filestream location, or str method
    FileStreamLoc = 0
    ignored_text = []
    short_str_method = False
    # -------------------

    # DESC: init functions calls load using the given file path
    def __init__(self, filePath, short=False):
        self.short_str_method = short
        self.ignored_text = []
        self.mySpeedTests = {  "TCP" : [],
                               "UDP" : []   }
        self.FileName = filePath.split("/")[-1]
        self.loadHeaderInfo(filePath)
    #END INIT


    # DESC: parses data and info in given file (location is filePath)
    #       and stores it in the object's attributes
    def loadHeaderInfo(self, filePath):
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
            self.Date = datetime.split(" ")[0]
            self.Time = datetime.split(" ")[1][:-1]
        else:
            self.NetworkType = "mobile"
            #Formatting the date and time as "mm/dd/yyyy" and "hh:mm:ss" when not in this format
            datetime = datetime.split("at ")[1][4:-1]
            month = str(monthAbbrToNum(datetime[:3]))
            day = str(datetime[4:6])
            year = str(datetime[-4:])
            time = str(datetime[7:9]) + ":" + str(datetime[10:12]) + ":" + str(datetime[13:15])
            self.Date = month + "/" + day + "/" + year
            self.Time = time
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
        #First TRY branch is for the mobile data files (no spaces in Network Provider)
        # Second TRY branch is for the netbook data files (space between Network and Provider)
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
        #First TRY branch is for the mobile data files (no spaces in Network Provider)
        # Second TRY branch is for the netbook data files (space between Network and Provider)
        try:
            self.DeviceID = readToAndGetLine(fs,"Device ID: ").split("Device ID: ")[1][:-1]
            if self.DeviceID == "": self.DeviceID = "N/A"
        except:
            fs.seek(self.FileStreamLoc)
            try:
                self.DeviceID = readToAndGetLine(fs,"Host name: ").split("Host name: ")[1][:-1]
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
            catching_exceptions_and_doing_nothing = True
        fs.seek(self.FileStreamLoc)

        #Set the file stream to the line after "Checking Connectivity"
        readToAndGetLine(fs, "Checking Connectivity..")
        self.FileStreamLoc = fs.tell()

        #Reading in the remaining contents of the file (the speed tests) and passing
        # it to the function that will split it into test chunks and create the objects
        remainingFileContents = fs.read()
        # !!!!
        # SUPER IMPORTANT!! Otherwise, problems galore
        # Don't want open streams o_O
        fs.close()
        #Passing the string of file contents to the function that will split each test into it's own unit
        self.createIndivTests(remainingFileContents)
    #END DEF


    # DESC: This takes the remaining contents of the file being parsed, splits the
    #       content by test (to included any error messages) and the creates the Test objects
    def createIndivTests(self, fileContents):
        fileContents = fileContents.split('\n\n')
        sortedFileContents = []
        appending = False
        for chunk in fileContents:
            if not appending:
                if "Starting Test " in chunk:
                    aTest =  chunk + "\n"
                    appending = True
                else:
                    continue
                #END IF/ELSE
            else:
                if "Starting Test " not in chunk:
                    aTest += chunk + "\n"
                else:
                    sortedFileContents.append(aTest)
                    aTest =  chunk + "\n"
                #END IF/ELSE
            #END IF/ELSE
            #This is so that the last test is appended, as it will not be when the loop finishes
            if chunk == fileContents[-1]:
                sortedFileContents.append(aTest)
            #END IF
        #END FOR
        for testText in sortedFileContents:
            testAsArray = testText.split('\n')
            command = ""
            #Getting the command line string used to run the test
            for line in testAsArray:
                if "Iperf command line" in line:
                    command = line; break
            #END FOR
            #Determining what kind of test the current chunk of test is
            # and calling the corresponding constructor
            if " -e " in command:
                newTCP = TCPTest(testText, short=self.short_str_method)
                self.mySpeedTests["TCP"].append(newTCP)
            elif " -u " in command:
                #The 1 second test chunk is organized a little differently than the 5 second test,
                # and needs to use a different variation of constructor
                if ("-t 1" in command):
                    #Adding an extra new line to separate each 1 second UDP test,
                    # and keeping track of the test number, as it is the same for each one
                    newTestText = ""
                    thisTestNumber = 0
                    for line in testText.split('\n'):
                        if "Starting Test" in line:
                            thisTestNumber = line.split(" ")[2].split(":")[0].split("..")[0]
                        if "Starting UDP 1" in line:
                            newTestText += '\n'
                        newTestText += line+'\n'
                    #END FOR
                    testText = newTestText.split('\n\n')
                    subTestNum = 0
                    for chunk in testText:
                        if "Starting UDP 1" in chunk:
                            subTestNum += 1
                            testNum = str(thisTestNumber)+"."+str(subTestNum)
                            newUDP = UDPTest(chunk, testNum, self.short_str_method)
                            self.mySpeedTests["UDP"].append(newUDP)
                    #END FOR
                else:
                    newUDP = UDPTest(testText, short=self.short_str_method)
                    self.mySpeedTests["UDP"].append(newUDP)
                #END IF/ELSE
            else:
                self.ignored_text.append(testText)
            #END IF/ELIF/ELSE
        #END FOR
    #END DEf


    """
    # DESC: Converts all of the individual test and ping threads and such
    #       in this object and returns a 2D array of it all
    def convertTo2D(self):
        toBeReturned = []
        #Setting up the basic information at the top of the 2D array/.csv file
        toBeReturned.append(["Filename", self.FileName])
        toBeReturned.append(["DateTime", self.Date + " " + self.Time])
        toBeReturned.append(["Location ID", self.LocationID])
        toBeReturned.append(["Network Type", self.NetworkType])
        toBeReturned.append(["Provider", (self.NetworkProvider
                                        if (self.NetworkProvider != "N/A")
                                        else self.NetworkOperator)])
        counter = 5
        testnum = 1
        for test in self.mySpeedTests:
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
            for thread in test.myPingThreads:
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
    """

    # DESC: Looping through each Test, if the test if of type TCP, then
    #       call it's thread sum function, and append the standard deviation to
    #       the passed structure reference.
    def calc_TCP_StDev_and_append_to_Distribution(self, structRef, list_carriers):
        for indivTest in self.mySpeedTests["TCP"]:
            if not indivTest.ERROR:
                if (self.NetworkOperator in list_carriers):
                    mycarrier = self.NetworkOperator
                elif (self.NetworkProvider in list_carriers):
                    mycarrier = self.NetworkProvider
                else:
                    continue
                #END IF/ELIF
                up_stdev = StDevP(indivTest.sumSpeed_UpThreads())
                if up_stdev is not None:
                    structRef[self.NetworkType]\
                             [mycarrier]\
                             [indivTest.ConnectionLoc]\
                             ["Up"].append(up_stdev)
                #END IF
                down_stdev = StDevP(indivTest.sumSpeed_DownThreads())
                if down_stdev is not None:
                    structRef[self.NetworkType]\
                             [mycarrier]\
                             [indivTest.ConnectionLoc]\
                             ["Down"].append(down_stdev)
                #END IF
            #END IF
        #END FOR
    #END DEF


    # DESC: ..
    def this_File_Index_in_MasterCSV(self, masterCSVRef):
        index = None
        for row in masterCSVRef:
            if ((self.DeviceID in str(row[13])) and
                (self.Date in str(row[5])) and
                (self.Time in str(row[6])) ):
                index = masterCSVRef.index(row)
                break
        return index
    #END DEF


    # DESC: ..
    def calc_StDev_and_Median_and_append_to_MasterCSV(self, origRef, list_carriers):
        thisFile = self.this_File_Index_in_MasterCSV(origRef)
        if thisFile is not None:
            westCount = 0
            eastCount = 0
            toAppend = [0]*16
            for indivTest in self.mySpeedTests["TCP"]:
                if not indivTest.ERROR:
                    upThread = indivTest.sumSpeed_UpThreads()
                    downThread = indivTest.sumSpeed_DownThreads()
                    up_stdev = StDevP(upThread)
                    up_median = getMedian(upThread)
                    down_stdev = StDevP(downThread)
                    down_median = getMedian(downThread)
                    if (indivTest.ConnectionLoc == "West"):
                        westCount += 1
                        toAppend[(westCount*8)-8] = up_stdev
                        toAppend[(westCount*8)-7] = up_median
                        toAppend[(westCount*8)-6] = down_stdev
                        toAppend[(westCount*8)-5] = down_median
                    else:
                        eastCount += 1
                        toAppend[(eastCount*8)-4] = up_stdev
                        toAppend[(eastCount*8)-3] = up_median
                        toAppend[(eastCount*8)-2] = down_stdev
                        toAppend[(eastCount*8)-1] = down_median
                #END IF
            #END FOR
            origRef[thisFile].extend(toAppend)
        #END IF
    #END DEF


    # DESC: Returns all of the sub tests for this file as a string
    def printSpeedTests(self):
        text = ""
        for speedTest in self.mySpeedTests["TCP"]:
            text +=  str(speedTest)
        for speedTest in self.mySpeedTests["UDP"]:
            text +=  str(speedTest)
        return text
    #END DEF


    # DESC: Returns a string representation of the object
    def __str__(self):
        if self.short_str_method:
            return (pad + "Filename: " + self.FileName + "\n" +
                    pad + "DateTime of Speed Test: " + self.Date + " " + self.Time + "\n" +
                    pad + "Network Type: " + self.NetworkType + "\n" +
                    pad + "Network: Provider = " + self.NetworkProvider +
                          ", Operator = " + self.NetworkOperator + "\n" +
                    pad + "Device ID: " + self.DeviceID + "\n" +
                    pad + "Location ID: " + self.LocationID + "\n" +
                    self.printSpeedTests() +
                    "\n"
                    )
        else:
            return (pad + "Filename: " + self.FileName + "\n" +
                    pad + "DateTime of Speed Test: " + self.Date + " " + self.Time + "\n" +
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
