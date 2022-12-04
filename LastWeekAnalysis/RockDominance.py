from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
import pandas as pd
import numpy as np
from tqdm import tqdm
##
PCTRock = []
IterationNum = []
Winners = []
RockWins = []
for pctRock in tqdm(range (0,20)):
    RockProb = pctRock / 20
    Prob = [RockProb, (1 - RockProb) / 2, (1 - RockProb) / 2]
    for iter in range(0,20):
        x = Iterator(18, 200, Ternary=False, Seed=iter, ProbsDist = Prob)

        NIters, Winner = x.RunUntilConvergence(LifeAndDeath = True, Winner = True, ConvergenceBound=1e5)

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
RockDominance = pd.read_csv("../RockDominance.csv")

RockVals = RockDominance.Rock_Dominance.unique()

MeanIters = [RockDominance.query('Rock_Dominance == @val').Convergence_Iter.mean()
             for val in RockVals]

StdIters = [RockDominance.query('Rock_Dominance == @val').Convergence_Iter.std()
             for val in RockVals]

RockWon = [RockDominance.query('Rock_Dominance == @val').Rock_Won.sum()/len(RockDominance.query('Rock_Dominance == @val'))
             for val in RockVals]

RockDominanceMeta = pd.DataFrame({"Rock_Dominance": RockVals, "Mean_Iters": MeanIters, "Std_Iters": StdIters,
                              "Rock_Won": RockWon})

RockDominanceMeta.to_csv("RockDominanceMeta.csv")
print(RockDominanceMeta.head())
# plt.errorbar(RockDominanceMeta.Rock_Dominance.values, RockDominanceMeta.Mean_Iters.values,
#              yerr = RockDominanceMeta.Std_Iters.values)
# plt.show()

plt.plot(RockDominanceMeta.Rock_Dominance.values, RockDominanceMeta.Rock_Won.values)
plt.show()

