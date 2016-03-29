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

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

IMG_STORE = "../orlo/spacegallery/"

iris = datasets.load_iris()

X = iris.data
y = iris.target
target_names = iris.target_names

pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

lda = LinearDiscriminantAnalysis(n_components=2)
X_r2 = lda.fit(X, y).transform(X)

if __name__ == '__main__':
    # Percentage of variance explained for each components
    print('explained variance ratio (first two components): %s'
          % str(pca.explained_variance_ratio_))

    plt.figure()
    for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
        plt.scatter(X_r[y == i, 0], X_r[y == i, 1], c=c, label=target_name)
    plt.legend()
    plt.title('PCA of IRIS dataset')

    plt.figure()
    for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
        plt.scatter(X_r2[y == i, 0], X_r2[y == i, 1], c=c, label=target_name)
    plt.legend()
    plt.title('LDA of IRIS dataset')

    plt.savefig(IMG_STORE+"iris.png")
