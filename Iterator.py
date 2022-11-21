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
from Agent import Agent

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
    KillOrBeKilledAndLearn = False, Birth = False,
    Murder = False, LifeAndDeath = False):

        # save data

        for i in tqdm(range(0, self.Iterations)):

            localcopy = copy.deepcopy(self.Agents)
            self.AllData.append(localcopy)
            self.CheckAllWinners()
            #i as an argument to add timed decay
            self.UpdateAllDists(i, KillOrBeKilled = KillOrBeKilled, KillOrBeKilledAndLearn = KillOrBeKilledAndLearn)
            #self.UpdateSomePositions(self.ListToArray(), ScoreArray)#for dying away and moving
            if Murder:
                self.Murder()
            localcopy = copy.deepcopy(self.Agents)
            self.AllData.append(localcopy)
            if Birth:
                self.BirthCells()
            if LifeAndDeath:
                self.LifeAndDeath()
            self.UpdateAllMoves()
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
        self.UpdateNextAgents()
        return self.Agents


    # Use scores to adjust each individual Agent's distribution
    def UpdateAllDists(self, TimeStep, KillOrBeKilled = False, KillOrBeKilledAndLearn = False):
        for i in range(0, self.Dimension**2): #changed this loop to make it easier to convert adj cell

            i
            if self.Agents[i] is None:
                continue

            RecentScore = self.Agents[i].GetRecentScore()
            TotalScore = self.Agents[i].GetTotalScore()
            RecentMove = self.Agents[i].GetMove()


            if KillOrBeKilled:
                NewDist = self.KillOrBeKilled(i, RecentScore, TotalScore, RecentMove)

            elif KillOrBeKilledAndLearn:
                NewDist = self.KillOrBeKilledAndLearn(i, RecentScore, TotalScore, RecentMove)

            else:
                NewDist = self.Agents[i].GetProbabilityDist()

            if self.Agents[i] is not None:
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

    def Murder(self, Prob = 0.1):


        #construct probability matrix for death and survival
        D = self.Dimension
        ProbabilityMatrix = np.zeros((D,D), dtype = object)
        for j in range(D):
            for i in range(D):
                if self.AgentsGrid[j,i] is not None:
                    AgentRecentScore = self.AgentsGrid[j,i].GetRecentScore()
                    if AgentRecentScore < 0:
                        DeathProb = Prob*abs(AgentRecentScore) 
                        ProbabilityMatrix[j,i] = np.array([DeathProb,1-DeathProb], dtype= float)
                        continue
                    ProbabilityMatrix[j,i] = np.array([0,1], dtype = float) # possible to avoid writing this twice?
                ProbabilityMatrix[j,i] = np.array([0,1], dtype = float)
        #execute probability matrix
        for j in range(D):
            for i in range(D):
                Dead = random.choices([True,False], weights = ProbabilityMatrix[j,i])[0]
                if Dead:
                    self.AgentsGrid[j,i] = None
        self.Agents = self.AgentsGrid.flatten().tolist()



        # if RecentScore < 0:
        #     DeathProb = 0.1*abs(RecentScore)
        #     Dead = random.choices([True, False], weights=[DeathProb, 1 - DeathProb])[0]
        #     if Dead:
        #         self.AgentsGrid[j]
        #         # self.Agents[k] = None
        #         # self.NextAgentsGrid = np.array(self.Agents).reshape(self.Dimension, self.Dimension)
        #     else:
        #         NewDist = self.Agents[k].GetProbabilityDist()
        # else: NewDist = self.Agents[k].GetProbabilityDist()
        # return NewDist

    def BirthCells(self, Prob = 0.25):
        D = self.Dimension
        #define probabilities (arrays for easy addition)
        ConversionProbDict = {
            "R" : np.array([Prob,0,0]),
            "P" : np.array([0,Prob,0]),
            "S" : np.array([0,0,Prob]),
        }

        BirthedProbDict = {
            "R" : [1,0,0],
            "P" : [0,1,0],
            "S" : [0,0,1],
        }

        #construct probability matrix
        ProbabilityMatrix = np.zeros((D,D), dtype = object)
        for j in range(D):
            for i in range(D):
                ProbabilityMatrix[j,i] = np.array([0,0,0], dtype= float)
                if self.AgentsGrid[j,i] is not None:
                    ProbabilityMatrix[j,i] = np.append(ProbabilityMatrix[j,i], 1-sum(ProbabilityMatrix[j,i]))
                    continue
                OppLoc = [ # i <3 modular arithmetic
                            ((j)%D, (i+1)%D),
                            ((j+1)%D, (i)%D),
                            ((j)%D, (i-1)%D),
                            ((j-1)%D, (i)%D),
                            ] #equivalent of a dictionary
                for k in range(len(OppLoc)):
                    if self.AgentsGrid[OppLoc[k]] is None:
                            continue
                    AgentType = self.AgentsGrid[OppLoc[k]].GetMove()
                    ProbabilityMatrix[j,i] = ProbabilityMatrix[j,i] + ConversionProbDict.get(AgentType)
                ProbabilityMatrix[j,i] = np.append(ProbabilityMatrix[j,i], 1-sum(ProbabilityMatrix[j,i])) #append on the 'do nothing' probabilty
        #loop through agentsgrid apply conversion probabilities (give birth)
        for j in range(D):
            for i in range(D):
                Outcome = random.choices(['R','P','S', None], weights = ProbabilityMatrix[j,i])[0]
                if Outcome is None:
                    continue
                Probs = BirthedProbDict.get(Outcome)
                self.AgentsGrid[j,i] = Agent(index = D*j+i, Probs=Probs)
        self.Agents = self.AgentsGrid.flatten().tolist()
    

    def LifeAndDeath(self, ProbLife = 0.25, ProbDeathSingle = 0.25):
        # combining the identical method for probabilities
        D = self.Dimension
        #define probabilities
        ConversionProbDict = {
            "R" : np.array([ProbLife,0,0,0]), #
            "P" : np.array([0,ProbLife,0,0]), # last 0 because there is 0 probability of death
            "S" : np.array([0,0,ProbLife,0]), #
        }
        #define input for RPS
        OutcomeDict = {
            "R" : [1,0,0],
            "P" : [0,1,0],
            "S" : [0,0,1],
        }
        #construct probability matrix. Each element is an array with:
        #[P(NoneToR),P(NoneToP),P(NoneToS), P(Death), P(DoNothing)]
        ProbabilityMatrix = np.zeros((D,D), dtype = object)
        for j in range(D):
            for i in range(D):
                #replace every zero with an array
                PMat = np.array([0,0,0,0], dtype = float)  #[P(NoneToR),P(NoneToP),P(NoneToS), P(Death)]
                #if not an empty cell, have a chance of dying
                if self.AgentsGrid[j,i] is not None:
                    AgentRecentScore = self.AgentsGrid[j,i].GetRecentScore()
                    if AgentRecentScore < 0:
                        ProbDeath = ProbDeathSingle*abs(AgentRecentScore)
                        PMat = np.array([0,0,0,ProbDeath], dtype = float)
                        PMat = np.append(PMat, 1-ProbDeath)#append P(DoNothing)
                    else:
                        PMat = np.append(PMat, 1)#append P(DoNothing) (nothing happens if score >0)
                    ProbabilityMatrix[j,i] = PMat
                    continue

                #if an empty cell, compute chances of conversion
                OppLoc = [ # i <3 modular arithmetic
                            ((j)%D, (i+1)%D),
                            ((j+1)%D, (i)%D),
                            ((j)%D, (i-1)%D),
                            ((j-1)%D, (i)%D),
                            ] #equivalent of a dictionary
                for k in range(len(OppLoc)):
                    if self.AgentsGrid[OppLoc[k]] is None:
                            continue
                    AgentType = self.AgentsGrid[OppLoc[k]].GetMove()
                    PMat = PMat + ConversionProbDict.get(AgentType)
                PMat = np.append(PMat, 1-sum(PMat)) #appending P(DoNothing)
                ProbabilityMatrix[j,i] = PMat

        #apply probabilities
        for j in range(D):
            for i in range(D):
                Outcome = random.choices(['R','P','S','D','N'], weights = ProbabilityMatrix[j,i])[0]
                if Outcome == 'N':
                    continue
                if Outcome == 'D':
                    self.AgentsGrid[j,i] = None
                    continue
                BirthedProb = OutcomeDict.get(Outcome)
                self.AgentsGrid[j,i] = Agent(index = D*j+i, Probs=BirthedProb)
        self.Agents = self.AgentsGrid.flatten().tolist()
    
    def Metrics(self):
        return Metrics(AgentList = self.AllData, Iterator = True)


    