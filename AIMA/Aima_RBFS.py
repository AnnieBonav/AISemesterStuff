from Node import Node
from utils import memoize
from GraphProblem import GraphProblem
from UnidirectedGraph import UndirectedGraph
import numpy as np

allVisitedNodes = []

print("\nWELCOME to Recursive Best First Search (RBFS)")
def recursive_best_first_search(problem, hCost=None):
    hCost = memoize(hCost or problem.hCost, 'hCost')

    def RBFS(problem, node, flimit):
        allVisitedNodes.append(node.state) # For visualization

        if problem.goal_test(node.state):
            return node, 0
        
        children = node.expand(problem)

        if len(children) == 0:
            return None, np.inf
        
        for child in children:
            child.fCost = max(child.pathCost + hCost(child), node.fCost)
        while True:
            # Order by lowest fCost value
            children.sort(key=lambda x: x.fCost)
            best = children[0]
            if best.fCost > flimit:
                return None, best.fCost
            if len(children) > 1:
                alternative = children[1].fCost
            else:
                alternative = np.inf
            result, best.fCost = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.fCost

    node = Node(problem.initial)
    node.fCost = hCost(node)
    result, bestf = RBFS(problem, node, np.inf)
    return result

romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))
romania_map.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))

startNode = 'Arad'
endNode = 'Bucharest'
romania_problem = GraphProblem(startNode, endNode, romania_map)
result = recursive_best_first_search(romania_problem).solution()

print(f"\nPATH from {startNode} to {endNode}")
for node in result:
    print(node, end = " -> ")

print("\n\nAll Visited Nodes: ", allVisitedNodes, sep = "")

