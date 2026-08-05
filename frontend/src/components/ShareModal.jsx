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
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-card w-full max-w-md">
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <h2 className="text-2xl font-bold">Share AeroWave</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* URL Copy */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Project URL</label>
            <div className="flex gap-2">
              <input
                type="text"
                value={shareUrl}
                readOnly
                className="input-field flex-1"
              />
              <button
                onClick={handleCopy}
                className="p-3 bg-primary-500 hover:bg-primary-600 rounded-xl transition-all duration-300"
                title="Copy URL"
              >
                {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* Social Share Buttons */}
          <div>
            <label className="block text-sm text-gray-400 mb-3">Share on Social Media</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={handleTwitterShare}
                className="flex items-center justify-center gap-2 p-3 bg-[#1DA1F2]/20 hover:bg-[#1DA1F2]/30 border border-[#1DA1F2]/50 rounded-xl transition-all duration-300"
              >
                <Twitter className="w-5 h-5 text-[#1DA1F2]" />
                <span>Twitter</span>
              </button>
              <button
                onClick={handleFacebookShare}
                className="flex items-center justify-center gap-2 p-3 bg-[#4267B2]/20 hover:bg-[#4267B2]/30 border border-[#4267B2]/50 rounded-xl transition-all duration-300"
              >
                <Facebook className="w-5 h-5 text-[#4267B2]" />
                <span>Facebook</span>
              </button>
            </div>
          </div>

          {/* Direct Link */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Direct Link</label>
            <a
              href={shareUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300"
            >
              <LinkIcon className="w-5 h-5" />
              <span>Open in New Tab</span>
            </a>
          </div>

          {/* Info */}
          <div className="p-4 bg-white/5 rounded-xl text-center">
            <p className="text-sm text-gray-400">
              Help spread the word about aerospace-grade cognitive audio synthesis!
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ShareModal
