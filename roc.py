#!/usr/bin/env python
# roc.py


# Title:        Plot ROC curves for tour
# Author:       Rebecca Bilbro
# Date:         3/8/16
# Organization: District Data Labs


"""
Plot ROC Curves for classified datasets.
"""

#####################################################################
# Imports
#####################################################################
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from sklearn.metrics import roc_curve

IMG_STORE = "../orlo/rocgallery/"
#####################################################################
# Plotter
#####################################################################

def plotROC(act,pred,outfile):
    """
    Takes as input arrays of actual and predicted values and a name for the outfile.
    Outputs a png image of the plotted ROC curve.
    """
    false_positive_rate, true_positive_rate, thresholds = roc_curve(act, pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)

    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, 'blue', label='AUC = %0.2f'% roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'m--')
    plt.xlim([0,1])
    plt.ylim([0,1.1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(IMG_STORE+outfile+".png")

if __name__ == '__main__':
    actual       =  [0,0,1,0,0,0,1,0,0,1,1,1,1,0]
    predictions  =  [0.1,0,1,0,0,0.3,1,0,0,.9,1,1,1,0.1]
    plotROC(actual, predictions,"testfile")
