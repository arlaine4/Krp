import unittest
import krpsim.parsing as p

class Options:
    def __init__(self, delay, path, verbose):
        self.delay = delay
        self.input_path = path
        self.verbose = verbose

class TestParsing(unittest.TestCase): 
    def setUp(self):
        self.parser = p.Parser(Options(1, 'resources/inception', 0))
        self.parser.main_parsing()

    def test_len_parser_elems(self):
        self.assertEqual(len(self.parser.stocks), 1)
        self.assertEqual(len(self.parser.content), 11)
        self.assertEqual(len(self.parser.optimize), 1)

    def test_stock(self):
        self.assertEqual(self.parser.stocks['clock'].name, 'clock')
        self.assertEqual(self.parser.stocks['clock'].qty, 1)
    
    def test_process(self):
        self.assertEqual(self.parser.content['make_sec'].name, 'make_sec')
        self.assertEqual(self.parser.content['make_sec'].need, {'clock' : 1})
        self.assertEqual(self.parser.content['make_sec'].result, {'clock' : 1, 'second' : 1})
        self.assertEqual(self.parser.content['make_sec'].delay, 1)

        self.assertEqual(self.parser.content['make_minute'].name, 'make_minute')
        self.assertEqual(self.parser.content['make_minute'].need, {'second' : 60})
        self.assertEqual(self.parser.content['make_minute'].result, {'minute' : 1})
        self.assertEqual(self.parser.content['make_minute'].delay, 6)

        self.assertEqual(self.parser.content['make_hour'].name, 'make_hour')
        self.assertEqual(self.parser.content['make_hour'].need, {'minute' : 60})
        self.assertEqual(self.parser.content['make_hour'].result, {'hour' : 1})
        self.assertEqual(self.parser.content['make_hour'].delay, 36)

        self.assertEqual(self.parser.content['make_day'].name, 'make_day')
        self.assertEqual(self.parser.content['make_day'].need, {'hour' : 24})
        self.assertEqual(self.parser.content['make_day'].result, {'day' : 1})
        self.assertEqual(self.parser.content['make_day'].delay, 86)

        self.assertEqual(self.parser.content['make_year'].name, 'make_year')
        self.assertEqual(self.parser.content['make_year'].need, {'day' : 365})
        self.assertEqual(self.parser.content['make_year'].result, {'year' : 1})
        self.assertEqual(self.parser.content['make_year'].delay, 365)

        self.assertEqual(self.parser.content['start_dream'].name, 'start_dream')
        self.assertEqual(self.parser.content['start_dream'].need, {'minute' : 1, 'clock' : 1})
        self.assertEqual(self.parser.content['start_dream'].result, {'dream' : 1})
        self.assertEqual(self.parser.content['start_dream'].delay, 60)

        self.assertEqual(self.parser.content['start_dream_2'].name, 'start_dream_2')
        self.assertEqual(self.parser.content['start_dream_2'].need, {'minute' : 1, 'dream' : 1})
        self.assertEqual(self.parser.content['start_dream_2'].result, {'dream' : 2})
        self.assertEqual(self.parser.content['start_dream_2'].delay, 60)

        self.assertEqual(self.parser.content['dream_minute'].name, 'dream_minute')
        self.assertEqual(self.parser.content['dream_minute'].need, {'second' : 1, 'dream' : 1})
        self.assertEqual(self.parser.content['dream_minute'].result, {'minute' : 1, 'dream' : 1})
        self.assertEqual(self.parser.content['dream_minute'].delay, 1)

        self.assertEqual(self.parser.content['dream_hour'].name, 'dream_hour')
        self.assertEqual(self.parser.content['dream_hour'].need, {'second' : 1, 'dream' : 2})
        self.assertEqual(self.parser.content['dream_hour'].result, {'hour' : 1, 'dream' : 2})
        self.assertEqual(self.parser.content['dream_hour'].delay, 1)

        self.assertEqual(self.parser.content['dream_day'].name, 'dream_day')
        self.assertEqual(self.parser.content['dream_day'].need, {'second' : 1, 'dream' : 3})
        self.assertEqual(self.parser.content['dream_day'].result, {'day' : 1, 'dream' : 3})
        self.assertEqual(self.parser.content['dream_day'].delay, 1)

        self.assertEqual(self.parser.content['end_dream'].name, 'end_dream')
        self.assertEqual(self.parser.content['end_dream'].need, {'dream' : 3})
        self.assertEqual(self.parser.content['end_dream'].result, {'clock' : 1})
        self.assertEqual(self.parser.content['end_dream'].delay, 60)

    def test_optimize(self):
        self.assertEqual(self.parser.optimize[0].opti_elems, ['year'])


if __name__ == '__main__':
    unittest.main()
