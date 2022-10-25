import numpy as np
from random import choices
'''
Non-Markovian adjustment of weights (based on what was just played)
subclasses define the weight adjustments. may get 
different behaviour if we define different scalings 
'''

class WeightsAndMoves:
    def __init__(self, Probs = None, Uniform = True, MoveType = None):#, JustPlayed):
        '''
        Scores - (int) current score of each agent
        Probs - (list)current probability to play O,I,X
        Status - (str: "W" , "L", "T") based on if they just won lost or tied
        JustPlayed - (Str: "O" ,"I" , "X") what was just played 
        instance to be initiated at every new iteration timestep
        '''
        if Uniform:
            self.Probs = [1/3,1/3,1/3]
        elif Probs:
            self.Probs = Probs
        self.PO, self.PI, self.PX = self.Probs #to make defining functions easier
        # self.JustPlayed = JustPlayed
        self.CheckProbs()

        if MoveType == None:
            self.MoveType = "Random"
        else: self.MoveType = MoveType

    def AdjustWeights(self):
        raise NotImplementedError("subclass needs to define this")

    #IDK what this is doing atm
    # def CheckAdj(self, Adjustment):
    #     DeltaP = 1-max(self.Probs)
    #     if Adjustment > DeltaP:
    #         raise ValueError("adjustment too large!")
    def CheckProbs(self, Probs = None):
        if Probs == None:
            Probs = self.Probs
        if sum(Probs) != 1:
            raise ValueError("not normed!")

    def GetProbs(self):
        return self.Probs

    def ChangeProbs(self, probs):
        self.CheckProbs(probs)
        self.Probs = probs
        return self.Probs

    def MakeAMove(self):
        if self.MoveType == "Random":
            Move = self.Random()
            return Move

        else:
            return "R" #Just incase
    def Random(self):
        return choices(["R", "P", "S"], self.Probs)[0]

    def UpdateDist(self):
        #FunkyFunction
        self.Probs = self.Probs
        return self.Probs







# class Exponential(Weights):
#     def __init__(self, Probs, Score, Status):
#         '''
#         an initial test. factorials chosen to ensure nothing > 1
#         '''
#         super().__init__(Probs, Score, Status)
#
#     def AdjustWeights(self, TimeStep):
#         Adjustment = np.exp(-self.Score)*np.exp(-TimeStep)
#         self.CheckAdj(Adjustment)
#         IWL, I1, I2, Oper = self.CompileDict() #unpack the dictionary
#         if Oper == "+":
#             self.Probs[IWL] += Adjustment
#             self.Probs[I1] -= Adjustment/2
#             self.Probs[I2] -= Adjustment/2
#         elif Oper == "-":
#             self.Probs[IWL] -= Adjustment
#             self.Probs[I1] += Adjustment/2
#             self.Probs[I2] += Adjustment/2
#         self.CheckProbs()
#         return self.Probs
#
# class Linear(Weights):
#     def __init__(self, Probs, Score, Status):
#         super().__init__(Probs, Score, Status)
#
#     def AdjustWeights(self, TimeStep, k = 1.1):
#         Adjustment = (self.Score*np.exp(-k*TimeStep))/4
#         self.CheckAdj(Adjustment)
#         IWL, I1, I2, Oper = self.CompileDict() #unpack the dictionary
#         if Oper == "+":
#             self.Probs[IWL] += Adjustment
#             self.Probs[I1] -= Adjustment/2
#             self.Probs[I2] -= Adjustment/2
#         elif Oper == "-":
#             self.Probs[IWL] -= Adjustment
#             self.Probs[I1] += Adjustment/2
#             self.Probs[I2] += Adjustment/2
#         self.CheckProbs()
#         return self.Probs




#debugging
# k = 0.2
# score = 1
# probs = [0.3,0.4,0.3]
# test = Exponential(probs, score, "W")#,"O")
# test.AdjustWeights(8)
# print()
# #should do nothing
# test = Linear(probs, score, "W")#,"T")
# for i in range(1,4):
#     a = test.AdjustWeights(i)
#     print(a)
