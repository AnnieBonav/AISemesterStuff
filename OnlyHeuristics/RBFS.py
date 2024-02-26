from Node import Node
from State import State
from Problem import GraphProblem
import json
verbose = False

print("\nWELCOME TO RECURSIVE BEST FIRST SEARCH! (only heuristics)")

with open('./WorkingAlg/data.json') as file:
    data = json.load(file)

testProblemA = GraphProblem(State("A"), State("E"), data["testDataOneE"])
testProblemB = GraphProblem(State("A"), State("E"), data["testDataTwoE"])

testDataLastNode = GraphProblem(State("A"), State("G"), data["testDataLastNode"])
presentationExample = GraphProblem(State("A"), State("M"), data["presentationExample"])

allExpandedNodes = []

def RecursiveBestFirstSearch(problem: GraphProblem) -> str:
    global allExpandedNodes
    allExpandedNodes = []

    rbfsResult = RBFS(problem, Node(problem.initialState, 0), float('inf'))
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()

    return f"Here is the result: {problem.initialState.name} -> {solution}"

def RBFS(problem : GraphProblem, node : Node, f_limit) -> Node:
    global allExpandedNodes
    if problem.goalTest(node.state):
        return node, node.fCost 
    
    successors = node.expand(problem, verbose)
    for succesor in successors:
        if verbose : print("Succesor:",succesor)
        succesor.hCost = (max(succesor.fCost, node.fCost))
        allExpandedNodes.append(succesor.state.name) ## Visualization

    if len(successors) == 0:
        return None, float('inf')

    while True:
        successors.sort(key=lambda x: x.fCost)
        best = successors[0]
        if best.fCost > f_limit:
            return None, best.fCost
        
        alternative = successors[1].fCost if len(successors) > 1 else float('inf')
        result, best.fCost = RBFS(problem, best, min(f_limit, alternative))

        if result is not None:
            return result, best.fCost
    
resultA = RecursiveBestFirstSearch(testProblemA)
resultB = RecursiveBestFirstSearch(testProblemB)
resultC = RecursiveBestFirstSearch(testDataLastNode)
presentationResults = RecursiveBestFirstSearch(presentationExample)

resultsToShow = [[resultA, f"Results A from {testProblemA.initialState.name} to {testProblemA.goalState.name}"], [resultB, f"Results B from {testProblemB.initialState.name} to {testProblemB.goalState.name}"], [resultC, f"Results C from {testDataLastNode.initialState.name} to {testDataLastNode.goalState.name}"], [presentationResults, f"Presentation Example Results from {presentationExample.initialState.name} to {presentationExample.goalState.name}"]]

def nodesString() -> str:
    nodesString = ""
    nodesToTurnToString = allExpandedNodes

    for i in range(len(nodesToTurnToString)):
        if i == len(nodesToTurnToString)-1:
            return nodesString + nodesToTurnToString[i]
        nodesString += nodesToTurnToString[i] + " -> "

    return nodesString

for result in resultsToShow:
    print(f"\n{result[1]}", result[0], f"All #{len(allExpandedNodes)} expanded nodes: {nodesString()}", sep="\n")