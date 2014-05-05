
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
#   speed_string        String, converted from speed, used in __str__
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
class Ping():
    # ------------------
    # Initializing some class attributes
    secIntervalStart = 0
    secIntervalEnd   = 0

    size             = 0
    speed            = 0

    size_string      = ""
    speed_string     = ""
    # ------------------

    # DESC: Initializing class
    def __init__(self, data):
        #This takes the given data String and parses the object information
        data_start = data.split("-")[0].strip()
        data       = data.split("-")[1]
        data_end   = data.split("sec", 1)[0].strip()
        data       = data.split("sec", 1)[1]
        data_size  = data.split("KBytes")[0].strip()
        data       = data.split("KBytes")[1]
        data_speed = data.split("Kbits")[0].strip()
        self.secIntervalStart = float(data_start)
        self.secIntervalEnd = float(data_end)
        self.size = float(data_size)
        self.speed = float(data_speed)


        if ("." in data_size):
            if (len(data_size.split(".")[1]) == 1):
                data_size += "0"
        else:
            data_size += ".00"
        self.size_string = data_size
        if ("." in data_speed):
            if (len(data_speed.split(".")[1]) == 1):
                data_speed += "0"
        else:
            data_speed += ".00"
        self.speed_string = data_speed
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        time_pad = ""
        if self.secIntervalEnd < 10.0:
            time_pad = "  "
        elif self.secIntervalStart < 10.0 and self.secIntervalEnd >= 10.0:
            time_pad = " "

        size_pad = ""
        if self.size < 10:
            size_pad = "  "
        elif self.size < 100:
            size_pad = " "

        speed_pad = ""
        if self.speed < 10:
            speed_pad = "  "
        elif self.speed < 100:
            speed_pad = " "

        return (pad + str(self.secIntervalStart) + "-"
                    + str(self.secIntervalEnd) + time_pad + "   " +
                size_pad + str(self.size_string) + " Kbytes " + "   " +
                speed_pad + str(self.speed_string) + " Kbytes/sec"
               )
    #END DEF
#END CLASS