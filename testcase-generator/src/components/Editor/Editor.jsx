import React from 'react';
import './Editor.css';

// Add export default
export default function Editor({ code, onCodeChange, onCompile }) {
  return (
    <div className="editor-container">
      <h2>Code Editor</h2>
      <textarea
        value={code}
        onChange={(e) => onCodeChange(e.target.value)}
        placeholder={`Enter your test case specification...\nExample:\nint n(1, 100);\narray(n, int(10, 100)) values;`}
      />
      <button onClick={onCompile}>Compile & Generate</button>
    </div>
  );
}