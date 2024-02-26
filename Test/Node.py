from State import State

class Node:
    def __init__(self, state : State, hCost, parent = None, action = None, ):
        self.parent = parent
        self.state = state
        self.action = action
        self.hCost = hCost
        self.fCost = self.hCost

    def getSolution(self):
        if self.parent == None:
            return "The initial node was the node Goal, no actions were taken"
        print("PATH", self.path())
        nodesPath = [node.action for node in self.path()[1:]]
        displayString = ""
        print(f"RANGE {len(nodesPath)} NodesPath: {nodesPath}")
        for i in range(len(nodesPath)):
            # print(f"Node {i}: {nodesPath[i]} type {type(nodesPath[i])}")
            if i == len(nodesPath)-1:
                return displayString
            print(f"Node {i}: {nodesPath[i][0]}")
            displayString += nodesPath[i][0] + " -> "
        
        return displayString

    def expand(self, problem, verbose = False):
        children = []
        for action in problem.actions(self.state, verbose):
            children.append(self.childNode(problem, action, verbose))
        return children
    
    # Returns a new node with the state that results from applying the given action to the current node's state (which will be a state which's name is the action's name)
    def childNode(self, problem, action, verbose = False):
        actionName = action[0]
        nextState : State = problem.result(self.state, actionName)
        nextNode = Node(state = nextState,
                        hCost = problem.hCost(self.state.name, actionName, verbose),
                        parent = self,
                        action = action,)
        return nextNode

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
            print("PARENT", node, "PATH_BACK", path_back)
        return list(reversed(path_back))
    
    def __str__(self):
        return f"Node: {self.state.name}, hCost: {self.hCost}, fCost: {self.fCost}, action: {self.action}, parent: {self.parent.state.name}"
