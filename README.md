iPerfParser
===========


This Program is currently out-of-date. More updated version, which will provide use of MySQL database to store and analyze data is available at https://github.com/pwalker91/iPerfParser_with_DB_Storage


iPerf Parser in Python
 - main.py is the starting script that will be run. It uses class files located in ParserStructure, which are used to store speed test information. After choosing the starting folder (which houses all of the raw data files), the parser will interpret the raw data into objects, and then ask the user what kind of analysis they would like done.

 - Current analyses:
   + Distribution of the standard deviation of TCP connections. The speeds used
     are the sum of all four threads’ speeds at each one second interval.
     (e.g.) thread4(0-1)speed = 400KB/s
            thread3(0-1)speed = 500KB/s
            thread6(0-1)speed = 200KB/s
            thread5(0-1)speed = 0KB/s
            sum = 1100KB/s
            sumThread = [1100KB/s, .. ]
            StDev = population stdev of sumThread [speed1, speed2, speed3, .. ]
     These StDevs are calculated for both directions (Up and Down) in all TCP tests,
     in all files, and a distribution is calculated. The distribution is separated
     by network type (mobile vs netbook), carrier, and direction
   +





 - The top-level structure created is organized as such:
Speed_Test_Data_Structure
 \__
    { mobile:
           \__{ Carrier #1: []
                              \__[SpeedTestFile #1, SpeedTestFile #2, .. ] ,
                Carrier #2: []    
      netbook:                \__[SpeedTestFile #3, SpeedTestFile #4, .. ]  }
           \__{ Carrier #1: []
                              \__[SpeedTestFile #5, SpeedTestFile #6, .. ] , 
                Carrier #2: []
                              \__[SpeedTestFile #7, SpeedTestFile #8, .. ]  }  }

{} represents a python dictionary
[] represents a python list

 - The SpeedTestFile objects are structured as follows:
SpeedTestFile
 \__FileName, FileStreamLoc, DateTime, OSName, OSArchitecture, OSVersion
  __JavaVersion, JavaVendor, NetworkType, Server, Host, NetworkProvider, NetworkOperator
  __DeviceId, ConnectionType, LocationID, Latitude, Longitude 
 |
 \__this_SpeedTests = [IndividualSpeedTest #1, IndividualSpeedTest #2, .. ]
      \__
         IndividualSpeedTest
           \__ConnectionType, ConnectionLoc, ReceieverIP, Port
           |
           \__this_PingThreads = [PingThread #1, PingThread #2, .. ]
                \__
                   PingThread
                     \__PipeNumber, DataDirection
                      __LocalIP, LocalPort, ServerIP, ServerPort
                      __final_secIntervalStart, final_secInteravalEnd
                      __final_size, final_speed
                      __Datagrams, ERROR
                     |
                     \__this_Pings = [Ping #1, Ping #2, Ping #3, .. ]
                          \__Ping
                               \__secIntervalStart, secIntervalEnd
                                __size, speed




