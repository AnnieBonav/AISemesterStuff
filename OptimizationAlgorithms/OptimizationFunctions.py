import math
from enum import Enum

class FunctionToOptimize(Enum):
    SPHERE = "sphere",
    EGG = "eggHolder",

def sphereFunction(x):
    return sum([xi**2 for xi in x])

def eggHolderFunction(x):
    assert len(x) >= 2, "Egg Holder function requires at least two variables"
    return -(x[1] + 47) * math.sin(math.sqrt(abs(x[0]/2 + (x[1]  + 47)))) - x[0] * math.sin(math.sqrt(abs(x[0] - (x[1]  + 47))))

FUNCTIONS = {
    FunctionToOptimize.SPHERE: sphereFunction,
    FunctionToOptimize.EGG: eggHolderFunction
}

# result = FUNCTIONS[FunctionToOptimize.SPHERE](individual)
