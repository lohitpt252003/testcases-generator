from tokens import Token, TokenType
import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        
    def error(self, msg):
        from error_handler import ErrorHandler
        ErrorHandler.add_error(self.line, self.column, msg)
        
    def advance(self):
        self.pos += 1
        self.column += 1
        
    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            if self.text[self.pos] == '\n':
                self.line += 1
                self.column = 0
            self.advance()
            
    def get_next_token(self):
        while self.pos < len(self.text):
            char = self.text[self.pos]
            
            if char.isspace():
                self.skip_whitespace()
                continue
                
            # Match identifiers and keywords
            if char.isalpha():
                return self.match_identifier()
                
            # Match numbers
            if char.isdigit() or char == '.':
                return self.match_number()
                
            # Match symbols
            for token_type in TokenType:
                if token_type.value == char:
                    self.advance()
                    return Token(token_type, char, self.line, self.column-1)
                
            self.error(f"Unexpected character: {char}")
            self.advance()
            
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def match_identifier(self):
        buffer = ''
        start_col = self.column
        
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            buffer += self.text[self.pos]
            self.advance()
            
        # Check if it's a keyword
        for token_type in TokenType:
            if token_type.value == buffer.lower():
                return Token(token_type, buffer, self.line, start_col)
                
        return Token(TokenType.IDENTIFIER, buffer, self.line, start_col)
    
    def match_number(self):
        # Implementation for integer/float matching
        pass