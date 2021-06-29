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
        self.parser = p.Parser(Options(1, 'resources/inception', False))
        self.parser.main_parsing()

    def test_len_parser_elems(self):
        self.assertEqual(len(self.parser.stocks), 1)
        self.assertEqual(len(self.parser.content), 11)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_stock(self):
        self.assertEqual(self.parser.stocks[0].name, 'clock')
    
    def test_process(self):
        self.assertEqual(self.parser.content[0].name, 'make_sec')
        self.assertEqual(self.parser.content[0].need, {'clock' : 1})
        self.assertEqual(self.parser.content[0].result, {'clock' : 1, 'second' : 1})
        self.assertEqual(self.parser.content[0].delay, 1)

        self.assertEqual(self.parser.content[1].name, 'make_minute')
        self.assertEqual(self.parser.content[1].need, {'second' : 60})
        self.assertEqual(self.parser.content[1].result, {'minute' : 1})
        self.assertEqual(self.parser.content[1].delay, 6)

        self.assertEqual(self.parser.content[2].name, 'make_hour')
        self.assertEqual(self.parser.content[2].need, {'minute' : 60})
        self.assertEqual(self.parser.content[2].result, {'hour' : 1})
        self.assertEqual(self.parser.content[2].delay, 36)

        self.assertEqual(self.parser.content[3].name, 'make_day')
        self.assertEqual(self.parser.content[3].need, {'hour' : 24})
        self.assertEqual(self.parser.content[3].result, {'day' : 1})
        self.assertEqual(self.parser.content[3].delay, 86)

        self.assertEqual(self.parser.content[4].name, 'make_year')
        self.assertEqual(self.parser.content[4].need, {'day' : 365})
        self.assertEqual(self.parser.content[4].result, {'year' : 1})
        self.assertEqual(self.parser.content[4].delay, 365)

        self.assertEqual(self.parser.content[5].name, 'start_dream')
        self.assertEqual(self.parser.content[5].need, {'minute' : 1, 'clock' : 1})
        self.assertEqual(self.parser.content[5].result, {'dream' : 1})
        self.assertEqual(self.parser.content[5].delay, 60)

        self.assertEqual(self.parser.content[6].name, 'start_dream_2')
        self.assertEqual(self.parser.content[6].need, {'minute' : 1, 'dream' : 1})
        self.assertEqual(self.parser.content[6].result, {'dream' : 2})
        self.assertEqual(self.parser.content[6].delay, 60)

        self.assertEqual(self.parser.content[7].name, 'dream_minute')
        self.assertEqual(self.parser.content[7].need, {'second' : 1, 'dream' : 1})
        self.assertEqual(self.parser.content[7].result, {'minute' : 1, 'dream' : 1})
        self.assertEqual(self.parser.content[7].delay, 1)

        self.assertEqual(self.parser.content[8].name, 'dream_hour')
        self.assertEqual(self.parser.content[8].need, {'second' : 1, 'dream' : 2})
        self.assertEqual(self.parser.content[8].result, {'hour' : 1, 'dream' : 2})
        self.assertEqual(self.parser.content[8].delay, 1)

        self.assertEqual(self.parser.content[9].name, 'dream_day')
        self.assertEqual(self.parser.content[9].need, {'second' : 1, 'dream' : 3})
        self.assertEqual(self.parser.content[9].result, {'day' : 1, 'dream' : 3})
        self.assertEqual(self.parser.content[9].delay, 1)

        self.assertEqual(self.parser.content[10].name, 'end_dream')
        self.assertEqual(self.parser.content[10].need, {'dream' : 3})
        self.assertEqual(self.parser.content[10].result, {'clock' : 1})
        self.assertEqual(self.parser.content[10].delay, 60)



if __name__ == '__main__':
    unittest.main()
