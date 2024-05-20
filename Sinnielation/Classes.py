from enum import Enum
import json

class Needs(Enum):
    """Class representing a Need"""
    BL = "BladderLevel"
    TL = "TirednessLevel"
    HL = "HungerLevel"
    RN = "RelaxationNeed"
    DN = "DetectiveNeed"

class TOD(Enum):
    """Class representing a Time of Day"""
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"

class Action:
    """Class representing an Action"""
    def __init__(self, name : str, value : int, time_in_min : int):
        self.name = name
        self.value = value
        self.time_in_min = time_in_min
    
    def get_json_info(self):
        return json.dumps(self.__dict__)
    
    def __str__(self):
        return json.dumps(self.__dict__)