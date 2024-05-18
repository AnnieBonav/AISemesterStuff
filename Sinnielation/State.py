from Classes import Needs

class State:
    def __init__(self, need : Needs, min_value : float = 0, max_value : float = 100, starting_value : float = 0):
        self.need = need
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = starting_value

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

    def __str__(self):
        return f"{self.need.value}: {self.current_value}"

