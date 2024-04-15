import math
from enum import Enum

class FunctionToOptimize(Enum):
    SPHERE = "sphere",
    EGG = "eggHolder",
    SHAFFER2 = "shaffer2"

def sphereFunction(x):
    return sum([xi**2 for xi in x])

def eggHolderFunction(x):
    assert len(x) >= 2, "Egg Holder function requires at least two variables"
    return -(x[1] + 47) * math.sin(math.sqrt(abs(x[0]/2 + (x[1]  + 47)))) - x[0] * math.sin(math.sqrt(abs(x[0] - (x[1]  + 47))))

def shafferFunction(x):
    assert len(x) >= 2, "Shaffer function requires at least two variables"
    return 0.5 + (math.sin(math.sqrt(x[0]**2 + x[1]**2))**2 - 0.5) / (1 + 0.001 * (x[0]**2 + x[1]**2))**2

FUNCTIONS = {
    FunctionToOptimize.SPHERE: sphereFunction,
    FunctionToOptimize.EGG: eggHolderFunction,
    FunctionToOptimize.SHAFFER2: shafferFunction
}

# CALLING THE FUNCTIONS
# result = FUNCTIONS[FunctionToOptimize.SPHERE](individual)
