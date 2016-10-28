#!/usr/bin/env python
#fn: indexref.py

FILE = open('crr5ref.fa','r')
OUTPUT = open('indexref.fa','w')
for line in FILE:
    if line[0] == '>':
        OUTPUT.write(line)
        continue
    #line = line.strip('\n')
    ali_str = '1---'
    for i in range(len(line)):
        if (i+1) % 5 == 0:
            if i >= 9 and i < 99:
                ali_str = ali_str + str(i+1)+'---'
            elif i >= 99:
                ali_str = ali_str + str(i+1)+'--'
            else:
                ali_str = ali_str + str(i+1) + '----'


    OUTPUT.write(ali_str+'\n')
    OUTPUT.write(line)
