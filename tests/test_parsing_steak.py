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
        self.parser = p.Parser(Options(1, 'resources/steak', False))
        self.parser.main_parsing()

    def test_simple_elems(self):
        self.assertEqual(len(self.parser.stocks), 2)
        self.assertEqual(len(self.parser.content), 5)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_process(self):
        self.assertEqual(self.parser.content[0].name, 'cuisson_1')
        self.assertEqual(self.parser.content[0].need, {'steak_cru' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content[0].result, {'steak_mi_cuit' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content[0].delay, 10)

        self.assertEqual(self.parser.content[1].name, 'cuisson_2')
        self.assertEqual(self.parser.content[1].need, {'steak_mi_cuit' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content[1].result, {'steak_cuit' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content[1].delay, 10)

        self.assertEqual(self.parser.content[2].name, 'cuisson_3')
        self.assertEqual(self.parser.content[2].need, {'steak_cru' : 1, 'steak_mi_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content[2].result, {'steak_mi_cuit' : 1, 'steak_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content[2].delay, 10)

        self.assertEqual(self.parser.content[3].name, 'cuisson_4')
        self.assertEqual(self.parser.content[3].need, {'steak_cru' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content[3].result, {'steak_mi_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content[3].delay, 10)

        self.assertEqual(self.parser.content[4].name, 'cuisson_5')
        self.assertEqual(self.parser.content[4].need, {'steak_mi_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content[4].result, {'steak_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content[4].delay, 10)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['time', 'steak_cuit'])

if __name__ == '__main__':
    unittest.main()
