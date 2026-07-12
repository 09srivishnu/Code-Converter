import { useState } from 'react'

function useConverter() {
  const [output, setOutput] = useState('')
  const [errors, setErrors] = useState([])
  const [warnings, setWarnings] = useState([])
  const [loading, setLoading] = useState(false)

  const convert = async (code, sourceLanguage, targetLanguage) => {
    setLoading(true)
    setErrors([])
    setWarnings([])
    setOutput('')

    try {
      const response = await fetch('http://localhost:5000/api/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          source: sourceLanguage,
          target: targetLanguage,
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      if (data.success) {
        setOutput(data.output)
        setWarnings(data.warnings || [])
      } else {
        setErrors(data.errors || ['Conversion failed'])
      }
    } catch (error) {
      setErrors([`Error: ${error.message}`])
    } finally {
      setLoading(false)
    }
  }

  return {
    output,
    errors,
    warnings,
    loading,
    convert,
  }
}

export default useConverter
