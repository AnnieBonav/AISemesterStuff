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

mexicoMap = Map("Mexico")

verbose = True
with open('./RBFS/data.json') as file:
    data = json.load(file)

origin = "Monterrey"
goal = "Tijuana"
mexico1Node = MapProblem(State(origin), State(goal), data["mexico1Node"], mexicoMap)

counter = 0
hCostFunction = None

best = None
alternative = None
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
    
    successors = node.expand(problem, verbose)

    if len(successors) == 0:
        return None, np.inf
    
    for succesor in successors:
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

        result, best.fCost = RBFS(problem, best, min(fLimit, alternative))
        if result is not None: # if result would also work
            return result, best.fCost
    
# resultA = RecursiveBestFirstSearch(testProblemA, True, False)
# resultB = RecursiveBestFirstSearch(testProblemB)
# resultC = RecursiveBestFirstSearch(testProblemC)

# resultUpsideDown = RecursiveBestFirstSearch(testUpsideDown)

resultMexico1Node = RecursiveBestFirstSearch(mexico1Node, None)
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