'use client'

import { useState } from 'react'
import { FileText, User, Send, Download, CheckCircle, AlertCircle, Copy } from 'lucide-react'
import { api, CoverLetterResponse, CoverLetterBatchResponse, APIError } from '@/lib/api'
import { ExportButtons } from '@/components/ExportButtons'
import { PdfUpload } from '@/components/PdfUpload'
import { Toast } from '@/components/Toast'

export default function Home() {
  const [jobPosting, setJobPosting] = useState('')
  const [cvData, setCvData] = useState('')
  const [tone, setTone] = useState<'formal' | 'friendly' | 'concise'>('formal')
  const [variants, setVariants] = useState(1)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isExporting, setIsExporting] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadedFileName, setUploadedFileName] = useState<string>('')
  const [coverLetter, setCoverLetter] = useState<CoverLetterResponse | null>(null)
  const [coverLetterBatch, setCoverLetterBatch] = useState<CoverLetterBatchResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isSuccess, setIsSuccess] = useState(false)
  const [toast, setToast] = useState<{ type: 'success' | 'error'; message: string } | null>(null)

  const handlePdfUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    
    // Check file type
    if (file.type !== 'application/pdf') {
      setError('Lütfen sadece PDF dosyası yükleyin.')
      return
    }
    
    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('PDF dosyası çok büyük. Maksimum 10MB olmalı.')
      return
    }
    
    try {
      setError(null) // Clear previous errors
      setIsUploading(true)
      setUploadedFileName(file.name)
      
      const { text } = await api.extractCvTextFromPdf(file)
      
      if (text && text.trim().length > 0) {
        setCvData(text)
      } else {
        setError('PDF\'den metin çıkarılamadı. Dosya görsel tabanlı olabilir.')
        setUploadedFileName('')
      }
    } catch (err) {
      if (err instanceof APIError) {
        setError(`PDF Hatası: ${err.message}`)
      } else {
        console.error('PDF upload error:', err)
        setError('PDF okunamadı. Lütfen geçerli bir PDF yükleyin.')
      }
      setUploadedFileName('')
    } finally {
      setIsUploading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsGenerating(true)
    setError(null)
    setIsSuccess(false)
    setCoverLetter(null)
    setCoverLetterBatch(null)
    
    try {
      const response = await api.generateCoverLetter({
        job_posting: {
          job_posting_text: jobPosting
        },
        cv_data: {
          cv_text: cvData
        },
        tone: tone,
        variants: variants
      })
      
      // Check if response has 'letters' property (batch response) or 'cover_letter' (single response)
      if ('letters' in response) {
        setCoverLetterBatch(response as CoverLetterBatchResponse)
      } else {
        setCoverLetter(response as CoverLetterResponse)
      }
      setIsSuccess(true)
      setToast({ type: 'success', message: `Cover letter${variants > 1 ? 's' : ''} generated successfully!` })
    } catch (err) {
      if (err instanceof APIError) {
        setError(`API Error: ${err.message}`)
        setToast({ type: 'error', message: `API Error: ${err.message}` })
      } else {
        setError('An unexpected error occurred. Please try again.')
        setToast({ type: 'error', message: 'An unexpected error occurred. Please try again.' })
      }
    } finally {
      setIsGenerating(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    setToast({ type: 'success', message: 'Cover letter copied to clipboard!' })
  }

  const downloadFile = (blob: Blob, filename: string) => {
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  const handleExportPdf = async (letter: string, jobTitle: string, companyName: string) => {
    setIsExporting(true)
    try {
      const blob = await api.exportPdf(letter, jobTitle, companyName)
      downloadFile(blob, `cover_letter_${companyName.replace(/\s+/g, '_')}_${jobTitle.replace(/\s+/g, '_')}.pdf`)
      setToast({ type: 'success', message: 'PDF exported successfully!' })
    } catch (err) {
      setError('PDF export failed. Please try again.')
      setToast({ type: 'error', message: 'PDF export failed. Please try again.' })
    } finally {
      setIsExporting(false)
    }
  }

  const handleExportDocx = async (letter: string, jobTitle: string, companyName: string) => {
    setIsExporting(true)
    try {
      const blob = await api.exportDocx(letter, jobTitle, companyName)
      downloadFile(blob, `cover_letter_${companyName.replace(/\s+/g, '_')}_${jobTitle.replace(/\s+/g, '_')}.docx`)
      setToast({ type: 'success', message: 'DOCX exported successfully!' })
    } catch (err) {
      setError('DOCX export failed. Please try again.')
      setToast({ type: 'error', message: 'DOCX export failed. Please try again.' })
    } finally {
      setIsExporting(false)
    }
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
              <PdfUpload
                onFileSelect={handlePdfUpload}
                isUploading={isUploading}
                fileName={uploadedFileName}
                error={error}
              />
            </div>

            {/* Tone and Variants Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="tone" className="block text-sm font-medium text-gray-700 mb-2">
                  Writing Tone
                </label>
                <select
                  id="tone"
                  value={tone}
                  onChange={(e) => setTone(e.target.value as 'formal' | 'friendly' | 'concise')}
                  className="input-field"
                >
                  <option value="formal">Formal</option>
                  <option value="friendly">Friendly</option>
                  <option value="concise">Concise</option>
                </select>
              </div>

              <div>
                <label htmlFor="variants" className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Variants
                </label>
                <select
                  id="variants"
                  value={variants}
                  onChange={(e) => setVariants(Number(e.target.value))}
                  className="input-field"
                >
                  <option value={1}>1 Variant</option>
                  <option value={2}>2 Variants</option>
                  <option value={3}>3 Variants</option>
                  <option value={5}>5 Variants</option>
                </select>
              </div>
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
                    <span>Generate Cover Letter{variants > 1 ? 's' : ''}</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-6 card border-l-4 border-red-500 bg-red-50">
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Success Message */}
        {isSuccess && (
          <div className="mt-6 card border-l-4 border-green-500 bg-green-50">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              <p className="text-green-700">Cover letter{variants > 1 ? 's' : ''} generated successfully!</p>
            </div>
          </div>
        )}

        {/* Single Cover Letter Result */}
        {coverLetter && (
          <div className="mt-6 card">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Generated Cover Letter</h3>
            
            {/* Cover Letter Text */}
            <div className="bg-gray-50 p-4 rounded-lg mb-6">
              <div className="flex justify-between items-start mb-2">
                <span className="text-sm font-medium text-gray-700">Cover Letter</span>
                <button
                  onClick={() => copyToClipboard(coverLetter.cover_letter)}
                  className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                >
                  <Copy className="h-4 w-4 mr-1" />
                  Copy
                </button>
              </div>
              <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans">
                {coverLetter.cover_letter}
              </pre>
            </div>

            {/* Analysis Results */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Skill Matches */}
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Skill Analysis</h4>
                <div className="space-y-2">
                  {coverLetter.skill_matches.map((match, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <span className="text-sm">{match.skill}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        match.matched 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {match.matched ? '✓' : '✗'} {Math.round(match.confidence * 100)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Recommendations</h4>
                <ul className="space-y-2">
                  {coverLetter.recommendations.map((rec, index) => (
                    <li key={index} className="text-sm text-gray-700 flex items-start">
                      <span className="text-blue-500 mr-2">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Export Buttons */}
            <ExportButtons
              coverLetter={coverLetter.cover_letter}
              jobTitle={coverLetter.analysis.position_title || 'Position'}
              companyName={coverLetter.analysis.company_name || 'Company'}
              isExporting={isExporting}
              onExportPdf={() => handleExportPdf(
                coverLetter.cover_letter, 
                coverLetter.analysis.position_title || 'Position',
                coverLetter.analysis.company_name || 'Company'
              )}
              onExportDocx={() => handleExportDocx(
                coverLetter.cover_letter, 
                coverLetter.analysis.position_title || 'Position',
                coverLetter.analysis.company_name || 'Company'
              )}
            />
          </div>
        )}

        {/* Multiple Cover Letters Result */}
        {coverLetterBatch && (
          <div className="mt-6 card">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Generated Cover Letters ({coverLetterBatch.letters.length} variants)</h3>
            
            {/* Cover Letters */}
            <div className="space-y-6">
              {coverLetterBatch.letters.map((letter, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-sm font-medium text-gray-700">Variant {index + 1}</span>
                    <button
                      onClick={() => copyToClipboard(letter)}
                      className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                    >
                      <Copy className="h-4 w-4 mr-1" />
                      Copy
                    </button>
                  </div>
                  <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans">
                    {letter}
                  </pre>
                  {/* Export buttons for each variant */}
                  <div className="mt-4 flex gap-2">
                    <button 
                      onClick={() => handleExportPdf(
                        letter, 
                        coverLetterBatch.analysis.position_title || 'Position',
                        coverLetterBatch.analysis.company_name || 'Company'
                      )}
                      disabled={isExporting}
                      className="group flex items-center px-3 py-1.5 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white text-xs font-medium rounded-md transition-all duration-200 shadow-sm hover:shadow-md"
                    >
                      {isExporting ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1"></div>
                          <span>Exporting...</span>
                        </>
                      ) : (
                        <>
                          <FileText className="h-3 w-3 mr-1 group-hover:scale-110 transition-transform" />
                          <span>PDF</span>
                        </>
                      )}
                    </button>
                    <button 
                      onClick={() => handleExportDocx(
                        letter, 
                        coverLetterBatch.analysis.position_title || 'Position',
                        coverLetterBatch.analysis.company_name || 'Company'
                      )}
                      disabled={isExporting}
                      className="group flex items-center px-3 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white text-xs font-medium rounded-md transition-all duration-200 shadow-sm hover:shadow-md"
                    >
                      {isExporting ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1"></div>
                          <span>Exporting...</span>
                        </>
                      ) : (
                        <>
                          <Download className="h-3 w-3 mr-1 group-hover:scale-110 transition-transform" />
                          <span>DOCX</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Analysis Results */}
            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Skill Matches */}
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Skill Analysis</h4>
                <div className="space-y-2">
                  {coverLetterBatch.skill_matches.map((match, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <span className="text-sm">{match.skill}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        match.matched 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {match.matched ? '✓' : '✗'} {Math.round(match.confidence * 100)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Recommendations</h4>
                <ul className="space-y-2">
                  {coverLetterBatch.recommendations.map((rec, index) => (
                    <li key={index} className="text-sm text-gray-700 flex items-start">
                      <span className="text-blue-500 mr-2">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

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
      
      {/* Toast Notifications */}
      {toast && (
        <Toast
          type={toast.type}
          message={toast.message}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  )
}
