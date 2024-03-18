import random, matplotlib.pyplot as plt

# Define the sphere function, which is used as the fitness function
# The goal of the genetic algorithm is to find the input to this function that produces the lowest output
def sphereFunction(x):
    return sum([xi**2 for xi in x])

# Define the GeneticAlgorithm class
class GeneticAlgorithm:
    # Initialize the genetic algorithm with the population size, number of dimensions, mutation rate, and crossover rate
    def __init__(self, populationSize, numDimensions, mutationRate, crossoverRate):
        self.populationSize = populationSize
        self.numDimensions = numDimensions
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.population = []

    # Initialize the population with random individuals
    def initializePopulation(self):
        self.population = [[random.uniform(-5.12, 5.12) for _ in range(self.numDimensions)] for _ in range(self.populationSize)]

    # Evaluate the fitness of each individual in the population using the sphere function
    def evaluate_population(self):
        fitnessScores = []
        for individual in self.population:
            fitnessScores.append(sphereFunction(individual))
        return fitnessScores

    # Select parents from the population using fitness proportionate selection
    def selectParents(self, fitnessScores):
        parents = []
        total_fitness = sum(fitnessScores)
        for _ in range(2):
            cumulativeFitness = 0
            randomValue = random.uniform(0, total_fitness)
            for i, fitness in enumerate(fitnessScores):
                cumulativeFitness += fitness
                if cumulativeFitness >= randomValue:
                    parents.append(self.population[i])
                    break
        return parents

    # Perform crossover on the parents to produce a child
    def crossover(self, parents):
        child = []
        for i in range(self.numDimensions):
            if random.random() < self.crossoverRate:
                child.append(parents[0][i])
            else:
                child.append(parents[1][i])
        return child

    # Perform mutation on the child
    def mutate(self, child):
        for i in range(self.numDimensions):
            if random.random() < self.mutationRate:
                child[i] = random.uniform(-5.12, 5.12)
        return child

    # Evolve the population for a certain number of generations
    def evolve(self, numGenerations):
        self.initializePopulation()
        bestFitnesses = []
        worstFItnesses = []
        avgFitnesses = []
        for _ in range(numGenerations):
            fitnessScores = self.evaluate_population()
            parents = self.selectParents(fitnessScores)
            child = self.crossover(parents)
            child = self.mutate(child)
            self.population.append(child)
            self.population.pop(0)
            bestFitnesses.append(min(fitnessScores))
            worstFItnesses.append(max(fitnessScores))
            avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
        bestIndividual = min(self.population, key = lambda x: sphereFunction(x))
        return bestIndividual, bestFitnesses, worstFItnesses, avgFitnesses

def testing(populationSize = 100, numDimensions = 2, mutationRate = 0.01, crossoverRate = 0.8, numGenerations = 100):
    ga = GeneticAlgorithm(populationSize, numDimensions, mutationRate, crossoverRate)
    bestSolution, bestFitnesses, worstFitnesses, avgFitnesses = ga.evolve(numGenerations)
    print("Best solution:", bestSolution)
    print("Fitness score:", sphereFunction(bestSolution))

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(bestFitnesses, label='Best Fitness')
    plt.plot(worstFitnesses, label='Worst Fitness')
    plt.plot(avgFitnesses, label='Average Fitness')
    plt.legend()
    plt.title('Fitness through the Generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()
    plt.clf()

testing()