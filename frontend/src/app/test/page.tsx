'use client'

import { useState } from 'react'
import { api } from '@/lib/api'

export default function TestPage() {
  const [status, setStatus] = useState<string>('')
  const [loading, setLoading] = useState(false)

  const testAPI = async () => {
    setLoading(true)
    try {
      const response = await api.testEndpoint()
      setStatus(`✅ API Test Successful: ${response.message}`)
    } catch (error) {
      setStatus(`❌ API Test Failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setLoading(false)
    }
  }

  const testHealth = async () => {
    setLoading(true)
    try {
      const response = await api.healthCheck()
      setStatus(`✅ Health Check: ${response.status} - ${response.service}`)
    } catch (error) {
      setStatus(`❌ Health Check Failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">API Test Page</h1>
        
        <div className="card">
          <div className="space-y-4">
            <button
              onClick={testAPI}
              disabled={loading}
              className="btn-primary"
            >
              {loading ? 'Testing...' : 'Test API Endpoint'}
            </button>
            
            <button
              onClick={testHealth}
              disabled={loading}
              className="btn-secondary"
            >
              {loading ? 'Testing...' : 'Test Health Check'}
            </button>
            
            {status && (
              <div className="mt-4 p-4 bg-gray-100 rounded-lg">
                <p className="text-sm font-mono">{status}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
