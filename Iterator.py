from Grid import Grid;
import pandas as pd;
import time;
import pickle as pk
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from matplotlib import colors
from time import sleep
import numpy as np
import random
import string
#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time


class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps):
        #Take all of Grid's methods and attributes:
        super().__init__(Dimension) 

        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps

    def GetNumberOfSteps(self):
        return self.Iterations

    def Run(self, SaveData = False, animate = True):
        
        if SaveData == True:
            AllData = []


        if animate == True:
            fig, ax = plt.subplots(figsize = (5,5))
            colormap = colors.ListedColormap(["red", "green", "blue"])
            ims = []
        
        for i in range(0, self.Iterations):
            self.CheckAllWinners()
            #i as an argument to add timed decay
            self.UpdateAllDists(i)
            self.UpdateAllMoves()
            AgentData = self.ListToArray()
            if animate == True:
                im = ax.imshow(AgentData, cmap=colormap, animated = True)
                ims.append([im])
            if SaveData == True:
                IterAgentData = self.ListToArray()
                # NEW METRICS GO HERE
                N = np.zeros(3)
                for k in range(3): # find how many RPS at each timestep
                    N[k] = np.count_nonzero(AgentData == k-1)
                IterData = [IterAgentData, N] #ADD NEW METRICS TO LIST
                AllData.append(IterData)
                
        if animate == True:
            animation = ani.ArtistAnimation(
                fig, ims, interval=500, 
                blit=True,repeat_delay=2000
                )
            plt.show()

        if SaveData == True:
            NoIters = self.GetNumberOfSteps()
            Dims = self.GetDimension()
            #no iterations + dimensions + random string .pkl
            letters = string.ascii_lowercase
            Filename = 'pkl/'+str(NoIters)+'_'+str(Dims)+'_'+''.join(random.choice(letters) for i in range(3))+'.pkl'
            pickle_out = open(Filename, 'wb')
            pk.dump(AllData, pickle_out)
            pickle_out.close()

    # All Agents make a new move
    def UpdateAllMoves(self):
        for i in range(0, len(self.Agents)):
            self.Agents[i].MakeAMove()
        return self.Agents

    # Use scores to adjust each individual Agent's distribution
    def UpdateAllDists(self,TimeStep):
        for i in range(0, len(self.Agents)):
            RecentScore = self.Agents[i].GetRecentScore()
            TotalScore = self.Agents[i].GetTotalScore()
            RecentMove = self.Agents[i].GetMove()
            

            # RPStoOIX = {
            #     "R" : "O",
            #     "P" : "I",
            #     "S" : "X",
            # }
            # RecentMove = RPStoOIX.get(RecentMove)

            ### CREATE FUNCTION HERE
            # Some Function using Score and recent move to change distribution

            NewDist = [1/3, 1/3, 1/3]
            ###

            self.Agents[i].ChangeDist(NewDist)



#Example of 5 iterations and then replotting grid:
x=Iterator(5,40)
x.VisualiseGrid()
x.CheckAllWinners()
sum(x.CheckAllWinners()) # will this always be 0?
x.Run(animate = False, SaveData=False)
time.sleep(3)
x.VisualiseGrid()

