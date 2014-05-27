
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
#   Date                String, holding the date the test was taken
#   Time                String, holding the time test was taken
#   OSName              String, holding OS name that this test was conducted with
#   OSArchitecture      String, holding OS architecture that this test was conducted with
#   OSVersion           String, holding OS version that this test was conducted with
#   JavaVersion         String, holding Java version that this test was conducted with
#   JavaVendor          String, holding Java vendor that this test was conducted with
#   NetworkType         String, holding Network Type that this test was conducted with
#                           note: this is either mobile or netbook
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
#   FileStreamLoc       Integer, representing byte location that the script is at in file stream
#   ignored_text        String, text from original file that was ignored when splitting up text by Test
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
#       OUTPUTS-    None
#
#   createIndivTests - This takes the string of the entire file contents, and splits it up by test.
#                      These chunks are then passed to their appropiate constructors
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   fileContents:   String, containing the entire file contents
#       OUTPUTS-    None            As tests are created, they are added to the struct
#
#   convert_Obj_To_2D - Converts this SpeedTestFile object into a 2D array, and returns the result
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    objectAs2D:   the 2D array that will be returned
#
#   calc_TCP_StDev_for_Distribution - For each test in this object, if the test is a TCP test, calculate the
#                       standard deviation of the sum of thread speeds at each 1 second interval.
#                       The IndivSpeedTest object will handle putting the value into the structure
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   structRef:      reference to the structure created in STDs.convertTo_ObjectToTCP()
#                   list_carriers:  reference to array of carriers
#       OUTPUTS-    None
#
#   calc_TCP_StDev_and_Median_then_Append - This calculates the standard deviation and
#                       median of the TCP tests in this object, and then appends the values to
#                       the CPUC_Results CSV the is provided in the package
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   masterCSVRef:   reference to the 2D array of the CSV file
#       OUTPUTS-    None
#
#   calc_rVal_and_MOS_then_Append - ..
#       INPUTS-     ..
#       OUTPUTS-    ..
#
#   this_File_Index_in_GivenCSV - This looks for the row in the CPUC_Results CSV that corresponds
#                       to this object's information
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#                   masterCSVRef:   reference to the 2D array of the CSV file
#       OUTPUTS-    index:          Integer, the row index at which this file is located in the CPUC_Results CSV
#                                   If the file was not found in the CSV, returns None
#
#   get_Test_with_TestNumber - This takes a given string, whose value corresponds to the test number
#                       (which will be either 1, 2, 4, or 5), and returns the corresponding TCPTest
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   testType:   String, is either TCP, UDP, or PING.
#                   num:        String, the test number of the TCP test we wish to get
#       OUTPUTS-    test:       TCPTest object whose number corresponds to the given value in num.
#                               If no test was found, returns None
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
from .Ping_Test import PingTest

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
                               "UDP" : [],
                               "PING": []   }
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

        #Reading in the Date and Time of the test
        #Also setting the Network Type, as this is where the file types start to differ
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
            datetime = datetime.split("started at ")[1][4:-1]
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

        #Set the file stream to the beginning
        fs.seek(0)

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
        #First splitting the contents into sections. These section are all of the chunks
        # that are separated by two newline characters ('\n\n')
        fileContents = fileContents.split('\n\n')
        sortedFileContents = []
        appending = False
        aNewChunk = ""
        #These loops will create a very large string that contains all of the text
        # pertaining to one test. This will include error messages, if they are present.
        # A new test is know to start if "Starting Test" is in the string chunk. Once we
        # know that we have all of the string pertaining to one test, it is appended to the array
        for chunk in fileContents:
            if not appending:
                if "Starting Test " in chunk:
                    aNewChunk =  chunk + "\n"
                    appending = True
                else:
                    continue
                #END IF/ELSE
            else:
                if "Starting Test " not in chunk:
                    aNewChunk += chunk + "\n"
                else:
                    sortedFileContents.append(aNewChunk)
                    aNewChunk =  chunk + "\n"
                #END IF/ELSE
            #END IF/ELSE
            #This is so that the last test is appended, as it will not be when the loop finishes
            if chunk == fileContents[-1]:
                sortedFileContents.append(aNewChunk)
            #END IF
        #END FOR
        #Now we go through each of our sorted string chunks, and determine whether they are a TCP test,
        # a UDP test, or a Ping Test. The appropiate constructor is then called
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
                    #This loop adds an extra empty line in between each "sub" test. This is
                    # because in the string, there are 3 one second UDP test, and this is the
                    # easiest way to split them up later
                    for line in testText.split('\n'):
                        if "Starting Test" in line:
                            thisTestNumber = line.split(" ")[2].split(":")[0].split("..")[0]
                        if "Starting UDP 1" in line:
                            newTestText += '\n'
                        newTestText += line+'\n'
                    #END FOR
                    #This is when the 3 one second tests are separated. One by one, the UDP constructor
                    # is called, and the text passed is and individual one second UDP test.
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
            elif ("PING" in testText or "Pinging" in testText):
                newPing = None
                if self.NetworkType == "mobile":
                    newPing = PingTest(testText, isMobile=True, short=self.short_str_method)
                else:
                    newPing = PingTest(testText, isMobile=False, short=self.short_str_method)
                self.mySpeedTests["PING"].append(newPing)
            else:
                self.ignored_text.append(testText)
            #END IF/ELIF/ELSE
        #END FOR
    #END DEf


    # DESC: Converts all of the individual test and ping threads and such
    #       in this object and returns a 2D array of it all
    def convert_Obj_To_2D(self):
        objectAs2D = []
        #Setting up the basic information at the top of the 2D array/.csv file
        objectAs2D.append(["Filename", self.FileName])
        objectAs2D.append(["DateTime", self.Date + " " + self.Time])
        objectAs2D.append(["Location ID", self.LocationID])
        objectAs2D.append(["Network Type", self.NetworkType])
        objectAs2D.append(["Provider", (self.NetworkProvider
                                        if (self.NetworkProvider != "N/A")
                                        else self.NetworkOperator)])
        #Counter refers to the current array in objectAs2D. This array is
        # where the tests will start to be array-itized and appened
        for TCPTest in self.mySpeedTests["TCP"]:
            objectAs2D.extend(TCPTest.convert_Obj_To_2D())
        #END FOR
        #Now we create the arrays for the UDP tests, as their structure differs from
        # that of the TCP tests.
        for UDPTest in self.mySpeedTests["UDP"]:
            objectAs2D.extend(UDPTest.convert_Obj_To_2D())
        #END FOR
        #This is where we convert the Ping tests into 2D versions of themselves. Their data
        # is the appended to the end of the 2D array for this file.
        for PingTest in self.mySpeedTests["PING"]:
            objectAs2D.extend(PingTest.convert_Obj_To_2D())
        #END FOR
        return objectAs2D
    #END DEF


    # DESC: Looping through each Test, if the test if of type TCP, then
    #       call it's thread sum function, and append the standard deviation to
    #       the passed structure reference.
    def calc_TCP_StDev_for_Distribution(self, structRef, list_carriers):
        #We only use the TCP tests in the function
        for TCPTest in self.mySpeedTests["TCP"]:
            #We only use the test if there were no errors in it
            if not TCPTest.ERROR:
                #This if/else block makes sure that the test is in our list of carriers.
                # Otherwise, continue will skip to the next test in the object
                if (self.NetworkOperator in list_carriers):
                    mycarrier = self.NetworkOperator
                elif (self.NetworkProvider in list_carriers):
                    mycarrier = self.NetworkProvider
                else:
                    continue
                #END IF/ELIF
                up_stdev = StDevP(TCPTest.sum_Threads_Speed("Up"))
                if up_stdev is not None:
                    structRef[self.NetworkType]\
                             [mycarrier]\
                             [TCPTest.ConnectionLoc]\
                             ["Up"].append(up_stdev)
                #END IF
                down_stdev = StDevP(TCPTest.sum_Threads_Speed("Down"))
                if down_stdev is not None:
                    structRef[self.NetworkType]\
                             [mycarrier]\
                             [TCPTest.ConnectionLoc]\
                             ["Down"].append(down_stdev)
                #END IF
            #END IF
        #END FOR
    #END DEF


    # DESC: This uses the information in this object to find the row in the CPUC_Results CSV
    #       that it corresponds to. It first checks with DeviceID, Date, and Time. If that
    #       doesn't work, it tries with LocationID, Date, and Time.
    def this_File_Index_in_GivenCSV(self, masterCSVRef):
        index = None
        for row in masterCSVRef:
            if ((self.DeviceID in str(row[13])) and
                (self.Date in str(row[5])) and
                (self.Time in str(row[6])) ):
                index = masterCSVRef.index(row)
                break
        #END FOR
        if (index == None):
            for row in masterCSVRef:
                if ((self.LocationID in str(row[3])) and
                    (self.Date in str(row[5])) and
                    (self.Time in str(row[6])) ):
                    index = masterCSVRef.index(row)
                    break
            #END FOR
        #END IF
        return index
    #END DEF


    # DESC: Using the value passed in num, this looks for the test whose TestNumber
    #       corresponds to that value. If there was no such test, returns None
    def get_Test_with_TestNumber(self, num, testType="TCP"):
        if not isinstance(num, str):
            raise TypeError
        for aTest in self.mySpeedTests[testType]:
            if aTest.TestNumber == num:
                return aTest
        #END FOR
        return None
    #END DEF


    # DESC: This function first tries to find the index of this file in the CPUC_Results CSV.
    #       If the file was found, it calculates the StDev and Median for all of the TCP tests,
    #       and appends the values to the CSV.
    def calc_TCP_StDev_and_Median_then_Append(self, origCSVRef):
        thisFile = self.this_File_Index_in_GivenCSV(origCSVRef)
        if thisFile is not None:
            toAppend = []
            #The test number order is specific, as test 1 is the first TCP West, 2 is TCP East, etc.
            # Also, the array values are all strings, as the initialization removed the values 
            # from a string, and so the Test Number variable remained a string
            for testNum in ["1","2","4","5"]:
                indivTest = self.get_Test_with_TestNumber(testNum, "TCP")
                if indivTest is not None:
                    toAppend.extend( indivTest.create_Array_of_StDev_Median_for_CSV() )
                else:
                    toAppend.extend( ["error"]*4 )
            #END FOR
            origCSVRef[thisFile].extend(toAppend)
        #END IF
    #END DEF

    #DESC: Calculates rVal and MOS of ping tests and appends to CSV reference
    #      delayThresh = if under then they get bucketed
    def calc_rVal_and_MOS_then_Append(self, masterCSVRef, delayThresh):
        import math
        thisFile = self.this_File_Index_in_GivenCSV(masterCSVRef)
        east = 0;       west = 0
        eastTotal = 0;  westTotal = 0
        eastMax = 0;    westMax = 0
        eastLost = 0;   westLost = 0
        if thisFile is not None:
            toAppend = []
            for speedTest in self.mySpeedTests["PING"]:
                fd = 0.0
                for time in speedTest.Times:
                    time = float(speedTest.Times[time])
                    if speedTest.ConnectionLoc == "East":
                        eastLost += speedTest.PacketsLost
                        east+=1
                        eastTotal += time
                        if(time > eastMax):
                            eastMax = time
                        #END IF
                    elif speedTest.ConnectionLoc == "West":
                        westLost += speedTest.PacketsLost
                        west+=1
                        westTotal += time
                        if(time > westMax):
                            westMax = time
                        #END IF
                    #END IF/ELSE
                    if(time < delayThresh):
                        fd+=1
                    #END IF
            #END FOR
            if(east + west <= 0):
                #print("Error. east + west <= 0 for " + str(self.FileName))
                #Some error when pinging
                toAppend = ["NA","NA"]
            else:
                pktSecAve = (eastTotal + westTotal)/(east + west)
                #F(d) calculated
                fd = fd/(east + west)
                #loss rate
                pn = (eastLost + westLost)/(east + west)
                #loss rate of jitter buffer
                pb = (1-pn)*(1-fd)

                #Equipment impairment factor
                ieEff = 5 + 90*(pn+pb)/(pn+pb+10); 
                #14.96 + 16.68*math.log(1+30.11*(pn+pb));//14.96 + 16.68*Math.log(1+30.11*(pn+pbTwo));

                #calculate H(x) -either a zero or a one
                hofx = 1
                if ((pktSecAve-177.3)<0):
                    hofx = 0

                #calculate delay impairment factor
                idf = (0.024 * pktSecAve) + 0.11*(pktSecAve-177.3)*hofx;

                #calculate r value
                rvalue = 93.2 - idf - ieEff;
                #calculate MOS from r value
                mos = 1
                if (rvalue>=0):
                    mos = 1+0.035*rvalue+rvalue*(rvalue-60)*(100-rvalue)*7*math.pow(10, -6);

                toAppend = [rvalue,mos];
            #END IF

            masterCSVRef[thisFile].extend(toAppend)
        #END IF
    #END DEF


    # DESC: Returns all of the sub tests for this file as a string. If there are no
    #       tests, then it returns a string saying there were no tests
    def printSpeedTests(self):
        text = ""
        for speedTest in self.mySpeedTests["TCP"]:
            text +=  str(speedTest)
        for speedTest in self.mySpeedTests["UDP"]:
            text +=  str(speedTest)
        for speedTest in self.mySpeedTests["PING"]:
            text +=  str(speedTest)
        #END FOR
        if text == "":
            text = pad + "No viable network speed tests"
        return text
    #END DEF

    # DESC: Returns a string representation of the object
    def __str__(self):
        if self.short_str_method:
            return (pad + "Filename: " + str(self.FileName) + "\n" +
                    pad + "DateTime of Speed Test: " + str(self.Date) + " " + str(self.Time) + "\n" +
                    pad + "Network Type: " + str(self.NetworkType) + "\n" +
                    pad + "Network: Provider = " + str(self.NetworkProvider) +
                          ", Operator = " + str(self.NetworkOperator) + "\n" +
                    pad + "Device ID: " + str(self.DeviceID) + "\n" +
                    pad + "Location ID: " + str(self.LocationID) + "\n" +
                    self.printSpeedTests() +
                    "\n"
                    )
        else:
            return (pad + "Filename: " + str(self.FileName) + "\n" +
                    pad + "DateTime of Speed Test: " + str(self.Date) + " " + str(self.Time) + "\n" +
                    pad + "OS: " + str(self.OSName) + ", " + str(self.OSArchitecture) + ", " + str(self.OSVersion) + "\n" +
                    pad + "Java: " + str(self.JavaVersion) + ", " + str(self.JavaVendor) + "\n" +
                    pad + "Network Type: " + str(self.NetworkType) + "\n" +
                    pad + "Connection: Server = " + str(self.Server) + ", Host = " + str(self.Host) + "\n" +
                    pad + "Network: Provider = " + str(self.NetworkProvider) +
                          ", Operator = " + str(self.NetworkOperator) + "\n" +
                    pad + "Device: ID = " + str(self.DeviceID) +
                          ", Connection Type = " + str(self.ConnectionType) + "\n" +
                    pad + "Location ID: " + str(self.LocationID) + "\n" +
                    pad + "Latitude:" + str(self.Latitude) +
                          " Longitude:" + str(self.Longitude) + "\n" +
                    self.printSpeedTests() +
                    "\n"
                    )
    #END DEF
#END CLASS
