from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
import pandas as pd
import numpy as np
from tqdm import tqdm

N = 26
B = []
M = []
Mean = []
Std = []
OStd = []
for BProb in tqdm(np.linspace(1, 25, N)):
    BProb = BProb / 100
    for MProb in np.linspace(1, 25, N):
        x = Iterator(27, 200, Ternary=True, Seed=0)
        MProb = MProb/100
        x.Run(LifeAndDeath=True, BProb = BProb, MProb = MProb)
        mean, std, ostd= x.Metrics().MeanMaxRPS()
        B.append(BProb)
        M.append(MProb)
        Mean.append(mean)
        Std.append(std)
        OStd.append(ostd)
MeanMaxGridSearch = pd.DataFrame({"Life Rate": B, "Death Rate": M, "Population": Mean, "Std": Std, "Overall Std": OStd})
print(MeanMaxGridSearch.head())
MeanMaxGridSearch.to_csv("PopulationRateGrid.csv")
