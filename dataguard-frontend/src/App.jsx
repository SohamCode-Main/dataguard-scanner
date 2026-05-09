import { useState, useEffect } from 'react'

export default function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/history')
      const data = await res.json()
      setHistory(data.history)
    } catch (err) { console.error("History offline") }
  }

  const runAudit = async () => {
    setLoading(true)
    try {
      const res = await fetch(`http://127.0.0.1:8000/audit?url=${url}`)
      const data = await res.json()
      setResult(data)
      fetchHistory()
    } catch (err) { alert("Backend offline") }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-[#F9F9F9] text-zinc-900 font-sans p-6 md:p-12 selection:bg-zinc-900 selection:text-white">
      <div className="max-w-6xl mx-auto">
        
        {/* Minimalist Header */}
        <header className="mb-16 pb-8 border-b border-zinc-200 flex justify-between items-end">
          <div>
            <h1 className="text-5xl font-medium tracking-tighter text-zinc-900">DataGuard.</h1>
            <p className="text-zinc-500 text-sm tracking-wide mt-2">EU GDPR COMPLIANCE PROTOCOL</p>
          </div>
          <button onClick={() => window.print()} className="text-xs font-bold tracking-widest uppercase text-zinc-900 hover:text-zinc-500 transition-colors">
            [ Export ]
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          {/* Main Audit Area */}
          <div className="lg:col-span-8 space-y-12">
            
            {/* Input Section - Brutalist */}
            <div className="flex flex-col sm:flex-row gap-0 border border-zinc-900 bg-white shadow-[4px_4px_0px_0px_rgba(24,24,27,1)]">
              <input 
                type="text" 
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Target URL..."
                className="flex-1 bg-transparent px-6 py-4 focus:outline-none placeholder:text-zinc-400 font-mono text-sm"
              />
              <button 
                onClick={runAudit}
                disabled={loading}
                className="bg-zinc-900 text-white font-medium tracking-wide px-8 py-4 hover:bg-zinc-800 transition-colors disabled:opacity-70 border-l border-zinc-900"
              >
                {loading ? 'ANALYZING...' : 'INITIATE'}
              </button>
            </div>

            {/* Results Section */}
            {result && (
              <div className="animate-in fade-in duration-700">
                <h2 className="text-xs font-bold tracking-widest uppercase text-zinc-400 mb-6">Audit Results</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* Stark Score Gauge */}
                  <div className="bg-white border border-zinc-200 p-8 flex flex-col items-center justify-center">
                    <div className="relative w-48 h-48">
                      <svg className="w-full h-full -rotate-90">
                        <circle cx="96" cy="96" r="90" stroke="currentColor" strokeWidth="2" fill="transparent" className="text-zinc-100" />
                        <circle cx="96" cy="96" r="90" stroke="currentColor" strokeWidth="4" fill="transparent" 
                          strokeDasharray="565.48" 
                          strokeDashoffset={565.48 - (result.compliance_score / 100) * 565.48}
                          className="text-zinc-900 transition-all duration-1000 ease-out" />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-5xl font-light tracking-tighter">{result.compliance_score}</span>
                        <span className="text-[10px] font-bold tracking-widest uppercase mt-1">Index</span>
                      </div>
                    </div>
                  </div>

                  {/* Clean List Data */}
                  <div className="flex flex-col justify-center space-y-0 border-t border-l border-r border-zinc-200 bg-white">
                    <StatusRow label="HTTPS Configuration" status={result.is_secure_https} />
                    <StatusRow label="Privacy Policy" status={result.found_privacy_policy} />
                    <StatusRow label="Cookie Consent" status={result.found_cookie_notice} />
                    <div className="p-5 border-b border-zinc-200 flex justify-between items-center bg-white">
                      <span className="text-zinc-600 text-sm tracking-wide">Security Headers</span>
                      <span className="text-zinc-900 font-mono text-sm">{result.security_headers_count}/3</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar - History */}
          <div className="lg:col-span-4">
            <h2 className="text-xs font-bold tracking-widest uppercase text-zinc-400 mb-6">Log History</h2>
            <div className="border-t border-zinc-200">
              {history.map((item, idx) => (
                <div key={idx} className="py-4 border-b border-zinc-200 group hover:pl-2 transition-all duration-300">
                  <div className="flex justify-between items-center mb-1">
                    <p className="text-sm font-medium text-zinc-900 truncate pr-4">{item.url}</p>
                    <span className="text-sm font-mono text-zinc-900">
                      {item.score}
                    </span>
                  </div>
                  <p className="text-[10px] tracking-widest uppercase text-zinc-400">{item.date}</p>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* System Colophon / Signature */}
        <footer className="mt-24 pt-8 border-t border-zinc-200 flex flex-col md:flex-row justify-between items-center gap-4 text-[10px] font-bold tracking-widest uppercase text-zinc-400">
          <span>DataGuard EU © 2026 // System Operational</span>
          <span className="text-zinc-500">
            Architect: <span className="text-zinc-900">Soham Salunkhe</span>
          </span>
        </footer>

      </div>
    </div>
  )
}

function StatusRow({ label, status }) {
  return (
    <div className="p-5 border-b border-zinc-200 flex justify-between items-center bg-white">
      <span className="text-zinc-600 text-sm tracking-wide">{label}</span>
      <span className="text-[10px] font-bold tracking-widest uppercase text-zinc-900">
        {status ? 'Pass' : 'Fail'}
      </span>
    </div>
  )
}