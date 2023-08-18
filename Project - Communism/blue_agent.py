from globals import*
import copy
class blueAgent:
    #blue Agent message potency
    potencyLevel = [0.1, 0.2, 0.3, 0.5, 0.75]

    energy = 25

    def loseEnergy(self,potency):
        self.energy -= (potency+1)

    def getEnergy(self):
        return self.energy

def BlueTurn(potency, grey = False):
    global state, world, PreviousChoiceB
    PreviousChoiceB = potency
    #Manipulate world
    if not grey:
        bAgent[0].energy -= potency + 1
    for person in world:
        if(person.siding == 1):
            person.certainty = min(1,person.certainty*(1+bAgent[0].potencyLevel[potency]))
        else:
            person.certainty = min(1,person.certainty*(1-bAgent[0].potencyLevel[potency]))
    state.append(copy.deepcopy(world))