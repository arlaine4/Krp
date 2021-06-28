import utils
import parsing
import graph
import solver

if __name__ == "__main__":
    # Parsing of CLI arguments
    options = utils.args_parsing()
    print(options)

    # Parsing of configuration file
    parser = parsing.Parser(options)
    parser.main_parsing()
    parser.verify_parsing_content()

    # Building a graph of processes
    graph = graph.Graph(parser)

    # Creating a list of possibles paths of processes (solutions) and their performances
    graph.get_possible_paths()
    graph.filter_usefull_paths()
    graph.evaluate_path_productivity()

    # Run simulation of paths over many generations to find the fittest path
    solver = solver.Solver(parser, graph)
    solution = solver.run_simulation()
