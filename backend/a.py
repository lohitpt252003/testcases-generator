from tokenization import tokenization

# print(tokenization("// "))

with open("file.txt", "r") as file:
    code = file.read()

try:
    tokens = tokenization(code)
    for token in tokens:
        print(token)
except SyntaxError as e:
    print(f"Error: {e}")