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


"""
def RecursiveBestFirstSearch(problem : MapProblem, hFunc = None) -> str:
    global hCostFunction
    hCostFunction = memoize(hFunc or problem.hCost, 'hCost')

    initialNode = Node(problem.initialState)
    initialNode.fCost = hCostFunction(initialNode, nodeVerbose)

    mexicoMap.updateState(initialNode.state.name, "start")
    rbfsResult = RBFS(problem, initialNode, np.inf)
    if rbfsResult[0] == None:
        return "No solution found"
    
    mexicoMap.resetAllStates()
    mexicoMap.updateState(rbfsResult[0].state.name, "goal")
    solution = rbfsResult[0].getSolution()
    print(f"Here is the result: {solution} {problem.goalState.name}, with a cost of {rbfsResult[0].pathCost}")
    return

def RBFS(problem : MapProblem, node : Node, fLimit) -> Node:
    global best, alternative
    if problem.goalTest(node.state):
        return node, 0 
    
    successors = node.expand(problem, nodeVerbose)

    if len(successors) == 0:
        return None, np.inf
    
    for succesor in successors:
        pathCost = succesor.pathCost
        hCost = hCostFunction(succesor)
        succesor.fCost = max(pathCost + hCost, node.fCost)

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


mexicoMap = UndirectedGraph(dict(
    Acapulco=dict(Morelia=343,Ecatepec=305,Cuernavaca=236,Puebla=294,Oaxaca=321),
    Apizaco=dict(Ecatepec=96, Pachuca=101,Puebla=40),
    Aguascalientes=dict(Guadalajara=174,Guadalupe=99),
    Campeche" : [["Merida", 262], ["Cancun", 196], ["Villahermosa", 199]],

        "Cancun" : [["Merida", 229], ["Campeche", 196]],

        "Cuernavaca" : [["Acapulco de Juarez", 236], ["Ecatepec", 69], ["Puebla", 110]],
                
        "Culiacan" : [["Hermosillo", 593], ["Juarez", 768], ["Durango", 255], ["Tepic", 448]],

        "Durango" : [["Culiacan", 255], ["Juarez", 757], ["Saltillo", 394], ["Guadalupe", 345], ["Tepic", 387]],

        "Ecatepec" : [["Acapulco de Juarez", 305], ["Morelia", 226], ["Queretaro", 185], ["Pachuca", 68], ["Apizaco", 96], ["Puebla", 103], ["Cuernavaca", 69]],

        "Guadalajara" : [["Tepic", 183], ["Guadalupe", 246], ["Aguascalientes", 174], ["San Luis Potosi", 294], ["Leon de los Aldama", 232], ["Morelia", 250], ["Manzanillo", 201]],
        
        "Guadalupe" : [["Monterrey", 394], ["San Luis Potosi", 170], ["Aguascalientes", 99], ["Guadalajara", 246], ["Tepic", 281], ["Durango", 345], ["Leon de los Aldama", 244], ["Saltillo", 336]],

        "Hermosillo" : [["Tijuana", 687], ["Juarez", 522], ["Culiacan", 593]],

        "Juarez" : [["Saltillo", 869], ["Durango", 757], ["Culiacan", 768], ["Hermosillo", 522]],

        "Leon de los Aldama" : [["Morelia", 141], ["Guadalajara", 232], ["Guadalupe", 244], ["San Luis Potosi", 131], ["Queretaro", 85]],

        "Manzanillo" : [["Guadalajara", 201], ["Morelia", 336]],

        "Merida" : [["Cancun", 229], ["Campeche", 262]],

        "Monterrey" : [["Reynosa", 205], ["San Luis Potosi", 399], ["Guadalupe", 394], ["Saltillo", 73]],

        "Morelia" : [["Manzanillo", 336], ["Guadalajara", 250], ["Leon de los Aldama", 141], ["Queretaro", 130], ["Ecatepec", 226], ["Acapulco de Juarez", 343]],

        "Oaxaca" : [["Acapulco de Juarez", 321], ["Puebla", 269], ["Veracruz", 249], ["Tuxtla", 396]],

        "Pachuca" : [["San Luis Potosi", 322], ["Veracruz", 292], ["Puebla", 130], ["Apizaco", 101], ["Ecatepec", 68], ["Queretaro", 179]],

        "Puebla" : [["Acapulco de Juarez", 294], ["Ecatepec", 103], ["Cuernavaca", 110], ["Apizaco", 40], ["Pachuca", 130], ["Veracruz", 216], ["Oaxaca", 269]],

        "Queretaro" : [["Morelia", 130], ["Leon de los Aldama", 85], ["San Luis Potosi", 181], ["Pachuca", 179], ["Ecatepec", 185]],

        "Reynosa" : [["Veracruz", 797], ["San Luis Potosi", 514], ["Monterrey", 205]],

        "San Luis Potosi" : [["Reynosa", 514], ["Veracruz", 600], ["Pachuca", 322], ["Queretaro", 181], ["Leon de los Aldama", 131], ["Guadalajara", 294], ["Guadalupe", 170], ["Saltillo", 366], ["Monterrey", 399]],
        
        "Saltillo" : [["Monterrey", 73], ["San Luis Potosi", 366], ["Guadalupe", 336], ["Durango", 394], ["Juarez", 869]],

        "Tepic" : [["Culiacan", 448], ["Durango", 387], ["Guadalupe", 281], ["Guadalajara", 183]],

        "Tijuana" : [["Hermosillo", 687]],

        "Tuxtla" : [["Oaxaca", 396], ["Veracruz", 421], ["Villahermosa", 138]],

        "Veracruz" : [["Villahermosa", 364], ["Tuxtla", 421], ["Reynosa", 797], ["Oaxaca", 249], ["Puebla", 216], ["Pachuca", 292], ["San Luis Potosi", 600]],

        "Villahermosa" : [["Campeche", 199], ["Tuxtla", 138], ["Veracruz", 364]]
    }
}
"""