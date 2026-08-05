import { X, Volume2, Sliders, Globe, Palette, Settings, Zap, Cpu, Eye } from 'lucide-react'

function SettingsPanel({ onClose }) {
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
            <Settings style={{width: '18px', height: '18px', color: '#71717a'}} />
            <h2 style={{color: '#fafafa', fontSize: '18px', fontWeight: '600', margin: 0}}>Settings</h2>
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

        <div style={{padding: '20px', display: 'flex', flexDirection: 'column', gap: '24px'}}>
          {/* Audio Settings */}
          <div>
            <h3 style={{color: '#fafafa', fontSize: '14px', fontWeight: '600', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px'}}>
              <Zap style={{width: '16px', height: '16px', color: '#71717a'}} />
              Audio Configuration
            </h3>
            <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
              <div>
                <label style={{display: 'block', fontSize: '13px', color: '#a1a1aa', marginBottom: '6px'}}>Sample Rate</label>
                <select style={{
                  width: '100%',
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  fontSize: '14px',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
                }}>
                  <option>44100 Hz</option>
                  <option>48000 Hz</option>
                  <option>96000 Hz</option>
                </select>
              </div>
              <div>
                <label style={{display: 'block', fontSize: '13px', color: '#a1a1aa', marginBottom: '6px'}}>Bit Depth</label>
                <select style={{
                  width: '100%',
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  fontSize: '14px',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
                }}>
                  <option>16-bit</option>
                  <option>24-bit</option>
                  <option>32-bit</option>
                </select>
              </div>
            </div>
          </div>

          {/* Processing Settings */}
          <div>
            <h3 style={{color: '#fafafa', fontSize: '14px', fontWeight: '600', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px'}}>
              <Cpu style={{width: '16px', height: '16px', color: '#71717a'}} />
              Processing Parameters
            </h3>
            <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
              <div>
                <label style={{display: 'block', fontSize: '13px', color: '#a1a1aa', marginBottom: '6px'}}>Complexity Level</label>
                <select style={{
                  width: '100%',
                  background: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#fafafa',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  fontSize: '14px',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
                }}>
                  <option>Low</option>
                  <option>Medium</option>
                  <option>High</option>
                  <option>Maximum</option>
                </select>
              </div>
              <div>
                <label style={{display: 'block', fontSize: '13px', color: '#a1a1aa', marginBottom: '6px'}}>Cache Size (MB)</label>
                <input
                  type="number"
                  defaultValue="64"
                  style={{
                    width: '100%',
                    background: '#27272a',
                    border: '1px solid #3f3f46',
                    color: '#fafafa',
                    borderRadius: '6px',
                    padding: '8px 12px',
                    fontSize: '14px',
                    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
                  }}
                />
              </div>
            </div>
          </div>

          {/* Save Button */}
          <button style={{
            background: '#fafafa',
            border: '1px solid #3f3f46',
            color: '#09090b',
            padding: '8px 16px',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: '500',
            cursor: 'pointer',
            width: '100%',
            transition: 'all 0.2s ease'
          }}>
            Save Settings
          </button>
        </div>
      </div>
    </div>
  )
}

export default SettingsPanel
