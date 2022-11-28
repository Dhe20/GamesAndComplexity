from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import random
x = Iterator(10, 20, Ternary = False, Seed = 0)


x.Run(LifeAndDeath=True)

x.Metrics().AnimateEvolution(1000)

# x.VisualiseGrid()
# #x.Metrics().PlotRPSAmount()
# # # x.Metrics().PlotNormRPSAmount()
# # x.Metrics().PlotPeriodicity(cutoff = 100)
# # Eval.PlotSimilarity()
# # Eval.PlotRPSAmount()




