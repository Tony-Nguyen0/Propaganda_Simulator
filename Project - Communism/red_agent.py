from globals import *
import copy
from random import randint
class redAgent:
    potencyLevel = [0.1, 0.2, 0.3, 0.5, 0.75]

def RedTurn(potency,grey=False):
    global state, goneValue, PreviousChoiceR,rAgent,population
    PreviousChoiceR = potency
    for person in world:
        if(person.gone == False):
            if(person.siding == 1):
                uncertaintyChange = loseFollowerCheck(person,(1-rAgent[0].potencyLevel[potency]))
                person.certainty = uncertaintyChange
        
            else:
                uncertaintyChange = loseFollowerCheck(person,(1+rAgent[0].potencyLevel[potency]))
                if(uncertaintyChange == 0):
                    if not grey:
                        if(randint(0,3) == 0):
                            person.gone = True
                            goneValue[0]+=1
                person.certainty = uncertaintyChange
    state.append(copy.deepcopy(world))


def loseFollowerCheck(person, value):
    #person.gone may not work due to local variable
    theResult = person.certainty * value
    if(theResult > upperLimit[0]):
        return 0
    else:
        return theResult