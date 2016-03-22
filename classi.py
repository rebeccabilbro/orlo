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


from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction import DictVectorizer

from sklearn import metrics
from sklearn import cross_validation as cv
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

#####################################################################
# Global Variables
#####################################################################
estimators = [LogisticRegression(),GaussianNB(),KNeighborsClassifier(),\
              DecisionTreeClassifier(),RandomForestClassifier()]

#####################################################################
# Classification
#####################################################################
def openFile(fname):
    """
    Opens data file and performs unique value count on each column.
    assumes that the column with the fewest unique values contains the labels
    for classification.
    Outputs label column.
    """
    with open(fname, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,\t')
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        data = list(reader)
        return data

def labelFind(dataset):
    """
    Performs unique value count on each column in dataset.
    assumes that the column with the fewest unique values contains the labels
    for classification.
    Outputs label column.
    """
    counts={}
    for line in dataset:
        for key in range(0,len(line)):
            if key not in counts:
                counts[key] = []
            if line[key] not in counts[key]:
                counts[key].append(line[key])

    label_col = [k for k in counts.keys() if len(counts.get(k))==min([len(n) for n in counts.values()])]
    labels = counts[label_col[0]]

    # print "column %d contains the labels, which are:" % label_col[0], labels

    targets = [row[label_col[0]] for row in dataset]

    features = []
    for row in dataset:
        row.remove(row[label_col[0]])
        features.append(row)

    return tuple([features, targets])



def classi(features, targets):
    """
    Takes data as input and runs different classifiers.
    Outputs a dict where the classifier name is the key, and the
    values are the expected and predicted values.
    """
    splits     = cv.train_test_split(features, targets, test_size=0.08)
    X_train, X_test, y_train, y_test = splits

    results = {}
    for estimator in estimators:
        model      = estimator
        model.fit(X_train, y_train)
        expected   = y_test
        predicted  = model.predict(X_test)

        precision = metrics.precision_score(expected, predicted)
        recall = metrics.recall_score(expected, predicted)
        accuracy = metrics.accuracy_score(expected, predicted)
        f1 = metrics.f1_score(expected, predicted)
        results[model] = (precision,recall,accuracy,f1)
    return results


if __name__ == '__main__':
    bundle = labelFind(openFile("data/tic-tac-toe.data"))
    labels = bundle[1]
    label_enc = LabelEncoder()
    encoded_labels = label_enc.fit_transform(labels)
    features = bundle[0]
    mapping = []
    for instance in range(len(features)):
        D = dict()
        for f in range(len(features[instance])):
            D[f] = features[instance][f]
        mapping.append(D)
    data_enc = DictVectorizer(sparse=False)
    encoded_data = data_enc.fit_transform(mapping)
    print classi(encoded_data, encoded_labels)

    # bundle = labelFind(openFile("data/breast-cancer-wisconsin.data"))
    # print bundle[0][0]
    # print bundle[1][0]
    #
    # bundle = labelFind(openFile("data/balance-scale.data"))
    # print bundle[0][0]
    # print bundle[1][0]
    #
    # bundle = labelFind(openFile("data/isolet5.data"))
    # print bundle[0][0]
    # print bundle[1][0]
