import { X, Github, Mail, Code, Music, Award, Zap } from 'lucide-react'

function DeveloperInfo({ onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-card w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <h2 className="text-2xl font-bold">Developer Information</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Profile Section */}
          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
              <span className="text-4xl font-bold">EHL</span>
            </div>
            <h3 className="text-2xl font-bold">Enrico Heinrich Leitch</h3>
            <p className="text-gray-400 mt-2">Founder & Lead Developer</p>
            <p className="text-primary-400 text-sm">Black Swan Technologies</p>
            <p className="text-accent-400 text-xs mt-1">AeroWave Systems DSP</p>
          </div>

          {/* Contact */}
          <div className="flex justify-center gap-4">
            <a
              href="https://github.com/Jellyjam2"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300"
            >
              <Github className="w-5 h-5" />
              <span>GitHub</span>
            </a>
            <a
              href="mailto:enrico@aerowave.systems"
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300"
            >
              <Mail className="w-5 h-5" />
              <span>Email</span>
            </a>
          </div>

          {/* About */}
          <div>
            <h4 className="font-semibold mb-3 flex items-center gap-2">
              <Code className="w-5 h-5 text-primary-400" />
              About the Project
            </h4>
            <p className="text-gray-300 text-sm leading-relaxed">
              AeroWave Systems DSP is a cognitive audio synthesis engine that transforms multi-dimensional 
              language semantics and physiological bio-signals into mathematically optimized multi-track 
              orchestral music. Built to aerospace-grade reliability standards using NASA and Tesla 
              architectural paradigms.
            </p>
          </div>

          {/* Technical Achievements */}
          <div>
            <h4 className="font-semibold mb-3 flex items-center gap-2">
              <Award className="w-5 h-5 text-accent-400" />
              Technical Achievements
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-3 bg-white/5 rounded-xl">
                <p className="text-sm text-gray-400">Formal Verification</p>
                <p className="font-semibold text-green-400">Kani Verified ✓</p>
              </div>
              <div className="p-3 bg-white/5 rounded-xl">
                <p className="text-sm text-gray-400">Performance</p>
                <p className="font-semibold text-accent-400">89,000x Speedup</p>
              </div>
              <div className="p-3 bg-white/5 rounded-xl">
                <p className="text-sm text-gray-400">Memory</p>
                <p className="font-semibold text-primary-400">Zero Allocation</p>
              </div>
              <div className="p-3 bg-white/5 rounded-xl">
                <p className="text-sm text-gray-400">Concurrency</p>
                <p className="font-semibold text-purple-400">Lock-Free</p>
              </div>
            </div>
          </div>

          {/* Core Technologies */}
          <div>
            <h4 className="font-semibold mb-3 flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              Core Technologies
            </h4>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-primary-500/20 text-primary-400 rounded-full text-sm">Rust</span>
              <span className="px-3 py-1 bg-accent-500/20 text-accent-400 rounded-full text-sm">Python</span>
              <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">PyO3</span>
              <span className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">nalgebra</span>
              <span className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-sm">Flask</span>
              <span className="px-3 py-1 bg-pink-500/20 text-pink-400 rounded-full text-sm">React</span>
              <span className="px-3 py-1 bg-orange-500/20 text-orange-400 rounded-full text-sm">TailwindCSS</span>
            </div>
          </div>

          {/* License */}
          <div className="p-4 bg-white/5 rounded-xl text-center">
            <p className="text-sm text-gray-400">
              Licensed under <span className="text-primary-400 font-semibold">Apache License 2.0</span>
            </p>
            <p className="text-xs text-gray-500 mt-1">
              © 2026 <span className="text-accent-400">Black Swan Technologies</span>. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DeveloperInfo
