from tokenization import tokenize
from parser import parse
from semantic_analyzer import analyze
from ir import ir

code = None

try :
    with open('file.stcl') as f:
        code = f.read()
except Exception as e:
    print(f'error : ', e)

if code:
    tokens = tokenize(code)
    parser = parse(tokens)
    if (parser['errors']) :
        print(f"Errors at parsing stage:")
        for error in parser['errors']:
            print(error)
        exit(0)
    