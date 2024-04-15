import random, os, sys, matplotlib.pyplot as plt
from AlgData import AlgData
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)
from OptimizationFunctions import FunctionToOptimize, FUNCTIONS
import numpy as np

# Define the GeneticAlgorithm class
class GeneticAlgorithm:
    # Initialize the genetic algorithm with the population size, number of dimensions, mutation rate, and crossover rate
    def __init__(self, functionToOptimize:FunctionToOptimize):
        self.algData:AlgData = AlgData() # Default values, can be changed when calling testing
        self.functionToOptimize = functionToOptimize
        if self.functionToOptimize == FunctionToOptimize.EGG or self.functionToOptimize == FunctionToOptimize.SHAFFER2:
            self.algData.numDimensions = 2
        self.population = []

    # Initialize the population with random individuals
    def initializePopulation(self):
        # We use a range of -5.12 to 5.12 for each dimension as it is a conventional range for the sphere function, and -512 to 512 for the egg function
        match self.functionToOptimize:
            case FunctionToOptimize.SPHERE:
                self.population = [[random.uniform(-5.12, 5.12) for _ in range(self.algData.numDimensions)] for _ in range(self.algData.populationSize)]
            case FunctionToOptimize.EGG:
                # Set the num of dimensions to 2
                self.population = [[random.uniform(-512, 512) for _ in range(self.algData.numDimensions)] for _ in range(self.algData.populationSize)]
            case FunctionToOptimize.SHAFFER2:
                self.population = [[random.uniform(-100, 100) for _ in range(self.algData.numDimensions)] for _ in range(self.algData.populationSize)]
            case default:
                raise ValueError("Invalid function")

    # Evaluate the fitness of each individual in the population using the sphere function
    def evaluatePopulation(self):
        fitnessScores = []
        for individual in self.population:
            fitnessScores.append(FUNCTIONS[self.functionToOptimize](individual))
        return fitnessScores

    # Select parents from the population using fitness proportionate selection
    def selectParents(self, fitnessScores):
        parents = []
        match self.algData.selectionMethod:
            case "RouletteSelection":
                totalFitness = sum(fitnessScores)
                for _ in range(2):
                    cumulativeFitness = 0
                    randomValue = random.uniform(0, totalFitness)
                    parentAdded = False
                    for i, fitness in enumerate(fitnessScores):
                        cumulativeFitness += fitness
                        if cumulativeFitness >= randomValue:
                            parents.append(self.population[i])
                            parentAdded = True
                            break
                        if not parentAdded:  # If no parent was added in the loop
                            randomParent = random.choice(self.population)
                            parents.append(randomParent)
                            # print("Appended random parent in Roulette")
            case "TournamentSelection":
                for _ in range(2):  # Select two parents
                    tournament = random.sample(self.population, self.algData.tournamentSize)
                    best = min(tournament, key=lambda individual: FUNCTIONS[self.functionToOptimize](individual))
                    parents.append(best)
            case default:
                raise ValueError("Invalid selection method")
        return parents

    # Perform crossover on the parents to produce a child. In uniform crossover, each gene is chosen from either parent with equal probability. The crossoverRate parameter can be used to adjust this probability. If crossoverRate is high, genes from the first parent are more likely to be chosen, and if it's low, genes from the second parent are more likely to be chosen.
    def crossover(self, parents):
        child = []
        if self.algData.verboseChanges: print(f"\nStarts crossover with Parent 0: {parents[0]}, Parent 1: {parents[1]}")
        for i in range(self.algData.numDimensions):
            if random.random() < self.algData.crossoverRate:
                toAppend = parents[0][i]
                if self.algData.verboseChanges: print("Appended from parent 0:", parents[0][i])
            else:
                toAppend = parents[1][i]
                if self.algData.verboseChanges: print("Appended from parent 1:", parents[0][i])
            child.append(toAppend)
        if self.algData.verboseChanges: print("Child:", child)
        return child

    # Perform mutation on the child
    def mutate(self, child):
        if self.algData.verboseChanges: print(f"\nStarts mutation with Child: {child}")
        for i in range(self.algData.numDimensions):
            if random.random() < self.algData.mutationRate:
                # TODO: Change limits so each function has its own implementatio (and limits)
                child[i] = random.uniform(-5.12, 5.12)
                if self.algData.verboseChanges: print(f"Mutated at index {i} to {child[i]}")
        if self.algData.verboseChanges: print("Mutated Child:", child)
        return child

    # Evolve the population for a certain number of generations
    def evolve(self, numGenerations):
        self.population = []
        self.initializePopulation()
        bestFitnesses = []
        worstFItnesses = []
        avgFitnesses = []
        match self.algData.evolveMethod:
            case "BasicReplacement":
                for i in range(numGenerations):
                    if self.algData.verboseChanges: print(f"\n************************************************************\nIteration #{i}")
                    fitnessScores = self.evaluatePopulation()
                    parents = self.selectParents(fitnessScores)
                    child = self.crossover(parents)
                    child = self.mutate(child)
                    self.population.append(child)
                    self.population.pop(0)
                    bestFitnesses.append(min(fitnessScores))
                    worstFItnesses.append(max(fitnessScores))
                    avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
                bestIndividual = min(self.population, key = lambda x: FUNCTIONS[self.functionToOptimize](x))
            case "ElitismAndGenerational":
                for _ in range(numGenerations):
                    fitnessScores = self.evaluatePopulation()
                    newPopulation = sorted(self.population, key=lambda individual: FUNCTIONS[self.functionToOptimize](individual))[:self.algData.elitismCount]
                    
                    while len(newPopulation) < self.algData.populationSize:
                        parents = self.selectParents(fitnessScores)  # Ensure your selection method is compatible
                        child = self.crossover(parents)
                        child = self.mutate(child)
                        newPopulation.append(child)

                    self.population = newPopulation
                    
                    bestFitnesses.append(FUNCTIONS[self.functionToOptimize](newPopulation[0]))  # Assuming the first individual is the best due to sorting
                    worstFItnesses.append(FUNCTIONS[self.functionToOptimize](newPopulation[-1]))  # Assuming the last individual is the worst due to sorting
                    avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
                bestIndividual = self.population[0]  # The best individual
            
            case default:
                raise ValueError("Invalid evolve method")
        return bestIndividual, bestFitnesses, worstFItnesses, avgFitnesses

    def plot(self, bestFitnesses, worstFitnesses, avgFitnesses, showPlots = False):
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

    def plotTests(self, testsResults, testTitle, showTestsPlots = True):
        # Generate x values as whole numbers
        x_values = np.arange(1, len(testsResults[0][0]) + 1)

        plt.figure(figsize=(12, 6))
        
        for testResult, label in zip(testsResults[0], testsResults[1]):
            plt.plot(x_values, testResult, label=label)

        plt.title(f"Fitness through the change in {testTitle}")
        plt.xlabel(f"{testTitle}")
        plt.xticks(x_values)  # Set x-axis ticks to be the whole numbers
        for x in x_values:
            plt.axvline(x = x, linestyle='dotted', color='gray')
        plt.ylabel('Fitness')
        plt.legend()
        if showTestsPlots: plt.show()
        plt.clf()
        plt.close()

    #
    # TESTING DIFFERENT PARAMETERS
    #

    # Can sent a new algData (to not use the default values)
    def test(self, algData: None | AlgData = None):
        if algData is not None:
            self.algData = algData
        
        bestSolution, bestFitnesses, worstFitnesses, avgFitnesses = self.evolve(self.algData.numGenerations)

        bestSolution = [round(x, 5) for x in bestSolution]
        bestFitnesses = [round(x, 5) for x in bestFitnesses]
        worstFitnesses = [round(x, 5) for x in worstFitnesses]
        avgFitnesses = [round(x, 5) for x in avgFitnesses]

        if self.algData.verboseChanges: print(f"\nRESULTS")
        fitnessScore = FUNCTIONS[FunctionToOptimize.SPHERE](bestSolution)
        # fitnessScore = round(fitnessScore, 5)
        if self.algData.verboseChanges: print(f"Best solution: {bestSolution}, Fitness score:", {fitnessScore})
        self.plot(bestFitnesses, worstFitnesses, avgFitnesses, self.algData.showComplexPlot)

        return bestSolution, fitnessScore
    
    def getLoopedResults(self, numOfIterations, parameters:list, increaseRates:list):
        results = []
        originalValues = self.algData.getParameters(parameters)
        self.algData.setParameters(parameters, originalValues)

        # Loop through the parameters, as multiple could be changed
        for _ in range(numOfIterations):

            if self.algData.verboseChanges: print(f"Using parameters {parameters} with values {self.algData.getParameters(parameters)}")
            bestSolution, fitnessScore = self.test(self.algData)
            self.algData.increaseParameters(parameters, increaseRates)
            results.append(fitnessScore)
            
        self.algData.setParameters(parameters, originalValues)
        return results
    
    def testMutationRate(self, algData: None | AlgData = None, mutationRate = 0.01, numOfIterations = 5, tests = [["RouletteSelection", "BasicReplacement"]]):
        if algData is not None:
            self.algData = algData

        # Values and Titles
        results = [[],[]]
        for selectionMethod, evolveMethod in tests:
            self.algData.selectionMethod = selectionMethod
            self.algData.evolveMethod = evolveMethod

            if self.algData.verboseChanges: print(f"\nCHANGES MUTATION RATE {selectionMethod}, {evolveMethod}")
            results[0].append(self.getLoopedResults(numOfIterations, ["mutationRate"], [mutationRate]))
            results[1].append(f"Select: {selectionMethod}, Evolve: {evolveMethod}")
        
        self.plotTests(results, "Mutation Rate")

    def testCrossoverRate(self, algData: None | AlgData = None, crossoverRate = 0.02, numOfIterations = 5, tests = [["RouletteSelection", "BasicReplacement"]]):
        if algData is not None:
            self.algData = algData

        # Values and Titles
        results = [[],[]]
        for selectionMethod, evolveMethod in tests:
            self.algData.selectionMethod = selectionMethod
            self.algData.evolveMethod = evolveMethod

            if self.algData.verboseChanges: print(f"\nCHANGES CROSSOVER RATE {selectionMethod}, {evolveMethod}")
            results[0].append(self.getLoopedResults(numOfIterations, ["crossoverRate"], [crossoverRate]))
            results[1].append(f"Select: {selectionMethod}, Evolve: {evolveMethod}")
        
        self.plotTests(results, "Crossover Rate")

    def testPopulationSize(self, algData: None | AlgData = None, populationRate = 50, numOfIterations = 5, tests = [["RouletteSelection", "BasicReplacement"]]):
        if algData is not None:
            self.algData = algData

        # Values and Titles
        results = [[],[]]
        for selectionMethod, evolveMethod in tests:
            self.algData.selectionMethod = selectionMethod
            self.algData.evolveMethod = evolveMethod

            if self.algData.verboseChanges: print(f"\nCHANGES POPULATION SIZE {selectionMethod}, {evolveMethod}")
            results[0].append(self.getLoopedResults(numOfIterations, ["populationSize"], [populationRate]))
            results[1].append(f"Select: {selectionMethod}, Evolve: {evolveMethod}")
        
        self.plotTests(results, "Population Size Growth")

    def testNumGenerations(self, algData: None | AlgData = None, numGenerationsRate = 50, numOfIterations = 10, tests = [["RouletteSelection", "BasicReplacement"]]):
        if algData is not None:
            self.algData = algData

        # Values and Titles
        results = [[],[]]
        for selectionMethod, evolveMethod in tests:
            self.algData.selectionMethod = selectionMethod
            self.algData.evolveMethod = evolveMethod

            if self.algData.verboseChanges: print(f"\nCHANGES NUMBER OF GENERATIONS {selectionMethod}, {evolveMethod}")
            results[0].append(self.getLoopedResults(numOfIterations, ["numGenerations"], [numGenerationsRate]))
            results[1].append(f"Select: {selectionMethod}, Evolve: {evolveMethod}")
        
        self.plotTests(results, "Num Generations Growth")

    def testNumGenerationsAndPopulationSize(self, algData: None | AlgData = None, numGenerations = 50, populationSize = 50, numOfIterations = 10, tests = [["RouletteSelection", "BasicReplacement"]]):
        if algData is not None:
            self.algData = algData

        # Values and Titles
        results = [[],[]]
        for selectionMethod, evolveMethod in tests:
            self.algData.selectionMethod = selectionMethod
            self.algData.evolveMethod = evolveMethod

            if self.algData.verboseChanges: print(f"\nCHANGES NUMBER OF GENERATIONS AND POPULATION SIZE {selectionMethod}, {evolveMethod}")
            results[0].append(self.getLoopedResults(numOfIterations, ["numGenerations", "populationSize"], [numGenerations, populationSize]))
            results[1].append(f"Select: {selectionMethod}, Evolve: {evolveMethod}")
        
        self.plotTests(results, "Num Generations and Population Growth")