from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
import pandas as pd




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


##


# TimeDict = {}

# for i in range(1,20+1):
#     GridSizeTimes = []
#     for j in range(0,10):
#         st = time.time()
#         x = Iterator(i*10, 10, Ternary=False, Seed=10*i + j)
#         x.Run(LifeAndDeath=True)
#         # x.VisualiseGrid()
#         et = time.time()
#         elapsed_time = et - st
#         GridSizeTimes.append(elapsed_time/10)
#     TimeDict.update({str(10*i): GridSizeTimes})
#
# Times = pd.DataFrame.from_dict(TimeDict)
# Times.to_csv("TimeComplexity.csv")
# print(Times.head())
# print(Times.mean().values)
# print(Times.std().values)
# plt.errorbar(Times.columns,Times.mean().values, yerr = Times.std().values)
# plt.show()

##


# TimeDict = {}

# for i in range(1,20+1):
#     GridSizeTimes = []
#     for j in range(0,10):
#         st = time.time()
#         x = Iterator(i*10, 10, Ternary=False, Seed=10*i + j)
#         x.Run(LifeAndDeath=True)
#         # x.VisualiseGrid()
#         et = time.time()
#         elapsed_time = et - st
#         GridSizeTimes.append(elapsed_time/10)
#     TimeDict.update({str(10*i): GridSizeTimes})
#
# Times = pd.DataFrame.from_dict(TimeDict)
# Times.to_csv("TimeComplexity.csv")
# print(Times.head())
# print(Times.mean().values)
# print(Times.std().values)
# plt.errorbar(Times.columns,Times.mean().values, yerr = Times.std().values)
# plt.show()
