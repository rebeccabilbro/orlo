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
import random
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
            name = re.sub(r'[^\w\s]','',pname).lower()
            if name not in urls:
                urls[name] = pname
        return urls

def parsePage(key,mltype):
    """
    Reads child urls from main url and determines whether the leaf node dataset
    is for the machine learning type ("Classification", "Regression", "Clustering",
    "Relational").
    """
    results = {}
    data_desc = requests.get(BASE_URL+"datasets/"+key)
    desc = data_desc.content
    soup = BeautifulSoup(desc)
    if len(soup.find_all(text=re.compile(mltype)))>0:
        for a in soup.find_all('a', href=re.compile("machine-learning-databases")):
            data_idx = requests.get((BASE_URL+a['href'].strip("../")))
            index = data_idx.content
            moresoup = BeautifulSoup(index)
            for b in moresoup.find_all('a', href=re.compile(r'\b\.xls\b|\b\.data\b|\b\.csv\b')):
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
        print "Couldn't get the file for '%s'" %surl

def getAll(urls,criteria):
    """
    Given the urls, gets all of the datasets that meet the search criteria
    """
    print "Getting all the datasets for you - hope you have enough disk space!"
    for name,pname in urls.items():
        x = parsePage(pname,criteria)
        for k,v in x.items():
            getData(v,BASE_STORE+k)

def getOne(urls,criteria):
    """
    Given the urls, get a random dataset that meets the search criteria
    """
    randompick = random.choice(urls.keys())
    x = parsePage(urls[randompick],criteria)
    if any(x):
        for k,v in x.items():
            print "Getting the '%s' dataset for you." %k
            getData(v,BASE_STORE+k)
    else: getOne(urls,criteria)


if __name__ == '__main__':
    # read the links from the saved text file
    links = readPage("../orlo/data/uci_text.txt")

    # get a random dataset suitable for Classification
    getOne(links,"Classification")
