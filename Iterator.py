from copy import copy
from Grid import Grid;
import random
from tqdm import tqdm
import pickle as pk
import numpy as np
import random
import string
import copy
from  Metrics import Metrics
from copy import deepcopy
from Agent import Agent
import datetime
#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time


class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps, Uniform = False, Ternary = False,
                 EmptyCellCount=0, Seed=None, Probs = None, ProbsDist = None):

        #Take all of Grid's methods and attributes:
        super().__init__(
                        Dimension = Dimension, EmptyCellCount = EmptyCellCount,
                         Uniform = Uniform, Ternary = Ternary, Seed=Seed, Probs = Probs, ProbsDist = ProbsDist)
        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps
        self.FileName = ""
        self.AlreadyRun = False
        self.AllData = []
        self.Seed = Seed
        self.AllGrids = []

    def GetNumberOfSteps(self):
        return self.Iterations

    def Run(self,
    SaveData = False, KillOrBeKilled = False,
    KillOrBeKilledAndLearn = False, Birth = False,
    Murder = False, LifeAndDeath = False, UnoReverse = False,
    BProb = None, MProb = None, SaveGrids = False):

        if not BProb:
            BProb = 0.25
        if not MProb:
            MProb = 0.25

        if SaveGrids:
            Huge3DArray = np.zeros((self.Iterations,self.Dimension, self.Dimension),dtype=str)

        # for i in tqdm(range(0, self.Iterations)):
        for i in range(0, self.Iterations):
            
            if SaveData:
                localcopy = copy.deepcopy(self.Agents)
                self.AllData.append(localcopy)
            if SaveGrids:
                MoveArray = copy.deepcopy(self.GetMoveArray())
                Huge3DArray[i] = MoveArray

            self.CheckAllWinners()
            #i as an argument to add timed decay
            self.UpdateAllDists(i, KillOrBeKilled = KillOrBeKilled, KillOrBeKilledAndLearn = KillOrBeKilledAndLearn)

            if Murder:
                self.Murder(MProb = MProb)
            if Birth:
                self.BirthCells(BProb = BProb)
            if LifeAndDeath:
                self.LifeAndDeath(BProb = BProb, MProb = MProb)
            if UnoReverse:
                self.UnoReverseLifeAndDeath()
            self.UpdateAllMoves()
        
        if SaveData:
            self.SaveData()
        if SaveGrids:
            self.SaveData(Data=Huge3DArray)

    def RunUntilConvergence(self,
    SaveData = False, KillOrBeKilled = False,
    KillOrBeKilledAndLearn = False, Birth = False,
    Murder = False, LifeAndDeath = False, BProb = None,
    MProb = None, Winner = False, AppendData = False, ConvergenceBound = None):

        if not BProb:
            BProb = 0.25
        if not MProb:
            MProb = 0.25
        if ConvergenceBound:
            Boundary = ConvergenceBound
        else: Boundary = 10e6

        NIters = 0
        while True: #oops
            #check if one of the agents dominates
            Count = self.CountAgents()
            if self.Dimension**2 in Count:
                break
            #same method as with Run
            if AppendData:
                localcopy = copy.deepcopy(self.Agents)
                self.AllData.append(localcopy)
            self.CheckAllWinners()
            self.UpdateAllDists(None, KillOrBeKilled = KillOrBeKilled, KillOrBeKilledAndLearn = KillOrBeKilledAndLearn)

            if Murder:
                self.Murder(MProb = MProb)
            if Birth:
                self.BirthCells(BProb = BProb)
            if LifeAndDeath:
                self.LifeAndDeath(BProb = BProb, MProb = MProb)

            self.UpdateAllMoves()

            #count the number of iterations
            NIters += 1
            if NIters>=Boundary:
                print(str(Boundary) + 'iterations and no convergence. Give up')
                return -1, -1

        try:
            FinalDom = self.Agents[0].GetMove()
        except AttributeError: # accounts for None
            FinalDom = 'E'

        # print('Final Agent:', FinalDom)
        # print(NIters, 'Iterations')


        if SaveData:
            self.SaveData()

        if Winner:
            return NIters, FinalDom
        else:
            return NIters


    def SaveData(self, Data = None):



        FilenameData = [str(self.GetNumberOfSteps()),
                        str(self.GetDimension()),
                        ''.join(random.choice(string.ascii_lowercase) for i in range(4)),
                        ''.join(datetime.datetime.today().strftime("%m-%d %H:%M"))
                        ]

        #merge conflict? why is this defined twice?
        # FilenameData = [str(self.GetNumberOfSteps()),
        #                 str(self.GetDimension()),
        #                 ''.join(random.choice(string.ascii_lowercase) for i in range(5)), ]
        # create a local /pkl dir
        # pkl/NoIterations_GridSize_5letterstring.pkl
        if self.Seed is not None:
            # print("Seed: " + str(Seed))
            random.seed(self.Seed)
            self.Filename = "pkl/" + FilenameData[0] + '_' + FilenameData[1] + '_' + FilenameData[-1] + '_' + str(
                self.seed) + '.pkl'
        else:
            self.Filename = "pkl/" + FilenameData[0] + '_' + FilenameData[1] + '_' + FilenameData[-1] + '.pkl'


        print('saved at ', self.Filename)
        pickle_out = open(self.Filename, 'wb')
        if Data is None:
            pk.dump(self.AllData, pickle_out)
        else:
            pk.dump(Data, pickle_out)
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
            NewDist = random.choices([[1, 0, 0], [0, 1, 0], [0, 0, 1]])[0]
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

    def BirthCells(self, BProb = 0.25):
        D = self.Dimension
        #define probabilities (arrays for easy addition)
        ConversionProbDict = {
            "R" : np.array([BProb,0,0]),
            "P" : np.array([0,BProb,0]),
            "S" : np.array([0,0,BProb]),
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
                self.AgentsGrid[j,i] = Agent(index = D*j+i, Probs=Probs, Seed = self.Seed)
        self.Agents = self.AgentsGrid.flatten().tolist()


    def LifeAndDeath(self, BProb = 0.25, MProb = 0.25):
        # combining the identical method for probabilities
        D = self.Dimension
        #define probabilities
        ConversionProbDict = {
            "R" : np.array([BProb,0,0,0]), #
            "P" : np.array([0,BProb,0,0]), # last 0 because there is 0 probability of death
            "S" : np.array([0,0,BProb,0]), #
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
                        ProbDeath = MProb*abs(AgentRecentScore)
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
                self.AgentsGrid[j,i] = Agent(index = D*j+i, Probs=BirthedProb, Seed = random.randint(0,1e6))
        self.Agents = self.AgentsGrid.flatten().tolist()


    def UnoReverseLifeAndDeath(self, ProbLifeSingle = 0.25, ProbDeathSingle = 0.25):
        # combining the identical method for probabilities
        D = self.Dimension
        #define probabilities
        ConversionProbDict = {
            "R" : np.array([ProbLifeSingle,0,0,0]), #
            "P" : np.array([0,ProbLifeSingle,0,0]), # last 0 because there is 0 probability of death
            "S" : np.array([0,0,ProbLifeSingle,0]), #
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
            j1 = D-1-j
            for i in range(D):
                i1 = D-1-i
                #replace every zero with an array
                PMat = np.array([0,0,0,0], dtype = float)  #[P(NoneToR),P(NoneToP),P(NoneToS), P(Death)]
                #if not an empty cell, have a chance of dying
                if self.AgentsGrid[j1,i1] is not None:
                    AgentRecentScore = self.AgentsGrid[j1,i1].GetRecentScore()
                    if AgentRecentScore < 0:
                        ProbDeath = ProbDeathSingle*abs(AgentRecentScore)
                        PMat = np.array([0,0,0,ProbDeath], dtype = float)
                        PMat = np.append(PMat, 1-ProbDeath)#append P(DoNothing)
                    else:
                        PMat = np.append(PMat, 1)#append P(DoNothing) (nothing happens if score >0)
                    ProbabilityMatrix[j1,i1] = PMat
                    continue

                #if an empty cell, compute chances of conversion
                OppLoc = [ # i <3 modular arithmetic
                            ((j1)%D, (i1+1)%D),
                            ((j1+1)%D, (i1)%D),
                            ((j1)%D, (i1-1)%D),
                            ((j1-1)%D, (i1)%D),
                            ] #equivalent of a dictionary
                for k in range(len(OppLoc)):
                    if self.AgentsGrid[OppLoc[k]] is None:
                            continue
                    AgentType = self.AgentsGrid[OppLoc[k]].GetMove()
                    PMat = PMat + ConversionProbDict.get(AgentType)
                PMat = np.append(PMat, 1-sum(PMat)) #appending P(DoNothing)
                ProbabilityMatrix[j1,i1] = PMat

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
                self.AgentsGrid[j,i] = Agent(index = D*j+i, Probs=BirthedProb, Seed = random.randint(0,1e6))
        self.Agents = self.AgentsGrid.flatten().tolist()

    def Metrics(self):
        return Metrics(AgentList = self.AllData, Iterator = True)


    