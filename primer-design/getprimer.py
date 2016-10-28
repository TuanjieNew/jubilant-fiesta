#!/usr/bin/env python
#fn getprimer.py

import sys, getopt, os

def usage():
    print('\nUsage: python -i input_file \n')
opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:")
if len(opts) == 0:
    usage()
    sys.exit()
rang = 300
for op, value in opts:
    if op == "-i":
        query_file = value
    elif op == "-l":
        rang = int(value)
    else:
        usage()
        sys.exit()
if not os.path.exists(query_file):
        print("The path [{}] not exit!".format(query_file))
        sys.exit()

def getrever(seq):
    rseq = ''
    for i in seq:
        if i =='A':
            rseq = rseq + 'T'
        elif i == 'T':
            rseq = rseq + 'A'
        elif i == 'G':
            rseq = rseq + 'C'
        elif i == 'C':
            rseq = rseq + 'G'
    return rseq[::-1]
fn = query_file.split('.')[0]
FILE = open(query_file,'r')
HG19 = open('/1/public_resources/hg19/hg19.fa','r')
OUTPUT = open(fn+'.out.txt', 'w')
gseq = ''
chrom = ''
pos = 0
count = 0
for line in FILE:
    count += 1
    line = line.strip('\n')
    ls = line.split('\t')
    #print(ls)
    gseq = ls[0]
    chrom = ls[4].split(':')[0][3:]
    pos = int(ls[4].split(':')[1][1:])
    sign = ls[4].split(':')[1][0]
    CHROM = open('/1/niutj/hg19_fa/'+chrom+'.fa','r')
    for line in CHROM:
        line = line.strip('\n')
        if sign == '+':
            print(line[pos+1:pos+24])
            OUTPUT.write(str(count)+':\t'+gseq+'\n')
            OUTPUT.write(line[pos-(rang/2 - 10): pos+(rang/2 - 10)]+'\n') 
        elif sign == '-':
            #print(line[pos+1:pos+21])
            OUTPUT.write(str(count)+':\t'+gseq+'\t'+line[pos+4:pos+27]+'\n')
            OUTPUT.write(line[pos-(rang/2 - 10): pos+(rang/2 - 10)]+'\n') 
            print(getrever(line[pos+4:pos+27]))
        print('len: '+str(len(line[pos-140:pos+160])))
print('The output file: '+fn+'.out.txt')
OUTPUT.close()
FILE.close()
HG19.close()
