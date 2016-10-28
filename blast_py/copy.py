#!/usr/bin/env python
#fn: copy.py
# write specifi contents of alignment_py.py to blast_py.py
INPUT = open('alignment_py.py','r')
OUTPUT = open('blast_py.py','a')
lnum = 0
for line in INPUT:
    lnum += 1
    line = line.strip('\n')
    if lnum > 6 and lnum < 138:
        OUTPUT.write(line+'\n')
