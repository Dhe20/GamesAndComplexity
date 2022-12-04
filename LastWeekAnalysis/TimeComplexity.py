#Method for time evaluation

from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
import pandas as pd
import numpy as np
from tqdm import tqdm

TimeDict = {}

for i in range(1,20):
    GridSizeTimes = []
    for j in range(0,10):
        st = time.time()
        x = Iterator(i*10, 10, Ternary=True, Seed=10*i+j)
        x.Run(LifeAndDeath=True)
        x.VisualiseGrid()
        et = time.time()
        elapsed_time = et - st
        GridSizeTimes.append(elapsed_time/10)
    TimeDict.update({str(10*i): GridSizeTimes})

Times = pd.DataFrame.from_dict(TimeDict)
Times.to_csv("TimeComplexity.csv")
##
Times = pd.read_csv("/Users/daneverett/Downloads/TimeComplexity.csv").iloc[:, 1:10]
Y = Times.mean().values
Yerr = Times.std().values
LogY = np.log(np.array(Y))

X = [int(x) for x in list(Times.columns)]
LogX = np.log(np.array(X))

plt.errorbar(X, Y, yerr = Yerr)
# plt.errorbar(LogX,LogY)
plt.show()
