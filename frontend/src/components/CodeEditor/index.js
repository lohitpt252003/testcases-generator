import { useState, useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { configureLanguage } from './language-config';
import './styles.css';

const CodeEditor = () => {
  const [code, setCode] = useState(`var username: string(20, lower+upper);
var age: int(0, 120);
var price: float(0.0, 100.0, 2);

lout("Welcome:", username);`);
  const [errors, setErrors] = useState([]);
  const [variables, setVariables] = useState([]);
  const [stdout, setStdout] = useState([]);
  const [stderr, setStderr] = useState([]);
  const editorRef = useRef(null);
  const monacoRef = useRef(null);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    configureLanguage(monaco, variables);
  };

  const handleEditorChange = (value) => {
    setCode(value);
    parseCode(value);
  };

  const parseCode = (value) => {
    // Mock parsing - replace with actual parser implementation
    const mockVariables = value.match(/var\s+(\w+):/g) || [];
    const newVars = mockVariables.map(v => v.replace(/var\s+(\w+):.*/, '$1'));
    setVariables(newVars);
    
    // Mock errors - replace with actual validation
    const mockErrors = [];
    if (value.includes('undefined')) mockErrors.push('Undefined variable at line 1');
    setErrors(mockErrors);
  };

  const handleRunCode = async () => {
    try {
      // Mock API call
      const response = await fetch('http://localhost:5000/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const result = await response.json();
      setStdout(result.stdout);
      setStderr(result.stderr);
      setErrors(result.errors);
      console.log('Execution result:', result);
    } catch (error) {
      console.error('Execution error:', error);
    }
  };

  return (
    <div className="code-editor-container">
      <div className="toolbar">
        <button onClick={handleRunCode} className="run-button">
          Run Code
        </button>
      </div>

      <Editor
        height="70vh"
        defaultLanguage="customLang"
        theme="customTheme"
        value={code}
        onChange={handleEditorChange}
        onMount={handleEditorDidMount}
        options={{
          minimap: { enabled: false },
          automaticLayout: true,
          fontSize: 14,
          scrollBeyondLastLine: false,
          roundedSelection: false,
        }}
      />

      <div className="error-panel">
        <div>
          <h1>STDOUT</h1>
          <div>
            {stdout}
          </div>
        </div>
        <div>
          <h1>STDERR</h1>
          <div>
            {stderr}
          </div>
        </div>
        <div>
          <h1>Errors</h1>
          <div>
            {errors.map((error, index) => (
              <div key={index} className="error-message">
                ⚠️ {error}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeEditor;