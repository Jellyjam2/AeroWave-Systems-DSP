import { useState } from 'react'
import { Send, Trash2, Download, Music, Loader2 } from 'lucide-react'
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
    <div className="glass-card p-8">
      <div className="flex items-center gap-3 mb-6">
        <Music className="w-8 h-8 text-neon-cyan" />
        <h2 className="text-2xl font-bold neon-text-cyan">TRANSMUTE COMMAND</h2>
      </div>
      
      <div className="space-y-6">
        {/* Input Area */}
        <div>
          <label className="block text-sm font-semibold text-neon-cyan mb-2">
            INPUT DATA
          </label>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter text description for audio synthesis..."
            className="input-field w-full h-40 rounded-xl p-4 resize-none"
          />
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={handleTransmute}
            disabled={loading || !inputText.trim()}
            className="glow-button px-8 py-3 rounded-xl font-semibold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed flex-1"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-neon-cyan border-t-transparent rounded-full animate-spin"></div>
                <span>PROCESSING...</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>EXECUTE TRANSMUTE</span>
              </>
            )}
          </button>
          
          <button
            onClick={handleClear}
            className="glow-button px-6 py-3 rounded-xl font-semibold flex items-center gap-2"
          >
            <Trash2 className="w-5 h-5" />
            <span>CLEAR</span>
          </button>
        </div>

        {/* Output Area */}
        {result && (
          <div className="mt-6 p-6 bg-void-800/50 rounded-xl border border-neon-cyan/20">
            <h3 className="text-lg font-semibold text-neon-cyan mb-4">OUTPUT DATA</h3>
            
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-400 mb-1">Generated MIDI</p>
                <p className="text-neon-green font-mono">{result.midi_file}</p>
              </div>
              
              {result.analysis && (
                <div>
                  <p className="text-sm text-gray-400 mb-2">Analysis Results</p>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-400">Emotion:</span>
                      <span className="text-neon-purple ml-2">{result.analysis.emotion || 'N/A'}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Complexity:</span>
                      <span className="text-neon-cyan ml-2">{result.analysis.complexity || 'N/A'}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Duration:</span>
                      <span className="text-neon-green ml-2">{result.analysis.duration || 'N/A'}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Tracks:</span>
                      <span className="text-neon-purple ml-2">{result.analysis.tracks || 'N/A'}</span>
                    </div>
                  </div>
                </div>
              )}
              
              <button
                onClick={handleDownload}
                className="glow-button px-6 py-2 rounded-lg font-semibold flex items-center gap-2 w-full justify-center"
              >
                <Music className="w-5 h-5" />
                <span>DOWNLOAD MIDI</span>
              </button>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mt-6 p-4 bg-neon-red/10 border border-neon-red/30 rounded-xl">
            <p className="text-neon-red font-semibold">ERROR: {error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default TransmutePanel
