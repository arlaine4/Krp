import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from parsing import Parsing

class TestParsing(unittest.TestCase):
    
    def setup(self):
        options = {
            "delay": 1,
            "input_path": "ressources/ikea",
            "debug": False
        }
        # self.parsing_test = Parser(options)

    def tearDown(self):
        pass

    def test_main_parsing(self):
        pass

    def test_fill_parser_lists(self):
        pass

    def test_verify_parsing_content(self):
        pass

if __name__ == '__main__':
    unittest.main()