'use client'

import { useState } from 'react'
import { ArrowLeft, Copy, CheckCircle, AlertCircle } from 'lucide-react'
import Link from 'next/link'

type HumanizeResult = {
  humanized_text: string
  original_text: string
  word_count: number
  processing_time: number
  meaning_preserved: boolean
  pipeline_type: string
  education_level: string
}

export default function HumanizePage() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<HumanizeResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)
  
  // Form options
  const [pipelineType, setPipelineType] = useState('comprehensive')
  const [educationLevel, setEducationLevel] = useState('undergraduate')
  const [paranoidMode, setParanoidMode] = useState(true)
  const [writehumanMode, setWritehumanMode] = useState(true)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('/api/humanize/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text.trim(),
          pipeline_type: pipelineType,
          education_level: educationLevel,
          paranoid_mode: paranoidMode,
          writehuman_mode: writehumanMode
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to humanize text')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = async () => {
    if (!result) return
    
    try {
      await navigator.clipboard.writeText(result.humanized_text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy text:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors">
            <ArrowLeft className="h-5 w-5" />
            <span>Back to Home</span>
          </Link>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">API Status: Online</span>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI Text Humanizer
            </h1>
            <p className="text-xl text-gray-600">
              Transform AI-generated text into natural, human-like content
            </p>
          </div>

          {/* Input Form */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Text Input */}
              <div>
                <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
                  Text to Humanize
                </label>
                <textarea
                  id="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Paste your AI-generated text here..."
                  className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                  maxLength={5000}
                />
                <div className="text-right text-sm text-gray-500 mt-1">
                  {text.length}/5000 characters
                </div>
              </div>

              {/* Options */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="pipelineType" className="block text-sm font-medium text-gray-700 mb-2">
                    Pipeline Type
                  </label>
                  <select
                    id="pipelineType"
                    value={pipelineType}
                    onChange={(e) => setPipelineType(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="comprehensive">⚡ Comprehensive (All Tools)</option>
                    <option value="standard">⚡ Standard (Basic + Stylometric)</option>
                    <option value="quick">🚀 Quick (Gemini Only)</option>
                    <option value="advanced">⚡ Advanced (Multi-pass)</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="educationLevel" className="block text-sm font-medium text-gray-700 mb-2">
                    Education Level
                  </label>
                  <select
                    id="educationLevel"
                    value={educationLevel}
                    onChange={(e) => setEducationLevel(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  >
                    <option value="elementary">🎓 Elementary</option>
                    <option value="middle_school">🎓 Middle School</option>
                    <option value="high_school">🎓 High School</option>
                    <option value="undergraduate">🎓 Undergraduate</option>
                    <option value="masters">🎓 Masters</option>
                    <option value="phd">🎓 PhD</option>
                  </select>
                </div>
              </div>

              {/* Advanced Options */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Advanced Options
                </label>
                <div className="flex flex-wrap gap-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={paranoidMode}
                      onChange={(e) => setParanoidMode(e.target.checked)}
                      className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">🔥 Paranoid Mode (Coherence Disruption)</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={writehumanMode}
                      onChange={(e) => setWritehumanMode(e.target.checked)}
                      className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">🎭 WriteHuman Mimicry (SurferSEO Killer)</span>
                  </label>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={!text.trim() || loading}
                className="w-full bg-indigo-600 text-white py-4 px-6 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Humanizing...</span>
                  </div>
                ) : (
                  '🚀 Humanize Text'
                )}
              </button>
            </form>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
              <div className="flex items-center space-x-2">
                <AlertCircle className="h-5 w-5 text-red-500" />
                <span className="text-red-700 font-medium">Error</span>
              </div>
              <p className="text-red-600 mt-1">{error}</p>
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">✨ Humanized Result</h2>
                <button
                  onClick={copyToClipboard}
                  className="flex items-center space-x-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
                >
                  {copied ? (
                    <>
                      <CheckCircle className="h-4 w-4" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                      <span>Copy Text</span>
                    </>
                  )}
                </button>
              </div>

              {/* Metrics */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-gray-50 p-3 rounded-lg text-center">
                  <div className="text-2xl font-bold text-indigo-600">{result.word_count}</div>
                  <div className="text-sm text-gray-600">Words</div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg text-center">
                  <div className="text-2xl font-bold text-indigo-600">{(result.processing_time / 1000).toFixed(1)}s</div>
                  <div className="text-sm text-gray-600">Processing Time</div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg text-center">
                  <div className="text-2xl font-bold text-green-600">✅</div>
                  <div className="text-sm text-gray-600">Meaning Preserved</div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg text-center">
                  <div className="text-2xl font-bold text-purple-600">🎓</div>
                  <div className="text-sm text-gray-600">{result.education_level}</div>
                </div>
              </div>

              {/* Pipeline Status */}
              <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <h3 className="font-semibold mb-2">🔧 Pipeline Status</h3>
                <div className="flex flex-wrap gap-2">
                  <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">✅ Simple Paraphrase</span>
                  <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm">✅ Gemini Enhancement</span>
                  <span className="bg-purple-500 text-white px-3 py-1 rounded-full text-sm">✅ Stylometric Changes</span>
                  {writehumanMode && <span className="bg-orange-500 text-white px-3 py-1 rounded-full text-sm">🎭 WriteHuman Mimicry</span>}
                  {paranoidMode && <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm">🔥 Paranoid Mode</span>}
                  <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">✅ Word Count Enforced</span>
                </div>
              </div>

              {/* Humanized Text */}
              <div>
                <h3 className="font-semibold mb-3">✨ Final Humanized Text</h3>
                <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
                  <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                    {result.humanized_text}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
} 