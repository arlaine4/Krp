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
        self.parser = p.Parser(Options(1, 'resources/recre', False))
        self.parser.main_parsing()

    def test_recre_elems(self):
        self.assertEqual(len(self.parser.stocks), 2)
        self.assertEqual(len(self.parser.content), 5)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_stocks(self):
        self.assertEqual(self.parser.stocks[0].name, 'bonbon')
        self.assertEqual(self.parser.stocks[0].qty, 10)
        self.assertEqual(self.parser.stocks[1].name, 'moi')
        self.assertEqual(self.parser.stocks[1].qty, 1)

    def test_process(self):
        self.assertEqual(self.parser.content[0].name, 'manger')
        self.assertEqual(self.parser.content[0].need, {'bonbon' : 1})
        self.assertEqual(self.parser.content[0].result, {})
        self.assertEqual(self.parser.content[0].delay, 10)

        self.assertEqual(self.parser.content[1].name, 'jouer_a_la_marelle')
        self.assertEqual(self.parser.content[1].need, {'bonbon' : 5, 'moi' : 1})
        self.assertEqual(self.parser.content[1].result, {'moi' : 1, 'marelle' : 1})
        self.assertEqual(self.parser.content[1].delay, 20)

        self.assertEqual(self.parser.content[2].name, 'parier_avec_un_copain')
        self.assertEqual(self.parser.content[2].need, {'bonbon' : 2, 'moi' : 1})
        self.assertEqual(self.parser.content[2].result, {'moi' : 1, 'bonbon' : 3})
        self.assertEqual(self.parser.content[2].delay, 10)

        self.assertEqual(self.parser.content[3].name, 'parier_avec_un_autre_copain')
        self.assertEqual(self.parser.content[3].need, {'moi' : 1, 'bonbon' : 2})
        self.assertEqual(self.parser.content[3].result, {'moi' : 1, 'bonbon' : 1})
        self.assertEqual(self.parser.content[3].delay, 10)

        self.assertEqual(self.parser.content[4].name, 'se_battre_dans_la_cours')
        self.assertEqual(self.parser.content[4].need, {'moi' : 1})
        self.assertEqual(self.parser.content[4].result, {'moi' : 1, 'bonbon' : 1})
        self.assertEqual(self.parser.content[4].delay, 50)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['marelle'])

if __name__ == '__main__':
    unittest.main()
