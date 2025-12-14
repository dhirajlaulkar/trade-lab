'use client';

import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, Activity, BarChart3, Settings } from 'lucide-react';

export default function Home() {
  const [symbol, setSymbol] = useState('SPY');
  const [strategy, setStrategy] = useState('momentum');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState('');
  const [summary, setSummary] = useState('');
  const [summaryLoading, setSummaryLoading] = useState(false);

  const runBacktest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setData(null);
    setSummary('');

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

  const generateSummary = async () => {
    if (!data) return;
    setSummaryLoading(true);
    try {
      const res = await fetch('/api/ai_summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          metrics: data.metrics,
          strategy: strategy,
          symbol: symbol
        }),
      });
      const resData = await res.json();
      setSummary(resData.summary);
    } catch (err) {
      console.error(err);
      setSummary('Failed to generate summary.');
    } finally {
      setSummaryLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f0f0f0] text-black font-mono p-8 relative">
      <div className="max-w-5xl mx-auto space-y-12">
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-center border-b-4 border-black pb-6 gap-4">
          <div>
            <h1 className="text-5xl md:text-6xl font-black bg-yellow-300 border-2 border-black px-4 py-2 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] inline-block transform -rotate-1">
              TradeLab
            </h1>
            <p className="mt-4 text-lg font-bold text-gray-700">
              /// INSTITUTIONAL GRADE BACKTESTING
            </p>
          </div>
          <div className="flex gap-2">
            <div className="p-3 bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all cursor-pointer">
              <Activity className="w-6 h-6" />
            </div>
            <div className="p-3 bg-blue-300 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all cursor-pointer">
              <Settings className="w-6 h-6" />
            </div>
          </div>
        </header>

        {/* Control Panel */}
        <div className="bg-white border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
          <h2 className="text-2xl font-black mb-6 flex items-center gap-2">
            <BarChart3 className="w-8 h-8" /> CONFIGURATION
          </h2>
          <form onSubmit={runBacktest} className="flex gap-6 flex-wrap items-end">
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-bold mb-2 uppercase tracking-wide">Ticker Symbol</label>
              <input
                type="text"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                className="w-full bg-gray-50 border-2 border-black px-4 py-3 font-bold focus:ring-0 focus:bg-yellow-100 focus:outline-none shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
                placeholder="e.g. SPY"
              />
            </div>

            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-bold mb-2 uppercase tracking-wide">Strategy Model</label>
              <select
                value={strategy}
                onChange={(e) => setStrategy(e.target.value)}
                className="w-full bg-gray-50 border-2 border-black px-4 py-3 font-bold focus:ring-0 focus:bg-yellow-100 focus:outline-none shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] appearance-none"
              >
                <option value="momentum">Momentum (Crossover)</option>
                <option value="mean_reversion">Mean Reversion (Z-Score)</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="bg-black text-white hover:bg-gray-800 px-8 py-3.5 border-2 border-black font-bold shadow-[4px_4px_0px_0px_rgba(128,128,128,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all disabled:opacity-50 disabled:cursor-not-allowed h-[52px] min-w-[150px]"
            >
              {loading ? 'RUNNING...' : 'EXECUTE >>'}
            </button>
          </form>
          {error && (
            <div className="mt-6 p-4 bg-red-100 border-2 border-black text-red-700 font-bold flex items-center gap-2">
              <span> ERROR:</span> {error}
            </div>
          )}
        </div>

        {/* Results */}
        {data && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500">
            {/* Metrics Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {Object.entries(data.metrics).map(([key, value]) => (
                <div key={key} className="bg-purple-100 border-4 border-black p-4 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 transition-transform">
                  <p className="text-xs font-black uppercase tracking-widest mb-2 border-b-2 border-black pb-1">{key}</p>
                  <p className="text-2xl md:text-3xl font-bold mt-1 text-black">{String(value)}</p>
                </div>
              ))}
            </div>

            {/* Chart */}
            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] h-[500px] relative">
              <div className="absolute -top-4 -left-4 bg-green-400 border-2 border-black px-4 py-1 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] z-10">
                <h3 className="text-lg font-black flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" /> EQUITY CURVE
                </h3>
              </div>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.chart_data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
                  <XAxis
                    dataKey="Date"
                    stroke="#000"
                    tick={{ fontSize: 12, fontWeight: 'bold' }}
                    tickFormatter={(str) => new Date(str).toLocaleDateString()}
                    tickMargin={10}
                  />
                  <YAxis stroke="#000" tick={{ fontSize: 12, fontWeight: 'bold' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '2px solid #000',
                      boxShadow: '4px 4px 0px 0px rgba(0,0,0,1)',
                      fontWeight: 'bold'
                    }}
                    itemStyle={{ color: '#000' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="Equity_Curve"
                    stroke="#000"
                    strokeWidth={3}
                    dot={false}
                    activeDot={{ r: 6, strokeWidth: 2, fill: '#fff', stroke: '#000' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* AI Summary Section */}
            <div className="bg-yellow-100 border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-4xl font-black flex items-center gap-2">
                  AI ANALYST
                </h3>
                <button
                  onClick={generateSummary}
                  disabled={summaryLoading}
                  className="bg-black text-white px-4 py-2 font-bold border-2 border-transparent hover:bg-gray-800 disabled:opacity-50"
                >
                  {summaryLoading ? 'ANALYZING...' : 'GENERATE INSIGHTS'}
                </button>
              </div>
              {summary && (
                <div className="bg-white border-2 border-black p-4 font-mono text-sm leading-relaxed whitespace-pre-wrap">
                  {summary}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
