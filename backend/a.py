from tokenization import tokenization
from parser import parse
from semantic_analyzer import analyse

with open("file.txt", "r") as file:
    code = file.read()

try:
    tokens = tokenization(code)
    for token in tokens:
        print(token)
    root = parse(tokens)
    ast = root['ast']
    for node in ast:
        print(node['params'])
    _errors = analyse(root)
    print('ERRORS FROM SEMANTIC ANALYSIS:', _errors['errors'])
    # errors = root['errors']
    # print(errors)
    # for node in root:
    #     print(node)
except SyntaxError as e:
    print(f"Error: {e}")