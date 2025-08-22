'use client'

import { useState } from 'react'
import { FileText, User, Send, Download, CheckCircle, AlertCircle, Copy, Sparkles, Zap, Target, Award } from 'lucide-react'
import { api, CoverLetterResponse, CoverLetterBatchResponse, APIError } from '@/lib/api'
import { ExportButtons } from '@/components/ExportButtons'
import { PdfUpload } from '@/components/PdfUpload'
import { Toast } from '@/components/Toast'

export default function Home() {
  const [jobPosting, setJobPosting] = useState('')
  const [cvData, setCvData] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [positionTitle, setPositionTitle] = useState('')
  const [yearsOfExperience, setYearsOfExperience] = useState('')
  const [keyAchievements, setKeyAchievements] = useState('')
  const [aiProvider, setAiProvider] = useState<'template' | 'ollama'>('template')
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
        company_name: companyName,
        position_title: positionTitle,
        years_of_experience: yearsOfExperience,
        key_achievements: keyAchievements,
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
      setToast({ type: 'success', message: 'Cover letter başarıyla oluşturuldu!' })
    } catch (err) {
      console.error('Generation error:', err)
      if (err instanceof APIError) {
        setError(`Hata: ${err.message}`)
      } else {
        setError('Cover letter oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.')
      }
      setToast({ type: 'error', message: 'Cover letter oluşturulamadı!' })
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadFile = async (blob: Blob, filename: string) => {
    try {
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    } catch (error) {
      console.error('Download error:', error)
      setError('Dosya indirilemedi.')
    }
  }

  const handleExportPdf = async () => {
    if (!coverLetter && !coverLetterBatch) return
    
    setIsExporting(true)
    try {
      const content = coverLetter?.cover_letter || coverLetterBatch?.letters?.[0] || ''
      const company = companyName || 'Company'
      const position = positionTitle || 'Position'
      
      const response = await api.exportPdf(content, position, company)
      
      downloadFile(response, `cover-letter-${company}-${position}.pdf`)
      setToast({ type: 'success', message: 'PDF başarıyla indirildi!' })
    } catch (error) {
      console.error('PDF export error:', error)
      setError('PDF export edilemedi.')
      setToast({ type: 'error', message: 'PDF export edilemedi!' })
    } finally {
      setIsExporting(false)
    }
  }

  const handleExportDocx = async () => {
    if (!coverLetter && !coverLetterBatch) return
    
    setIsExporting(true)
    try {
      const content = coverLetter?.cover_letter || coverLetterBatch?.letters?.[0] || ''
      const company = companyName || 'Company'
      const position = positionTitle || 'Position'
      
      const response = await api.exportDocx(content, position, company)
      
      downloadFile(response, `cover-letter-${company}-${position}.docx`)
      setToast({ type: 'success', message: 'DOCX başarıyla indirildi!' })
    } catch (error) {
      console.error('DOCX export error:', error)
      setError('DOCX export edilemedi.')
      setToast({ type: 'error', message: 'DOCX export edilemedi!' })
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-cyan-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                  AI Cover Letter Generator
                </h1>
                <p className="text-blue-200 text-sm">Powered by Advanced AI</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 bg-white/10 backdrop-blur-md rounded-full border border-white/20 mb-6">
            <Zap className="h-4 w-4 text-cyan-400 mr-2" />
            <span className="text-white text-sm font-medium">AI-Powered Cover Letter Generation</span>
          </div>
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Create Perfect
            <span className="block bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Cover Letters
            </span>
          </h2>
          <p className="text-xl text-blue-200 max-w-3xl mx-auto leading-relaxed">
            Upload your job posting and CV, and let our advanced AI create personalized, 
            professional cover letters that match your experience with job requirements.
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-8 mb-12 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Job Posting Section */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-white mb-3">
                📋 Job Posting
              </label>
              <textarea
                value={jobPosting}
                onChange={(e) => setJobPosting(e.target.value)}
                                  placeholder="Paste the job posting text here..."
                  className="w-full h-32 p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-blue-300 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                required
              />
            </div>

            {/* Company & Position Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <label className="block text-lg font-semibold text-white">
                  🏢 Company Name *
                </label>
                <input
                  type="text"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="e.g., Google, Microsoft, Apple"
                  className="w-full p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                  required
                />
              </div>
              <div className="space-y-3">
                <label className="block text-lg font-semibold text-white">
                  💼 Position Title *
                </label>
                <input
                  type="text"
                  value={positionTitle}
                  onChange={(e) => setPositionTitle(e.target.value)}
                  placeholder="e.g., Senior Software Engineer"
                  className="w-full p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                  required
                />
              </div>
            </div>

            {/* Experience & Achievements Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <label className="block text-lg font-semibold text-white">
                  ⏰ Years of Experience
                </label>
                <input
                  type="text"
                  value={yearsOfExperience}
                  onChange={(e) => setYearsOfExperience(e.target.value)}
                  placeholder="e.g., 5 years, 2-3 years"
                  className="w-full p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                />
              </div>
              <div className="space-y-3">
                <label className="block text-lg font-semibold text-white">
                  🏆 Key Achievements
                </label>
                <textarea
                  value={keyAchievements}
                  onChange={(e) => setKeyAchievements(e.target.value)}
                  placeholder="e.g., Led a team of 5 developers, Improved performance by 40%"
                  className="w-full h-20 p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-blue-300 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            {/* CV Section */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-white mb-3">
                📄 Your CV/Resume
              </label>
              <textarea
                value={cvData}
                onChange={(e) => setCvData(e.target.value)}
                                  placeholder="Paste your CV text or upload a file..."
                  className="w-full h-32 p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-blue-300 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                required
              />
              
              {/* PDF Upload */}
              <div className="mt-4">
                <div className="relative">
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={handlePdfUpload}
                    className="hidden"
                    id="pdf-upload"
                  />
                  <label
                    htmlFor="pdf-upload"
                    className="group relative flex flex-col items-center justify-center w-full h-24 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-300 border-blue-300/50 bg-white/5 hover:border-blue-400 hover:bg-white/10 backdrop-blur-md"
                  >
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                              <FileText className="h-8 w-8 text-blue-300 group-hover:text-blue-200 mb-2 transition-colors" />
                        <p className="text-sm text-blue-200 group-hover:text-white font-medium transition-colors">
                          Upload CV as PDF
                        </p>
                        <p className="text-xs text-blue-300 group-hover:text-blue-200 transition-colors">
                        or drag and drop
                      </p>
                    </div>
                  </label>
                </div>
                {uploadedFileName && (
                  <div className="mt-2 flex items-center text-green-400">
                    <CheckCircle className="h-4 w-4 mr-2" />
                    <span className="text-sm">{uploadedFileName}</span>
                  </div>
                )}
                <p className="text-xs text-blue-300 mt-2">
                  PDF yükleyin; metin otomatik doldurulur. Maksimum 10MB.
                </p>
              </div>
            </div>

            {/* Tone & Variants Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <label className="block text-lg font-semibold text-white">
                  🎭 Writing Tone
                </label>
                                  <select
                    value={tone}
                    onChange={(e) => setTone(e.target.value as 'formal' | 'friendly' | 'concise')}
                    className="w-full p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                >
                  <option value="formal" className="bg-gray-800">Formal</option>
                  <option value="friendly" className="bg-gray-800">Friendly</option>
                  <option value="concise" className="bg-gray-800">Concise</option>
                </select>
              </div>
              <div className="space-y-3">
                <label className="block text-lg font-semibold text-white">
                  🔄 Number of Variants
                </label>
                                  <select
                    value={variants}
                    onChange={(e) => setVariants(Number(e.target.value))}
                    className="w-full p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
                >
                  <option value={1} className="bg-gray-800">1 Variant</option>
                  <option value={2} className="bg-gray-800">2 Variants</option>
                  <option value={3} className="bg-gray-800">3 Variants</option>
                  <option value={5} className="bg-gray-800">5 Variants</option>
                </select>
              </div>
            </div>

            {/* Generate Button */}
            <div className="flex justify-center pt-6">
              <button
                type="submit"
                disabled={isGenerating}
                className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <div className="flex items-center space-x-3">
                  {isGenerating ? (
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  ) : (
                    <Sparkles className="h-5 w-5 group-hover:rotate-12 transition-transform" />
                  )}
                  <span>{isGenerating ? 'Generating...' : 'Generate Cover Letter'}</span>
                </div>
              </button>
            </div>
          </form>
        </div>

        {/* Results Section */}
        {error && (
          <div className="bg-red-500/20 backdrop-blur-md border border-red-500/30 rounded-xl p-6 mb-8">
            <div className="flex items-center space-x-3">
              <AlertCircle className="h-6 w-6 text-red-400" />
              <p className="text-red-200">{error}</p>
            </div>
          </div>
        )}

        {/* Single Cover Letter Result */}
        {coverLetter && (
          <div className="bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-8 mb-8 shadow-2xl">
            <div className="flex items-center justify-between mb-6">
                             <h3 className="text-2xl font-bold text-white flex items-center">
                 <Target className="h-6 w-6 mr-3 text-blue-400" />
                 Generated Cover Letter
               </h3>
              <ExportButtons
                onExportPdf={handleExportPdf}
                onExportDocx={handleExportDocx}
                isExporting={isExporting}
              />
            </div>
            
            <div className="bg-white/5 backdrop-blur-md rounded-xl p-6 border border-white/10">
              <pre className="text-white whitespace-pre-wrap font-sans leading-relaxed">
                {coverLetter.cover_letter}
              </pre>
            </div>

            {/* Analysis */}
            {coverLetter.analysis && (
              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                  <h4 className="text-lg font-semibold text-white mb-3">📊 Analysis</h4>
                                     <div className="space-y-2 text-sm text-blue-200">
                    <p><strong>Company:</strong> {coverLetter.analysis.company_name}</p>
                    <p><strong>Position:</strong> {coverLetter.analysis.position_title}</p>
                    <p><strong>Experience:</strong> {coverLetter.analysis.required_experience}</p>
                  </div>
                </div>
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                  <h4 className="text-lg font-semibold text-white mb-3">🎯 Skill Matches</h4>
                  <div className="space-y-2">
                    {coverLetter.skill_matches?.map((match, index) => (
                      <div key={index} className="flex items-center justify-between">
                                                 <span className="text-blue-200">{match.skill}</span>
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          match.matched 
                            ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
                            : 'bg-red-500/20 text-red-300 border border-red-500/30'
                        }`}>
                          {match.matched ? '✓' : '✗'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Multiple Cover Letters Result */}
        {coverLetterBatch && (
          <div className="space-y-8">
            {/* Analysis Dashboard for Batch */}
            <div className="bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-8 shadow-2xl">
              <h3 className="text-2xl font-bold text-white flex items-center mb-6">
                <BarChart3 className="h-6 w-6 mr-3 text-blue-400" />
                Analysis Dashboard
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                  <h4 className="text-lg font-semibold text-white mb-3">📊 Job Analysis</h4>
                  <div className="space-y-2 text-blue-200">
                    <p><strong>Company:</strong> {coverLetterBatch.analysis.company_name}</p>
                    <p><strong>Position:</strong> {coverLetterBatch.analysis.position_title}</p>
                    <p><strong>Experience:</strong> {coverLetterBatch.analysis.required_experience}</p>
                  </div>
                </div>
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                  <h4 className="text-lg font-semibold text-white mb-3">🎯 Skill Matches</h4>
                  <div className="space-y-2">
                    {coverLetterBatch.skill_matches?.map((match, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <span className="text-blue-200">{match.skill}</span>
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          match.matched 
                            ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
                            : 'bg-red-500/20 text-red-300 border border-red-500/30'
                        }`}>
                          {match.matched ? '✓' : '✗'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Cover Letter Variants */}
            {coverLetterBatch.letters.map((letter, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-8 shadow-2xl">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-2xl font-bold text-white flex items-center">
                    <Award className="h-6 w-6 mr-3 text-blue-400" />
                    Variant {index + 1} - {coverLetterBatch.tone_used?.[index] || 'Formal'}
                  </h3>
                  <ExportButtons
                    onExportPdf={handleExportPdf}
                    onExportDocx={handleExportDocx}
                    isExporting={isExporting}
                  />
                </div>
                
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-6 border border-white/10">
                  <pre className="text-white whitespace-pre-wrap font-sans leading-relaxed">
                    {letter}
                  </pre>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Features Section */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
                     <div className="text-center group">
             <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl p-6 w-16 h-16 mx-auto mb-6 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
               <Target className="h-8 w-8 text-white" />
             </div>
             <h3 className="text-xl font-bold text-white mb-4">Smart Analysis</h3>
             <p className="text-blue-200 leading-relaxed">
              AI extracts key skills and requirements from job postings with advanced NLP
            </p>
          </div>
          
                     <div className="text-center group">
             <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl p-6 w-16 h-16 mx-auto mb-6 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
               <User className="h-8 w-8 text-white" />
             </div>
             <h3 className="text-xl font-bold text-white mb-4">Personalized Matching</h3>
             <p className="text-blue-200 leading-relaxed">
              Matches your experience with job requirements for perfect alignment
            </p>
          </div>
          
                     <div className="text-center group">
             <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl p-6 w-16 h-16 mx-auto mb-6 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
               <Download className="h-8 w-8 text-white" />
             </div>
             <h3 className="text-xl font-bold text-white mb-4">Easy Export</h3>
             <p className="text-blue-200 leading-relaxed">
              Download as PDF, DOCX, or copy to clipboard with one click
            </p>
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
