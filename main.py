from Grid import Grid
from Iterator import Iterator
import time


x = Iterator(100,10, Ternary = True)
x.VisualiseGrid()
x.CheckAllWinners()
sum(x.CheckAllWinners()) #will this always be 0? - yes
x.Run(animate = False, SaveData=False, KillOrBeKilledAndLearn = True)
time.sleep(3)
x.VisualiseGrid()