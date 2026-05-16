'use client'

import { useEffect, useState } from 'react'

interface Threat {
  ip: string
  threat_score: number
  severity: string
  failed_ratio: number
  total_requests: number
  is_threat: boolean
  explanation: string
}

interface Stats {
  total_logs: number
  suspected_attacks: number
  normal_traffic: number
}

export default function Dashboard() {
  const [threats, setThreats] = useState<Threat[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [threatsRes, statsRes] = await Promise.all([
        fetch('http://localhost:8000/threats'),
        fetch('http://localhost:8000/stats')
      ])
      const threatsData = await threatsRes.json()
      const statsData = await statsRes.json()
      setThreats(threatsData.threats)
      setStats(statsData)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    // Har 30 sec mein auto refresh
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-600 text-white'
      case 'HIGH': return 'bg-orange-500 text-white'
      case 'MEDIUM': return 'bg-yellow-500 text-black'
      default: return 'bg-green-500 text-white'
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-red-500'
    if (score >= 70) return 'text-orange-500'
    if (score >= 40) return 'text-yellow-500'
    return 'text-green-500'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-red-500 mx-auto mb-4"></div>
          <p className="text-gray-400 text-lg">Loading threat data...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
          <h1 className="text-3xl font-bold text-white">
            AI Threat Detection Dashboard
          </h1>
        </div>
        <p className="text-gray-400 ml-6">Real-time security monitoring powered by ML + AI</p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <p className="text-gray-400 text-sm mb-1">Total Logs</p>
            <p className="text-3xl font-bold text-white">{stats.total_logs.toLocaleString()}</p>
            <p className="text-gray-500 text-xs mt-1">All time</p>
          </div>
          <div className="bg-gray-900 border border-red-900 rounded-xl p-5">
            <p className="text-gray-400 text-sm mb-1">Suspected Attacks</p>
            <p className="text-3xl font-bold text-red-500">{stats.suspected_attacks.toLocaleString()}</p>
            <p className="text-gray-500 text-xs mt-1">Failed login attempts</p>
          </div>
          <div className="bg-gray-900 border border-green-900 rounded-xl p-5">
            <p className="text-gray-400 text-sm mb-1">Normal Traffic</p>
            <p className="text-3xl font-bold text-green-500">{stats.normal_traffic.toLocaleString()}</p>
            <p className="text-gray-500 text-xs mt-1">Safe requests</p>
          </div>
        </div>
      )}

      {/* Threats Section */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold text-white">
          Active Threats
          <span className="ml-2 bg-red-600 text-white text-xs px-2 py-1 rounded-full">
            {threats.filter(t => t.is_threat).length}
          </span>
        </h2>
        <button
          onClick={fetchData}
          className="bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm px-4 py-2 rounded-lg transition"
        >
          Refresh
        </button>
      </div>

      {/* Threat Cards */}
      <div className="space-y-4">
        {threats.map((threat, index) => (
          <div
            key={index}
            className={`bg-gray-900 border rounded-xl p-5 ${
              threat.is_threat ? 'border-red-900' : 'border-gray-800'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${threat.is_threat ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`}></div>
                <span className="font-mono text-lg font-semibold text-white">{threat.ip}</span>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${getSeverityColor(threat.severity)}`}>
                  {threat.severity}
                </span>
              </div>
              <div className="text-right">
                <span className={`text-2xl font-bold ${getScoreColor(threat.threat_score)}`}>
                  {threat.threat_score}
                </span>
                <span className="text-gray-500 text-sm">/100</span>
              </div>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-3 gap-3 mb-3">
              <div className="bg-gray-800 rounded-lg p-2 text-center">
                <p className="text-xs text-gray-400">Failed Ratio</p>
                <p className={`font-semibold ${threat.failed_ratio > 0.5 ? 'text-red-400' : 'text-green-400'}`}>
                  {(threat.failed_ratio * 100).toFixed(0)}%
                </p>
              </div>
              <div className="bg-gray-800 rounded-lg p-2 text-center">
                <p className="text-xs text-gray-400">Total Requests</p>
                <p className="font-semibold text-white">{threat.total_requests}</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-2 text-center">
                <p className="text-xs text-gray-400">Threat</p>
                <p className={`font-semibold ${threat.is_threat ? 'text-red-400' : 'text-green-400'}`}>
                  {threat.is_threat ? 'YES' : 'NO'}
                </p>
              </div>
            </div>

            {/* AI Explanation */}
            {threat.explanation && (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                <p className="text-xs text-gray-400 mb-1">🤖 AI Analysis</p>
                <p className="text-sm text-gray-300 leading-relaxed">{threat.explanation}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-8 text-center text-gray-600 text-sm">
        Auto-refreshes every 30 seconds • Powered by ML + Groq AI
      </div>
    </main>
  )
}