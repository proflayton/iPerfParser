
# ------------------------------------------------------------------------
# READTO.PY
#
# AUTHOR(S):    Brandon Layton
#
# PURPOSE-  To read to a given delimiter in a given file stream
#
# FUNCTIONS:
#   readToAndGetLine - Given a file stream, reads the stream until the delimiter is found
#       INPUTS-     fileStream: FileStream object, called with open(FILEPATH, 'r')
#                   delimiter:  String, the text that you are looking for
#       OUTPUTS-    line:       String, containing the fully read line that contained the delimiter
#
# ------------------------------------------------------------------------
def readToAndGetLine(fileStream, delimiter):
    line = fileStream.readline()
    while delimiter not in line:
        line = fileStream.readline()
        if not line: break
    return line