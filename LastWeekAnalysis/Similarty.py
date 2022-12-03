#redirect to main directory
import sys
sys.path.append('./')
from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;
import numpy as np
import pickle

x = Iterator(300, 1000, Ternary = True)#, EmptyCellCount= 150)
x.EmptyGrid()# x.AddAgent('R',[0,1])
# x.AddAgent('R',[1,2])
# x.AddAgent('R',[2,1])
x.AddAgent('R',[0,0])
x.VisualiseGrid()
x.CountAgents()
#x.Run(LifeAndDeath=True, SaveData=False)
#x.RunUntilConvergence(LifeAndDeath=True)
#x.Metrics().AnimateEvolution(20)
x.VisualiseGrid()


'''similarity analysis'''
x.Metrics().PlotRPSAmount()
# x.Metrics().PlotNormRPSAmount()
x.Metrics().PlotPeriodicity(cutoff = 100)
Eval.PlotSimilarity()
Eval.PlotRPSAmount()

