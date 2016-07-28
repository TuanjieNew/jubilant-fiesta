#!/usr/bin/env python
# fn: getVenn.py
# for hujj, produced by niutj, start: 20160721
# plot venn by matplotlib. 
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_unweighted

FILE = open('geneVenn.txt','r')
OUTFILE = open('statResults.txt','w')
A = 0
D = 0
N = 0
AD = 0
AN = 0
DN = 0
ADN = 0

lnum = 0
for line in FILE:
    ln_ls = []
    lnum += 1
    line = line.strip('\n')
    sln_ls = line.split('\t')[1:]
    if lnum == 1:
        continue
    for i in sln_ls:
        ln_ls.append(float(i))

    #print(ln_ls)
    #if lnum < 3:
        #print(ln_ls)

    mean_a = sum((ln_ls[0:7]))/7.0
    mean_d = sum(ln_ls[7:12])/5.0
    mean_n = sum(ln_ls[12:])/5.0
       
    if mean_a > 0:
        if mean_d > 0:
            if mean_n > 0:
                ADN +=1
            else:
                AD +=1
        else:
            if mean_n > 0:
                AN +=1
            else:
                A +=1
    else:
        if mean_d > 0:
            if mean_n > 0:
                DN +=1
            else:
                D +=1
        else:
            if mean_n > 0:
                N +=1
    
    '''
    if lnum<3:
        print(lnum)
        print(ln_ls)
        print(mean_a, mean_d, mean_n)
    '''


total = [A,D,AD, N, AN, DN, ADN]
print('A: '+str(A) + ';\nD: '+str(D)+';\nAD: '+str(AD) + ';\nN: '+str(N)+';\nAN: '+str(AN)+';\nDN: '+str(DN)+';\nADN: '+str(ADN))
OUTFILE.write('A: '+str(A)+'\n'+'D: '+str(D)+'\nN: '+str(N)+'\nAD: '+str(AD)+'\nAN: '+str(AN)+'\nDN: '+str(DN)+'\nADN: '+str(ADN)+'\n')

print('Sum: '+str(sum(total)))
print('Over!!!')
plt.figure(figsize = (15, 15))
v = venn3_unweighted(subsets = ( A, D, AD, N, AN, DN, ADN), set_labels = ('A', 'D', 'N'))

plt.savefig('venn_gene.jpg')

