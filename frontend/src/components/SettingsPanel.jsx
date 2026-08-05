import { X, Volume2, Sliders, Globe, Palette, Settings, Zap, Cpu, Eye } from 'lucide-react'

function SettingsPanel({ onClose }) {
  return (
    <div className="fixed inset-0 bg-void-900/90 backdrop-blur-glass flex items-center justify-center z-50 p-4">
      <div className="glass-card rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-glass-border">
          <div className="flex items-center gap-3">
            <Settings className="w-6 h-6 text-neon-cyan" />
            <h2 className="text-2xl font-bold neon-text-cyan">COMMAND PARAMETERS</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-neon-cyan transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-8">
          {/* Audio Settings */}
          <div>
            <h3 className="text-lg font-semibold text-neon-cyan mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5" />
              AUDIO CONFIGURATION
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Sample Rate</label>
                <select className="input-field w-full rounded-lg p-3">
                  <option>44100 Hz</option>
                  <option>48000 Hz</option>
                  <option>96000 Hz</option>
                </select>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">Bit Depth</label>
                <select className="input-field w-full rounded-lg p-3">
                  <option>16-bit</option>
                  <option>24-bit</option>
                  <option>32-bit</option>
                </select>
              </div>
            </div>
          </div>

          {/* Processing Settings */}
          <div>
            <h3 className="text-lg font-semibold text-neon-purple mb-4 flex items-center gap-2">
              <Cpu className="w-5 h-5" />
              PROCESSING PARAMETERS
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Complexity Level</label>
                <select className="input-field w-full rounded-lg p-3">
                  <option>Low</option>
                  <option>Medium</option>
                  <option>High</option>
                  <option>Maximum</option>
                </select>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">Cache Size (MB)</label>
                <input
                  type="number"
                  defaultValue="64"
                  className="input-field w-full rounded-lg p-3"
                />
              </div>
            </div>
          </div>

          {/* Cultural Context */}
          <div>
            <h3 className="text-lg font-semibold text-neon-green mb-4 flex items-center gap-2">
              <Globe className="w-5 h-5" />
              CULTURAL CONTEXT
            </h3>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Cultural Style</label>
              <select className="input-field w-full rounded-lg p-3">
                <option>Western Classical</option>
                <option>Eastern Traditional</option>
                <option>Contemporary</option>
                <option>Experimental</option>
              </select>
            </div>
          </div>

          {/* Appearance */}
          <div>
            <h3 className="text-lg font-semibold text-neon-cyan mb-4 flex items-center gap-2">
              <Eye className="w-5 h-5" />
              INTERFACE CONFIGURATION
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Dark Mode</span>
                <div className="w-12 h-6 bg-neon-cyan/20 rounded-full relative cursor-pointer">
                  <div className="absolute right-1 top-1 w-4 h-4 bg-neon-cyan rounded-full"></div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Animations</span>
                <div className="w-12 h-6 bg-neon-cyan/20 rounded-full relative cursor-pointer">
                  <div className="absolute right-1 top-1 w-4 h-4 bg-neon-cyan rounded-full"></div>
                </div>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <button className="glow-button w-full py-3 rounded-xl font-semibold">
            SAVE CONFIGURATION
          </button>
        </div>
      </div>
    </div>
  )
}

export default SettingsPanel
