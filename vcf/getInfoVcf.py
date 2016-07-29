#!/usr/bin/env pyhton 
# File name: getInfoVcf.py
# For hujj, produce by niutj, 20170728
# First put the names of all vcf files to vcfNames.txt.
# snp files and indel files are process separately.
# The first column of output files is chr_pos information. The next columns consist of specific information and corresponding patient's name.
# Usagei (in command line): python getInfoVcf.py 

import os

# in the vcf directory
#vcfNames = 'vcfNames.txt' # contains vcf files' names and directory
#li = os.listdic(".")
#if vcfNames in not in li:
    
## os.system command put all *.vcf into vcfNames.txt 
os.system('ls ./sample/*.vcf | cat > vcfNames.txt')
os.system('mv vcfNames.txt output')
path = os.getcwd()


def getInfo(file_type):

    if file_type == 'snp':
        out_type = 'indel'
    else:
        out_type = 'snp'

    # initialize dic to create a multi-dimensional hash structure
    dic = {}
    FILE = open('./output/vcfNames.txt','r')
    lnum = 0
    for line in FILE:
        lnum += 1
        line = line.strip('\n')
        line_ls = line.split('/')
        info_ty = line_ls[-1].split('.')[2]
        #info_ty = line.split('.')[2]#line_ls[8].split('.')[2]
        if info_ty == file_type:
            lnum -= 1
        if info_ty == out_type:
            VCFFILE = open(line, 'r')
            for ln in VCFFILE:
                ln = ln.strip('\n')
                if ln[0:2] == '##':
                    continue
                ln_ls = ln.split('\t')
                chr_pos = ln_ls[0] + '_' + str(ln_ls[1])
                dic[chr_pos] ={lnum:'-' }
            VCFFILE.close()
    FILE.close()

    # fill dic with '-'
    for e in dic:
        #print(dic[e])
        for j in range(lnum + 1):
            #j += 1
            dic[e][j] = '-'

    # read vcfNames.txt
    FNAME = open('./output/vcfNames.txt', 'r')
    dic['#CHROM_POS'][0] = 'INFO'
    line_num = 0
    for line in FNAME:
        line_num += 1
        line = line.strip('\n')
        line_ls = line.split('/')
        pName = line_ls[-1].split('.')[0]
        info_ty = line_ls[-1].split('.')[2]
        #pName = line.split('.')[0]#line_ls[8].split('.')[0]
        #info_ty = line.split('.')[2]#line_ls[8].split('.')[2]

        # pass snp or indel files
        if info_ty == file_type:
            line_num -=1
            continue

        # assign patient names
        dic['#CHROM_POS'][line_num] = pName
        # collect information from vcf files
        VCFFILE = open(line, 'r')
        for ln in VCFFILE:
            ln = ln.strip('\n')
            if ln[0] == '#':
                continue
            ln_ls = ln.split('\t')
            chr_pos = ln_ls[0] + '_' + str(ln_ls[1])
            info_ls = ln_ls[7].split(';')
            # infomation length in each line is not equal to others
            if len(info_ls) == 52:
                INFO = ';'.join(info_ls[7:12]) + ';' + info_ls[45] 
                info = ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
            elif len(info_ls) == 51:
                INFO = ';'.join(info_ls[6:11]) + ';' + info_ls[44] 
                info = ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
            #  assign dic
            dic[chr_pos][0] = INFO
            dic[chr_pos][line_num] = info
        VCFFILE.close()
    # sort dic according to chr_pos
    dic_sort = sorted(dic.iteritems(), key = lambda asd:asd[0], reverse = False)
    FNAME.close()

    # output results from sorted dic_sort
    OUTFILE = open('./output/'+out_type+'_info_summary.tsv','w')
    for e in dic_sort:
        info_str = ''
        info_sort = sorted(e[1].iteritems(), key = lambda asd:asd[0], reverse = False)
        for i in info_sort:
            info_str = info_str + '\t' + i[1]
        OUTFILE.write(e[0]+'\t'+info_str+'\n')
    return out_type+' file summary finished'

for i in ['snp','indel']:
    # information from snp and indel files output to different files
    print(getInfo(i))
