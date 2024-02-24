    
from State import State
from Problem import MapProblem

class Graph:
    def __init__(self, graphDict):
        self.graphDict = graphDict
        self.initialize()

    def initialize(self):
        """Make a digraph by adding symmetric edges."""
        for a in list(self.graphDict.keys()):
            for (b, dist) in self.graphDict[a].items():
                self.connect(b, a, dist)

    def connect(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graphDict.setdefault(A, {})[B] = distance

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graphDict.keys()])
        s2 = set([k2 for v in self.graphDict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
    
class Node:
    def __init__(self, state : State, fCost, parent = None, action = None):
        self.parent = parent
        self.fCost = fCost
        self.state = state
        self.action = action

    def changeHeuristicValue(self, newValue):
        self.fCost = newValue

    def getSolution(self):
        if self.parent == None:
            return "The initial node was the node Goal, no actions were taken"
        nodesPath = [node.action for node in self.path()[1:]]
        displayString = ""
        for i in range(len(nodesPath)):
            if i == len(nodesPath)-1:
                displayString += nodesPath[i]
                return displayString
            displayString += nodesPath[i] + " -> "
        
        return displayString

    def expand(self, problem : MapProblem):
        return [self.childNode(problem, action) for action in problem.actions(self.state)]
    
    def __str__(self):
        return f"Node: {self.state.name}, fCost: {self.fCost}, action: {self.action}, parent: {self.parent.state.name}"
    
    # Returns a new node with the state that results from applying the given action to the current node's state (which will be a state which's name is the action's name)
    def childNode(self, problem : MapProblem, action):
        nextState : State = problem.result(self.state, action)
        cost = problem.pathCost(self.state, action, nextState)
        return Node(nextState, cost, self, action)

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
