import sys
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import re

def plot(repo):
    columns = ['Message']
    data = pd.read_csv(repo, usecols=columns)
    num_linkedcommits = 0
    pat = '(#|[gG][hH]-)\d+'
    for row in data.itertuples():
        match = re.search(pat, row[1])
        if match:
            num_linkedcommits += 1

    perclinked = (num_linkedcommits * 100)/ len(data)
    percnotlinked = 100 - perclinked

    labels = ['commits linked to issues', 'commits not linked to issues']
    fracs = [perclinked, percnotlinked]
    plt.pie(fracs, labels=labels, autopct='%.0f%%', shadow=False, radius=0.5)
    plt.savefig(repo[:-4] + '.png')
    plt.close()

def plotcommits():
    filenames = ['data/Repo 1_commits.csv', 'data/Repo 2_commits.csv', 'data/Repo 3_commits.csv']
    for filename  in filenames:
        plot(filename)

plotcommits()
