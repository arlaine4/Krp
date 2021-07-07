from math import ceil
import numpy as np
from dataclasses import dataclass, field
from typing import Any, TypeVar, Optional
from copy import deepcopy
import itertools

from krpsim.parsing import Process

# Custom types
T = TypeVar('T')
Matrix = list[list[T]]

COLOR_BLUE = '\033[38;5;74m'
RESET_COLOR = '\033[0m'

@dataclass
class NodeElem:
    """
    Wrapper around a process and the number of time it needs to be
    executed to produce enough stock for the parent process
    _name: name of process
    _times: number of times the process is needed to produce enough stock
    """
    _name: str
    _times: int

    @property
    def name(self) -> str:
        return self._name

    @property
    def times(self) -> int:
        return self._times

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @times.setter
    def times(self, value) -> None:
        self._times = value

    def __str__(self) -> str:
        return f'[{self.name} * {self.times}]'
    


@dataclass
class Node:
    """
    Collection of processes and stock
    list: list of tuple of process names and their number of executions
    _stock: dict containing the state of the stock current node 
    """

    _process_list: list[NodeElem]
    _stock: dict[str, int]


    @property
    def process_list(self) -> dict[str, int]:
        return self._process_list

    @property
    def stock(self) -> dict[str, int]:
        return self._stock

    @process_list.setter
    def process_list(self, value) -> None:
        self._process_list = value

    @stock.setter
    def stock(self, value) -> None:
        self._stock = value

    def __str__(self) -> str:
        
        string: str = f'{COLOR_BLUE}Processes{RESET_COLOR}: '
        for process in self.process_list:
            string += f'({process.name} * {process.times}) '
        string += f'| {COLOR_BLUE}Stocks{RESET_COLOR}: '
        for name, qty in self.stock.items():
            if qty != 0:
                string += f'({name}: {qty}) '
        return string

    def __add__(self, other):
        return Node([*self.process_list, *other.process_list], self.stock)

    def __radd__(self, other):
        return self if other == 0 else self.__add__(other)

    @staticmethod
    def combinations(matrix: Matrix) -> Matrix:
        """
        Get the combinations of elements in the matrix
        returns: matrix of combinations
        example: 
        matrix = [[1, 2, 3], [4, 5], [6, 7]]
        Node.combinations(matrix)
        [[1, 4, 6],
        [1, 5, 6],
        [2, 4, 6],
        [2, 5, 6],
        [3, 4, 6],
        [3, 5, 6],
        [1, 4, 7],
        [1, 5, 7],
        [2, 4, 7],
        [2, 5, 7],
        [3, 4, 7],
        [3, 5, 7]])
        """

        return np \
            .array(np.meshgrid(*matrix)) \
            .T \
            .reshape(-1, len(matrix)) \
            .tolist()



@dataclass
class Graph:
    """
    Class representing a graph of processes connected to each other by the stock they produce/need.
    _process: dict of processes.
    _stock: dict of stocks. dict[key: stock name, value: quantity]
    _optimize: name of stock to optimize
    _needs: dict of processes regrouped by the stock they need.
    """
    _process: dict[str, Process]
    _stock: dict[str, int]
    _optimize: str
    _needs: dict[str, list[Process]] = field(default_factory=dict)
    _produces: dict[str, list[Process]] = field(default_factory=dict)
    _paths: list[list[Node]] = field(default_factory=list)

    @property
    def process(self) -> dict[str, Process]:
        return self._process
    
    @property
    def stock(self) -> dict[str, int]:
        return self._stock
    
    @property
    def optimize(self) -> int:
        return self._optimize
    
    @property
    def needs(self) -> dict[str, list]:
        return self._needs
    
    @property
    def produces(self) -> dict[str, list]:
        return self._produces
    
    @property
    def paths(self) -> list[list[Node]]:
        return self._paths
    
    @process.setter
    def process(self, value) -> None:
        self._process = value
    
    @stock.setter
    def stock(self, value) -> None:
        self._stock = value
    
    @optimize.setter
    def optimize(self, value) -> None:
        self._optimize = value
    
    @needs.setter
    def needs(self, value) -> None:
        self._needs = value
    
    @produces.setter
    def produces(self, value) -> None:
        self._produces = value
    
    @paths.setter
    def paths(self, value) -> None:
        self._paths = value

    def sort(self) -> None:
        """
        Method that sorts processes by their needs and products
        """
        for stock, process in self.needs.items():
            process.sort(key=lambda p: p.need[stock])
        for stock, process in self.produces.items():
            process.sort(key=lambda p: p.result[stock], reverse=True)

    def build(self) -> None:
        """
        Method that builds a graph by regrouping and 
        """
        for process in self.process.values():
            for stock in process.need:
                self.needs.setdefault(stock, []).append(process)
                self.stock.setdefault(stock, 0)
            for stock in process.result:
                self.produces.setdefault(stock, []).append(process)
                self.stock.setdefault(stock, 0)

    def update_stocks(self, node: Node) -> None:
        for process in node.process_list:
            for need, qty in self.process[process.name].need.items():
                node.stock[need] -= qty
        return node

    def stocks_available(self, node: Node) -> Optional[bool]:
        dead_end = True
        available = True
        for node_elem in node.process_list:
            for need, qty in self.process[node_elem.name].need.items():
                if node.stock[need] <= 0 or qty < node.stock[need]:
                    available = False
                else:
                    dead_end = False
        return available if not dead_end else None
    
    def get_root(self) -> list[Node]:
        """
        Get root nodes that produces the stock to optimize
        returns: a node with a list of process that produces the stock to optimize
        """
        process_list: list[NodeElem] = [NodeElem(p.name, 1) for p in self.produces[self.optimize]]
        _node_list: list[Node] = [Node([process], deepcopy(self.stock)) for process in process_list]
        root: list[Node] = [self.update_stocks(node) for node in _node_list]
        return root

    def get_process_children(self, parent_process: NodeElem, stock: dict[str, int]) -> list[Node]:
        """
        Get all possible nodes that produce stocks that is needed by parent
        returns: list of combinations of nodes that produces stocks needed by
            one of the process (parent) of the parent node
        """
        matrices: Matrix = []
        for need, qty in self.process[parent_process.name].need.items():
            if stock.get(need, 1) >= qty:
                continue
            matrices.append([NodeElem(p.name, 1) for p in self.produces[need]])
        if not matrices:
            return []
        combinations = Node.combinations(matrices)
        return [Node(lst, deepcopy(stock)) for lst in combinations]

    def get_children(self, parent: Node) -> list[Node]:
        """
        Get a combination of all possible needed process as nodes
        parent: current node of processes
        returns: list of combinations of nodes that produces stocks needed by
            all the processes in the parent node
        """
        nodes_lists: Matrix = [self.get_process_children(process, parent.stock) for process in parent.process_list]
        nodes_combinations: Matrix = Node.combinations(nodes_lists)
        _children: list[Node] = [sum(nodes) for nodes in nodes_combinations]
        children: list[Node] = [self.update_stocks(node) for node in _children]
        return children
    
    def depth_first_search(self, current: Node, path: list[Node]) -> None:
        """
        Perfoms DFS to find every sequence of process that will be stored in self.paths
        current: the current node to explore
        """
        path.append(current)
        for child in self.get_children(current):
            path_found = self.stocks_available(child)
            if path_found == True:
                path.append(child)
                return paths.append(path)
            elif path_found == False:
                return self.depth_first_search(child, path)
            else:
                return None
        return None

    def start_dfs(self) -> None:
        root = self.get_root()
        for node in root:
            self.depth_first_search(node, [])