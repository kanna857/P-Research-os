"use client";

import React, { useState } from "react";
import { Sparkles, Play, CheckCircle2, AlertTriangle, Layers, BookOpen, Activity, ArrowRight, ShieldCheck, Terminal, Compass, Network, FileText } from "lucide-react";

export default function UniversalAutopilotPage() {
  const [topic, setTopic] = useState("Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection");
  const [running, setRunning] = useState(false);
  const [autopilotData, setAutopilotData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<"logs" | "methodology" | "manuscript" | "graph">("logs");

  const sampleScenarios = [
    { title: "Remote Sensing / AI", query: "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection" },
    { title: "Biomedical Informatics", query: "Machine Learning Methods for Liver Disease Classification" },
    { title: "Physics / Materials", query: "Numerical Simulation of Heat Transfer in Composite Materials" },
    { title: "Macroeconomics", query: "Forecasting Inflation Using Economic Time-Series Data" },
    { title: "Psychology / Education", query: "Systematic Review of Digital Learning and Student Motivation" },
    { title: "Theoretical Mathematics", query: "Symbolic and Numerical Analysis of Nonlinear Differential Equations" }
  ];

  const handleStartResearch = async (selectedTopic?: string) => {
    const targetTopic = selectedTopic || topic;
    if (selectedTopic) setTopic(selectedTopic);
    setRunning(true);
    setAutopilotData(null);

    try {
      const res = await fetch("http://localhost:8000/api/universal/autopilot/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: targetTopic }),
      });
      if (res.ok) {
        const data = await res.json();
        setAutopilotData(data);
      }
    } catch (err) {
      console.error("Autopilot error:", err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-amber-500 via-rose-500 to-indigo-600 text-white shadow-lg shadow-indigo-500/20">
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              P-Research-OS Ω <span className="text-xs px-2 py-0.5 rounded-full bg-gradient-to-r from-cyan-500 to-indigo-500 text-white font-mono">UNIVERSAL AUTOPILOT</span>
            </h1>
            <p className="text-sm text-slate-400">Autonomous research lifecycle across 36 academic disciplines — Zero predefined ML forcing</p>
          </div>
        </div>
      </div>

      {/* Single Topic Input Card */}
      <div className="bg-slate-900/70 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
        <div>
          <label className="text-sm font-bold text-slate-200 block mb-2 flex items-center gap-2">
            <Compass className="w-4 h-4 text-cyan-400" />
            Enter Any Academic or Scientific Research Topic
          </label>
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="flex-1 bg-slate-950 border border-white/15 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium"
              placeholder="e.g. Numerical Simulation of Heat Transfer in Composite Materials..."
            />
            <button
              onClick={() => handleStartResearch()}
              disabled={running}
              className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 via-indigo-600 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50 min-w-[160px]"
            >
              <Play className={`w-4 h-4 fill-white ${running ? "animate-spin" : ""}`} />
              {running ? "Orchestrating..." : "Start Research"}
            </button>
          </div>
        </div>

        {/* Quick Benchmark Pills */}
        <div className="pt-2">
          <span className="text-xs font-semibold text-slate-400 block mb-2">Try Multidisciplinary Benchmark Topics:</span>
          <div className="flex flex-wrap gap-2">
            {sampleScenarios.map((s, idx) => (
              <button
                key={idx}
                onClick={() => handleStartResearch(s.query)}
                className="text-xs px-3 py-1.5 rounded-lg bg-slate-950/80 border border-white/10 hover:border-cyan-500/50 text-slate-300 hover:text-cyan-300 transition-all"
              >
                <span className="text-cyan-400 font-semibold">{s.title}:</span> {s.query.slice(0, 35)}...
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Pipeline Status Summary */}
      {autopilotData && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Discovered Domain</span>
            <div className="text-lg font-extrabold text-cyan-300 mt-1 truncate">{autopilotData.primary_domain}</div>
            <span className="text-xs text-slate-500 mt-0.5 block">Confidence: {(autopilotData.domain_classification?.classification_confidence * 100).toFixed(0)}%</span>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Scientific Methodology</span>
            <div className="text-lg font-extrabold text-emerald-400 mt-1 truncate">{autopilotData.selected_methodology}</div>
            <span className="text-xs text-slate-500 mt-0.5 block">Zero ML forcing applied</span>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Ethics & Compliance</span>
            <div className="text-lg font-extrabold text-white mt-1 flex items-center gap-1.5">
              {autopilotData.ethics_screening?.is_sensitive_research ? (
                <span className="text-amber-400 flex items-center gap-1"><AlertTriangle className="w-4 h-4" /> Sensitive</span>
              ) : (
                <span className="text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> Cleared</span>
              )}
            </div>
            <span className="text-xs text-slate-500 mt-0.5 block">Human gate enforced</span>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Manuscript Status</span>
            <div className="text-lg font-extrabold text-purple-300 mt-1 truncate">{autopilotData.manuscript?.document_type}</div>
            <span className="text-xs text-slate-500 mt-0.5 block">IEEE / Nature compile-ready</span>
          </div>
        </div>
      )}

      {/* Tabs */}
      {autopilotData && (
        <div className="space-y-4">
          <div className="flex border-b border-white/10 gap-4 text-sm font-semibold text-slate-400">
            <button
              onClick={() => setActiveTab("logs")}
              className={`pb-2.5 transition-colors ${activeTab === "logs" ? "text-cyan-400 border-b-2 border-cyan-400 font-bold" : "hover:text-white"}`}
            >
              13-Stage Execution Telemetry
            </button>
            <button
              onClick={() => setActiveTab("methodology")}
              className={`pb-2.5 transition-colors ${activeTab === "methodology" ? "text-cyan-400 border-b-2 border-cyan-400 font-bold" : "hover:text-white"}`}
            >
              10-Point Methodology Plan
            </button>
            <button
              onClick={() => setActiveTab("manuscript")}
              className={`pb-2.5 transition-colors ${activeTab === "manuscript" ? "text-cyan-400 border-b-2 border-cyan-400 font-bold" : "hover:text-white"}`}
            >
              Manuscript Draft & LaTeX
            </button>
            <button
              onClick={() => setActiveTab("graph")}
              className={`pb-2.5 transition-colors ${activeTab === "graph" ? "text-cyan-400 border-b-2 border-cyan-400 font-bold" : "hover:text-white"}`}
            >
              Knowledge Graph ({autopilotData.knowledge_graph?.nodes_count} Nodes)
            </button>
          </div>

          {/* Tab 1: Execution Logs */}
          {activeTab === "logs" && (
            <div className="bg-slate-950 border border-white/10 rounded-xl p-4 font-mono text-xs text-slate-300 space-y-2">
              {autopilotData.execution_logs?.map((log: string, idx: number) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="text-cyan-400 select-none">›</span>
                  <span className={log.includes("completed") ? "text-emerald-300" : (log.includes("ALERT") ? "text-amber-300" : "text-slate-300")}>
                    {log}
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Tab 2: Methodology Plan */}
          {activeTab === "methodology" && (
            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
              <div>
                <h3 className="text-base font-bold text-white">{autopilotData.methodology_plan?.methodology_name}</h3>
                <p className="text-xs text-slate-400">{autopilotData.methodology_plan?.methodology_description}</p>
              </div>

              <div className="space-y-3 text-xs">
                <div className="p-3 bg-slate-950 rounded-lg border border-white/5">
                  <span className="font-bold text-cyan-400 block mb-1">Research Questions:</span>
                  <ul className="list-disc pl-5 space-y-1 text-slate-300">
                    {autopilotData.methodology_plan?.["2_research_questions"]?.map((rq: string, idx: number) => (
                      <li key={idx}>{rq}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-3 bg-slate-950 rounded-lg border border-white/5">
                  <span className="font-bold text-emerald-400 block mb-1">Analysis Protocol:</span>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {autopilotData.methodology_plan?.["6_analysis_methods"]?.map((m: string, idx: number) => (
                      <span key={idx} className="px-2 py-0.5 rounded bg-slate-800 text-slate-200">{m}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Tab 3: Manuscript Draft */}
          {activeTab === "manuscript" && (
            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-white/5 pb-3">
                <h3 className="text-base font-bold text-white">{autopilotData.manuscript?.title}</h3>
                <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-mono">
                  {autopilotData.manuscript?.journal_style} Template
                </span>
              </div>
              <div className="text-xs leading-relaxed text-slate-300 space-y-3 max-h-96 overflow-y-auto pr-2">
                <div className="p-3 bg-slate-950 rounded-lg">
                  <span className="font-bold text-cyan-400 block mb-1">ABSTRACT</span>
                  <p>{autopilotData.manuscript?.abstract}</p>
                </div>
                {autopilotData.manuscript?.sections && Object.entries(autopilotData.manuscript.sections).map(([sec, txt]) => (
                  <div key={sec} className="p-3 bg-slate-950 rounded-lg">
                    <span className="font-bold text-slate-400 uppercase block mb-1">{sec.replace(/_/g, " ")}</span>
                    <p className="whitespace-pre-line">{txt as string}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tab 4: Knowledge Graph Nodes */}
          {activeTab === "graph" && (
            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Network className="w-4 h-4 text-cyan-400" />
                Multi-Relational Knowledge Graph Nodes ({autopilotData.knowledge_graph?.nodes_count} Total)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 max-h-96 overflow-y-auto">
                {autopilotData.knowledge_graph?.nodes?.map((n: any) => (
                  <div key={n.id} className="p-2.5 bg-slate-950 rounded-lg border border-white/5 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-cyan-400 text-[10px]">{n.type}</span>
                      <span className="text-[10px] text-slate-500">{n.category}</span>
                    </div>
                    <div className="font-medium text-slate-200 truncate">{n.label}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
