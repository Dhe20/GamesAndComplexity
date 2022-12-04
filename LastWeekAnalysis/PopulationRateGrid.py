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
N = 26
B = []
M = []
Mean = []
Std = []
OStd = []

for BProbPercent in tqdm(np.linspace(1, 25, N)):
    BProb = BProbPercent / 100
    for MProbPercent in np.linspace(1, 25, N):
        x = Iterator(27, 200, Ternary=True, Seed=0)
        MProb = MProbPercent/100
        x.Run(LifeAndDeath=True, BProb = BProb, MProb = MProb)

        mean, std, ostd= x.Metrics().MeanMaxRPS()

        B.append(BProb)
        M.append(MProb)
        Mean.append(mean)
        Std.append(std)
        OStd.append(ostd)

PopulationRateGrid = pd.DataFrame({"Life Rate": B, "Death Rate": M, "Population": Mean, "Std": Std, "Overall Std": OStd})
print(PopulationRateGrid.head())
PopulationRateGrid.to_csv("PopulationRateGrid.csv")


##Eval
from matplotlib import cm
from matplotlib.ticker import LinearLocator

PopulationRateGrid = pd.read_csv("../PopulationRateGrid.csv")
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = PopulationRateGrid['Life Rate']
Y = PopulationRateGrid['Death Rate']
# X, Y = np.meshgrid(X, Y)
Z = PopulationRateGrid['Population']
Zerr = PopulationRateGrid['Std']

# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel("Life Rate")
ax.set_ylabel("Death Rate")
ax.set_zlabel('Max Population')
plt.show()

##

from matplotlib import cm
from matplotlib.ticker import LinearLocator

PopulationRateGrid = pd.read_csv("../PopulationRateGrid.csv")
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = PopulationRateGrid['Life Rate']
Y = PopulationRateGrid['Death Rate']
# X, Y = np.meshgrid(X, Y)
Z = PopulationRateGrid['Overall Std']

# Plot the surface.
surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel("Life Rate")
ax.set_ylabel("Death Rate")
ax.set_zlabel('Standard Deviation')
plt.show()
##

ZBox = np.zeros([2,len(Z)])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
X = PopulationRateGrid['Life Rate']
Y = PopulationRateGrid['Death Rate']
# X, Y = np.meshgrid(X, Y)
for i, elem in enumerate(Z):
    ZBox[0,i] = elem + PopulationRateGrid["Std"].loc[i]
    ZBox[1,i] = elem - PopulationRateGrid["Std"].loc[i]



# Set an equal aspect ratio
# ax.set_aspect('equal')

plt.show()