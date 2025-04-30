import React from 'react';
import './CompilerOutput.css';

// Add export default
export default function CompilerOutput({ errors, ast }) {
  return (
    <div className="compiler-output">
      <h2>Compilation Results</h2>
      {errors.length > 0 && (
        <div className="errors">
          {errors.map((error, index) => (
            <div key={index} className="error">
              Line {error.line}: {error.message}
            </div>
          ))}
        </div>
      )}
      {ast && (
        <div className="ast-output">
          <h3>Abstract Syntax Tree</h3>
          <pre>{JSON.stringify(ast, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}