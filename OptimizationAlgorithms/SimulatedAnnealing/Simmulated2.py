import math, random, os, sys, time
import matplotlib.pyplot as plt
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)

from HelperFunctions import visualization, saveDataToCsv
from OptimizationFunctions import FUNCTIONS, FunctionToOptimize
path = "SphereFunction/SimulatedAnnealing.csv"

# Select the function to optimize, from the following options:
selectedFunction = FunctionToOptimize.SPHERE
# selectedFunction = FunctionToOptimize.EGG
# selectedFunction = FunctionToOptimize.SHAFFER2

onlyRunRandomOne = True
minTemperature = 0.01
# Defines the degrees that will be used to test the simulated annealing, these will become the length on the array of the initial state
degree = 5
if(degree == 3):
    visualization()
    
match (selectedFunction):
    case FunctionToOptimize.SPHERE:
        degree = degree
    case FunctionToOptimize.EGG:
        degree = 2
    case FunctionToOptimize.SHAFFER2:
        degree = 2
    
# The cooling rate is the rate (speed) at which the temperature is reduced, the closer to 1, the slower the temperature is reduced
coolingRate = 0.95

# The temperature is the initial temperature of the system, the higher the temperature, the more likely the algorithm is to accept worse solutions
temperature = 100

# The Simulated Annealing algorithm is a probabilistic technique used for finding an approximate solution to an optimization problem
def simulatedAnnealing(initialState, temperature, coolingRate, numIterations, searchRange = 1):
    initialTemperature = temperature
    initialState = [round(x, 3) for x in initialState]

    currentState = initialState
    bestState = currentState

    startTime = time.time()
    costs = []  # List to store the cost of the best solution in each iteration

    for i in range(numIterations):
        temperature *= coolingRate

        # Generate a new candidate state by perturbing the current state
        candidateState = [xi + random.uniform(-searchRange, searchRange) for xi in currentState]

        # Calculate the cost (fitness) of the current and candidate states
        currentCost = FUNCTIONS[selectedFunction](currentState)
        candidateCost = FUNCTIONS[selectedFunction](candidateState)

        # If the candidate state is better, accept it as the new current state
        if candidateCost < currentCost:
            currentState = candidateState

            # If the candidate state is the best so far, update the best state
            if candidateCost < FUNCTIONS[selectedFunction](bestState):
                bestState = candidateState
                costs.append(candidateCost)  # Add the cost of the new best state to the list, for visualization
        else:
            # If the candidate state is worse, accept it with a certain probability
            if temperature <= 0:
                temperature = minTemperature
            acceptanceProbability = math.exp((currentCost - candidateCost) / temperature)
            if random.random() < acceptanceProbability:
                currentState = candidateState

    endTime = time.time()
    finalTime = round(endTime - startTime, 3)
    

    # Plot the cost of the best solution in each iteration
    bestState = [round(x, 3) for x in bestState]

    print("PLOTTING")
    plt.figure(figsize=(10, 5))
    plt.plot(costs)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)
    plt.title(f"Simulated Annealing\nInitial Temp: {initialTemperature}, Final Temp: {round(temperature, 3)}\nInitial State: {initialState}, Final State: {bestState}\nFinal Cost: {round(currentCost, 3)}, Cooling Rate: {coolingRate}, Time it took: {finalTime}")
    plt.ylabel('Cost')
    plt.xlabel(f'Iteration (Total: {numIterations})')
    plt.show()
    plt.clf()
    plt.close()

    return bestState

def baseline(temperature = 100, coolingRate = 0.95, numIterations = 1000):
    match selectedFunction:
        case FunctionToOptimize.SPHERE:
            baselineSolution = [0, 0, 0]
        case FunctionToOptimize.EGG:
            baselineSolution = [0, 0]
        case FunctionToOptimize.SHAFFER2:
            baselineSolution = [0, 0]
        case default:
            raise ValueError("The selected function does not exist")
        
    bestState = simulatedAnnealing(baselineSolution, temperature, coolingRate, numIterations)
    saveDataToCsv(path, [f"Baseline solution from: {baselineSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestState}"])

def testing(temperature = 100, coolingRate = 0.95, numIterations = 1000, degree = 3):
    initialState = [4, -3, 9]
    match selectedFunction:
        case FunctionToOptimize.SPHERE:
            initialState = [4, -3, 9]
        case FunctionToOptimize.EGG:
            initialState = [400, -310]
        case FunctionToOptimize.SHAFFER2:
            initialState = [-98, 10]
        case default:
            raise ValueError("The selected function does not exist")
    
    bestState = simulatedAnnealing(initialState, temperature, coolingRate, numIterations)
    saveDataToCsv(path, [f"Testing solution from: {initialState}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestState}"])

def randomSolution(temperature = 100, coolingRate = 0.95, numIterations = 1000, space = 10, degree = 3):
    initialTemperature = temperature
    initialState = []
    match selectedFunction:
        case FunctionToOptimize.SPHERE:
            for _ in range(degree):
                initialState.append(round(random.uniform(-space, space), 3))
        case FunctionToOptimize.EGG:
            space = 512
            for _ in range(degree):
                initialState.append(round(random.uniform(-space, space), 3))
        case FunctionToOptimize.SHAFFER2:
            space = 100
            for _ in range(degree):
                initialState.append(round(random.uniform(-space, space), 3))
        
    bestState = simulatedAnnealing(initialState, temperature, coolingRate, numIterations)
    saveDataToCsv(path, [f"Random Solution from: {initialState}", f"Initial Temperature: {initialTemperature}", f"Cooling Rate: {coolingRate}", f"Number of Iterations: {numIterations}", f"Best Solution: {bestState}"])

# numIterations = 10
# if not onlyRunRandomOne:
#     # baseline()
#     for i in range(7):
#         testing(temperature = temperature, coolingRate = coolingRate, numIterations = numIterations, degree = degree)
#         numIterations *= 10

numIterations = 10
# space = 100
space = 10000
match (selectedFunction):
    case FunctionToOptimize.SPHERE:
        space = 5.12
    case FunctionToOptimize.EGG:
        space = 512
    case FunctionToOptimize.SHAFFER2:
        space = 100

for i in range(5):
    randomSolution(numIterations = numIterations, space = space, coolingRate = coolingRate, degree = degree)
    numIterations *= 10
