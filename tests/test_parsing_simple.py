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
        self.parser = p.Parser(Options(1, 'resources/simple', False))
        self.parser.main_parsing()

    def test_simple_elems(self):
        self.assertEqual(len(self.parser.stocks), 1)
        self.assertEqual(len(self.parser.content), 3)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_process(self):
        self.assertEqual(self.parser.content['achat_materiel'].name, 'achat_materiel')
        self.assertEqual(self.parser.content['achat_materiel'].need, {'euro' : 8})
        self.assertEqual(self.parser.content['achat_materiel'].result, {'materiel' : 1})
        self.assertEqual(self.parser.content['achat_materiel'].delay, 10)

        self.assertEqual(self.parser.content['realisation_produit'].name, 'realisation_produit')
        self.assertEqual(self.parser.content['realisation_produit'].need, {'materiel' : 1})
        self.assertEqual(self.parser.content['realisation_produit'].result, {'produit' : 1})
        self.assertEqual(self.parser.content['realisation_produit'].delay, 30)

        self.assertEqual(self.parser.content['livraison'].name, 'livraison')
        self.assertEqual(self.parser.content['livraison'].need, {'produit' : 1})
        self.assertEqual(self.parser.content['livraison'].result, {'client_content' : 1})
        self.assertEqual(self.parser.content['livraison'].delay, 20)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['time', 'client_content'])

if __name__ == '__main__':
    unittest.main()
