from fileinput import filename
import matplotlib.pyplot as plt
import pickle
import numpy as np
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from matplotlib import colors

from Agent import Agent
from Grid import Grid

class Metrics: #inherits methods 
        #weird boilerplate to inherit class variables ...
    def __init__(self, Filename):

        if Filename[-4:] != ".pkl":
            raise ValueError(".pkl only pls")
        self.filename = Filename
        
        #reading data
        pickle_in = open(Filename, 'rb')
        self.AgentList = pickle.load(pickle_in)

        self.AgentArray = np.array(self.AgentList)
        self.NoIters = len(self.AgentArray)
        self.NoAgents = len(self.AgentArray.T)#take the transpose
        self.Dimension = int(np.sqrt(self.NoAgents))

        if None in self.AgentArray: #no need for == True is funny
            self.KeyMapping = {"R": -1, "P": 0, "S": 1, "E": 2}
            self.colorlist = ["red", "green", "blue", "white"]
        else:
            self.KeyMapping = {"R": -1, "P": 0, "S": 1}
            self.colorlist = ["red", "green", "blue"]
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
        for j in range(self.NoIters):
            for i in range(self.NoAgents):
                if self.AgentArray[j][i] is None:
                    continue
                Move = self.AgentArray[j][i].GetMove()
                N[self.KeyMapping.get(Move)][j] += 1

        ax.plot(tsteps, N[0], color = 'red', label = 'Rock')
        ax.plot(tsteps, N[1] , color = 'green', label = 'Paper')
        ax.plot(tsteps, N[2] , color = 'blue', label = 'Scissors')
        ax.plot(tsteps, N[0]+N[1]+N[2] , color = 'black', label = 'Total')
        ax.legend(title = '', prop={'size': 8})
        #plt.savefig('.png', dpi = 600)
        plt.show()

    def ListToArrayMetrics(self, AgentIteration):
        Array = []
        for i in range(0, self.Dimension):
            ArrayFile = []
            for j in range(0, self.Dimension):
                if AgentIteration[self.Dimension * i + j] is None:
                    ArrayFile.append(2)
                    continue
                ArrayElement = AgentIteration[self.Dimension * i + j].GetMove()
                ArrayFile.append(self.KeyMapping[ArrayElement])
            Array.append(ArrayFile)
        # make a matrix
        Array = np.array(Array).reshape((self.Dimension,self.Dimension))
        return Array


    def AnimateEvolution(self):
        #WIP 
        fig, ax = plt.subplots(figsize = (5,5))
        colormap = colors.ListedColormap(self.colorlist)
        ims = []
        #MoveDict = {"R": -1, "P": 1, "S": 2, "E": 3} self.movedict
        Grid = np.zeros(self.NoAgents)
        for i in range(self.NoIters):
            AgentData = self.ListToArrayMetrics(self.AgentArray[i])
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

x = Metrics('pkl/20_3_ewgwz.pkl')
x.PlotRPSAmount()
x.AnimateEvolution()