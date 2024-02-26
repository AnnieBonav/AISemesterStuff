from State import State
import numpy as np
from Node import Node

# initialState: string that represents the initial state, in this case, the initial node name
# goalState: string that represents the goal state, in this case, the goal node name
class GraphProblem():    
    def __init__(self, initialState: State, goalState: State, mapDict: dict):
        self.initialState : State = initialState
        self.goalState : State = goalState
        self.adjacencyMap : dict = mapDict
        self.map = map

    def hCost(self, currentNodeName : str, nextNodeName : Node, verbose = False):
        for action in self.adjacencyMap[currentNodeName]:
            if action[0] == nextNodeName:
                heuristic = action[1]
        return heuristic
        
    def goalTest(self, state : State) -> bool:
        return state.name == self.goalState.name
    
    # returns a list of actions that can be taken from the current state, which are the locations that can be reached from the current location
    def actions(self, state : State, verbose = False) -> list[str]:
        if verbose : print("\nState:", state.name, "\nADJACENCY\n", self.adjacencyMap[state.name], sep = "")
        return self.adjacencyMap[state.name]
    
    def result(self, state: State, actionName : str) -> State:
        nextState = State(actionName)
        return nextState
    
    def value(self, state):
        return 1

    def __repr__(self):
        return "<MapProblem initial: {}, goal: {}>".format(self.initialState, self.goalState)