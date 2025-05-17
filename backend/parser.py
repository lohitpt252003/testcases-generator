def parse(tokens):
    tokens = [token for token in tokens if token.type != 'COMMENT']
    ast = []
    index = 0

    def current_token():
        return tokens[index] if index < len(tokens) else None
    
    def advance():
        nonlocal index
        if index < len(tokens):
            index += 1
    
    def expect_token(token_type, values=None, error_message=None):
        token = current_token()
        if not token:
            raise_syntax_error(error_message or 'Unexpected end of input', token)
        if token.type != token_type or (values and token.value not in values):
            raise_syntax_error(error_message or f"Expected {token_type}{f' with value {values}' if values else ''}", token)
        
        advance()
        return token
    
    def raise_syntax_error(error_message, token=None):
        line = token.line if token else 0
        column = token.column if token else 0
        raise SyntaxError(f'{error_message} at {line}:{column}')
    
    def parse_variable_declaration():
        expect_token('KEYWORD', ['var'], 'Expected "var" keyword')
        name_token = expect_token('IDENTIFIER', error_message='Expected Identifier')

        var_name = name_token.value
        
        expect_token('COLON', error_message='Expected \':\' after identifier')
        type_token = expect_token('KEYWORD', ['int', 'float', 'char', 'string'], 'Invalid type of data type')


        params = {}
        if current_token() and current_token().value == '(':
            advance()
            params = parse_params(type_token.value)
            expect_token('RPAREN', error_message='Expected closing \')\'')
        
        expect_token('SEMICOLON', error_message='Expected \';\' at end of declaration')
        
        return {
            'type': 'VariableDecl',
            'name': name_token.value,
            'data_type': type_token.value,
            'params': params,
            'line': name_token.line,
            'column': name_token.column
        }
    
    def parse_params(data_type):
        params = {}
        if data_type == 'int':
            params = parse_int_params()
        elif data_type == 'float':
            params = parse_float_params()
        elif data_type == 'char':
            params = parse_char_params()
        elif data_type == 'string':
            params = parse_string_params()
        return params
    
    def parse_int_params():
        lower = parse_limit()
        expect_token('COMMA', error_message='Expected \',\' in int parameters')
        upper = parse_limit()
        return {'lower': lower, 'upper': upper}
    
    def parse_float_params():
        lower = parse_limit()
        expect_token('COMMA', error_message='Expected \',\' in float parameters')
        upper = parse_limit()
        precision = None

        if current_token() and current_token().value == ',':
            advance()
            precision = parse_precision()
        
        return {'lower': lower, 'upper': upper, 'precision': precision}
    
    def parse_char_params():
        return {'charset': parse_charset_expr()}
    
    def parse_string_params():
        size = parse_size()
        expect_token('COMMA', error_message='Expected \',\' after string size')
        charset = parse_charset_expr()
        return {'size': size, 'charset': charset}
    
    def parse_limit():
        # limit can be int, float or a (int, float) identifier
        # +ve or -ve
        token = current_token()
        op = False
        if token and token.type == 'OPERATOR' and token.value in '+-':
            operator = token.value
            advance()
            token = current_token()
            op = True
        if token and token.type in ['INT', 'FLOAT']:
            _value = token.value
            advance()
            if op:
                value = {
                    'OPERATOR' : operator,
                    'value' : {
                        'type' : f'{token.type.lower()}',
                        'value' : _value
                    }
                }
            else:
                value = _value
        elif token.type == 'IDENTIFIER':
            _value = token.value
            advance()
            if op:
                value = {
                    'OPERATOR' : operator,
                    'value' : {
                        'type' : 'IDENTIFIER',
                        'value' : _value
                    }
                }
            else:
                value = _value
        else:
            raise_syntax_error('Expected numeric value or identifier', token)
        
        return {'type': 'number', 'value': value}
    
    def parse_precision():
        token = current_token()
        if token and token.type == 'INT' and token.value <= 6:
            value = token.value
            advance()
            return {'type': 'integer', 'value': value}
        raise_syntax_error('Expected positive integer and the precision must be a constatnt and it should less than or equal to 6', token)
    
    def parse_size():
        token = current_token()
        op = False
        if token and token.type == 'OPERATOR' and token.value in '+-':
            operator = token.value
            advance()
            token = current_token()
            op = True
        if token and token.type == 'INT':
            _value = token.value
            advance()
            if op:
                value = {
                    'OPERATOR' : operator,
                    'value' : {
                        'type' : f'{token.type.lower()}',
                        'value' : _value
                    }
                }
            else:
                value = _value
        elif token.type == 'IDENTIFIER':
            _value = token.value
            advance()
            if op:
                value = {
                    'OPERATOR' : operator,
                    'value' : {
                        'type' : 'IDENTIFIER',
                        'value' : _value
                    }
                }
            else:
                value = _value
        else:
            raise_syntax_error(token = token, error_message = 'Expected a integer or a integer identifier')
        return {'type': 'number', 'value': value}
    
    def parse_charset_expr():
        parts = []
        while True:
            token = expect_token('IDENTIFIER', ['lower', 'upper', 'digit', 'special'], 
                               'Invalid charset identifier')
            parts.append(token.value)

            if current_token() and current_token().value == '+':
                advance()
            else:
                break
        return '+'.join(parts)
    
    try:
        while index < len(tokens):
            ast.append(parse_variable_declaration())
        return {'ast': ast, 'errors': []}
    except SyntaxError as e:
        return {'ast': ast, 'errors': [str(e)]}