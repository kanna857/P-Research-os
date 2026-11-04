"use client";

import React, { useState, useEffect } from "react";
import { AlertCircle, CheckCircle2, ShieldAlert, AlertTriangle, FileSearch, Sparkles, RefreshCw } from "lucide-react";

export default function IntegrityPage() {
  const [manuscriptText, setManuscriptText] = useState(
    "Abstract: In this work, we propose the first ever flawless framework for SAR change detection, achieving an unprecedented 94.5% accuracy.\n\n" +
    "Introduction: Recent advances in convnets show great promise for multitemporal remote sensing imagery. Prior research has identified speckle noise as the primary bottleneck.\n\n" +
    "Methodology: The framework processes dual-polarized Sentinel-1 GRD imagery through a Siamese attention backbone.\n\n" +
    "Results: Experimental evaluation demonstrates an F1-score of 0.884 and an IoU of 0.795, outperforming standard baselines.\n\n" +
    "Conclusion: We presented a complete solution that surpasses all known methods in SAR change delineation."
  );

  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState<any>(null);

  const runAudit = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/integrity/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          manuscript_text: manuscriptText,
          metrics: {
            accuracy: 0.945,
            f1_score: 0.884,
            iou: 0.795,
            precision: 0.892,
            recall: 0.876
          },
          split_metadata: {
            split_method: "Spatial Tile Cross-Validation (80/20 non-overlapping partition)",
            train_tile_ids: ["S1_Tile_01", "S1_Tile_02", "S1_Tile_03", "S1_Tile_04"],
            test_tile_ids: ["S1_Tile_05"]
          }
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setAuditResult(data);
      }
    } catch (err) {
      console.error("Integrity audit error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runAudit();
  }, []);

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "Critical":
        return <span className="px-2 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">CRITICAL</span>;
      case "High":
        return <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">HIGH</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-xs font-bold bg-yellow-500/20 text-yellow-300 border border-yellow-500/30">MEDIUM</span>;
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
            <h1 className="text-2xl font-bold text-white tracking-tight">Research Integrity & Rigour Checker</h1>
            <p className="text-sm text-slate-400">Automated audit for attribution, novelty claims, metric anomalies & spatial leakage</p>
          </div>
        </div>

        <button
          onClick={runAudit}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-medium text-sm transition-colors shadow-lg shadow-rose-600/30 disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          Run Integrity Audit
        </button>
      </div>

      {/* Score Overview */}
      {auditResult && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Integrity Score</span>
            <div className={`text-3xl font-extrabold mt-1 ${auditResult.overall_integrity_score >= 80 ? "text-emerald-400" : (auditResult.overall_integrity_score >= 60 ? "text-amber-400" : "text-rose-400")}`}>
              {auditResult.overall_integrity_score} / 100
            </div>
            <span className="text-xs text-slate-500 mt-1 block">Status: {auditResult.status}</span>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Attribution Check</span>
            <div className="text-lg font-bold text-slate-200 mt-2 flex items-center gap-1.5">
              {auditResult.audit_summary?.attribution_check === "PASSED" ? (
                <><CheckCircle2 className="w-4 h-4 text-emerald-400" /> PASSED</>
              ) : (
                <><AlertTriangle className="w-4 h-4 text-amber-400" /> NEEDS REVISION</>
              )}
            </div>
            <span className="text-xs text-slate-500 mt-1 block">Prior work citations</span>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Novelty Tone</span>
            <div className="text-lg font-bold text-slate-200 mt-2 flex items-center gap-1.5">
              {auditResult.audit_summary?.novelty_check === "PASSED" ? (
                <><CheckCircle2 className="w-4 h-4 text-emerald-400" /> BALANCED</>
              ) : (
                <><AlertCircle className="w-4 h-4 text-rose-400" /> OVERCLAIMING</>
              )}
            </div>
            <span className="text-xs text-slate-500 mt-1 block">Hedged claim language</span>
          </div>

          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Data Leakage Guard</span>
            <div className="text-lg font-bold text-slate-200 mt-2 flex items-center gap-1.5">
              {auditResult.audit_summary?.leakage_check === "PASSED" ? (
                <><CheckCircle2 className="w-4 h-4 text-emerald-400" /> PASSED (80/20 Non-Leaking)</>
              ) : (
                <><AlertCircle className="w-4 h-4 text-rose-400" /> LEAK RISK</>
              )}
            </div>
            <span className="text-xs text-slate-500 mt-1 block">Spatial tile isolation</span>
          </div>
        </div>
      )}

      {/* Editor & findings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-3">
          <label className="text-sm font-semibold text-slate-300 flex items-center gap-2">
            <FileSearch className="w-4 h-4 text-rose-400" />
            Manuscript Draft to Audit
          </label>
          <textarea
            value={manuscriptText}
            onChange={(e) => setManuscriptText(e.target.value)}
            rows={14}
            className="w-full bg-slate-950/80 border border-white/10 rounded-lg p-3 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-rose-500 font-mono leading-relaxed"
          />
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center justify-between">
            <span>Audit Findings</span>
            <span className="text-xs px-2.5 py-1 rounded bg-slate-800 text-slate-400">
              {auditResult?.findings_count || 0} Issues Detected
            </span>
          </h2>

          <div className="space-y-3 max-h-[460px] overflow-y-auto pr-1">
            {auditResult?.findings?.map((f: any, idx: number) => (
              <div key={idx} className="bg-slate-900/70 border border-white/10 rounded-xl p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-200">{f.category}</span>
                  {getSeverityBadge(f.severity)}
                </div>
                <div className="text-xs text-slate-400 font-mono bg-slate-950 p-2 rounded border border-white/5">
                  "{f.excerpt}"
                </div>
                <p className="text-xs text-slate-300">{f.finding}</p>
                <div className="text-xs text-emerald-300 bg-emerald-500/10 px-2.5 py-1.5 rounded border border-emerald-500/20">
                  <span className="font-semibold text-emerald-400">Action:</span> {f.recommendation}
                </div>
              </div>
            ))}

            {auditResult?.findings?.length === 0 && (
              <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-8 text-center text-emerald-300">
                <CheckCircle2 className="w-8 h-8 mx-auto mb-2 text-emerald-400" />
                All research integrity checks passed! No missing citations, data leakage, or novelty overclaims.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
