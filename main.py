from Grid import Gridfrom Iterator import Iteratorfrom Metrics import Metricsimport matplotlib.pyplot as pltimport time;x = Iterator(45, 200, Ternary = True)# x.ThreeWideRows()# x.VisualiseGrid()x.Run(SaveData = False, KillOrBeKilledAndLearn = True)x.Metrics().AnimateEvolution()x.Metrics().PlotRPSAmount()x.Metrics().PlotPerodicity(cutoff = 100)# Eval.PlotSimilarity()# Eval.PlotRPSAmount()