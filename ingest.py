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
    We don't want to do this very often, so when we do, save result to a file.
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

def getData(surl,fname):
    """
    For a dataset URL, use requests library to grab the dataset,
    and save it to the data directory using the name.
    """
    response = requests.get(singURL)
    outpath = os.path.abspath(fname)
    with open(outpath, 'w') as f:
        f.write(response.content)

def ingest(urldict):
    """
    Read the key, value pairs from a dictionary, get & store the datasets.
    """
    for key,val in urlsdict.items():
        getData(BASE_URL+"datasets/"+val, BASE_STORE+key+".csv")

if __name__ == '__main__':
    my_urls = readPage("../orlo/data/uci_text.txt")
    # for key,val in my_urls.items():
    #     print BASE_URL+val, BASE_STORE+key+".csv"


    kinship_desc_url = "https://archive.ics.uci.edu/ml/datasets/kinship"
    kinship_data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/kinship/"
    response = requests.get(kinship_desc_url)
    txt = response.content
    soup = BeautifulSoup(txt)
    if len(soup.find_all(text=re.compile('Relational')))>0:
        response = requests.get(kinship_data_url)
        txt = response.content
        soup = BeautifulSoup(txt)
        for a in soup.find_all('a', href=re.compile(".data")):
          print a['href']

    # print soup.find_all(text=re.compile('Classification'))
    # for a in soup.find_all('a', href=re.compile(".data")):
    #     print a['href']
