from Grid import Grid;
import pandas as pd;
import time;


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
            self.UpdateAllDists()
            self.UpdateAllMoves()

    # All Agents make a new move
    def UpdateAllMoves(self):
        for i in range(0, len(self.Agents)):
            self.Agents[i].MakeAMove()
        return self.Agents

    # Use scores to adjust each individual Agent's distribution
    def UpdateAllDists(self):
        for i in range(0, len(self.Agents)):
            Score = self.Agents[i].GetScore()
            RecentMove = self.Agents[i].GetMove()

            ### CREATE FUNCTION HERE
            # Some Function using Score and recent move to change distribution

            NewDist = [0.34, 0.33, 0.33]
            ###

            self.Agents[i].ChangeDist(NewDist)



#Example of 5 iterations and then replotting grid:
# x=Iterator(3,5)
# x.VisualiseGrid()
# print(x.CheckAllWinners())
# print(sum(x.CheckAllWinners()))
# x.Run()
# time.sleep(3)
# x.VisualiseGrid()

