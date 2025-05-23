import sys

class LexicalError(Exception):
    pass

class Token:
    def __init__(self, value, type, line, column):
        self.value = value
        self.type = type
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token('{self.value}', '{self.type}', line={self.line}, column={self.column})"

def tokenize(code: str):
    tokens = []
    errors = {'LexicalError': []}

    pos = 0
    size = len(code)
    line = 1
    column = 1

    keywords = {'int', 'float', 'char', 'string', 'var', 'lout', 'lerr'}

    def cur_char():
        return code[pos] if pos < size else None

    def advance():
        nonlocal pos, line, column
        if pos < size:
            if code[pos] == '\n':
                line += 1
                column = 0
            pos += 1
            column += 1

    def skip_whitespaces():
        while pos < size and code[pos].isspace():
            advance()

    def skip_comment():
        nonlocal pos, line, column
        start_line, start_col = line, column
        # Line comment //
        if pos + 1 < size and code[pos] == '/' and code[pos + 1] == '/':
            advance(); advance()
            start = pos
            while pos < size and code[pos] != '\n':
                advance()
            comment_text = code[start:pos]
            tokens.append(Token(comment_text, 'COMMENT', start_line, start_col))
            return

        # Block comment /* ... */
        if pos + 1 < size and code[pos] == '/' and code[pos + 1] == '*':
            advance(); advance()
            start = pos
            while pos + 1 < size and not (code[pos] == '*' and code[pos + 1] == '/'):
                advance()
            if pos + 1 >= size:
                errors['LexicalError'].append(f"Unclosed block comment at {start_line}:{start_col}")
                return
            comment_text = code[start:pos]
            advance(); advance()  # skip '*/'
            tokens.append(Token(comment_text, 'COMMENT', start_line, start_col))
            return

    def read_identifier():
        start = pos
        while pos < size and (code[pos].isalnum() or code[pos] == '_'):
            advance()
        return code[start:pos]

    def read_number():
        nonlocal pos
        start = pos
        is_float = False
        has_digit = False

        # optional leading '-'
        if cur_char() == '-' and pos + 1 < size and (code[pos+1].isdigit() or code[pos+1] == '.'):
            advance()

        # leading dot float
        if cur_char() == '.' and pos + 1 < size and code[pos+1].isdigit():
            is_float = True
            advance()

        while pos < size and (code[pos].isdigit() or code[pos] == '.'):
            if code[pos] == '.':
                if is_float:
                    errors['LexicalError'].append(f"Invalid number format at {line}:{column}")
                else:
                    is_float = True
                advance()
            else:
                has_digit = True
                advance()

        num_str = code[start:pos]
        if not num_str or num_str == '.' or num_str == '-':
            errors['LexicalError'].append(f"Invalid number format at {line}:{column}")
            return None

        try:
            return float(num_str) if is_float else int(num_str)
        except ValueError:
            errors['LexicalError'].append(f"Invalid number format at {line}:{column}")
            return None

    def read_string():
        nonlocal pos
        quote = code[pos]
        start_line, start_col = line, column
        advance()  # skip opening quote
        start = pos
        content = ''
        while pos < size and code[pos] != quote:
            if code[pos] == '\n':
                errors['LexicalError'].append(f"Unclosed string at {start_line}:{start_col}")
                return None
            content += code[pos]
            advance()
        if pos >= size:
            errors['LexicalError'].append(f"Unclosed string at {start_line}:{start_col}")
            return None
        advance()  # skip closing quote
        return content

    while pos < size:
        current = cur_char()
        curr_line, curr_col = line, column

        if current.isspace():
            skip_whitespaces()
            continue

        # comments
        if current == '/' and pos + 1 < size and code[pos+1] in ('/', '*'):
            skip_comment()
            continue

        # identifier or keyword
        if current.isalpha() or current == '_':
            ident = read_identifier()
            typ = 'KEYWORD' if ident in keywords else 'IDENTIFIER'
            tokens.append(Token(ident, typ, curr_line, curr_col))
            continue

        # number
        if current.isdigit() or (current == '.' and pos + 1 < size and code[pos+1].isdigit()) or \
           (current == '-' and pos + 1 < size and (code[pos+1].isdigit() or code[pos+1]=='.')):
            num = read_number()
            if num is not None:
                typ = 'FLOAT' if isinstance(num, float) else 'INT'
                tokens.append(Token(num, typ, curr_line, curr_col))
            continue

        # string (only double quotes supported)
        if current == '"':
            s = read_string()
            if s is not None:
                tokens.append(Token(s, 'STRING', curr_line, curr_col))
            continue

        # operators
        if current in '+-*/<>=%!':
            op = current
            advance()
            # two-char ops
            if cur_char() is not None and (op + cur_char()) in ('==','!=','<=','>='):
                op += cur_char()
                advance()
            tokens.append(Token(op, 'OPERATOR', curr_line, curr_col))
            continue

        # punctuators
        if current in '(){},;:[]':
            punct_map = {
                '(': 'LPAREN', ')': 'RPAREN',
                '{': 'LBRACE', '}': 'RBRACE',
                '[': 'LBRACKET', ']': 'RBRACKET',
                ',': 'COMMA', ';': 'SEMICOLON',
                ':': 'COLON'
            }
            tok_type = punct_map[current]
            tokens.append(Token(current, tok_type, curr_line, curr_col))
            advance()
            continue

        # unknown character
        errors['LexicalError'].append(f"Unexpected character '{current}' at {curr_line}:{curr_col}")
        advance()

    return {
        'tokens': tokens,
        'errors': errors
    }