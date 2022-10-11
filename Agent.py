from random import choices

class Agent:

    #Stores data for Individual RPS Agent with fixed Probability Dist & "Scope" to change the Dist.
    #Stores ID & Location (equivalent at t=0), as well as first move.
    #Stores Score of recent round (can be changed to cumulative) starting at 0
    def __init__(self, index):
        self.Id = index
        self.Location = index
        self.ProbabilityDist = [0.34, 0.33, 0.33]
        self.Move = choices(["R", "P", "S"], self.ProbabilityDist)[0]
        self.Score = 0

    def ChangeDist(self, Array):
        self.ProbabilityDist = Array
        return self.ProbabilityDist

    def ChangeLoc(self, Location):
        self.Location = Location
        return self.Location

    def ChangeScore(self, Score):
        self.Score = Score
        return self.Score

    def MakeAMove(self):
        self.Move = choices(["R", "P", "S"], self.ProbabilityDist)[0]
        return self.Move

    def GetLocation(self):
        return self.Location

    def GetMove(self):
        return self.Move

    def GetScore(self):
        return self.Score





