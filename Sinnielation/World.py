from Classes import TOD
from Agent import Agent

class Day:
    def __init__(self):
        self.time = 0
        self.time_of_day = TOD.MORNING
        self.observers = []

    def add_observer_agent(self, agent: Agent):
        self.observers.append(agent)

    def tick_in_min(self, minutes = 10, times = 1):
        for _ in range(times):
            for agent in self.observers:
                agent.pass_time(minutes)
            self.time += minutes

    def fake_pass_time(self, minutes = 10, activity = None, action = None):
        for agent in self.observers:
            agent.pass_time(minutes, activity, action)
        self.time += minutes