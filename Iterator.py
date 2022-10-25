from copy import copy
from Grid import Grid;
import pandas as pd;
import time;
import pickle as pk
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from matplotlib import colors
from time import sleep
import numpy as np
import random
import string
import copy

#from WeightsAndMoves import Linear

#Inherited class of Grid now allowing multiple iterations in time


class Iterator(Grid):
    def __init__(self, Dimension, NumberOfSteps, EmptyCellCount=0):
        #Take all of Grid's methods and attributes:
        super().__init__(Dimension, EmptyCellCount) 

        #Adding storage for PKL and iterations
        self.Iterations = NumberOfSteps

    def GetNumberOfSteps(self):
        return self.Iterations

    def Run(self, SaveData = False):
        #only fills if SaveDate == True
        AllAgentGrids = []

        for i in range(0, self.Iterations):
            #i as an argument to add timed decay
            
            #update
            ScoreArray = self.CheckAllWinners()[1] #method still works the same just outputs ScoreArray
            self.UpdateAllDists(i)
            self.UpdateAllMoves()
            AgentData = self.ListToArray()
            self.UpdateSomePositions(AgentData, ScoreArray)#for dying away and moving

            #save data
            if SaveData == True:
                localcopy = copy.deepcopy(self.Agents)
                print(localcopy[1].TotalScore)
                AllAgentGrids.append(localcopy)

        if SaveData == True:
            #add any other data to the filename here
            FilenameData = [str(self.GetNumberOfSteps()),
                            str(self.GetDimension()),
                            ''.join(random.choice(string.ascii_lowercase) for i in range(5)),]
            #create a local /pkl dir
            #pkl/NoIterations_GridSize_5letterstring.pkl
            Filename = 'pkl/'+FilenameData[0]+'_'+FilenameData[1]+'_'+FilenameData[-1]+'.pkl'
            print('saved at ', Filename)
            pickle_out = open(Filename, 'wb')
            pk.dump(AllAgentGrids, pickle_out)
            pickle_out.close()

    # All Agents make a new move
    def UpdateAllMoves(self):
        for i in range(0, len(self.Agents)):
            if self.Agents[i] is None:
                continue
            self.Agents[i].MakeAMove()
        return self.Agents

    # Use scores to adjust each individual Agent's distribution
    def UpdateAllDists(self,TimeStep):
        for i in range(0, len(self.Agents)):
            if self.Agents[i] is None:
                continue

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
x=Iterator(5,40, EmptyCellCount=0)
x.VisualiseGrid()
x.CheckAllWinners()
sum(x.CheckAllWinners()[0]) # will this always be 0?
x.Run(SaveData=True)
time.sleep(3)
x.VisualiseGrid()

