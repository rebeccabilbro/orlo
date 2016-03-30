#!/usr/bin/env python
# space.py


# Title:        Plot LDA and PCA for Classified UCI Datasets for ROC Curves Tour
# Author:       Rebecca Bilbro
# Date:         3/29/16
# Organization: District Data Labs


"""
Plot PCA and LDA for classified datasets.
"""

#####################################################################
# Imports
#####################################################################
import matplotlib.pyplot as plt
import classi

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction import DictVectorizer

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

IMG_STORE = "../orlo/spacegallery/"


def pcaFit(data):
    pca = PCA(n_components=2)
    pcaT = pca.fit(data).transform(data)
    # Percentage of variance explained for each components
    print 'explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_)
    return pcaT

def ldaFit(data,labels):
    lda = LinearDiscriminantAnalysis(n_components=2)
    ldaT = lda.fit(data, labels).transform(data)
    return ldaT

if __name__ == '__main__':
    bundle = classi.labelFind(classi.openFile("data/tic-tac-toe.data.txt"))
    target_names = bundle[1]
    label_enc = LabelEncoder()
    encoded_labels = label_enc.fit_transform(target_names)
    features = bundle[0]
    mapping = []
    for instance in range(len(features)):
        D = dict()
        for f in range(len(features[instance])):
            D[f] = features[instance][f]
        mapping.append(D)
    data_enc = DictVectorizer(sparse=False)
    encoded_data = data_enc.fit_transform(mapping)

    X_r = pcaFit(encoded_data)
    X_r2 = ldaFit(encoded_data,encoded_labels)

    plt.figure()
    for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
        plt.scatter(X_r[encoded_labels == i, 0], X_r[encoded_labels == i, 1], c=c, label=target_name)
    plt.legend()
    plt.title('PCA of tic-tac-toe dataset')

    plt.figure()
    #TODO fix IndexError in following two lines
    for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
        plt.scatter(X_r2[encoded_labels == i, 0], X_r2[encoded_labels == i, 1], c=c, label=target_name)
    plt.legend()
    plt.title('LDA of tic-tac-toe dataset')
    plt.savefig(IMG_STORE+"tic-tac-toe.png")
