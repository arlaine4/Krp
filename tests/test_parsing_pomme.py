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
        self.assertEqual(self.parser.stocks[0].name, 'four')
        self.assertEqual(self.parser.stocks[0].qty, 10)
        self.assertEqual(self.parser.stocks[1].name, 'euro')
        self.assertEqual(self.parser.stocks[1].qty, 10000)

    def test_process(self):
        self.assertEqual(self.parser.content[0].name, 'buy_pomme')
        self.assertEqual(self.parser.content[0].need, {'euro' : 100})
        self.assertEqual(self.parser.content[0].result, {'pomme' : 700})
        self.assertEqual(self.parser.content[0].delay, 200)

        self.assertEqual(self.parser.content[1].name, 'buy_citron')
        self.assertEqual(self.parser.content[1].need, {'euro' : 100})
        self.assertEqual(self.parser.content[1].result, {'citron'  : 400})
        self.assertEqual(self.parser.content[1].delay, 200)

        
        self.assertEqual(self.parser.content[2].name, 'buy_oeuf')
        self.assertEqual(self.parser.content[2].need, {'euro' : 100})
        self.assertEqual(self.parser.content[2].result, {'oeuf' : 100})
        self.assertEqual(self.parser.content[2].delay, 200)

        self.assertEqual(self.parser.content[3].name, 'buy_farine')
        self.assertEqual(self.parser.content[3].need, {'euro' : 100})
        self.assertEqual(self.parser.content[3].result, {'farine' : 800})
        self.assertEqual(self.parser.content[3].delay, 200)

        self.assertEqual(self.parser.content[4].name, 'buy_beurre')
        self.assertEqual(self.parser.content[4].need, {'euro' : 100})
        self.assertEqual(self.parser.content[4].result, {'beurre' : 2000})
        self.assertEqual(self.parser.content[4].delay, 200)

        self.assertEqual(self.parser.content[5].name, 'buy_lait')
        self.assertEqual(self.parser.content[5].need, {'euro' : 100})
        self.assertEqual(self.parser.content[5].result, {'lait' : 2000})
        self.assertEqual(self.parser.content[5].delay, 200)

        self.assertEqual(self.parser.content[6].name, 'separation_oeuf')
        self.assertEqual(self.parser.content[6].need, {'oeuf' : 1})
        self.assertEqual(self.parser.content[6].result, {'jaune_oeuf' : 1, 'blanc_oeuf' : 1})
        self.assertEqual(self.parser.content[6].delay, 2)

        self.assertEqual(self.parser.content[7].name, 'reunion_oeuf')
        self.assertEqual(self.parser.content[7].need, {'jaune_oeuf' : 1, 'blanc_oeuf' : 1})
        self.assertEqual(self.parser.content[7].result, {'oeuf' : 1})
        self.assertEqual(self.parser.content[7].delay, 1)

        self.assertEqual(self.parser.content[8].name, 'do_pate_sablee')
        self.assertEqual(self.parser.content[8].need, {'oeuf' : 5, 'farine' : 100, 'beurre' : 4, 'lait' : 5})
        self.assertEqual(self.parser.content[8].result, {'pate_sablee' : 300, 'blanc_oeuf' : 3})
        self.assertEqual(self.parser.content[8].delay, 300)

        self.assertEqual(self.parser.content[9].name, 'do_pate_feuilletee')
        self.assertEqual(self.parser.content[9].need, {'oeuf' : 3, 'farine' : 200, 'beurre' : 10, 'lait' : 2})
        self.assertEqual(self.parser.content[9].result, {'pate_feuilletee' : 100})
        self.assertEqual(self.parser.content[9].delay, 800)

        self.assertEqual(self.parser.content[10].name, 'do_tarte_citron')
        self.assertEqual(self.parser.content[10].need, {'pate_feuilletee' : 100, 'citron' : 50, 'blanc_oeuf' : 5, 'four' : 1})
        self.assertEqual(self.parser.content[10].result, {'tarte_citron' : 5, 'four' : 1})
        self.assertEqual(self.parser.content[10].delay, 60)

        self.assertEqual(self.parser.content[11].name, 'do_tarte_pomme')
        self.assertEqual(self.parser.content[11].need, {'pate_sablee' : 100, 'pomme' : 30, 'four' : 1})
        self.assertEqual(self.parser.content[11].result, {'tarte_pomme' : 8, 'four' : 1})
        self.assertEqual(self.parser.content[11].delay, 50)

        self.assertEqual(self.parser.content[12].name, 'do_flan')
        self.assertEqual(self.parser.content[12].need, {'jaune_oeuf' : 10, 'lait' : 4, 'four' : 1})
        self.assertEqual(self.parser.content[12].result, {'flan' : 5, 'four' : 1})
        self.assertEqual(self.parser.content[12].delay, 300)

        self.assertEqual(self.parser.content[13].name, 'do_boite')
        self.assertEqual(self.parser.content[13].need, {'tarte_citron' : 3, 'tarte_pomme' : 7, 'flan' : 1, 'euro' : 30})
        self.assertEqual(self.parser.content[13].result, {'boite' : 1})
        self.assertEqual(self.parser.content[13].delay, 1)

        self.assertEqual(self.parser.content[14].name, 'vente_boite')
        self.assertEqual(self.parser.content[14].need, {'boite' : 100})
        self.assertEqual(self.parser.content[14].result, {'euro' : 55000})
        self.assertEqual(self.parser.content[14].delay, 30)

        self.assertEqual(self.parser.content[15].name, 'vente_tarte_pomme')
        self.assertEqual(self.parser.content[15].need, {'tarte_pomme' : 10})
        self.assertEqual(self.parser.content[15].result, {'euro' : 100})
        self.assertEqual(self.parser.content[15].delay, 30)

        self.assertEqual(self.parser.content[16].name, 'vente_tarte_citron')
        self.assertEqual(self.parser.content[16].need, {'tarte_citron' : 10})
        self.assertEqual(self.parser.content[16].result, {'euro' : 200})
        self.assertEqual(self.parser.content[16].delay, 30)

        self.assertEqual(self.parser.content[17].name, 'vente_flan')
        self.assertEqual(self.parser.content[17].need, {'flan' : 10})
        self.assertEqual(self.parser.content[17].result, {'euro' : 300})
        self.assertEqual(self.parser.content[17].delay, 30)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['euro'])


if __name__ == '__main__':
    unittest.main()
