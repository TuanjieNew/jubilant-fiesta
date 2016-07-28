#!/usr/bin/env python
# fn: getinfo_snp.py
# for hujj 10kplan, produced by niutj, time: 20160722
# Algorithm II

import os

def getInfo(fileName, pName, info_ty):
    VCFFILE = open(fileName,'r') # open imported vcf file
    INFOFILE = open('wanrenInfo_'+info_ty+'.txt', 'r')# open existed info file
    INFOTEMP = open('infotemp.txt', 'w') # write updated lines to infotemp.txt

    info_dic = {}
    for ln in INFOFILE:
        ln = ln.strip('\n')
        ln_ls = ln.split('\t')
        #print(ln_ls)
        '''
        if ln[0] == '#':
            if info_ty == "snp":
                ln_ls.append(pName+'_snp')
                #print('snp')
            elif info_ty == "indel":
                ln_ls.append(pName+'_indel')
            INFOTEMP.write('\t'.join(ln_ls) + '\n')
            continue
        '''
        if ln[0] == '#':
            ln_ls.append(pName)
            INFOTEMP.write('\t'.join(ln_ls) + '\n')
            continue
        ln_ls.append('---')
        #print(ln_ls)
        len_ln = len(ln_ls)
        info_dic[ln_ls[0]] = ln_ls

    print('dic over')
    for line in VCFFILE:
        line = line.strip('\n')
        if line[0] == '#':
            continue
        ls = line.split('\t')
        chrom = ls[0]
        pos = int(ls[1])
        chr_pos = ls[0]+'_'+str(ls[1])
        info_ls = ls[7].split(';')
        #print(len(info_ls))
        # INFO length varies from 51 to 52
        if len(info_ls) == 52:
            info = ";".join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ls[9].split(':')[5] + ';' + ls[10].split(':')[5]
        elif len(info_ls) == 51:
            info = ";".join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ls[9].split(':')[5] + ';' + ls[10].split(':')[5]
        if chr_pos in info_dic.keys():
            info_dic[chr_pos][-1] = info
        else:
            new_ls = [chr_pos] 
            for i in range(len(ln_ls)-2):
                new_ls.append( '---')
            new_ls.append(info)
            info_dic[chr_pos] = new_ls
    # sort key
    print('accumulat over')
    dic_sort = sorted(info_dic.iteritems(), key = lambda asd:asd[0], reverse = False)
    print('start sort\n')
    for e in dic_sort:
        #print(e)
        out = '\t'.join(e[1])
        #print(out)
        INFOTEMP.write(out+'\n')
    VCFFILE.close()
    INFOFILE.close()
    INFOTEMP.close()

    li = os.listdir(".")
    if "infotemp.txt" in li:
        os.rename("infotemp.txt","wanrenInfo_"+info_ty+".txt")

# for snp
def getInfo_snp(fileName, pName, info_ty):           
    VCFFILE = open(fileName, 'r')

    dic = {}
    for line in VCFFILE:
        line = line.strip('\n')
        if line[0] == '#':
            continue
        ls = line.split('\t')
        chrom = ls[0]
        pos = int(ls[1])
        chr_pos = str(ls[0])+'_'+str(ls[1])
        #chr_pos = ls[0]+'_'+str(ls[1])
        info_ls = ls[7].split(';')
        #print(len(info_ls))
        # INFO length varies from 51 to 52
        if len(info_ls) == 52:
            info = ";".join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ls[9].split(':')[5] + ';' + ls[10].split(':')[5]
        elif len(info_ls) == 51:
            info = ";".join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ls[9].split(':')[5] + ';' + ls[10].split(':')[5]
        dic[chr_pos] = info

    print(len(dic))
    INFOFILE = open("wanrenInfo_"+info_ty+".txt","r")
    INFOTEMP = open("infotemp_"+info_ty+".txt", "w")
    lnum = 0
    #check = 0
    count = 0
    for ln in INFOFILE:
        lnum +=1
        ln = ln.strip('\n')
        ln_ls = ln.split('\t')
        if ln[0] == '#':
            ln_ls[-1]=pName
            #print('name: ')
            #print(ln_ls)
            INFOTEMP.write('\t'.join(ln_ls) + '\n')
            continue
        #info_chr = ln_ls[0].split('_')[0]
        #info_pos = int(ln_ls[0].split('_')[1])
        info_chr_pos = ln_ls[0] 
        if info_chr_pos in dic.keys():
            count +=1
            #print(info_chr_pos)
            ln_ls[-1] = dic[info_chr_pos]
            #INFOTEMP.write('\t'.join(ln_ls) + '\n')
            INFOTEMP.write(ln+'\t'+info+'\n')
        else:
            #INFOTEMP.write('\t'.join(ln_ls) + '\n')
            INFOTEMP.write(ln+'\t'+'---'+'\n')
        #print(lnum)
        '''
        if check == 0:
            if chrom == info_chr:
                if pos == info_pos:
                    check = 1
                    #print('hello')
                    #print('lnum: '+str(lnum))
                    ln_ls[-1] = info
                    #print(ln_ls)
                    INFOTEMP.write('\t'.join(ln_ls) + '\n')
                else:
                    INFOTEMP.write('\t'.join(ln_ls) + '\n')
            else:
                INFOTEMP.write('\t'.join(ln_ls) + '\n')
        else:
            INFOTEMP.write('\t'.join(ln_ls) + '\n')
        '''
            

    print('count: ' +str(count))
    INFOFILE.close()
    INFOTEMP.close()
    li = os.listdir(".")
    if "infotemp_"+info_ty+".txt" in li:
        os.rename("infotemp_"+info_ty+".txt","wanrenInfo_"+info_ty+".txt")
    VCFFILE.close()
    '''
    AFILE = open('wanrenInfo_' + info_ty + '.txt', 'r')
    TFILE = open('infotemp_snp.txt','w')
    for line in AFILE:
        line = line.strip('\n')
        line += '\t---\n'
        TFILE.write(line)
    AFILE.close()
    TFILE.close()
    li = os.listdir(".")
    if "infotemp_snp.txt" in li:
        os.rename("infotemp_snp.txt","wanrenInfo_"+info_ty+".txt")
    '''

# initialize
def posInfo():
    FILE = open("vcfNames.txt", 'r')
    INIFILE = open("wanrenInfo_indel.txt",'w')
    INIFILE.write("#CHR_PSO\n")
    #row_ls = []
    dic = {}
    lnum =0
    for line in FILE:
        lnum += 1
        print('file: '+str(lnum))
        line = line.strip('\n') #vcf file directory
        line_ls = line.split('/')
        patientName = line_ls[8].split('.')[0]
        info_type = line_ls[8].split('.')[2]
        if info_type == 'snp':
            VCFFILE = open(line,'r')
            for ln in VCFFILE:
                ln = ln.strip('\n')
                if ln[0] == '#':
                    continue
                ls = ln.split('\t')
                chr_pos = ls[0] + '_' +str(ls[1])
                dic[chr_pos] = ''
    sort_ls = sorted(dic.iteritems(), key = lambda asd:asd[0], reverse = False)
    #print(len(sort_ls))
    for e in sort_ls:
        INIFILE.write(e[0]+'\n')
    FILE.close()
    INIFILE.close()

li = os.listdir(".")
if "infotemp_indel.txt" in li:
        os.remove("infotemp_indel.txt")
    #print(patientName)

posInfo() #initialize file at the first time
FNAME = open("vcfNames.txt", "r")
lnum = 0
for line in FNAME:
    lnum +=1
    line = line.strip('\n') #vcf file directory
    line_ls = line.split('/')
    patientName = line_ls[8].split('.')[0]
    info_type = line_ls[8].split('.')[2]
    '''
    #initialize file at the first time
    if lnum ==1:
        iniInfo(line, patientName, info_type)
        continue
    '''
    print('File number: '+str(lnum))
    if info_type == 'indel':
        getInfo_snp(line, patientName, info_type) # call function getInfo

