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



# Select the function to optimize, from the following options:
selectedFunction = FunctionToOptimize.SPHERE
# selectedFunction = FunctionToOptimize.EGG


ga = GeneticAlgorithm(functionToOptimize = selectedFunction)
defaultAlgData = algData()

favoursBestParents = algData(
    numDimensions = 3,
    populationSize = 100,
    numGenerations = 100,
    mutationRate = 0.01,
    crossoverRate = 0.95,

    selectionMethod = "TournamentSelection",
    tournamentSize = 5,
    evolveMethod = "ElitismAndGenerational", 
    elitismCount = 2,

    verboseChanges = False,
    showComplexPlot = False,
    showPlots = True,
    )

# Using default alg data

# ga.test(defaultAlgData)
ga.testMutationRate(defaultAlgData,
                    mutationRate = 0.01,
                    numOfIterations = 5
                    )

ga.testCrossoverRate(defaultAlgData,
                    crossoverRate = 0.02,
                    numOfIterations = 10
                    )

# ga.testPopulationSize(defaultAlgData,
#                       populationRate = 50,
#                       numOfIterations = 20
#                       )

# ga.testNumGenerations(defaultAlgData,
#                       numGenerationsRate = 50,
#                       numOfIterations = 30
#                       )

# ga.testNumGenerationsAndPopulationSize(defaultAlgData,
#                                        populationSize = 50,
#                                        numGenerations = 50,
#                                        numOfIterations = 50
#                                        )