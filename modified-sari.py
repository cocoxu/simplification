from __future__ import division
from collections import Counter
import glob
import numpy as np
from argparse import ArgumentParser


"""
Based on code by Wei Xu
#https://github.com/cocoxu/simplification

This a slightly improved version of SARI implementation to exclude the spurious ngrams while 
calculating the F1 score for add. For example, if the input contains the phrase “is very beautiful”, 
the phrase “is beautiful” is treated as a new phrase in the original implementation even though it is 
caused by the delete operation.

"""

def is_subsequence(str1,str2):
    m = len(str1) 
    n = len(str2)
    i, j = 0, 0
    while j<m and i<n: 
        if str1[j] == str2[i]:     
            j = j+1    
        i = i + 1
    return j==m 

def SARIngram(sgrams, cgrams, rgramslist, numref, complex):
    rgramsall = [rgram for rgrams in rgramslist for rgram in rgrams]
    rgramcounter = Counter(rgramsall)

    sgramcounter = Counter(sgrams)
    sgramcounter_rep = Counter()
    for sgram, scount in sgramcounter.items():
        sgramcounter_rep[sgram] = scount * numref

    cgramcounter = Counter(cgrams)
    cgramcounter_rep = Counter()
    for cgram, ccount in cgramcounter.items():
        cgramcounter_rep[cgram] = ccount * numref

    # KEEP
    keepgramcounter_rep = sgramcounter_rep & cgramcounter_rep
    keepgramcountergood_rep = keepgramcounter_rep & rgramcounter
    keepgramcounterall_rep = sgramcounter_rep & rgramcounter

    keeptmpscore1 = 0
    keeptmpscore2 = 0
    for keepgram in keepgramcountergood_rep:
        keeptmpscore1 += keepgramcountergood_rep[keepgram] / keepgramcounter_rep[keepgram]
        keeptmpscore2 += keepgramcountergood_rep[keepgram] / keepgramcounterall_rep[keepgram]
        # print "KEEP", keepgram, keepscore, cgramcounter[keepgram], sgramcounter[keepgram], rgramcounter[keepgram]
    keepscore_precision = 0
    if len(keepgramcounter_rep) > 0:
        keepscore_precision = keeptmpscore1 / len(keepgramcounter_rep)
    keepscore_recall = 0
    if len(keepgramcounterall_rep) > 0:
        keepscore_recall = keeptmpscore2 / len(keepgramcounterall_rep)
    keepscore = 0
    if keepscore_precision > 0 or keepscore_recall > 0:
        keepscore = 2 * keepscore_precision * keepscore_recall / (keepscore_precision + keepscore_recall)

    # DELETION
    delgramcounter_rep = sgramcounter_rep - cgramcounter_rep
    delgramcountergood_rep = delgramcounter_rep - rgramcounter
    delgramcounterall_rep = sgramcounter_rep - rgramcounter
    deltmpscore1 = 0
    deltmpscore2 = 0
    for delgram in delgramcountergood_rep:
        deltmpscore1 += delgramcountergood_rep[delgram] / delgramcounter_rep[delgram]
        deltmpscore2 += delgramcountergood_rep[delgram] / delgramcounterall_rep[delgram]
    delscore_precision = 0
    if len(delgramcounter_rep) > 0:
        delscore_precision = deltmpscore1 / len(delgramcounter_rep)
    delscore_recall = 0
    if len(delgramcounterall_rep) > 0:
        delscore_recall = deltmpscore1 / len(delgramcounterall_rep)
    delscore = 0
    if delscore_precision > 0 or delscore_recall > 0:
        delscore = 2 * delscore_precision * delscore_recall / (delscore_precision + delscore_recall)

    # ADDITION
    addgramcounter = set(cgramcounter) - set(sgramcounter)
    addgramcountergood = set(addgramcounter) & set(rgramcounter)
    addgramcounterall = set(rgramcounter) - set(sgramcounter)

    sgrams_set = set()
    for gram in sgrams:
        sgrams_set.update(gram.split())

    addgramcountergood_new = set()
    for gram in addgramcountergood:
        if any([tok not in sgrams_set for tok in gram.split()]) or not is_subsequence(gram.split(), complex.split()):
            addgramcountergood_new.add(gram)
    addgramcountergood = addgramcountergood_new

    addtmpscore = 0
    for _ in addgramcountergood:
        addtmpscore += 1

    addscore_precision = 0
    addscore_recall = 0
    if len(addgramcounter) > 0:
        addscore_precision = addtmpscore / len(addgramcounter)
    if len(addgramcounterall) > 0:
        addscore_recall = addtmpscore / len(addgramcounterall)
    addscore = 0
    if addscore_precision > 0 or addscore_recall > 0:
        addscore = 2 * addscore_precision * addscore_recall / (addscore_precision + addscore_recall)

    return (keepscore, (delscore_precision, delscore_recall, delscore), addscore)


def SARIsent(ssent, csent, rsents):
    numref = len(rsents)

    s1grams = ssent.lower().split(" ")
    c1grams = csent.lower().split(" ")
    s2grams = []
    c2grams = []
    s3grams = []
    c3grams = []
    s4grams = []
    c4grams = []

    r1gramslist = []
    r2gramslist = []
    r3gramslist = []
    r4gramslist = []

    for rsent in rsents:
        r1grams = rsent.lower().split(" ")
        r2grams = []
        r3grams = []
        r4grams = []
        r1gramslist.append(r1grams)
        for i in range(0, len(r1grams) - 1):
            if i < len(r1grams) - 1:
                r2gram = r1grams[i] + " " + r1grams[i + 1]
                r2grams.append(r2gram)
            if i < len(r1grams) - 2:
                r3gram = r1grams[i] + " " + r1grams[i + 1] + " " + r1grams[i + 2]
                r3grams.append(r3gram)
            if i < len(r1grams) - 3:
                r4gram = r1grams[i] + " " + r1grams[i + 1] + " " + r1grams[i + 2] + " " + r1grams[i + 3]
                r4grams.append(r4gram)
        r2gramslist.append(r2grams)
        r3gramslist.append(r3grams)
        r4gramslist.append(r4grams)

    for i in range(0, len(s1grams) - 1):
        if i < len(s1grams) - 1:
            s2gram = s1grams[i] + " " + s1grams[i + 1]
            s2grams.append(s2gram)
        if i < len(s1grams) - 2:
            s3gram = s1grams[i] + " " + s1grams[i + 1] + " " + s1grams[i + 2]
            s3grams.append(s3gram)
        if i < len(s1grams) - 3:
            s4gram = s1grams[i] + " " + s1grams[i + 1] + " " + s1grams[i + 2] + " " + s1grams[i + 3]
            s4grams.append(s4gram)

    for i in range(0, len(c1grams) - 1):
        if i < len(c1grams) - 1:
            c2gram = c1grams[i] + " " + c1grams[i + 1]
            c2grams.append(c2gram)
        if i < len(c1grams) - 2:
            c3gram = c1grams[i] + " " + c1grams[i + 1] + " " + c1grams[i + 2]
            c3grams.append(c3gram)
        if i < len(c1grams) - 3:
            c4gram = c1grams[i] + " " + c1grams[i + 1] + " " + c1grams[i + 2] + " " + c1grams[i + 3]
            c4grams.append(c4gram)

    (keep1score, del1score, add1score) = SARIngram(s1grams, c1grams, r1gramslist, numref, ssent)
    (keep2score, del2score, add2score) = SARIngram(s2grams, c2grams, r2gramslist, numref, ssent)
    (keep3score, del3score, add3score) = SARIngram(s3grams, c3grams, r3gramslist, numref, ssent)
    (keep4score, del4score, add4score) = SARIngram(s4grams, c4grams, r4gramslist, numref, ssent)

    del1p, del1r, del1f = del1score
    del2p, del2r, del2f = del2score
    del3p, del3r, del3f = del3score
    del4p, del4r, del4f = del4score

    avgkeepscore = sum([keep1score, keep2score, keep3score, keep4score]) / 4
    avgdelpscore = sum([del1p, del2p, del3p, del4p]) / 4
    avgdelrscore = sum([del1r, del2r, del3r, del4r]) / 4
    avgdelfscore = sum([del1f, del2f, del3f, del4f]) / 4
    avgaddscore = sum([add1score, add2score, add3score, add4score]) / 4
    finalpscore = (avgkeepscore + avgdelpscore + avgaddscore) / 3
    finalfscore = (avgkeepscore + avgdelfscore + avgaddscore) / 3
    return avgkeepscore, (avgdelpscore, avgdelrscore, avgdelfscore), avgaddscore, (finalpscore, finalfscore)


def compute_sari(complex_sentences, reference_sentences, simplified_sentences):

    delp_scores = list()
    delr_scores = list()
    delf_scores = list()
    add_scores = list()
    sari_scores = list()
    sarif_scores = list()
    keep_scores = list()
    for i in range(len(simplified_sentences)):
        keep, dels, add, final = SARIsent(complex_sentences[i], simplified_sentences[i],
                                          reference_sentences[i])
        add_scores.append(add)
        delp_scores.append(dels[0])
        delr_scores.append(dels[1])
        delf_scores.append(dels[2])
        keep_scores.append(keep)
        sari_scores.append(final[0])
        sarif_scores.append(final[1])
    
    return np.mean(sari_scores), np.mean(sarif_scores), np.mean(add_scores), np.mean(keep_scores), np.mean(
        delp_scores), np.mean(delr_scores), np.mean(delf_scores)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--complex", dest="complex",
                        help="complex sentences", metavar="FILE")
    parser.add_argument("-r", "--reference", dest="reference",
                        help="reference sentences", metavar="FILE")
    parser.add_argument("-s", "--simplified", dest="simplified",
                        help="simplified sentences", metavar="FILE")

    args = parser.parse_args()
    print('SARI score: {}'.format(compute_sari(args.complex, args.reference, args.simplified)))
