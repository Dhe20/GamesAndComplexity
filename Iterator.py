from copy import copy
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
import copy
from Grid import Grid;
import pandas as pd;
import time
import pickle as pk;
import matplotlib.animation as ani;
import matplotlib.pyplot as plt;
from matplotlib import colors;
from time import sleep;
import numpy as np;
import random;
import string;
from random import choices;
from tqdm import tqdm
import pickle as pk
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from matplotlib import colors
from time import sleep
import numpy as np
import random
import string
import copy

#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time


class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps, Uniform = False, Ternary = False, EmptyCellCount=0):

        #Take all of Grid's methods and attributes:
        super().__init__(Dimension, Uniform = Uniform, Ternary=Ternary, EmptyCellCount)

        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps
        self.IncestMetre = []

    def GetNumberOfSteps(self):
        return self.Iterations

    def Run(self, SaveData = False, KillOrBeKilled = False, KillOrBeKilledAndLearn = False):
        
        if SaveData == True:
            AllData = []

        for i in tqdm(range(0, self.Iterations)):
            ScoreArray = self.CheckAllWinners()[1]
            self.CheckAllWinners()
            self.IncestMetre.append(self.Incest())
            #i as an argument to add timed decay
            self.UpdateAllDists(i, KillOrBeKilled = KillOrBeKilled, KillOrBeKilledAndLearn = KillOrBeKilledAndLearn)
            self.UpdateAllMoves()
            AgentData = self.ListToArray()
            self.UpdateSomePositions(AgentData, ScoreArray)#for dying away and moving

            #save data
            if SaveData == True:
                localcopy = copy.deepcopy(self.Agents)
                #print(localcopy[1].TotalScore)
                AllAgentGrids.append(localcopy)

        if SaveData == True:
            #add any other data to the filename here
            FilenameData = [str(self.GetNumberOfSteps()),
                            str(self.GetDimension()),
                            ''.join(random.choice(string.ascii_lowercase) for i in range(5)),]
            #create a local /pkl dir
            #pkl/NoIterations_GridSize_5letterstring.pkl
            Filename = 'pkl/'+FilenameData[0]+'_'+FilenameData[1]+'_'+FilenameData[-1]+'.pkl'
            print('saved at ', Filename)
            pickle_out = open(Filename, 'wb')
            pk.dump(AllAgentGrids, pickle_out)
            pickle_out.close()



    # All Agents make a new move
    def UpdateAllMoves(self):
        for i in range(0, len(self.Agents)):
            if self.Agents[i] is None:
                continue
            self.Agents[i].MakeAMove()
        return self.Agents

    def GetIncest(self):
        return self.IncestMetre

    # Use scores to adjust each individual Agent's distribution
    def UpdateAllDists(self, TimeStep, KillOrBeKilled = False, KillOrBeKilledAndLearn = False):
        for i in range(0, len(self.Agents)):
            if self.Agents[i] is None:
                continue

            RecentScore = self.Agents[i].GetRecentScore()
            TotalScore = self.Agents[i].GetTotalScore()
            RecentMove = self.Agents[i].GetMove()

            # RPStoOIX = {
            #     "R" : "O",
            #     "P" : "I",
            #     "S" : "X",
            # }
            # RecentMove = RPStoOIX.get(RecentMove)

            if KillOrBeKilled:
                NewDist = self.KillOrBeKilled(i, RecentScore, TotalScore, RecentMove)

            elif KillOrBeKilledAndLearn:
                NewDist = self.KillOrBeKilledAndLearn(i, RecentScore, TotalScore, RecentMove)

            else:
                NewDist = self.Agents[i].GetProbabilityDist()

            self.Agents[i].ChangeDist(NewDist)


    def KillOrBeKilled(self, i, RecentScore, TotalScore, RecentMove):
        if RecentScore < 0:
            NewDist = choices([[1, 0, 0], [0, 1, 0], [0, 0, 1]])[0]
        else:
            NewDist = self.Agents[i].GetProbabilityDist()
        return NewDist

    def KillOrBeKilledAndLearn(self, i, RecentScore, TotalScore, RecentMove):
        #Change Move according to what beat you:
        MoveShuffle = {"R": [0,1,0], "P": [0,0,1], "S": [1,0,0]}

        if RecentScore < 0:
            NewDist = MoveShuffle[RecentMove]
        else:
            NewDist = self.Agents[i].GetProbabilityDist()
        return NewDist

    def Incest(self):

        SimilarityDict = {"Total":[], "R":[], "P":[], "S":[]}

        TopLeftCorner = 0
        TopRightCorner = self.Dimension - 1
        BottomLeftCorner = self.Dimension ** 2 - self.Dimension
        BottomRightCorner = self.Dimension ** 2 - 1
        TopSide = [i for i in range(1, self.Dimension - 1)]
        BottomSide = [self.Dimension ** 2 - self.Dimension + i for i in range(1, self.Dimension - 1)]
        LeftSide = [self.Dimension * i for i in range(1, self.Dimension - 1)]
        RightSide = [self.Dimension - 1 + self.Dimension * i for i in range(1, self.Dimension - 1)]

        for Index in range(0, self.Dimension ** 2):

            if Index == TopLeftCorner:
                Opponents = [1, LeftSide[0], TopRightCorner, BottomLeftCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index == TopRightCorner:
                Opponents = [Index - 1, RightSide[0], TopLeftCorner, BottomRightCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index == BottomLeftCorner:
                Opponents = [Index + 1, LeftSide[-1], BottomRightCorner, TopLeftCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index == BottomRightCorner:
                Opponents = [Index - 1, RightSide[-1], BottomLeftCorner, TopRightCorner]
                Score = 0
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index in TopSide:
                Score = 0
                Opponents = [Index - 1, Index + self.Dimension, Index + 1,
                             Index + (self.Dimension ** 2 - self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index in BottomSide:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index + 1,
                             Index - (self.Dimension ** 2 - self.Dimension)]
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index in LeftSide:
                Score = 0
                Opponents = [Index - 1 + self.Dimension, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            elif Index in RightSide:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index - self.Dimension + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)

            else:
                Score = 0
                Opponents = [Index - 1, Index - self.Dimension, Index + 1, Index + self.Dimension]
                for Opponent in Opponents:
                    Score += self.CheckSimilar(Index, Opponent)


            SimilarityDict["Total"].append(Score)
            SimilarityDict[self.Agents[Index].GetMove()].append(Score)

        for key in SimilarityDict:
            SimilarityDict[key] = np.mean(SimilarityDict[key])/4

        return SimilarityDict



