import { useState } from 'react'
import { Share2, Copy, Check, Twitter, Facebook, ExternalLink, X } from 'lucide-react'

function ShareModal({ onClose }) {
  const [copied, setCopied] = useState(false)
  const shareUrl = 'https://github.com/Titan-Black-Swan-Technologies/AeroWave-Systems-DSP'

  const handleCopy = () => {
    navigator.clipboard.writeText(shareUrl)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0, 0, 0, 0.5)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 50,
      padding: '16px'
    }}>
      <div style={{
        background: '#18181b',
        border: '1px solid #27272a',
        borderRadius: '8px',
        width: '100%',
        maxWidth: '400px',
        boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '20px',
          borderBottom: '1px solid #27272a'
        }}>
          <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
            <Share2 style={{width: '18px', height: '18px', color: '#71717a'}} />
            <h2 style={{color: '#fafafa', fontSize: '18px', fontWeight: '600', margin: 0}}>Share</h2>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#71717a',
              cursor: 'pointer',
              padding: '4px',
              borderRadius: '4px'
            }}
          >
            <X style={{width: '18px', height: '18px'}} />
          </button>
        </div>

        <div style={{padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px'}}>
          {/* Copy URL */}
          <div>
            <label style={{display: 'block', fontSize: '13px', color: '#a1a1aa', marginBottom: '6px'}}>Repository URL</label>
            <div style={{display: 'flex', gap: '6px'}}>
              <input
                type="text"
                readOnly
                value={shareUrl}
                style={{
                  flex: 1,
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  fontFamily: 'monospace',
                  fontSize: '13px'
                }}
              />
              <button
                onClick={handleCopy}
                style={{
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                {copied ? <Check style={{width: '16px', height: '16px'}} /> : <Copy style={{width: '16px', height: '16px'}} />}
              </button>
            </div>
            {copied && (
              <p style={{color: '#10b981', fontSize: '13px', marginTop: '6px'}}>URL copied to clipboard</p>
            )}
          </div>

          {/* Social Sharing */}
          <div>
            <label style={{display: 'block', fontSize: '13px', color: '#a1a1aa', marginBottom: '8px'}}>Social</label>
            <div style={{display: 'flex', flexDirection: 'column', gap: '8px'}}>
              <a
                href={`https://twitter.com/intent/tweet?text=${encodeURIComponent('Check out AeroWave Systems DSP - audio engine verified for 12ms latency ')}&url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 12px',
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  borderRadius: '6px',
                  textDecoration: 'none',
                  transition: 'all 0.2s ease'
                }}
              >
                <Twitter style={{width: '16px', height: '16px', color: '#71717a'}} />
                <span style={{color: '#fafafa', fontSize: '14px'}}>Twitter</span>
              </a>
              <a
                href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 12px',
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  borderRadius: '6px',
                  textDecoration: 'none',
                  transition: 'all 0.2s ease'
                }}
              >
                <Facebook style={{width: '16px', height: '16px', color: '#71717a'}} />
                <span style={{color: '#fafafa', fontSize: '14px'}}>Facebook</span>
              </a>
            </div>
          </div>

          {/* Open Link */}
          <a
            href={shareUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              background: '#fafafa',
              border: '1px solid #3f3f46',
              color: '#09090b',
              padding: '8px 16px',
              borderRadius: '6px',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              justifyContent: 'center',
              width: '100%',
              textDecoration: 'none',
              transition: 'all 0.2s ease'
            }}
          >
            <ExternalLink style={{width: '16px', height: '16px'}} />
            <span>Open in new tab</span>
          </a>
        </div>
      </div>
    </div>
  )
}

export default ShareModal
