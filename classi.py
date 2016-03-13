#!/usr/bin/env python
# classi.py


# Title:        Apply Classification to UCI Datasets for ROC Curves Tour
# Author:       Rebecca Bilbro
# Date:         3/9/16
# Organization: District Data Labs


"""
Apply different classification methods to applicable datasets from UCI.
Use highest-scoring-estimator wins approach.
"""

#####################################################################
# Imports
#####################################################################
import csv
import numpy as np
from sklearn.svm import SVC
# from sklearn.lda import LDA
from sklearn.metrics import f1_score
from sklearn import cross_validation as cv
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

#####################################################################
# Global Variables
#####################################################################
estimators = ["LogisticRegression()","LDA()","GaussianNB()",\
              "KNeighborsClassifier()","DecisionTreeClassifier()",\
              "SVC(kernel=kernel)","RandomForestClassifier()"]

#####################################################################
# Classification
#####################################################################
def labelFind(fname):
    """
    Opens data file and performs unique value count on each column.
    assumes that the column with the fewest unique values contains the labels
    for classification.
    Outputs data organized as features, target.
    """
    with open(fname, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,\t')
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        counts={}
        for line in reader:
            for key in range(0,len(line)):
                if key not in counts:
                    counts[key] = []
                if line[key] not in counts[key]:
                    counts[key].append(line[key])

        label_col = [k for k in counts.keys() if len(counts.get(k))==min([len(n) for n in counts.values()])]
        labels = counts[label_col[0]]
        print "column %d contains the labels, which are:" % label_col[0], labels


def classi(data, target):
    """
    Takes data as input and runs different classifiers.
    Outputs a dict where the classifier name is the key, and the
    values are the expected and predicted values.
    """
    splits     = cv.train_test_split(data, target, test_size=0.08)
    X_train, X_test, y_train, y_test = splits

    results = {}
    for estimator in estimators:
        model      = estimator
        model.fit(X_train, y_train)
        expected   = y_test
        predicted  = model.predict(X_test)
        results[estimator] = (expected,predicted)
    return results


if __name__ == '__main__':
    labelFind("data/balance-scale.data")
    labelFind("data/breast-cancer-wisconsin.data")
    labelFind("data/isolet5.data")
    labelFind("data/tic-tac-toe.data")
