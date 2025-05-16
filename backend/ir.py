from random_ import generate_char, generate_float, generate_integer, generate_string

def ir(ast):
    nodes = ast['ast']
    output_arr = []

    for node in nodes:
        if node['type'] == 'VariableDecl':
            name = node['name']
            params = node['params']
            data_type = node['data_type']
            if data_type == 'int':
                if not params:
                    value = generate_integer()
                else:
                    value = generate_integer(params['lower'], params['upper'])
            elif data_type == 'float':
                if not params:
                    value = generate_float()
                else:
                    value = generate_float(params['lower'], params['upper'])
            elif data_type == 'char':
                value = generate_char()
            elif data_type == 'string':
                value = generate_string()

        output_arr.push_back({
            'name' : name,
            'value' : value
            })
        
        return output_arr