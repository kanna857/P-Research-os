"use client";

import React, { useState } from "react";
import { LineChart, CheckCircle2, AlertTriangle, ArrowRight, Play, RefreshCw, BarChart2 } from "lucide-react";

export default function StatisticsPage() {
  const [groupA, setGroupA] = useState("0.81, 0.83, 0.82, 0.80, 0.84, 0.82, 0.81, 0.83");
  const [groupB, setGroupB] = useState("0.88, 0.90, 0.89, 0.88, 0.91, 0.89, 0.90, 0.88");
  const [nameA, setNameA] = useState("Baseline Standard");
  const [nameB, setNameB] = useState("Proposed Method");
  const [paired, setPaired] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleRunAnalysis = async () => {
    setLoading(true);
    try {
      const parsedA = groupA.split(",").map((s) => parseFloat(s.trim())).filter((n) => !isNaN(n));
      const parsedB = groupB.split(",").map((s) => parseFloat(s.trim())).filter((n) => !isNaN(n));

      const res = await fetch("http://localhost:8000/api/universal/statistical-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          group_a: parsedA,
          group_b: parsedB,
          group_names: [nameA, nameB],
          paired: paired,
        }),
      });

      if (res.ok) {
        setResult(await res.json());
      }
    } catch (err) {
      console.error("Stats analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-600 text-white shadow-lg shadow-teal-500/20">
            <LineChart className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Universal Statistical Analysis Studio</h1>
            <p className="text-sm text-slate-400">Hypothesis testing, assumption diagnostics, effect sizes & confidence intervals</p>
          </div>
        </div>

        <button
          onClick={handleRunAnalysis}
          disabled={loading}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-bold text-sm shadow-lg shadow-teal-600/30 transition-all disabled:opacity-50"
        >
          <Play className={`w-4 h-4 fill-white ${loading ? "animate-spin" : ""}`} />
          {loading ? "Calculating..." : "Run Statistical Test"}
        </button>
      </div>

      {/* Input Form */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900/60 border border-white/10 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-300">Group A (Control / Baseline)</label>
            <input
              type="text"
              value={nameA}
              onChange={(e) => setNameA(e.target.value)}
              className="bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-cyan-300 font-mono"
            />
          </div>
          <textarea
            value={groupA}
            onChange={(e) => setGroupA(e.target.value)}
            rows={3}
            className="w-full bg-slate-950 border border-white/10 rounded-lg p-3 text-xs font-mono text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            placeholder="Comma-separated numbers e.g. 0.81, 0.83, 0.82..."
          />
        </div>

        <div className="bg-slate-900/60 border border-white/10 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-300">Group B (Treatment / Proposed)</label>
            <input
              type="text"
              value={nameB}
              onChange={(e) => setNameB(e.target.value)}
              className="bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-emerald-300 font-mono"
            />
          </div>
          <textarea
            value={groupB}
            onChange={(e) => setGroupB(e.target.value)}
            rows={3}
            className="w-full bg-slate-950 border border-white/10 rounded-lg p-3 text-xs font-mono text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            placeholder="Comma-separated numbers e.g. 0.88, 0.90, 0.89..."
          />
        </div>
      </div>

      {/* Results View */}
      {result && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Test Selected</span>
              <div className="text-sm font-bold text-white mt-1">{result.test_selected}</div>
              <span className="text-xs text-slate-500 mt-1 block">Stat: {result.test_statistic}</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">p-value</span>
              <div className={`text-2xl font-extrabold mt-1 ${result.is_statistically_significant ? "text-emerald-400" : "text-slate-400"}`}>
                p = {result.p_value}
              </div>
              <span className="text-xs text-slate-500 mt-1 block">{result.is_statistically_significant ? "Significant (p < 0.05)" : "Not Significant"}</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Effect Size</span>
              <div className="text-2xl font-extrabold text-cyan-400 mt-1">{result.effect_size?.value}</div>
              <span className="text-xs text-slate-500 mt-1 block">{result.effect_size?.interpretation}</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Normality Check</span>
              <div className="text-sm font-bold text-emerald-300 mt-1">{result.assumption_diagnostics?.normality_assumption}</div>
              <span className="text-xs text-slate-500 mt-1 block">{result.assumption_diagnostics?.equal_variance_assumption}</span>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-emerald-400" />
              Scientific Inference & Conclusion
            </h3>
            <p className="text-xs text-slate-200 leading-relaxed bg-slate-950 p-3 rounded-lg border border-white/5 font-mono">
              {result.scientific_conclusion}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
