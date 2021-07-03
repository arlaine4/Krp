import unittest
import krpsim.parsing as p

class Options:
    def __init__(self, delay, path, verbose):
        self.delay = delay
        self.input_path = path
        self.verbose = verbose

class TestParsing(unittest.TestCase): 
    def setUp(self):
        self.parser = p.Parser(Options(1, 'resources/ikea', 0))
        self.parser.main_parsing()

    def test_ikea_stock(self):
        self.assertEqual(len(self.parser.stocks), 1)
        self.assertEqual(self.parser.stocks['planche'].name, 'planche')
        self.assertEqual(self.parser.stocks['planche'].qty, 7)

    def test_ikea_process_zero(self):
        self.assertEqual(len(self.parser.content), 4)
        self.assertEqual(self.parser.content['do_montant'].name, 'do_montant')
        self.assertEqual(self.parser.content['do_montant'].need, {'planche' : 1})
        self.assertEqual(self.parser.content['do_montant'].result, {'montant' : 1})
        self.assertEqual(self.parser.content['do_montant'].delay, 15)

    def test_ikea_process_one(self):
        self.assertEqual(self.parser.content['do_fond'].name, 'do_fond')
        self.assertEqual(self.parser.content['do_fond'].need, {'planche' : 2})
        self.assertEqual(self.parser.content['do_fond'].result, {'fond' : 1})
        self.assertEqual(self.parser.content['do_fond'].delay, 20)

    def test_ikea_process_two(self):
        self.assertEqual(self.parser.content['do_etagere'].name, 'do_etagere')
        self.assertEqual(self.parser.content['do_etagere'].need, {'planche' : 1})
        self.assertEqual(self.parser.content['do_etagere'].result, {'etagere' : 1})
        self.assertEqual(self.parser.content['do_etagere'].delay, 10)
                
    def test_ikea_process_three(self):
        self.assertEqual(self.parser.content['do_armoire_ikea'].name, 'do_armoire_ikea')
        self.assertEqual(self.parser.content['do_armoire_ikea'].need, {'montant' : 2, 'fond' : 1, 'etagere' : 3})
        self.assertEqual(self.parser.content['do_armoire_ikea'].result, {'armoire' : 1})
        self.assertEqual(self.parser.content['do_armoire_ikea'].delay, 30)

    def test_ikea_optimize(self):
        self.assertEqual(len(self.parser.optimize), 1)
        self.assertEqual(self.parser.optimize[0].opti_elems, ['time', 'armoire'])

if __name__ == '__main__':
    unittest.main()
