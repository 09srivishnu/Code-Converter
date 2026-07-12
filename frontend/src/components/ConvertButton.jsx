import React from 'react'

function ConvertButton({ onClick, loading, sourceLanguage }) {
  const targetLanguage = sourceLanguage === 'c' ? 'Python' : 'C'

  return (
    <div className="convert-button-container">
      <button
        onClick={onClick}
        disabled={loading}
        className={`convert-btn ${loading ? 'loading' : ''}`}
      >
        {loading ? (
          <>
            <span className="spinner">⚡</span>
            Converting...
          </>
        ) : (
          <>
            ⚡ Convert to {targetLanguage}
          </>
        )}
      </button>
    </div>
  )
}

export default ConvertButton
