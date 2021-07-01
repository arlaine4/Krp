import time
import utils
from copy import deepcopy

class Simulation:
    def __init__(self, options, graph):
        self.max_cycle = options.delay
        self.graph = graph
        self.cycle = 0
        self.solution = []
        self.stack = [self.graph.optimize[0]]
        self.queue = []

    def update_queue(self, tmp_p):
        #The goal here is to update the queue with the needs for the last process
        #added to the stack

    def check_new_sub_process(self, tmp_p):
        #Check method used to determine if we need more sub_process in order to run the last
        #one added to the stack
        pass

    def create_stock_simulation(self):
        #Temporary method
        for elem in self.graph.processes.items():
            self.queue.append(deepcopy(elem[1].need))

    def start_simulation(self):
        #Data structure not definitive, just some tests
        self.create_stock_simulation() 
        tmp_process = [self.stack[0]]
        self.update_queue(tmp_process)
        while self.cycle < self.max_cycle:
            while self.check_new_sub_process(tmp_process):
                tmp_process = self.update_tmp_process_lst(tmp_process)
                break
            break
            #if self.check_filled_needs_current_process():
            #    self.stack.append(
