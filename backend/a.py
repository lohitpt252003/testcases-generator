from tokenization import tokenize
from parser import parse
from semantic_analyzer import analyze
from ir import ir

with open("file.stcl", "r") as file:
    code = file.read()

try:
    tokens = tokenize(code)
    for token in tokens:
        print(token)
    root = parse(tokens)
    # print(f'ast:\n{root["ast"]}\nerrors:\n{root["errors"]}')
    # print(root)
    i = 1
    for node in root['ast']:
        print(i)
        print(node)
        # print(node['data_type'])
        # print(node['params'])
        i += 1
    print('Errors:', root['errors'])

    _n = analyze(root)
    # # print('Symbol Table:', _n['symbol_table'])
    print('Errors:', _n['errors'])
    # ast = root['ast']
    # for node in ast:
    #     print(node)
    # # _errors = analyse(root)

    # print('ERRORS FROM SEMANTIC ANALYSIS:', _errors['errors'])
    
    # if not _n['errors']:
        # IR = ir(root)
        # print(IR)
    #     for i in IR:
    #         print(i['name'], i['value'], i['constraints'])
    IR = ir(root)
    print(IR)
    print(IR['stdout'])
    # else:
    #     print('Fuck u Nigga\nThere are still some errors in the code, check below\nErrors:', _n['errors'])

except SyntaxError as e:
    print(f"Error: {e}")