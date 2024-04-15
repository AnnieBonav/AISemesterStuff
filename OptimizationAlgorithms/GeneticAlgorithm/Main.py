import random, matplotlib.pyplot as plt, math, sys, os
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)

from OptimizationFunctions import FUNCTIONS, FunctionToOptimize
from AlgData import AlgData as algData
from GeneticAlgorithm import GeneticAlgorithm

# The goal of the genetic algorithm is to find the input to this function that produces the lowest output

#
# SELECTION METHODS
#
#Possible: RouletteSelection, TournamentSelection
# ROULETTE SELECTION METHOD: What roullette selection does is to select a random number between 0 and the sum of all fitnesses, and then iterate through the fitnesses summing them up until the sum is greater than the random number. The individual that corresponds to that fitness is the one selected.

# TOURNAMENT SELECTION METHOD is a selection method where a number of individuals are selected at random from the population and the best individual from that group is chosen as the parent. This process is repeated to select the second parent.

#
# EVOLVE METHODS
#
# Possible: BasicReplacement, ElitismAndGenerational
# BASIC REPLACEMENT: The basic replacement method is a generational replacement method where the entire population is replaced by the offspring at each generation.
# ELITISM AND GENERATIONAL : Elitisim is a method where the best individuals from the current population are carried over to the next generation. This ensures that the best individuals are not lost.,

data = algData(
    numDimensions = 10,
    populationSize = 100,
    mutationRate = 95,
    crossoverRate = 95,
    tournamentSize = 5,
    elitismCount = 2,

    selectionMethod = "TournamentSelection",
    evolveMethod = "ElitismAndGenerational", 

    verboseChanges = False,
    showPlots = False,
    showTestsPlots = True,
    )

# Select the function to optimize, from the following options:
selectedFunction = FunctionToOptimize.SPHERE
selectedFunction = FunctionToOptimize.EGG


# TODO: Change to be part of the class
def testing(populationSize = 100, numDimensions = 2, mutationRate = 0.01, crossoverRate = 0.8, numGenerations = 100):
    ga = GeneticAlgorithm(
        functionToOptimize = selectedFunction,
        populationSize= populationSize,
        numDimensions = numDimensions,
        mutationRate = mutationRate,
        crossoverRate = crossoverRate)
    
    bestSolution, bestFitnesses, worstFitnesses, avgFitnesses = ga.evolve(numGenerations)

    bestSolution = [round(x, 5) for x in bestSolution]
    bestFitnesses = [round(x, 5) for x in bestFitnesses]
    worstFitnesses = [round(x, 5) for x in worstFitnesses]
    avgFitnesses = [round(x, 5) for x in avgFitnesses]

    if printAllChanges: print(f"\nRESULTS")
    fitnessScore = round(selectedFunction(bestSolution), 5)
    print(f"Best solution: {bestSolution}, Fitness score:", {fitnessScore})

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(bestFitnesses, label='Best Fitness')
    plt.plot(worstFitnesses, label='Worst Fitness')
    plt.plot(avgFitnesses, label='Average Fitness')
    plt.legend()
    plt.title('Fitness through the Generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    if showPlots: plt.show()
    plt.clf()
    plt.close()
    return bestSolution, fitnessScore

def plotTests(testsResults, xLabel):
    plt.figure(figsize=(12, 6))
    plt.plot(testsResults)
    plt.title(f"Fitness through the change in {xLabel}")
    plt.xlabel(f"{xLabel}")
    plt.ylabel('Fitness')
    if showTestsPlots: plt.show()
    plt.clf()
    plt.close()

def testMutationRate():
    mutationRate = 0.01
    print("\nCHANGES MUTATION RATE")
    mutationResults = []
    for _ in range(5):
        bestSolution, fitnessScore = testing(numDimensions = numDimensions, mutationRate = mutationRate)
        mutationResults.append(fitnessScore)
        mutationRate += 0.01
    return mutationResults

def testCrossoverRate():
    crossoverRate = 0.02
    print("\nCHANGES CROSSOVER RATE")
    crossoverResults = []
    for _ in range(5):
        bestSolution, fitnessScore = testing(numDimensions = numDimensions, crossoverRate = crossoverRate)
        crossoverResults.append(fitnessScore)
        crossoverRate += 0.02
    return crossoverResults

def testPopulationSize():
    populationSize = 50
    print("\nCHANGES POPULATION SIZE")
    populationSizeResults = []
    for _ in range(5):
        bestSolution, fitnessScore = testing(populationSize = populationSize, numDimensions = numDimensions)
        populationSizeResults.append(fitnessScore)
        populationSize += 50
    return populationSizeResults

def testNumGenerations(numGenerations = 50):
    print("\nCHANGES NUMBER OF GENERATIONS")
    numGenerationsResults = []
    for _ in range(10):
        bestSolution, fitnessScore = testing(numGenerations = numGenerations, numDimensions = numDimensions)
        numGenerationsResults.append(fitnessScore)
        numGenerations += 50
    return numGenerationsResults

def testNumGenerationsAndPopulationSize(numGenerations = 50, populationSize = 50):
    print("\nCHANGES NUMBER OF GENERATIONS AND POPULATION SIZE")
    numGenerationsAndPopulationSizeResults = []
    for _ in range(10):
        bestSolution, fitnessScore = testing(numGenerations = numGenerations, numDimensions = numDimensions)
        numGenerationsAndPopulationSizeResults.append(fitnessScore)
        numGenerations += 50
        populationSize += 50
    return numGenerationsAndPopulationSizeResults

mutationResults = testMutationRate()
plotTests(mutationResults, "Mutation Rate")

crossoverResults = testCrossoverRate()
plotTests(crossoverResults, "Crossover Rate")

populationSizeResults = testPopulationSize()
plotTests(populationSizeResults, "Population Size")

numGenerationsResults = testNumGenerations()
plotTests(numGenerationsResults, "Number of Generations")

numGenerationsAndPopulationSizeResults = testNumGenerationsAndPopulationSize()
plotTests(numGenerationsAndPopulationSizeResults, "Number of Generations and Population Size")