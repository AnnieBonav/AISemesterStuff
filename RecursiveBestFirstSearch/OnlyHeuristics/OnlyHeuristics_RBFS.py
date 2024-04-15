from Node import Node
from State import State
from Problem import GraphProblem
import json, numpy as np
verbose = False
verboseStates = True
verboseExpanded = False
print("\nWELCOME TO RECURSIVE BEST FIRST SEARCH! (only heuristics)")

with open('./OnlyHeuristics/data.json') as file:
    data = json.load(file)

testProblemA = GraphProblem(State("A"), State("B"), data["testDataOneE"])
testProblemB = GraphProblem(State("A"), State("E"), data["testDataTwoE"])

testDataLastNode = GraphProblem(State("A"), State("O"), data["testDataLastNode"])
presentationExample = GraphProblem(State("A"), State("M"), data["presentationExample"])

allExpandedNodes = []

def RecursiveBestFirstSearch(problem: GraphProblem) -> str:
    global allExpandedNodes
    allExpandedNodes = [] # Used for visualization purposes

    # Initialize search with initial Node and start recursion
    rbfsResult = RBFS(problem, Node(problem.initialState), float('inf'))
    if rbfsResult[0] == None:
        if verboseStates : print("FAILURE No solution found")
        return "No solution found"
    
    return f"Here is the result: {problem.initialState.name} -> {rbfsResult[0].getSolution()}"

def RBFS(problem : GraphProblem, node : Node, f_limit) -> Node:
    global allExpandedNodes

    # Check if node is the goal
    if problem.goalTest(node.state):
        if verboseStates : print("GOAL REACHED")
        return node, node.fCost 
    
    # Expand the node: get initialized children
    children = node.expand(problem, verbose)

    # If there are no more children, return None and infinity
    if len(children) == 0:
        if verboseStates : print("NO MORE CHILDREN")
        return None, np.inf
    
    for child in children:
        if verbose : print("Child:",child)
        child.hCost = (max(child.fCost, node.fCost))
        allExpandedNodes.append(child.state.name) ## Visualization

    while True:
        children.sort(key=lambda x: x.fCost)
        best = children[0]

        # If the best node's fCost is greater than the f_limit, return None and the f_limit (so the parent can choose the next best node to expand on)
        if best.fCost > f_limit:
            if verboseStates : print("BEST HIGHER F LIMIT")
            return None, best.fCost
        
        # Get the second best node
        alternative = children[1].fCost if len(children) > 1 else np.inf
        # Recurse on the best node
        result, best.fCost = RBFS(problem, best, min(f_limit, alternative))

        # Check failure conditions
        if result is None and best.fCost == np.inf:
            return None, np.inf
        
        if result is not None:
            if verboseStates : print("RESULTING")
            return result, best.fCost

if verboseStates : print("\nTEST A\n")   
resultA = RecursiveBestFirstSearch(testProblemA)
if verboseStates : print("\nTEST B\n")   
resultB = RecursiveBestFirstSearch(testProblemB)
if verboseStates : print("\nTEST LAST NODE\n")
resultC = RecursiveBestFirstSearch(testDataLastNode)
if verboseStates : print("\nPRESENTATION\n")   
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

print("\n\n** RESULTS **")
for result in resultsToShow:
    if verboseExpanded:
        print(f"{result[1]}", result[0], f"All #{len(allExpandedNodes)} expanded nodes: {nodesString()}")
        continue
    print(f"{result[1]}, {result[0]}")