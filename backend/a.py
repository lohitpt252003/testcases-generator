from tokenization import tokenization
from parser import parse

with open("file.txt", "r") as file:
    code = file.read()

try:
    tokens = tokenization(code)
    print(tokens)
    for token in tokens:
        print(token)
    root = parse(tokens)
    print(root)
except SyntaxError as e:
    print(f"Error: {e}")