from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(21, 1000, Ternary = True, EmptyCellCount= 150)
# x.EmptyGrid()
# x.AddAgent('R',[0,1])
# x.AddAgent('R',[1,2])
# x.AddAgent('R',[2,1])
# x.AddAgent('R',[1,0])
x.VisualiseGrid()
x.Run(LifeAndDeath=True, KillOrBeKilledAndLearn=True)
x.Metrics().AnimateEvolution(20)
x.VisualiseGrid()
#x.Metrics().PlotRPSAmount()
# # x.Metrics().PlotNormRPSAmount()
# x.Metrics().PlotPeriodicity(cutoff = 100)
# Eval.PlotSimilarity()
# Eval.PlotRPSAmount()

#



