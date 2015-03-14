#!/usr/bin/python
#coding=utf-8
#
# cut off guile.txt into pieces, and write the n-level contents into different files.
#

import sys

# all the default values, and maybe used for default argument
globalTheLeastRepeats = 7
globalOutputPostfix = "md"
globalExecProgram = "split_nlevel_contents.py"

# help/usage metainfo
#    the key is <option name> which is displayed in command string and begun with '-' or '--'
#    the value is a list containing the followings:
#        <option value>, which is holdplace for passed argument value
#                  it's None for bool datatype.
#        <help info description>, descript this command argument in detail
#        <whether set the default>, bool datatype, False if forced given, or True if optional given
#        <default argument value>, the default argument value or None
#
globalFunctionalOpts = {
    "-f" : ["infile",  " the file about n-level contents ", False, None],
    "-m" : ["marker",  " the n-level marker ",              False, None],
    "-n" : ["number",  " at least how many char within n-level marker ", True, globalTheLeastRepeats],
    "-t" : ["postfix", " the postfix of output file ",      True, globalOutputPostfix]
};

# the other non-functional command arguments, for example '-h'
# either functional or non-functional is needed, and the case don't make any sense in which they appear both.
globalNonFunctionalOpts = {
    "-T" : [None,      " only just run all the testcases ", True, False],
    "-h" : [None,      " only print help infomation",       True, False]
};

# store the real command arguments for user inputting.
globalRealCmdArgVals = {}

def OptHasDefaultVal(optValList):
    return optValList[2]

def OptGetDefaultVal(optValList):
    return optValList[3]

def OptIsOfBoolType(optValList):
    return optValList[0] is None

def OptGetOptValue(optValList):
    return optValList[0]

def OptGetDescInfo(optValList):
    return optValList[1]

def JoinOptionMeta(optDict):
    arguments = ""
    for opt in optDict:
        optval = optDict[opt]
        if OptHasDefaultVal(optval):
            arguments = arguments + " ["
        arguments = arguments + " " + opt + " "
        if not OptIsOfBoolType(optval):
            arguments = arguments + OptGetOptValue(optval)
        if OptHasDefaultVal(optval):
            arguments = arguments + "] "
    return arguments

def JoinArgDetails(optDict):
    for opt in optDict:
        print "\t", opt, ", ", OptGetDescInfo(optDict[opt])

def Usage(scripts_name=globalExecProgram):
    # print help infomation
    print ""
    print scripts_name + JoinOptionMeta(globalFunctionalOpts) + JoinOptionMeta(globalNonFunctionalOpts)
    JoinArgDetails(globalFunctionalOpts)
    JoinArgDetails(globalNonFunctionalOpts)
    print ""

def ParseOptions():
    length = len(sys.argv) - 1
    options = sys.argv[1:]
    idx = 0
    while idx < length:
        # parse the options
        opt = options[idx]
        if opt in globalFunctionalOpts.keys():
            if OptIsOfBoolType(globalFunctionalOpts[opt]):
                # bool datatype, and set True
                globalRealCmdArgVals[opt] = True
                idx = idx + 1
            else:
                globalRealCmdArgVals[opt] = options[idx+1]
                idx = idx + 2
        elif opt in globalNonFunctionalOpts.keys():
            if OptIsOfBoolType(globalNonFunctionalOpts[opt]):
                # bool datatype, and set True
                globalRealCmdArgVals[opt] = True
                idx = idx + 1
            else:
                globalRealCmdArgVals[opt] = options[idx+1]
                idx = idx + 2
        else:
            # invalid options, report error and print help info
            Usage()
            sys.exit()

    # if item in globalNonFunctionalOpts occurs, don't need to search the globalFunctionalOpts
    hasNonFunctionalOpt = False
    for opt in globalNonFunctionalOpts:
        if opt in globalRealCmdArgVals.keys():
            hasNonFunctionalOpt = True
        else:
            # set the default options values
            globalRealCmdArgVals[opt] = OptGetDefaultVal(globalNonFunctionalOpts[opt])

    if not hasNonFunctionalOpt:
        for opt in globalFunctionalOpts:
            optval = globalFunctionalOpts[opt]
            if opt not in globalRealCmdArgVals.keys():
                if not OptHasDefaultVal(optval): 
                    # if some arguments without default value aren't given by user, report error and exit
                    Usage()
                    sys.exit()
                else:
                    # set the default options values
                    globalRealCmdArgVals[opt] = OptGetDefaultVal(optval)

# markerChar: the marker char for different level contents
#   for the 1-level contents, it's '*'
#   for the 2-level contents, it's '='
# repeats: how many times marker repeats
#
def IsTheTopLevelContentMarker(oneLine, markerChar, repeats=globalTheLeastRepeats):
    # whether this line mark the top level content 
    if (len(oneLine) < repeats):
        return False
    
    for ch in oneLine[0:repeats]:
        if (ch != markerChar):
            return False
    return True

def IsDigit(ch):
    return ch >= '0' and ch <= '9'

def IsChar(ch):
    return (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')

def ConvertToChapterName(title, fileType=globalOutputPostfix):
    # return the file name according to the given title string and file type
    filename = []
    aList = title.split(' ')
    idx = 0

    # handle the chapter seq number, containing digits or '.' and ended with ' '
    if IsDigit(aList[0][0]):
        bList = aList[0].split('.')
        cList = []
        for bItem in bList:
            if 1 == len(bItem):
                cList.append('0' + bItem)
            else:
                cList.append(bItem)
        filename.append('_'.join(cList))
        idx = 1

    # handle the rest
    total = len(aList)
    while idx < total:
        newItem = []
        for ch in aList[idx]:
            if ch == '-':
                newItem.append('_')
            elif IsChar(ch) or IsDigit(ch):
                newItem.append(ch)
        filename.append(''.join(newItem))
        idx = idx + 1

    return '_'.join(filename) + "." + fileType;

def SplitMainBody(nlevelContentFile, markerChar, repeats, outtype):
    outputIsAvaiable = False
    twoLines = [None, None]
    nextpos  = 0
    outfile = None

    infile = open(nlevelContentFile)
    for eachline in infile.readlines():
        prevpos = (nextpos + 1) % 2
        twoLines[nextpos] = eachline

        # need to create file for a new chapter
        if IsTheTopLevelContentMarker(eachline, markerChar, repeats):
            if outputIsAvaiable:
                # close the open file
                outfile.close()
            outfile = open(ConvertToChapterName(twoLines[prevpos][:-1], outtype), 'w')
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

#####################################################################
##    test area
####################################################################

def CheckTestcaseResult(expected, result):
    if expected == result:
        return " OK "
    else:
        return " Failed " + "expected: " + expected + ", result: " + result

def RunAllTestcases():
    print " ", '='*40
    print " IsTheTopLevelContentMarker() test01  ", CheckTestcaseResult( False, IsTheTopLevelContentMarker("*", "*"))
    print " IsTheTopLevelContentMarker() test02  ", CheckTestcaseResult( False, IsTheTopLevelContentMarker("******", "*"))
    print " IsTheTopLevelContentMarker() test03  ", CheckTestcaseResult( True , IsTheTopLevelContentMarker("*******", "*"))
    print " IsTheTopLevelContentMarker() test04  ", CheckTestcaseResult( True , IsTheTopLevelContentMarker("********", "*"))
    print " IsTheTopLevelContentMarker() test05  ", CheckTestcaseResult( False, IsTheTopLevelContentMarker("", "*"))

    print " ", '='*40
    print " IsDigit() test01 ", CheckTestcaseResult( True, IsDigit('0'))
    print " IsDigit() test02 ", CheckTestcaseResult( True, IsDigit('1'))
    print " IsDigit() test03 ", CheckTestcaseResult( True, IsDigit('2'))
    print " IsDigit() test04 ", CheckTestcaseResult( True, IsDigit('3'))
    print " IsDigit() test05 ", CheckTestcaseResult( True, IsDigit('4'))
    print " IsDigit() test06 ", CheckTestcaseResult( True, IsDigit('5'))
    print " IsDigit() test07 ", CheckTestcaseResult( True, IsDigit('6'))
    print " IsDigit() test08 ", CheckTestcaseResult( True, IsDigit('7'))
    print " IsDigit() test09 ", CheckTestcaseResult( True, IsDigit('8'))
    print " IsDigit() test10 ", CheckTestcaseResult( True, IsDigit('9'))
    print " IsDigit() test11 ", CheckTestcaseResult( False, IsDigit("%c" % (int('9')+1)))

    print " ", '='*40
    print " ConvertToChapterName() test01 ", CheckTestcaseResult( "The_Guile_Reference_Manual", ConvertToChapterName("The Guile Reference Manual")[:-3])
    print " ConvertToChapterName() test02 ", CheckTestcaseResult( "Preface", ConvertToChapterName("Preface")[:-3])
    print " ConvertToChapterName() test03 ", CheckTestcaseResult( "01_Introduction", ConvertToChapterName("1 Introduction")[:-3])
    print " ConvertToChapterName() test04 ", CheckTestcaseResult( "02_Hello_Guile", ConvertToChapterName("2 Hello Guile!")[:-3])
    print " ConvertToChapterName() test05 ", CheckTestcaseResult( "03_Hello_Scheme", ConvertToChapterName("3 Hello Scheme!")[:-3])
    print " ConvertToChapterName() test06 ", CheckTestcaseResult( "01_01_Guile_and_Scheme", ConvertToChapterName("1.1 Guile and Scheme")[:-3])
    print " ConvertToChapterName() test07 ", CheckTestcaseResult( "01_06_Obtaining_and_Installing_Guile", ConvertToChapterName("1.6 Obtaining and Installing Guile")[:-3])
    print " ConvertToChapterName() test08 ", CheckTestcaseResult( "07_02_01_POSIX_Interface_Conventions", ConvertToChapterName("7.2.1 POSIX Interface Conventions")[:-3])
    print " ConvertToChapterName() test09 ", CheckTestcaseResult( "07_03_HTTP_the_Web_and_All_That", ConvertToChapterName("7.3 HTTP, the Web, and All That")[:-3])
    print " ConvertToChapterName() test10 ", CheckTestcaseResult( "07_04_The_ice_9_getopt_long_Module", ConvertToChapterName("7.4 The (ice-9 getopt-long) Module")[:-3])
    print " ConvertToChapterName() test11 ", CheckTestcaseResult( "07_10_Formatted_Output", ConvertToChapterName("7.10 Formatted Output")[:-3])
    print " ConvertToChapterName() test12 ", CheckTestcaseResult( "07_16_sxml_match_Pattern_Matching_of_SXML", ConvertToChapterName("7.16 ‘sxml-match’: Pattern Matching of SXML")[:-3])
    print " ConvertToChapterName() test13 ", CheckTestcaseResult( "SXPath_SXML_Query_Language", ConvertToChapterName("SXPath: SXML Query Language")[:-3])
    print " ConvertToChapterName() test14 ", CheckTestcaseResult( "07_02_12_System_Identification", ConvertToChapterName("7.2.12 System Identification")[:-3])

if __name__ == '__main__':
    ParseOptions()
    if globalRealCmdArgVals["-T"]:
        RunAllTestcases();
    elif globalRealCmdArgVals["-h"]:
        Usage()
    else:
        SplitMainBody(globalRealCmdArgVals["-f"],
                globalRealCmdArgVals["-m"],
                globalRealCmdArgVals["-n"],
                globalRealCmdArgVals["-t"])

