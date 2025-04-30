from tokens import TokenType
from ast_nodes import *
from error_handler import ErrorHandler

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.next_token()
        
    def next_token(self):
        self.current_token = self.lexer.get_next_token()
        
    def parse(self):
        declarations = []
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.VAR:
                declarations.append(self.parse_variable_declaration())
            else:
                ErrorHandler.add_error(
                    self.current_token.line,
                    self.current_token.column,
                    f"Unexpected token {self.current_token.type}"
                )
                self.next_token()
        return declarations
    
    def parse_variable_declaration(self):
        # Implementation for parsing variable declarations
        pass