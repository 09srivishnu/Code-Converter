import React, { useState } from 'react'
import CodeEditor from './components/CodeEditor'
import LanguageSelector from './components/LanguageSelector'
import ConvertButton from './components/ConvertButton'
import OutputViewer from './components/OutputViewer'
import ErrorDisplay from './components/ErrorDisplay'
import useConverter from './hooks/useConverter'
import './App.css'

function App() {
  const [input, setInput] = useState('')
  const [sourceLanguage, setSourceLanguage] = useState('c')
  const { output, errors, warnings, loading, convert } = useConverter()

  const targetLanguage = sourceLanguage === 'c' ? 'python' : 'c'

  const handleConvert = async () => {
    if (!input.trim()) {
      alert('Please enter code to convert')
      return
    }
    await convert(input, sourceLanguage, targetLanguage)
  }

  const handleLanguageToggle = () => {
    setSourceLanguage(sourceLanguage === 'c' ? 'python' : 'c')
    setInput('')
  }

  return (
    <div className="app">
      <header className="header">
        <h1>C ↔ Python Code Converter</h1>
        <p>Seamlessly convert between C and Python syntax</p>
      </header>

      <main className="container">
        <div className="converter-section">
          <div className="editor-panel">
            <div className="panel-header">
              <h2>{sourceLanguage.toUpperCase()} Code</h2>
              <LanguageSelector 
                sourceLanguage={sourceLanguage}
                onToggle={handleLanguageToggle}
              />
            </div>
            <CodeEditor
              value={input}
              onChange={setInput}
              language={sourceLanguage}
            />
          </div>

          <div className="converter-control">
            <ConvertButton 
              onClick={handleConvert}
              loading={loading}
              sourceLanguage={sourceLanguage}
            />
          </div>

          <div className="output-panel">
            <div className="panel-header">
              <h2>{targetLanguage.toUpperCase()} Code</h2>
            </div>
            <OutputViewer
              value={output}
              language={targetLanguage}
            />
          </div>
        </div>

        <div className="messages-section">
          {errors.length > 0 && (
            <ErrorDisplay
              errors={errors}
              type="error"
              title="Errors"
            />
          )}
          {warnings.length > 0 && (
            <ErrorDisplay
              errors={warnings}
              type="warning"
              title="Warnings"
            />
          )}
        </div>
      </main>

      <footer className="footer">
        <p>© 2024 Code Converter | Built with React + Flask</p>
      </footer>
    </div>
  )
}

export default App
