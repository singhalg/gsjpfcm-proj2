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



def geneBySiteCSV(file_name):
    fhin = open(file_name, 'rU')
    data = fhin.readlines()
    fhin.close()

    outfile_name = + 'geneByCancer.csv'
    fhout = open(outfile_name, 'w')
    geneSet = Set([])


    for line in data[1:]:
        flds = line.split(',')
        geneSet.add(flds[0])

    print len(geneSet)


    primarySites = pSite.keys()


    firstline = '\t' + ','.join(primarySites) + '\n'


    pSite = geneBySite(file_name)



def processGene(flds):




    pass

def geneByHistology():


    pass

def main():

    geneBySite('CosmicMutantExport_v58_150312.csv')
    #printme('hello !!')

if __name__ == '__main__':
    main()