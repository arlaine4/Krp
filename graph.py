from collections import defaultdict

class Graph:
    """
    Class representing a graph of processes connected to each other by the stock they produce/need.
    """

    def __init__(self, processes, stocks, optimize):
        self.stocks = stocks
        self.processes = processes
        self.optimize = optimize
        self.needs = defaultdict(list)
        self.produces = defaultdict(list)

    def build_graph(self):
        """
        Method that builds a graph by regrouping and sort processes by their needs and products
        """
        for process in self.processes.values():
            for stock in process.need:
                self.needs[stock].append(process)
            for stock in process.result:
                self.produces[stock].append(process)

        for stock, processes in self.needs.items():
            processes.sort(key= lambda p: p.need[stock])
        for stock, processes in self.produces.items():
            processes.sort(reverse=True, key= lambda p: p.result[stock])

    def get_possible_paths(self):
        pass

    def filter_usefull_paths(self):
        pass

    def evaluate_path_productivity(self): # Possibly in Solver class
        pass

