from State import State

class Node:
    def __init__(self, state : State, parent = None, action = None, pathCost = 0):
        self.parent = parent
        self.state = state
        self.action = action
        self.pathCost = pathCost

    def getSolution(self):
        if self.parent == None:
            return "The initial node was the node Goal, no actions were taken"
        nodesPath = [node.action for node in self.path()[1:]]
        displayString = ""
        for i in range(len(nodesPath)):
            print(f"Node {i}: {nodesPath[i]} type {type(nodesPath[i])}")
            if i == len(nodesPath)-1:
                return displayString
            displayString += nodesPath[i][0] + " -> "
        
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
        nextState : State = problem.result(self.state, actionName)
        nextNode = Node(nextState, self, action, problem.pathCost(self.pathCost, self.state, action, nextState))
        return nextNode

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
    def __str__(self):
        return f"Node: {self.state.name}, fCost: {self.fCost}, action: {self.action}, parent: {self.parent.state.name}"
