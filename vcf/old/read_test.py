#!/usr/bin/env python
# read_test.py

FILE = open('wanrenInfo_snp.txt', 'r')
DICFILE = open('/haplox/users/huanghuiqiang/project/wanren/VCF/vcf/caobo.final.snp.hg19_multianno.vcf', 'r')
dic = {}
for line in DICFILE:
    line = line.strip('\n')
    ln_ls = line.split('\t')
    if line[0] == '#':
        continue
    chr_pos = ln_ls[0]+'_'+str(ln_ls[1])
    dic[chr_pos] = 'test'


for line in FILE:
    count = 0
    line = line.strip('\n')
    ln_ls = line.split('\t')
    if line[0] == '#':
        continue
    chrom_pos = ln_ls[0]
    if chrom_pos in dic.keys():
        count+=1
    
    
