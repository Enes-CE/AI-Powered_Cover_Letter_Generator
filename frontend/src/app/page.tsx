'use client'

import { useState } from 'react'
import { FileText, User, Send, Download } from 'lucide-react'

export default function Home() {
  const [jobPosting, setJobPosting] = useState('')
  const [cvData, setCvData] = useState('')
  const [tone, setTone] = useState('formal')
  const [isGenerating, setIsGenerating] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsGenerating(true)
    
    // TODO: Implement API call
    console.log('Generating cover letter...', { jobPosting, cvData, tone })
    
    // Simulate API call
    setTimeout(() => {
      setIsGenerating(false)
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-primary-600" />
              <h1 className="ml-2 text-2xl font-bold text-gray-900">
                AI Cover Letter Generator
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Generate Personalized Cover Letters with AI
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload a job posting and your CV, and let our AI create a tailored cover letter that matches your experience with the job requirements.
          </p>
        </div>

        {/* Form */}
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Job Posting Input */}
            <div>
              <label htmlFor="jobPosting" className="block text-sm font-medium text-gray-700 mb-2">
                Job Posting
              </label>
              <textarea
                id="jobPosting"
                value={jobPosting}
                onChange={(e) => setJobPosting(e.target.value)}
                placeholder="Paste the job posting text here..."
                className="input-field h-32 resize-none"
                required
              />
            </div>

            {/* CV Input */}
            <div>
              <label htmlFor="cvData" className="block text-sm font-medium text-gray-700 mb-2">
                Your CV/Resume
              </label>
              <textarea
                id="cvData"
                value={cvData}
                onChange={(e) => setCvData(e.target.value)}
                placeholder="Paste your CV text or upload a file..."
                className="input-field h-32 resize-none"
                required
              />
            </div>

            {/* Tone Selection */}
            <div>
              <label htmlFor="tone" className="block text-sm font-medium text-gray-700 mb-2">
                Writing Tone
              </label>
              <select
                id="tone"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="input-field"
              >
                <option value="formal">Formal</option>
                <option value="friendly">Friendly</option>
                <option value="concise">Concise</option>
              </select>
            </div>

            {/* Submit Button */}
            <div className="flex justify-center">
              <button
                type="submit"
                disabled={isGenerating}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    <span>Generate Cover Letter</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Features */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-3 w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <FileText className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Analysis</h3>
            <p className="text-gray-600">AI extracts key skills and requirements from job postings</p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-3 w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <User className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Personalized Matching</h3>
            <p className="text-gray-600">Matches your experience with job requirements</p>
          </div>
          
          <div className="text-center">
            <div className="bg-primary-100 rounded-full p-3 w-12 h-12 mx-auto mb-4 flex items-center justify-center">
              <Download className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Easy Export</h3>
            <p className="text-gray-600">Download as PDF, DOCX, or copy to clipboard</p>
          </div>
        </div>
      </main>
    </div>
  )
}
