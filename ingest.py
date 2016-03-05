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
import re
import requests
from bs4 import BeautifulSoup

#####################################################################
# Global Variables
#####################################################################

UCI_URL = "https://archive.ics.uci.edu/ml/datasets.html"
BASE_URL = "https://archive.ics.uci.edu/ml/"
BASE_STORE = "../orlo/data/"
#####################################################################
# Ingestion Tools
#####################################################################

def getPage(url):
    """
    Get all the text and links from the page.
    We don't want to do very often, so when we do, save result to a file.
    """
    result = requests.get(url)
    text = result.content
    with open('uci_text.txt', 'w') as f:
        f.write(text.read())

def readPage(fname):
    """
    Find names for all datasets on the page, get their links, and return a dict.
    """
    urls = {}
    with open(fname, 'r') as f:
        text = f.read()
        soup = BeautifulSoup(text)
        for a in soup.find_all('a', href=re.compile("datasets/")):
            pname = re.sub("datasets/","",str(a['href']))
            # name = pname.split()
            name = re.sub(r'[^\w\s]','',pname).lower()
            if name not in urls:
                urls[name] = pname
        return urls

def parsePage(key,mltype):
    """
    Reads child urls from main url and determines whether the leaf node dataset
    is for the machine learning type ("Classification", "Regression", "Relational").
    """
    results = {}
    data_desc = requests.get(BASE_URL+"datasets/"+key)
    desc = data_desc.content
    soup = BeautifulSoup(desc)
    if len(soup.find_all(text=re.compile(mltype)))>0:
        for a in soup.find_all('a', href=re.compile("machine-learning-databases")):
            data_idx = requests.get((BASE_URL+a['href'].strip("../")))
            index = data_idx.content
            soup = BeautifulSoup(index)
            for b in soup.find_all('a', href=re.compile(r'\b\.xls\b|\b\.data\b|\b\.csv\b')):
                results[b['href']] = BASE_URL+a['href'].strip("../")+"/"+b['href']
    return results


def getData(surl,fname):
    """
    For a dataset URL, use requests library to grab the dataset,
    and save it to the data directory using the name.
    """
    try:
        response = requests.get(surl)
        outpath = os.path.abspath(fname)
        with open(outpath, 'w') as f:
            f.write(response.content)
    except:
        print "Couldn't get the file for %d" %surl

def ingest(urldict):
    """
    Read the key, value pairs from a dictionary, get & store the datasets.
    """
    for key,val in urlsdict.items():
        getData(BASE_URL+"datasets/"+val, BASE_STORE+key+".csv")

if __name__ == '__main__':
    # Create parent url dict
    links = readPage("../orlo/data/uci_text.txt")
    for name,pname in links.items():
        x = parsePage(pname,"Classification")
        for k,v in x.items():
            getData(v,BASE_STORE+k)

    # testsets = {"pageblocks":"https://archive.ics.uci.edu/ml/machine-learning-databases/page-blocks/page-blocks.data.Z",
    #             "winequality":"https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    #             "lenses":"https://archive.ics.uci.edu/ml/machine-learning-databases/lenses/lenses.data"}
    # for k,v in testsets.items():
    #
    # with open('uci_links.csv', 'w') as f:
    #     f.write(links)
    # print ("Regression:")
    # parsePage("cardiotocography","Regression")
    # parsePage("lungcancer","Regression")
    # parsePage("annealing","Regression")
    # parsePage("kinship","Regression")
    # print ("Classification:")
    # parsePage("cardiotocography","Classification")
    # parsePage("lung+cancer","Classification")
    # parsePage("annealing","Classification")
    # parsePage("kinship","Classication")
    # print ("Relational:")
    # parsePage("cardiotocography","Relational")
    # parsePage("lungcancer","Relational")
    # parsePage("annealing","Relational")
    # parsePage("kinship","Relational")
    # print ("Clustering:")
    # parsePage("cardiotocography","Clustering")
    # parsePage("lungcancer","Clustering")
    # parsePage("annealing","Clustering")
    # parsePage("kinship","Clustering")
    # data_desc = requests.get('https://archive.ics.uci.edu/ml/datasets/annealing')
    # desc = data_desc.content
    # soup = BeautifulSoup(desc)
    # for a in soup.find_all('a', href=re.compile("machine-learning-databases")):
    #     print a['href']
