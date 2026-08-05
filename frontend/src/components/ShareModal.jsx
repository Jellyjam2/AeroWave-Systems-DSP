import { X, Link as LinkIcon, Twitter, Facebook, Copy, Check } from 'lucide-react'
import { useState } from 'react'

function ShareModal({ onClose }) {
  const [copied, setCopied] = useState(false)
  const shareUrl = 'https://github.com/Jellyjam2/AeroWave-Systems-DSP'
  const shareText = 'Check out AeroWave Systems DSP - A cognitive audio synthesis engine built to aerospace-grade standards!'

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleTwitterShare = () => {
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`
    window.open(twitterUrl, '_blank')
  }

  const handleFacebookShare = () => {
    const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`
    window.open(facebookUrl, '_blank')
  }

  return (
    <div className="fixed inset-0 bg-void-900/90 backdrop-blur-glass flex items-center justify-center z-50 p-4">
      <div className="glass-card rounded-2xl w-full max-w-md">
        <div className="flex items-center justify-between p-6 border-b border-glass-border">
          <div className="flex items-center gap-3">
            <Share2 className="w-6 h-6 text-neon-cyan" />
            <h2 className="text-2xl font-bold neon-text-cyan">TRANSMIT DATA</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-neon-cyan transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Copy URL */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">SYSTEM URL</label>
            <div className="flex gap-2">
              <input
                type="text"
                readOnly
                value={shareUrl}
                className="input-field flex-1 rounded-lg p-3 font-mono text-sm"
              />
              <button
                onClick={handleCopy}
                className="glow-button px-4 rounded-lg"
              >
                {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
              </button>
            </div>
            {copied && (
              <p className="text-neon-green text-sm mt-2">URL COPIED TO CLIPBOARD</p>
            )}
          </div>

          {/* Social Sharing */}
          <div>
            <label className="block text-sm text-gray-400 mb-3">SOCIAL TRANSMISSION</label>
            <div className="space-y-3">
              <a
                href="https://twitter.com/intent/tweet?text=Check%20out%20AeroWave%20Systems%20DSP%20by%20Titan%20Black%20Swan%20Technologies%20-%20aerospace-grade%20cognitive%20audio%20synthesis%20engine%20https://github.com/Titan-Black-Swan-Technologies/AeroWave-Systems-DSP"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 px-4 py-3 bg-glass-highlight hover:bg-glass-border rounded-xl transition-all duration-300 border border-glass-border"
              >
                <Twitter className="w-5 h-5 text-neon-cyan" />
                <span className="text-neon-cyan">TRANSMIT VIA TWITTER</span>
              </a>
              <a
                href="https://www.facebook.com/sharer/sharer.php?u=https://github.com/Titan-Black-Swan-Technologies/AeroWave-Systems-DSP"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 px-4 py-3 bg-glass-highlight hover:bg-glass-border rounded-xl transition-all duration-300 border border-glass-border"
              >
                <Facebook className="w-5 h-5 text-neon-purple" />
                <span className="text-neon-purple">TRANSMIT VIA FACEBOOK</span>
              </a>
            </div>
          </div>

          {/* Open Link */}
          <a
            href={shareUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="glow-button w-full py-3 rounded-xl font-semibold flex items-center justify-center gap-2"
          >
            <ExternalLink className="w-5 h-5" />
            <span>OPEN IN NEW TAB</span>
          </a>
        </div>
      </div>
    </div>
  )
}

export default ShareModal
