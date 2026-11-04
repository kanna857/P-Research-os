"use client";

import React, { useState } from "react";
import { ShieldAlert, CheckCircle2, AlertTriangle, AlertCircle, FileCheck, Shield, RefreshCw } from "lucide-react";

export default function EthicsCenterPage() {
  const [topic, setTopic] = useState("Machine Learning Methods for Liver Disease Classification with human clinical records");
  const [methodology, setMethodology] = useState("computational");
  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState<any>(null);

  const handleRunEthicsScreening = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/universal/ethics-screening", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, methodology }),
      });
      if (res.ok) {
        setAuditResult(await res.json());
      }
    } catch (err) {
      console.error("Ethics screening error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-rose-500 to-red-600 text-white shadow-lg shadow-rose-500/20">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Research Ethics & Regulatory Compliance</h1>
            <p className="text-sm text-slate-400">IRB human participant screening, HIPAA/GDPR health data privacy, and ethical guardrails</p>
          </div>
        </div>

        <button
          onClick={handleRunEthicsScreening}
          disabled={loading}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-400 hover:to-red-500 text-white font-bold text-sm shadow-lg shadow-rose-600/30 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          {loading ? "Screening..." : "Run Compliance Audit"}
        </button>
      </div>

      {/* Input */}
      <div className="bg-slate-900/60 border border-white/10 rounded-2xl p-5 space-y-3">
        <label className="text-xs font-bold text-slate-300">Research Topic & Protocol Context</label>
        <textarea
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          rows={2}
          className="w-full bg-slate-950 border border-white/10 rounded-lg p-3 text-xs text-white focus:outline-none focus:ring-2 focus:ring-rose-500"
        />
      </div>

      {/* Audit Banner */}
      {auditResult && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Ethics Risk Level</span>
              <div className={`text-2xl font-extrabold mt-1 ${auditResult.overall_ethics_risk === "CRITICAL" ? "text-rose-400" : (auditResult.overall_ethics_risk === "HIGH" ? "text-amber-400" : "text-emerald-400")}`}>
                {auditResult.overall_ethics_risk}
              </div>
              <span className="text-xs text-slate-500 mt-1 block">{auditResult.triggers_detected_count} triggers detected</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Human Confirmation</span>
              <div className="text-base font-bold text-white mt-2 flex items-center gap-1.5">
                {auditResult.human_approval_required ? (
                  <span className="text-amber-400 flex items-center gap-1"><AlertTriangle className="w-4 h-4" /> MANDATORY</span>
                ) : (
                  <span className="text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> NOT REQUIRED</span>
                )}
              </div>
              <span className="text-xs text-slate-500 mt-1 block">IRB/IACUC check gate</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">PHI / Medical Shield</span>
              <div className="text-base font-bold text-cyan-300 mt-2">HIPAA Safe Harbor</div>
              <span className="text-xs text-slate-500 mt-1 block">De-identification audit</span>
            </div>

            <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Diagnostic Disclaimer</span>
              <div className="text-xs font-bold text-amber-300 mt-2">Research Use Only</div>
              <span className="text-xs text-slate-500 mt-1 block">Zero clinical diagnosis claims</span>
            </div>
          </div>

          {/* Compliance Triggers List */}
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-rose-400" />
              Detected Compliance Triggers & Governing Bodies
            </h3>
            <div className="space-y-2">
              {auditResult.compliance_triggers?.map((trig: any, idx: number) => (
                <div key={idx} className="bg-slate-950 p-3.5 rounded-lg border border-white/5 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-rose-300">{trig.category}</span>
                    <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 font-mono text-[10px] font-bold">
                      {trig.severity}
                    </span>
                  </div>
                  <div className="text-slate-400">
                    <span className="text-slate-500">Oversight Body:</span> <span className="text-slate-200">{trig.oversight_body}</span>
                  </div>
                  <div className="text-slate-300 bg-slate-900/80 p-2 rounded border border-white/5">
                    <span className="text-amber-400 font-semibold">Requirement:</span> {trig.mandatory_requirement}
                  </div>
                </div>
              ))}
            </div>

            {/* Legal Notice */}
            <div className="mt-4 p-3 bg-rose-950/40 border border-rose-500/30 rounded-lg text-xs text-rose-300 font-medium">
              {auditResult.legal_disclaimer}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
