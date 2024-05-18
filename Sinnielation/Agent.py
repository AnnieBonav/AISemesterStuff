from State import State
from Classes import Needs, Action

import numpy as np

class Agent:
    """Class representing an Agent, in this project, Perry the Platypus."""

    def __init__(self, name : str):
        # hunger_level : State, tiredness_level : State, bladder_level : State
        self.name = name
        self.hunger = State(Needs.HL, 0, 100)
        self.tiredness = State(Needs.TL, 0, 100)
        self.bladder = State(Needs.BL, 0, 100)
        self.time = 0

        self.fake_time = True
        self.actions_history = []

    def go_bathroom(self, action : Action):
        # TODO: Value should be calculated based on the activity (how much time they spent on the bathroom)
        self.bladder.decrease(action.value) # Decreases the need of going to bathroom
        print(action)

        if self.fake_time:
            self.tick_10_min(action.time_in_10_min, "go_bathroom", action.name)

    def eat(self, action : Action):
        # TODO: Value should be calculated based on the activity (what they ate)
        self.hunger.decrease(action.value)
        print(action)

        if self.fake_time:
            self.tick_10_min(action.time_in_10_min, "eat", action.name)

    def sleep(self, action : Action):
        # TODO: Value should be calculated based on the activity (how much time they slept)
        self.tiredness.decrease(action.value)
        print(action)

        if self.fake_time:
            self.tick_10_min(action.time_in_10_min, "sleep", action.name)

    def tick_10_min(self, times, activity = None, action = None):
        hunger_increase = round(1/0.24, 3)
        tiredness_increase = round(1/0.96, 3)
        bladder_increase = round(1/0.18, 3)

        for i in range(times):
            # Simulates the passage of time, specifically 10 minutes for now
            # TODO: This should be based on the real time, and on how each need is affected by the time
            
            # want to eat every 4 hours (240 min) then hunger increases by 1/0.24 every 10 min tick
            self.hunger.increase(hunger_increase)

            # want to sleep every 16 hours (960 min) then tiredness increases by 1/0.96 every 10 min tick
            self.tiredness.increase(tiredness_increase)

            # want to go to the bathroom every 2 hours, then bladder increases by 1/0.18 every 10 min tick
            self.bladder.increase(bladder_increase)

            info_json = {"current_time" : self.time, "entry_type" : "time_increase", "delta_mins" : "10", "character_name": self.name, "hunger_increase": hunger_increase, "tiredness_increase": tiredness_increase, "bladder_increase": bladder_increase, "modified_hunger_value" : self.hunger.current_value, "modified_tiredness_value" : self.tiredness.current_value, "modified_bladder_value" : self.bladder.current_value}

            if activity:
                info_json["called_by_activity"] = activity
                info_json["specific_action"] = action
                info_json["action_increase_index"] = i

            self.actions_history.append(info_json)
            self.time += 10

    def print_actions_history(self):
        print("\n\nActions History")
        for action in self.actions_history:
            print("\n",action)

    def __str__(self):
        return f"{self.name} - Hunger: {self.hunger.current_value}, Tiredness: {self.tiredness.current_value}, Bladder: {self.bladder.current_value}"
    
    def choose_activity(self):
        # The agent should choose the activity based on the needs, using bayes and the exponential functions of the needs

        # For now, it will choose randomly
        return np.random.choice([Needs.HL, Needs.BL, Needs.TL])
