import matplotlib.pyplot as plt;
from matplotlib import colors;
from Agent import Agent;
import numpy as np;
import random

class Grid:

    #Initialise Instance Of Grid:
    # Rock = Red = -1
    # Paper = Green = 0
    # Scissors = Blue = 1
    # List of Objects (Agent Instances)
    #Dimension is Width of Grid

    def __init__(self, Dimension, EmptyCellCount = 0, Uniform = False, Ternary = False):
        '''
        EmptyCellCount: (int) number of empty cells
        '''

        self.Dimension = Dimension
        self.KeyMapping = {"R": -1, "P": 0, "S": 1}
        self.colormap = ["red", "green", "blue"]
        #forms a list of Agent instances
        AgentList = [] 

        for i in range(0,self.Dimension**2):
            AgentList.append(Agent(i, Uniform = Uniform, Ternary=Ternary))

        ###EmptyCells###
        if isinstance(EmptyCellCount, int) == False:
            raise ValueError("Empty cells must be int!")

        if EmptyCellCount !=0:
            EmptyCellLocs = random.sample(range(0, self.Dimension**2), EmptyCellCount)
            for i in range(EmptyCellCount):
                AgentList[EmptyCellLocs[i]] = None
                #also update colormap if there are emptycells
                self.KeyMapping = {"R": -1, "P": 0, "S": 1, "E": 2}
                self.colormap = ["red", "green", "blue", "white"]

        self.Agents = AgentList

    def GetDimension(self):
        return self.Dimension
    #Converter Purely for Visuals of Grid

    def ListToArray(self):
        Array = []
        for i in range(0, self.Dimension):
            ArrayFile = []
            for j in range(0, self.Dimension):
                if self.Agents[self.Dimension * i + j] is None:
                    ArrayFile.append(2)
                    continue
                ArrayElement = self.Agents[self.Dimension * i + j].GetMove()
                ArrayFile.append(self.KeyMapping[ArrayElement])
            Array.append(ArrayFile)

        return np.array(Array)

    #Visualises Grid

    def VisualiseGrid(self):
        colormap = colors.ListedColormap(self.colormap)
        plt.figure(figsize=(5, 5))
        plt.imshow(self.ListToArray(), cmap=colormap)
        plt.show()

    def GetAgents(self):
        return self.Agents


    # Checks Winner of Invididual Round

    def CheckWinner(self,IndexA,IndexB):

        if self.Agents[IndexA] is None or self.Agents[IndexB] is None:
            return 0

        Outcomes ={
            "RR" :  0, "RP" : -1, "RS" :  1,
            "PR" :  1, "PP" :  0, "PS" : -1,
            "SR" : -1, "SP" :  1, "SS" :  0,
        }

        Move = self.Agents[IndexA].GetMove()+self.Agents[IndexB].GetMove()
        ValueFromDict = Outcomes.get(Move)
        return ValueFromDict

        

    # Iterates through board finding total score from non-diagonal neighbours
    # If statements are to check different edge cases, now made to have equal opponents to central agents
    # Scores now encoded into individual Agents but for debugging / storage also outputs list of...
    # ...scores in same order as agents in self.Agents

    def CheckAllWinners(self):

        ScoreList = []

        TopLeftCorner = 0
        TopRightCorner = self.Dimension - 1
        BottomLeftCorner = self.Dimension ** 2 - self.Dimension
        BottomRightCorner = self.Dimension ** 2 - 1
        TopSide = [i for i in range(1, self.Dimension-1)]
        BottomSide = [self.Dimension ** 2 - self.Dimension + i for i in range(1, self.Dimension-1)]
        LeftSide = [self.Dimension * i for i in range(1, self.Dimension-1)]
        RightSide = [self.Dimension - 1 + self.Dimension * i for i in range(1, self.Dimension-1)]

        for Index in range(0, self.Dimension**2):

            Score = 0

            if Index == TopLeftCorner:
                Opponents = [1, LeftSide[0], TopRightCorner, BottomLeftCorner]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index == TopRightCorner:
                Opponents = [Index - 1, RightSide[0], TopLeftCorner, BottomRightCorner]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index == BottomLeftCorner:
                Opponents = [Index+1, LeftSide[-1], BottomRightCorner, TopLeftCorner]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index == BottomRightCorner:
                Opponents = [Index-1, RightSide[-1], BottomLeftCorner, TopRightCorner]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in TopSide:
                Opponents = [Index-1, Index+self.Dimension, Index+1, Index + (self.Dimension**2-self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in BottomSide:
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index - (self.Dimension ** 2 - self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in LeftSide:
                Opponents = [Index - 1 + self.Dimension, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in RightSide:
                Opponents = [Index - 1, Index - self.Dimension, Index - self.Dimension + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            else:
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            if self.Agents[Index] is None:
                # just adds 0 to this agent
                ScoreList.append(Score)
            else:
                self.Agents[Index].ChangeScore(Score)
                ScoreList.append(Score)

        ScoreArray = np.reshape(ScoreList, (self.Dimension,self.Dimension)) # to make analysis a little easier
        return ScoreList, ScoreArray

    def CheckAroundAgent(self, index):
        pass



    def UpdateSomePositions(self, AgentData, ScoreArray):
        #ScoreArray[:,1][(5)%5]
        pass




#Example Script for debugging -> sum of score list should be 0 (net zero game)
#P.S. comment out before running Iterator

# x=Grid(3)
# print(x.Dimension)
# x.VisualiseGrid()
# print(x.CheckAllWinners())
# print(sum(x.CheckAllWinners()))
