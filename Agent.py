from random import choices

class Agent:
    def __init__(self, index):
        self.Id = index
        self.Location = index
        self.ProbabilityDist = [0.34, 0.33, 0.33]
        self.Move = choices(["R", "P", "S"], self.ProbabilityDist)[0]

    def ChangeDist(self, Array):
        self.ProbabilityDist = Array
        return self.ProbabilityDist

    def ChangeLoc(self, Location):
        self.Location = Location
        return self.Location

    def MakeAMove(self):
        self.Move = choices(["R", "P", "S"], self.ProbabilityDist)

    def GetLocation(self):
        return self.Location

    def GetMove(self):
        return self.Move





