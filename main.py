from Grid import Grid
from Iterator import Iterator
import time;

x = Iterator(20,100, Ternary = True)
x.VisualiseGrid()
x.CheckAllWinners()
sum(x.CheckAllWinners()) #will this always be 0? - yes
x.Run(animate = False, SaveData=False, KillOrBeKilledAndLearn = True)
x.VisualiseGrid()