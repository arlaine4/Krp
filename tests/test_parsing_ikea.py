import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
import parsing as p

class Options:
    def __init__(self, delay, path, debug):
        self.delay = delay
        self.input_path = path
        self.debug = debug

class TestParsing(unittest.TestCase): 
    def setUp(self):
        self.parser = p.Parser(Options(1, 'resources/ikea', False))
        self.parser.main_parsing()

    def test_ikea_stock(self):
        self.assertEqual(len(self.parser.stocks), 1)
        self.assertEqual(self.parser.stocks[0].name, 'planche')
        self.assertEqual(self.parser.stocks[0].qty, 7)

    def test_ikea_process_zero(self):
        self.assertEqual(len(self.parser.content), 4)
        self.assertEqual(self.parser.content[0].name, 'do_montant')
        self.assertEqual(self.parser.content[0].need, {'planche' : 1})
        self.assertEqual(self.parser.content[0].result, {'montant' : 1})
        self.assertEqual(self.parser.content[0].delay, 15)

    def test_ikea_process_one(self):
        self.assertEqual(self.parser.content[1].name, 'do_fond')
        self.assertEqual(self.parser.content[1].need, {'planche' : 2})
        self.assertEqual(self.parser.content[1].result, {'fond' : 1})
        self.assertEqual(self.parser.content[1].delay, 20)

    def test_ikea_process_two(self):
        self.assertEqual(self.parser.content[2].name, 'do_etagere')
        self.assertEqual(self.parser.content[2].need, {'planche' : 1})
        self.assertEqual(self.parser.content[2].result, {'etagere' : 1})
        self.assertEqual(self.parser.content[2].delay, 10)
                
    def test_ikea_process_three(self):
        self.assertEqual(self.parser.content[3].name, 'do_armoire_ikea')
        self.assertEqual(self.parser.content[3].need, {'montant' : 2, 'fond' : 1, 'etagere' : 3})
        self.assertEqual(self.parser.content[3].result, {'armoire' : 1})
        self.assertEqual(self.parser.content[3].delay, 30)

    def test_ikea_optimize(self):
        self.assertEqual(len(self.parser.optimize), 1)
        self.assertEqual(self.parser.optimize[0].opti_elems, ['time', 'armoire'])

if __name__ == '__main__':
    unittest.main()
