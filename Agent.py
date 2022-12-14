
from WeightsAndMoves import WeightsAndMoves;
import numpy as np;
import random as random

class Agent():

    #Stores data for Individual RPS Agent with fixed Probability Dist & "Scope" to change the Dist.
    #Stores ID & Location (equivalent at t=0), as well as first move.
    #Stores Score of recent round (can be changed to cumulative) starting at 0
    def __init__(self, index, Uniform = False, Ternary = False, Probs = None, Seed = None, ProbsDist = None):
        self.Seed = Seed
        self.Id = index
        self.Location = index #maybe have these different?
        if Ternary or Uniform:
            self.DistributionAndMove = WeightsAndMoves(Uniform = Uniform, Ternary = Ternary, Seed = self.Seed)
        elif Probs:
            self.DistributionAndMove = WeightsAndMoves(Probs = Probs, Seed = self.Seed)
        elif ProbsDist:
            Weights = ProbsDist
            Outcomes = [[1,0,0],[0,1,0],[0,0,1]]
            ProbsDistOutcome = random.choices(Outcomes, Weights)[0]
            self.DistributionAndMove = WeightsAndMoves(Probs=ProbsDistOutcome, Seed=self.Seed)
        else:
            self.DistributionAndMove = WeightsAndMoves(Uniform = True, Seed = self.Seed)
        self.Move = self.DistributionAndMove.MakeAMove()
        self.TotalScore = 0 # cumulative
        self.RecentScore = 0 # what was just played

    def ChangeDist(self, Array):
        self.DistributionAndMove.ChangeProbs(Array)
        return self.DistributionAndMove.ChangeProbs(Array)

    def ChangeLoc(self, Location):
        self.Location = Location
        return self.Location

    def ChangeScore(self, Score):
        self.TotalScore += Score
        self.RecentScore = Score
        return self.TotalScore 

    def MakeAMove(self):
        self.Move = self.DistributionAndMove.MakeAMove()
        return self.Move

    def GetLocation(self):
        return self.Location

    def GetMove(self):
        return self.Move

    def GetRecentScore(self):
        return self.RecentScore

    def GetTotalScore(self):
        return self.TotalScore

    def GetProbabilityDist(self):
        return self.DistributionAndMove.GetProbs()

    def GetAllData(self):
        Loc = self.GetLocation()
        Move = self.GetMove()
        RS = self.GetRecentScore()
        TS = self.GetTotalScore()
        return [Loc, Move, RS, TS]

    def ListToArray(self):
        Array = []
        for i in range(0, self.Dimension):
            ArrayFile = []
            for j in range(0, self.Dimension):
                ArrayElement = self.Agents[self.Dimension * i + j].GetMove()
                ArrayFile.append(self.KeyMapping[ArrayElement])
            Array.append(ArrayFile)

        return np.array(Array)






