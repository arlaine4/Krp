import utils

class Parser:
    def __init__(self, options):
        self.path, self.delay = options.input_path, options.delay
        self.stocks = []
        self.content = []
        self.fd = open(self.path, 'r+')

    def main_parsing(self):
        curr_line = None
        for line in self.fd:
            if line[0] == '#':
                print("Found a comment")
                continue
            else:
                curr_line = utils.parse_line(line)
                print("Found",curr_line)

    def verify_parsing_content(self):
        pass


class Stock:
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

    def __str__(self):
        return 'Stock -> {} : {}'.format(self.name, self.qty)


class Process:
    def __init__(self, name, content, delay):
        self.name = name
        self.content = content
        self.delay = delay

    def __str__(self):
        return 'Process -> {} : {}, delay : {}'.format(self.name, self.content, self.delay)

class Optimize:
    def __init__(self, elems):
        self.opti_elems = [i for i in elems]

    def __str__(self):
        return 'Optimize -> {}'.format(self.opti_elems)
