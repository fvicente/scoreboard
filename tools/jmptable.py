#!/usr/bin/python
# -*- coding: utf-8 -*-

def main():
    # map lines 50 to 430
    print "jmptable:"
    print "    ; characters to ijmp position"
    line = ""
    pos = 0
    for i in range(10):
        if (i % 10) == 0:
            line += "\n    .byte "
        line += "0x%.2x"%(i * 6, )
        if ((i + 1) % 10) != 0:
            line += ", "
    print line

if __name__ == "__main__":
    main()
