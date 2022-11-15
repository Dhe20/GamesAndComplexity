from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(6, 2, Ternary = True)
x.ThreeWideRows()
x.VisualiseGrid()
x.Run(SaveData = False, Convert = False, KillOrBeKilledAndLearn=False, Murder = True)
# x.Metrics().AnimateEvolution(500)
x.VisualiseGrid()
# x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



