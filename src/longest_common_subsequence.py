def Memoize (memo, seq1, seq2, pos1, pos2, lcs):
    if seq1 in memo:
        memo[seq1][seq2] = (pos1, pos2, lcs)
    else:
        memo[seq1] = { seq2: (pos1, pos2, lcs) }

    if seq2 in memo:
        memo[seq2][seq1] = (pos2, pos1, lcs)
    else:
        memo[seq2] = { seq1: (pos2, pos1, lcs) }

def LCS(seq1, seq2, memo = {}):
    if seq1 in memo and seq2 in memo[seq1]:
        r = memo[seq1][seq2]
        return r [0], r[1], r [2]

    l1 = len(seq1)
    l2 = len(seq2)

    if l1 == 1:
        if seq1 in seq2:
            lcs  = seq1
            pos1 = 0
            pos2 = seq2.index(seq1)
            #print ("1. Returning LCS '{}' for '{}' & '{}'. pos1 = {}, pos2 = {}".format(lcs, seq1, seq2, pos1, pos2))
            Memoize (memo, seq1, seq2, pos1, pos2, lcs)
            return pos1, pos2, lcs
        else:
            #print ("2. Returning LCS '{}' for '{}' & '{}'".format('', seq1, seq2))
            Memoize (memo, seq1, seq2, -1, -1, '')
            return -1, -1, ''

    if l2 == 1:
        if seq2 in seq1:
            lcs  = seq2
            pos1 = seq1.index(seq2)
            pos2 = 0
            #print ("3. Returning LCS '{}' for '{}' & '{}'. pos1 = {}, pos2 = {}".format(lcs, seq1, seq2, pos1, pos2))
            Memoize (memo, seq1, seq2, pos1, pos2, lcs)
            return pos1, pos2, lcs
        else:
            #print ("4. Returning LCS '{}' for '{}' & '{}'".format('', seq1, seq2))
            Memoize (memo, seq1, seq2, -1, -1, '')
            return -1, -1, ''

    c = seq1[0]
    pos11, pos12, lcs1 = LCS(seq1[1:], seq2, memo)
    #print ("lcs1 is '{}' for '{}' & '{}'".format (lcs1, seq1, seq2))
    if pos11 >= 0:
        if c in seq2[:pos12]:
            lcs1 = c + lcs1
            pos11 = 0
            pos12 = seq2[:pos12].index(c)
        else:
            pos11 = pos11 + 1
    else:
        if c in seq2:
            lcs1  = c
            pos11 = 0
            pos12 = seq2.index(c)
    #print ("New lcs1 is '{}' for '{}' & '{}'".format (lcs1, seq1, seq2))

    c = seq2[0]
    pos21, pos22, lcs2 = LCS(seq1, seq2[1:], memo)
    #print ("lcs2 is '{}' for '{}' & '{}'. pos21 = {}, pos22 = {}".format (lcs2, seq1, seq2, pos21, pos22))
    if pos21 >= 0:
        if c in seq1[:pos21]:
            lcs2 = c + lcs2
            pos21 = seq1[:pos21].index(c)
            pos22 = 0
        else:
            pos22 = pos22 + 1
    else:
        if c in seq1:
            lcs2 = c
            pos21 = seq1.index(c)
            pos22 = 0
    #print ("New lcs2 is '{}' for '{}' & '{}'. pos21 = {}, pos22 = {}".format (lcs2, seq1, seq2, pos21, pos22))

    if len(lcs1) >= len(lcs2):
        #print ("5. Returning LCS '{}' for '{}' & '{}'. pos1 = {}, pos2 = {}".format(lcs1, seq1, seq2, pos11, pos12))
        Memoize (memo, seq1, seq2, pos11, pos12, lcs1)
        return pos11, pos12, lcs1
    else:
        #print ("6. Returning LCS '{}' for '{}' & '{}'. pos1 = {}, pos2 = {}".format(lcs2, seq1, seq2, pos21, pos22))
        Memoize (memo, seq1, seq2, pos21, pos22, lcs2)
        return pos21, pos22, lcs2

def solution(seq1, seq2):
    pos1, pos2, lcs = LCS (seq1, seq2)
    return lcs

if __name__ == "__main__":
    lcs = solution('ABC','ABC')
    if lcs == 'ABC':
        print ("LCS('ABC', 'ABC') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('ABC', 'ABC') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('ABCBDAB','BDCABA')
    if lcs == 'BDAB':
        print ("LCS('ABCBDAB', 'BDCABA') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('ABCBDAB', 'BDCABA') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('XMJYAUZ','MZJAWXU')
    if lcs == 'MJAU':
        print ("LCS('XMJYAUZ', 'MZJAWXU') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('XMJYAUZ', 'MZJAWXU') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('ABCDGH','AEDFHR')
    if lcs == 'ADH':
        print ("LCS('ABCDGH', 'AEDFHR') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('ABCDGH', 'AEDFHR') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('AGGTAB','AGGTAB')
    if lcs == 'AGGTAB':
        print ("LCS('AGGTAB', 'AGGTAB') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('AGGTAB', 'AGGTAB') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('ABCDEFG','XZACKDFWGH')
    if lcs == 'ACDFG':
        print ("LCS('ABCDEFG', 'XZACKDFWGH') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('ABCDEFG', 'XZACKDFWGH') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('CHIMPANZEE','HUMAN')
    if lcs == 'HMAN':
        print ("LCS('CHIMPANZEE', 'HUMAN') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('CHIMPANZEE', 'HUMAN') = {} - DID NOT MATCH".format(lcs))

    lcs = solution('ACCGGTCGAGTGCGCGGAAGCCGGCCGAA','GTCGTTCGGAATGCCGTTGCTCTGTAAA')
    if lcs == 'GTCGTCGGAAGCCGGCCGAA':
        print ("LCS('ACCGGTCGAGTGCGCGGAAGCCGGCCGAA', 'GTCGTTCGGAATGCCGTTGCTCTGTAAA') = {} - MATCHED".format(lcs))
    else:
        print ("LCS('ACCGGTCGAGTGCGCGGAAGCCGGCCGAA', 'GTCGTTCGGAATGCCGTTGCTCTGTAAA') = {} - DID NOT MATCH".format(lcs))
