from State import State
from Map import Map
import numpy as np
from Node import Node

# initialState: string that represents the initial state, in this case, the initial node name
# goalState: string that represents the goal state, in this case, the goal node name
# mapInformationFile: string that represents the file with the adjacencyMap information
class MapProblem():    
    def __init__(self, initialState: State, goalState: State, mapDict: dict, map : Map = None):
        self.initialState : State = initialState
        self.goalState : State = goalState
        self.adjacencyMap : dict = mapDict
        self.map = map

    def hCost(self, node : Node, verbose = False):
        """hCost function is the eucledian distance from a node's state to goal."""
        if verbose: print("\nNode:", node.state.name, "Goal:", self.goalState.name, "Distance:", self.map.getEuclideanDistance(node.state.name, self.goalState.name))
        return self.map.getEuclideanDistance(node.state.name, self.goalState.name)
        
    def goalTest(self, state : State) -> bool:
        return state.name == self.goalState.name
    
    # returns a list of actions that can be taken from the current state, which are the locations that can be reached from the current location
    def actions(self, state : State, verbose = False) -> list[str]:
        if verbose : print("\nState:", state.name, "\nADJACENCY\n", self.adjacencyMap[state.name], sep = "")
        return self.adjacencyMap[state.name]
    
    def result(self, state: State, actionName : str) -> State:
        nextState = State(actionName)
        return nextState
    
    def pathCost(self, costSoFar, currentState : State, action : str, nextState : State, verbose = False):
        for action in self.adjacencyMap[currentState.name]:
            if action[0] == nextState.name:
                actionCost = action[1]
        pathCost = costSoFar + (actionCost or np.inf)
        if verbose : print(f"Costs between {currentState.name} | {nextState.name}: Cost so far: {costSoFar}, ActionCost: {actionCost} PathCost:  {pathCost}")
        return pathCost
    
    """ HERE """

    def value(self, state):
        return 1

    def __repr__(self):
        return "<MapProblem initial: {}, goal: {}>".format(self.initialState, self.goalState)