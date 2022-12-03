#redirect to main directory
import sys
sys.path.append('./')
from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import numpy as np
import pickle


#sanity check

Run = False
Graph = not Run

if Graph:
    filepath = 'pkl/timedata/'
    filename = '20 21 - 12-03 12:30.pkl'
    pickle_in = open(filepath+filename, 'rb')
    data1 = pickle.load(pickle_in)
    data1 = data1[1][:-1]

    filename = '20 21 - 12-03 03:57.pkl'
    pickle_in = open(filepath+filename, 'rb')
    data = pickle.load(pickle_in)
    data=  np.delete(data, 1)

    NGrids = 21
    Grids = np.arange(3,NGrids+2) # dumb arange
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1,1, figsize =(10,6))
    ax.plot(Grids, data1, color = 'red')
    ax.set_xlabel('Grid Size')
    ax.set_ylabel('TimeSteps (scaled)')
    plt.show()


if Run:
    from tqdm import tqdm

    NSamples = 20
    NGrids = 21
    Grids = np.arange(2,NGrids+2) # dumb arange
    DataStruc = np.zeros((NSamples,NGrids))
    for j in range(NSamples):
        for i in tqdm(range(len(Grids))):
            x = Iterator(Grids[i], 1000, Ternary=True)
            NIters = x.RunUntilConvergence(LifeAndDeath=True, AppendData=False)
            DataStruc[j,i] = NIters

    print(DataStruc)
    #import
    # import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1,1, figsize =(10,6))
    ax.plot(Grids, DataStruc/max(DataStruc), color = 'red')
    ax.set_xlabel('Grid Size')
    ax.set_ylabel('TimeSteps (scaled)')
    plt.show()

