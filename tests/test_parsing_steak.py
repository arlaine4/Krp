import unittest
import krpsim.parsing as p

class Options:
    def __init__(self, delay, path, verbose):
        self.delay = delay
        self.input_path = path
        self.verbose = verbose

class TestParsing(unittest.TestCase): 
    def setUp(self):
        self.parser = p.Parser(Options(1, 'resources/steak', False))
        self.parser.main_parsing()

    def test_simple_elems(self):
        self.assertEqual(len(self.parser.stocks), 2)
        self.assertEqual(len(self.parser.content), 5)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_process(self):
        self.assertEqual(self.parser.content['cuisson_1'].name, 'cuisson_1')
        self.assertEqual(self.parser.content['cuisson_1'].need, {'steak_cru' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_1'].result, {'steak_mi_cuit' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_1'].delay, 10)

        self.assertEqual(self.parser.content['cuisson_2'].name, 'cuisson_2')
        self.assertEqual(self.parser.content['cuisson_2'].need, {'steak_mi_cuit' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_2'].result, {'steak_cuit' : 2, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_2'].delay, 10)

        self.assertEqual(self.parser.content['cuisson_3'].name, 'cuisson_3')
        self.assertEqual(self.parser.content['cuisson_3'].need, {'steak_cru' : 1, 'steak_mi_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_3'].result, {'steak_mi_cuit' : 1, 'steak_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_3'].delay, 10)

        self.assertEqual(self.parser.content['cuisson_4'].name, 'cuisson_4')
        self.assertEqual(self.parser.content['cuisson_4'].need, {'steak_cru' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_4'].result, {'steak_mi_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_4'].delay, 10)

        self.assertEqual(self.parser.content['cuisson_5'].name, 'cuisson_5')
        self.assertEqual(self.parser.content['cuisson_5'].need, {'steak_mi_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_5'].result, {'steak_cuit' : 1, 'poele' : 1})
        self.assertEqual(self.parser.content['cuisson_5'].delay, 10)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['time', 'steak_cuit'])

if __name__ == '__main__':
    unittest.main()
