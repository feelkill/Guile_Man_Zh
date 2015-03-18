#!/usr/bin/python
#
# comments the continual lines with '<!-- -->' for a file. '<!--' will hold a single line while '-->' another single line.
#

import re
import sys

def help():
    print " comment_continual_lines.py [ -h ] [ -f onefile ] "
    print "   -h, print this help info "
    print "   -f, the file to comments with \"<!-- -->\" "
    print ""

def comments(onefile):
    # main body of comments
    tmp = onefile + ".tmp"
    infile = open(onefile)
    outfile = open(tmp, 'w')

    commentStr1 = "<!--\n"
    commentStr2 = "-->\n"
    nCommentSeg = 0
    nowCommenting = False

    for oneLine in infile.readlines():
        if not re.search(r'^\s+$', oneLine):
            if not nowCommenting:
                # start to comment a new segment
                nowCommenting = True
                nCommentSeg = nCommentSeg + 1
                outfile.write(commentStr1)
                outfile.write(oneLine)
            else:
                # continue until a blank line occurs
                outfile.write(oneLine)
                continue
        elif nowCommenting:
            # finish commenting this segment
            nowCommenting = False
            outfile.write(commentStr2)
            # keep this blank line staying there
            outfile.write(oneLine)
        else:
            # just keep these lines
            outfile.write(oneLine)

    if nCommentSeg > 0 and nowCommenting:
        outfile.write(commentStr2)
    infile.close()
    outfile.close()

def parse():
    length = len(sys.argv) - 1
    options = sys.argv[1:]
    idx = 0

    while idx < length:
        if options[idx] == '-f':
            comments(options[idx+1])
        else:
            help()
        sys.exit()

if __name__ == "__main__":
    parse()
