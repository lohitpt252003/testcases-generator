export const generateTestCases = (ast) => {
    const testCases = {};
    const generatedValues = {};
  
    const getRandomInRange = (min, max, precision = 0) => {
      const value = Math.random() * (max - min) + min;
      return Number(value.toFixed(precision));
    };
  
    const generateChar = (constraints) => {
      const chars = [];
      constraints.forEach(constraint => {
        if (constraint === 'lower') chars.push(...'abcdefghijklmnopqrstuvwxyz');
        if (constraint === 'upper') chars.push(...'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
        if (constraint === 'digit') chars.push(...'0123456789');
        if (constraint === 'special') chars.push(...'!@#$%^&*()_+-=[]{}|;:,.<>?');
      });
      return chars[Math.floor(Math.random() * chars.length)] || 'A';
    };
  
    ast.forEach(node => {
      if (node.type === 'variable') {
        let value;
        switch(node.dataType) {
          case 'int':
            const [min = 0, max = 2**64] = node.constraints.map(Number);
            value = Math.floor(Math.random() * (max - min + 1)) + min;
            break;
            
          case 'float':
            const [fmin = 0, fmax = 2**64, prec = 2] = node.constraints.map(Number);
            value = getRandomInRange(fmin, fmax, prec);
            break;
            
          case 'char':
            value = generateChar(node.constraints);
            break;
        }
        generatedValues[node.name] = value;
        testCases[node.name] = value;
      }
      
      if (node.type === 'array') {
        const size = parseInt(node.size) || generatedValues[node.size];
        const arrayValues = [];
        
        for (let i = 0; i < size; i++) {
          // Parse array data type
          const match = node.dataType.match(/(int|float|char)(?:\((.*?)\))?/);
          const [_, type, params] = match;
          const constraints = params ? params.split(',').map(p => p.trim()) : [];
          
          // Generate array elements
          switch(type) {
            case 'int':
              const [min = 0, max = 2**64] = constraints.map(Number);
              arrayValues.push(Math.floor(Math.random() * (max - min + 1)) + min);
              break;
              
            case 'float':
              const [fmin = 0, fmax = 2**64, prec = 2] = constraints.map(Number);
              arrayValues.push(getRandomInRange(fmin, fmax, prec));
              break;
              
            case 'char':
              arrayValues.push(generateChar(constraints));
              break;
          }
        }
        
        testCases[node.name] = arrayValues;
      }
    });
  
    return testCases;
  };