import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, FileText } from 'lucide-react'

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void
  maxFiles?: number
}

export const FileUpload: React.FC<FileUploadProps> = ({ 
  onFilesSelected, 
  maxFiles = 10 
}) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const pdfFiles = acceptedFiles.filter(
      file => file.type === 'application/pdf'
    )
    
    if (pdfFiles.length + selectedFiles.length > maxFiles) {
      alert(`Maximum ${maxFiles} files allowed`)
      return
    }

    setSelectedFiles(prev => [...prev, ...pdfFiles])
  }, [selectedFiles, maxFiles])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles,
    multiple: true
  })

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleAnalyze = () => {
    if (selectedFiles.length > 0) {
      onFilesSelected(selectedFiles)
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
        `}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p className="text-lg font-medium text-gray-700">
          {isDragActive
            ? 'Drop the PDF files here'
            : 'Drag & drop PDF bank statements here'}
        </p>
        <p className="text-sm text-gray-500 mt-2">
          or click to select files (max {maxFiles} files)
        </p>
      </div>

      {selectedFiles.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-medium mb-3">
            Selected Files ({selectedFiles.length})
          </h3>
          <div className="space-y-2">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-red-500" />
                  <div>
                    <p className="text-sm font-medium">{file.name}</p>
                    <p className="text-xs text-gray-500">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="p-1 hover:bg-gray-200 rounded"
                >
                  <X className="h-5 w-5 text-gray-500" />
                </button>
              </div>
            ))}
          </div>

          <button
            onClick={handleAnalyze}
            className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg
                     hover:bg-blue-700 transition-colors font-medium"
          >
            Analyze Statements
          </button>
        </div>
      )}
    </div>
  )
}
