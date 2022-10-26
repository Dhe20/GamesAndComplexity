from Grid import Grid
from Iterator import Iterator
from Metrics import Metrics
import matplotlib.pyplot as plt
import time;

x = Iterator(10,20, Ternary = True)
x.Run(SaveData=True, KillOrBeKilledAndLearn = True)
Eval = Metrics(x.GetFileName())
Eval.AnimateEvolution(50)



