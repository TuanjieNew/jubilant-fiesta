#!/usr/bin/env python
# fn: blast_py.py

import gzip

w_len = 13 # words length

#get complementary query sequence
def getrev(query):
    rquery = ''
    for i in query:
        if i == 'A':
            rquery += 'T'
        elif i == 'T':
            rquery += 'A'
        elif i == 'G':
            rquery += 'C'
        elif i == 'C':
            rquery += 'G'
        elif i == 'N':
            rquery += 'N'
    print('reverse query: '+rquery)
    return rquery[::1]

# get reference library
def getlib(ref):
    lib = {} #words library dic
    ref_len = len(ref)
    i = ref_len
    j = 0
    
    while i >= w_len:
        word = ref[j:j+w_len]
        if word in lib.keys():
            print(word)
            print('repetive')
            lib[word] += ';'+str(j)
        else:
            lib[word] = str(j)
        j += 1
        i -= 1
    print('j: '+str(j))
    print('lib len: '+str(len(lib)))
    return lib

# blast to find query sequence location in ref
def blast(query, lib):
    que_len = len(query)
    loc_lib = {}
    ii = que_len
    jj = 0
    while ii >= w_len:
        q_word = query[jj:jj+w_len]
        if q_word in lib.keys():
            loc = int(lib[q_word]) - jj
            #print(jj)
            #print(loc)
            if loc in loc_lib:
                loc_lib[loc] += 1
            else:
                loc_lib[loc] = 1
        jj += 1
        ii -= 1
    loc_len = 0
    print(len(loc_lib))
    print(loc_lib)
    if len(loc_lib) == 0:
        return 0
    for e in loc_lib:
        #print('loc: '+str(loc_lib[e]))
        if int(loc_lib[e]) > 0.6 * jj:
            return int(e+1)
        else:
            loc_len += 1
            if loc_len == len(loc_lib):
                return 0

        

def alignment(loc, seq1, seq2):

    len1 = len(seq1)
    len2 = len(seq2)

    match=6;
    mismatch=-1;
    gap=-8
    #i=0
    #j=0
    matrix=[([0] *(len1+1)) for i in range(len2+1)]
    matrix[0][0]=0
    for j in range(len(seq1)):
        j+=1
        matrix[0][j]=0
        
    for i in range(len(seq2)):
        i=i+1
        matrix[i][0]=0
    max_i=0
    max_j=0
    max_score=0
    #i=0
    #j=0

    for i in range(len(seq2)):
        i=i+1
        for j in range(len(seq1)):
            j=j+1
            #print(j)
            #print(i)
            #print(matrix[i])
            diag_score=0
            left_score=0
            up_score=0

            letter1=seq1[j-1:j]
            letter2=seq2[i-1:i]

            if letter1==letter2:
                diag_score=matrix[i-1][j-1]+match
            else:
                diag_score=matrix[i-1][j-1]+mismatch
            up_score=matrix[i-1][j]+gap
            left_score=matrix[i][j-1]+gap
            #print('diag: '+str(diag_score))
            #print('up: '+str(up_score))
            #print('left: '+str(left_score))
            if diag_score <=0 and up_score<=0 and left_score<=0:
                matrix[i][j]=0
                continue
            #choose the highest socre
            if diag_score >=up_score:
                if diag_score>=left_score:
                    matrix[i][j]=diag_score
                else:
                    matrix[i][j]=left_score

            else:
                if left_score>=up_score:
                    matrix[i][j]=left_score
                else:
                    matrix[i][j]=up_score

            #set maximum score
            if matrix[i][j]>max_score:
                max_i=i
                max_j=j
                max_score=matrix[i][j]
    #trace back

    #print('max_j: '+str(max_j))
    #print('max_i: '+str(max_i))
    ref_restore = ''
    align1=''
    align2=''
    #j=max_j
    #i=max_i
    j=len1
    i=len2
    equal_num=0

    while 1:
        if matrix[i][j]==0:
            break
        if matrix[i-1][j-1]>=matrix[i-1][j]:
            if matrix[i-1][j-1]>=matrix[i][j-1]:

                ref_restore=ref_restore+seq1[j-1:j]
                align1=align1+seq1[j-1:j]
                align2=align2+seq2[i-1:i]
                j-=1
                i-=1
            else:
                ref_restore=ref_restore+seq1[j-1:j]
                align1=align1+seq1[j-1:j]
                align2=align2+'-'
                j-=1
        else:
            if matrix[i-1][j]>=matrix[i][j-1]:
                align1=align1+'-'
                align2=align2+seq2[i-1:i]
                i-=1
            else:
                ref_restore=ref_restore+seq1[j-1:j]
                align1=align1+seq1[j-1:j]
                align2=align2+'-'
                j-=1
    ref_restore = ref_restore[::-1]
    align1=align1[::-1]
    align2=align2[::-1]
    #number scale
    ali_str = '1---'
    for i in range(len(align1)):
        if (i+1) % 5 ==0:
            if i >= 9 and i < 99:
                ali_str = ali_str +str(i+1)+'---'
            elif i >= 99:
                ali_str = ali_str + str(i+1)+'--'
            else: 
                ali_str = ali_str + str(i+1)+'----'
    #print('\n')
    '''
    print('\033[1;31;40m'+'loca: '+'\033[0m'+ali_str[:len(align1)])
    print('\033[1;31;40m'+'seq1: '+'\033[0m'+align1)
    print('\033[1;31;40m'+'seq2: '+'\033[0m'+align2)
    '''
    t_loc = loc-len(ref_restore)+len1
    #if t_loc < 605 and t_loc + len(seq2) > 586:
    print('pos : '+ali_str[:len(align1)])
    #print('ref_: '+ref_restore)
    print('seq1: '+align1)
    print('seq2: '+align2)
    print('true loc: '+str(t_loc))
    c=0
    equ_num=0
    non_eq=0
    for c in range(len(align1)):
        if align1[c]==align2[c]:
            equ_num+=1
        '''
        else:
            non_eq+=1
        if non_eq>5:
            return non_eq+equ_num
        '''
    return equ_num
#def test(ref):

rFILE = open('crr5ref.fa','r')
#qFILE = gzip.open('/1/niutj/crispr_data/human_CCR5_20160901/4_S4_L001_R1_001.fastq.gz','rb')
qFILE = open('test.fastq','r')
for line in rFILE:
    if line[0] == '>':
        continue
    line = line.strip('\n')
    ref = line
    lib = getlib(line)

lnum = 0
for line in qFILE:
    lnum += 1
    if lnum % 4 == 2:
        #print(line)
        if lnum > 1548:
            break
        line = line.strip('\n')
        print('line number: '+str(lnum))
        location = blast(line, lib)
        print('location: '+str(location))
        print('query length: '+str(len(line)))
        print('query: '+line)
        if location == 0:
            location == blast(getrev(line), lib)
        if location == 0:
            continue
        print('ref: '+ref[location-1:location-1+len(line)])
        alignment(location, ref[location-1:location-1+len(line)], line)
