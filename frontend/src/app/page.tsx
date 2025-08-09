import Link from 'next/link'
import { ArrowRight, Sparkles, Shield, Zap } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-8 w-8 text-indigo-600" />
            <span className="text-2xl font-bold text-gray-900">ReHumanizer</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link 
              href="/login" 
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              Sign In
            </Link>
            <Link 
              href="/register" 
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Transform AI Text into
            <span className="text-indigo-600"> Human Content</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Bypass AI detection with our advanced humanization technology. 
            Make your AI-generated content sound natural and authentic.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/humanize" 
              className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center justify-center space-x-2"
            >
              <span>Try for Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <button className="border border-gray-300 text-gray-700 px-8 py-4 rounded-lg text-lg font-semibold hover:border-gray-400 transition-colors">
              Watch Demo
            </button>
          </div>
        </div>

        {/* Features */}
        <div className="mt-24 grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white rounded-xl shadow-sm">
            <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Zap className="h-6 w-6 text-indigo-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Lightning Fast</h3>
            <p className="text-gray-600">
              Humanize your text in seconds with our optimized algorithms
            </p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-sm">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Shield className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Detection Proof</h3>
            <p className="text-gray-600">
              Bypass major AI detectors while maintaining content quality
            </p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-sm">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Sparkles className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Smart Processing</h3>
            <p className="text-gray-600">
              Advanced NLP algorithms ensure natural, human-like output
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-24 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-12">
            Trusted by Content Creators Worldwide
          </h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="text-3xl font-bold text-indigo-600 mb-2">50K+</div>
              <div className="text-gray-600">Texts Humanized</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-indigo-600 mb-2">95%</div>
              <div className="text-gray-600">Success Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-indigo-600 mb-2">10K+</div>
              <div className="text-gray-600">Happy Users</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-indigo-600 mb-2">24/7</div>
              <div className="text-gray-600">Support Available</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-24 bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Sparkles className="h-6 w-6 text-indigo-400" />
                <span className="text-xl font-bold">ReHumanizer</span>
              </div>
              <p className="text-gray-400">
                Transform AI-generated text into human-like content with our advanced technology.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/features" className="hover:text-white transition-colors">Features</Link></li>
                <li><Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="/api" className="hover:text-white transition-colors">API</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/docs" className="hover:text-white transition-colors">Documentation</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
                <li><Link href="/status" className="hover:text-white transition-colors">Status</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-white transition-colors">Terms</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 ReHumanizer. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 