#!/usr/bin/env python
# ingest.py


# Title:        Dataset Ingestor for ROC Curves Tour
# Author:       Rebecca Bilbro
# Date:         2/27/16
# Organization: District Data Labs


"""
Ingest all the necessary datasets from UCI that are appropriate for classification.
"""

#####################################################################
# Imports
#####################################################################

import os
import requests


def findData(mastURL):
    """
    Identify datasets from UCI repository that are appropriate for classification.
    """
    pass

def getData(singURL,fname):
    """
    For a dataset URL, use requests library to grab and save the dataset to the data directory.
    """
    response = requests.get(singURL)
    outpath = os.path.abspath(fname)
    with open(outpath, 'w') as f:
        f.write(response.content)

if __name__ == '__main__':
    print "not implemented yet"
    # UCI_URL = "https://archive.ics.uci.edu/ml/datasets.html?format=&task=cla&att=&area=&numAtt=&numIns=&type=&sort=nameUp&view=table"
    # data_urls = findData(UCI_URL)
    # for url in data_urls:
    #     getData(url,fname)
