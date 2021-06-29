import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
import utils
from parsing import Stock, Process, Optimize

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_parse_line_valid_stock(self):
        self.assertEqual(utils.parse_line("test:1"), Stock("test", 1))
    
    def test_parse_line_invalid_stock(self):
        with self.assertRaises(SystemExit) as e:
            utils.parse_line("test::1")
        self.assertEqual(e.exception.code, 0)

        


if __name__ == '__name__':
    unittest.main()