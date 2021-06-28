import argparse
import sys
import os
import parsing
from copy import deepcopy

def parse_line(line):
    """
    Method used to parse a line and extract the corresponding elem
    res -> Class instance, either Stock, Process or Optimize
           every instance is filled with the corresponding params
    """
    tmp = None
    res = None
    line = line.replace('\n', '')
    tmp = [i for i in line.split(':')]
    tmp.pop(tmp.index('')) if '' in tmp else tmp
    if '(' not in line: #Parsing for stock
        if tmp[0].isalpha() and tmp[1].isdecimal() or\
                tmp[0].replace('_', '').isalpha() and tmp[1].isdecimal():
            res = parsing.Stock(tmp[0], tmp[1])
        else:
            res = 'Error'
    elif 'optimize:' in line: #Parsing for optimize
        if tmp[-1].isdigit():
            sys.exit("You can't specify a delay for an optimize element, error with \033[4m{}\033[0m"
                    .format(line))
        tmp = str(tmp[1]).replace('(', '').replace(')', '')
        res = parsing.Optimize(tmp.split(';'))
    elif tmp[-1].isdigit(): #Parsing for process
        tmp = [i.replace(')', '') for i in line.split('(')]
        name, need, result, delay = split_need_result_delay(tmp, line)
        res = parsing.Process(name, build_process_dic(need), build_process_dic(result), delay)
    elif not tmp[-1].isdigit(): #Invalid
        sys.exit("Error with \033[4m{}\033[0m, invalid element.".format(line))
    return res


def split_need_result_delay(content, line):
    """
    Method used to split a list of string into the corresponding
    elems to build a Process instance, we extract the name, the needs
    and results for this process, and finally the delay needed to run this
    process
    """
    name = content[0]
    name = name.replace(':', '')
    need = content[1].split(';')
    need = [i.split(':') for i in need]
    result = content[2].split(';')
    result = [i.split(':') for i in result]
    for i in range(len(result)):
        if len(result[i]) > 2:
            result[i].pop(-1)
    delay = content[2].split(':')
    try:
        delay = int(delay[-1])
    except:
        sys.exit("Invalid type for delay in process : {}.".format(line))
    if result[0][-2].isdigit() and result[0][-1].isdigit() and delay == int(result[0][-1]):
        result = result[0][0:-1]
    return name, need, result, delay


def build_process_dic(lst):
    """
    Simple method to build a dictionnary for process need and results
    from a list such as ['cake', '8', 'dollar', '20'] wich will result in
                        {'cake' : 8, 'dollar' : 20}
    """
    dico = {}
    i = 0
    for i, elem in enumerate(lst):
        if elem[-1] == '':
            elem.pop(-1)
        dico[elem[0]] = int(elem[1])
        i += 1
    return dico

def args_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='path to input file')
    parser.add_argument('delay', help='max delay for the program')
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
    options = parser.parse_args()
    return options


def check_valid_options(options):
    """
    Method used to check valid arguments, checking
    path / delay params validity
    """
    if not options.input_path:
        sys.exit('Missing input file.')
    if not options.delay:
        sys.exit('Missing delay.')
    try:
        tmp_d = int(options.delay)
    except ValueError:
        sys.exit('Invalid data type for delay.')
    try:
        tmp = str(options.delay)
    except ValueError:
        sys.exit('Invalid data type for input path.')
    if tmp_d <= 0:
        sys.exit('Invalid delay, please enter a value greater than one')
    if not os.path.exists(options.input_path):
        sys.exit('Input path given does not exist, please enter a valid path for an existing file.')
    if not os.path.isfile(options.input_path):
        sys.exit('Input path corresponds to a folder, please enter a file path.')
    else:
        print("Valid parameters ✅, mooving on to optimization for \033[4m{}\033[m with a delay of \033[4m{}\033[0m."
                .format(options.input_path, tmp_d))
