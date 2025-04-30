from ast_nodes import *
from error_handler import ErrorHandler

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        
    def analyze(self, ast):
        for node in ast:
            if isinstance(node, VariableDeclaration):
                self.check_variable_declaration(node)
                
    def check_variable_declaration(self, node):
        # Check for duplicate declarations
        if node.name in self.symbol_table:
            ErrorHandler.add_error(
                node.line, node.column,
                f"Duplicate declaration of '{node.name}'"
            )
        self.symbol_table[node.name] = node