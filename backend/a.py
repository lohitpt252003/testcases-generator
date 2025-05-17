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
    print(f'ast:\n{root["ast"]}\nerrors:\n{root["errors"]}')
    analyze(root)
    # ast = root['ast']
    # for node in ast:
    #     print(node)
    # # _errors = analyse(root)

    # print('ERRORS FROM SEMANTIC ANALYSIS:', _errors['errors'])
    
    # IR = ir(root)
    # print(IR)
    # for i in IR:
    #     print(i['name'], i['value'], i['constraints'])

except SyntaxError as e:
    print(f"Error: {e}")