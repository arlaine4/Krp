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

    # Debug for graph
    if options.verbose >= 2:
        for stock, processes in graph.needs.items():
            print(f"\nProcesses that \033[31mneeds\033[0m {stock}:")
            for process in processes:
                print(f"{process}")
        for stock, processes in graph.produces.items():
            print(f"\nProcesses that \033[32mproduces\033[0m {stock}:")
            for process in processes:
                print(f"{process}")

    root = graph.get_root()
    children = graph.get_children(root)
    if options.verbose >= 2:
        for node in children:
            print(node)

