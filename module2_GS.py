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
import pickle



def PCAnalysis():
    data = normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')
    print data.shape
    print data[0,9]
    pca = PCA(n_components=168)
    pca.fit(data)
##    print pca.explained_variance_
##    print pca.explained_variance_ratio_


def kmeansInd():
    data = normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')


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
'''
This method does 2 jobs.
First, it picks out the most mutated genes from the whole data, and secondly, it tries to normalize the data as per the row or column.
I have commented the second part (normalization) since after normalization, most of the elements were getting reduced to zeros.
'''
def normalization(dataPickle, topGenesPickle):

    data = joblib.load(dataPickle)
    print 'starting data.shape = ', data.shape
    top10Genes = joblib.load(topGenesPickle)
    dataTrimmed = []
    genes = []


    for each in top10Genes:
        dataTrimmed.append(data[each[2]])
        genes.append(each[0])

##    print len(dataTrimmed)
##    print len(dataTrimmed[0])
##    print genes
    dataArr = np.array(dataTrimmed, dtype='float')
    print 'm genes X n samples, shape of array = ', dataArr.shape

    dataMatrix = dataArr.transpose()
    print 'n samples X m genes, shape of array = ',dataMatrix.shape
    del data, dataTrimmed


##
##
##    dataMatrixNorm = nm(dataMatrix, axis=0, copy=True)
##    zeroC1 = 0
##    for each in dataMatrix:
##        for i in each:
##            if i != 0:
##                zeroC1+=1
##    zeroC2 = 0
##    for each in dataMatrixNorm:
##        for i in each:
##            if i != 0:
##                zeroC2+=1
##    sp = dataMatrixNorm.shape
##    print '# total elements in matrix = ', str(sp[0]*sp[1])
##
##    print dataMatrix[0]
##    print dataMatrixNorm[0]
##    print zeroC1
##    print zeroC2
    return dataMatrix

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



'''
NEEDS TO IMPORT

from sklearn.externals import joblib
import pickle

I have made 2 types of pickles, one using the pickle module and second using the joblib module.
sklearn.externals.joblib module allows efficient pickling of numpy arrays. On the other hand, pickle module allows serialization of any object.
@pickle: name of the pickle file, like gene_primarySiteArr.pkl
@type: type of pickle, 1 for joblib; 2 for pickle.

Most of the pickle files have been saved using joblib pickle. So try using type=1. If that does not work, try type=0.
'''
def loadPickle(pickle, type):
    if type:
        return joblib.load(pickle)
    else:
        fhPickle = open(pickle, 'rU')
        return pickle.load(fhPickle)





def main():
##    dataSurvey(5, True )
##    dataSurvey2(2, False, 'geneByIndividuals.csv' )
##    kmeansIter()
##    normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')
    PCAnalysis()
if __name__ == '__main__':
    main()
