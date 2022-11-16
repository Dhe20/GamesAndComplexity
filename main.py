from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(20, 40, Ternary = True)
x.EmptyGrid()
x.AddAgent('R', [10,10])
x.AddAgent('P', [0,0])
x.AddAgent('S', [19,19])
# x.VisualiseGrid()
x.Run(Murder=True)
#x.Run( Convert=True)
x.Metrics().AnimateEvolution(150)
#x.VisualiseGrid()
#x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()



