from tokenization import tokenization
from parser import parse

with open("file.txt", "r") as file:
    code = file.read()

try:
    tokens = tokenization(code)
    # print(tokens)
    for token in tokens:
        print(token)
    root = parse(tokens)
    ast = root['ast']
    for node in ast:
        print(node)
    errors = root['errors']
    print(errors)
    # for node in root:
    #     print(node)
except SyntaxError as e:
    print(f"Error: {e}")