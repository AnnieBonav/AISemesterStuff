import random

# Define the sphere function
def sphereFunction(x):
    return sum([xi**2 for xi in x])

# Define the GeneticAlgorithm class
class GeneticAlgorithm:
    def __init__(self, populationSize, numDimensions, mutationRate, crossoverRate):
        self.populationSize = populationSize
        self.numDimensions = numDimensions
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.population = []

    def initializePopulation(self):
        self.population = [[random.uniform(-5.12, 5.12) for _ in range(self.numDimensions)] for _ in range(self.populationSize)]

    def evaluate_population(self):
        fitnessScores = []
        for individual in self.population:
            fitnessScores.append(sphereFunction(individual))
        return fitnessScores

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

    def crossover(self, parents):
        child = []
        for i in range(self.numDimensions):
            if random.random() < self.crossoverRate:
                child.append(parents[0][i])
            else:
                child.append(parents[1][i])
        return child

    def mutate(self, child):
        for i in range(self.numDimensions):
            if random.random() < self.mutationRate:
                child[i] = random.uniform(-5.12, 5.12)
        return child

    def evolve(self, numGenerations):
        self.initializePopulation()
        for _ in range(numGenerations):
            fitnessScores = self.evaluate_population()
            parents = self.selectParents(fitnessScores)
            child = self.crossover(parents)
            child = self.mutate(child)
            self.population.append(child)
            self.population.pop(0)
        bestIndividual = min(self.population, key = lambda x: sphereFunction(x))
        return bestIndividual

def testing(populationSize = 100, numDimensions = 2, mutationRate = 0.01, crossoverRate = 0.8, numGenerations = 100):
    ga = GeneticAlgorithm(populationSize, numDimensions, mutationRate, crossoverRate)
    bestSolution = ga.evolve(numGenerations)
    print("Best solution:", bestSolution)
    print("Fitness score:", sphereFunction(bestSolution))

testing()