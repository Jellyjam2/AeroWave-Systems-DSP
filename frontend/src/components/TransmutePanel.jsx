import { useState } from 'react'
import { Send, Trash2, Download, Music, Loader2, Zap } from 'lucide-react'
import axios from 'axios'

function TransmutePanel() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleTransmute = async () => {
    if (!text.trim()) return
    
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/transmute', { text })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Transmutation failed')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setResult(null)
    setError(null)
  }

  const handleDownload = async () => {
    try {
      const response = await axios.get('/api/download', { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'transmutation.mid')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      setError('Download failed')
    }
  }

  return (
    <div style={{
      background: '#18181b',
      border: '1px solid #27272a',
      borderRadius: '8px',
      padding: '24px',
      boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
    }}>
      <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px'}}>
        <Music style={{width: '20px', height: '20px', color: '#71717a'}} />
        <h2 style={{color: '#fafafa', fontSize: '18px', fontWeight: '600', margin: 0}}>Transmute</h2>
      </div>
      
      <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
        {/* Input Area */}
        <div>
          <label style={{display: 'block', fontSize: '13px', fontWeight: '500', color: '#a1a1aa', marginBottom: '8px'}}>
            Input
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text description for audio synthesis..."
            style={{
              width: '100%',
              height: '120px',
              background: '#27272a',
              border: '1px solid #3f3f46',
              color: '#fafafa',
              borderRadius: '6px',
              padding: '12px',
              resize: 'none',
              fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
              fontSize: '14px'
            }}
          />
        </div>

        {/* Action Buttons */}
        <div style={{display: 'flex', gap: '8px'}}>
          <button
            onClick={handleTransmute}
            disabled={loading || !text.trim()}
            style={{
              background: loading || !text.trim() ? '#27272a' : '#fafafa',
              border: '1px solid #3f3f46',
              color: loading || !text.trim() ? '#71717a' : '#09090b',
              padding: '8px 16px',
              borderRadius: '6px',
              fontSize: '14px',
              fontWeight: '500',
              cursor: loading || !text.trim() ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.2s ease',
              flex: 1,
              opacity: loading || !text.trim() ? 0.5 : 1
            }}
          >
            {loading ? (
              <>
                <div style={{width: '16px', height: '16px', border: '2px solid #71717a', borderTop: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite'}}></div>
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Zap style={{width: '16px', height: '16px'}} />
                <span>Execute</span>
              </>
            )}
          </button>
          
          <button
            onClick={handleClear}
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
            <Trash2 style={{width: '16px', height: '16px'}} />
            <span>Clear</span>
          </button>
        </div>

        {/* Output Area */}
        {result && (
          <div style={{
            marginTop: '16px',
            padding: '16px',
            background: '#27272a',
            borderRadius: '6px',
            border: '1px solid #3f3f46'
          }}>
            <h3 style={{color: '#fafafa', fontSize: '14px', fontWeight: '500', marginBottom: '12px'}}>Output</h3>
            
            <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
              <div>
                <p style={{fontSize: '13px', color: '#71717a', marginBottom: '4px'}}>Generated MIDI</p>
                <p style={{color: '#10b981', fontFamily: 'monospace', fontSize: '13px'}}>{result.midi_file}</p>
              </div>
              
              {result.analysis && (
                <div>
                  <p style={{fontSize: '13px', color: '#71717a', marginBottom: '8px'}}>Analysis</p>
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', fontSize: '13px'}}>
                    <div>
                      <span style={{color: '#71717a'}}>Emotion:</span>
                      <span style={{color: '#fafafa', marginLeft: '8px'}}>{result.analysis.emotion || 'N/A'}</span>
                    </div>
                    <div>
                      <span style={{color: '#71717a'}}>Complexity:</span>
                      <span style={{color: '#fafafa', marginLeft: '8px'}}>{result.analysis.complexity || 'N/A'}</span>
                    </div>
                    <div>
                      <span style={{color: '#71717a'}}>Duration:</span>
                      <span style={{color: '#fafafa', marginLeft: '8px'}}>{result.analysis.duration || 'N/A'}</span>
                    </div>
                    <div>
                      <span style={{color: '#71717a'}}>Tracks:</span>
                      <span style={{color: '#fafafa', marginLeft: '8px'}}>{result.analysis.tracks || 'N/A'}</span>
                    </div>
                  </div>
                </div>
              )}
              
              <button
                onClick={handleDownload}
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
                  justifyContent: 'center',
                  width: '100%',
                  transition: 'all 0.2s ease'
                }}
              >
                <Music style={{width: '16px', height: '16px'}} />
                <span>Download MIDI</span>
              </button>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div style={{
            marginTop: '16px',
            padding: '12px',
            background: 'rgba(239, 68, 68, 0.1)',
            borderRadius: '6px',
            border: '1px solid rgba(239, 68, 68, 0.2)'
          }}>
            <p style={{color: '#ef4444', fontSize: '14px', fontWeight: '500', margin: 0}}>Error: {error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default TransmutePanel
