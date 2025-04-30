import re

def isValidVariableName(str):
    regex = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(regex, str))

print(isValidVariableName("Lohit"))