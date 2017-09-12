#!/usr/bin/python

import filecmp
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

def getFiles(d):
    '''Get all files in a folder
    '''
    files = []
    for (dirpath, dirnames, filenames) in os.walk(d):
        for f in filenames:
            if f[0] != '.':
                files.append(os.path.join(dirpath, f));
    return files;

def getDir(d):
    '''Get all directories in a folder
    '''
    l = os.listdir(d);
    return [os.path.join(d, e) for e in l if os.path.isdir(os.path.join(d,e))];

def compareFiles(f1, f2):
    with open(f1, 'r') as content_file:
        c1= content_file.read()
    with open(f2, 'r') as content_file:
        c2= content_file.read()
    documents = [c1, c2];
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity[0, 1]

def compareFolders(dir1, dir2):
    '''Compare the files in a directory with the files in another directory
    '''
    files_1 = getFiles(dir1);
    files_2 = getFiles(dir2);
    for f1 in files_1:
        for f2 in files_2:
            similarity = compareFiles(f1, f2);
            if similarity > 0.8:
                print f1, f2, similarity

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python comparison.py dir'
        sys.exit(1);

    #Get all folders
    folders = getDir(sys.argv[1]);

    for index, d1 in enumerate(folders):
        for d2 in range(index+1, len(folders)):
            compareFolders(d1, folders[d2]);
