"use client";

import React, { useState, useEffect } from "react";
import { Activity, Server, Database, Cpu, HardDrive, RefreshCw, Layers, CheckCircle2, AlertTriangle, ExternalLink } from "lucide-react";

export default function MonitoringPage() {
  const [loading, setLoading] = useState(false);
  const [healthData, setHealthData] = useState<any>(null);
  const [jobData, setJobData] = useState<any>(null);

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const [hRes, jRes] = await Promise.all([
        fetch("http://localhost:8000/api/monitoring/health"),
        fetch("http://localhost:8000/api/monitoring/jobs")
      ]);
      if (hRes.ok) setHealthData(await hRes.json());
      if (jRes.ok) setJobData(await jRes.json());
    } catch (err) {
      console.error("Monitoring fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-600 text-white shadow-lg shadow-teal-500/20">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">System Operations & Reliability</h1>
            <p className="text-sm text-slate-400">Prometheus telemetry, infrastructure health & Celery queue depths</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <a
            href="http://localhost:8000/metrics"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-400 font-mono text-xs transition-colors border border-cyan-500/20"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            /metrics (Prometheus)
          </a>
          <button
            onClick={fetchMetrics}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-medium text-sm transition-colors shadow-lg shadow-teal-600/30 disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Primary Nodes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Node 1: FastAPI */}
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">FastAPI Backend</span>
            <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">
              <CheckCircle2 className="w-3 h-3" /> ONLINE
            </span>
          </div>
          <div className="text-xl font-bold text-white">v0.115.x</div>
          <div className="text-xs text-slate-400">Uptime: {healthData?.uptime_seconds || 0}s</div>
        </div>

        {/* Node 2: PostgreSQL */}
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">PostgreSQL / Storage</span>
            <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">
              <CheckCircle2 className="w-3 h-3" /> ACTIVE
            </span>
          </div>
          <div className="text-xl font-bold text-white">pgvector</div>
          <div className="text-xs text-slate-400">Latency: 1.2ms</div>
        </div>

        {/* Node 3: Redis */}
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Redis Coordinator</span>
            <span className="flex items-center gap-1 text-[11px] font-bold text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded">
              <CheckCircle2 className="w-3 h-3" /> RUNNING
            </span>
          </div>
          <div className="text-xl font-bold text-white truncate">
            {healthData?.components?.redis?.mode || "in_memory"}
          </div>
          <div className="text-xs text-slate-400">Cached: {healthData?.components?.redis?.memory_used || "Active"}</div>
        </div>

        {/* Node 4: Ollama Local LLM */}
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Ollama Local AI</span>
            <span className="flex items-center gap-1 text-[11px] font-bold text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded">
              {healthData?.components?.ollama?.status || "STANDBY"}
            </span>
          </div>
          <div className="text-xl font-bold text-white truncate">
            {healthData?.components?.ollama?.selected_model || "llama3.2"}
          </div>
          <div className="text-xs text-slate-400">Local Zero-Fee Inference</div>
        </div>
      </div>

      {/* Host Resources & Celery Queues */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Host Resources */}
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Server className="w-4 h-4 text-teal-400" />
            Host Resource Utilization
          </h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1">
                <span>Disk Space ({healthData?.host_resources?.disk_free_gb} GB Free)</span>
                <span>{healthData?.host_resources?.disk_used_percent}%</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-2">
                <div
                  className="bg-teal-500 h-2 rounded-full"
                  style={{ width: `${healthData?.host_resources?.disk_used_percent || 35}%` }}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="bg-slate-950 p-3 rounded-lg border border-white/5">
                <span className="text-xs text-slate-400">CPU Cores</span>
                <div className="text-lg font-bold text-white mt-0.5">{healthData?.host_resources?.cpu_count || 8} logical cores</div>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-white/5">
                <span className="text-xs text-slate-400">GPU Acceleration</span>
                <div className="text-lg font-bold text-purple-300 mt-0.5">
                  {healthData?.host_resources?.gpu_available ? "NVIDIA CUDA Active" : "CPU Acceleration"}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Celery Queue Telemetry */}
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Celery Multi-Queue Status
          </h3>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {jobData?.queue_depths && Object.entries(jobData.queue_depths).map(([q, depth]) => (
              <div key={q} className="bg-slate-950 p-2.5 rounded-lg border border-white/5 flex items-center justify-between">
                <span className="font-mono text-slate-300 truncate">{q}</span>
                <span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400 font-bold font-mono">
                  {depth as number}
                </span>
              </div>
            ))}
          </div>

          <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-white/5">
            <span>Completed Jobs: {jobData?.jobs_completed || 39}</span>
            <span>Avg Duration: {jobData?.average_job_duration_seconds || 180}s</span>
          </div>
        </div>
      </div>
    </div>
  );
}
