
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
# TCP.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This class will hold just an individual speed test (be it either a TCP or UDP test).
#           This will be where we have functions that do a lot of data analysis functions (like
#           standard deviation of TCP upload and download speed tests).
#
# VARIABLES:
#   ConnectionType      String, represents the type of connection (TCP or UDP)
#   WindowSize          Integer, the size of TCP window to be used in this test
#   ConnectionLoc       String, represents where this test is connected to (East or West)
#   myPingThreads       list, holding all of the PingThreads in this test
#   RecieverIP          String, IP of the server this test is connected to
#   Port                Integer, the port this test is connected to
#   TestInterval        Integer, the length of time that the test will be run
#   MeasuringFmt        String, the format (Kbytes, Kbits, etc.) that the data has been stored in
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
#   loadHeaderInfo - Given a string (in most cases, a line read from the file stream starting
#                    with "Iperf command line:"), this section will use the string to determine
#                    the basic information about this test
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#                   data:   a String, holding the command used to run this iPerf test, which
#                           also has all of the information we need
#       OUTPUTS-    none
#
#   createPingThreads - Given the data stream, parses the Speed Test streams into
#                       individual Ping Threads
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#                   dataStream: a data stream, with the rest of the Speed Test information
#       OUTPUTS-    none
#
#   convert_Obj_To_2D - Converts this SpeedTestFile object into a 2D array, and returns the result
#       INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    objectAs2D:   the 2D array that will be returned
#
#   getLongestThreadTime - The looks through all of the threads in this function and
#                          returns the longest thread time in seconds
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    time:   Integer, representing the longest thread time
#
#   getThreadWithNum - ..
#       INPUTS-     ..
#       OUTPUTS-    ..
#
#   sum_Threads_Speed - Creating an array of the sum of each 1 second interval of all 4 thread's speed
#       INPUTS-     self:               reference to the object calling this method (i.e. Java's THIS)
#                   direction:          String, threads of specified direction (Up or Down) that will be summed
#       OUTPUTS-    threads_summed:     an array containing values representing the sum of each 4 threads' speed
#
#   create_Array_of_StDev_Median_for_CSV - Creates 4 value long array, to be returned to the SpeedTestFile object.
#                        The four values are the StDev and Median of each direction (Up and Down)
#       INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    toReturn:   Array, 4 values corresponding to this test's StDev and Median for Up and Down direction
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import calcStDevP, getMedian
from .utils import global_str_padding as pad; pad = pad*2
from .IndividualSpeedTest import SpeedTest
from .PingThread import PingThread
from .Pings import Ping

class TCPTest(SpeedTest):
    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "TCP"
    WindowSize = 0

    #---- Inherited Variables ----
    # ConnectionLoc = "UNKNOWN"
    # myPingThreads = []
    # TestNumber = 0
    # RecieverIP = "UNKNOWN"
    # Port = 0000
    # TestInterval = 0
    # MeasuringFmt = None
    # iPerfCommand = ""
    # ERROR = False
    # ErrorMessage = None
    # short_str_method = False
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString, testNum=0, short=False):
        #Call the parent class' __init__
        SpeedTest.__init__(self, dataString, testNum, short)
        if not self.iPerfCommand: return
        #Getting the window size
        self.WindowSize = self.iPerfCommand[self.iPerfCommand.find("-w"):].split(" ")[1].strip()
        if not self.ERROR:
            #Declaring and creating the Ping Threads for this test
            self.myPingThreads = { "Up" : [], "Down" : [] }
            #This will run the function that creates the Ping Threads, but will only
            # clear self.text if there were no errors
            if self.createPingThreads():
                self.text = None
            #END IF
    #END DEF


    # DESC: Given the data stream, parses the Speed Test streams into individual Ping Threads
    def createPingThreads(self):
        #This block does the initial organization, going through each line and
        # putting them into the array whose key corresponds with their thread number.
        tempThreads = {}
        for line in self.text:
            if ("[" in line) and ("SUM" not in line):
                newKey = line.split("]")[0][1:].strip()
                if newKey not in tempThreads.keys():
                    tempThreads[newKey] = []
                #END IF
                tempThreads[newKey].append(line)
            #END IF
        #END FOR
        #Now that everything is sorted, we are going to put everything into a try/except block.
        # If there is any error, we know that there must have been something wrong with what was 
        # recorded by the iPerf program, and the test is ignored. The ErrorMessage will say which
        # test caused the problem.
        currentThreadNum = ""
        try:
            #This block does the initial declaration of further organization, setting up
            # the structure to separate the Upload threads from the Download threads.
            dirSplitTempThreads = {"Up":{},"Down":{}}
            for key in list(tempThreads):
                dirSplitTempThreads["Down"][key] = []
                dirSplitTempThreads["Up"][key] = []
            #END FOR
            #This block goes through each thread in the first structure, and essentially
            # divides the array of strings in half, putting the Upload streams into their
            # appropiate array, and the Downloads in their's.
            for thread in tempThreads:
                #Tracking which thread num we are dealing with
                currentThreadNum = thread
                #Each thread startes with a line containing "connected with", and a second one
                # later in the array of line. These are where the program switched from uploading to
                # downloading, and is where we can split the array into two separate arrays.
                direction = ["Up", "Down"]
                dircInd = -1
                for line in tempThreads[thread]:
                    if "connected with" in line:
                        dircInd += 1
                    dirSplitTempThreads[direction[dircInd]][thread].append(line)
                #END FOR
            #END FOR
            #Sorting the arrays of threads, as they are now organized by thread and direction.
            # Once the sorted() function runs, the line are not in their correct order. We need to take
            # the last line (which contains the "local xxx.xxx.xxx.xxx ....") and the second line (which is
            # the [x] 0.0-t.t line, or the summation line) and put them in their respective locations, which
            # is the beginning and end of the array of lines
            for direction in dirSplitTempThreads:
                for thread in dirSplitTempThreads[direction]:
                    #Tracking which thread num we are dealing with
                    currentThreadNum = thread
                    #Sorting the array, and then removing the final element (which contains
                    # "connected with") and the second element (contains the sum). The array is
                    # redeclared, with the "connected with" in front, the remaining array next, and then
                    # the final string appended to the end
                    temp = sorted(dirSplitTempThreads[direction][thread])
                    start = temp.pop(-1); end = temp.pop(1)
                    dirSplitTempThreads[direction][thread] = [start]
                    dirSplitTempThreads[direction][thread].extend(temp)
                    dirSplitTempThreads[direction][thread].append(end)
            #END FOR
            #Now pass each array of Pings (as Strings) to the PingThread constructor
            for direction in dirSplitTempThreads:
                for thread in dirSplitTempThreads[direction]:
                    self.myPingThreads[direction].append( 
                        PingThread(dirSplitTempThreads[direction][thread],
                                   thread, direction,
                                   self.MeasuringFmt["Size"],
                                   self.MeasuringFmt["Speed"],
                                   self.short_str_method) )
            #END FOR
            return True
        except:
            #If there was an error in the sorting of the file, there must have been some problem in what
            # was output by iPerf. The ErrorMessage will give a clue to which test, and which thread has the problem
            self.ERROR = True
            self.ErrorMessage = ("There was an error in the output of the network test. "+
                                 "Check test #" + str(self.TestNumber) + " , around thread #" + currentThreadNum
                                )
            self.myPingThreads = []
            return False
        #END TRY/EXCEPT
    #END DEF


    # DESC: This converts the object into a 2D representation of itself. Will return a 2D array
    #       that will be used in the SpeedTestFile class.
    def convert_Obj_To_2D(self):
        objectAs2D = []
        index = 0
        #This section sets up the column headers for the test. Each
        # test will have column headers. The timing headers need
        # to account for different length threads, hence getLongest
        test_length = int(self.getLongestThreadTime())
        objectAs2D.append(["","","","Thread Num","Data Direction"])
        #This loop creates the text above the tests that show what interval the numbers
        # correspond to. An empty value is appended because we are going to print out
        # the speed and size with one cell per value.
        for t in range(test_length):
            objectAs2D[index].append(str(float(t)) + "-" + str(float(t+1)))
            objectAs2D[index].append("")
        #END FOR
        #After creating the array that holds the second intervals, we add the END column,
        # which is where the final ping will go
        objectAs2D[index].append("END")
        #These two lines set up the Test information in the array
        objectAs2D.append(["","","Test #" + self.TestNumber])
        objectAs2D.append(["","",self.ConnectionType+" "+self.ConnectionLoc])
        index +=1
        #If the test has an error, then we print error. Otherwise, we array-itize the
        # threads and add then to the 2D array
        if (self.ERROR):
            objectAs2D[index].extend(["ERROR","ERROR","ERROR"])
            index += 1
        else:
            #Append the threads to the array. We first append the Ups, then the Downs
            # (test_length*2)+4 refers to how many elements must be in the array that will
            # be returned by array_itize(). The longest thread is of length "test_length", and
            # each row has two items (speed and size), and the +4 is for the final Ping object
            for thread in self.myPingThreads["Up"]:
                try:
                    objectAs2D[index].extend(thread.array_itize((test_length*2)+4))
                except:
                    objectAs2D.append(["","",""])
                    objectAs2D[index].extend(thread.array_itize((test_length*2)+4))
                index += 1
            #END FOR
            for thread in self.myPingThreads["Down"]:
                try:
                    objectAs2D[index].extend(thread.array_itize((test_length*2)+4))
                except:
                    objectAs2D.append(["","",""])
                    objectAs2D[index].extend(thread.array_itize((test_length*2)+4))
                index += 1
            #END FOR
        #END IF/ELSE
        #Adding a little spacer between the tests.
        objectAs2D.append(["",""])
        return objectAs2D
    #END DEF


    # DESC: In this test, find the longest thread time among all of the threads of the given direction
    def getLongestThreadTime(self, direction_passed="ALL"):
        time = 0
        if self.ERROR:
            return time
        if (direction_passed != "Up") and (direction_passed != "Down"):
            for direction in self.myPingThreads:
                for thread in self.myPingThreads[direction]:
                    #As long as the PingThreads array of Pings is ordered correctly, the last
                    # Ping object will always be the last Ping in the sequence. Hence, we can -1
                    new_time = thread.myPings[-1].secIntervalEnd
                    time = new_time if new_time > time else time
            #END FOR
        else:
            for thread in self.myPingThreads[direction_passed]:
                new_time = thread.myPings[-1].secIntervalEnd
                time = new_time if new_time > time else time
            #END FOR
        return time
    #END DEF


    # DESC: ..
    #       ..
    def getThreadWithNum(self, direction="Up", pipeNum="3"):
        if pipeNum not in ["3","4","5","6"]:
            print("You must input a string, either 3, 4, 5, or 6")
            print(pipeNum)
            raise SystemExit
        #END IF
        if (direction != "Up") and (direction != "Down"):
            direction = "Down"
        #END IF
        for thread in self.myPingThreads[direction]:
            if thread.PipeNumber == pipeNum:
                return thread
        #END FOR
        return None
    #END DEF


    # DESC: This returns the sum of the threads of the given direction in this test
    def sum_Threads_Speed(self, direction="Down"):
        if (direction != "Up") and (direction != "Down"):
            direction = "Down"
        #END IF
        threads_summed = []
        #Calculating max thread length
        max_up_length = int(self.getLongestThreadTime(direction))
        #Get the sums of the Up threads. The first FOR loop will iterate X number of times
        # based on what was returned by getLongestThreadTime(). Within the FOR loop, we set up
        # a temporary variable. We then try to add a specific interval (e.g. 1.0-2.0 sec) for each
        # thread to the temporary variable. If the interval does not exist, then nothing is added
        # (i.e. we add 0). We then append this value to Up_threads_sum, which will be returned.
        for step in range(max_up_length):
            temp = 0
            for thread in self.myPingThreads[direction]:
                try: temp += thread.myPings[step].speed
                except: pass
            #END FOR
            threads_summed.append(temp)
        #END FOR
        return threads_summed
    #END DEF


    # DESC: This creates an array of 4 values that will be appended to the Results CSV
    # provided by CPUC. If there was an error in the test, the 4 values returned say "TestDataError",
    # otherwise, the 4 values are the StDev and Median for both thread directions for this test
    def create_Array_of_StDev_Median_for_CSV(self):
        toReturn = []
        #If there was no error, there are values to StDev and Median
        # Otherwise, we return an array of "None"
        if not self.ERROR:
            #Calculating the stDev's and medians of the Up and Down threads
            upThread = self.sum_Threads_Speed("Up")
            downThread = self.sum_Threads_Speed("Down")
            toReturn.append( calcStDevP(upThread) )
            toReturn.append( getMedian(upThread) )
            toReturn.append( calcStDevP(downThread) )
            toReturn.append( getMedian(downThread) )
        else:
            toReturn = ["DataError"]*4
        return toReturn
    #END DEF


    # DESC: Creating a string representation of our object
    def __str__(self):
        this_str = (pad + "Test Number: " + str(self.TestNumber) + "\n" +
                    pad + "Connection Type: " + str(self.ConnectionType) + "\n" +
                    pad + "Connection Location: " + str(self.ConnectionLoc) + "\n"
                   )
        if not self.short_str_method:
            this_str += (pad + "Reciever IP:" + str(self.RecieverIP) + " port:" + str(self.Port) + "\n" +
                         pad + "Test Interval:" + str(self.TestInterval) +
                             "  Window Size:" + str(self.WindowSize) +
                             "  Measurement Format:" + str(self.MeasuringFmt["Size"]) +
                                               ", " + str(self.MeasuringFmt["Speed"]) + "\n"
                        )
        if self.ERROR:
            this_str += pad + "  ERROR: " + str(self.ErrorMessage) + "\n"
        else:
            for num in ["3","4","5","6"]:
                this_str += str(self.getThreadWithNum("Up", num))
            for num in ["3","4","5","6"]:
                this_str += str(self.getThreadWithNum("Down", num))
            #END FOR
        #END IF/ELSE
        return this_str
    #END DEF
#END CLASS
