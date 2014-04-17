'''
This fuction takes in two values:
The 2D representing the rows and columns in the CSV
The fileName in which the CSV will be saved to
'''
def export(Array2D,fileNameToSave):
    f = open(fileNameToSave,"w")
    for row in Array2D:
        rowOfText = ''
        for col in row:
            rowOfText += ('"' + str(col) + '",')
        f.write(rowOfText[:-1]+"\n")
    f.close()