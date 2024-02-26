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

testProblemA = MapProblem(State("A"), State("E"), data["testDataOneE"])
testProblemB = MapProblem(State("A"), State("E"), data["testDataTwoE"])

testProblemC = MapProblem(State("A"), State("H"), data["testDataLastNode"])
testUpsideDown = MapProblem(State("A"), State("E"), data["testUpsideDown"])

mexico1Node = MapProblem(State("Campeche"), State("La Paz"), data["mexico1Node"], mexicoMap)
allExpandedNodes = []
allVisitedNodes = []

counter = 0
hCostFunction = None

best = None
alternative = None
# If dataHasHeuristics, then the data does not contain the adjacency (action value), but the heuristics itself, so our action cost will be 0
def RecursiveBestFirstSearch(problem : MapProblem, hFunc = None) -> str:
    global allExpandedNodes, allVisitedNodes, hCostFunction
    allExpandedNodes = []
    allVisitedNodes = []

    hCostFunction = memoize(hFunc or problem.hCost, 'hCost')
    initialNode = Node(problem.initialState, 0)
    initialNode.fCost = hCostFunction(initialNode)

    rbfsResult = RBFS(problem, initialNode, np.inf)
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()
    cost = rbfsResult[1]

    return f"Here is the result: {solution}, with a cost of {cost}"

def RBFS(problem : MapProblem, node : Node, fLimit) -> Node:
    global counter, allExpandedNodes, allVisitedNodes, best, alternative
    counter += 1

    print("\nNODE:", node.state.name, "fCost:", node.fCost, "fLimit:", fLimit, "Counter:", counter, "GoalTest:", problem.goalTest(node.state)   )

    if type(best) == Node:
        print("\nBEST Node: ", best.state.name, "Best fCost: ", best.fCost)
    print("Alternative", alternative)

    if problem.goalTest(node.state):
        #return node, node.fCost 
        return node, 0 
    
    allVisitedNodes.append(node.state.name) # Just for visualizing
    successors = node.expand(problem, verbose)

    if len(successors) == 0:
        return None, np.inf
    
    for succesor in successors:
        # if verbose : print("Succesor:",succesor)
        allExpandedNodes.append(succesor.state.name)
        pathCost = succesor.pathCost
        hCost = hCostFunction(succesor)
        print("\nSuccesor:", succesor.state.name, "pathCost:", succesor.pathCost, "hCost:", hCostFunction(succesor))
        succesor.fCost = (max(pathCost + hCost, node.fCost))
        print("Succesor NEW fCost:", succesor.fCost)

        if problem.goalTest(succesor.state):
            return succesor, succesor.fCost 
    while True:
        successors.sort(key=lambda x: x.fCost)
        best = successors[0]
        print("\nBest Node:", best.state.name, "Best fCost:", best.fCost, "fLimit:", fLimit)

        if best.fCost > fLimit:
            print("RETURNING")
            return None, best.fCost
        
        if len(successors) > 1:
            alternative = successors[1].fCost
            for successor in successors[1:]:
                print("\nSUCCS:", successor.state.name, "fCost:", successor.fCost)
            # best.fCost = min(successor.fCost for successor in successors[1:])
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
    print(f"\n{result[1]}", result[0], f"All #{len(allVisitedNodes)} visited nodes: {nodesString('visited')}", f"All #{len(allExpandedNodes)} expanded nodes: {nodesString('expanded')}", sep="\n")