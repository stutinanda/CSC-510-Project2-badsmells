import sys
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

def plot(repo):
    columns = ['Issue', 'Text']
    data = pd.read_csv(repo, usecols=columns)
    noofcomments = {}
    for row in data.itertuples():
        if row[1] in noofcomments:
            if row[2] is None or row[2] is '' or row[2].isspace():
                continue
            noofcomments[row[1]] += 1
        else:
            if row[2] is None or row[2] is '' or row[2].isspace():
                noofcomments[row[1]] = 0
                continue
            noofcomments[row[1]] = 1
    mean = sum(noofcomments.values()) / float(len(noofcomments))
    sumsq = 0
    for val in noofcomments.values():
        sumsq = sumsq + ((val - mean)*(val - mean))
    variance = sumsq / len(noofcomments)
    sd = math.sqrt(variance)

    print 'MIN = ', min(noofcomments.values())
    print 'MAX = ', max(noofcomments.values())
    print 'MEAN = ', mean
    print 'VARIANCE = ', variance
    print 'STANDARD DEVIATION = ', sd

    x = np.linspace(-1, 3, len(noofcomments))
    plt.plot(x, mlab.normpdf(x, mean, sd))
    plt.savefig(repo[:-4] + '_avg.png')
    plt.close()

def plotavgcomments():
    filenames = ['data/Repo 1_comments.csv', 'data/Repo 2_comments.csv', 'data/Repo 3_comments.csv']
    for filename  in filenames:
        plot(filename)

plotavgcomments()
