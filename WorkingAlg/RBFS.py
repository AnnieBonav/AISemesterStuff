from Node import Node
from State import State
from Problem import GraphProblem
import json
# problem: a problem that can be solved with a recursive best first search, in this case, a graph that represents cities locations and distances between them

verbose = True
with open('./RBFS/data.json') as file:
    data = json.load(file)

testProblemA = GraphProblem(State("A"), State("E"), data["testDataOneE"])
testProblemB = GraphProblem(State("A"), State("E"), data["testDataTwoE"])

testProblemC = GraphProblem(State("A"), State("H"), data["testDataLastNode"])
presentationExample = GraphProblem(State("A"), State("M"), data["presentationExample"])

allExpandedNodes = []
allVisitedNodes = []

def RecursiveBestFirstSearch(problem: GraphProblem) -> str:
    global allExpandedNodes, allVisitedNodes
    allExpandedNodes = []
    allVisitedNodes = []

    rbfsResult = RBFS(problem, Node(problem.initialState, 0), float('inf'))
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()
    cost = rbfsResult[1]

    return f"Here is the result: {solution}"

def RBFS(problem : GraphProblem, node : Node, f_limit) -> Node:
    global allExpandedNodes, allVisitedNodes
    if problem.goalTest(node.state):
        return node, node.fCost 
    
    allVisitedNodes.append(node.state.name)
    successors = node.expand(problem, verbose)
    for succesor in successors:
        if verbose : print("Succesor:",succesor)
        # succesor.hCost = (max(succesor.fCost, node.fCost))
        allExpandedNodes.append(succesor.state.name)

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
presentationResults = RecursiveBestFirstSearch(presentationExample)

resultsToShow = [[resultA, f"Results A from {testProblemA.initialState.name} to {testProblemA.goalState.name}"], [resultB, f"Results B from {testProblemB.initialState.name}"], [resultC, f"Results C from {testProblemC.initialState.name} to {testProblemC.goalState.name}"], [presentationResults, f"Presentation Example Results from {presentationExample.initialState.name} to {presentationExample.goalState.name}"]]

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