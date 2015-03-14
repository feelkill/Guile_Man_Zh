#!/usr/bin/python
#
# cut off guile.txt into pieces, and write the top level contents into different files.
#

import sys

# the import constants
theLeastLenOfTopLevelContentMarkerLine = 7
theChapterFileType = "md"

def IsTheTopLevelContentMarker(oneLine):
    # whether this line mark the top level content 
    if (len(oneLine) < theLeastLenOfTopLevelContentMarkerLine):
        return False
    
    for ch in oneLine[0:theLeastLenOfTopLevelContentMarkerLine]:
        if (ch != '*'):
            return False
    return True

def IsDigit(ch):
    return ch >= '0' and ch <= '9'

def ConvertToChapterName(titleStr, fileType):
    # return the file name according to the given title string and file type
    filename = []
    idx = 0
    total = len(titleStr)
    while idx < total:
        # handle the chapter seq number
        if idx == 0 and IsDigit(titleStr[0]):
            if IsDigit(titleStr[1]):
                filename.append(titleStr[0])
                filename.append(titleStr[1])
                idx = 2
            else:
                filename.append('0')
                filename.append(titleStr[0])
                idx = 1
            continue

        ch = titleStr[idx]
        if ch == ' ':
            filename.append('_')
        elif ch != '!':
            filename.append(ch)
        idx = idx + 1
    return ''.join(filename) + "." + fileType;

outputIsAvaiable = False
twoLines = [None, None]
nextpos  = 0
outfile = None
infile = open("guile.txt")
for eachline in infile.readlines():
    prevpos = (nextpos + 1) % 2
    twoLines[nextpos] = eachline

    # need to create file for a new chapter
    if IsTheTopLevelContentMarker(eachline):
        if outputIsAvaiable:
            # close the open file
            outfile.close()
        outfile = open(ConvertToChapterName(twoLines[prevpos][:-1], theChapterFileType), 'w')
        outfile.write(twoLines[prevpos])
        # don't write this line, which will be written into the next loop
        outputIsAvaiable = True
    # skip the unsed lines before the first chapter
    elif outputIsAvaiable and twoLines[prevpos] is not None:
        outfile.write(twoLines[prevpos])
    # move to the next position to record
    nextpos = (nextpos + 1) % 2

if outputIsAvaiable:
    # that last line shoud be written into correctly
    prevpos = (nextpos + 1) % 2
    outfile.write(twoLines[prevpos])
    outfile.close()
infile.close()

if __name__ == '__main__':
    def CheckTestcaseResult(expre):
        if True == expre:
            return " OK "
        else:
            return " Failed "

    print " ", '='*40
    print " IsTheTopLevelContentMarker() test01  ", CheckTestcaseResult( False == IsTheTopLevelContentMarker("*"))
    print " IsTheTopLevelContentMarker() test02  ", CheckTestcaseResult( False == IsTheTopLevelContentMarker("******"))
    print " IsTheTopLevelContentMarker() test03  ", CheckTestcaseResult( True  == IsTheTopLevelContentMarker("*******"))
    print " IsTheTopLevelContentMarker() test04  ", CheckTestcaseResult( True  == IsTheTopLevelContentMarker("********"))
    print " IsTheTopLevelContentMarker() test05  ", CheckTestcaseResult( False == IsTheTopLevelContentMarker(""))

    print " ", '='*40
    print " IsDigit() test01 ", CheckTestcaseResult( True == IsDigit('0'))
    print " IsDigit() test02 ", CheckTestcaseResult( True == IsDigit('1'))
    print " IsDigit() test03 ", CheckTestcaseResult( True == IsDigit('2'))
    print " IsDigit() test04 ", CheckTestcaseResult( True == IsDigit('3'))
    print " IsDigit() test05 ", CheckTestcaseResult( True == IsDigit('4'))
    print " IsDigit() test06 ", CheckTestcaseResult( True == IsDigit('5'))
    print " IsDigit() test07 ", CheckTestcaseResult( True == IsDigit('6'))
    print " IsDigit() test08 ", CheckTestcaseResult( True == IsDigit('7'))
    print " IsDigit() test09 ", CheckTestcaseResult( True == IsDigit('8'))
    print " IsDigit() test10 ", CheckTestcaseResult( True == IsDigit('9'))
    print " IsDigit() test11 ", CheckTestcaseResult( False == IsDigit("%c" % (int('9')+1)))

    print " ", '='*40
    print " ConvertToChapterName() test01 ", CheckTestcaseResult( "The_Guile_Reference_Manual" == ConvertToChapterName("The Guile Reference Manual", theChapterFileType)[:-3])
    print " ConvertToChapterName() test02 ", CheckTestcaseResult( "Preface" == ConvertToChapterName("Preface", theChapterFileType)[:-3])
    print " ConvertToChapterName() test03 ", CheckTestcaseResult( "01_Introduction" == ConvertToChapterName("1 Introduction", theChapterFileType)[:-3])
    print " ConvertToChapterName() test04 ", CheckTestcaseResult( "02_Hello_Guile" == ConvertToChapterName("2 Hello Guile!", theChapterFileType)[:-3])
    print " ConvertToChapterName() test05 ", CheckTestcaseResult( "03_Hello_Scheme" == ConvertToChapterName("3 Hello Scheme!", theChapterFileType)[:-3])
