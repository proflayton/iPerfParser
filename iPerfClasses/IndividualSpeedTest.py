
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




# Small tests within each Test file
# ------------------------------------------------------------------------
# INDIVIDUALSPEEDTEST.PY
#
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  ..
#
# FUNCTIONS:
#   __init__ - ..
#       INPUTS-     ..:     ..
#       OUTPUTS-    ..
#
# ------------------------------------------------------------------------
import io
from .utils import readToAndGetLine
from .utils import global_str_padding as pad
pad = pad*2
from .PingThread import PingThread
from .Pings import Ping

class SpeedTest():

    # ------------------------
    # Class variables
    #e.g. TCP, UDP
    ConnectionType = "UNKNOWN"
    #e.g. West, East
    ConnectionLoc = "UNKNOWN"

    RecieverIP = "UNKNOWN"
    Port = 0000

    # ------------------------

    def __init__(self, dataStream):
        self.this_PingThreads = []
        self.loadHeaderInfo(readToAndGetLine(dataStream, "Iperf command line:"))
        self.createPingThreads(dataStream)
    #END DEF


    def loadHeaderInfo(self, data):
        #splitting the first line from the rest of the data
        iPerfCommand = data.split("\n", 1)[0]

        #Finding the connection type
        if iPerfCommand.find("-e")>0:
            self.ConnectionType = "TCP"
        if iPerfCommand.find("-u")>0:
            self.ConnectionType = "UDP"

        #Getting the Reciever IP address
        c_opt_strt = iPerfCommand.find("-c")+3
        c_opt_end = iPerfCommand.find(" ", c_opt_strt)+1
        if (c_opt_end != 0):
            self.RecieverIP = iPerfCommand[c_opt_strt:c_opt_end]
        else:
            self.RecieverIP = iPerfCommand[c_opt_strt:]

        #Determining the Connection Location
        if self.RecieverIP == "184.72.222.65":
            self.ConnectionLoc = "East"
        if self.RecieverIP == "184.72.63.139":
            self.ConnectionLoc = "West"

        #Getting port number
        p_opt_strt = iPerfCommand.find("-p")+3
        p_opt_end = iPerfCommand.find(" ", p_opt_strt)+1
        if (p_opt_end != 0):
            self.Port = iPerfCommand[p_opt_strt:p_opt_end]
        else:
            self.Port = iPerfCommand[p_opt_strt:]

        #Getting test time interval number
        t_opt_strt = iPerfCommand.find("-t")+3
        t_opt_end = iPerfCommand.find(" ", t_opt_strt)+1
        if (t_opt_end != 0):
            self.TestInterval = iPerfCommand[t_opt_strt:t_opt_end]
        else:
            self.TestInterval = iPerfCommand[t_opt_strt:]
        #END IF/ELSE
    #END DEF


    def createPingThreads(self, dataStream):
        a = readToAndGetLine(dataStream,"[")
        while a:
            if a.strip() == '':
                break
            else:
                if self.ConnectionType == "TCP":
                    temp = a.split("[")[1]
                    threadNumber = temp.split("]")[0].replace(" ","")
                    temp = temp.split("]")[1]
                    if "local" in temp:
                        temp     = temp.split("local")[1]
                        localIP  = temp.split("port")[0].replace(" ","")
                        temp     = temp.split(localIP + " port")[1]
                        localPort= temp.split("connected")[0]
                        temp     = temp.split("connected with")[1]
                        serverIP = temp.split("port")[0]
                        temp     = temp.split("port")[1]
                        serverPort=temp.split("\n")[0]
                        self.this_PingThreads.append(
                            PingThread(threadNumber,localIP,localPort,serverIP,serverPort)
                            );
                        #print("Local")
                    elif threadNumber == "SUM":
                        pass
                    else:
                        start = temp.split("-")[0].replace(" ","")
                        temp  = temp.split("-")[1]
                        end   = temp.split("sec")[0].replace(" ","")
                        temp  = temp.split("sec")[1]
                        size  = temp.split("KBytes")[0].replace(" ","")
                        temp  = temp.split("KBytes")[1]
                        speed = temp.split("Kbits/sec")[0].replace(" ","")

                        currPingThread = self.getPingThreadWithNumber(threadNumber)

                        currPingThread.addPing(Ping(start,end,size,speed))
                        #print("CURR: " + str(currPingThread))
                    #END IF/ELSE
                elif self.ConnectionType == "UDP":
                    temp = a.split("[")[1]
                    threadNumber = temp.split("]")[0]
                    temp = temp.split("]")[1]
                    if "local" in temp:
                        temp     = temp.split("local")[1]
                        localIP  = temp.split("port")[0].replace(" ","")
                        temp     = temp.split(localIP + " port")[1]
                        localPort= temp.split("connected")[0]
                        temp     = temp.split("connected with")[1]
                        serverIP = temp.split("port")[0]
                        temp     = temp.split("port")[1]
                        serverPort=temp.split("\n")[0]
                        self.this_PingThreads.append(
                            PingThread(threadNumber,localIP,localPort,serverIP,serverPort)
                            );
                        #print("Local")
                    elif "-" in temp:
                        if "datagrams" in temp:
                            #error with the test (datagrams received out-of-order)
                            a = dataStream.readline() 
                            continue
                        start = temp.split("-")[0].replace(" ","")
                        temp  = temp.split("-")[1]
                        end   = temp.split("sec")[0].replace(" ","")
                        temp  = temp.split("sec")[1]
                        size  = temp.split("KBytes")[0].replace(" ","")
                        temp  = temp.split("KBytes")[1]
                        speed = temp.split("Kbits/sec")[0].replace(" ","")

                        self.this_PingThreads[0].addPing(
                            Ping(start,end,size,speed)
                            ) 
                    elif "datagrams" in temp:
                        datagrams = temp.split("Sent")[1].split("datagrams")[0].replace(" ","")
                        self.this_PingThreads[0].datagrams = datagrams
                    elif "Server Report" in temp:
                        #the report is actually a line down
                        temp = dataStream.readline() 
                    #END IF/ELSE
                else:
                    print("ERROR! NO CONNECTION TYPE")
                    return
                #END IF/ELSE
            #END IF/ELSE
            a = dataStream.readline()
        #END LOOP
    #END DEF

    #Searches for the ping thread with the threadNumber provided
    #Gets the LATTER one so that when new ones are created, we add to that one
    def getPingThreadWithNumber(self,threadNumber):
        realPing = None
        for ping in self.this_PingThreads:
            if ping.testNum == threadNumber:
                realPing = ping
        return realPing
    #END DEF


    def __str__(self):
        this_str = (pad + " Connection Type: " + self.ConnectionType + "\n" +
                    pad + " Connection Location: " + self.ConnectionLoc + "\n" +
                    pad + " Reciever IP:" + self.RecieverIP + " port:" + str(self.Port) + "\n" +
                    pad + " Test Interval:" + self.TestInterval + "\n"
                   )

        for pingThread in self.this_PingThreads:
            this_str = (
                        this_str + 
                        pad + pad+ str(pingThread) + "\n"
                        )

        return this_str
    #END DEF
#END CLASS
