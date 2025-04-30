from dataclasses import dataclass

@dataclass
class Node:
    line: int
    column: int

@dataclass
class VariableDeclaration(Node):
    name: str
    var_type: str
    params: list
    constraints: list

@dataclass
class ArrayDeclaration(Node):
    name: str
    element_type: str
    size: Node
    constraints: list

@dataclass
class MatrixDeclaration(Node):
    name: str
    element_type: str
    rows: int
    cols: int
    constraints: list

@dataclass
class GraphDeclaration(Node):
    name: str
    graph_type: str
    properties: dict