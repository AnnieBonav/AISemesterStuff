import math, random
from HelperFunctions import saveDataToCsv
import matplotlib.pyplot as plt

path = "SphereFunction/SimulatedAnnealing.csv"

def sphereFunction(x):
    return sum([xi**2 for xi in x])

import matplotlib.pyplot as plt

def simulatedAnnealing(initialSolution, temperature, coolingRate, numIterations):
    current_solution = initialSolution
    bestSolution = current_solution
    costs = []  # List to store the cost of the best solution in each iteration

    for i in range(numIterations):
        temperature *= coolingRate

        # Generate a new candidate solution by perturbing the current solution
        candidate_solution = [xi + random.uniform(-1, 1) for xi in current_solution]

        # Calculate the cost (fitness) of the current and candidate solutions
        current_cost = sphereFunction(current_solution)
        candidate_cost = sphereFunction(candidate_solution)

        # If the candidate solution is better, accept it as the new current solution
        if candidate_cost < current_cost:
            current_solution = candidate_solution

            # If the candidate solution is the best so far, update the best solution
            if candidate_cost < sphereFunction(bestSolution):
                bestSolution = candidate_solution
                costs.append(candidate_cost)  # Add the cost of the new best solution to the list
        else:
            # If the candidate solution is worse, accept it with a certain probability
            acceptance_probability = math.exp((current_cost - candidate_cost) / temperature)
            if random.random() < acceptance_probability:
                current_solution = candidate_solution

    # Plot the cost of the best solution in each iteration
    plt.plot(costs)
    plt.ylabel('Cost')
    plt.xlabel('Iteration')
    plt.show()
    plt.clf()

    return bestSolution

def baseline():
    baselineSolution = [0, 0, 0]  # Initial solution
    print("\nInitial solution:", baselineSolution)

    temperature = 100  # Initial temperature
    coolingRate = 0.95  # Cooling rate
    numIterations = 1000  # Number of iterations

    bestSolution = simulatedAnnealing(baselineSolution, temperature, coolingRate, numIterations)
    print("Baseline Best solution:", bestSolution)
    print("Baseline Best cost:", sphereFunction(bestSolution))
    saveDataToCsv(path, [f"Baseline solution from: {baselineSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestSolution}"])

baseline()

def testing(temperature = 100, coolingRate = 0.95, numIterations = 1000):
    initialSolution = [4, -3, 9]
    print("\nTesting initial solution:", initialSolution)

    bestSolution = simulatedAnnealing(initialSolution, temperature, coolingRate, numIterations)
    print("Best solution:", bestSolution)
    print("Best cost:", sphereFunction(bestSolution))
    saveDataToCsv(path, [f"Testing solution from: {initialSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of iterations: {numIterations}", f"Best Solution: {bestSolution}"])

testing(temperature = 50, coolingRate = 0.90, numIterations = 500)

def randomSolution(temperature = 100, coolingRate = 0.95, numIterations = 1000):
    initialSolution = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
    print("\nInitial solution:", initialSolution)

    bestSolution = simulatedAnnealing(initialSolution, temperature, coolingRate, numIterations)
    print("Best solution:", bestSolution)
    print("Best cost:", sphereFunction(bestSolution))
    saveDataToCsv(path, [f"Random Solution from: {initialSolution}", f"Temperature: {temperature}", f"Cooling Rate: {coolingRate}", f"Number of Iterations: {numIterations}", f"Best Solution: {bestSolution}"])

randomSolution(numIterations = 10)