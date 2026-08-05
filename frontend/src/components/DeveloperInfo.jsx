import { X, Github, Mail, Code, Music, Award, Zap, Info, Cpu } from 'lucide-react'

function DeveloperInfo({ onClose }) {
  return (
    <div className="fixed inset-0 bg-void-900/90 backdrop-blur-glass flex items-center justify-center z-50 p-4">
      <div className="glass-card rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-glass-border">
          <div className="flex items-center gap-3">
            <Info className="w-6 h-6 text-neon-cyan" />
            <h2 className="text-2xl font-bold neon-text-cyan">SYSTEM INFORMATION</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-neon-cyan transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Profile Section */}
          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-br from-neon-cyan to-neon-purple rounded-full flex items-center justify-center shadow-neon-cyan">
              <span className="text-4xl font-bold text-void-900">TBS</span>
            </div>
            <h3 className="text-2xl font-bold neon-text-cyan">TITAN BLACK SWAN TECHNOLOGIES</h3>
            <p className="text-gray-400 mt-2">ENGINEERING DIVISION</p>
            <p className="text-neon-purple text-sm">AEROWAVE SYSTEMS DSP</p>
          </div>

          {/* Contact */}
          <div className="flex justify-center gap-4">
            <a
              href="https://github.com/Titan-Black-Swan-Technologies"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-4 py-2 bg-glass-highlight hover:bg-glass-border rounded-xl transition-all duration-300 border border-glass-border"
            >
              <Github className="w-5 h-5 text-neon-cyan" />
              <span className="text-neon-cyan">GITHUB ORGANIZATION</span>
            </a>
            <a
              href="mailto:engineering@blackswan.tech"
              className="flex items-center gap-2 px-4 py-2 bg-glass-highlight hover:bg-glass-border rounded-xl transition-all duration-300 border border-glass-border"
            >
              <Mail className="w-5 h-5 text-neon-purple" />
              <span className="text-neon-purple">CONTACT ENGINEERING</span>
            </a>
          </div>

          {/* About */}
          <div>
            <h4 className="font-semibold mb-3 flex items-center gap-2 text-neon-cyan">
              <Code className="w-5 h-5" />
              SYSTEM OVERVIEW
            </h4>
            <p className="text-gray-300 text-sm leading-relaxed">
              AeroWave Systems DSP is a deterministic, lock-free cognitive audio synthesis engine built to aerospace-grade reliability standards using NASA and Tesla architectural paradigms.
            </p>
          </div>

          {/* Technical Achievements */}
          <div>
            <h4 className="font-semibold mb-3 flex items-center gap-2 text-neon-purple">
              <Award className="w-5 h-5" />
              TECHNICAL SPECIFICATIONS
            </h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Processing Speed</span>
                <span className="text-neon-green font-mono">89,000x</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Memory Allocation</span>
                <span className="text-neon-cyan font-mono">Zero-Heap</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Thread Isolation</span>
                <span className="text-neon-purple font-mono">Lock-Free</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Formal Verification</span>
                <span className="text-neon-green font-mono">Kani ✓</span>
              </div>
            </div>
          </div>

          {/* Core Technologies */}
          <div>
            <h4 className="font-semibold mb-3 flex items-center gap-2 text-neon-cyan">
              <Cpu className="w-5 h-5" />
              CORE TECHNOLOGIES
            </h4>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-neon-cyan/20 text-neon-cyan rounded-full text-sm border border-neon-cyan/30">Rust</span>
              <span className="px-3 py-1 bg-neon-purple/20 text-neon-purple rounded-full text-sm border border-neon-purple/30">Python</span>
              <span className="px-3 py-1 bg-neon-green/20 text-neon-green rounded-full text-sm border border-neon-green/30">React</span>
              <span className="px-3 py-1 bg-neon-cyan/20 text-neon-cyan rounded-full text-sm border border-neon-cyan/30">TailwindCSS</span>
            </div>
          </div>

          {/* License */}
          <div className="p-4 bg-glass-highlight rounded-xl text-center border border-glass-border">
            <p className="text-sm text-gray-400">
              Licensed under <span className="text-neon-cyan font-semibold">Apache License 2.0</span>
            </p>
            <p className="text-xs text-gray-500 mt-1">
              2026 <span className="text-neon-purple">TITAN BLACK SWAN TECHNOLOGIES</span>. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DeveloperInfo
