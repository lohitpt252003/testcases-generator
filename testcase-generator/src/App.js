import { useState } from 'react';
import { parseCode } from './utils/parser';
import { generateTestCases } from './utils/generator';
import Editor from './components/Editor/Editor';
import CompilerOutput from './components/CompilerOutput/CompilerOutput';
import TestCaseGenerator from './components/TestCaseGenerator/TestCaseGenerator';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [ast, setAst] = useState(null);
  const [testCases, setTestCases] = useState(null);
  const [errors, setErrors] = useState([]);

  const handleCompile = () => {
    const { ast, variables, errors } = parseCode(code);
    setErrors(errors);
    
    if (errors.length === 0) {
      setAst(ast);
      const generated = generateTestCases(ast);
      setTestCases(generated);
    } else {
      setAst(null);
      setTestCases(null);
    }
  };

  return (
    <div className="app-container">
      <h1>Test Case Generator</h1>
      <div className="main-content">
        <Editor 
          code={code}
          onCodeChange={setCode}
          onCompile={handleCompile}
        />
        
        <CompilerOutput 
          errors={errors}
          ast={ast}
        />
        
        {testCases && (
          <TestCaseGenerator 
            testCases={testCases}
            onRegenerate={handleCompile}
          />
        )}
      </div>
    </div>
  );
}

export default App;