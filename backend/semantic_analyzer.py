def analyze(ast):
    errors = []
    symbol_table = {}

    def get_identifier_name(value_obj):
        """Extract identifier name from an object"""
        return value_obj.get('value').get('value')

    def is_identifier(value_obj):
        """Check if the value object is an identifier"""
        return isinstance(value_obj, dict) and value_obj.get('value', {}).get('type') == 'IDENTIFIER'

    def check_defined_identifier(obj):
        """Verify identifier is defined in symbol table"""
        if is_identifier(obj):
            ident = get_identifier_name(obj)
            if ident not in symbol_table:
                errors.append(f"Undefined variable '{ident}'")

    def check_number(obj):
        """Check if an object is a valid number or defined identifier"""
        if isinstance(obj, (int, float)):
            return
        if isinstance(obj, str):
            if obj not in symbol_table:
                errors.append(f"Undefined variable '{obj}'")
            return
        if isinstance(obj, dict):
            check_defined_identifier(obj)

    def check_integer(obj):
        """Check if an object is a valid integer or defined identifier of int type"""
        if isinstance(obj, int):
            return
        if isinstance(obj, str):
            if obj not in symbol_table:
                errors.append(f"Undefined variable '{obj}'")
            return
        if isinstance(obj, dict):
            if is_identifier(obj):
                ident = get_identifier_name(obj)
                if ident not in symbol_table:
                    errors.append(f"Undefined variable '{ident}'")
                elif symbol_table[ident] != 'int':
                    errors.append(f"Type mismatch: expected 'int', found '{symbol_table[ident]}'")

    def check_int_limits(params):
        if not params:
            return
        lower = params.get('lower', {}).get('value')
        upper = params.get('upper', {}).get('value')
        check_number(lower)
        check_number(upper)
        if (isinstance(lower, int) and isinstance(upper, int) and lower > upper):
            errors.append(f"Invalid integer limits: {lower} > {upper}")

    def check_float_limits(params):
        if not params:
            return
        lower = params.get('lower', {}).get('value')
        upper = params.get('upper', {}).get('value')
        check_number(lower)
        check_number(upper)
        precision = params.get('precision')
        if precision is not None:
            if not isinstance(precision, int):
                errors.append("Precision must be an integer")
            elif precision < 0 or precision > 6:
                errors.append("Precision must be between 0 and 6")

    def check_char_limits(params):
        # No semantic checks for char sets at the moment
        pass

    def check_string_limits(params):
        size = params.get('size', {}).get('value')
        if isinstance(size, dict) and 'OPERATOR' in size:
            operator = size['OPERATOR']
            value = size['value']['value']
            if operator == '-' and isinstance(value, int):
                errors.append(f"Invalid string size: {-value}")
        check_integer(size)

    for node in ast['ast']:
        if node['type'] == 'VariableDecl':
            name = node['name']
            data_type = node['data_type']
            params = node.get('params', {})
            if name in symbol_table:
                raise SyntaxError(f"Duplicate declaration\nVariable '{name}' already declared.")
            if data_type == 'int':
                check_int_limits(params)
            elif data_type == 'float':
                check_float_limits(params)
            elif data_type == 'char':
                check_char_limits(params)
            elif data_type == 'string':
                check_string_limits(params)

            symbol_table[name] = data_type

    return {
        'errors': errors,
        'symbol_table': symbol_table
    }
