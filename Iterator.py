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
from copy import deepcopy

#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time


class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps, Uniform = False, Ternary = False, EmptyCellCount=0):

        #Take all of Grid's methods and attributes:
        super().__init__(
                        Dimension = Dimension, EmptyCellCount = EmptyCellCount,
                         Uniform = Uniform, Ternary = Ternary)
        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps
        self.FileName = ""
        self.AlreadyRun = False 
        self.AllData = []

        FilenameData = [str(self.GetNumberOfSteps()),
                        str(self.GetDimension()),
                        ''.join(random.choice(string.ascii_lowercase) for i in range(5)), ]
        # create a local /pkl dir
        # pkl/NoIterations_GridSize_5letterstring.pkl
        self.Filename = "pkl/" + FilenameData[0] + '_' + FilenameData[1] + '_' + FilenameData[-1] + '.pkl'

    def GetNumberOfSteps(self):
        return self.Iterations

    def Run(self, 
    SaveData = False, KillOrBeKilled = False, 
    KillOrBeKilledAndLearn = False, Convert = False,
        Murder = False):

        # save data

        for i in tqdm(range(0, self.Iterations)):

            localcopy = copy.deepcopy(self.Agents)
            self.AllData.append(localcopy)
            self.CheckAllWinners()
            #i as an argument to add timed decay
            self.UpdateAllDists(i, KillOrBeKilled = KillOrBeKilled, KillOrBeKilledAndLearn = KillOrBeKilledAndLearn, Murder = Murder,Convert = Convert)
            self.UpdateAllMoves()
            #self.UpdateSomePositions(self.ListToArray(), ScoreArray)#for dying away and moving

        if SaveData:
            self.SaveData()

    def SaveData(self):
        print('saved at ', self.Filename)
        pickle_out = open(self.Filename, 'wb')
        pk.dump(self.AllData, pickle_out)
        pickle_out.close()
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
    def UpdateAllDists(self, TimeStep, KillOrBeKilled = False, KillOrBeKilledAndLearn = False, Convert = False, Murder = False):
        for j in range(0, self.Dimension): #changed this loop to make it easier to convert adj cell
            for i in range(self.Dimension):
                k = self.Dimension*j+i
                if self.NextAgents[k] is None:
                    continue

                RecentScore = self.NextAgents[k].GetRecentScore()
                TotalScore = self.NextAgents[k].GetTotalScore()
                RecentMove = self.NextAgents[k].GetMove()

                if Murder:
                    NewDist = self.Murder(k, RecentScore, TotalScore, RecentMove)

                elif KillOrBeKilled:
                    NewDist = self.KillOrBeKilled(k, RecentScore, TotalScore, RecentMove)

                elif KillOrBeKilledAndLearn:
                    NewDist = self.KillOrBeKilledAndLearn(k, RecentScore, TotalScore, RecentMove)

                else:
                    NewDist = self.Agents[k].GetProbabilityDist()

                if self.NextAgents[k] is not None:
                    self.NextAgents[k].ChangeDist(NewDist)

                #may have to do this in another loop
                if Convert:
                    self.ConvertEmptyCell(j,i)

        self.Agents = deepcopy(self.NextAgents)
        self.AgentsGrid = deepcopy(self.NextAgentsGrid)
           


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

    def Murder(self, k, RecentScore, TotalScore, RecentMove):
        if RecentScore < 0:
            DeathProb = 0.1*abs(RecentScore)
            Dead = random.choices([True, False], weights=[DeathProb, 1 - DeathProb])[0]
            if Dead:
                self.NextAgents[k] = None
                self.NextAgentsGrid = np.array(self.NextAgents).reshape(self.Dimension, self.Dimension)
                NewDist = None
            else:
                NewDist = self.NextAgents[k].GetProbabilityDist()
        else: NewDist = self.NextAgents[k].GetProbabilityDist()
        return NewDist

    def ConvertEmptyCell(self, j,i, Prob = 0.5):
        '''
        Prob - probability of conversion
        '''

        D = self.Dimension
        OppLoc = [ # i <3 modular arithmetic
                    ((j)%D, (i+1)%D),
                    ((j+1)%D, (i)%D),
                    ((j)%D, (i-1)%D),
                    ((j-1)%D, (i)%D),
                    ] #equivalent of a dictionary

        for k in range(len(OppLoc)):
            if self.AgentsGrid[OppLoc[k]] is None:
                Outcome = random.choices([0,1], weights = [Prob, 1-Prob])[0]
                if Outcome == 1:
                    continue
                elif Outcome == 0:
                    AgentCopy = copy.deepcopy(self.AgentsGrid[j,i])
                    self.AgentsGrid[OppLoc[k]] = AgentCopy
                    self.Agents = self.AgentsGrid.flatten().tolist()
        
    


    
    def Metrics(self):
        return Metrics(AgentList = self.AllData, Iterator = True)


