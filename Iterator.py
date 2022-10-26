from copy import copy
from Grid import Grid;
from random import choices;
from tqdm import tqdm
import pickle as pk
import numpy as np
import random
import string
import copy
from  Metrics import Metrics

#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time


class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps, Uniform = False, Ternary = False, EmptyCellCount=0):

        #Take all of Grid's methods and attributes:
        super().__init__(Dimension, EmptyCellCount, Uniform = Uniform, Ternary=Ternary)

        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps
        self.FileName = ""
        self.AlreadyRun = False

    def GetNumberOfSteps(self):
        return self.Iterations

    def Run(self, SaveData = False, KillOrBeKilled = False, KillOrBeKilledAndLearn = False):

        # save data
        if SaveData == True:
            AllData = []

        for i in tqdm(range(0, self.Iterations)):

            if SaveData == True:
                localcopy = copy.deepcopy(self.Agents)
                AllData.append(localcopy)


            ScoreArray = self.CheckAllWinners()[1]
            self.CheckAllWinners()
            #i as an argument to add timed decay
            self.UpdateAllDists(i, KillOrBeKilled = KillOrBeKilled, KillOrBeKilledAndLearn = KillOrBeKilledAndLearn)
            self.UpdateAllMoves()
            self.UpdateSomePositions(self.ListToArray(), ScoreArray)#for dying away and moving

        if SaveData == True:
            #add any other data to the filename here
            FilenameData = [str(self.GetNumberOfSteps()),
                            str(self.GetDimension()),
                            ''.join(random.choice(string.ascii_lowercase) for i in range(5)),]
            #create a local /pkl dir
            #pkl/NoIterations_GridSize_5letterstring.pkl
            Filename = "pkl/"+FilenameData[0]+'_'+FilenameData[1]+'_'+FilenameData[-1]+'.pkl'
            print('saved at ', Filename)
            pickle_out = open(Filename, 'wb')
            pk.dump(AllData, pickle_out)
            pickle_out.close()
            self.FileName = Filename
            self.AlreadyRun = True

    def GetFileName(self):
        return self.FileName

    # All Agents make a new move
    def UpdateAllMoves(self):
        for i in range(0, len(self.Agents)):
            if self.Agents[i] is None:
                continue
            self.Agents[i].MakeAMove()
        return self.Agents

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




