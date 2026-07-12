import React from 'react'

function LanguageSelector({ sourceLanguage, onToggle }) {
  return (
    <div className="language-selector">
      <button 
        onClick={onToggle}
        className="toggle-btn"
        title="Toggle conversion direction"
      >
        🔄 Toggle
      </button>
    </div>
  )
}

export default LanguageSelector
