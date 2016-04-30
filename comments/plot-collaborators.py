import sys
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

def plot(repo):
    columns = ['Issue', 'User', 'Text']
    data = pd.read_csv(repo, usecols=columns)
    comments = {}
    maxc = 0
    for row in data.itertuples():
        if row[1] in comments:
            if row[3] is None or row[3] is '' or row[3].isspace():
                continue
            if row[2] not in comments[row[1]]:
                comments[row[1]].append(row[2])
                if len(comments[row[1]]) > maxc:
                    maxc = len(comments[row[1]])
        else:
            if row[3] is None or row[3] is '' or row[3].isspace():
                comments[row[1]] = []
                continue
            comments[row[1]] = [row[2]]

    minc = maxc
    sumc = 0
    for val in comments.values():
        if len(val) < minc:
            minc = len(val)
        sumc += len(val)
    mean = sumc / float(len(comments))
    sumsq = 0
    for val in comments.values():
        sumsq = sumsq + ((len(val) - mean)*(len(val) - mean))
    variance = sumsq / len(comments)
    sd = math.sqrt(variance)

    print 'MIN = ', minc
    print 'MAX = ', maxc
    print 'MEAN = ', mean
    print 'VARIANCE = ', variance
    print 'STANDARD DEVIATION = ', sd

    x = np.linspace(0, 2, len(comments))
    plt.plot(x, mlab.normpdf(x, mean, sd))
    plt.savefig(repo[:-4] + '.png')
    plt.close()

def plotcollaborators():
    filenames = ['data/Repo 1_comments.csv', 'data/Repo 2_comments.csv', 'data/Repo 3_comments.csv']
    for filename  in filenames:
        plot(filename)

plotcollaborators()
