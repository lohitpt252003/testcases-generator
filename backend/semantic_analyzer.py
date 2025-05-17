def analyze(ast):
    # errors = []
    symbol_table = {}

    def check_limit(params):
        if not params:
            return
        lower = params.get('lower')
        upper = params.get('upper')
    
    for node in ast['ast']:
        if node['type'] == 'VariableDecl':
            name = node['name']
            data_type = node['data_type']
            params = node['params']
            if name in symbol_table:
                raise SyntaxError(f"Duplicate declaration\nVariable '{name}' already declared.")
            symbol_table[name] = data_type
            if data_type == 'int':
                check_limit(params)