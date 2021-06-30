import argparse
import sys
import os
import parsing
from copy import deepcopy

def parse_line(line):
    """
    Method used to parse a line and extract the corresponding elem
    tmp -> Used for splitting the line and removing some junk from the list
    res -> Class instance, either Stock, Process or Optimize
           every instance is filled with the corresponding params
    """
    tmp = None
    res = None
    line = line.replace('\n', '')
    tmp = [i for i in line.split(':')]
    tmp.pop(tmp.index('')) if '' in tmp else tmp
    # Parsing for stock elem
    if '(' not in line:
        if tmp[0].isalpha() and tmp[1].isdecimal() or\
                tmp[0].replace('_', '').isalpha() and tmp[1].isdecimal():
            res = parsing.Stock(tmp[0], int(tmp[1]))
        else:
            res = 'Error'
    # Parsing for optimize elem
    elif 'optimize:' in line:
        if tmp[-1].isdigit():
            sys.exit("You can't specify a delay for an optimize element, error with \033[4m{}\033[0m"
                    .format(line))
        tmp = str(tmp[1]).replace('(', '').replace(')', '')
        res = parsing.Optimize(tmp.split(';'))
    # Parsing for process elem
    elif tmp[-1].isdigit():
        tmp = [i.replace(')', '') for i in line.split('(')]
        name, need, result, delay = split_need_result_delay(tmp, line)
        res = parsing.Process(name, build_process_dic(need), build_process_dic(result), delay)
    # Invalid elem
    elif not tmp[-1].isdigit():
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
    # len(content) == 3 is when we have both needs and result for the process
    if len(content) == 3:
        need = content[1].split(';')
        need = [i.split(':') for i in need]
        result = content[2].split(';')
        result = [i.split(':') for i in result]
    # len(content) == 2 is when we are either missing needs or result for the process
    # We want to create an empty need if we are missing it, same for result
    elif len(content) == 2:
        if check_no_need_or_result(content[0]) == "result":
            need, result = split_need_result(content[1], 'result')
            #need = []
            #result = content[1].split(';')
            #result = [i.split(':') for i in result]
        elif check_no_need_or_result(content[0]) == "need":
            need, result = split_need_result(content[1], 'need')
            #result = []
            #need = content[1].split(';')
            #need = [i.split(':') for i in need]
    # Just removing unwanted junk at the end of the result list if there is any
    for i in range(len(result)):
        if len(result[i]) > 2:
            result[i].pop(-1)
    delay = content[2].split(':') if len(content) == 3 else content[1].split(':')
    try:
        delay = int(delay[-1])
    except:
        sys.exit("Invalid type for delay in process : {}.".format(line))
    if len(result) != 0 and result[0][-2].isdigit() and result[0][-1].isdigit() and delay == int(result[0][-1]):
        result = result[0][0:-1]
    return name, need, result, delay


def split_need_result(content, ret=''):
    if ret == 'result':
        need = []
        result = content.split(';')
        result = [i.split(':') for i in result]
    elif ret == 'need':
        result = []
        need = content.split(';')
        need = [i.split(':') for i in need]
    return need, result


def check_no_need_or_result(content):
    """
    Little method used when the len of content equals 2.
    If the lenght isn't 3 it means that we are missing something,
    either needs or result.
    Here we just determine if the need or result is missing
    """
    if content.count(':') == 2:
        return 'result'
    else:
        return 'need'


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


def is_valid_file(path):
    """
    Method passed in argparse to check if the input file is valid
    """
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("{0} is not a valid file".format(path))
    return path


def args_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=is_valid_file, help='path to input file')
    parser.add_argument('delay', type=int, help='max delay for the program (delay >= 1)')
    parser.add_argument('-v', '--verbose', type=int, help='verbose mode, 1 for parsing and 2 for process verbose')
    options = parser.parse_args()
    if options.delay < 1:
        parser.error("Minimum delay is 1")
    print("Valid parameters ✅, mooving on to optimization for \033[4m{}\033[m with a delay of \033[4m{}\033[0m."
                .format(options.input_path, options.delay))
    return options
