from State import State
from Problem import GraphProblem

class Node:
    def __init__(self, state : State, fCost = 0, parent = None, action = None):
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

    def expand(self, problem : GraphProblem, verbose = False):
        children = []
        for action in problem.actions(self.state, verbose):
            actionName = action[0]
            heuristicValue = action[1]
            children.append(self.childNode(problem, actionName, heuristicValue))
        return children
    
    def __str__(self):
        return f"Node: {self.state.name}, fCost: {self.fCost}, action: {self.action}, parent: {self.parent.state.name}"
    
    # Returns a new node with the state that results from applying the given action to the current node's state (which will be a state which's name is the action's name)
    def childNode(self, problem : GraphProblem, actionName : str, heuristicValue : int):
        nextState : State = problem.result(self.state, actionName)
        cost = problem.pathCost(self.state, heuristicValue, nextState)
        return Node(nextState, cost, self, actionName)

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))