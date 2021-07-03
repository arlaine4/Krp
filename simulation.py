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
            print(opti.opti_elems)
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

    def get_starting_stack_and_queue(self):
        self.queue.append(self.start_needs)
        self.stack.append(self.keys_res_p[self.start_needs[0]])

    def recursive_stack_and_queue_update(self):
        if self.stop_recursion:
            return
        else:
            print(self)
            return
            #add condition check le contenu de la queue, si elle est vide
            # on set self.stop_recursion a False et on arrete la recursion
            # avec une stack remplie de process

    def start_simulation(self):
        print("Keys results from processes : ", self.keys_res_p)
        print("Max Cycle : ", self.max_cycle)
        print(self.start_needs)
        self.get_starting_stack_and_queue()
        self.recursive_stack_and_queue_update()
