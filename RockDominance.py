from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
import pandas as pd
import numpy as np
from tqdm import tqdm

PCTRock = []
IterationNum = []
Winners = []
RockWins = []
for pctRock in range (2,5):
    for iter in range(0,2):
        RockProb = pctRock / 100

        Prob = [RockProb,(1-RockProb)/2,(1-RockProb)/2]

        for j in range(0,10):
            x = Iterator(27, 200, Ternary=False, Seed=j, ProbsDist = Prob)
            NIters, Winner = x.RunUntilConvergence(LifeAndDeath = True, Winner = True)


            PCTRock.append(RockProb)
            Winners.append(Winner)
            IterationNum.append(NIters)

            if Winner == "R":
                RockWins.append(1)
            else: RockWins.append(0)

RockDominance = pd.DataFrame({"Rock_Dominance": PCTRock, "Convergence_Iter": IterationNum,
                              "Winner": Winners, "Rock_Won": RockWins})
print(RockDominance.head())
RockDominance.to_csv("RockDominance.csv")

##Eval

RockVals = RockDominance.Rock_Dominance.unique()

MeanIters = [RockDominance.query('Rock_Dominance == @val').Convergence_Iter.mean()
             for val in RockVals]

StdIters = [RockDominance.query('Rock_Dominance == @val').Convergence_Iter.std()
             for val in RockVals]

RockWon = [RockDominance.query('Rock_Dominance == @val').RockWins.sum()/10
             for val in RockVals]

RockDominanceMeta = pd.DataFrame({"Rock_Dominance": RockVals, "Mean_Iters": MeanIters, "Std_Iters": StdIters,
                              "Rock_Won": RockWon})

RockDominanceMeta.to_csv("RockDominanceMeta.csv")

plt.errorbar(RockDominanceMeta.RockVals.values, RockDominanceMeta.MeanIters.values,
             yerr = RockDominanceMeta.StdIters.values,c = RockDominanceMeta.RockWon.values, cmap = 'jet')
plt.show()




