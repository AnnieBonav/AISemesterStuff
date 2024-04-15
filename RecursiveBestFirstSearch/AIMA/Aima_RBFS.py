from Node import Node
from utils import memoize
from GraphProblem import GraphProblem
from UnidirectedGraph import UndirectedGraph
import numpy as np, json

allVisitedNodes = []

runVisualization = True

# waiting times for the visualization
waitingStart = 1 # 3
waitingComplete = 3 # 5
waitingParent = 1 # 2

print("\nWELCOME to Recursive Best First Search (RBFS)")
def RecursiveBestFirstSearch(problem, hCost=None):
    global romaniaMap
    hCost = memoize(hCost or problem.hCost, 'hCost')

    def RBFS(problem, node, flimit):
        allVisitedNodes.append(node.state) # For visualization

        if problem.goal_test(node.state):
            print("GOAL REACHED")
            return node, 0
        
        children = node.expand(problem)

        if len(children) == 0:
            return None, np.inf
        
        if runVisualization : time.sleep(waitingParent) ## For visualization
        for child in children:
            child.fCost = max(child.pathCost + hCost(child), node.fCost)
            romaniaMap.updateState(child.state, "frontier") # For visualization
        
        if runVisualization : time.sleep(waitingComplete)
        romaniaMap.resetAllStates() ## For visualization
        
        while True:
            # Order by lowest fCost value
            children.sort(key=lambda x: x.fCost)
            best = children[0]
            if best.fCost > flimit:
                return None, best.fCost
            if len(children) > 1:
                alternative = children[1].fCost
            else:
                alternative = np.inf
            
            ### Updates Visuals
            romaniaMap.updateState(best.state, "open")
            romaniaMap.maxPath = best.pathCost
            romaniaMap.mainNodeText = f"Visited Node : {best.state}"

            result, best.fCost = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                print("RESULTING")
                return result, best.fCost

    initialNode = Node(problem.initial)
    initialNode.fCost = hCost(initialNode)
    romaniaMap.updateState(initialNode.state, "start")
    romaniaMap.mainNodeText = f"Starting Node : {initialNode.state}"

    if runVisualization : time.sleep(waitingStart)

    result, bestf = RBFS(problem, initialNode, np.inf)

    if result is None:
        print("\nNo solution found")

    romaniaMap.updateState(result.state, "goal")
    romaniaMap.mainNodeText = f"Reached Goal Node : {result.state}"

    solution = result.solution()
    print(f"\nPATH from {startNode} to {endNode}")
    for node in solution:
        print(node, end = " -> ")
    return result

romaniaMap = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))

mexicoMap = UndirectedGraph()

romaniaMap.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))

import pandas as pd
romaniaMapData = pd.read_csv('./AIMA/romania.csv')
print("MAP DATA\n", romaniaMapData)

romaniaMap.addMap(romaniaMapData) ## Adds to main Proble,

with open('./AIMA/data.json') as file:
    data = json.load(file)
adjacencyData = data["romania"]
print("ADJACENCY DATA\n", adjacencyData)

startNode = 'Arad'
endNode = 'Hirsova'
romaniaProblem = GraphProblem(startNode, endNode, romaniaMap)

import threading

def runRBFSasThread(problem, hFunc=None):
    thread = threading.Thread(target=RecursiveBestFirstSearch, args=(problem, hFunc))
    thread.start()
    return thread

import pandas as py, pygame, matplotlib.pyplot as plt, time
mapForVisualization = romaniaMap.map

print(mapForVisualization)
def playVisualization():
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
        purple = (128, 0, 128)
        
        font = pygame.font.Font(None, 36)
        titleText = font.render(f"{startNode}'s Map", True, black)
        mainNodeInfo = font.render("Visited Node:", True, black)
        currentPathCostText = font.render("Current Path Cost:", True, black)

        # Set the width and height of the screen
        screenWidth = 1200
        screenHeight = 800
        screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(f"{startNode} Map Visualization")

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
                    case "alternative":
                        color = purple
                    case _:
                        color = gray
                pygame.draw.circle(screen, color, (int(lng), int(lat)), 8)

            # Update the screen
            textX = (screenWidth - textWidth) // 2
            textY = 20
            screen.blit(titleText, (textX, textY))

            textY = 40
            screen.blit(mainNodeInfo, (40, textY))
            mainNodeInfo = font.render((romaniaMap.mainNodeText), True, black)

            textY = screenHeight
            screen.blit(currentPathCostText, (40, textY))
            currentPathCostText = font.render("Current Path Cost: " + str(romaniaMap.maxPath), True, black)
            
            pygame.display.flip()
        pygame.quit()

result = runRBFSasThread(romaniaProblem, None)
playVisualization()
# result = RecursiveBestFirstSearch(romaniaProblem).solution()

print("\n\nAll Visited Nodes: ", allVisitedNodes, sep = "")

