
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
# PINGS.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  Holds a single measurement of data transfer speed in a single test
#           (i.e. This object represent one line of text in a speed test)
#
# VARIABLES:
#   secIntervalStart    Float, represents the start time of this Ping
#   secIntervalEnd      Float, represents the end time of this Ping (should always be start + 1)
#   size                Float, represents this Ping's size in Kbits sent
#   speed               Float, represents this Ping's speed in KBytes/sec
#   size_string         String, converted from size, used in __str__
#   size_units          String, units to be appended to string
#   speed_string        String, converted from speed, used in __str__
#   speed_units         String, units to be appended to string
#
# FUNCTIONS:
#   __init__ - Used to initialize an object of this class
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    none
#
#   __str__ - Returns a string represenation of the object
#       INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
#       OUTPUTS-    String, representing the attributes of the object (THIS)
# ------------------------------------------------------------------------
from .utils import global_str_padding as pad; pad = pad*4
class Ping(object):
    # ------------------
    # Initializing some class attributes
    secIntervalStart = 0
    secIntervalEnd   = 0

    size             = 0
    speed            = 0

    size_string      = ""
    size_units       = ""
    speed_string     = ""
    speed_units      = ""
    # ------------------

    # DESC: Initializing class
    def __init__(self, data, size_u, speed_u):
        self.size_units = size_u
        self.speed_units = speed_u
        #This takes the given data String and parses the object information
        data_start = data.split("-")[0].split("]")[1].strip()
        data       = data.split("-")[1]
        data_end   = data.split("sec", 1)[0].strip()
        data       = data.split("sec", 1)[1]
        data_size  = data.split(self.size_units)[0].strip()
        data       = data.split(self.size_units)[1]
        data_speed = data.split(self.speed_units)[0].strip()
        self.secIntervalStart = float(data_start)
        self.secIntervalEnd = float(data_end)
        self.size = float(data_size)
        self.speed = float(data_speed)

        #This section adds the zeros following the speed and size numbers, as sometimes
        # the size may vary between ##.# and ###
        if ("." in data_size):
            if (len(data_size.split(".")[1]) == 1):
                data_size += "0"
            #END IF
        else:
            data_size += ".00"
        self.size_string = data_size
        if ("." in data_speed):
            if (len(data_speed.split(".")[1]) == 1):
                data_speed += "0"
            #END IF
        else:
            data_speed += ".00"
        self.speed_string = data_speed

        #Creating the padding of spaces needed to line up all of the numbers
        # The padding after the time varies because the time may be between 0 and 99.
        # If the start and end are both 1 digit, two spaces are needed. If start and end are
        #  a 1 and 2 digit number, one space is needed
        self.time_pad = ""
        if self.secIntervalEnd < 10.0:
            self.time_pad = "  "
        elif self.secIntervalStart < 10.0 and self.secIntervalEnd >= 10.0:
            self.time_pad = " "

        from math import log10
        self.size_pad = (" " * (4 - int(log10(self.size)))) if self.size else (" " * 4)
        self.speed_pad = (" " * (4 - int(log10(self.speed)))) if self.speed else (" " * 4)
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        return (pad + str(self.secIntervalStart) + "-"
                    + str(self.secIntervalEnd) + self.time_pad + "  " + self.size_pad 
                    + str(self.size_string) + " " + self.size_units + "  " + self.speed_pad 
                    + str(self.speed_string) + " " + self.speed_units 
               )
    #END DEF
#END CLASS