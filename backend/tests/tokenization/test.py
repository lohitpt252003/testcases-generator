import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tokenization import tokenization

# Get all files in the current directory ending with .stcl
files = [file for file in os.listdir() if file.endswith('.stcl')]

# Read contents of each .stcl file
codes = []
for file in files:
    with open(file, encoding='utf-8') as f:
        code = f.read()
    codes.append(code)

# Function to run a specific test
def run_test(i):
    print(f'\n\n=== Running Test {i + 1} ===')
    print('\n=== Original Code ===')
    print(codes[i])
    print('=== End of Code ===\n')
    try:
        tokens = tokenization(codes[i])
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(f"Error: {e}")
    print(f'=== Done with Test {i + 1} ===\n\n')


for i in range(len(files)):
    run_test(i)