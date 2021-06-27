import argparse
import sys
import os

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
