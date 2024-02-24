from HelperClasses import Graph, Node, State
from Problem import MapProblem
import json
# problem: a problem that can be solved with a recursive best first search, in this case, a graph that represents cities locations and distances between them

verbose = True
with open('./RBFS/data.json') as file:
    data = json.load(file)

testProblemA = MapProblem(State("A"), State("E"), data["testDataOneE"])
testProblemB = MapProblem(State("A"), State("E"), data["testDataTwoE"])

testProblemC = MapProblem(State("A"), State("H"), data["testDataLastNode"])
testUpsideDown = MapProblem(State("A"), State("E"), data["testUpsideDown"])

allExpandedNodes = []
allVisitedNodes = []

def RecursiveBestFirstSearch(problem: MapProblem) -> str:
    global allExpandedNodes, allVisitedNodes
    allExpandedNodes = []
    allVisitedNodes = []

    rbfsResult = RBFS(problem, Node(problem.initialState, 0), float('inf'))
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()
    cost = rbfsResult[1]

    return f"Here is the result: {solution}, with a cost of {cost}"

def RBFS(problem : MapProblem, node : Node, f_limit) -> Node:
    global allExpandedNodes, allVisitedNodes
    if problem.goalTest(node.state):
        return node, node.fCost 
    
    allVisitedNodes.append(node.state.name)
    successors = node.expand(problem, verbose)
    for succesor in successors:
        if verbose : print("Succesor:",succesor)
        allExpandedNodes.append(succesor.state.name)
        # succesor.changeHeuristicValue(max(succesor.fCost, node.fCost))

    if len(successors) == 0:
        return None, float('inf')

    while True:
        successors.sort(key=lambda x: x.fCost)
        best = successors[0]
        if best.fCost > f_limit:
            return None, best.fCost
        
        alternative = successors[1].fCost if len(successors) > 1 else float('inf')
        result, best.fCost = RBFS(problem, best, min(f_limit, alternative))

        if result is not None: # if result would also work
            return result, best.fCost
    
resultA = RecursiveBestFirstSearch(testProblemA)
resultB = RecursiveBestFirstSearch(testProblemB)
resultC = RecursiveBestFirstSearch(testProblemC)

resultUpsideDown = RecursiveBestFirstSearch(testUpsideDown)

resultsToShow = [[resultA, "Results A"], [resultB, "Results B"], [resultC, "Results C"], [resultUpsideDown, "Results Upside Down"]]

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