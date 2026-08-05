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
        <div className="p-2 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg">
          <Music className="w-6 h-6 text-white" />
        </div>
        <h2 className="text-xl font-bold">Cognitive Transmutation</h2>
      </div>

      <div className="space-y-4">
        <div className="relative">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter your emotional text or bio-feedback data..."
            className="input-field w-full h-40 resize-none"
          />
          <button
            onClick={handleClear}
            className="absolute top-3 right-3 p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300"
            title="Clear text"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleTransmute}
            disabled={loading || !text.trim()}
            className="glow-button flex-1 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Transmute to Music
              </>
            )}
          </button>

          {result && (
            <button
              onClick={handleDownload}
              className="glow-button flex items-center justify-center gap-2"
            >
              <Download className="w-5 h-5" />
              Download MIDI
            </button>
          )}
        </div>

        {error && (
          <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {result && (
          <div className="p-6 bg-green-500/10 border border-green-500/30 rounded-xl space-y-3">
            <h3 className="font-semibold text-green-400">✓ Transmutation Successful</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-400">Data Points</p>
                <p className="font-semibold">{result.data_points}</p>
              </div>
              <div>
                <p className="text-gray-400">Sentiment</p>
                <p className="font-semibold">{result.sentiment?.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-gray-400">Arousal</p>
                <p className="font-semibold">{result.arousal?.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-gray-400">Complexity</p>
                <p className="font-semibold">{result.complexity?.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-gray-400">Generation Time</p>
                <p className="font-semibold">{result.generation_time?.toFixed(3)}s</p>
              </div>
              <div>
                <p className="text-gray-400">Cache Hit</p>
                <p className="font-semibold">{result.cache_hit ? 'Yes' : 'No'}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default TransmutePanel
