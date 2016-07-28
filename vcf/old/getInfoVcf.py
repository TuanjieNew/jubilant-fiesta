#!/usr/bin/env pyhton 
# fn: getinfo_snp4.py

import os

# in the vcf directory
#li = os.listdic(".")
vcfNames = 'vcfNames.txt' # contains vcf files' names and directory
#os.system('ls *.vcf | cat >' + vcfNames)

def getInfo(file_type):

    if file_type == 'snp':
        out_type = 'indel'
    else:
        out_type = 'snp'

    # initialize dic to create a multi-dimensional hash structure
    dic = {}
    FILE = open(vcfNames,'r')
    lnum = 0
    for line in FILE:
        lnum += 1
        line = line.strip('\n')
        line_ls = line.split('/')
        info_ty = line_ls[8].split('.')[2]
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
                dic[chr_pos] ={str(lnum):'-' }
            VCFFILE.close()
    FILE.close()

    # fill dic with '-'
    for e in dic:
        #print(dic[e])
        for j in range(lnum):
            j += 1
            dic[e][str(j)] = '-'

    # read vcfNames.txt
    FNAME = open(vcfNames, 'r')
    line_num = 0
    for line in FNAME:
        line_num += 1
        line = line.strip('\n')
        line_ls = line.split('/')
        pName = line_ls[8].split('.')[0]
        info_ty = line_ls[8].split('.')[2]

        # pass snp or indel files
        if info_ty == file_type:
            line_num -=1
            continue

        # assign patient names
        dic['#CHROM_POS'][str(line_num)] = pName
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
                info = ';'.join(info_ls[7:12]) + ';' + info_ls[45] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
            elif len(info_ls) == 51:
                info = ';'.join(info_ls[6:11]) + ';' + info_ls[44] + ';' + ln_ls[9].split(':')[5] + ';' + ln_ls[10].split(':')[5]
            #  assign dic
            dic[chr_pos][str(line_num)] = info
        VCFFILE.close()
    dic_sort = sorted(dic.iteritems(), key = lambda asd:asd[0], reverse = False)
    FNAME.close()

    # output results from sorted dic_sort
    OUTFILE = open(out_type+'_info_summary.tsv','w')
    for e in dic_sort:
        info_str = ''
        for i in e[1]:
            info_str = info_str + '\t' + e[1][i]
        OUTFILE.write(e[0]+'\t'+info_str+'\n')
    return out_type+' file summary finished'

for i in ['snp','indel']:
    # information from snp and indel files output to different files
    print(getInfo(i))
