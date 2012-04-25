#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gsinghal
#
# Created:     21/04/2012
# Copyright:   (c) gsinghal 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sets import Set
from sklearn.externals import joblib
import pickle
import numpy as np

def geneBySite(file_name):
    fhin = open(file_name, 'rU')
    data = fhin.readlines()
    fhin.close()
    pSite = {}

    for line in data[1:]:
        flds = line.split(',')
        if flds[6] not in pSite:
            geneDict  = {} # this will become a new value in pSite
            mutationList =[]
            mutationList.append(flds[14])
            geneDict[flds[0]] = mutationList
            pSite[flds[6]] = geneDict # new entry for the primary site has been created.
        else:
            genDict = pSite[flds[6]]
            if flds[0] in genDict: # if gene entry is present in that cancer
                mutList = genDict[flds[0]]
                mutList.append(flds[14])
                genDict[flds[0]] = mutList
                pSite[flds[6]] = genDict

            else:
                # create new entry with gene name as the key and list of mutation types as value
                mutList = []
                mutList.append(flds[14])
                genDict[flds[0]] = mutList

                pSite[flds[6]] = genDict






    keys = pSite.keys()
    for each in keys[:10]:
        print each
        genDict = pSite[each]
        genes = genDict.keys()
        for aGene in genes[:10]:
            print aGene, genDict[aGene]

    return pSite



def geneBySiteCSV(file_name, pickleDump):
    fhin = open(file_name, 'rU')
    data = fhin.readlines()
    fhin.close()


    geneSet = Set([])

    for line in data[1:]:
        flds = line.split(',')
        geneSet.add(flds[0])

    print '# of genes = ', len(geneSet)
    genes = sorted(list(geneSet))


    pSite = geneBySite(file_name)
    primarySites = sorted(pSite.keys())

    fhout = open('geneByPrimSite.csv', 'w')
    firstline = '\t' + ','.join(primarySites) + '\n'
    fhout.write(firstline)

    geneSite = []

    for aGene in genes:
        geneScore = []
        for aSite in primarySites:
            geneDict = pSite[aSite]
            if aGene in geneDict:
                geneScore.append(processGene(geneDict[aGene]))
            else:
                geneScore.append(0)
        geneSite.append(geneScore)

    geneSiteArr = np.array(geneSite)

    if pickleDump:
        fhPickle = open('geneXprimarySites.pkl', 'w')
        pickle.dump(geneSite, fhPickle)
        fhPickle.close()
        joblib.dump(geneSiteArr, 'geneXprimarySiteArr.pkl')

    for i in range(len(genes)):
        geneSiteStr = [str(n) for n in geneSite[i]]
        outline = genes[i]+ ','+ ','.join(geneSiteStr) + '\n'
        fhout.write(outline)

    fhout.close()

    return primarySites, genes, geneSite, geneSiteArr

def processGene(flds):
    score = 0
    dict = {'Complex - compound substitution':1,
    'Complex - deletion inframe':1,
    'Complex - frameshift':4,
    'Complex - insertion inframe':1,
    'Deletion - Frameshift':4,
    'Deletion - In frame':1,
    'Insertion - Frameshift':4,
    'Insertion - In frame':1,
    'Mutations':0,
    'No detectable mRNA/protein':4,
    'Nonstop extension':4,
    'Substitution - Missense':1,
    'Substitution - Nonsense':4,
    'Substitution - coding silent':0,
    'Unknown':0,
    'Whole gene deletion':4
    }



    for each in flds:
        score+= dict[each]
    return score

def geneByHistology():


    pass

def main():

  #  geneBySite('CosmicMutantExport_v58_150312.csv')
    geneBySiteCSV('CosmicMutantExport_v58_150312.csv', True)

    #printme('hello !!')

if __name__ == '__main__':
    main()