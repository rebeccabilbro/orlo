#!/usr/bin/env python
# valcurve.py


# Title:        Plot validation curves for tour
# Author:       Rebecca Bilbro
# Date:         3/23/16
# Organization: District Data Labs


"""
Plot Validation Curves for classified datasets.
"""

#####################################################################
# Imports
#####################################################################
import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer

from sklearn.svm import SVC
from sklearn.learning_curve import validation_curve

IMG_STORE = "../orlo/valgallery/"

#####################################################################
# Helpers
#####################################################################
def openFile(fname):
    """
    Opens data file.
    """
    with open(fname, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,\t')
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        data = list(reader)
        return data

#####################################################################
# Plotter
#####################################################################


dataset = openFile("data/tic-tac-toe.data")

target = [row[-1] for row in dataset]
data = []
for row in dataset:
    row.remove(row[-1])
    data.append(row)

label_enc = LabelEncoder()
encoded_labels = label_enc.fit_transform(target)
mapping = []
for instance in range(len(data)):
    D = dict()
    for f in range(len(data[instance])):
        D[f] = data[instance][f]
    mapping.append(D)
data_enc = DictVectorizer(sparse=False)
encoded_data = data_enc.fit_transform(mapping)


X, y = encoded_data, encoded_labels

param_range = np.logspace(-7, 3, 5)
train_scores, test_scores = validation_curve(
    SVC(), X, y, param_name="gamma", param_range=param_range,    #Gamma is the kernel coefficient for SVM
    cv=10, scoring="accuracy", n_jobs=1)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.title("Validation Curve with SVM")
plt.xlabel("$\gamma$")
plt.ylabel("Score")
plt.ylim(0.0, 1.1)
plt.semilogx(param_range, train_scores_mean, label="Training score", color="r")
plt.fill_between(param_range, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.2, color="r")
plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
             color="g")
plt.fill_between(param_range, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.2, color="g")
plt.legend(loc="best")
plt.savefig("valgallery/tictactoe.png")
