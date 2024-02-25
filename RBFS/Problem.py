from State import State
from Map import Map
import numpy as np

# initialState: string that represents the initial state, in this case, the initial node name
# goalState: string that represents the goal state, in this case, the goal node name
# mapInformationFile: string that represents the file with the adjacencyMap information
class MapProblem():    
    def __init__(self, initialState: State, goalState: State, mapDict: dict, map : Map = None, heuristicsDict = None):
        self.initialState : State = initialState
        self.goalState : State = goalState
        self.adjacencyMap : dict = mapDict
        self.map = map
        self.heuristicsDict = heuristicsDict

        # if there is a map, then we need to calculate the heuristic values
        if self.map != None:
            self.calculateHeuristicValues()

    # calculates the heuristic values for the nodes of the map
    def calculateHeuristicValues(self):
        print("\n\nCalculating heuristic values")
        for state in self.adjacencyMap:
            print("State:", state, "Distance:", self.map.getEuclideanDistance(state, self.goalState.name))
            self.heuristicsDict[state] = self.map.getEuclideanDistance(state, self.goalState.name)
    
    def goalTest(self, state : State) -> bool:
        return state.name == self.goalState.name
    
    # returns a list of actions that can be taken from the current state, which are the locations that can be reached from the current location
    def actions(self, state : State, verbose = False) -> list[str]:
        if verbose : print("\nState:", state.name)
        print("ADJACENCY\n", self.adjacencyMap[state.name])
        return self.adjacencyMap[state.name]
    
    def result(self, state: State, actionName : str) -> State:
        nextState = State(actionName)
        return nextState
    
    def pathCost(self, costSoFar, currentState : State, heuristicsValue : int, nextState : State, actionCost : int):
        hCost = 0
        if heuristicsValue == 0 or None:
            hCost = self.heuristicsDict[nextState.name]
        fCost = costSoFar + (hCost or np.inf)
        print("Costs:", fCost, " Next State:", nextState.name)
        return fCost
    
    """ HERE """

    def value(self, state):
        return 1

    def __repr__(self):
        return "<MapProblem initial: {}, goal: {}>".format(self.initialState, self.goalState)