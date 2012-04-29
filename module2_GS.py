#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gsinghal
#
# Created:     27/04/2012
# Copyright:   (c) gsinghal 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy as np
from sklearn.preprocessing import normalize as nm
from sklearn.decomposition import PCA



def PCAnalysis():
    data = normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')
    print data.shape
    pca = PCA(n_components=168)
    pca.fit(data)
    print pca.explained_variance_
    print pca.explained_variance_ratio_

def kmeansIter():

    data = normalization('gene_primarySiteArr.pkl', 'top10Genes_primSites.pkl')
    print data.shape
    models = joblib.load('kmeans_models4')
    for i in range(2,35):
        seeds = i
        model = kmeans(data, seeds, 50, 0.001)
        models.append(model)
    joblib.dump(models, 'kmeans_models4')
    print models[0]
##    for each in models:
##        print each.inertia_


def kmeans(data, seeds, nInit, step):

    KM = KMeans(k=seeds, n_init=nInit, init='k-means++', max_iter=300, tol=step)
    model = KM.fit(data)
##    print 'model = ', model
    return KM
##    return (KM.cluster_centers_, KM.labels_, KM.inertia_)
##inertia: float
##        The final value of the inertia criterion (sum of squared distances to
##        the closest centroid for all observations in the training set).

def normalization(dataPickle, topGenesPickle):
    top10Genes = joblib.load(topGenesPickle)
    data = joblib.load(dataPickle)

    dataTrimmed = []
    genes = []
    for each in top10Genes:
        dataTrimmed.append(data[each[2]])
        genes.append(each[0])

##    print len(dataTrimmed)
##    print len(dataTrimmed[0])
##    print genes
    dataArr = np.array(dataTrimmed)
    dataMatrix = dataArr.transpose()
    del data, dataTrimmed
    return dataMatrix


##    dataMatrixNorm = nm(dataMatrix, axis=0, copy=True)
##    zeroC1 = 0
##    for each in dataMatrix:
##        for i in each:
##            if i == 0:
##                zeroC1+=1
##    zeroC2 = 0
##    for each in dataMatrixNorm:
##        for i in each:
##            if i == 0:
##                zeroC2+=1
##    sp = dataMatrixNorm.shape
##    print '# total elements in matrix = ', str(sp[0]*sp[1])
##    print zeroC1
##    print zeroC2

def dataSurvey(topN, pickleDump):

    fhin = open('geneByPrimHist.csv', 'rU')
    samples = fhin.readline()
    csv = fhin.readlines()
    fhin.close()
    genes = []
    for each in csv:
        flds = each.split(',')
        genes.append(flds[0])


    data = joblib.load('gene_primaryHistArr.pkl')
    print data.shape

    print data[0]

    geneSum = []

    for i in range (len(data)):
        total = sum(data[i])
        geneSum.append((genes[i],  total, i))



    geneSumSorted = sorted(geneSum, key=myFun, reverse=True)


    print geneSumSorted[:1682]
    if pickleDump:
        relevantGenes = geneSumSorted[:1682]
        joblib.dump(relevantGenes, 'top10Genes_primHist.pkl') # this

    outFile = 'top' + str(topN)+ 'geneByPrimHist.csv'
    fhout = open(outFile, 'w')
    fhout.write(samples)
    topNpercent = int(0.01*float(topN)*float(16822))
    for i in range(topNpercent):
        geneVals = [str(x) for x in data[geneSumSorted[i][2]] ]
        outline = geneSumSorted[i][0]+ ',' + ','.join(geneVals) + '\n'
        fhout.write(outline)
    fhout.close()

##    impGenes = []
##
##    for each in relevantGenes:
##        impGenes.append(each[2])
##
##
##    print len(impGenes)


def dataSurvey2(topN, pickleDump, filename):
    fhin = open(filename, 'rU')
    samples = fhin.readline()
    csv = fhin.readlines()
    fhin.close()
    genes = []
    for each in csv:
        flds = each.split(',')
        genes.append(flds[0])


    data = joblib.load('gene_IndividualsArr.pkl')
    print data.shape

    print data[0]

    geneSum = []

    for i in range (len(data)):
        total = sum(data[i])
        geneSum.append((genes[i],  total, i))



    geneSumSorted = sorted(geneSum, key=myFun, reverse=True)


##    print geneSumSorted[:1682]
    if pickleDump:
        relevantGenes = geneSumSorted[:1682]
        joblib.dump(relevantGenes, 'top10Genes_Indiv.pkl') # this is a list of top 10 % most mutated genes.

    outFile = 'top' + str(topN)+ 'geneByInd.csv'
    fhout = open(outFile, 'w')
    fhout.write(samples)
    topNpercent = int(0.01*float(topN)*float(16822))
    for i in range(topNpercent):
        geneVals = [str(x) for x in data[geneSumSorted[i][2]] ]
        outline = geneSumSorted[i][0]+ ',' + ','.join(geneVals) + '\n'
        fhout.write(outline)
    fhout.close()


def myFun(list):
    return list[:][1]





def main():
##    dataSurvey(5, True )
##    dataSurvey2(2, False, 'geneByIndividuals.csv' )
##    kmeansIter()
##    normalization()
    PCAnalysis()
if __name__ == '__main__':
    main()
