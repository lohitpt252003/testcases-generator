from random_ import generate_char, generate_float, generate_integer, generate_string

def ir(ast):
    nodes = ast['ast']
    variable_map = {}
    variable_values = []
    stdout = ''
    stderr = ''

    def eval_bound(bound):
        """
        bound is one of:
          - int or float
          - str (an identifier)
          - dict with {'OPERATOR': '+/-', 'value': nested_value}
        Returns a numeric Python value by looking up identifiers in variable_map.
        """
        # literal
        if isinstance(bound, (int, float)):
            return bound

        # identifier name
        if isinstance(bound, str):
            return variable_map[bound]

        # unary +/- wrapper
        if isinstance(bound, dict) and 'OPERATOR' in bound:
            op = bound['OPERATOR']
            inner = bound['value']
            # inner is {'type':..., 'value':...}
            val = inner['value']
            v = eval_bound(val)
            return +v if op == '+' else -v

        raise ValueError(f"Cannot evaluate bound: {bound}")

    for node in nodes:
        if node['type'] == 'VariableDecl':

            name      = node['name']
            dtype     = node['data_type']
            params    = node.get('params', {})

            if dtype == 'int':
                # get bounds
                if not params:
                    val = generate_integer()
                    constraints = {}
                else:
                    low_obj  = params['lower']['value']
                    high_obj = params['upper']['value']
                    low  = eval_bound(low_obj)
                    high = eval_bound(high_obj)
                    val = generate_integer(low, high)
                    constraints = {'lower': low_obj, 'upper': high_obj}

            elif dtype == 'float':
                if not params:
                    val = generate_float()
                    constraints = {}
                else:
                    low_obj  = params['lower']['value']
                    high_obj = params['upper']['value']
                    prec_obj = params.get('precision')
                    low  = eval_bound(low_obj)
                    high = eval_bound(high_obj)
                    prec = prec_obj if isinstance(prec_obj, int) else \
                        (prec_obj.get('value') if isinstance(prec_obj, dict) else 6)
                    val = generate_float(low, high, prec)
                    if prec == 0:
                        val = int(val)
                    constraints = {
                        'lower': low_obj,
                        'upper': high_obj,
                        'precision': prec
                    }

            elif dtype == 'char':
                # params.get('charset') is something like "lower+digit+special"
                charset_spec = params.get('charset', '')
                charset = charset_spec.split('+') if charset_spec else ['upper','lower','digit','special']
                val = generate_char(charset)
                constraints = {'charset': charset_spec}

            elif dtype == 'string':
                size_obj = params['size']['value']
                size = eval_bound(size_obj)
                charset_spec = params.get('charset', '')
                charset = charset_spec.split('+') if charset_spec else ['upper','lower','digit','special']
                val = generate_string(size, charset)
                constraints = {
                    'size': size_obj,
                    'charset': charset_spec
                }

            else:
                # unknown type – skip
                continue
            
            # record
            variable_map[name] = val
            variable_values.append({
                'name': name,
                'value': val,
                'constraints': constraints
            })

        elif node['type'] == 'PrintStmt':
            args = node.get('args')
            for arg in args:
                if arg['type'] == 'IDENTIFIER':
                    ident = arg['value']
                    if ident in variable_map:
                        stdout += f"{variable_map[ident]}"
                    # else:
                    #     stderr += f"Undefined variable '{ident}'\n"
                elif arg['type'] == 'STRING':
                    stdout += f"{arg['value']}"
                else:
                    stderr += f"Unknown argument type: {arg['type']}\n"

    return {
        'stdout': stdout,
        'stderr': stderr,
        'variables': variable_map,
        'variable_values': variable_values
    }
    # return variable_values
