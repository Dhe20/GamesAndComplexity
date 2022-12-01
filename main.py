from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(3, 1000, Ternary = True)#, EmptyCellCount= 150)
x.EmptyGrid()
# x.AddAgent('R',[0,1])
# x.AddAgent('R',[1,2])
# x.AddAgent('R',[2,1])
x.AddAgent('R',[0,0])
x.VisualiseGrid()
x.CountAgents()
#x.Run(LifeAndDeath=True, SaveData=False)
x.RunUntilConvergence(LifeAndDeath=True)
#x.Metrics().AnimateEvolution(20)
x.VisualiseGrid()



'''scaling analysis'''
from tqdm import tqdm
import numpy as np
Grids = np.arange(3,30)
NItersAll = np.zeros(len(Grids))
for i in tqdm(range(len(Grids))):
    x = Iterator(Grids[i], 1000, Ternary=True)
    x.EmptyGrid()
    x.AddAgent('R',[0,0])
    NIters = x.RunUntilConvergence(LifeAndDeath=True)
    NItersAll[i] = NIters
#import
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1,1, figsize =(10,6))
ax.plot(Grids, NItersAll/max(NItersAll), color = 'red')
ax.set_xlabel('Grid Size')
ax.set_ylabel('TimeSteps (scaled)')
plt.show()


'''similarity analysis'''
#x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



