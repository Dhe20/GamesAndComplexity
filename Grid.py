import matplotlib.pyplot as plt;
from matplotlib import colors;
from Agent import Agent;


class Grid:
    def __init__(self, Dimension):
        self.KeyMapping = {"R": -1, "P": 0, "S": 1}
        self.Dimension = Dimension
        AgentList = []
        for i in range(0,self.Dimension**2):
            AgentList.append(Agent(i))
        self.Agents = AgentList

    def ListToArray(self):
        Array = []
        for i in range(0, self.Dimension):
            ArrayFile = []
            for j in range(0, self.Dimension):
                ArrayElement = self.Agents[self.Dimension * i + j].GetMove()
                ArrayFile.append(self.KeyMapping[ArrayElement])
            Array.append(ArrayFile)
        return Array

    def VisualiseGrid(self):
        colormap = colors.ListedColormap(["red", "green", "blue"])
        plt.figure(figsize=(5, 5))
        plt.imshow(self.ListToArray(), cmap=colormap)
        plt.show()


    def GetAgents(self):
        return self.Agents

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
                return Score

            elif Index == TopRightCorner:
                Opponents = [1, RightSide[0], TopRightCorner, BottomLeftCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            elif Index == BottomLeftCorner:
                Opponents = [1, LeftSide[-1], BottomRightCorner, TopLeftCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            elif Index == BottomRightCorner:
                Opponents = [1, RightSide[-1], BottomLeftCorner, TopRightCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            elif Index in TopSide:
                Score = 0
                Opponents = [Index-1, Index+self.Dimension, Index+1, Index + (self.Dimension**2-self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            elif Index in BottomSide:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index - (self.Dimension ** 2 - self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            elif Index in LeftSide:
                Score = 0
                Opponents = [Index - 1 + self.Dimension, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            elif Index in RightSide:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index - self.Dimension + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            else:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckWinner(Index, Opponent)
                return Score

            ScoreList.append(Score)

        return self.Dimension



x=Grid(3)
print(x.Dimension)
x.VisualiseGrid()
print(x.CheckAllWinners())