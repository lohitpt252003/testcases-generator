# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# your modules
import tokenization
import parser
import semantic_analyzer
import ir as ir_module

app = Flask(__name__)
CORS(app)  # allow React frontend on localhost:3000

@app.route('/')
def  home():
    return 'Backend is working'

@app.route('/api/execute', methods=['POST'])
def execute():
    data = request.get_json(force=True)
    code = data.get('code', '')

    stdout = ''
    stderr = ''
    errors = []

    # 1) Tokenization
    try:
        tokens = tokenization.tokenize(code)
    except Exception as e:
        errors.append(f"Lexing error: {e}")
        return jsonify({'stdout':'', 'stderr':'', 'errors': errors})

    # 2) Parsing
    parse_result = parser.parse(tokens)
    if parse_result.get('errors'):
        errors.extend(parse_result['errors'])
        return jsonify({'stdout':'', 'stderr':'', 'errors': errors})

    ast = {'ast': parse_result['ast']}

    # 3) Semantic analysis
    sem = semantic_analyzer.analyze(ast)
    if sem.get('errors'):
        errors.extend(sem['errors'])
        return jsonify({'stdout':'', 'stderr':'', 'errors': errors})

    # 4) IR generation & execution
    try:
        ir_result = ir_module.ir(ast)
        # ir_result contains stdout, stderr, plus variables if you want
        stdout = ir_result.get('stdout', '')
        stderr = ir_result.get('stderr', '')
    except Exception as e:
        # catch any runtime in IR
        stderr = ''
        errors.append(f"Runtime error: {e}\n{traceback.format_exc()}")

    return jsonify({
        'stdout': stdout,
        'stderr': stderr,
        'errors': errors
    })


if __name__ == '__main__':
    # debug=True for development
    app.run(host='0.0.0.0', port=5000, debug=True)
