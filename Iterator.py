from Grid import Grid;
import pandas as pd;
import time;
#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time

class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps):
        #Take all of Grid's methods and attributes:
        super().__init__(Dimension) 

        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps
        self.AllStoredData = pd.DataFrame()

    def Run(self):
        for i in range(0, self.Iterations):
            self.CheckAllWinners()
            #i as an argument to add timed decay
            self.UpdateAllDists(i)
            self.UpdateAllMoves()

    # All Agents make a new move
    def UpdateAllMoves(self):
        for i in range(0, len(self.Agents)):
            self.Agents[i].MakeAMove()
        return self.Agents

    # Use scores to adjust each individual Agent's distribution
    def UpdateAllDists(self,TimeStep):
        for i in range(0, len(self.Agents)):
            RecentScore = self.Agents[i].GetRecentScore()
            TotalScore = self.Agents[i].GetTotalScore()
            RecentMove = self.Agents[i].GetMove()
            

            # RPStoOIX = {
            #     "R" : "O",
            #     "P" : "I",
            #     "S" : "X",
            # }
            # RecentMove = RPStoOIX.get(RecentMove)

            ### CREATE FUNCTION HERE
            # Some Function using Score and recent move to change distribution

            NewDist = [1/3, 1/3, 1/3]
            ###

            self.Agents[i].ChangeDist(NewDist)



#Example of 5 iterations and then replotting grid:
x=Iterator(3,5)
x.VisualiseGrid()
x.CheckAllWinners()
sum(x.CheckAllWinners()) # will this always be 0?
x.Run()
time.sleep(3)
x.VisualiseGrid()

