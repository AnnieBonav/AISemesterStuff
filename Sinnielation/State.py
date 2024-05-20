from Classes import Needs
import numpy as np

class State:
    def __init__(self, need : Needs, probability_function, min_value : float = 0, max_value : float = 100, starting_value : float = 0):
        self.need = need
        self.probability_function = probability_function

        self.min_value = min_value
        self.max_value = max_value
        self.current_value = starting_value
        self.probability_values = self.cache_probability_values()

    def cache_probability_values(self):
        self.probability_values = self.probability_function()
        return self.probability_values
    
    def get_probability(self, verbose = False):
        index = np.abs(self.probability_values[0] - self.current_value).argmin()
        probability = self.probability_values[1][index]
        if verbose: print(f"{self.need.value}: the y value for x = {self.current_value} (with index {index}) is {probability}")
        return probability

    def update(self, value):
        self.current_value = value

    def increase(self, value):
        self.current_value += value
        if self.current_value > self.max_value:
            self.current_value = self.max_value

        self.current_value = round(self.current_value, 3)
        
    def decrease(self, value):
        self.current_value -= value
        if self.current_value < self.min_value:
            self.current_value = self.min_value

        print(f"{self.need.value}: {self.current_value}")

    def __str__(self):
        return f"{self.need.value}: {self.current_value}"

# Questions to self:
# - Do I want to eexponential functions to be passed? Or do I want the values to be passed and then the function does the calculation?