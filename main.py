from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(30, 100, Ternary = True)
x.VisualiseGrid()
x.Run(SaveData = False, Convert = False, KillOrBeKilledAndLearn=True, Murder = False)
x.Metrics().AnimateEvolution(100)
x.VisualiseGrid()
# x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



