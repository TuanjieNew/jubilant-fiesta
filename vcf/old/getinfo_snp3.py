#!/usr/bin/env pyhton 
# fn: getinfo_snp3.py
# by niutj, 20160726
# Algoritm III

import os

# in the vcf directory
#li = os.listdic(".")
#os.system('ls *.vcf | cat > vcfNames.txt')

def getInfo(fileName, line_num):
    count = 0
    VCFFILE = open(fileName, 'r')
    for ln in VCFFILE:
        count += 1
        ln = ln.strip('\n')
        if ln[0] == '#':
            continue
        ln_ls = ln.split('\t')
        chr_pos = ln_ls[0] + '_' + str(ln_ls[1])
        info_ls = ln_ls[7].split(';')
        if chr_pos == '#CHROM_POS':
            print('hello')

        if len(info_ls) == 52:
            info = ';'.join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
        elif len(info_ls) == 51:
            info = ';'.join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
        #dic[chr_pos][line_num - 1] = info
        return [chr_pos,info]

FILE = open('vcfNames.txt', 'r')
dic = {}
lnum = 0
for line in FILE:
    lnum += 1
FILE.close()

dic_ls = []
for i in range(int(lnum/2)):
    dic_ls.append('---')
FILE = open('vcfNames.txt','r')
for line in FILE:
    line = line.strip('\n')
    line_ls = line.split('/')
    info_ty = line_ls[8].split('.')[2]
    if info_ty == 'snp':
        VCFFILE = open(line, 'r')
        for ln in VCFFILE:
            ln = ln.strip('\n')
            if ln[0:2] == '##':
                continue
            ln_ls = ln.split('\t')
            chr_pos = ln_ls[0] + '_' + str(ln_ls[1])
            dic[chr_pos] = dic_ls
        VCFFILE.close()
FILE.close()

FNAME = open('vcfNames.txt', 'r')
line_num = 0
for line in FNAME:
    line_num += 1
    line = line.strip('\n')
    line_ls = line.split('/')
    pName = line_ls[8].split('.')[0]
    info_ty = line_ls[8].split('.')[2]

    if info_ty == 'indel':
        line_num -=1
        continue
    if line_num < 2:
        #info_ls =  getInfo(line, line_num)
        #dic[info_ls[0]][line_num-1] = info_ls[1]
            
        count = 0
        VCFFILE = open(line, 'r')
        big_ls = []
        for lns in VCFFILE:
            count+=1
        VCFFILE.close()

        VCFFILE = open(line, 'r')
        check = 0
        for ln in VCFFILE:
            check += 1
            #if check == count - 1:
                #break
                #for e in dic:
                    #print(dic[e])
            ln = ln.strip('\n')
            if ln[0] == '#':
                continue
            ln_ls = ln.split('\t')
            chr_pos = ln_ls[0] + '_' + str(ln_ls[1])
            info_ls = ln_ls[7].split(';')
            if chr_pos == '#CHROM_POS':
                print('hello')

            if len(info_ls) == 52:
                info = ';'.join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
            elif len(info_ls) == 51:
                info = ';'.join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
            #small_ls = [chr_pos,info]
            #big_ls.append(small_ls)
            dic[chr_pos][line_num - 1] = info
            #info = ''
            #print(chr_pos)

            #dic_ls = dic.get(chr_pos, default = None)
            #print(dic_ls)
            #dic_ls[line_num-1] = info
            #print(dic_ls)
            #dic[chr_pos] = dic_ls
            #print('a: '+str(count)+':'+str(line_num)+': '+info+str(dic_ls))
            
        #print('b: '+str(count))
'''
d = {}
d_ls = ['---','---','---']
a_ls = ['abc','def','hgi','jkl']
for i in big_ls:
    d[i[0]] = d_ls
d['list'] = ['---', '---', '---']
d['list1'] = ['---', '---', '---']
d['list2'] = ['---', '---', '---']
d['list3'] = ['---', '---', '---']
d['chr1_11846046'] = ['---', '---', '---']
b_ls = ['list', 'list1', 'list2', 'list3']

for i in b_ls:
    d[i][0] = i
#for e in d:
    #print(d[e])
#TFILE = open('test_a.txt','w')
b2 = []
for i in big_ls:
    #b2.append(i)
    #print(len(big_ls))
    #dic[i[0]][1] = i[1]
    #TFILE.write(i+'\n')
    d[i[0]][0] = i[1]
for e in d:
    print(d[e])
    d[e][0] = dic[e][0]
        #VCFFILE.close()
'''

FNAME.close()
for e in dic:
    print(e)
    #print(dic[e])
