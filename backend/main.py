from tokenization import tokenize
from parser import parse

code = None

try :
    with open('file.stcl') as f:
        code = f.read()
except Exception as e:
    print(f'error : ', e)

if code:
    # try:
        tokens = tokenize(code)
        # print(tokens)
        root = parse(tokens)

    # except Exception as e:
    #     print(f'error : ', e)
print(root)