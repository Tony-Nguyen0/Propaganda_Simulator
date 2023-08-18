from random import randint,choice
from blue_agent import BlueTurn
from red_agent import RedTurn
from globals import *

from red_agent import RedTurn

class greyAgent:
    #False = neutral, True = red
    gAgentList = []
    def __init__(self, greyPop, rChance):
        for grey in range(greyPop):
            if (randint(0,10))/10 <= rChance:
                self.gAgentList.append(True)
            else:
                self.gAgentList.append(False)

def greyUse():
    global state,gAgent
    agentValue = []
    agentValue.append(population)
    agent = choice(gAgent[0].gAgentList)
    gAgent[0].gAgentList.remove(agent)
    #True = red spy
    #False = blue
    if(not agent):  
        #turn into function
        BlueTurn(4,True)
    else:
        #Decide global later
        RedTurn(4,True)