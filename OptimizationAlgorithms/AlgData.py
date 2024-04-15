# This is used on the algorithms to handle the non-changing data passed to them
# Could be a struct or a dictionary, but I prefer a class for better readability

class AlgData:
    def __init__(self, numDimensions = 10, populationSize = 100, mutationRate = 95, crossoverRate = 95, tournamentSize = 5, selectionMethod = "RouletteSelection", evolveMethod = "ElitismAndGenerational",  elitismCount = 2, verboseChanges = False, showPlots = False, showTestsPlots = True):
        self.numDimensions = numDimensions
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.tournamentSize = tournamentSize
        self.selectionMethod = selectionMethod
        self.evolveMethod = evolveMethod
        self.elitismCount = elitismCount
        self.verboseChanges = verboseChanges
        self.showPlots = showPlots
        self.showTestsPlots = showTestsPlots