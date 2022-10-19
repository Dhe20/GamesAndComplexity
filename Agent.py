from random import choices;
from WeightsAndMoves import WeightsAndMoves;

class Agent():

    #Stores data for Individual RPS Agent with fixed Probability Dist & "Scope" to change the Dist.
    #Stores ID & Location (equivalent at t=0), as well as first move.
    #Stores Score of recent round (can be changed to cumulative) starting at 0
    def __init__(self, index):
        self.Id = index
        self.Location = index #maybe have these different?
        self.DistributionAndMove = WeightsAndMoves(Uniform = True)
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







