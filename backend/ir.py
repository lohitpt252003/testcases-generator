from random_ import generate_char, generate_float, generate_integer, generate_string

def ir(ast):
    nodes = ast['ast']
    output_arr = []

    for node in nodes:
        if node['type'] == 'VariableDecl':
            name = node['name']
            params = node.get('params', {})
            data_type = node['data_type']
            value = None

            if data_type == 'int':
                # Handle integer constraints
                if 'lower' in params and 'upper' in params:
                    value = generate_integer(
                        lower=params['lower']['value'],
                        upper=params['upper']['value']
                    )
                else:
                    value = generate_integer()

            elif data_type == 'float':
                # Handle float constraints and precision
                precision = params.get('precision', {}).get('value', 6) if 'precision' in params else 6
                lower = params.get('lower', {}).get('value', 0)
                upper = params.get('upper', {}).get('value', 1e18)
                value = generate_float(lower, upper, precision)

            elif data_type == 'char':
                # Handle character set constraints
                charset = params.get('charset', 'lower+upper+digit+special').split('+')
                value = generate_char(charset)

            elif data_type == 'string':
                # Handle string length and character set
                size = params.get('size', {}).get('value', 10)
                charset = params.get('charset', 'lower+upper+digit+special').split('+')
                value = generate_string(size, charset)

            output_arr.append({
                'name': name,
                'type': data_type,
                'value': value,
                'constraints': params
            })

    return output_arr