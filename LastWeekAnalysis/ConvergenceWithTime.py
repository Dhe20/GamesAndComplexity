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
Graph = False
ThreeDee = False

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

if ThreeDee:
    import pandas as pd
    df = pd.read_csv('LastWeekAnalysis/ConvergenceRateGridWithNoIters.csv', usecols=['Life Rate','Death Rate','Number of Iterations'])
    data = df.to_numpy()
    from mpl_toolkits import mplot3d
    from matplotlib import cm
    #ax._axis3don = False
    fig = plt.figure(figsize=(6,6))
    fig.tight_layout()
    ax = plt.axes(projection='3d')
    p = ax.plot_trisurf(data[:,0], data[:,1], data[:,2], cmap=cm.jet, alpha = 1,linewidth = 0.2, antialiased = True)
    ax.set_xlabel('Birth Rate', fontsize = 12, labelpad=1000)
    ax.zaxis.set_rotate_label(False)  # disable automatic rotation
    ax.view_init(30,240-180)
    #ax.set_proj_type('persp', focal_length = 100)
    ax.zaxis.labelpad=0.001
    ax.xaxis.labelpad=1
    ax.yaxis.labelpad=0.001
    ax.set_ylabel('Death Rate', fontsize = 12, labelpad=0)
    ax.tick_params( labelsize = 7.5, pad = 0.5)
    ax.set_zlabel('Number of Iterations', rotation = 90, fontsize = 10, labelpad=0)
    fig.colorbar(p, shrink = 0.3, aspect = 3)
    ax.set_title('Time to Converge against Birth and Death Probability', fontsize = 10)
    plt.savefig('pres/lifeanddeathconvergence.png', dpi = 600)
    plt.show()

import pandas as pd

pottsham = pd.read_csv('LastWeekAnalysis/PottHamiltonian (1).csv', usecols=['Times'])

pottsham = pottsham.to_numpy()

times = []
for i in range(len(pottsham)-1):
    if pottsham[i+1]<pottsham[i]:
        times.append(pottsham[i][0])

print(len(times))

#import
import matplotlib.pyplot as plt
#make figure
fig, ax = plt.subplots(1,1, figsize =(10,6))
ax.hist(times, bins = 50, color = 'red')
ax.set_xlabel('Time')
ax.set_ylabel('Number of Events')
plt.savefig('pres/PottsHist.png', dpi = 600)
plt.show()