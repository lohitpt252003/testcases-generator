export const configureLanguage = (monaco, variables) => {
  monaco.languages.register({ id: 'customLang' });

  // Syntax highlighting
  monaco.languages.setMonarchTokensProvider('customLang', {
    keywords: ['var', 'int', 'float', 'char', 'string', 'lout'],
    typeKeywords: ['lower', 'upper', 'digit', 'special'],
    operators: ['+', '-', ',', ':', ';', '(', ')'],
    tokenizer: {
      root: [
        [/[a-z_$][\w$]*/, {
          cases: {
            '@keywords': 'keyword',
            '@typeKeywords': 'type',
            '@default': 'identifier'
          }
        }],
        [/"([^"\\]|\\.)*$/, 'string.invalid'],
        [/"([^"\\]|\\.)*"/, 'string'],
        [/\d+\.\d+/, 'number.float'],
        [/\d+/, 'number'],
        [/[:,;()]/, 'delimiter'],
        [/[+\-]/, 'operator']
      ]
    }
  });

  // Autocomplete
  monaco.languages.registerCompletionItemProvider('customLang', {
    triggerCharacters: [':', '(', ',', '+'],
    provideCompletionItems: (model, position) => {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn
      };

      return {
        suggestions: [
          ...['var', 'lout'].map(label => ({
            label,
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: label,
            range
          })),
          ...['int', 'float', 'char', 'string'].map(label => ({
            label,
            kind: monaco.languages.CompletionItemKind.Type,
            insertText: label,
            range
          })),
          ...['lower', 'upper', 'digit', 'special'].map(label => ({
            label,
            kind: monaco.languages.CompletionItemKind.Enum,
            insertText: label,
            range
          })),
          ...variables.map(label => ({
            label,
            kind: monaco.languages.CompletionItemKind.Variable,
            insertText: label,
            range
          }))
        ]
      };
    }
  });

  // Editor theme
  monaco.editor.defineTheme('customTheme', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: '#569CD6' },
      { token: 'type', foreground: '#4EC9B0' },
      { token: 'string', foreground: '#CE9178' },
      { token: 'number', foreground: '#B5CEA8' },
      { token: 'delimiter', foreground: '#D4D4D4' },
      { token: 'operator', foreground: '#D4D4D4' }
    ],
    colors: {
      'editor.background': '#1E1E1E',
      'editor.lineHighlightBackground': '#2A2A2A'
    }
  });
};