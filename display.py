from operator import add, sub
from typing import Tuple
from dataclasses import dataclass

@dataclass
class display_base:
    cell_size: int = 20
    cell_width: int = 10
    cell_height: int = 10
    window_width = cell_size * cell_width
    window_height = cell_size * cell_height
    
    @staticmethod
    def node_add(node_a: Tuple[int, int], node_b: Tuple[int, int]):
        result: Tuple[int, int] = tuple(map(add, node_a, node_b))
        return result

    @staticmethod
    def node_sub(node_a: Tuple[int, int], node_b: Tuple[int, int]):
        result: Tuple[int, int] = tuple(map(sub, node_a, node_b))
        return result
    
    @staticmethod
    def mean(l):
        return round(sum(l) / len(l), 4)