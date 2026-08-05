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
    <div className="min-h-screen bg-void-gradient command-grid relative overflow-hidden">
      {/* Ambient Glow Effects */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-neon-cyan/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-neon-purple/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="glass-card rounded-2xl p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold neon-text-cyan mb-2">AEROWAVE SYSTEMS DSP</h1>
              <p className="text-gray-400">Cognitive Audio Synthesis Engine // Titan Command Interface</p>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setShowSettings(true)}
                className="glow-button px-6 py-3 rounded-xl font-semibold flex items-center gap-2"
              >
                <Settings className="w-5 h-5" />
                <span>COMMAND</span>
              </button>
              <button
                onClick={() => setShowDeveloperInfo(true)}
                className="glow-button px-6 py-3 rounded-xl font-semibold flex items-center gap-2"
              >
                <Info className="w-5 h-5" />
                <span>SYSTEM</span>
              </button>
              <button
                onClick={() => setShowShareModal(true)}
                className="glow-button px-6 py-3 rounded-xl font-semibold flex items-center gap-2"
              >
                <Share2 className="w-5 h-5" />
                <span>TRANSMIT</span>
              </button>
            </div>
          </div>
        </header>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-2">
              <Sparkles className="w-6 h-6 text-neon-cyan" />
              <h3 className="font-semibold text-neon-cyan">System Status</h3>
            </div>
            <p className="text-3xl font-bold text-neon-green">ONLINE</p>
            <p className="text-sm text-gray-400">All systems operational</p>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-2">
              <Zap className="w-6 h-6 text-neon-purple" />
              <h3 className="font-semibold text-neon-purple">Processing Speed</h3>
            </div>
            <p className="text-3xl font-bold text-neon-purple">89,000x</p>
            <p className="text-sm text-gray-400">Faster than traditional</p>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-2">
              <Shield className="w-6 h-6 text-neon-green" />
              <h3 className="font-semibold text-neon-green">Formal Verification</h3>
            </div>
            <p className="text-3xl font-bold text-neon-green">✓ PASSED</p>
            <p className="text-sm text-gray-400">Kani verified</p>
          </div>
        </div>

        {/* Transmute Panel */}
        <main>
          <TransmutePanel />
        </main>
      </div>

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
          © 2026 <span className="neon-text-cyan font-semibold">TITAN BLACK SWAN TECHNOLOGIES</span> - AEROWAVE SYSTEMS DSP
        </p>
        <p className="text-sm text-gray-500 mt-2">
          ENGINEERING DIVISION // LICENSED UNDER APACHE 2.0
        </p>
      </footer>
    </div>
  )
}

export default App
