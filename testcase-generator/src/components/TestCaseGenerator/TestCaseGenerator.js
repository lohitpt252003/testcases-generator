import React from 'react';
import './TestCaseGenerator.css';

// Add export default
export default function TestCaseGenerator({ testCases, onRegenerate }) {
  const downloadTestCases = () => {
    const blob = new Blob([JSON.stringify(testCases, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'testcases.json';
    a.click();
  };

  return (
    <div className="testcase-generator">
      <h2>Generated Test Cases</h2>
      <div className="actions">
        <button onClick={onRegenerate}>Regenerate</button>
        <button onClick={downloadTestCases}>Download JSON</button>
      </div>
      <pre>{JSON.stringify(testCases, null, 2)}</pre>
    </div>
  );
}