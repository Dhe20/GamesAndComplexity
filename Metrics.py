from fileinput import filename
import matplotlib.pyplot as plt
import pickle
import numpy as np
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from matplotlib import colors

from Agent import Agent
# import Grid

class Metrics:
    def __init__(self, filename):
    
        if filename[-4:] != ".pkl":
            raise ValueError(".pkl only pls")
        self.filename = filename
        
        #reading data
        pickle_in = open(filename, 'rb')
        self.AgentList = pickle.load(pickle_in)

        self.AgentArray = np.array(self.AgentList)
        self.NoIters = len(self.AgentArray)
        self.NoAgents = len(self.AgentArray.T)#take the transpose

        # dk what this is doing
        # AgentCount = self.AgentArray[0][1]
        # for i in range(len(data)-1):
        #     AgentCount = np.vstack((data[i+1][1], AgentCount))

    #rps -> rgb
    #make figure
    def PlotRPSAmount(self):
        fig, ax = plt.subplots(1,1, figsize =(10,6))
        ax.tick_params(labelsize = 20)

        tsteps = np.linspace(0,self.NoIters, self.NoIters)#is there a better way to do this?
        #need to change this to account for empty cells
        N = np.zeros((3,self.NoIters))
        MoveDict = {"R": 0, "P": 1, "S": 2, "E": 3}
        for j in range(self.NoIters):
            for i in range(self.NoAgents):
                Move = self.AgentArray[j][i].GetMove()
                N[MoveDict.get(Move)][j] += 1


        ax.plot(tsteps, N[0], color = 'red', label = 'Rock')
        ax.plot(tsteps, N[1] , color = 'green', label = 'Paper')
        ax.plot(tsteps, N[2] , color = 'blue', label = 'Scissors')
        ax.plot(tsteps, N[0]+N[1]+N[2] , color = 'black', label = 'Total')
        ax.legend(title = '', prop={'size': 8})
        #plt.savefig('.png', dpi = 600)
        plt.show()

    def AnimateEvolution(self):
        #WIP 
        fig, ax = plt.subplots(figsize = (5,5))
        colormap = colors.ListedColormap(["red", "green", "blue", "white"])
        ims = []
        MoveDict = {"R": -1, "P": 1, "S": 2, "E": 3}
        Grid = np.zeros(self.NoAgents)
        for i in range(self.NoIters):
            AgentData = self.AgentArray[i]
            
            # Dim = int(np.sqrt(len(AgentData)))
            # AgentData = AgentData.reshape((Dim, Dim))

            im = ax.imshow(AgentData, cmap=colormap, animated = True)
            ims.append([im])

        animation = ani.ArtistAnimation(
            fig, ims, interval=250, 
            blit=True,repeat_delay=2000
            )
        plt.show()


        IterAgentData = self.ListToArray()
        # NEW METRICS GO HERE
        N = np.zeros(3)
        for k in range(3): # find how many RPS at each timestep
            N[k] = np.count_nonzero(AgentData == k-1)
        IterData = [IterAgentData, N] #ADD NEW METRICS TO LIST

x = Metrics('pkl/40_5_rqjpe.pkl')
x.PlotRPSAmount()
x.AnimateEvolution()