from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(30, 100, Ternary = True)
x.ThreeWideRows()
x.VisualiseGrid()
x.Run(SaveData = False, KillOrBeKilledAndLearn = True)
x.Metrics().AnimateEvolution(10)
# x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)

# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



