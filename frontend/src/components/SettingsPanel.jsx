import { X, Volume2, Sliders, Globe, Palette } from 'lucide-react'

function SettingsPanel({ onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-card w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <h2 className="text-2xl font-bold">Settings</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-8">
          {/* Audio Settings */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Volume2 className="w-5 h-5 text-primary-400" />
              <h3 className="text-lg font-semibold">Audio Settings</h3>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Output Sample Rate</label>
                <select className="input-field w-full">
                  <option value="44100">44.1 kHz (CD Quality)</option>
                  <option value="48000">48.0 kHz (Professional)</option>
                  <option value="96000">96.0 kHz (High-Res)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">Bit Depth</label>
                <select className="input-field w-full">
                  <option value="16">16-bit</option>
                  <option value="24">24-bit</option>
                  <option value="32">32-bit Float</option>
                </select>
              </div>
            </div>
          </div>

          {/* Processing Settings */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Sliders className="w-5 h-5 text-accent-400" />
              <h3 className="text-lg font-semibold">Processing Settings</h3>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Complexity Level</label>
                <input
                  type="range"
                  min="1"
                  max="10"
                  defaultValue="5"
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Simple</span>
                  <span>Complex</span>
                </div>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">Cache Size (MB)</label>
                <input
                  type="number"
                  defaultValue="64"
                  min="16"
                  max="512"
                  className="input-field w-full"
                />
              </div>
            </div>
          </div>

          {/* Cultural Settings */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Globe className="w-5 h-5 text-green-400" />
              <h3 className="text-lg font-semibold">Cultural Context</h3>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Default Cultural Style</label>
              <select className="input-field w-full">
                <option value="western">Western (Major Scale)</option>
                <option value="eastern">Eastern (Pentatonic)</option>
                <option value="african">African Scale</option>
                <option value="latin">Latin Scale</option>
              </select>
            </div>
          </div>

          {/* Appearance Settings */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Palette className="w-5 h-5 text-purple-400" />
              <h3 className="text-lg font-semibold">Appearance</h3>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Dark Mode</span>
                <button className="w-12 h-6 bg-primary-500 rounded-full relative">
                  <span className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full" />
                </button>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Animations</span>
                <button className="w-12 h-6 bg-primary-500 rounded-full relative">
                  <span className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full" />
                </button>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <button className="glow-button w-full">
            Save Settings
          </button>
        </div>
      </div>
    </div>
  )
}

export default SettingsPanel
