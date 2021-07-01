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
        self.stocks = {}
        self.content = {}
        self.optimize = []
        self.verbose = options.verbose
        self.fd = open(self.path, 'r+')

    def main_parsing(self):
        """
        Main parsing loop, the goal here is to iterate over
        the fd content, and to parse every line we encounter to
        determine its type
        """
        curr_line = None
        for line in self.fd:
            if line[0] == '#':
                print("Found a comment") if self.verbose == 1 or self.verbose == 3 else 0
                continue
            elif len(line) == 1 and line[0] == '\n':
                print("Skipping empty line") if self.verbose == 1 or self.verbose == 3 else 0
                continue
            else:
                curr_line = utils.parse_line(line)
                self.fill_parser_lists(curr_line)
                print(curr_line) if self.verbose == 1 or self.verbose == 3 else 0
        self.fd = self.fd.close()

    def fill_parser_lists(self, line):
        """
        Comparing the line type after utils.parse_line,
        we compare class instances with the base classes
        """
        if type(line) is Process:
            self.content[line.name] = line
        elif type(line) is Optimize:
            self.optimize.append(line)
        elif type(line) is Stock:
            self.stocks[line.name] = line


    def verify_parsing_content(self):
        """
        Afterward check method for the parsing content
        """
        if not self.optimize:
            sys.exit("Missing optimize content.")
        elif not self.stocks:
            sys.exit("Missing initial stocks.")
        elif not self.content:
            sys.exit("No process detected inside {}, please provide at least one".format(self.path))
        #Check if there is at most two optimize elems and if one of them is time
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
        return '\033[1mStock\033[0m -> \033[38;5;155m{}\033[0m : {}'.format(self.name, self.qty)

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
        return '\033[38;5;74m{}\033[0m - \033[1mneeds\033[0m : {} -> \033[1mresult\033[0m : {} - \033[1mdelay\033[0m : {}'\
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
       # if 'time' in elems:
       #     elems.pop(elems.index('time'))
        self.opti_elems = [i for i in elems]

    def __str__(self):
        return '\033[1mOptimize\033[0m -> \033[38;5;218m{}\033[0m'.format(str(self.opti_elems).replace('[', '').replace(']', ''))
    
    def __eq__(self, other):
        return self.opti_elems == other.opti_elems
