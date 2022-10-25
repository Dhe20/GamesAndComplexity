from Grid import Grid
from Iterator import Iterator
import matplotlib.pyplot as plt
import time;

x = Iterator(100,20, Ternary = True)
x.VisualiseGrid()
x.CheckAllWinners()
sum(x.CheckAllWinners()) #will this always be 0? - yes
x.Run(animate = False, SaveData=False, KillOrBeKilledAndLearn = True)
x.VisualiseGrid()

Dicts = x.GetIncest()
Total = [x['Total'] for x in Dicts]
Red = [x['R'] for x in Dicts]
Green = [x['P'] for x in Dicts]
Blue = [x['S'] for x in Dicts]

plt.plot(Total, color = "k")
plt.plot(Red, color = "red")
plt.plot(Green, color = "Green")
plt.plot(Blue, color = "Blue")

plt.show()