
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
# AUTHOR(S):   Peter Walker, Brandon Layton
#
# PURPOSE-  Holds a single measurement of data transfer speed in a single test
#           (i.e. This object represent one line of text in a speed test)
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
from .utils import global_str_padding as pad
pad = pad*4
class Ping():
    # ------------------
    # Initializing some class attributes
    secIntervalStart = 0
    secIntervalEnd   = 0

    size             = 0
    speed            = 0
    # ------------------

    # DESC: Initializing class
    def __init__(self, data):
        #This takes the given data String and parses the object information
        start = data.split("-")[0].replace(" ","")
        data  = data.split("-")[1]
        end   = data.split("sec")[0].replace(" ","")
        data  = data.split("sec")[1]
        size  = data.split("KBytes")[0].replace(" ","")
        data  = data.split("KBytes")[1]
        speed = data.split("Kbits/sec")[0].replace(" ","")
        self.secIntervalStart = start
        self.secIntervalEnd = end
        self.size = size
        self.speed = speed
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        return (pad + self.secIntervalStart + "-" + self.secIntervalEnd +
                " " + self.size + "Kbytes, " +
                " " + self.speed + "Kbytes/sec"
               )
    #END DEF
#END CLASS