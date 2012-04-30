# Copyright 2012 Colin McDonough (cmcdonough@wustl.edu)

from module2_GS import *
from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import PCA
from sklearn.externals import joblib

X = normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')
random_pca_data = normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')
pca_data = normalization('gene_IndividualsArr.pkl', 'top10Genes_Indiv.pkl')

random_pca = RandomizedPCA(n_components=50)
random_pca_model = random_pca.fit(random_pca_data)
random_X_new = random_pca.fit_transform(X)
print 'random_pca explained', random_pca.explained_variance_ratio_
print 'random_pca explained sum', sum(random_pca.explained_variance_ratio_)
joblib.dump(random_pca_model, 'random_pca_model.pkl')
joblib.dump(random_pca.explained_variance_ratio_, 'random_pca.explained_variance_ratio_.pkl')
joblib.dump(random_X_new, 'random_X_new.pkl')

pca = PCA(n_components=50)
pca_model = pca.fit(pca_data)
pca_X_new = pca.fit_transform(X)
print 'pca explained', pca.explained_variance_ratio_
print 'pca explained sum', sum(pca.explained_variance_ratio_)
joblib.dump(pca_model, 'pca_model.pkl')
joblib.dump(pca_X_new, 'pca_X_new.pkl')
print pca_model
