import argparse
import sys
import os
import parsing
from copy import deepcopy

def parse_line(line):
    tmp = None
    res = None
    tmp = [i.replace('\n', '') for i in line.split(':')]
    tmp.pop(tmp.index('')) if '' in tmp else tmp
    if '(' not in line:
        if tmp[0].isalpha() and tmp[1].isdecimal() or\
                tmp[0].replace('_', '').isalpha() and tmp[1].isdecimal():
            res = parsing.Stock(tmp[0], tmp[1])
        else:
            res = 'Error'
    elif 'optimize:' in line:
        tmp = str(tmp[1]).replace('(', '').replace(')', '')
        res = parsing.Optimize(tmp.split(';'))
    else:
        name = tmp[0]
        tmp.pop(0)
        delay = tmp[-1]
        tmp.pop(-1)
        if check_comma_inside_lst_process(tmp):
            tmp = reshape_process_info_before_dic(tmp)
        res = parsing.Process(name, build_process_dictionnary(tmp), delay)
    return res


def check_comma_inside_lst_process(process):
    for elem in process:
        if ';' in elem:
            return True
    return False


def reshape_process_info_before_dic(process):
    process = [i.replace('(', '').replace(')', '') for i in process]
    print(process)
    for i in range(len(process)):
        print(process[i])
        if ';' in process[i]:
            tmp = process[i].split(';')
            process.insert(i + 1, tmp[1])
            process[i] = tmp[0]
    return process


def build_process_dictionnary(lst):
    dico = {}
    lst = [i.replace('(', '').replace(')', '') for i in lst]
    for i in range(0, len(lst) , 2):
        dico[lst[i]] = int(lst[i + 1])
    return dico


def args_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='path to input file')
    parser.add_argument('delay', help='max delay for the program')
    options = parser.parse_args()
    return options


def check_valid_options(options):
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
