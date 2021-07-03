from math import ceil
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Any, Generic, TypeVar
from copy import deepcopy

from krpsim.parsing import Process

T = TypeVar('T')

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
    
    def __str__(self) -> str:
        return f'[{self.name} * {self.times}]'
        string: str = f'Depth\033[0m: {self.depth} \033[38;5;74mList\033[0m: '
        for process in self.process_list:
            string += f'{process} '
        return string


@dataclass
class Node:
    """
    Collection of processes and stock
    list: list of tuple of process names and their number of executions
    _depth: distance from starting process
    _stock: dict containing the state of the stock current node 
    """

    _process_list: list[NodeElem]
    _stock: dict[str, int]
    _parent: Any = None
    _depth: int = 0


    @property
    def process_list(self) -> dict[str, int]:
        return self._process_list
    
    @property
    def stock(self) -> dict[str, int]:
        return self._stock
    
    @property
    def depth(self) -> int:
        return self._depth

    def __str__(self) -> str:
        string: str = f'Depth\033[0m: {self.depth} \033[38;5;74mList\033[0m: '
        for process in self.process_list:
            string += f'[{process.name} * {process.times}] '
        return string
    
    def __add__(self, other):
        return Node([*self.process_list, *other.process_list], self.depth, self.stock)
    
    def __radd__(self, other):
        return self if other == 0 else self.__add__(other)
    
    @staticmethod
    def combinations(matrix: list[list[Generic[T]]]) -> list[list[T]]:
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
            .transpose() \
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

    def get_root(self) -> Node:
        """
        Get root nodes that produces the stock to optimize
        returns: a node with a list of process that produces the stock to optimize
        """
        process_list: list[NodeElem] = [NodeElem(p.name, 1) for p in self.produces[self.optimize]]
        return Node(process_list, deepcopy(self.stock))

    def get_process_children(self, parent_process: NodeElem, depth: int, stock: dict[str, int]) -> list[Node]:
        """
        Get all possible nodes that produce stocks that is needed by parent
        returns: list of combinations of nodes that produces stocks needed by
            one of the process (parent) of the parent node
        """
        matrices: list[list[NodeElem]] = []
        for need, qty in self.process[parent_process.name].need.items():
            if stock.get(need, 1) >= qty:
                continue
            matrices.append([NodeElem(p.name, ceil(qty / (p.result[need] + stock[need]))) for p in self.produces[need]])
        combinations = Node.combinations(matrices)
        return [Node(lst, depth + 1, deepcopy(stock)) for lst in combinations]

    def get_children(self, parent: Node) -> list[Node]:
        """
        Get a combination of all possible needed process as nodes
        parent: current node of processes
        returns: list of combinations of nodes that produces stocks needed by
            all the processes in the parent node
        """
        nodes_lists: list[list[Node]] = [self.get_process_children(process, parent.depth, parent.stock) for process in parent.process_list]
        nodes_combinations = Node.combinations(nodes_lists)
        children = [sum(nodes) for nodes in nodes_combinations]
        parent.children = children
        return children
    
    def get_sequences(self, max_cycle: int = 10000) -> list[list[Node]]:
        """
        Get all paths of processes recursively
        max_cycle: maximum number of cycles that a sequence of process can take
        returns: list of all sequences of process that optimize the wanted stock
        """
        pass
