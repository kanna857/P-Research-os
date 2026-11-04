"use client";

import React, { useState } from "react";
import { Cpu, Play, CheckCircle2, RefreshCw, Layers, ShieldAlert } from "lucide-react";

export default function SimulationStudioPage() {
  const [lengthMeters, setLengthMeters] = useState(0.10);
  const [alpha, setAlpha] = useState(1.2e-4);
  const [leftTemp, setLeftTemp] = useState(180.0);
  const [rightTemp, setRightTemp] = useState(25.0);
  const [initialTemp, setInitialTemp] = useState(25.0);
  const [duration, setDuration] = useState(20.0);
  const [loading, setLoading] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/universal/run-simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          length_meters: lengthMeters,
          thermal_diffusivity_alpha: alpha,
          initial_temp_celsius: initialTemp,
          boundary_temp_left: leftTemp,
          boundary_temp_right: rightTemp,
          simulation_time_seconds: duration,
        }),
      });
      if (res.ok) {
        setSimResult(await res.json());
      }
    } catch (err) {
      console.error("Simulation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Scientific Simulation Studio</h1>
            <p className="text-sm text-slate-400">Numerical PDE solvers, finite difference modeling & CFL stability verification</p>
          </div>
        </div>

        <button
          onClick={handleRunSimulation}
          disabled={loading}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-sm shadow-lg shadow-cyan-500/30 transition-all disabled:opacity-50"
        >
          <Play className={`w-4 h-4 fill-white ${loading ? "animate-spin" : ""}`} />
          {loading ? "Simulating..." : "Execute Simulation"}
        </button>
      </div>

      {/* Parameter Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-3">
          <label className="text-[11px] text-slate-400 block">Length (m)</label>
          <input
            type="number"
            step="0.01"
            value={lengthMeters}
            onChange={(e) => setLengthMeters(parseFloat(e.target.value))}
            className="w-full bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-white font-mono mt-1"
          />
        </div>
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-3">
          <label className="text-[11px] text-slate-400 block">Alpha (m²/s)</label>
          <input
            type="number"
            step="0.00001"
            value={alpha}
            onChange={(e) => setAlpha(parseFloat(e.target.value))}
            className="w-full bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-white font-mono mt-1"
          />
        </div>
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-3">
          <label className="text-[11px] text-slate-400 block">Left Temp (°C)</label>
          <input
            type="number"
            value={leftTemp}
            onChange={(e) => setLeftTemp(parseFloat(e.target.value))}
            className="w-full bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-amber-400 font-mono mt-1"
          />
        </div>
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-3">
          <label className="text-[11px] text-slate-400 block">Right Temp (°C)</label>
          <input
            type="number"
            value={rightTemp}
            onChange={(e) => setRightTemp(parseFloat(e.target.value))}
            className="w-full bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-cyan-400 font-mono mt-1"
          />
        </div>
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-3">
          <label className="text-[11px] text-slate-400 block">Initial Temp (°C)</label>
          <input
            type="number"
            value={initialTemp}
            onChange={(e) => setInitialTemp(parseFloat(e.target.value))}
            className="w-full bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-white font-mono mt-1"
          />
        </div>
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-3">
          <label className="text-[11px] text-slate-400 block">Duration (s)</label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(parseFloat(e.target.value))}
            className="w-full bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-emerald-400 font-mono mt-1"
          />
        </div>
      </div>

      {/* Simulation Results */}
      {simResult && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Governing PDE</span>
              <div className="text-xs font-mono font-bold text-cyan-400 mt-1">{simResult.governing_pde}</div>
              <span className="text-xs text-slate-500 mt-1 block">1D Heat Conduction</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Stability (CFL)</span>
              <div className="text-sm font-bold text-emerald-400 mt-1">{simResult.parameters?.numerical_stability}</div>
              <span className="text-xs text-slate-500 mt-1 block">r = {simResult.parameters?.cfl_number}</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Max Temperature</span>
              <div className="text-2xl font-extrabold text-amber-400 mt-1">{simResult.summary_metrics?.maximum_temperature_celsius}°C</div>
              <span className="text-xs text-slate-500 mt-1 block">Mean: {simResult.summary_metrics?.mean_temperature_celsius}°C</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Spatial Points</span>
              <div className="text-2xl font-extrabold text-purple-400 mt-1">{simResult.spatial_profile?.temperatures_celsius?.length * 3}</div>
              <span className="text-xs text-slate-500 mt-1 block">dx = {simResult.parameters?.spatial_discretization_dx}m</span>
            </div>
          </div>

          {/* Spatial Temperature Profile Bar Grid */}
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-white flex items-center justify-between">
              <span>Spatial Temperature Gradient Along Specimen Axis (x = 0 to L)</span>
              <span className="text-xs font-mono text-cyan-400">t = {duration}s</span>
            </h3>

            <div className="grid grid-cols-6 sm:grid-cols-9 md:grid-cols-17 gap-1 pt-2">
              {simResult.spatial_profile?.temperatures_celsius?.map((temp: number, idx: number) => {
                const heightPercent = Math.max(10, Math.min(100, (temp / leftTemp) * 100));
                return (
                  <div key={idx} className="flex flex-col items-center gap-1">
                    <div className="w-full bg-slate-950 h-28 rounded flex flex-col justify-end p-0.5">
                      <div
                        className="w-full rounded bg-gradient-to-t from-cyan-500 to-amber-500 transition-all duration-300"
                        style={{ height: `${heightPercent}%` }}
                      />
                    </div>
                    <span className="text-[10px] font-mono text-slate-400">{temp.toFixed(0)}°</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
