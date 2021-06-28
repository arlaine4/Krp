import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
import utils

class TestUtils(unittest.TestCase):
    
    def setup(self):
        options = {
            "delay": 1,
            "input_path": "ressources/ikea",
            "debug": False
        }
        self.parsing_test = Parser(options)

        self.comment_line = "# This is a comment"
        self.valid_stock_line = "stock:1"
        self.valid_process_line = "process:(input:1):(output:1):1"
        self.valid_optimize_line = "optimize:(time;stock)"

    def test_parse_line(self):
        
        self.assertEqual(utils.parse_line(self.valid_stock_line).__str__, "Stock -> stock : 1")
        # with self.assertRaises(ValueError):
        #     utils.parse_line()

    def test_split_need_result_delay(self):
        pass
        # with self.assertRaises(ValueError):
        #     utils.split_need_result_delay()

    def build_process_dic(self):
        pass


if __name__ == '__name__':
    unittest.main()