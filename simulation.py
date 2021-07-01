import time
import utils
from copy import deepcopy

class Simulation:
    def __init__(self, options, graph):
        self.max_cycle = options.delay
        self.graph = graph
        self.cycle = 0
        self.solution = []
        self.define_start_needs()
        self.stack = []
        self.stock_keys = list(self.graph.stocks.items())
        self.queue = []

    def define_start_needs(self):
        if 'time' in self.graph.optimize[0].opti_elems and len(self.graph.optimize[0].opti_elems) == 2:
            self.graph.optimize[0].opti_elems.pop(self.graph.optimize[0].opti_elems.index('time'))
        self.start_needs = self.graph.optimize[0].opti_elems

    def __str__(self):
        return '\033[4mSimulation status\033[0m :\n\nStocks :\n{}\nQueue :\n{}\nStack :\n{}'\
                .format(self.get_stocks(), self.queue, self.stack)

    def get_stocks(self):
        contents = []
        for e in self.graph.stocks.items():
            contents.append((e[0], e[1].qty))
        return contents

    def check_curr_stock_in_stocks(self, elem, qty, adding=False):
        #if elem in self.stock_keys and self.check_qty_for_specific_item(elem, qty):
        if elem in self.stock_keys:
            return True
        else:
            return False

    def update_stocks(self, new_stock, operation='-'):
        keys = list(new_stock.keys())
        for key in keys:
            if operation == '+':
                if self.check_curr_stock_in_stocks(key, new_stock[key], True):
                    print("Stock key exists for {}".format(key))
                else:
                    print("Stock key does no exists for {}".format(key))
            elif operation == '-':
                if self.check_curr_stock_in_stocks(key, new_stock[key]):
                    print("Stock key exists for {}".format(key))
                else:
                    print("Error, trying to remove {} but {} does not exists in stocks".format((key, new_stock[key]), key))

    def start_simulation(self):
        print("Simluation first needs : ",self.start_needs[0])
        print('-'*100,'\n\n', self)
        self.queue.append(self.start_needs[0])
#        self.update_stocks(self.graph.stocks, '-')
        print('-'*100, '\n\n',self)

























