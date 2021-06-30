import utils
from parsing import Parser
from graph import Graph
from solver import Solver

if __name__ == "__main__":
    # Parsing of CLI arguments
    options = utils.args_parsing()

    # Parsing of configuration file
    parser = Parser(options)
    parser.main_parsing()
    parser.verify_parsing_content()

    # Building a graph of processes
    graph = Graph(parser.content, parser.stocks, parser.optimize)
    graph.build_graph()

    # Debug graph
    if parser.debug:
        for stock, processes in graph.needs.items():
            print(f"\nProcesses that needs {stock}:")
            for process in processes:
                print(f"{process}")
        for stock, processes in graph.produces.items():
            print(f"\nProcesses that produces {stock}:")
            for process in processes:
                print(f"{process}")


    # Creating a list of possibles paths of processes (solutions) and their performances
    # graph.get_possible_paths()
    # graph.filter_usefull_paths()
    # graph.evaluate_path_productivity()

    # Run simulation of paths over many generations to find the fittest path
    # solver = Solver(parser, graph)
    # solution = solver.run_simulation()
