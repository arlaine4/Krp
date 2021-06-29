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
        self.assertEqual(self.parser.stocks['bonbon'].name, 'bonbon')
        self.assertEqual(self.parser.stocks['bonbon'].qty, 10)
        self.assertEqual(self.parser.stocks['moi'].name, 'moi')
        self.assertEqual(self.parser.stocks['moi'].qty, 1)

    def test_process(self):
        self.assertEqual(self.parser.content['manger'].name, 'manger')
        self.assertEqual(self.parser.content['manger'].need, {'bonbon' : 1})
        self.assertEqual(self.parser.content['manger'].result, {})
        self.assertEqual(self.parser.content['manger'].delay, 10)

        self.assertEqual(self.parser.content['jouer_a_la_marelle'].name, 'jouer_a_la_marelle')
        self.assertEqual(self.parser.content['jouer_a_la_marelle'].need, {'bonbon' : 5, 'moi' : 1})
        self.assertEqual(self.parser.content['jouer_a_la_marelle'].result, {'moi' : 1, 'marelle' : 1})
        self.assertEqual(self.parser.content['jouer_a_la_marelle'].delay, 20)

        self.assertEqual(self.parser.content['parier_avec_un_copain'].name, 'parier_avec_un_copain')
        self.assertEqual(self.parser.content['parier_avec_un_copain'].need, {'bonbon' : 2, 'moi' : 1})
        self.assertEqual(self.parser.content['parier_avec_un_copain'].result, {'moi' : 1, 'bonbon' : 3})
        self.assertEqual(self.parser.content['parier_avec_un_copain'].delay, 10)

        self.assertEqual(self.parser.content['parier_avec_un_autre_copain'].name, 'parier_avec_un_autre_copain')
        self.assertEqual(self.parser.content['parier_avec_un_autre_copain'].need, {'moi' : 1, 'bonbon' : 2})
        self.assertEqual(self.parser.content['parier_avec_un_autre_copain'].result, {'moi' : 1, 'bonbon' : 1})
        self.assertEqual(self.parser.content['parier_avec_un_autre_copain'].delay, 10)

        self.assertEqual(self.parser.content['se_battre_dans_la_cours'].name, 'se_battre_dans_la_cours')
        self.assertEqual(self.parser.content['se_battre_dans_la_cours'].need, {'moi' : 1})
        self.assertEqual(self.parser.content['se_battre_dans_la_cours'].result, {'moi' : 1, 'bonbon' : 1})
        self.assertEqual(self.parser.content['se_battre_dans_la_cours'].delay, 50)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['marelle'])

if __name__ == '__main__':
    unittest.main()
