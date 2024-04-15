import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from Node import Node
from State import State
from Problem import MapProblem
from Map import Map
from utils import memoize
import json, numpy as np, time
genVerbose = False
nodeVerbose = False

print("\n\nWELCOME TO RBFS (Recursive Best First Search) ALGORITHM")

# creates a Map object that represents the country of Mexico
countryName = "Mexico"
mexicoMap = Map(countryName, 1, genVerbose)

# loads the adjacency data from the json file
with open('./RBFS/data.json') as file:
    data = json.load(file)

# can be changed between the different valid nodes of the json file
origin = "Acapulco de Juarez"
goal = "Cuernavaca"
adjacencyData = data["mexico1Node"]

if origin not in adjacencyData:
    print("Origin does not exist on the problem, please change to a valid node.")
    exit()
if goal not in adjacencyData:
    print("Goal does not exist on the problem, please change to a valid node.")
    exit()

# problem: a problem that can be solved with a recursive best first search, in this case, a graph that represents cities locations and distances between them, specifically from Mexico
mexico1Node = MapProblem(State(origin), State(goal), adjacencyData, mexicoMap)

# hCostFunction, best and alternative as kept as global variables to be used in the RBFS function
hCostFunction = None
best = None
alternative = None

# waiting times for the visualization
waitingStart = 1 # 3
waitingComplete = 2 # 5
waitingParent = 1 # 2

runVisualization = True

expandedNodes = []
# If dataHasHeuristics, then the data does not contain the adjacency (action value), but the heuristics itself, so our action cost will be 0
def RecursiveBestFirstSearch(problem : MapProblem, hFunc = None) -> str:
    global hCostFunction
    hCostFunction = memoize(hFunc or problem.hCost, 'hCost')

    initialNode = Node(problem.initialState)
    initialNode.fCost = hCostFunction(initialNode, nodeVerbose)

    mexicoMap.updateState(initialNode.state.name, "start")
    if runVisualization : time.sleep(waitingStart)
    rbfsResult = RBFS(problem, initialNode, np.inf)
    if rbfsResult[0] == None:
        return "No solution found"
    
    mexicoMap.resetAllStates()
    mexicoMap.updateState(rbfsResult[0].state.name, "goal")
    solution = rbfsResult[0].getSolution()
    print(f"Here is the result: {solution} {problem.goalState.name}, with a cost of {rbfsResult[0].pathCost}")
    return

def RBFS(problem : MapProblem, node : Node, fLimit) -> Node:
    global best, alternative, expandedNodes

    if problem.goalTest(node.state):
        return node, 0 
    
    children = node.expand(problem, nodeVerbose)

    if len(children) == 0:
        return None, np.inf
    
    if runVisualization : time.sleep(waitingParent)
    for child in children:
        mexicoMap.updateState(child.state.name, "frontier")
        pathCost = child.pathCost
        hCost = hCostFunction(child)
        child.fCost = pathCost + hCost
        if genVerbose: print("Succesor:", child.state.name, "pathCost:", child.pathCost, "hCost:", hCostFunction(child), "fCost:", child.fCost)
        expandedNodes.append(child.state.name) ## Visualization

    if runVisualization : time.sleep(waitingComplete)
    mexicoMap.resetAllStates()
    while True:
        children.sort(key=lambda x: x.fCost)
        best = children[0]

        if best.fCost > fLimit:
            return None, best.fCost
        
        if len(children) > 1:
            alternative = children[1].fCost
        else:
            alternative = np.inf

        ### Updates Visuals
        mexicoMap.updateState(best.state.name, "open")
        mexicoMap.maxPath = best.pathCost
        mexicoMap.currentVisitedNode = best.state.name

        result, best.fCost = RBFS(problem, best, min(fLimit, alternative))
        if result is not None: # if result would also work
            return result, best.fCost

import threading

def run_RBFS_as_thread(problem, hFunc=None):
    thread = threading.Thread(target=RecursiveBestFirstSearch, args=(problem, hFunc))
    thread.start()
    return thread


# resultA = RecursiveBestFirstSearch(testProblemA, True, False)
# resultB = RecursiveBestFirstSearch(testProblemB)
# resultC = RecursiveBestFirstSearch(testProblemC)

# resultUpsideDown = RecursiveBestFirstSearch(testUpsideDown)

import pandas as py, pygame, matplotlib.pyplot as plt, time
mapForVisualization = mexicoMap.map
def playVisualization(sleepTime = 2):
        pygame.init()

        # Define colors
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        black = (0, 0, 0)
        gray = (200, 200, 200)
        white = (255, 255, 255)
        pink = (235, 50, 180)
        orange = (245, 115, 0)
        
        font = pygame.font.Font(None, 36)
        titleText = font.render(f"{countryName}'s Map", True, black)
        currentVisitedNode = font.render("Visited Node:", True, black)
        currentPathCostText = font.render("Current Path Cost:", True, black)

        # Set the width and height of the screen
        screenWidth = 1200
        screenHeight = 800
        screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(f"{countryName} Map Visualization")

        textWidth = titleText.get_width()
        textHeight = titleText.get_height()
        
        screenWidth *= .9
        screenHeight *= .9

        scaledMap = mapForVisualization.copy()
        # Scale the latitude and longitude values to fit the screen
        min_lat = mapForVisualization['lat'].min()
        max_lat = mapForVisualization['lat'].max()
        min_lng = mapForVisualization['lng'].min()
        max_lng = mapForVisualization['lng'].max()

        scaled_lat = (mapForVisualization['lat'] - min_lat) / (max_lat - min_lat) * screenHeight
        scaled_lng = (mapForVisualization['lng'] - min_lng) / (max_lng - min_lng) * screenWidth
        scaled_lat = screenHeight - scaled_lat

        scaledMap['lat'] = scaled_lat
        scaledMap['lng'] = scaled_lng
        # Game loop
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            screen.fill(white)
            
            # Draw the lines (connecting edges) between all the states on the map
            for origin, destinations in adjacencyData.items():
                originData = scaledMap[scaledMap['city'] == origin]
                xValue = originData['lng'].values[0] + screenWidth/10
                yValue = originData['lat'].values[0] + screenHeight/10
                originCoords = (int(xValue), int(yValue))

                for destination in destinations:
                    destinationData = scaledMap[scaledMap['city'] == destination[0]]
                    destXValue = destinationData['lng'].values[0] + screenWidth/10
                    destYValue =destinationData['lat'].values[0] + screenHeight/10
                    destinationCoords = (int(destXValue), int(destYValue))
                    pygame.draw.line(screen, black, originCoords, destinationCoords, 4)

            # Draw the points
            for lat, lng, state in zip(scaled_lat + screenHeight/10, scaled_lng + screenWidth/10, mapForVisualization['state']):
                match (state):
                    case "open":
                        color = red
                    case "closed":
                        color = black
                    case "frontier":
                        color = green
                    case "start":
                        color = pink
                    case "goal":
                        color = orange
                    case _:
                        color = gray
                pygame.draw.circle(screen, color, (int(lng), int(lat)), 8)

            # Update the screen
            textX = (screenWidth - textWidth) // 2
            textY = 20
            screen.blit(titleText, (textX, textY))

            textY = 40
            screen.blit(currentVisitedNode, (40, textY))
            currentVisitedNode = font.render("Visited Node: " + str(mexicoMap.currentVisitedNode), True, black)

            textY = screenHeight - 40
            screen.blit(currentPathCostText, (40, textY))
            currentPathCostText = font.render("Current Path Cost: " + str(mexicoMap.maxPath), True, black)
            
            pygame.display.flip()
        pygame.quit()

resultMexico1Node = run_RBFS_as_thread(mexico1Node, None)
if runVisualization : playVisualization()
resultsToShow = [
    # [resultA, "Results A"],
    # [resultB, "Results B"],
    # [resultC, "Results C"],
    # [resultUpsideDown, "Results Upside Down"],
    [resultMexico1Node, f"Results Mexico {origin} to {goal}"]
    ]

def nodesString() -> str:
    nodesString = ""
    nodesToTurnToString = expandedNodes
    
    for i in range(len(nodesToTurnToString)):
        if i == len(nodesToTurnToString)-1:
            return nodesString + nodesToTurnToString[i]
        nodesString += nodesToTurnToString[i] + " -> "

    return nodesString

for result in resultsToShow:
    print(f"\n{result[1]}", result[0], f"All #{len(expandedNodes)} expanded nodes: {nodesString()}", sep="\n")