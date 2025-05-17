from random_ import generate_char, generate_float, generate_integer, generate_string

def ir(ast):
    nodes = ast['ast']
    variable_map = {}
    output_arr = []

    for node in nodes:
        if node['type'] == 'VariableDecl':
            name = node['name']
            params = node['params']
            data_type = node['data_type']
            # name, type, value, constraints
            
            if data_type == 'int':
                if not params:
                    value = generate_integer()
                    constraints = {}
                else:
                    lower = params['lower']['value']
                    upper = params['upper']['value']
                    if isinstance(lower, int):
                        _lower = lower
                    else:
                        if lower.startswith('-'):
                            _lower = -variable_map[lower[1 : ]]
                        else:
                            _lower = variable_map[lower]
                    
                    if isinstance(upper, int):
                        _upper = upper
                    else:
                        if upper.startswith('-'):
                            _upper = -variable_map[upper[1 : ]]
                        else:
                            _upper = variable_map[upper]
                    value = generate_integer(_lower, _upper)
                    constraints = {
                        'lower' : lower,
                        'upper' : upper
                    }
                variable_map[name] = value
                output_arr.append(
                    {
                        'name' : name,
                        'value' : value,
                        'constraints' : constraints
                    }
                )
    
            elif data_type == 'float':
                if not params:
                    value = generate_integer()
                    constraints = {}
                else:
                    lower = params['lower']['value']
                    upper = params['upper']['value']
                    precision = params.get('precision')
                    if not precision:
                        precision = 6
                    else:
                        precision = params.get('precision').get('value')
                    if isinstance(lower, (int, float)):
                        _lower = lower
                    else:
                        if lower.startswith('-'):
                            _lower = -variable_map[lower[1 : ]]
                        else:
                            _lower = variable_map[lower]
                    
                    if isinstance(upper, (int, float)):
                        _upper = upper
                    else:
                        if upper.startswith('-'):
                            _upper = -variable_map[upper[1 : ]]
                        else:
                            _upper = variable_map[upper]
                    value = generate_float(_lower, _upper, precision)
                    constraints = {
                        'lower' : lower,
                        'upper' : upper,
                        'precision' : precision
                    }
                variable_map[name] = value
                output_arr.append(
                    {
                        'name' : name,
                        'value' : value,
                        'constraints' : constraints
                    }
                )
    
    return output_arr