import CodeEditor from './components/CodeEditor';

function App() {
  return (
    <div className="App">
      <h1 style={{ 
        textAlign: 'center', 
        color: '#fff', 
        margin: '20px 0',
        fontFamily: 'monospace'
      }}>
        Custom Language Editor
      </h1>
      <CodeEditor />
    </div>
  );
}

export default App;