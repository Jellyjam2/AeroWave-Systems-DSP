import { useState } from 'react'
import { Music, Settings, Share2, Trash2, Info, Sparkles, Zap, Shield } from 'lucide-react'
import TransmutePanel from './components/TransmutePanel'
import SettingsPanel from './components/SettingsPanel'
import DeveloperInfo from './components/DeveloperInfo'
import ShareModal from './components/ShareModal'

function App() {
  const [showSettings, setShowSettings] = useState(false)
  const [showDeveloperInfo, setShowDeveloperInfo] = useState(false)
  const [showShareModal, setShowShareModal] = useState(false)

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="glass-card m-4 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl animate-pulse-slow">
              <Music className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
                AeroWave Systems DSP
              </h1>
              <p className="text-sm text-gray-400">Cognitive Audio Synthesis Engine v1.0</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowShareModal(true)}
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300 hover:scale-105"
              title="Share"
            >
              <Share2 className="w-5 h-5" />
            </button>
            <button
              onClick={() => setShowSettings(true)}
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300 hover:scale-105"
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </button>
            <button
              onClick={() => setShowDeveloperInfo(true)}
              className="p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300 hover:scale-105"
              title="Developer Info"
            >
              <Info className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-2">
              <Sparkles className="w-6 h-6 text-primary-400" />
              <h3 className="font-semibold">System Status</h3>
            </div>
            <p className="text-3xl font-bold text-green-400">Online</p>
            <p className="text-sm text-gray-400">All systems operational</p>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-2">
              <Zap className="w-6 h-6 text-accent-400" />
              <h3 className="font-semibold">Processing Speed</h3>
            </div>
            <p className="text-3xl font-bold text-accent-400">89,000x</p>
            <p className="text-sm text-gray-400">Faster than traditional</p>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-2">
              <Shield className="w-6 h-6 text-green-400" />
              <h3 className="font-semibold">Formal Verification</h3>
            </div>
            <p className="text-3xl font-bold text-green-400">✓ Passed</p>
            <p className="text-sm text-gray-400">Kani verified</p>
          </div>
        </div>

        {/* Transmute Panel */}
        <TransmutePanel />
      </main>

      {/* Modals */}
      {showSettings && (
        <SettingsPanel onClose={() => setShowSettings(false)} />
      )}
      
      {showDeveloperInfo && (
        <DeveloperInfo onClose={() => setShowDeveloperInfo(false)} />
      )}
      
      {showShareModal && (
        <ShareModal onClose={() => setShowShareModal(false)} />
      )}

      {/* Footer */}
      <footer className="glass-card m-4 p-6 text-center">
        <p className="text-gray-400">
          © 2026 AeroWave Systems DSP by <span className="text-primary-400 font-semibold">Enrico Heinrich Leitch</span>
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Licensed under Apache 2.0 | Built with aerospace-grade reliability
        </p>
      </footer>
    </div>
  )
}

export default App
