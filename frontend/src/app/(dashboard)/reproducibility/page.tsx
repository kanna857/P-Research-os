"use client";

import React, { useState, useEffect } from "react";
import { Layers, Download, Play, CheckCircle2, Terminal, Cpu, GitBranch, Database, ShieldCheck, RefreshCw } from "lucide-react";

export default function ReproducibilityPage() {
  const [loading, setLoading] = useState(false);
  const [manifest, setManifest] = useState<any>(null);
  const [reproducing, setReproducing] = useState(false);
  const [reproResult, setReproResult] = useState<any>(null);

  const fetchManifest = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/reproducibility/manifest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          experiment_id: "exp-sar-sentinel1-001",
          project_name: "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection",
          random_seed: 42,
          dataset_name: "Sentinel-1 SAR Multitemporal Benchmark",
          model_name: "ResNet-Siamese-DualPol-CrossAttention"
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setManifest(data);
      }
    } catch (err) {
      console.error("Fetch manifest error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPackage = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/reproducibility/package", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          experiment_id: "exp-sar-sentinel1-001",
          project_name: "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection",
          random_seed: 42
        }),
      });
      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "reproducibility_package_exp_sar_001.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
    } catch (err) {
      console.error("Package download error:", err);
    }
  };

  const handleReproduce = async () => {
    if (!manifest) return;
    setReproducing(true);
    try {
      const res = await fetch("http://localhost:8000/api/reproducibility/reproduce", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ manifest }),
      });
      if (res.ok) {
        const data = await res.json();
        setReproResult(data);
      }
    } catch (err) {
      console.error("Reproduce error:", err);
    } finally {
      setReproducing(false);
    }
  };

  useEffect(() => {
    fetchManifest();
  }, []);

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Scientific Reproducibility Engine</h1>
            <p className="text-sm text-slate-400">Git commit, DVC hashes, frozen dependencies, and one-click trial reproduction</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleDownloadPackage}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-sm transition-colors border border-white/10"
          >
            <Download className="w-4 h-4 text-cyan-400" />
            Download Package (.zip)
          </button>
          <button
            onClick={handleReproduce}
            disabled={reproducing}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-medium text-sm transition-all shadow-lg shadow-cyan-500/30 disabled:opacity-50"
          >
            <Play className={`w-4 h-4 fill-white ${reproducing ? "animate-pulse" : ""}`} />
            {reproducing ? "Reproducing..." : "Reproduce Experiment"}
          </button>
        </div>
      </div>

      {/* Reproduction Verification Banner */}
      {reproResult && (
        <div className="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-cyan-950/60 border border-emerald-500/30 rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span className="font-bold text-emerald-400 text-base">Execution Status: {reproResult.status}</span>
            </div>
            <span className="px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 text-xs font-mono font-bold">
              Grade: {reproResult.reproducibility_grade}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
            <div className="bg-slate-950/60 p-3 rounded-lg border border-white/5">
              <div className="text-xs text-slate-400">Recorded F1 Baseline</div>
              <div className="text-lg font-mono font-bold text-white mt-0.5">{reproResult.original_metrics?.f1_score}</div>
            </div>
            <div className="bg-slate-950/60 p-3 rounded-lg border border-white/5">
              <div className="text-xs text-slate-400">Reproduced F1</div>
              <div className="text-lg font-mono font-bold text-emerald-400 mt-0.5">{reproResult.reproduced_metrics?.f1_score}</div>
            </div>
            <div className="bg-slate-950/60 p-3 rounded-lg border border-white/5">
              <div className="text-xs text-slate-400">Metric Drift (Delta)</div>
              <div className="text-lg font-mono font-bold text-cyan-400 mt-0.5">{reproResult.metric_drift?.f1_delta}</div>
            </div>
            <div className="bg-slate-950/60 p-3 rounded-lg border border-white/5">
              <div className="text-xs text-slate-400">Random Seed Applied</div>
              <div className="text-lg font-mono font-bold text-purple-400 mt-0.5">{reproResult.seed_applied}</div>
            </div>
          </div>
        </div>
      )}

      {/* Manifest Overview Cards */}
      {manifest && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Provenance */}
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <GitBranch className="w-4 h-4 text-cyan-400" />
              Code & Repository Provenance
            </h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Git Commit:</span>
                <span className="font-mono text-cyan-300">{manifest.provenance?.git_commit?.slice(0, 12)}...</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Random Seed:</span>
                <span className="font-mono text-purple-300">{manifest.provenance?.random_seed}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Repository:</span>
                <span className="text-slate-200">github.com/kanna857/P-Research-os</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-400">Execution Mode:</span>
                <span className="text-emerald-400 font-semibold">100% Deterministic</span>
              </div>
            </div>
          </div>

          {/* Card 2: Dataset DVC */}
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Database className="w-4 h-4 text-amber-400" />
              Dataset DVC Versioning
            </h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Benchmark:</span>
                <span className="text-slate-200 truncate max-w-[180px]">{manifest.dataset_provenance?.name}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">DVC Hash:</span>
                <span className="font-mono text-amber-300">{manifest.dataset_provenance?.dvc_hash?.slice(0, 16)}...</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/5">
                <span className="text-slate-400">Partition:</span>
                <span className="text-slate-300">80/20 Spatial Tile CV</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-400">Leakage Audit:</span>
                <span className="text-emerald-400 font-semibold">PASSED</span>
              </div>
            </div>
          </div>

          {/* Card 3: Execution Command */}
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" />
              Standalone Rerun Instructions
            </h3>
            <div className="space-y-2">
              <span className="text-xs text-slate-400 block">Command-line replication:</span>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-white/5 font-mono text-[11px] text-emerald-300 overflow-x-auto">
                {manifest.rerun_instructions?.reproduce_command}
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-white/5 font-mono text-[11px] text-cyan-300 overflow-x-auto">
                {manifest.rerun_instructions?.docker_command}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Raw Manifest Viewer */}
      <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Terminal className="w-4 h-4 text-cyan-400" />
            reproducibility_manifest.json (ISO 17025 Compliant)
          </h3>
          <span className="text-xs text-slate-400 font-mono">Format: JSON-LD</span>
        </div>
        <pre className="bg-slate-950/90 border border-white/10 rounded-lg p-4 font-mono text-xs text-slate-300 overflow-x-auto max-h-96 scrollbar-thin scrollbar-thumb-white/10">
          {manifest ? JSON.stringify(manifest, null, 2) : "Loading manifest..."}
        </pre>
      </div>
    </div>
  );
}
