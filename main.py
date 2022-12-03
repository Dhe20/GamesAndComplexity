from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
import pandas as pd
import numpy as np
from tqdm import tqdm




# x.Metrics().AnimateEvolution(50)

# y = Iterator(20, 20, Ternary=False, Seed=0)
# y.Run(UnoReverse=True)
# # y.Metrics().AnimateEvolution(100)
# y.VisualiseGrid()

# #x.Metrics().PlotRPSAmount()
# # # x.Metrics().PlotNormRPSAmount()
# # x.Metrics().PlotPeriodicity(cutoff = 100)
# # Eval.PlotSimilarity()
# # Eval.PlotRPSAmount()



x = Iterator(300, 1000, Ternary = True)#, EmptyCellCount= 150)
x.EmptyGrid()# x.AddAgent('R',[0,1])
# x.AddAgent('R',[1,2])
# x.AddAgent('R',[2,1])
x.AddAgent('R',[0,0])
x.VisualiseGrid()
x.CountAgents()
#x.Run(LifeAndDeath=True, SaveData=False)
#x.RunUntilConvergence(LifeAndDeath=True)
#x.Metrics().AnimateEvolution(20)
x.VisualiseGrid()

'''
#sanity check
import numpy as np
import pickle
# filepath = 'pkl/timedata/'
# filename = '20 21 - 12-03 12:30.pkl'
# pickle_in = open(filepath+filename, 'rb')
# data1 = pickle.load(pickle_in)
# data1 = data1[1][:-1]

# filename = '20 21 - 12-03 03:57.pkl'
# pickle_in = open(filepath+filename, 'rb')
# data = pickle.load(pickle_in)
# data=  np.delete(data, 1)

# NGrids = 21
# Grids = np.arange(3,NGrids+2) # dumb arange
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1,1, figsize =(10,6))
# ax.plot(Grids, data1, color = 'red')
# ax.set_xlabel('Grid Size')
# ax.set_ylabel('TimeSteps (scaled)')
# plt.show()



from tqdm import tqdm
import numpy as np

NSamples = 20
NGrids = 21
Grids = np.arange(2,NGrids+2) # dumb arange
DataStruc = np.zeros((NSamples,NGrids))
for j in range(NSamples):
    for i in tqdm(range(len(Grids))):
        x = Iterator(Grids[i], 1000, Ternary=True)
        NIters = x.RunUntilConvergence(LifeAndDeath=True, AppendData=False)
        DataStruc[j,i] = NIters

# print(NItersAll)
# #import
# # import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1,1, figsize =(10,6))
# ax.plot(Grids, NItersAll/max(NItersAll), color = 'red')
# ax.set_xlabel('Grid Size')
# ax.set_ylabel('TimeSteps (scaled)')
# plt.show()


#similarity analysis
#x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()

import numpy as np
meantsteps = np.zeros(NGrids)

for i in range(NGrids):
    meantsteps[i] = np.mean(DataStruc[:,i])

import pickle
#writing data
data=[DataStruc, meantsteps]
filepath = 'pkl/timedata/'
import datetime
filename = str(NSamples)+' '+str(NGrids)+' - '+''.join(datetime.datetime.today().strftime("%m-%d %H:%M"))+'.pkl'
pickle_out = open(filepath+filename, 'wb')
pickle.dump(data, pickle_out)
pickle_out.close()


#sanity check
pickle_in = open(filepath+filename, 'rb')
data1 = pickle.load(pickle_in)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1,1, figsize =(10,6))
ax.plot(Grids, data1[0], color = 'red')
ax.set_xlabel('Grid Size')
ax.set_ylabel('TimeSteps (scaled)')
plt.show()
'''
