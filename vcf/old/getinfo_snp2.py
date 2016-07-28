#!/usr/bin/env python
# fn: getinfo_snp2.py
# for hujj 10kplan, produced by niutj, time: 20160722
# algorithm III

import os
#import numpy as np

# initialize
def posInfo():
    FILE = open("vcfNames.txt", 'r')
    dic = {}
    lnum =0
    for line in FILE:
        lnum += 1
    print(lnum)
    FILE.close()
    dic_ls = []
    for i in range(lnum/2):
        dic_ls.append('---')
    FILE = open('vcfNames.txt','r')
    for line in FILE:
        #print('file: '+str(lnum))
        line = line.strip('\n') #vcf file directory
        line_ls = line.split('/')
        patientName = line_ls[8].split('.')[0]
        info_type = line_ls[8].split('.')[2]
        if info_type == 'indel':
            VCFFILE = open(line,'r')
            for ln in VCFFILE:
                ln = ln.strip('\n')
                if ln[0:2] == '##':
                    continue
                ls = ln.split('\t')
                chr_pos = ls[0] + '_' +str(ls[1])
                dic[chr_pos] = dic_ls
    print('Inilization over')
    FILE.close()
    return dic


dic = posInfo() #initialize file at the first time

OUTFILE = open('dic_test.txt','w')
for e in dic:
    out = '\t'.join(dic[e])
    out = e+'\t'+out
    OUTFILE.write(out+'\n')
OUTFILE.close()
#print(len(dic['#CHROM_POS']))

FNAME = open("vcfNames_2.txt", "r")
OUTFILE = open('info_check.txt','w')
lnum = 0
for line in FNAME:
    lnum +=1
    line = line.strip('\n') #vcf file directory
    line_ls = line.split('/')
    pName = line_ls[8].split('.')[0]
    info_ty = line_ls[8].split('.')[2]

    if info_ty == 'snp':
        lnum -= 1
        continue
        #getInfo_snp(line, patientName, info_type) # call function getInfo
    dic['#CHROM_POS'][lnum - 1] = pName
    #print(dic['#CHROM_POS'])
    print('File number: '+str(lnum))
    VCFFILE = open(line,'r')
    count = 0
    for ln in VCFFILE:
        ln = ln.strip('\n')
        if ln[0] == '#':
            continue
        ln_ls = ln.split('\t')
        chr_pos = ln_ls[0]+'_'+str(ln_ls[1])
        info_ls = ln_ls[7].split(';')
        # INFO length varies from 51 to 52
        if len(info_ls) == 52:
            info = ";".join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
        elif len(info_ls) == 51:
            info = ";".join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
        dic[chr_pos][lnum - 1] = info
        #print(dic['#CHROM_POS'])
    #print(info)
    #print(dic['#CHROM_POS'])

    VCFFILE.close()
FNAME.close()
OUTFILE.close()

for e in dic:
    print(e)
    print(dic[e])
    dic[e][0] = dic[e][0]

OUTFILE = open('indel_2.txt','w')
dic_sort = sorted(dic.iteritems(), key = lambda asd:asd[0], reverse = False)
for e in dic_sort:
    #print(e[1])
    out = '\t'.join(e[1])
    out = e[0]+'\t'+out
    OUTFILE.write(out+'\n')
OUTFILE.close()
