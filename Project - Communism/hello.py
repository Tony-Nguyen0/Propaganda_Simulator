
import ast
def makeDict():
    aDict = {}
    for x in range(100):
        aDict[x] = [0,0,0,0,0]

    # print(aDict)
    return aDict

createDict = makeDict()

# print(createDict)
with open('redAI_data.txt','w') as rAIfile:
    rAIfile.write(str(createDict))

def makeDict2():
    aDict = {}
    for x in range(100):
        aDict[x] = [0,0,0,0,0,0]

    # print(aDict)
    return aDict

createDict = makeDict2()

# print(createDict)
with open('blueAI_data.txt','w') as rAIfile:
    rAIfile.write(str(createDict))

# def grabDict():
#     with open('redAI_data.txt', 'r') as RAIFILE:
#         fileLines= RAIFILE.read()
#         dictionary = ast.literal_eval(fileLines)
#     return dictionary


# grabDict()

