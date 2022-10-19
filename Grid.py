import matplotlib.pyplot as plt;
from matplotlib import colors;
from Agent import Agent;
import numpy as np

class Grid:

    #Initialise Instance Of Grid:
    # Rock = Red = -1
    # Paper = Green = 0
    # Scissors = Blue = 1
    # List of Objects (Agent Instances)
    #Dimension is Width of Grid

    def __init__(self, Dimension):
        self.KeyMapping = {"R": -1, "P": 0, "S": 1}
        self.Dimension = Dimension
        #forms a list of Agent instances
        AgentList = [] 
        for i in range(0,self.Dimension**2):
            AgentList.append(Agent(i))
        self.Agents = AgentList

    def GetDimension(self):
        return self.Dimension
    #Converter Purely for Visuals of Grid

    def ListToArray(self):
        Array = []
        for i in range(0, self.Dimension):
            ArrayFile = []
            for j in range(0, self.Dimension):
                ArrayElement = self.Agents[self.Dimension * i + j].GetMove()
                ArrayFile.append(self.KeyMapping[ArrayElement])
            Array.append(ArrayFile)

        return np.array(Array)

    #Visualises Grid

    def VisualiseGrid(self):
        colormap = colors.ListedColormap(["red", "green", "blue"])
        plt.figure(figsize=(5, 5))
        plt.imshow(self.ListToArray(), cmap=colormap)
        plt.show()

    def GetAgents(self):
        return self.Agents


    # Checks Winner of Invididual Round

    def CheckWinner(self,IndexA,IndexB):
        if self.Agents[IndexA].GetMove() == "P":
            if self.Agents[IndexB].GetMove() == "R":
                return 1
            if self.Agents[IndexB].GetMove() == "P":
                return 0
            if self.Agents[IndexB].GetMove() == "S":
                return -1
        if self.Agents[IndexA].GetMove() == "R":
            if self.Agents[IndexB].GetMove() == "R":
                return 0
            if self.Agents[IndexB].GetMove() == "P":
                return -1
            if self.Agents[IndexB].GetMove() == "S":
                return 1
        if self.Agents[IndexA].GetMove() == "S":
            if self.Agents[IndexB].GetMove() == "R":
                return -1
            if self.Agents[IndexB].GetMove() == "P":
                return 1
            if self.Agents[IndexB].GetMove() == "S":
                return 0


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

            if Index == TopLeftCorner:
                Opponents = [1, LeftSide[0], TopRightCorner, BottomLeftCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index == TopRightCorner:
                Opponents = [Index - 1, RightSide[0], TopLeftCorner, BottomRightCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index == BottomLeftCorner:
                Opponents = [Index+1, LeftSide[-1], BottomRightCorner, TopLeftCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)


            elif Index == BottomRightCorner:
                Opponents = [Index-1, RightSide[-1], BottomLeftCorner, TopRightCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in TopSide:
                Score = 0
                Opponents = [Index-1, Index+self.Dimension, Index+1, Index + (self.Dimension**2-self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in BottomSide:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index - (self.Dimension ** 2 - self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in LeftSide:
                Score = 0
                Opponents = [Index - 1 + self.Dimension, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            elif Index in RightSide:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index - self.Dimension + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            else:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)

            self.Agents[Index].ChangeScore(Score)
            ScoreList.append(Score)

        return ScoreList





#Example Script for debugging -> sum of score list should be 0 (net zero game)
#P.S. comment out before running Iterator

# x=Grid(3)
# print(x.Dimension)
# x.VisualiseGrid()
# print(x.CheckAllWinners())
# print(sum(x.CheckAllWinners()))
