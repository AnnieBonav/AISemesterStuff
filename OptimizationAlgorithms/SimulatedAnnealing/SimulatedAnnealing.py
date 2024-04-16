import math, random, time, sys, os, numpy as np
import matplotlib.pyplot as plt

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)
from HelperFunctions import visualization, saveDataToCsv

# def eggFunction(x):
#     assert len(x) >= 2, "Egg Holder function requires at least two variables"
#     return -(x[1] + 47) * math.sin(math.sqrt(abs(x[0]/2 + (x[1]  + 47)))) - x[0] * math.sin(math.sqrt(abs(x[0] - (x[1]  + 47))))
# space = 512

def shafferFunction(x):
    assert len(x) >= 2, "Shaffer function requires at least two variables"
    return 0.5 + (math.sin(math.sqrt(x[0]**2 + x[1]**2))**2 - 0.5) / (1 + 0.001 * (x[0]**2 + x[1]**2))**2
space = 100

selectedFunction = shafferFunction

onlyRunRandomOne = True
minTemperature = 0.01
# Defines the degrees that will be used to test the simulated annealing, these will become the length on the array of the initial state
degree = 2

# The cooling rate is the rate (speed) at which the temperature is reduced, the closer to 1, the slower the temperature is reduced
coolingRate = 0.95

# The temperature is the initial temperature of the system, the higher the temperature, the more likely the algorithm is to accept worse solutions
temperature = 95
numIterations = 5

# Change to show all or only best on visualization
onlyBetter = True

# The Simulated Annealing algorithm is a probabilistic technique used for finding an approximate solution to an optimization problem
def simulatedAnnealing(initialState, temperature, coolingRate, numIterations, searchRange = 1):
    initialTemperature = temperature
    
    initialState[0] = round(initialState[0], 3)
    initialState[1] = round(initialState[1], 3)
    
    currentState = initialState
    bestState = currentState

    startTime = time.time()
    costs = []  # List to store the cost of the best solution in each iteration
    allNumbersGraph = []
    print(f"NUM ITERATIONS: {numIterations}")
    for _ in range(numIterations):
        temperature *= coolingRate

        # Generate a new candidate state by perturbing the current state
        candidateState = [xi + random.uniform(-searchRange, searchRange) for xi in currentState]

        # Calculate the cost (fitness) of the current and candidate states
        currentCost = selectedFunction(currentState)
        candidateCost = selectedFunction(candidateState)

        # If the candidate state is better, accept it as the new current state
        if candidateCost < currentCost:
            currentState = candidateState

            # If the candidate state is the best so far, update the best state
            if candidateCost < selectedFunction(bestState):
                bestState = candidateState
                costs.append(candidateCost)  # Add the cost of the new best state to the list, for visualization
            allNumbersGraph.append(candidateCost)
        else:
            # If the candidate state is worse, accept it with a certain probability
            if temperature <= 0:
                temperature = minTemperature
            acceptanceProbability = math.exp((currentCost - candidateCost) / temperature)
            if random.random() < acceptanceProbability:
                currentState = candidateState
            allNumbersGraph.append(currentCost)

    endTime = time.time()
    finalTime = round(endTime - startTime, 3)
    
    if(not onlyBetter):
        costs = allNumbersGraph
    if(len(costs)<= 1):
        return
    costs = np.array(costs)
    print("COSTS LENGTH", len(costs))
    # Plot the cost of the best solution in each iteration
    bestState = [round(x, 3) for x in bestState]
    xValues = np.arange(0, len(costs))

    plt.figure(figsize=(10, 5))
    plt.plot(costs)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)
    plt.title(f"Simulated Annealing\nInitial Temp: {initialTemperature}, Final Temp: {round(temperature, 3)}\nInitial State: {initialState}, Final State: {bestState}\nFinal Cost: {round(currentCost, 3)}, Cooling Rate: {coolingRate}, Time it took: {finalTime}")
    plt.ylabel('Cost')
    for x in xValues:
        plt.axvline(x = x, linestyle='dotted', color='gray')
    plt.xlabel(f'Iterations (Total: {len(costs)})')
    plt.show()
    plt.clf()
    plt.close()

    return bestState

def baseline(numIterations, temperature = 100, coolingRate = 0.95):
    baselineSolution = [0, 0]
    bestState = simulatedAnnealing(baselineSolution, temperature, coolingRate, numIterations)
    # saveDataToCsv(path, [f"Baseline solution from: {baselineSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestState}"])

def testing(numIterations, temperature = 100, coolingRate = 0.95):
    initialState = [50, -30]
    
    bestState = simulatedAnnealing(numIterations, initialState, temperature, coolingRate)
    # saveDataToCsv(path, [f"Testing solution from: {initialState}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestState}"])

def randomSolution(space, numIterations, degree, temperature = 100, coolingRate = 0.95):
    initialTemperature = temperature
    initialState = []
    for _ in range(degree):
        initialState.append(round(random.uniform(-space, space), 3))
    bestState = simulatedAnnealing(initialState, temperature, coolingRate, numIterations)
    # saveDataToCsv(path, [f"Random Solution from: {initialState}", f"Initial Temperature: {initialTemperature}", f"Cooling Rate: {coolingRate}", f"Number of Iterations: {numIterations}", f"Best Solution: {bestState}"])

# numIterations = 10
# if not onlyRunRandomOne:
#     # baseline()
#     for i in range(numIterations):
#         testing(temperature = temperature, coolingRate = coolingRate, numIterations = numIterations, degree = degree)
#         numIterations *= 10

for _ in range(5):
    randomSolution(numIterations = numIterations, space = space, coolingRate = coolingRate, degree = degree)
    numIterations += 100
