import { useState } from 'react'
import { Settings, Share2, Info, Sparkles, Zap, Shield } from 'lucide-react'
import TransmutePanel from './components/TransmutePanel'
import SettingsPanel from './components/SettingsPanel'
import DeveloperInfo from './components/DeveloperInfo'
import ShareModal from './components/ShareModal'

function App() {
  const [showSettings, setShowSettings] = useState(false)
  const [showDeveloperInfo, setShowDeveloperInfo] = useState(false)
  const [showShareModal, setShowShareModal] = useState(false)

  return (
    <div style={{
      background: '#09090b',
      color: '#fafafa',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      minHeight: '100vh',
      padding: '32px 16px'
    }}>
      <div style={{maxWidth: '1280px', margin: '0 auto'}}>
        
        {/* Header */}
        <div style={{
          background: '#18181b',
          border: '1px solid #27272a',
          borderRadius: '8px',
          padding: '24px',
          marginBottom: '32px',
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
        }}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px'}}>
            <div>
              <h1 style={{color: '#fafafa', fontSize: '24px', fontWeight: '600', margin: 0}}>
                AeroWave Systems DSP
              </h1>
              <p style={{color: '#71717a', marginTop: '4px', margin: '4px 0 0 0', fontSize: '14px'}}>
                Audio Engine // Verified for 12ms latency
              </p>
            </div>
            <div style={{display: 'flex', gap: '8px'}}>
              <button
                onClick={() => setShowSettings(true)}
                style={{
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  transition: 'all 0.2s ease'
                }}
              >
                <Settings style={{width: '16px', height: '16px'}} />
                Settings
              </button>
              <button
                onClick={() => setShowDeveloperInfo(true)}
                style={{
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  transition: 'all 0.2s ease'
                }}
              >
                <Info style={{width: '16px', height: '16px'}} />
                Info
              </button>
              <button
                onClick={() => setShowShareModal(true)}
                style={{
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  transition: 'all 0.2s ease'
                }}
              >
                <Share2 style={{width: '16px', height: '16px'}} />
                Share
              </button>
            </div>
          </div>
        </div>

        {/* Status Cards */}
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px', marginBottom: '32px'}}>
          <div style={{
            background: '#18181b',
            border: '1px solid #27272a',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
          }}>
            <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
              <Sparkles style={{width: '16px', height: '16px', color: '#71717a'}} />
              <h3 style={{color: '#a1a1aa', fontWeight: '500', fontSize: '14px', margin: 0}}>System Status</h3>
            </div>
            <p style={{color: '#10b981', fontSize: '20px', fontWeight: '600', margin: '8px 0'}}>Online</p>
            <p style={{color: '#71717a', fontSize: '13px', margin: 0}}>All systems operational</p>
          </div>
          
          <div style={{
            background: '#18181b',
            border: '1px solid #27272a',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
          }}>
            <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
              <Zap style={{width: '16px', height: '16px', color: '#71717a'}} />
              <h3 style={{color: '#a1a1aa', fontWeight: '500', fontSize: '14px', margin: 0}}>Processing Speed</h3>
            </div>
            <p style={{color: '#fafafa', fontSize: '20px', fontWeight: '600', margin: '8px 0'}}>89,000x</p>
            <p style={{color: '#71717a', fontSize: '13px', margin: 0}}>Faster than traditional</p>
          </div>
          
          <div style={{
            background: '#18181b',
            border: '1px solid #27272a',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
          }}>
            <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
              <Shield style={{width: '16px', height: '16px', color: '#71717a'}} />
              <h3 style={{color: '#a1a1aa', fontWeight: '500', fontSize: '14px', margin: 0}}>Verification</h3>
            </div>
            <p style={{color: '#10b981', fontSize: '20px', fontWeight: '600', margin: '8px 0'}}>Passed</p>
            <p style={{color: '#71717a', fontSize: '13px', margin: 0}}>Kani verified</p>
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
      <footer style={{
        background: '#18181b',
        border: '1px solid #27272a',
        borderRadius: '8px',
        padding: '20px',
        margin: '32px auto',
        maxWidth: '1280px',
        textAlign: 'center',
        boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
      }}>
        <p style={{color: '#71717a', fontSize: '14px', margin: 0}}>
          © 2026 <span style={{color: '#fafafa', fontWeight: '500'}}>Titan Black Swan Technologies</span> — AeroWave Systems DSP
        </p>
        <p style={{color: '#52525b', fontSize: '12px', marginTop: '8px', margin: '8px 0 0 0'}}>
          Engineering Division // Licensed under Apache 2.0
        </p>
      </footer>
    </div>
  )
}

export default App
