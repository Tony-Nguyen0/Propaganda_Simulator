from globals import *
from random import choice, randint,shuffle
import copy
class greenAgent:
    #Blue = 1, Red = 0
    #Uncertainty = [0,1]
    neighbours = []
    def __init__(self, individual):
        self.individual = individual
        # self.certainty = float(randint(0,10))/10
        self.certainty = float(randint(float(lowerLimit[0])*100,float(upperLimit[0])*100)/100)
        self.siding = choice([0,1])
        self.gone = False

# def GreenTurn():
#     global state,cworld
#     #Manipulate each other
#     #Definitely need to use adjency matrix to manipulate variables
#     cworld = copy.deepcopy(world)
#     shuffle(cworld)
#     for person in cworld:
#         for friends in person.neighbours:
#             if(person.individual in cworld[friends].neighbours):
#                 temp = copy.deepcopy(cworld[friends])
#                 GUncertaintyChange(person, cworld[friends])
#                 GUncertaintyChange(temp, person)
#             else:
#                 GUncertaintyChange(person, cworld[friends])
#     cworld = sorted(cworld,key=lambda x:x.individual)
#     #Switching sides
#     switchSide()
#     state.append(cworld)

def GreenTurn():
    global state
    #Manipulate each other
    #Definitely need to use adjency matrix to manipulate variables
    global world
    shuffle(world)
    for person in world:
        for friends in person.neighbours:
            if(person.individual in world[friends].neighbours):
                temp = copy.deepcopy(world[friends])
                GUncertaintyChange(person, world[friends])
                GUncertaintyChange(temp, person)
            else:
                GUncertaintyChange(person, world[friends])
    world = sorted(world,key=lambda x:x.individual)
    #Switching sides
    switchSide()
    state.append(copy.deepcopy(world))

def switchSide():
    global cworld
    siding = [1,0]
    for person in world:
        chance = (1 - person.certainty)*100
        if(randint(1,100) <= chance):
            person.siding = siding[person.siding] 
            person.certainty = upperLimit[0] +lowerLimit[0] - person.certainty

def GUncertaintyChange(person, friends):
    global world
    if(friends.siding == person.siding):
        if(person.certainty >= friends.certainty):
            difference = person.certainty + friends.certainty
            if((friends.certainty + difference) > upperLimit[0]):
                friends.certainty = upperLimit[0]
            else:
                friends.certainty += difference
        else: 
            difference = friends.certainty -person.certainty
            if((friends.certainty + difference/2) > upperLimit[0]):
                friends.certainty = upperLimit[0]
            else:
                friends.certainty += difference/2
    else:
        if(person.certainty >= friends.certainty):
            difference = person.certainty - friends.certainty
            
            if((friends.certainty - difference) < lowerLimit[0]):
                friends.certainty = lowerLimit[0]
            else:
                friends.certainty -= difference
        else: 
            difference = friends.certainty - person.certainty
            if((friends.certainty - difference/2) < lowerLimit[0]):
                friends.certainty = lowerLimit[0]
            else:
                friends.certainty -= difference/2