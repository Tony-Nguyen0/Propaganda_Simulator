from tkinter.ttk import Combobox
import networkx as nx
from matplotlib import pyplot as plt,animation
from green_agent import *
from red_agent import *
from blue_agent import *
from grey_agent import *
from globals import *
from tkinter import *
from ai import *
from random import choice,randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_colouring(currentState):
    global counter
    color_map = []
    for agent in currentState:
        a = agent.certainty
        if agent.siding == 1: #blue
            # print((agent.certainty/upperLimit[0]))
            color_map.append((0,0,1,a))
        else:
            # print((agent.certainty/upperLimit[0]))
            color_map.append((1,0,0,a))
    counter+=1
    return color_map

def resultCheck():
    global population, blueCount, redCount,goneValue
    blueCount[0] = sum([1 for person in world if person.siding == 1])
    redCount[0] = sum([1 for person in world if person.siding == 0])
    # print(goneValue[0])
    # When no more to manipulate
    if goneValue[0] == population[0]:
        if(blueCount[0] > redCount[0]):
            return False,"Blue has won by having more followers than Red"
        elif(bAgent[0].energy <= 0 and len(gAgent[0].gAgentList) == 0):
            return False,"Red has won by having more followers than Blue, and Blue has run out of energy and grey agents"
    if redCount[0] == population[0]:
        return False,"Red has all the followers"

    if blueCount[0] == population[0]:
        return False, "Blue has all the followers"
    #When red has won
    if bAgent[0].energy <= 0 and len(gAgent[0].gAgentList) == 0 and redCount[0] > (population[0]//2):
            return False,"Red has won, since Blue has no resources to use and Red has more followers"

    # return len(state) < 10
    return True,None

def environment(population):
    global world
    for individual in range(population):
        world.append(greenAgent(individual))
    addNeighbourToAgents()


def addNeighbourToAgents():
    index=0
    for line in nx.generate_adjlist(G):
        line = line.split(' ')
        line.pop(0)
        fixed_line = [int(i) for i in line]
        world[index].neighbours = fixed_line
        index+=1
    state.append(copy.deepcopy(world))

def updateGUI():
    global nodes,canvas,pos
    colour_map = get_colouring(state[counter])
    pos = nx.circular_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos=pos, ax=ax,node_color=colour_map)
    nx.draw_networkx_labels(G,pos=pos,ax=ax)
    nx.draw_networkx_edges(G,pos=pos,ax=ax)
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.get_tk_widget().pack(fill=BOTH,expand=True)
    fig.canvas.mpl_connect("motion_notify_event",hover)

def updateGraph(colour):
    global canvas,fig,ax,turnCounter,nodes,stringVar,O1,O2,O3,O4,O5
    plt.close(fig)  
    canvas.get_tk_widget().destroy()
    stringVar.set("")
    fig,ax = plt.subplots()
    if colour == player:
        if player == "BLUE":
            if intVar.get() == 10:
                plt.suptitle(f"You have picked to use a grey agent")
                greyUse()
            elif intVar.get() != -1:
                plt.suptitle(f"You have picked option {intVar.get()+1}")
                BlueTurn(intVar.get())
            else:
                plt.suptitle(f"No more energy to make any moves")
                state.append(copy.deepcopy(world))
        else:
            plt.suptitle(f"You have picked option {intVar.get()+1}")
            RedTurn(intVar.get())
    else: #AI stuff
        if colour == "RED":
            v = redAI()
            RedTurn(v)
            plt.suptitle(f"The AI has picked option {v+1}")
        elif colour == "BLUE":
            v = blueAI()
            print(v)
            if v == 5:
                plt.suptitle(f"AI has picked to use a grey agent")
                greyUse()
            elif v == -1:
                plt.suptitle(f"Blue has no more energy")
                state.append(copy.deepcopy(world))
            else:
                BlueTurn(v)
                plt.suptitle(f"The AI has picked option {v+1}")
        else: #this means green turns
            GreenTurn()
    plt.figtext(0,0,f"Turn {counter}",size=15)
    plt.figtext(0,0.97,f"{colour}'s Turn",size=15)
    updateGUI()
    updateinfobox()
    turnCounter+=1
    check,msg = resultCheck()
    if not check and colour == "GREEN":
        nextButton.configure(state=DISABLED)
        configureButtons(DISABLED)
        plt.title(msg)
        return None
    if turnList[(turnCounter%3)] == player:
        intVar.set(-1)
        configureButtons(NORMAL)
    if turnList[(turnCounter%3)] == 'RED':
        O1['text'] = '0.1: ' + choice(blueOrRed[0][0])
        O2['text'] = '0.2: ' + choice(blueOrRed[0][1])
        O3['text'] = '0.3: ' + choice(blueOrRed[0][2])
        O4['text'] = '0.5: ' + choice(blueOrRed[0][3])
        O5['text'] = '0.75: ' + choice(blueOrRed[0][4])
        O1.pack(fill=Y)
        O2.pack(fill=Y)
        O3.pack(fill=Y)
        O4.pack(fill=Y)
        O5.pack(fill=Y)
        # O6.pack_forget()
    elif turnList[(turnCounter%3)] == 'BLUE':
        O1['text'] = '0.1: ' + choice(blueOrRed[1][0])
        O2['text'] = '0.2: ' + choice(blueOrRed[1][1])
        O3['text'] = '0.3: ' + choice(blueOrRed[1][2])
        O4['text'] = '0.5: ' + choice(blueOrRed[1][3])
        O5['text'] = '0.75: ' + choice(blueOrRed[1][4])
        # print(bAgent[0].getEnergy())
        if bAgent[0].getEnergy() <= 4:
            O5.pack_forget()
        if bAgent[0].getEnergy() <= 3:
            O4.pack_forget()
        if bAgent[0].getEnergy() <= 2:
            O3.pack_forget()
        if bAgent[0].getEnergy() <= 1:
            O2.pack_forget()
        if bAgent[0].getEnergy() <= 0:
            O1.pack_forget()


def createButtons():
    global O1,O2,O3,O4,O5,O6,quitButton,nextButton, msg,infobox
    quitButton = Button(master=root, text="Quit", command=root.quit)
    leftFrame = Frame(root)
    leftFrame.pack(side=LEFT)
    msg = Message(leftFrame,textvariable=stringVar,font=("Arial",13),width=1000)
    infobox = Message(leftFrame,textvariable=infoVar,font=("Arial",13),width=1000)
    if turnList[(turnCounter%3)] == "RED":
        O1 = Radiobutton(leftFrame, text='0.1: ' + choice(messagesforRed[0]), value=0,variable=intVar)
        O2 = Radiobutton(leftFrame, text='0.2: ' + choice(messagesforRed[1]), value=1,variable=intVar)
        O3 = Radiobutton(leftFrame, text='0.3: ' + choice(messagesforRed[2]), value=2,variable=intVar)
        O4 = Radiobutton(leftFrame, text='0.5: ' + choice(messagesforRed[3]), value=3,variable=intVar)
        O5 = Radiobutton(leftFrame, text='0.75: ' + choice(messagesforRed[4]), value=4,variable=intVar)
        O6 = Radiobutton(leftFrame, text="Grey Turn", value=10,variable=intVar)
    nextButton = Button(leftFrame,text="Next",command=goNext,bg='white')
    quitButton.pack(side=TOP)
    msg.pack(fill=Y)
    infobox.pack(fill=Y)
    O1.pack(fill=Y)
    O2.pack(fill=Y)
    O3.pack(fill=Y)
    O4.pack(fill=Y)
    O5.pack(fill=Y)
    O6.pack(fill=Y)
    nextButton.pack(fill=X)


def configureButtons(x):
    global intVar,player
    O1.configure(state=x)
    O2.configure(state=x)
    O3.configure(state=x)
    O4.configure(state=x)
    O5.configure(state=x)
    if player != "BLUE" or len(gAgent[0].gAgentList) == 0:
        O6.pack_forget()
    else:
        O6.configure(state=x)
    if x == DISABLED:
        intVar.set(-1)

def goNext():
    global intVar
    if turnList[(turnCounter%3)] == player:
        if intVar.get() == -1 and player=='RED':
            return None
        else:
            if intVar.get() == -1 and player=='BLUE' and (bAgent[0].getEnergy() != 0 or len(gAgent[0].gAgentList) != 0):
                return None
            updateGraph(player)
            configureButtons(DISABLED)
    else:
        intVar.set(1000)
        updateGraph(turnList[(turnCounter%3)])

def hover(event):
    global stringVar, state
    cont, ind = nodes.contains(event)
    if cont:
        node = ind["ind"][0]
        node_attr = {'node': node}
        node_attr.update(G.nodes[node])
        id = node_attr['node']
        world = state[counter-1]
        side = "Red" if world[id].siding == 0 else "Blue"
        if player == "RED":
            attr = f"Node: {id}\nUncertainty: {world[id].certainty:.2f}\nSiding: {side}\nGone?: {world[id].gone}\nNeighbours : {world[id].neighbours}"
        else:
            attr = f"Node: {id}\nUncertainty: {world[id].certainty:.2f}\nSiding: {side}\nNeighbours : {world[id].neighbours}"
        if stringVar.get() != attr:
            stringVar.set(attr)

def updateinfobox():
    global infoVar
    arr = state[counter-1]
    blueCount = sum([1 for person in arr if person.siding == 1])
    redCount = sum([1 for person in arr if person.siding == 0])
    certainty = sum([person.certainty for person in world])/population[0]
    followerslost = sum([1 for person in arr if person.gone])
    if player == "BLUE":
        message = f"Energy Left = {bAgent[0].energy}\nRed nodes = {redCount}\nBlue nodes = {blueCount}\nAverage Uncertainty = {certainty:.2f}"
    else:
        message = f"Followers lost = {followerslost}\nRed nodes = {redCount}\nBlue nodes = {blueCount}\nAverage Uncertainty = {certainty:.2f}"
    infoVar.set(message)

def PlayervsAImain(n,p,colour):
    global G,fig,state,world,root,intVar,canvas,population,player,turnCounter,nodes,ax,pos,stringVar,infoVar,conProb,rAgent,bAgent,goneValue,counter, theDictR, theDictB
    theDictR.append(grabDict('redAI_data.txt'))
    theDictB.append(grabDict('blueAI_data.txt'))
    rAgent.append(redAgent())
    bAgent.append(blueAgent())
    population[0] = n
    conProb[0] = p
    greyPop = max(1,population[0]//10)
    rChance = 0.3
    gAgent.append(greyAgent(greyPop, rChance))
    player=colour
    root = Tk()
    root.geometry("1500x800")
    root.title("PROJECT")
    fig, ax = plt.subplots()
    plt.figtext(0,0,f"Turn 0",size=15)
    plt.figtext(0,0.97,f"START OF GAME",size=15)
    G = nx.erdos_renyi_graph(population[0],conProb[0], directed = True)
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.draw()
    intVar = IntVar()
    stringVar = StringVar()
    infoVar = StringVar()
    intVar.set(-1)
    stringVar.set("")
    createButtons()
    environment(population[0])
    updateGUI()
    if turnList[(turnCounter%3)] != player:
        configureButtons(DISABLED)
    else:
        configureButtons(NORMAL)
    updateinfobox()
    # mainloop()

def getSliderValue():
    global startMenu,upperLimit, lowerLimit
    n = nodesNumber.get()
    p = probs.get()/100
    upperLimit[0] = upperBounds.get()
    lowerLimit[0] = lowerBounds.get()
    mode = arg.get()
    if mode ==  1:
        if combobox.get() == "RANDOM":
            player = choice(["RED","BLUE"])
        else:
            player = combobox.get()
        startMenu.destroy()
        PlayervsAImain(n,p,player)
    elif mode == 0:
        startMenu.destroy()
        AIvsAImain(n,p)

def turnOnPlayerOptions():
    combobox.pack()

def turnOffPlayerOptions():
    combobox.pack_forget()
 
def AIvsAImain(n,p):
    global G,fig,state,world,root,intVar,canvas,population,player,turnCounter,nodes,ax,pos,stringVar,infoVar,conProb,rAgent,bAgent,goneValue,counter,msg, theDictR, theDictB,listOfTurns,redOrBlue
    theDictR.append(grabDict('redAI_data.txt'))
    theDictB.append(grabDict('blueAI_data.txt'))
    rAgent.append(redAgent())
    bAgent.append(blueAgent())
    population[0] = n
    conProb[0] = p
    greyPop = max(1,population[0]//10)
    rChance = 0.3
    gAgent.append(greyAgent(greyPop, rChance))
    G = nx.erdos_renyi_graph(population[0],conProb[0], directed = True)
    environment(population[0])
    listOfTurns = [[],[]]
    check = True
    msg = "temp"
    while check:
        v = redAI()
        RedTurn(v)
        listOfTurns[0].append(v)
        v = blueAI()
        if(v != -1):
            if(v != 5):
                BlueTurn(v)
            else:
                greyUse()
        else:
            state.append(copy.deepcopy(world))
        listOfTurns[1].append(v)
        GreenTurn()
        check,msg = resultCheck()
    redOrBlue = 0
    print(listOfTurns)
    writeToDict('redAI_data.txt', theDictR[0])
    writeToDict('blueAI_data.txt',theDictB[0])
    fig,ax = plt.subplots()
    color_map = get_colouring(state[counter])
    plt.suptitle(f"Start of the Game")
    nx.draw_circular(G,with_labels=True,node_color=color_map)
    ani = animation.FuncAnimation(fig, animate, frames=len(state)-1, interval=500, repeat=False)
    plt.show()

def animate(frame):
    global G,counter,redOrBlue
    try:
        fig.clear()
        plt.suptitle(f"Turn {counter-1}")
        if turnList[(counter-1)%3] == "RED":
            plt.title(f"Red has picked option {listOfTurns[0][redOrBlue]+1}")
        elif turnList[(counter-1)%3] == "BLUE":
            if listOfTurns[1][redOrBlue] == -1:
                plt.title(f"Blue has no energy so no change")
            elif listOfTurns[1][redOrBlue] == 5:
                plt.title(f"Blue has used a grey agent")
            else:
                plt.title(f"Blue has picked option {listOfTurns[1][redOrBlue]+1}")
        else:
            plt.title(f"Green Turn")
            redOrBlue+=1
        color_map = get_colouring(state[counter])
        nx.draw_circular(G,with_labels=True,node_color=color_map)
    except:
        print('end of the road')
        plt.suptitle(f"Game has Ended")
        plt.title(msg)
        color_map = get_colouring(state[counter-1])
        nx.draw_circular(G,with_labels=True,node_color=color_map)
        return None

if __name__ == '__main__':
    startMenu = Tk()
    startMenu.geometry('1000x400')
    startMenu.title("Start Menu")
    arg = IntVar()
    arg.set(-1)
    AIvsAIbutton = Radiobutton(master=startMenu,text="AI vs AI", value=0,variable=arg,command=turnOffPlayerOptions).pack()
    PlayervsAIbutton = Radiobutton(master=startMenu,text="Player vs AI", value=1,variable=arg,command=turnOnPlayerOptions).pack()
    nodeslabels = Label(master=startMenu, text="Number of Nodes")
    nodeslabels.pack()
    nodesNumber = Scale(master=startMenu,from_=3,to=50,orient=HORIZONTAL,length=500)
    nodesNumber.pack()
    probslabels = Label(master=startMenu, text="Probability of connection between agents (Percentages)")
    probslabels.pack()
    probs = Scale(master=startMenu,from_=1,to=100,orient=HORIZONTAL,length=1000)
    probs.pack()
    lowerlabels = Label(master=startMenu, text="Lower bounds (from 0 to 0.4)")
    lowerlabels.pack()
    lowerBounds = Scale(master=startMenu,from_=0,to=0.4, digits = 3,resolution = 0.1,orient=HORIZONTAL,length=500)
    lowerBounds.pack()
    lowerBounds.set(0)
    upperlabels = Label(master=startMenu, text="upper bounds (from 0.6 to 1)")
    upperlabels.pack()
    upperBounds = Scale(master=startMenu,from_=0.6,to=1, digits = 3,resolution = 0.1,orient=HORIZONTAL,length=500)
    upperBounds.pack()
    upperBounds.set(1)
    option = StringVar()
    combobox = Combobox(master=startMenu,textvariable=option)
    combobox['values'] = ('RANDOM','BLUE','RED')
    combobox['state']='readonly'
    combobox.current(0)
    combobox.pack_forget()
    Button(master=startMenu,text="press",command=getSliderValue).pack(side=BOTTOM)
    mainloop()