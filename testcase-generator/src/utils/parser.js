export const parseCode = (code) => {
    const variables = {};
    const errors = [];
    const ast = [];
  
    const lines = code.split('\n').map(line => line.trim()).filter(Boolean);
  
    lines.forEach((line, lineNumber) => {
      try {
        // Variable declarations
        if (/^(int|float|char)\s/.test(line)) {
          const match = line.match(/^(int|float|char)\s+([a-zA-Z_]\w*)\s*(?:\((.*?)\))?;?$/);
          if (!match) throw new Error('Invalid declaration syntax');
          
          const [_, type, name, params] = match;
          const constraints = params ? params.split(',').map(p => p.trim()) : [];
          
          variables[name] = { type, constraints, line: lineNumber + 1 };
          ast.push({ type: 'variable', dataType: type, name, constraints });
        }
        // Array declarations
        else if (/^array\(/.test(line)) {
          const match = line.match(/^array\(\s*([^,]+)\s*,\s*(.*?)\s*\)\s+([a-zA-Z_]\w*)\s*;?$/);
          if (!match) throw new Error('Invalid array syntax');
          
          const [_, size, dataType, name] = match;
          ast.push({ type: 'array', name, size, dataType });
        }
        else {
          throw new Error('Unknown statement');
        }
      } catch (err) {
        errors.push({
          line: lineNumber + 1,
          message: err.message,
          original: line
        });
      }
    });
  
    return { ast, variables, errors };
  };