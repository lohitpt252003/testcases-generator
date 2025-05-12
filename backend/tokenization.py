import sys

class Token:
    def __init__(self, value, type, line, column):
        self.value = value
        self.type = type
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f'Token(\'{self.value}\', \'{self.type}\', line = {self.line}, column = {self.column})'

def tokenization(code):
    tokens = []
    pos = 0
    size = len(code)
    line = 1
    column = 1
    keywords = {'int', 'float', 'char', 'string', 'var'}

    def cur_char():
        return code[pos] if pos < size else None
    
    def advance():
        nonlocal pos, line, column
        if pos >= size:
            return
        if code[pos] == '\n':
            line += 1
            column = 0
        else:
            column += 1
        pos += 1
    
    def skip_whitespaces():
        while pos < size and code[pos].isspace():
            advance()
    
    def skip_comment():
        start_line = line
        start_col = column
        comment = ''

        # Line comment
        if pos + 1 < size and code[pos] == '/' and code[pos + 1] == '/':
            advance()  # Skip first /
            advance()  # Skip second /
            start = pos
            while pos < size and code[pos] != '\n':
                advance()
            comment = code[start:pos]
        
        # Block comment
        elif pos + 1 < size and code[pos] == '/' and code[pos + 1] == '*':  # FIXED: Check next character
            advance()  # Skip /
            advance()  # Skip *
            start = pos
            while pos + 1 < size and not (code[pos] == '*' and code[pos + 1] == '/'):  # FIXED: Check for */
                advance()
            if pos + 1 >= size:
                raise SyntaxError(f"Unclosed block comment at {start_line}:{start_col}")
            comment = code[start:pos]
            advance()  # Skip *
            advance()  # Skip /
        
        tokens.append(Token(comment, 'COMMENT', start_line, start_col))
    
    def read_identifier():
        start = pos
        while pos < size and (code[pos].isalnum() or code[pos] == '_'):
            advance()
        return code[start:pos]
    
    def read_number():
        start = pos
        is_float = False
        has_digit = False
        negative = False

        # Check for leading '-' (if followed by a digit or .)
        if cur_char() == '-' and (pos + 1 < size) and (code[pos + 1].isdigit() or code[pos + 1] == '.'):
            advance()  # Consume the '-'
            negative = True
            start = pos  # Reset start after consuming '-'

        # Handle numbers like -.5
        if cur_char() == '.' and (pos + 1 < size) and code[pos + 1].isdigit():
            is_float = True
            advance()

        # Process digits and .
        while pos < size and (code[pos].isdigit() or code[pos] == '.'):
            if code[pos] == '.':
                if is_float:
                    break  # Multiple dots → invalid
                is_float = True
            else:
                has_digit = True
            advance()

        if not has_digit and not is_float:
            return None  # Not a valid number

        num_str = code[start:pos]
        if negative:
            num_str = '-' + num_str
        return num_str
    def read_string():
        quote_type = code[pos]  # ' or "
        start_line = line
        start_col = column
        advance()  # Skip opening quote
        
        start = pos  # FIXED: Track string start position correctly
        while pos < size and code[pos] != quote_type:
            if code[pos] == '\n':
                raise SyntaxError(f'Unclosed string at {start_line}:{start_col}')
            advance()
        
        if pos >= size:
            raise SyntaxError(f'Unclosed string at {start_line}:{start_col}')
        
        value = code[start:pos]
        advance()  # Skip closing quote
        return value
    
    while pos < size:
        current_char = cur_char()
        current_line = line
        current_col = column

        if current_char.isspace():
            skip_whitespaces()
            continue
        
        # Handle comments
        elif current_char == '/' and pos + 1 < size and code[pos + 1] in ['/', '*']:
            skip_comment()
            continue
        
        # Identifiers/keywords
        elif current_char.isalpha() or current_char == '_':
            current_token = read_identifier()
            token_type = 'KEYWORD' if current_token in keywords else 'IDENTIFIER'
            tokens.append(Token(current_token, token_type, current_line, current_col))
            continue
        
        # Numbers (including those starting with .)
        # In the main loop:
        elif (current_char == '-' and (pos + 1 < size) and (code[pos + 1].isdigit() or code[pos + 1] == '.')) \
                or current_char.isdigit() \
                or (current_char == '.' and (pos + 1 < size) and code[pos + 1].isdigit()):
            num_str = read_number()
            if num_str is None:
                raise SyntaxError(f"Invalid number format at {current_line}:{current_col}")
            
            is_float = '.' in num_str
            try:
                value = float(num_str) if is_float else int(num_str)
            except ValueError:
                raise SyntaxError(f"Invalid number format at {current_line}:{current_col}")
            
            tokens.append(Token(value, 'FLOAT' if is_float else 'INT', current_line, current_col))
            continue
        
        # Strings
        elif current_char in '\'"':
            current_token = read_string()
            tokens.append(Token(current_token, 'STRING', current_line, current_col))
            continue
        
        # Operators
        elif current_char in '+-*/<>=%!':
            op = current_char
            advance()
            
            # Handle multi-character operators
            if cur_char() is not None:
                possible_op = op + cur_char()
                if possible_op in ['==', '!=', '<=', '>=']:
                    op = possible_op
                    advance()
            
            tokens.append(Token(op, 'OPERATOR', current_line, current_col))
            continue
        
        # Punctuators
        elif current_char in '(){},;:[]':
            punct = current_char
            token_type = ''
            if current_char == '(':
                token_type = 'LPAREN'
            elif current_char == ')':
                token_type = 'RPAREN'
            elif current_char == ':':
                token_type = 'COLON'
            elif current_char == ';':
                token_type = 'SEMICOLON'
            elif current_char == ',':
                token_type = 'COMMA'
            elif current_char == '}':
                token_type = 'CURLY_RPAREN'
            elif current_char == '[':
                token_type = 'SQUARE_LPAREN'
            elif current_char == ']':
                token_type = 'SQUARE_RPAREN'
            tokens.append(Token(punct, token_type, current_line, current_col))
            advance()
            continue
        
        # Error handling
        else:
            raise SyntaxError(f'Unexpected character {current_char} at {current_line}:{current_col}')

    return tokens