import { useState } from 'react'
import './App.css'
import { FileUpload } from './components/FileUpload'
import { AnalysisResults } from './components/AnalysisResults'

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState<any>(null)

  const handleFilesSelected = async (files: File[]) => {
    setIsAnalyzing(true)
    
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      // Use relative URL - ALB will route /api/* to backend
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Analysis failed')
      }

      const result = await response.json()
      console.log('Analysis result:', result)
      setResults(result)
    } catch (error) {
      console.error('Error:', error)
      alert('Error analyzing files')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleReset = () => {
    setResults(null)
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Bank Statement Analyzer
          </h1>
          <p className="text-gray-600 mt-2">
            Upload your bank statements to analyze debits, credits, and transactions
          </p>
        </div>
      </header>

      <main className="py-10">
        {results ? (
          <AnalysisResults results={results} onReset={handleReset} />
        ) : isAnalyzing ? (
          <div className="max-w-4xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow-md p-8">
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="ml-3 text-lg font-medium">
                  Analyzing statements...
                </span>
              </div>
            </div>
          </div>
        ) : (
          <FileUpload onFilesSelected={handleFilesSelected} />
        )}
      </main>
    </div>
  )
}

export default App
