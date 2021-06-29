import utils
import sys

class Parser:
    """
    Parsing Class, heart of the parsing is here.
    -> stocks is a list of Stock class instances
    -> content is a list of Process class instances
    -> optimize is a list of Optimize class instances
    -> delay corresponds to the maximal delay given as a parameter
    """
    def __init__(self, options):
        self.path, self.delay = options.input_path, options.delay
        self.stocks = []
        self.content = []
        self.optimize = []
        self.debug = options.debug
        self.fd = open(self.path, 'r+')

    def main_parsing(self):
        curr_line = None
        for line in self.fd:
            if line[0] == '#':
                print("Found a comment") if self.debug else 0
                continue
            elif len(line) == 1 and line[0] == '\n':
                print("Skipping empty line") if self.debug else 0
                continue
            else:
                curr_line = utils.parse_line(line)
                self.fill_parser_lists(curr_line)
                print(curr_line) if self.debug else 0
        self.fd = self.fd.close()

    def fill_parser_lists(self, line):
        if type(line) is Process:
            self.content.append(line)
        elif type(line) is Optimize:
            self.optimize.append(line)
        elif type(line) is Stock:
            self.stocks.append(line)


    def verify_parsing_content(self):
        if not self.optimize:
            sys.exit("Missing optimize content.")
        elif not self.stocks:
            sys.exit("Missing initial stocks.")
        elif not self.content:
            sys.exit("No process detected inside {}, please provide at least one".format(self.path))
        #Check if what need to be optimized is indeed inside at least one process and is accesible
        #like if the process never gets called because of stocks that can never be filled, then
        #the optimize values are not valid.

class Stock:
    """
    Stock elem associated Class
    -> name is obviously the stock name
    -> qty is the quantity available for this stock
    """
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

    def __str__(self):
        return 'Stock -> {} : {}'.format(self.name, self.qty)

    def __eq__(self, other):
        return self.name == other.name and self.qty == other.qty


class Process:
    """
    Process elem associated Class
    -> name is obviously the process name
    -> need is a list of stocks (name & qty) needed to run this process
    -> result is a list of resulting stocks after running the process
    -> delay is the delay needed to run the process
    """
    def __init__(self, name, need, result, delay):
        self.name = name
        self.need = need
        self.result = result
        self.delay = delay

    def __str__(self):
        return 'Process : {} - needs : {} -> result : {} - delay : {}'\
                .format(self.name, self.need, self.result, self.delay)
        
    def __eq__(self, other):
        return self.name == other.name and \
            self.delay == other.delay and \
            self.need == other.need and \
            self.result == other.result

class Optimize:
    """
    Optimize elem associated Class
    -> opti_elems is a list of name associated with what is
        to optimize, like client and time
    """
    def __init__(self, elems):
        self.opti_elems = [i for i in elems]

    def __str__(self):
        return 'Optimize -> {}'.format(self.opti_elems)
    
    def __eq__(self, other):
        return self.opti_elems == other.opti_elems
