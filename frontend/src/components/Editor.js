import React, { useState, useRef } from "react";
import "./Editor.css";

function Editor() {
  const [code, setCode] = useState("// Code here");
  const [lines, setLines] = useState(["// Code here"]);
  const textareaRef = useRef(null);

  const bracketMap = {
    '(': ')',
    '{': '}', 
    '[': ']'
  };

  const tabSize = 4;

  const moveCursor = (index) => {
    setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.focus();
          textareaRef.current.setSelectionRange(index, index);
        }
      }, 0);
    };

  const handleCodeChange = (e) => {
    const text = e.target.value;
    const pos = e.target.selectionStart;
    const lastChar = text[pos - 1];
    
    let updatedText = text;
    
    // Check if the last entered character is an opening bracket
    if (lastChar in bracketMap) {
      // Insert closing bracket after the cursor position
      updatedText = 
        text.slice(0, pos) + 
        bracketMap[lastChar] + 
        text.slice(pos);
    }

    // Update state with new text
    setCode(updatedText);
    setLines(updatedText.split("\n"));

    // Move cursor back to original position if bracket was added
    if (lastChar in bracketMap) {
      moveCursor(pos);
    }
  };

  const indentFWD = (e) => {
    let text = e.target.value;
    const pos = e.target.selectionStart;
    text = text.slice(0, pos) + (' '.repeat(tabSize)) + text.slice(pos);    
    moveCursor(pos);
    setCode(text);
  };

  const indentBKWD = (e) => {
    let text = e.target.value;
    const pos = e.target.selectionStart;

    // Calculate the start of the possible indentation
    const start = Math.max(0, pos - tabSize);
    const possibleIndent = text.slice(start, pos);

    // Only unindent if it's actually spaces equal to tabSize
    if (possibleIndent === ' '.repeat(tabSize)) {
      text = text.slice(0, start) + text.slice(pos);
      moveCursor(start);  // move cursor to new position after removal
      setCode(text);
    } else {
      // No indentation to remove, do nothing or beep (optional)
    }
  };


  const handleKeyDown = (e) => {
    console.log(e.key);
    if (e.key.toLowerCase() === 'tab') {
      e.preventDefault();
      if (e.shiftKey) {
        indentBKWD(e);
      }
      else {
        indentFWD(e);
      }
    }
    
    else if (e.key.toLowerCase() === 'enter') {
      // e.preventDefault();
    }
  }

  return (
    <div className="Editor-container">
      <div className="Editor-lines">
        {lines.map((_, i) => (
          <div key={i}>{i + 1}</div>
        ))}
      </div>
      <textarea
        ref={textareaRef}
        className="Editor-textarea"
        value={code}
        onChange={handleCodeChange}
        rows={Math.max(lines.length, 1)}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
}

export default Editor;