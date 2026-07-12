import React from 'react'

function CodeEditor({ value, onChange, language }) {
  const handleCopy = () => {
    navigator.clipboard.writeText(value)
    alert('Code copied to clipboard!')
  }

  const handleDownload = () => {
    const element = document.createElement('a')
    const file = new Blob([value], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = `code.${language === 'c' ? 'c' : 'py'}`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="code-editor">
      <div className="editor-toolbar">
        <button 
          onClick={handleCopy}
          className="toolbar-btn"
          title="Copy code"
        >
          📋 Copy
        </button>
        <button 
          onClick={handleDownload}
          className="toolbar-btn"
          title="Download code"
        >
          ⬇️ Download
        </button>
      </div>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={`Enter ${language.toUpperCase()} code here...`}
        className="editor-textarea"
        spellCheck="false"
      />
      <div className="editor-info">
        {value.length} characters | {value.split('\n').length} lines
      </div>
    </div>
  )
}

export default CodeEditor
