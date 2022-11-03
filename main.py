from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(20,100, Ternary = True)
# x.CreateEmptyRowCol(RoworCol="C", WhichRowCol= 0) # "R" or "C", then which one of the rows/cols
# x.CreateEmptyRowCol(RoworCol="R", WhichRowCol= 0)
x.CreateEmptyDiagonal(UporDown="D")
x.CreateEmptyDiagonal(UporDown="U")
x.VisualiseGrid()

x.Run(SaveData=True, KillOrBeKilledAndLearn = True)

Eval = Metrics(x.GetFileName())
Eval.AnimateEvolution(50)
Eval.PlotSimilarity()
Eval.PlotRPSAmount()

