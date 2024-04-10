import random, matplotlib.pyplot as plt, math
import OptimizationFunctions as optFunc

# The goal of the genetic algorithm is to find the input to this function that produces the lowest output

numDimensions = 10
printAllChanges = False
showPlots = False
showTestsPlots = True
# What roullette selection does is to select a random number between 0 and the sum of all fitnesses, and then iterate through the fitnesses summing them up until the sum is greater than the random number. The individual that corresponds to that fitness is the one selected.
# selectionMethod = "RouletteSelection"

# Tournament selection is a selection method where a number of individuals are selected at random from the population and the best individual from that group is chosen as the parent. This process is repeated to select the second parent.
selectionMethod = "TournamentSelection"

# The basic replacement method is a generational replacement method where the entire population is replaced by the offspring at each generation.
# evolveMethod = "BasicReplacement"
evolveMethod = "ElitismAndGenerational"

# Select the function to optimize, from the following options:
# selectedFunction = optFunc.sphereFunction
selectedFunction = optFunc.eggHolderFunction

# Define the GeneticAlgorithm class
class GeneticAlgorithm:
    # Initialize the genetic algorithm with the population size, number of dimensions, mutation rate, and crossover rate
    def __init__(self, functionToOptimize, populationSize, numDimensions, mutationRate, crossoverRate, tournamentSize = 5, elitismCount = 2):
        self.populationSize = populationSize
        self.numDimensions = numDimensions
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.tournamentSize = tournamentSize  # For tournament selection
        self.elitismCount = elitismCount # For elitism
        self.functionToOptimize = functionToOptimize
        self.population = []

    # Initialize the population with random individuals
    def initializePopulation(self):
        # We use a range of -5.12 to 5.12 for each dimension as it is a conventional range for the sphere function
        self.population = [[random.uniform(-5.12, 5.12) for _ in range(self.numDimensions)] for _ in range(self.populationSize)]

    # Evaluate the fitness of each individual in the population using the sphere function
    def evaluatePopulation(self):
        fitnessScores = []
        for individual in self.population:
            fitnessScores.append(self.functionToOptimize(individual))
        return fitnessScores

    # Select parents from the population using fitness proportionate selection
    def selectParents(self, fitnessScores):
        parents = []
        match selectionMethod:
            case "RouletteSelection":
                totalFitness = sum(fitnessScores)
                for _ in range(2):
                    cumulativeFitness = 0
                    randomValue = random.uniform(0, totalFitness)
                    for i, fitness in enumerate(fitnessScores):
                        cumulativeFitness += fitness
                        if cumulativeFitness >= randomValue:
                            parents.append(self.population[i])
                            break
            case "TournamentSelection":
                for _ in range(2):  # Select two parents
                    tournament = random.sample(self.population, self.tournamentSize)
                    best = min(tournament, key=lambda individual: self.functionToOptimize(individual))
                    parents.append(best)
        return parents

    # Perform crossover on the parents to produce a child. In uniform crossover, each gene is chosen from either parent with equal probability. The crossoverRate parameter can be used to adjust this probability. If crossoverRate is high, genes from the first parent are more likely to be chosen, and if it's low, genes from the second parent are more likely to be chosen.
    def crossover(self, parents):
        child = []
        if printAllChanges: print(f"\nStarts crossover with Parent 0: {parents[0]}, Parent 1: {parents[1]}")
        for i in range(self.numDimensions):
            if random.random() < self.crossoverRate:
                toAppend = parents[0][i]
                if printAllChanges: print("Appended from parent 0:", parents[0][i])
            else:
                toAppend = parents[1][i]
                if printAllChanges: print("Appended from parent 1:", parents[0][i])
            child.append(toAppend)
        if printAllChanges: print("Child:", child)
        return child

    # Perform mutation on the child
    def mutate(self, child):
        if printAllChanges: print(f"\nStarts mutation with Child: {child}")
        for i in range(self.numDimensions):
            if random.random() < self.mutationRate:
                # TODO: Change limits so each function has its own implementatio (and limits)
                child[i] = random.uniform(-5.12, 5.12)
                if printAllChanges: print(f"Mutated at index {i} to {child[i]}")
        if printAllChanges: print("Mutated Child:", child)
        return child

    # Evolve the population for a certain number of generations
    def evolve(self, numGenerations):
        self.initializePopulation()
        bestFitnesses = []
        worstFItnesses = []
        avgFitnesses = []
        match evolveMethod:
            case "BasicReplacement":
                for i in range(numGenerations):
                    if printAllChanges: print(f"\n************************************************************\nIteration #{i}")
                    fitnessScores = self.evaluatePopulation()
                    parents = self.selectParents(fitnessScores)
                    child = self.crossover(parents)
                    child = self.mutate(child)
                    self.population.append(child)
                    self.population.pop(0)
                    bestFitnesses.append(min(fitnessScores))
                    worstFItnesses.append(max(fitnessScores))
                    avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
                bestIndividual = min(self.population, key = lambda x: self.functionToOptimize(x))
            case "ElitismAndGenerational":
                for _ in range(numGenerations):
                    fitnessScores = self.evaluatePopulation()
                    newPopulation = sorted(self.population, key=lambda individual: self.functionToOptimize(individual))[:self.elitismCount]
                    
                    while len(newPopulation) < self.populationSize:
                        parents = self.selectParents(fitnessScores)  # Ensure your selection method is compatible
                        child = self.crossover(parents)
                        child = self.mutate(child)
                        newPopulation.append(child)

                    self.population = newPopulation
                    
                    bestFitnesses.append(self.functionToOptimize(newPopulation[0]))  # Assuming the first individual is the best due to sorting
                    worstFItnesses.append(self.functionToOptimize(newPopulation[-1]))  # Assuming the last individual is the worst due to sorting
                    avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
                bestIndividual = self.population[0]  # The best individual
        return bestIndividual, bestFitnesses, worstFItnesses, avgFitnesses

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