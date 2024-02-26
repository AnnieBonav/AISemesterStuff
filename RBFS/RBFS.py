import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from Graph import Graph
from Node import Node
from State import State
from Problem import MapProblem
from Map import Map
import json
import numpy as np

from utils import memoize
# problem: a problem that can be solved with a recursive best first search, in this case, a graph that represents cities locations and distances between them
countryName = "Mexico"
mexicoMap = Map(countryName)

verbose = True
with open('./RBFS/data.json') as file:
    data = json.load(file)

origin = "Monterrey"
goal = "Tijuana"
adjacencyData = data["mexico1Node"]
mexico1Node = MapProblem(State(origin), State(goal), adjacencyData, mexicoMap)

counter = 0
hCostFunction = None

best = None
alternative = None

waiting = 5

# If dataHasHeuristics, then the data does not contain the adjacency (action value), but the heuristics itself, so our action cost will be 0
def RecursiveBestFirstSearch(problem : MapProblem, hFunc = None) -> str:
    global hCostFunction
    hCostFunction = memoize(hFunc or problem.hCost, 'hCost')
    initialNode = Node(problem.initialState)
    initialNode.fCost = hCostFunction(initialNode)

    rbfsResult = RBFS(problem, initialNode, np.inf)
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()

    return f"Here is the result: {solution} {problem.goalState.name}, with a cost of {rbfsResult[0].pathCost}"

def RBFS(problem : MapProblem, node : Node, fLimit) -> Node:
    global counter, best, alternative
    counter += 1
    if problem.goalTest(node.state):
        return node, 0 
    
    mexicoMap.resetAllStates()
    successors = node.expand(problem, verbose)

    if len(successors) == 0:
        return None, np.inf
    
    for succesor in successors:
        mexicoMap.updateState(succesor.state.name, "frontier")
        # if verbose : print("Succesor:",succesor)
        pathCost = succesor.pathCost
        hCost = hCostFunction(succesor)
        succesor.fCost = pathCost + hCost
        print("Succesor:", succesor.state.name, "pathCost:", succesor.pathCost, "hCost:", hCostFunction(succesor), "fCost:", succesor.fCost)

    while True:
        successors.sort(key=lambda x: x.fCost)
        best = successors[0]

        if best.fCost > fLimit:
            return None, best.fCost
        
        if len(successors) > 1:
            alternative = successors[1].fCost
        else:
            alternative = np.inf

        # Update Map
        mexicoMap.updateState(best.state.name, "open")
        import time
        time.sleep(waiting)

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
        
        font = pygame.font.Font(None, 36)
        titleText = font.render(f"{countryName}'s Map", True, black)
        visitedNodeText = font.render("Visited Node:", True, black)

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
        print("Info", type(scaled_lat))

        scaled_lng = (mapForVisualization['lng'] - min_lng) / (max_lng - min_lng) * screenWidth
        scaled_lat = screenHeight - scaled_lat

        scaledMap['lat'] = scaled_lat
        scaledMap['lng'] = scaled_lng
        # Game loop
        running = True

        counter = 0
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            screen.fill(white)

            # Draw the points
            for lat, lng, state in zip(scaled_lat + screenHeight/10, scaled_lng + screenWidth/10, mapForVisualization['state']):
                match (state):
                    case "open":
                        color = red
                    case "closed":
                        color = black
                    case "frontier":
                        color = blue
                    case _:
                        color = gray
                pygame.draw.circle(screen, color, (int(lng), int(lat)), 6)
            
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

            # Update the screen
            textX = (screenWidth - textWidth) // 2
            textY = 20
            screen.blit(titleText, (textX, textY))

            textY = 40
            screen.blit(visitedNodeText, (40, textY))

            visitedNodeText = font.render("Visited Node: " + str(counter), True, black)
            counter += 1
            # if(counter%2 == 0):
            #     self.updateState('Mexico City', 'closed')
            # else:
            #     self.updateState('Mexico City', 'frontier')

            pygame.display.flip()

            # time.sleep(sleepTime)
            # print("Slept")
        # Quit Pygame
        pygame.quit()

resultMexico1Node = run_RBFS_as_thread(mexico1Node, None)
playVisualization()
resultsToShow = [
    # [resultA, "Results A"],
    # [resultB, "Results B"],
    # [resultC, "Results C"],
    # [resultUpsideDown, "Results Upside Down"],
    [resultMexico1Node, "Results Mexico 1 Node"]
    ]

def nodesString(stringToShow) -> str:
    nodesString = ""
    match (stringToShow):
        case "visited":
            nodesToTurnToString = allVisitedNodes
        case "expanded":
            nodesToTurnToString = allExpandedNodes
        case _:
            return "Invalid stringToShow value"
    
    for i in range(len(nodesToTurnToString)):
        if i == len(nodesToTurnToString)-1:
            return nodesString + nodesToTurnToString[i]
        nodesString += nodesToTurnToString[i] + " -> "

    return nodesString

for result in resultsToShow:
    print(f"\n{result[1]}", result[0], sep="\n")