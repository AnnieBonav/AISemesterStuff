from State import State

class Node:
    def __init__(self, state : State, fCost, parent = None, action = None):
        self.parent = parent
        self.fCost = fCost
        self.state = state
        self.action = action

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

    def expand(self, problem, verbose = False):
        children = []
        for action in problem.actions(self.state, verbose):
            # TODO: Here would be the checking if the value is heuristics or action cost
            children.append(self.childNode(problem, action))
        return children
    
    # Returns a new node with the state that results from applying the given action to the current node's state (which will be a state which's name is the action's name)
    def childNode(self, problem, action):
        actionName = action[0]
        actionCost = action[1]
        nextState : State = problem.result(self.state, actionName)
        cost = problem.pathCost(self.fCost, self.state, actionCost, nextState)
        return Node(nextState, cost, self, actionName)

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
    def __str__(self):
        return f"Node: {self.state.name}, fCost: {self.fCost}, action: {self.action}, parent: {self.parent.state.name}"
