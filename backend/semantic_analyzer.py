def analyse(ast):
    errors = []
    symbol_table = {}

    # Helper: Get declaration context for error reporting
    def get_context(decl):
        return {'line': decl['line'], 'column': decl['column']}

    # Constraint validators
    def validate_int_constraints(decl, params):
        check_numeric_value(decl, params.get('lower'), ['int', 'float'])
        check_numeric_value(decl, params.get('upper'), ['int', 'float'])

    def validate_float_constraints(decl, params):
        check_numeric_value(decl, params.get('lower'), ['int', 'float'])
        check_numeric_value(decl, params.get('upper'), ['int', 'float'])
        if 'precision' in params:
            check_integer_value(decl, params['precision'])

    def validate_char_constraints(decl, params):
        if 'charset' not in params:
            errors.append(f"Missing charset in char declaration at {decl['line']}:{decl['column']}")
            return
            
        charset = params['charset']
        valid = {'lower', 'upper', 'digit', 'special'}
        for part in charset.split('+'):
            if part not in valid:
                errors.append(f"Invalid charset '{part}' in char declaration at {decl['line']}:{decl['column']}")

    def validate_string_constraints(decl, params):
        if 'size' not in params:
            errors.append(f"Missing size in string declaration at {decl['line']}:{decl['column']}")
        else:
            check_numeric_value(decl, params['size'], ['int', 'float'])
        
        if 'charset' not in params:
            errors.append(f"Missing charset in string declaration at {decl['line']}:{decl['column']}")
        else:
            validate_char_constraints(decl, {'charset': params['charset']})

    # Value checking
    def check_numeric_value(decl, value_obj, allowed_types):
        if not value_obj:
            return
            
        if isinstance(value_obj['value'], (int, float)):
            return
            
        if isinstance(value_obj['value'], str):
            check_identifier(decl, value_obj['value'], allowed_types)
        else:
            errors.append(f"Invalid numeric value at {decl['line']}:{decl['column']}")

    def check_integer_value(decl, value_obj):
        if not value_obj:
            return
            
        if isinstance(value_obj['value'], int):
            return
            
        if isinstance(value_obj['value'], str):
            check_identifier(decl, value_obj['value'], ['int'])
        else:
            errors.append(f"Invalid integer value at {decl['line']}:{decl['column']}")

    def check_identifier(decl, identifier, allowed_types):
        # Handle negative identifiers
        original_name = identifier
        if identifier.startswith('-'):
            identifier = identifier[1:]
            
        if identifier not in symbol_table:
            errors.append(f"Undefined variable '{original_name}' referenced at {decl['line']}:{decl['column']}")
            return
            
        var_type = symbol_table[identifier]['data_type']
        if var_type not in allowed_types:
            allowed_str = " or ".join(allowed_types)
            errors.append(f"Type mismatch: '{original_name}' is {var_type} but expected {allowed_str} at {decl['line']}:{decl['column']}")

    # Build symbol table (first pass)
    for declaration in ast['ast']:
        name = declaration['name']
        
        if name in symbol_table:
            errors.append(f"Duplicate declaration of '{name}' at {declaration['line']}:{declaration['column']}")
        else:
            symbol_table[name] = {
                'data_type': declaration['data_type'],
                'line': declaration['line'],
                'column': declaration['column']
            }

    # Validate constraints (second pass)
    for declaration in ast['ast']:
        decl_type = declaration['data_type']
        params = declaration.get('params', {})
        
        try:
            if decl_type == 'int':
                validate_int_constraints(declaration, params)
            elif decl_type == 'float':
                validate_float_constraints(declaration, params)
            elif decl_type == 'char':
                validate_char_constraints(declaration, params)
            elif decl_type == 'string':
                validate_string_constraints(declaration, params)
        except KeyError as e:
            errors.append(f"Malformed {decl_type} declaration at {declaration['line']}:{declaration['column']}")

    return {'errors': errors}