#!/usr/bin/env python
# fn: getinfo.py
# for hujj 10kplan, produced by niutj, time: 20160721

import os

def getInfo(fileName, pName, info_ty):
    #FILE = open('vcfNames.txt','r')
    VCFFILE = open(fileName,'r') # open imported vcf file
    INFOFILE = open('info_'+info_ty+'.txt', 'r')# open existed info file
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
        os.rename("infotemp.txt","info_"+info_ty+".txt")
            

        #OUTFILE.write(info+'\n')
def iniInfo(fileName, pName, info_ty):
    OUTFILE = open('info_'+info_ty+'2.txt','w')
    OUTFILE.write('#CHR_POS\t'+pName+'_'+info_ty+'\n')
    #line = fileName
    FILE = open(fileName, 'r')
    for line in FILE:
        line = line.strip('\n')
        if line[0] == '#':
            continue
        ls = line.split('\t')
        #print(len(ls))
        #print(info)
        chr_pos = ls[0]+'_'+str(ls[1])
        info_ls = ls[7].split(';')
        #print(len(info_ls))
        if len(info_ls) == 52:
            info = ";".join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ls[9].split(':')[5] + ';' + ls[10].split(':')[5]
        elif len(info_ls) == 51:
            info = ";".join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ls[9].split(':')[5] + ';' + ls[10].split(':')[5]
        OUTFILE.write(chr_pos + '\t' + info+'\n')
        #getInfo(line, patientName)

iniInfo('/haplox/users/huanghuiqiang/project/wanren/VCF/vcf/caobo.final.indel.hg19_multianno.vcf','caobo','indel')
#iniInfo('/haplox/users/huanghuiqiang/project/wanren/VCF/vcf/caobo.final.snp.hg19_multianno.vcf','caobo','snp')
FNAME = open("vcfNames.txt", "r")
#file_name = ''
INFOFILE = open('info_'+'indel'+'2.txt', 'r')# open existed info file
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
        ln_ls.append('caobo')
        #INFOTEMP.write('\t'.join(ln_ls) + '\n')
        #continue
    else:
        ln_ls.append('---')
    #print(ln_ls)
    len_ln = len(ln_ls)
    info_dic[ln_ls[0]] = ln_ls
lnum = 0
for line in FNAME:
    lnum +=1
    line = line.strip('\n') #vcf file directory
    line_ls = line.split('/')
    patientName = line_ls[8].split('.')[0]
    info_type = line_ls[8].split('.')[2]
    print('File number: '+str(lnum))
    if info_type == 'snp':
        continue
    fileName = line
    #initialize file at the first time
    #if lnum ==1:
    #    iniInfo(line, patientName, info_type)
    #if info_type == 'indel':
        #getInfo(line, patientName, info_type) # call function getInfo
    VCFFILE = open(fileName,'r') # open imported vcf file
    INFOTEMP = open('infotemp'+info_type+'2.txt', 'w') # write updated lines to infotemp.txt


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
    VCFFILE.close()
    print('accumulat over')
dic_sort = sorted(info_dic.iteritems(), key = lambda asd:asd[0], reverse = False)

print('start sort\n')
for e in dic_sort:
    #print(e)
    out = '\t'.join(e[1])
    #print(out)
    INFOTEMP.write(out+'\n')
INFOFILE.close()


'''
li = os.listdir(".")
if "infotemp.txt" in li:
        os.remove("infotemp.txt")
    #print(patientName)
'''
