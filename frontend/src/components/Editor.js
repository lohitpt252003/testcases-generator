import React, { useState } from "react";
import "./Editor.css";

function Editor() {
  const [code, setCode] = useState("// Code here");
  const [lines, setLines] = useState(["// Code here"]);

  const handleCodeChange = (e) => {
    const text = e.target.value;
    setCode(text);
    const newLines = text.split("\n");
    setLines(newLines);
    console.log(text);
    console.log(newLines);
  };

  return (
    <div className="Editor-container">
      <div className="Editor-lines">
        {lines.map((_, i) => (
          <div key={i}>{i + 1}</div>
        ))}
      </div>
      <textarea
        className="Editor-textarea"
        value={code}
        onChange={handleCodeChange}
        rows={lines.length + 1}
      />
    </div>
  );
}

export default Editor;
