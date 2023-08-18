from cmath import inf
import copy
from random import randint
import ast

from red_agent import loseFollowerCheck
from globals import redCount, blueCount, bAgent, rAgent, world, population, theDictB, theDictR, gAgent

def grabDict(file):
    with open(file, 'r') as aiFile:
        fileLines= aiFile.read()
        dictionary = ast.literal_eval(fileLines)
    return dictionary

def writeToDict(file, dict):
    with open(file, 'w') as aiFile:
        aiFile.write(str(dict))

def blueAI():
    global theDictB
    if(bAgent[0].energy <= 0):
        return -1
    percentage = int((redCount[0]/population[0])*100)
    # print(percentage)

    dictList = theDictB[0][percentage]  
    # print(dictList)  

    possibilities = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    if(bAgent[0].energy >=5):
        for x in range(5):
            result = tempBlueTurn(x)
            possibilities.append(result)

        for x in range(5):
            dictList[x] = (possibilities[x][0] + dictList[x])/2
    else:
        for x in range(bAgent[0].energy%5):
            result = tempBlueTurn(x)
            possibilities.append(result)

        for x in range(bAgent[0].energy%5):
            dictList[x] = (possibilities[x][0] + dictList[x])/2

    possibleUse = []
    if(len(gAgent[0].gAgentList) != 0):
        result = tempGreyUse()
        possibilities.insert(5, result)
        dictList[5] = (possibilities[5][0]+dictList[5])/2
        possibleUse.append(dictList[5])
    
    for potency in range(len(dictList)-1):
        if (potency + 1) <= bAgent[0].energy:
            possibleUse.append(dictList[potency])
    return dictList.index(max(possibleUse))

def tempGreyUse():
    #Need to add condition in grey if value returned is 6.
    thisWorld = copy.deepcopy(world)
    tempBlueCount = 0
    for person in thisWorld:
        if(person.siding == 1):
            person.certainty = min(1,person.certainty*(1+bAgent[0].potencyLevel[4]))
        else:
            person.certainty = min(1,person.certainty*(1-bAgent[0].potencyLevel[4]))
    thisWorld = switchSideAI(thisWorld)

    for person in thisWorld:
        if person.siding == 1:
            tempBlueCount+= 1
    
    return [blueCount[0] - tempBlueCount,6]

def tempBlueTurn(potency, grey = False):
    #Manipulate world
    thisWorld = copy.deepcopy(world)
    tempBlueCount = 0
    for person in thisWorld:

        if(person.siding == 1):
            person.certainty = min(1,person.certainty*(1+bAgent[0].potencyLevel[potency]))
        else:
            person.certainty = min(1,person.certainty*(1-bAgent[0].potencyLevel[potency]))
    thisWorld = switchSideAI(thisWorld)

    for person in thisWorld:
        if person.siding == 1:
            tempBlueCount+= 1
    return [(tempBlueCount- blueCount[0])/(potency+1), potency]

def redAI():
    global theDictR
    percentage = int((blueCount[0]/population[0])*100)
    dictList = theDictR[0][percentage]
    possibilities = []
    for x in range(5):
        result = tempRedTurn(x)
        possibilities.append(result)

    
    # possibilities = sorted(possibilities, key = lambda x:x[0], reverse = True)
    for x in range(5):
        dictList[x] = (possibilities[x][0] + dictList[x])/2

    return dictList.index(max(dictList))


def tempRedTurn(potency,grey=False):
    thisWorld = copy.deepcopy(world)
    tempGone = 0    
    tempRCount = 0
    for person in thisWorld:
        if(person.gone == False):
            if(person.siding == 1):
                uncertaintyChange = loseFollowerCheck(person,(1-rAgent[0].potencyLevel[potency]))
                if(uncertaintyChange == 0):
                    if not grey:
                        person.gone = True
                        tempGone+=1
                person.certainty = uncertaintyChange
        
            else:
                uncertaintyChange = loseFollowerCheck(person,(1+rAgent[0].potencyLevel[potency]))
                if(uncertaintyChange == 0):
                    if not grey:
                        if(randint(0,3) == 0):
                            person.gone = True
                            tempGone+=1
                person.certainty = uncertaintyChange
    thisWorld = switchSideAI(thisWorld)
    for person in thisWorld:
        if(person.siding == 0):
            tempRCount += 1
    return [(tempRCount-redCount[0])/(tempGone+1), potency]        

def switchSideAI(tempWorld):
    siding = [1,0]
    for person in tempWorld:
        chance = (1 - person.certainty)*100
        if(randint(1,100) <= chance):
            person.siding = siding[person.siding] 

    return tempWorld

