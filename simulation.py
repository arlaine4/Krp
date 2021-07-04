class Simulation:
    def __init__(self, options, parser):
        self.start_needs = [[]]
        self.process = parser.content
        self.stocks = parser.stocks
        self.define_keys_res_process()
        self.max_cycle = self.define_max_delay(parser.optimize[0], options)
        self.cycle = 0
        self.solution = []
        self.stack = []
        self.queue = []
        self.stop_recursion = False

    def __str__(self):
        return '{}\n\n\033[4mSimulation status at epoch {}\033[0m :\n\nStocks :\n\n{}\n\nQueue :\n\n{}\n\nStack :\n\n{}\n\n{}'\
                .format('-'*100, self.cycle, self.stocks, self.queue, self.stack, '-'*100)

    def define_keys_res_process(self):
        self.keys_res_p = {}
        for elem in self.process:
            for res_key in self.process[elem].result:
                if res_key in self.keys_res_p:
                    self.keys_res_p[res_key].append(elem)
                else:
                    self.keys_res_p[res_key] = [elem]

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

    def available_stocks_for_process(self):
        key = list(self.stack[-1].need.keys())
        if key[0] in self.stocks and self.queue[-1][key[0]] <= self.stocks[key[0]].qty:
            return True
        return False

    def order_queue_filling(self):
        sub_queue = self.queue[-1]
        print(sub_queue)
        return

    def one_queue_stack_update(self):
        key = list(self.queue[-1].keys())
        s = self.keys_res_p[key[0]]
        self.stack.append(self.process[s[0]])
        print("bon ta mere la print : ", self.stack[-1].need)
        self.queue[0] = self.stack[-1].need
        if len(self.queue[-1]) > 1:
            self.order_queue_filling()

    def recursive_stack_queue_update(self):
        if not self.available_stocks_for_process():
            self.one_queue_stack_update()
           # key = list(self.queue[-1].keys())
           # s = self.keys_res_p[key[0]]
           # self.stack.append(self.process[s[0]])
           # self.queue[0] = self.stack[-1].need
           # key = list(self.queue[-1].keys())
            #while self.queue[0][key[0]] != 0:
            #    self.queue[0][key[0]] -= self.stack[-1].need[key[0]]
            #    if self.queue[0][key[0]] == 0:
            #        break
            #    self.stack.append(self.process[s[0]])
            print(self)
            self.recursive_stack_queue_update()
        else:
            return

    def start_simulation(self):
        print("\n\nKeys results from processes : ", self.keys_res_p)
        print("\n\nMax Cycle : ", self.max_cycle)
        print("\n\nFirst needs : ", self.start_needs[0])

        print("\n", self)
        # Do a callback that updates the stocks everytime a process is added to the stack
        key = self.keys_res_p[self.start_needs[0]]
        self.stack.append(self.process[key[0]])
        self.queue.append(self.stack[-1].need)
        self.recursive_stack_queue_update()
        for elem in self.stack:
            print(elem)
#        print(self)
#
#        key = list(self.queue[-1].keys())
#        s = self.keys_res_p[key[0]]
#        self.stack.append(self.process[s[0]])
#        self.queue.append(self.stack[-1].need)
#        print(self)
#
#        key = list(self.queue[-1].keys())
#        s = self.keys_res_p[key[0]]
#        self.stack.append(self.process[s[0]])
#        self.queue.append(self.stack[-1].need)
#        print(self)

#        key = list(self.queue[0].keys())
#        print(key[0], self.keys_res_p[key[0]])
#        s = self.keys_res_p[key[0]]
#        print(self.process, s[0])
                
#        self.stack.append(self.process[key[0]])
#        self.queue.append(self.stack[-1].need)



    """def recursive_stack_and_queue_update(self):
        if self.stop_recursion:
            return
        else:
            self.update_stack_and_queue(self.get_next_need())
            if self.stop_recursion:
                return
            else:
                return self.recursive_stack_and_queue_update()
            #add condition check le contenu de la queue, si elle est vide
            # on set self.stop_recursion a False et on arrete la recursion
            # avec une stack remplie de process"""

    """def update_stack_and_queue(self, need=None):
        if need is None:
            try:
                self.queue.append(self.start_needs)
                key = self.keys_res_p[self.start_needs[0]]
                self.stack.append(self.process[key[0]])
                #del(self.queue[0])
                self.stop_recursion = False
            except:
                self.stop_recursion = True
        else:
            try:
                self.queue.append(need)
                key = self.keys_res_p[need[0]]
                self.stack.append(self.process[key[0]])
                del(self.queue[0])
                self.stop_recursion = False
            except:
                self.stop_recursion = True"""
