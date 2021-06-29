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
        self.parser = p.Parser(Options(1, 'resources/pomme', False))
        self.parser.main_parsing()

    def test_parsing_len_elems(self):
        self.assertEqual(len(self.parser.stocks), 2)
        self.assertEqual(len(self.parser.content), 18)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_stock(self):
        self.assertEqual(self.parser.stocks['four'].name, 'four')
        self.assertEqual(self.parser.stocks['four'].qty, 10)
        self.assertEqual(self.parser.stocks['euro'].name, 'euro')
        self.assertEqual(self.parser.stocks['euro'].qty, 10000)

    def test_process(self):
        self.assertEqual(self.parser.content['buy_pomme'].name, 'buy_pomme')
        self.assertEqual(self.parser.content['buy_pomme'].need, {'euro' : 100})
        self.assertEqual(self.parser.content['buy_pomme'].result, {'pomme' : 700})
        self.assertEqual(self.parser.content['buy_pomme'].delay, 200)

        self.assertEqual(self.parser.content['buy_citron'].name, 'buy_citron')
        self.assertEqual(self.parser.content['buy_citron'].need, {'euro' : 100})
        self.assertEqual(self.parser.content['buy_citron'].result, {'citron'  : 400})
        self.assertEqual(self.parser.content['buy_citron'].delay, 200)

        
        self.assertEqual(self.parser.content['buy_oeuf'].name, 'buy_oeuf')
        self.assertEqual(self.parser.content['buy_oeuf'].need, {'euro' : 100})
        self.assertEqual(self.parser.content['buy_oeuf'].result, {'oeuf' : 100})
        self.assertEqual(self.parser.content['buy_oeuf'].delay, 200)

        self.assertEqual(self.parser.content['buy_farine'].name, 'buy_farine')
        self.assertEqual(self.parser.content['buy_farine'].need, {'euro' : 100})
        self.assertEqual(self.parser.content['buy_farine'].result, {'farine' : 800})
        self.assertEqual(self.parser.content['buy_farine'].delay, 200)

        self.assertEqual(self.parser.content['buy_beurre'].name, 'buy_beurre')
        self.assertEqual(self.parser.content['buy_beurre'].need, {'euro' : 100})
        self.assertEqual(self.parser.content['buy_beurre'].result, {'beurre' : 2000})
        self.assertEqual(self.parser.content['buy_beurre'].delay, 200)

        self.assertEqual(self.parser.content['buy_lait'].name, 'buy_lait')
        self.assertEqual(self.parser.content['buy_lait'].need, {'euro' : 100})
        self.assertEqual(self.parser.content['buy_lait'].result, {'lait' : 2000})
        self.assertEqual(self.parser.content['buy_lait'].delay, 200)

        self.assertEqual(self.parser.content['separation_oeuf'].name, 'separation_oeuf')
        self.assertEqual(self.parser.content['separation_oeuf'].need, {'oeuf' : 1})
        self.assertEqual(self.parser.content['separation_oeuf'].result, {'jaune_oeuf' : 1, 'blanc_oeuf' : 1})
        self.assertEqual(self.parser.content['separation_oeuf'].delay, 2)

        self.assertEqual(self.parser.content['reunion_oeuf'].name, 'reunion_oeuf')
        self.assertEqual(self.parser.content['reunion_oeuf'].need, {'jaune_oeuf' : 1, 'blanc_oeuf' : 1})
        self.assertEqual(self.parser.content['reunion_oeuf'].result, {'oeuf' : 1})
        self.assertEqual(self.parser.content['reunion_oeuf'].delay, 1)

        self.assertEqual(self.parser.content['do_pate_sablee'].name, 'do_pate_sablee')
        self.assertEqual(self.parser.content['do_pate_sablee'].need, {'oeuf' : 5, 'farine' : 100, 'beurre' : 4, 'lait' : 5})
        self.assertEqual(self.parser.content['do_pate_sablee'].result, {'pate_sablee' : 300, 'blanc_oeuf' : 3})
        self.assertEqual(self.parser.content['do_pate_sablee'].delay, 300)

        self.assertEqual(self.parser.content['do_pate_feuilletee'].name, 'do_pate_feuilletee')
        self.assertEqual(self.parser.content['do_pate_feuilletee'].need, {'oeuf' : 3, 'farine' : 200, 'beurre' : 10, 'lait' : 2})
        self.assertEqual(self.parser.content['do_pate_feuilletee'].result, {'pate_feuilletee' : 100})
        self.assertEqual(self.parser.content['do_pate_feuilletee'].delay, 800)

        self.assertEqual(self.parser.content['do_tarte_citron'].name, 'do_tarte_citron')
        self.assertEqual(self.parser.content['do_tarte_citron'].need, {'pate_feuilletee' : 100, 'citron' : 50, 'blanc_oeuf' : 5, 'four' : 1})
        self.assertEqual(self.parser.content['do_tarte_citron'].result, {'tarte_citron' : 5, 'four' : 1})
        self.assertEqual(self.parser.content['do_tarte_citron'].delay, 60)

        self.assertEqual(self.parser.content['do_tarte_pomme'].name, 'do_tarte_pomme')
        self.assertEqual(self.parser.content['do_tarte_pomme'].need, {'pate_sablee' : 100, 'pomme' : 30, 'four' : 1})
        self.assertEqual(self.parser.content['do_tarte_pomme'].result, {'tarte_pomme' : 8, 'four' : 1})
        self.assertEqual(self.parser.content['do_tarte_pomme'].delay, 50)

        self.assertEqual(self.parser.content['do_flan'].name, 'do_flan')
        self.assertEqual(self.parser.content['do_flan'].need, {'jaune_oeuf' : 10, 'lait' : 4, 'four' : 1})
        self.assertEqual(self.parser.content['do_flan'].result, {'flan' : 5, 'four' : 1})
        self.assertEqual(self.parser.content['do_flan'].delay, 300)

        self.assertEqual(self.parser.content['do_boite'].name, 'do_boite')
        self.assertEqual(self.parser.content['do_boite'].need, {'tarte_citron' : 3, 'tarte_pomme' : 7, 'flan' : 1, 'euro' : 30})
        self.assertEqual(self.parser.content['do_boite'].result, {'boite' : 1})
        self.assertEqual(self.parser.content['do_boite'].delay, 1)

        self.assertEqual(self.parser.content['vente_boite'].name, 'vente_boite')
        self.assertEqual(self.parser.content['vente_boite'].need, {'boite' : 100})
        self.assertEqual(self.parser.content['vente_boite'].result, {'euro' : 55000})
        self.assertEqual(self.parser.content['vente_boite'].delay, 30)

        self.assertEqual(self.parser.content['vente_tarte_pomme'].name, 'vente_tarte_pomme')
        self.assertEqual(self.parser.content['vente_tarte_pomme'].need, {'tarte_pomme' : 10})
        self.assertEqual(self.parser.content['vente_tarte_pomme'].result, {'euro' : 100})
        self.assertEqual(self.parser.content['vente_tarte_pomme'].delay, 30)

        self.assertEqual(self.parser.content['vente_tarte_citron'].name, 'vente_tarte_citron')
        self.assertEqual(self.parser.content['vente_tarte_citron'].need, {'tarte_citron' : 10})
        self.assertEqual(self.parser.content['vente_tarte_citron'].result, {'euro' : 200})
        self.assertEqual(self.parser.content['vente_tarte_citron'].delay, 30)

        self.assertEqual(self.parser.content['vente_flan'].name, 'vente_flan')
        self.assertEqual(self.parser.content['vente_flan'].need, {'flan' : 10})
        self.assertEqual(self.parser.content['vente_flan'].result, {'euro' : 300})
        self.assertEqual(self.parser.content['vente_flan'].delay, 30)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['euro'])


if __name__ == '__main__':
    unittest.main()
