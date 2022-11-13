from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(30, 100, Ternary = True)
x.EmptyGrid()
x.AddAgent('R', [15,15])
x.AddAgent('P', [3,4])
# x.AddAgent('S', [27,28])
# x.AddAgent('P')
# x.AddAgent('S')
x.VisualiseGrid()
x.Run(SaveData = False, Convert = True,KillOrBeKilledAndLearn=True)
x.Metrics().AnimateEvolution(100)
# x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)

# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



