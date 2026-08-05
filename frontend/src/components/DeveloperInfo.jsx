import { X, Github, Mail, Code, Music, Award, Zap, Info, Cpu } from 'lucide-react'

function DeveloperInfo({ onClose }) {
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
        maxWidth: '512px',
        maxHeight: '90vh',
        overflowY: 'auto',
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
            <Info style={{width: '18px', height: '18px', color: '#71717a'}} />
            <h2 style={{color: '#fafafa', fontSize: '18px', fontWeight: '600', margin: 0}}>System Information</h2>
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

        <div style={{padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px'}}>
          {/* Profile Section */}
          <div style={{textAlign: 'center'}}>
            <div style={{
              width: '64px',
              height: '64px',
              margin: '0 auto 12px',
              background: '#27272a',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid #3f3f46'
            }}>
              <span style={{fontSize: '20px', fontWeight: '600', color: '#fafafa'}}>TBS</span>
            </div>
            <h3 style={{color: '#fafafa', fontSize: '18px', fontWeight: '600', margin: '0 0 4px 0'}}>Titan Black Swan Technologies</h3>
            <p style={{color: '#71717a', fontSize: '14px', margin: '0 0 2px 0'}}>Engineering Division</p>
            <p style={{color: '#a1a1aa', fontSize: '13px', margin: 0}}>AeroWave Systems DSP</p>
          </div>

          {/* Contact */}
          <div style={{display: 'flex', justifyContent: 'center', gap: '8px'}}>
            <a
              href="https://github.com/Titan-Black-Swan-Technologies"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 12px',
                background: '#27272a',
                border: '1px solid #3f3f46',
                borderRadius: '6px',
                textDecoration: 'none',
                transition: 'all 0.2s ease'
              }}
            >
              <Github style={{width: '16px', height: '16px', color: '#71717a'}} />
              <span style={{color: '#fafafa', fontSize: '14px'}}>GitHub</span>
            </a>
            <a
              href="mailto:engineering@blackswan.tech"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 12px',
                background: '#27272a',
                border: '1px solid #3f3f46',
                borderRadius: '6px',
                textDecoration: 'none',
                transition: 'all 0.2s ease'
              }}
            >
              <Mail style={{width: '16px', height: '16px', color: '#71717a'}} />
              <span style={{color: '#fafafa', fontSize: '14px'}}>Email</span>
            </a>
          </div>

          {/* About */}
          <div>
            <h4 style={{fontWeight: '600', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', color: '#fafafa', fontSize: '14px'}}>
              <Code style={{width: '16px', height: '16px', color: '#71717a'}} />
              System Overview
            </h4>
            <p style={{color: '#a1a1aa', fontSize: '14px', lineHeight: '1.5', margin: 0}}>
              AeroWave Systems DSP is a deterministic, lock-free audio processing unit verified for 12ms latency targets.
            </p>
          </div>

          {/* Technical Achievements */}
          <div>
            <h4 style={{fontWeight: '600', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', color: '#fafafa', fontSize: '14px'}}>
              <Award style={{width: '16px', height: '16px', color: '#71717a'}} />
              Technical Specifications
            </h4>
            <div style={{display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '13px'}}>
              <div style={{display: 'flex', justifyContent: 'space-between'}}>
                <span style={{color: '#71717a'}}>Processing Speed</span>
                <span style={{color: '#10b981', fontFamily: 'monospace'}}>89,000x</span>
              </div>
              <div style={{display: 'flex', justifyContent: 'space-between'}}>
                <span style={{color: '#71717a'}}>Memory Allocation</span>
                <span style={{color: '#fafafa', fontFamily: 'monospace'}}>Zero-Heap</span>
              </div>
              <div style={{display: 'flex', justifyContent: 'space-between'}}>
                <span style={{color: '#71717a'}}>Thread Isolation</span>
                <span style={{color: '#fafafa', fontFamily: 'monospace'}}>Lock-Free</span>
              </div>
              <div style={{display: 'flex', justifyContent: 'space-between'}}>
                <span style={{color: '#71717a'}}>Formal Verification</span>
                <span style={{color: '#10b981', fontFamily: 'monospace'}}>Kani ✓</span>
              </div>
            </div>
          </div>

          {/* Core Technologies */}
          <div>
            <h4 style={{fontWeight: '600', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', color: '#fafafa', fontSize: '14px'}}>
              <Cpu style={{width: '16px', height: '16px', color: '#71717a'}} />
              Core Technologies
            </h4>
            <div style={{display: 'flex', flexWrap: 'wrap', gap: '6px'}}>
              <span style={{
                padding: '4px 10px',
                background: '#27272a',
                color: '#fafafa',
                borderRadius: '9999px',
                fontSize: '13px',
                border: '1px solid #3f3f46'
              }}>Rust</span>
              <span style={{
                padding: '4px 10px',
                background: '#27272a',
                color: '#fafafa',
                borderRadius: '9999px',
                fontSize: '13px',
                border: '1px solid #3f3f46'
              }}>Python</span>
              <span style={{
                padding: '4px 10px',
                background: '#27272a',
                color: '#fafafa',
                borderRadius: '9999px',
                fontSize: '13px',
                border: '1px solid #3f3f46'
              }}>React</span>
              <span style={{
                padding: '4px 10px',
                background: '#27272a',
                color: '#fafafa',
                borderRadius: '9999px',
                fontSize: '13px',
                border: '1px solid #3f3f46'
              }}>TailwindCSS</span>
            </div>
          </div>

          {/* License */}
          <div style={{
            padding: '12px',
            background: '#27272a',
            borderRadius: '6px',
            textAlign: 'center',
            border: '1px solid #3f3f46'
          }}>
            <p style={{fontSize: '13px', color: '#71717a', margin: 0}}>
              Licensed under <span style={{color: '#fafafa', fontWeight: '500'}}>Apache License 2.0</span>
            </p>
            <p style={{fontSize: '12px', color: '#52525b', marginTop: '6px', margin: '6px 0 0 0'}}>
              © 2026 <span style={{color: '#fafafa'}}>Titan Black Swan Technologies</span>. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DeveloperInfo
