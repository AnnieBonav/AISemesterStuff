from State import State
from Classes import Needs, Action

import numpy as np

class Agent:
    """Class representing an Agent, in this project, Perry the Platypus."""

    def __init__(self, name : str, day, states):
        # hunger_level : State, tiredness_level : State, bladder_level : State
        self.name = name
        self.states = states

        self.actions_history = []
        self.fake_time = True
        self.day = day

    # TODO: Maybe need to change the specific actions to be just one "do action" ufnction that is based on the enums
    def go_bathroom(self, action : Action):
        if self.fake_time:
            self.day.fake_pass_time(action.time_in_min, "bathroom", action.name)

        self.states["bladder"].decrease(action.value) # Decreases the need of going to bathroom
        print(action)


    def eat(self, action : Action):
        # First fake time so the decreased values make more sense, will be different when implemented in unity as time will pass in real time
        if self.fake_time:
            self.day.fake_pass_time(action.time_in_min, "eat", action.name)

        self.states["hunger"].decrease(action.value)
        print(action)

    def sleep(self, action : Action):
        if self.fake_time:
            self.day.fake_pass_time(action.time_in_min, "sleep", action.name)
            # "activity" and "action" can be passed through the observables in unity, for now some weird arquitecture is used, but its fine for now :)

        self.states["tiredness"].decrease(action.value)
        print(action)

    def solve_crime(self, action : Action):
        if self.fake_time:
            self.day.fake_pass_time(action.time_in_min, "solve_crime", action.name)

        self.states["detectiveness"].decrease(action.value)
        print(action)

    def relax(self, action : Action):
        if self.fake_time:
            self.day.fake_pass_time(action.time_in_min, "relax", action.name)

        self.states["relaxation"].decrease(action.value)
        print(action)

    def pass_time(self, minutes, activity = None, action = None):
        hunger_increase = round(1/2.4, 4)
        tiredness_increase = round(1/9.6, 4)
        bladder_increase = round(1/1.8, 4)
        detectiveness_increase = round(1/6.2, 4) # No reason
        relaxation_increase = round(1/4.8, 4) # No reason

        for _ in range(minutes):
            # want to eat every 4 hours (240 min) then hunger increases by 1/0.24 every 10 min tick
            self.states["hunger"].increase(hunger_increase)

            # want to sleep every 16 hours (960 min) then tiredness increases by 1/0.96 every 10 min tick
            self.states["tiredness"].increase(tiredness_increase)

            # want to go to the bathroom every 2 hours, then bladder increases by 1/0.18 every 10 min tick
            self.states["bladder"].increase(bladder_increase)

            self.states["detectiveness"].increase(detectiveness_increase)
            self.states["relaxation"].increase(relaxation_increase)

        info_json = {"current_time" : self.day.time, "entry_type" : "time_increase", "delta_mins" : minutes, "character_name": self.name, "hunger_increase": hunger_increase, "tiredness_increase": tiredness_increase, "bladder_increase": bladder_increase, "detectiveness_increase" : detectiveness_increase, "relaxation_increase" : relaxation_increase, "modified_hunger_value" : self.states["hunger"].current_value, "modified_tiredness_value" : self.states["tiredness"].current_value, "modified_bladder_value" : self.states["bladder"].current_value, "modified_detectiveness_value" : self.states["detectiveness"].current_value, "modified_relaxation_value" : self.states["relaxation"].current_value}

        if activity:
            info_json["called_by_activity"] = activity
            info_json["specific_action"] = action
            # info_json["action_increase_index"] = i

        self.actions_history.append(info_json)

    def print_actions_history(self):
        print("\n\nActions History")
        for action in self.actions_history:
            print("\n",action)

    def __str__(self):
        return f"{self.name} T{self.day.time} - Hunger: {self.states['hunger'].current_value}, Tiredness: {self.states['tiredness'].current_value}, Bladder: {self.states['bladder'].current_value}, Detectiveness: {self.states['detectiveness'].current_value}, Relaxation: {self.states['relaxation'].current_value}"
    
    def choose_random_activity(self):
        # The agent should choose a random activity
        return np.random.choice(list(self.states.keys()))
    
    def choose_activity(self, verbose = False):
        # The agent should choose the activity based on the needs, using bayes and the exponential functions of the needs

        highest_probability = 0
        chosen_activity = None

        for key in self.states.keys():
            probability = self.states[key].get_probability(verbose)
            if probability > highest_probability:
                highest_probability = probability
                chosen_activity = key

        return self.states[chosen_activity].need
