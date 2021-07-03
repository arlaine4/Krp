import time
import utils
from copy import deepcopy

class Simulation:
    def __init__(self, options, parser):
        self.start_needs = [[]]
        self.process = parser.content
        self.stocks = parser.stocks
        self.define_keys_result()
        self.max_cycle = self.define_max_delay(parser.optimize[0], options)
        self.cycle = 0
        self.solution = []
        self.stack = []
        self.queue = []

    def define_keys_result(self):
        self.keys_result = {}
        tmp_keys = self.process.keys()
        for elem in self.process:
            for res_key in self.process[elem].result:
                if res_key in self.keys_result:
                    self.keys_result[res_key].append(elem)
                else:
                    self.keys_result[res_key] = [elem]

    def define_max_delay(self, opti, options):
        if options.delay:
            if 'time' in opti.opti_elems:
                index = opti.opti_elems.index('time')
                self.start_needs[0] = opti.opti_elems[1] if index == 0 else opti.opti_elems[0]
                return options.delay
            else:
                self.start_needs[0] = opti.opti_elems[0]
                return self.define_max_delay_from_processes()

    def define_max_delay_from_processes(self):
        total = 0
        keys = list(self.process.keys())
        for key in keys:
            total += self.process[key].delay
        return total * len(keys)

    #def recursive_stack_update(self, curr_needs, i):
    #    if len(curr_needs) == 1:
    #        curr_needs = self.find_process_for_stack_update(curr_needs, list(curr_needs.keys()))
    #        self.queue.append(curr_needs)
    #        if len(curr_needs) != 0:
    #            return self.recursive_stack_update(curr_needs, list(curr_needs.keys()))
    #    else:
    #        return
    #        #return self.recursive_stack_update(curr_needs[-1], len(curr_needs))
    def recursive_stack_update(self, curr_needs):
        if curr_needs is None:
            return
        else:


    def find_process_for_stack_update(self, need, name_need):
        name_p = self.keys_result[name_need[0]]
        need[str(name_need[0])] = self.process[str(name_p[0])].result[str(name_need[0])]
        while need[str(name_need[0])] != 0:
            self.stack.append(self.process[name_p[0]])
            need[str(name_need[0])] -= self.process[str(name_p[0])].result[str(name_need[0])]
        del(self.queue[0])
        return self.stack[0].need
        #self.stack.append(self.process[self.keys_result[str(name_need[0])]])

#    def find_process_for_stack_update(self, need, names):
#        name = self.keys_result[names[0]]
#        self.stack.append(self.process[name[0]])
        #need[str(names[0])] = self.process[str(name[0])].result[str(names[0])]
#        print(names)
#        print("Process that gives {} is {}".format(need, self.process[name[0]]))
#        print("Need in find_process_for_stack_update : ", need)
    #    for need in need:
    #        if need not in self.process.
#        return 

    def start_simulation(self):
        print(self.keys_result)
        self.queue.append([{self.start_needs[0] : 0}])
        print(self)
        while self.cycle < self.max_cycle:
            self.cycle += 10
            self.recursive_stack_update(self.queue[0][-1], len(self.queue[0][-1]))
            print(self)

    def __str__(self):
        return '{}\n\n\033[4mSimulation status at epoch {}\033[0m :\n\nStocks :\n\n{}\n\nQueue :\n\n{}\n\nStack :\n\n{}\n\n{}'\
                .format('-'*100, self.cycle, self.stocks, self.queue, self.stack, '-'*100)

        

"""class Simulation:
    def __init__(self, options, parser):
        self.max_cycle = options.delay
        self.graph = graph
        self.cycle = 0
        self.solution = []
        self.define_start_needs()
        self.stack = []
        self.stock_keys = dict(list(self.graph.stocks.items()))
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

    def refresh_stock_qty(self, info_stock_update, ope='-'):
        if ope == '-':
            self.graph.stocks[info_stock_update[0]] -= info_stock_update
#            self.graph.stocks[info_stock_update[0]].qty -= info_stock_update[1].qty
        elif ope == '+':
            self.graph.stocks[info_stock_update[0]] += info_stock_update

    def update_stocks(self, new_stock, operation='-'):
        keys = list(new_stock.keys())
        for key in keys:
            if operation == '+':
                if self.check_curr_stock_in_stocks(key, new_stock[key], True):
                    print("Stock key exists for {}".format(key))
                else:
                    print("Stock key does no exists for {}".format(key))
            elif operation == '-':
                #print(key, new_stock[key].qty)
                if self.check_curr_stock_in_stocks(key, new_stock[key]):
                    print("Stock key exists for {}".format(key))
                    print("Removing {} {} from stocks".format(new_stock[key], key))
                    self.refresh_stock_qty((key, new_stock[key]), '-')
                else:
                    print("Error, trying to remove {} but {} does not exists in stocks".format((key, new_stock[key]), key))

    def start_simulation(self):
        print("Simluation first needs : ",self.start_needs[0])
        print('-'*100,'\n\n', self)
        self.queue.append(self.start_needs[0])
        print(self.graph.stocks.items())
        self.update_stocks(self.graph.stocks.items(), '-')
        print('-'*100, '\n\n',self)
        self.update_stocks(self.graph.stocks.items(), '+')
#        self.update_stocks({'euro' : self.graph.stocks['euro']}, '-')
        print('-'*100, '\n\n',self)
#        self.update_stocks({'euro' : self.graph.stocks['euro'] + 1}, '+')"""

























