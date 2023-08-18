gAgent = []
bAgent = []
rAgent = []
world = []
population = [0]
state = []
counter=0
turnList = ['RED','BLUE','GREEN']
turnCounter = 0
goneValue = [0]
conProb = [0]


upperLimit = [0]
lowerLimit = [0]
#For AI


redCount = [0]
blueCount = [0] 
theDictR = []
theDictB = []

messagesforRed = {0:["Nope 2 vote","2 cool 4 voting"],1:["Voting wastes your time","You're a sheep if you vote"],2:["Voting doesn't matter, it's rigged anyways","Did you get to vote on being born? EXACTLY"],3:["Might as well not vote if you're gonna donkey vote","It divides us, forcing us to pick sides when we can be one"],4:["Why should we vote? Why must we pay a fine just because we don't want to be forced into some political struggle","Voting takes up our taxpayer's money at an extravagant rate just to give an opinion"]}
messagesforBlue = {0:["Voting is cool","I like voting"],1:["Voting creates opportunities","Cast your vote from a boat"],2:["Be an absolute g of a goat and vote" ,"Since the dawn of time voting has kept society going"],3:["If Ryan Reynolds will vote why can't you?","We value everyone's opinion, that's why share yours with us by voting"],4:["The democratic power of voting ensures the survival of individuals rights and freedom","Voting is an ancestral right given to us through much struggle and hardship to get us this right today"]}

blueOrRed = [messagesforRed,messagesforBlue]