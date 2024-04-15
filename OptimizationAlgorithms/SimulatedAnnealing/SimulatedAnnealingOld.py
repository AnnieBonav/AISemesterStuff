import math, random
from OptimizationAlgorithms.HelperFunctions import saveDataToCsv
import matplotlib.pyplot as plt
import time

path = "SphereFunction/SimulatedAnnealing.csv"

def sphereFunction(x):
    return sum([xi**2 for xi in x])

import matplotlib.pyplot as plt

onlyRunRandomOne = True

def simulatedAnnealing(initialSolution, temperature, coolingRate, numIterations):
    initialSolution[0] = round(initialSolution[0], 3)
    initialSolution[1] = round(initialSolution[1], 3)
    initialSolution[2] = round(initialSolution[2], 3)

    startTime = time.time()
    initialTemperature = temperature
    currentSolution = initialSolution
    bestSolution = currentSolution
    costs = []  # List to store the cost of the best solution in each iteration

    for i in range(numIterations):
        temperature *= coolingRate

        # Generate a new candidate solution by perturbing the current solution
        candidateSolution = [xi + random.uniform(-1, 1) for xi in currentSolution]

        # Calculate the cost (fitness) of the current and candidate solutions
        currentCost = sphereFunction(currentSolution)
        candidateCost = sphereFunction(candidateSolution)

        # If the candidate solution is better, accept it as the new current solution
        if candidateCost < currentCost:
            currentSolution = candidateSolution

            # If the candidate solution is the best so far, update the best solution
            if candidateCost < sphereFunction(bestSolution):
                bestSolution = candidateSolution
                costs.append(candidateCost)  # Add the cost of the new best solution to the list
        else:
            # If the candidate solution is worse, accept it with a certain probability
            acceptanceProbability = math.exp((currentCost - candidateCost) / temperature)
            if random.random() < acceptanceProbability:
                currentSolution = candidateSolution

    endTime = time.time()
    finalTime = round(endTime - startTime, 3)
    
    plt.figure(figsize=(10, 5))

    # Plot the cost of the best solution in each iteration
    plt.plot(costs)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)
    plt.title(f"Simulated Annealing\nInitial Temp: {initialTemperature}, Final Temp: {round(temperature, 3)}\nInitial Solution: {initialSolution}, Final Solution: {round(currentCost, 3)}\nCooling Rate: {coolingRate}, Time it took: {finalTime}")
    plt.ylabel('Cost')
    plt.xlabel(f'Iteration (Total: {numIterations})')
    plt.show()
    plt.clf()
    plt.close()

    return bestSolution

def baseline(temperature = 100, coolingRate = 0.95, numIterations = 1000):
    baselineSolution = [0, 0, 0]
    bestSolution = simulatedAnnealing(baselineSolution, temperature, coolingRate, numIterations)
    
    print("Initial solution:", baselineSolution, "Baseline Best solution:", bestSolution, "Baseline Best cost:", sphereFunction(bestSolution))
    saveDataToCsv(path, [f"Baseline solution from: {baselineSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestSolution}"])

def testing(temperature = 100, coolingRate = 0.95, numIterations = 1000):
    initialSolution = [4, -3, 9]
    bestSolution = simulatedAnnealing(initialSolution, temperature, coolingRate, numIterations)
    
    print("Testing initial solution:", initialSolution, "Best solution:", bestSolution, "Best cost:", sphereFunction(bestSolution))
    saveDataToCsv(path, [f"Testing solution from: {initialSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestSolution}"])

def randomSolution(temperature = 100, coolingRate = 0.95, numIterations = 1000, space = 10, degree = 3):
    initialTemperature = temperature
    initialSolution = []
    for _ in range(degree):
        initialSolution.append(round(random.uniform(-space, space), 3))
    bestSolution = simulatedAnnealing(initialSolution, temperature, coolingRate, numIterations)
    
    print("Initial solution:", initialSolution, "Best solution:", bestSolution, "Best cost:", sphereFunction(bestSolution), "Initial Temperature:", initialTemperature, "Cooling Rate:", coolingRate, "Number of iterations:", numIterations)
    saveDataToCsv(path, [f"Random Solution from: {initialSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of Iterations: {numIterations}", f"Best Solution: {bestSolution}"])

numIterations = 10
if not onlyRunRandomOne:
    baseline()
    for i in range(5):
        testing(temperature = 100, coolingRate = 0.90, numIterations = numIterations)
        numIterations *= 10

numIterations = 10
# space = 100
space = 10000
for i in range(5):
    randomSolution(numIterations = numIterations, space = space)
    numIterations *= 10
