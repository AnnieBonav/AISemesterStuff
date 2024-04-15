import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from Node import Node
from State import State
from GraphProblem import GraphProblem
import json, numpy as np, time
genVerbose = True
nodeVerbose = False

print("\n\nWELCOME TO RBFS (Recursive Best First Search) ALGORITHM")

# loads the adjacency data from the json file
with open('./data.json') as file:
    data = json.load(file)

# can be changed between the different valid nodes of the json file
origin = "A"
goal = "G1"
adjacencyData_testA = data["testDataLastNode"]

problemA = GraphProblem(State(origin), State(goal), adjacencyData_testA)

if origin not in adjacencyData_testA:
    print("Origin does not exist on the problem, please change to a valid node.")
    exit()
if goal not in adjacencyData_testA:
    print("Goal does not exist on the problem, please change to a valid node.")
    exit()

runVisualization = True
# If dataHasHeuristics, then the data does not contain the adjacency (action value), but the heuristics itself, so our action cost will be 0
def RecursiveBestFirstSearch(problem : GraphProblem) -> str:

    initialNode = Node(problem.initialState, 0)

    rbfsResult = RBFS(problem, initialNode, np.inf)
    if rbfsResult[0] == None:
        return "No solution found"

    solution = rbfsResult[0].getSolution()
    print(f"Here is the result: {solution} {problem.goalState.name}")
    return

def RBFS(problem : GraphProblem, node : Node, fLimit) -> Node:
    if problem.goalTest(node.state):
        return node, 0 
    
    successors = node.expand(problem, nodeVerbose)

    if len(successors) == 0:
        return None, np.inf
    
    for succesor in successors:
        succesor.fCost = max(succesor.hCost, node.fCost)

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

testA = RecursiveBestFirstSearch(problemA)
resultsToShow = [
    # [resultA, "Results A"],
    # [resultB, "Results B"],
    # [resultC, "Results C"],
    # [resultUpsideDown, "Results Upside Down"],
    [adjacencyData_testA, f"Results Test A: Node {origin} to Node {goal}"]
    ]

for result in resultsToShow:
    print(f"\n{result[1]}", result[0], sep="\n")