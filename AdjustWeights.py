import numpy as np

'''
Markovian adjustment of weights (based on what was just played)
subclasses define the weight adjustments. may get 
different behaviour if we define different scalings 
'''

class AdjustWeights:
    def __init__(self, Probs, Score, Status, JustPlayed):
        '''
        Scores - (int) current score of each agent
        Probs - (list)current probability to play O,I,X
        Status - (str: "W" , "L", "T") based on if they just won lost or tied
        JustPlayed - (Str: "O" ,"I" , "X") what was just played 
        instance to be initiated at every new iteration timestep
        '''

        self.Probs = Probs
        self.Score = Score
        self.Status = Status
        self.PO, self.PI, self.PX = Probs #to make defining functions easier
        self.JustPlayed = JustPlayed
        self.CheckProbs()

    def AdjustWeights(self):
        raise NotImplementedError("subclass needs to define this")

    def CheckProbs(self):
        if sum(self.Probs) != 1:
            raise ValueError("not normed!")

    def CheckStatus(self):
        if self.Status != "W" or self.Status != "L":
            raise ValueError("illegal status!")

    def CheckJustPlayed(self):
        if self.JustPlayed != "O" or self.JustPlayed != "I" or self.JustPlayed != "X":
            raise ValueError("illegal status!")

    def CheckAdj(self, Adjustment):
        DeltaP = 1-max(self.Probs)
        if Adjustment > DeltaP:
            raise ValueError("adjustment too large!")
 
    def GetScore(self):
        return str(self.Score)

    def GetProbs(self):
        return self.Probs

    def CompileDict(self):
        '''
        Dict for each case (maybe don't need a specific method for this?)
        First index - index of W/L
        Second and third index - index of others
        '''
        Dict = {
        "WO": [0,1,2, "+"],
        "WI": [1,2,0, "+"],
        "WX": [2,0,1, "+"],
        "LO": [0,1,2, "-"],
        "LI": [1,2,0, "-"],
        "LX": [2,0,1, "-"],
        "T": [None,None,None,None], #there must be a better way lol
        }
        StatRepr = self.Status+self.JustPlayed
        #special case for T
        if StatRepr[-1] == "T":
            return Dict.get("T")
        return Dict.get(StatRepr) #who needs else: return 

class Exponential(AdjustWeights):
    def __init__(self, Probs, Score, Status, JustPlayed):
        '''
        an initial test. factorials chosen to ensure nothing > 1
        '''
        super().__init__(Probs, Score, Status, JustPlayed)
    
    def AdjustWeights(self):
        Adjustment = np.exp(-self.Score)
        self.CheckAdj(Adjustment)
        IWL, I1, I2, Oper = self.CompileDict() #unpack the dictionary
        if Oper == "+":
            self.Probs[IWL] += Adjustment
            self.Probs[I1] -= Adjustment/2
            self.Probs[I2] -= Adjustment/2  
        elif Oper == "-":
            self.Probs[IWL] -= Adjustment
            self.Probs[I1] += Adjustment/2
            self.Probs[I2] += Adjustment/2
        self.CheckProbs()
        return self.Probs

'''
#debugging
score = 3
probs = [0.3,0.4,0.3]
test = Exponential(probs, score, "W","O")
test.AdjustWeights()
print()
#should do nothing
test = Exponential(probs, score, "W","T")
test.AdjustWeights()
'''