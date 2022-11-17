from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(21, 150, Ternary = True)#, EmptyCellCount= 150)

x.ThreeWideRows()
x.VisualiseGrid()
x.Run(Murder = True, Birth = True, KillOrBeKilled=True)
x.Metrics().AnimateEvolution(100)
x.VisualiseGrid()
#x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



