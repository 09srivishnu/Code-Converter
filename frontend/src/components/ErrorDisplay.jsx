import React, { useState } from 'react'

function ErrorDisplay({ errors, type = 'error', title = 'Error' }) {
  const [visible, setVisible] = useState(true)

  if (!visible || errors.length === 0) return null

  const className = `error-display ${type}`
  const icon = type === 'error' ? '❌' : '⚠️'

  return (
    <div className={className}>
      <div className="error-header">
        <div className="error-title">
          <span>{icon}</span>
          <h3>{title}</h3>
        </div>
        <button
          onClick={() => setVisible(false)}
          className="close-btn"
        >
          ✕
        </button>
      </div>
      <div className="error-list">
        {errors.map((error, index) => (
          <div key={index} className="error-item">
            {error}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ErrorDisplay
