import React from 'react'

function OutputViewer({ value, language }) {
  const handleCopy = () => {
    navigator.clipboard.writeText(value)
    alert('Code copied to clipboard!')
  }

  const handleDownload = () => {
    const element = document.createElement('a')
    const file = new Blob([value], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = `output.${language === 'c' ? 'c' : 'py'}`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="output-viewer">
      <div className="viewer-toolbar">
        <button 
          onClick={handleCopy}
          className="toolbar-btn"
          disabled={!value}
          title="Copy code"
        >
          📋 Copy
        </button>
        <button 
          onClick={handleDownload}
          className="toolbar-btn"
          disabled={!value}
          title="Download code"
        >
          ⬇️ Download
        </button>
      </div>
      <textarea
        value={value}
        readOnly
        placeholder="Converted code will appear here..."
        className="viewer-textarea"
      />
      <div className="viewer-info">
        {value.length} characters | {value.split('\n').length} lines
      </div>
    </div>
  )
}

export default OutputViewer
