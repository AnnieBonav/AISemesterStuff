from utils import memoize

class Graph:
    def __init__(self, graphDict):
        self.graphDict = graphDict
        self.initialize()

    def initialize(self):
        """Make a digraph by adding symmetric edges."""
        for a in list(self.graphDict.keys()):
            for (b, dist) in self.graphDict[a].items():
                self.connect(b, a, dist)

    def connect(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graphDict.setdefault(A, {})[B] = distance

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graphDict.keys()])
        s2 = set([k2 for v in self.graphDict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)