import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from HelperClasses import Graph, Node, State
from Problem import MapProblem
from Map import Map
import json
# problem: a problem that can be solved with a recursive best first search, in this case, a graph that represents cities locations and distances between them

mexicoMap = Map("Mexico")

verbose = True
with open('./RBFS/data.json') as file:
    data = json.load(file)

testProblemA = MapProblem(State("A"), State("E"), data["testDataOneE"])
testProblemB = MapProblem(State("A"), State("E"), data["testDataTwoE"])

testProblemC = MapProblem(State("A"), State("H"), data["testDataLastNode"])
testUpsideDown = MapProblem(State("A"), State("E"), data["testUpsideDown"])

mexico1Node = MapProblem(State("Cuernavaca"), State("Veracruz"), data["mexico1Node"], mexicoMap, data["mexico1NodeHeuristics"])
allExpandedNodes = []
allVisitedNodes = []
hasHeuristics = False
hasActionCost = False

counter = 0
def RecursiveBestFirstSearch(problem : MapProblem, willHaveHeuristics : bool, willHaveActionCost : bool) -> str:
    global allExpandedNodes, allVisitedNodes, hasHeuristics, hasActionCost
    allExpandedNodes = []
    allVisitedNodes = []
    hasHeuristics = willHaveHeuristics
    hasActionCost = willHaveActionCost

    rbfsResult = RBFS(problem, Node(problem.initialState, 0), float('inf'))
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()
    cost = rbfsResult[1]

    return f"Here is the result: {solution}, with a cost of {cost}"

def RBFS(problem : MapProblem, node : Node, f_limit) -> Node:
    global counter
    counter += 1
    global allExpandedNodes, allVisitedNodes
    if problem.goalTest(node.state) or counter > 10:
        return node, node.fCost 
    
    allVisitedNodes.append(node.state.name)
    successors = node.expand(problem, hasHeuristics, hasActionCost, verbose)
    for succesor in successors:
        # if verbose : print("Succesor:",succesor)
        allExpandedNodes.append(succesor.state.name)
        succesor.changeHeuristicValue(max(succesor.fCost, node.fCost))

    if len(successors) == 0:
        return None, float('inf')

    while True:
        successors.sort(key=lambda x: x.fCost)
        best = successors[0]
        if best.fCost > f_limit:
            return None, best.fCost
        
        alternative = successors[1].fCost if len(successors) > 1 else float('inf')
        # result, best.fCost = RBFS(problem, best, min(f_limit, alternative))

        result, newfCost = RBFS(problem, best, min(f_limit, alternative))
        bestIndex = successors.index(best)
        successors[bestIndex].changeHeuristicValue(newfCost)

        if result is not None: # if result would also work
            return result, best.fCost
    
# resultA = RecursiveBestFirstSearch(testProblemA, True, False)
# resultB = RecursiveBestFirstSearch(testProblemB)
# resultC = RecursiveBestFirstSearch(testProblemC)

# resultUpsideDown = RecursiveBestFirstSearch(testUpsideDown)

resultMexico1Node = RecursiveBestFirstSearch(mexico1Node, False, True)
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