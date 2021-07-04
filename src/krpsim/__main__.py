from copy import deepcopy

from krpsim.utils import args_parsing
from krpsim.parsing import Parser
from krpsim.graph import Graph, Node, NodeElem

if __name__ == '__main__':
    # Parsing of CLI arguments
    options = args_parsing()

    # Parsing of configuration file
    parser = Parser(options)
    parser.main_parsing()
    parser.verify_parsing_content()

    optimize = parser.optimize[0].opti_elems
    if 'time' in optimize:
            optimize.remove('time')
    stock = { k: v.qty for k, v in parser.stocks.items() }

    # Building a graph of processes
    graph = Graph(parser.content, stock, optimize[0])
    graph.build()
    graph.sort()


    graph.start_dfs()
    if options.verbose >= 2:
        for i, path in enumerate(graph.paths):
            print(f'Path #{i}\n--------')
            for j, node in enumerate(path):
                print(f'Node #{j}')
                print(node)
            print('')
        

