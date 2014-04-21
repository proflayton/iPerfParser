

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
# CSVEXPORTER.PY
#
# AUTHOR(S):    Peter Walker    pwalker@csumb.edu
#               Brandon Layton  blayton@csumb.edu
#
# PURPOSE-  This file provides some functions that will be used to convert
#           data structures into 2D arrays, and then converting the 2D arrays
#           into .csv files
#
# FUNCTIONS:
#   csvExport - Used to initialize an object of this class
#       INPUTS-     a_2D_Array:     A 2-dimensional array with each sub array representing
#                                   a line in the end csv file
#                   fileNameToSave: The full path of the resulting csv file
#       OUTPUTS-    none
#
# ------------------------------------------------------------------------


# DESC: This fuction takes in two values:
#       The 2D representing the rows and columns in the CSV
#       The fileName in which the CSV will be saved to
def csvExport(a_2D_Array, fileNameToSave):
    f = open(fileNameToSave,"w")
    for row in a_2D_Array:
        rowOfText = ''
        for col in row:
            rowOfText += ('"' + str(col) + '",')
        f.write(rowOfText[:-1]+"\n")
    f.close()
#END DEF
