from fileinput import filename
import matplotlib.pyplot as plt
# import matplotlib; matplotlib.use("TkAgg")
import pickle
import numpy as np
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.fft import fft, fftfreq

class Metrics: #inherits methods
        #weird boilerplate to inherit class variables ...
    def __init__(self, Filename = "", AgentList = None, Iterator = False):

        if Iterator:
            self.AgentList = AgentList
        else:
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
            self.KeyMapping = {"R": 0, "P": 1, "S": 2, "E": 3}
            self.colorlist = ["red", "green", "blue", "white"]
        else:
            self.KeyMapping = {"R": 0, "P": 1, "S": 2}
            self.colorlist = ["red", "green", "blue"]
        # dk what this is doing
        # AgentCount = self.AgentArray[0][1]
        # for i in range(len(data)-1):
        #     AgentCount = np.vstack((data[i+1][1], AgentCount))

    #rps -> rgb
    #make figure

    def GetArray(self):
        return self.AgentArray

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

    def PlotNormRPSAmount(self):
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.tick_params(labelsize=20)

        tsteps = np.linspace(0, self.NoIters, self.NoIters)  # is there a better way to do this?
        # need to change this to account for empty cells
        N = np.zeros((3, self.NoIters))
        for j in range(self.NoIters):
            for i in range(self.NoAgents):
                if self.AgentArray[j][i] is None:
                    continue
                Move = self.AgentArray[j][i].GetMove()
                N[self.KeyMapping.get(Move)][j] += 1

        N[0] = N[0] - np.mean(N[0])
        N[1] = N[1] - np.mean(N[1])
        N[2] = N[2] - np.mean(N[2])


        ax.plot(tsteps, N[0], color='red', label='Rock')
        ax.plot(tsteps, N[1], color='green', label='Paper')
        ax.plot(tsteps, N[2], color='blue', label='Scissors')
        ax.plot(tsteps, N[0] + N[1] + N[2], color='black', label='Total')
        ax.legend(title='', prop={'size': 8})
        # plt.savefig('.png', dpi = 600)
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


    def AnimateEvolution(self, intervalms=250):
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
            fig, ims, interval=intervalms,
            blit=True,repeat_delay=2000
            )
        plt.show()


        IterAgentData = self.ListToArrayMetrics(self.AgentArray[i])
        # NEW METRICS GO HERE
        N = np.zeros(3)
        for k in range(3): # find how many RPS at each timestep
            N[k] = np.count_nonzero(AgentData == k-1)
        IterData = [IterAgentData, N] #ADD NEW METRICS TO LIST

    def CheckSimilar(self, iter, IndexA, IndexB):
        if self.AgentArray[iter][IndexA] is None or self.AgentArray[iter][IndexB] is None:
            return 0

        Outcomes = {
            "RR": 1,
            "RP": 0,
            "RS": 0,
            "PR": 0,
            "PP": 1,
            "PS": 0,
            "SR": 0,
            "SP": 0,
            "SS": 1,
        }

        Move = self.AgentArray[iter][IndexA].GetMove() + self.AgentArray[iter][IndexB].GetMove()
        ValueFromDict = Outcomes.get(Move)
        return ValueFromDict

    def PlotPeriodicity(self, cutoff = 50):

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.tick_params(labelsize=20)

        tsteps = np.linspace(0, self.NoIters, self.NoIters)  # is there a better way to do this?
        # need to change this to account for empty cells
        N = np.zeros((3, self.NoIters))
        for j in range(cutoff,self.NoIters):
            for i in range(self.NoAgents):
                if self.AgentArray[j][i] is None:
                    continue
                Move = self.AgentArray[j][i].GetMove()
                N[self.KeyMapping.get(Move)][j] += 1


        #Slice final 20% of data for steady state periodicity

        SteadyStateSliceRock = N[0] - np.mean(N[0])
        SteadyStateSlicePaper = N[1] - np.mean(N[1])
        SteadyStateSliceScissors = N[2] - np.mean(N[2])

        #FFT Total, R, P, S

        N=len(SteadyStateSliceRock)
        yfRock = fft(SteadyStateSliceRock)
        yfPaper = fft(SteadyStateSlicePaper)
        yfScissors = fft(SteadyStateSliceScissors)

        xf = fftfreq(N, 1)[:N // 2]

        plt.plot(xf, (2.0 / N) * np.abs(yfRock[0:N // 2]), color='red', label='Rock', ls = "--")
        plt.plot(xf, (2.0 / N) * np.abs(yfPaper[0:N // 2]), color='green', label='Paper', ls = "dashdot")
        plt.plot(xf, (2.0 / N) * np.abs(yfScissors[0:N // 2]), color='blue', label='Scissors', ls = "dotted")
        plt.grid()
        ax.legend(title='', prop={'size': 8})
        # plt.savefig('.png', dpi = 600)
        plt.show()




        #Output plot of FFT


    def PlotSimilarity(self):

        TopLeftCorner = 0
        TopRightCorner = self.Dimension - 1
        BottomLeftCorner = self.Dimension ** 2 - self.Dimension
        BottomRightCorner = self.Dimension ** 2 - 1
        TopSide = [i for i in range(1, self.Dimension - 1)]
        BottomSide = [self.Dimension ** 2 - self.Dimension + i for i in range(1, self.Dimension - 1)]
        LeftSide = [self.Dimension * i for i in range(1, self.Dimension - 1)]
        RightSide = [self.Dimension - 1 + self.Dimension * i for i in range(1, self.Dimension - 1)]

        SimilarityOverTime = []

        for iter in range(0, self.NoIters):
            SimilarityDict = {"Total": [], "R": [], "P": [], "S": []}

            for Index in range(0, self.Dimension ** 2):
                if Index == TopLeftCorner:
                    Opponents = [1, LeftSide[0], TopRightCorner, BottomLeftCorner]
                    Score = 0
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index == TopRightCorner:
                    Opponents = [Index - 1, RightSide[0], TopLeftCorner, BottomRightCorner]
                    Score = 0
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index == BottomLeftCorner:
                    Opponents = [Index + 1, LeftSide[-1], BottomRightCorner, TopLeftCorner]
                    Score = 0
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index == BottomRightCorner:
                    Opponents = [Index - 1, RightSide[-1], BottomLeftCorner, TopRightCorner]
                    Score = 0
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index in TopSide:
                    Score = 0
                    Opponents = [Index - 1, Index + self.Dimension, Index + 1,
                                 Index + (self.Dimension ** 2 - self.Dimension)]
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index in BottomSide:
                    Score = 0
                    Opponents = [Index - 1, Index - self.Dimension, Index + 1,
                                 Index - (self.Dimension ** 2 - self.Dimension)]
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index in LeftSide:
                    Score = 0
                    Opponents = [Index - 1 + self.Dimension, Index - self.Dimension, Index + 1, Index + self.Dimension]
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                elif Index in RightSide:
                    Score = 0
                    Opponents = [Index - 1, Index - self.Dimension, Index - self.Dimension + 1, Index + self.Dimension]
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)

                else:
                    Score = 0
                    Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index + self.Dimension]
                    for Opponent in Opponents:
                        Score += self.CheckSimilar(iter, Index, Opponent)


                SimilarityDict["Total"].append(Score)
                if self.AgentArray[iter][Index] is None:
                    continue
                
                SimilarityDict[self.AgentArray[iter][Index].GetMove()].append(Score)

            for key in SimilarityDict:
                SimilarityDict[key] = np.mean(SimilarityDict[key])/4

            SimilarityOverTime.append(SimilarityDict)


        Total = [x['Total'] for x in SimilarityOverTime]
        Rock = [x['R'] for x in SimilarityOverTime]
        Paper = [x['P'] for x in SimilarityOverTime]
        Scissors = [x['S'] for x in SimilarityOverTime]

        plt.plot(Total, color="k")
        plt.plot(Rock, color="red")
        plt.plot(Paper, color="Green")
        plt.plot(Scissors, color="Blue")
        plt.show()

# x = Metrics('')
# x.PlotRPSAmount()
# x.PlotSimilarity()
# x.AnimateEvolution()