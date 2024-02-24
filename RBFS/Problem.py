from State import State

# initialState: string that represents the initial state, in this case, the initial node name
# goalState: string that represents the goal state, in this case, the goal node name
# mapInformationFile: string that represents the file with the map information
class MapProblem():    
    def __init__(self, initialState: State, goalState: State, mapDict: dict):
        self.initialState : State = initialState
        self.goalState : State = goalState
        self.map : dict = mapDict

    def goalTest(self, state : State) -> bool:
        return state.name == self.goalState.name
    
    # returns a list of actions that can be taken from the current state, which are the locations that can be reached from the current location
    def actions(self, state : State) -> list[str]:
        print("State:", state.name)
        return self.map[state.name]["actions"]
    
    def result(self, state: State, action : str) -> State:
        nextState = State(action)
        return nextState
    
    def pathCost(self, currentState : State, action, nextState : State):
        fCost = self.map[nextState.name]["fCost"]
        movingCost = 0
        return fCost + movingCost
    
    """ HERE """

    def value(self, state):
        return 1

    def __repr__(self):
        return "<MapProblem initial: {}, goal: {}>".format(self.initial, self.goal)