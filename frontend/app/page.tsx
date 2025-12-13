'use client';

import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Home() {
  const [symbol, setSymbol] = useState('SPY');
  const [strategy, setStrategy] = useState('momentum');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState('');

  const runBacktest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setData(null);

    try {
      const res = await fetch('/api/run_backtest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, strategy }),
      });

      if (!res.ok) throw new Error('Failed to run backtest');
      const result = await res.json();
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="text-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            TradeLab Analytics
          </h1>
          <p className="text-gray-400 mt-2">Institutional-grade Backtesting Platform</p>
        </header>

        {/* Control Panel */}
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <form onSubmit={runBacktest} className="flex gap-4 flex-wrap items-end">
            <div>
              <label className="block text-sm font-medium mb-1 text-gray-300">Symbol</label>
              <input
                type="text"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                className="bg-gray-900 border border-gray-600 rounded px-3 py-2 w-32 focus:ring-2 focus:ring-blue-500 outline-none uppercase"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-300">Strategy</label>
              <select
                value={strategy}
                onChange={(e) => setStrategy(e.target.value)}
                className="bg-gray-900 border border-gray-600 rounded px-3 py-2 w-48 focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="momentum">Momentum (Crossover)</option>
                <option value="mean_reversion">Mean Reversion (Z-Score)</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed h-[42px]"
            >
              {loading ? 'Running...' : 'Run Backtest'}
            </button>
          </form>
          {error && <p className="text-red-400 mt-4 text-sm">{error}</p>}
        </div>

        {/* Results */}
        {data && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Metrics Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(data.metrics).map(([key, value]) => (
                <div key={key} className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                  <p className="text-xs text-gray-400 uppercase tracking-wider">{key}</p>
                  <p className="text-xl font-bold mt-1">{String(value)}</p>
                </div>
              ))}
            </div>

            {/* Chart */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 h-[400px]">
              <h3 className="text-lg font-medium mb-4">Equity Curve</h3>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.chart_data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis
                    dataKey="Date"
                    stroke="#9CA3AF"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(str) => new Date(str).toLocaleDateString()}
                  />
                  <YAxis stroke="#9CA3AF" tick={{ fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="Equity_Curve"
                    stroke="#8B5CF6"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
