iPerfParser
===========

iPerf Parser in Python
 - main.py is the starting script that will be run. It uses class files located in iPerfClasses, which are used to store speed test information. After choosing the starting folder (which houses all of the raw data files), the parser will interpret the raw data into objects, and then ask the user what kind of analysis they would like done.

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
 \__
 |
 \__




