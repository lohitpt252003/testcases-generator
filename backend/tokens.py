from enum import Enum

class TokenType(Enum):
    # Keywords
    VAR = 'var'
    INT = 'int'
    FLOAT = 'float'
    STRING = 'string'
    MATRIX = 'matrix'
    GRAPH = 'graph'
    TREE = 'tree'
    
    # Symbols
    COLON = ':'
    LPAREN = '('
    RPAREN = ')'
    LBRACKET = '['
    RBRACKET = ']'
    DOTDOT = '..'
    COMMA = ','
    EQUALS = '='
    
    # Literals
    IDENTIFIER = 'IDENTIFIER'
    INTEGER = 'INTEGER'
    FLOATVAL = 'FLOATVAL'
    STRINGLIT = 'STRINGLIT'
    
    # Special
    EOF = 'EOF'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"