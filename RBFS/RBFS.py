from HelperClasses import Graph, Node, State
from Problem import MapProblem
import json
# problem: a problem that can be solved with a recursive best first search, in this case, a graph that represents cities locations and distances between them

with open('./RBFS/data.json') as file:
    testData = json.load(file)["testData"]

testProblem = MapProblem(State("A"), State("D"), testData)

def RecursiveBestFirstSearch(problem: MapProblem) -> str:
    rbfsResult = RBFS(problem, Node(problem.initialState, 0), float('inf'))
    if rbfsResult[0] == None:
        return "No solution found"
    
    solution = rbfsResult[0].getSolution()
    cost = rbfsResult[1]

    return f"Here is the result: {solution}, with a cost of {cost}"

def RBFS(problem : MapProblem, node : Node, f_limit) -> Node:
    if problem.goalTest(node.state):
        return node, node.fCost 
    
    successors = node.expand(problem)
    for succesor in successors:
        print("Succesor:",succesor)
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
    
result = RecursiveBestFirstSearch(testProblem)
print(result)