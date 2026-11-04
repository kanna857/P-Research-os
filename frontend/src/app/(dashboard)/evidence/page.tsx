"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck, Search, CheckCircle2, AlertTriangle, XCircle, HelpCircle, FileText, ArrowRight, RefreshCw } from "lucide-react";

export default function EvidencePage() {
  const [manuscriptText, setManuscriptText] = useState(
    "Recent Siamese convolutional networks achieve F1-scores over 0.88 when trained on dual-polarized Sentinel-1 GRD imagery [1]. " +
    "Applying log-ratio difference images combined with spatial attention mechanisms yields an IoU of 0.825 and F1 score of 89.4% on multitemporal flood mapping benchmarks [2]. " +
    "Spatial cross-validation is mandatory; random pixel splitting produces up to 15% inflated accuracy due to spatial autocorrelation between adjacent SAR pixels [3]. " +
    "In this paper, our proposed architecture outperforms all previous methods by achieving zero false alarms."
  );

  const [loading, setLoading] = useState(false);
  const [auditResult, setAuditResult] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("Sentinel-1 SAR change detection speckle noise");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);

  const handleVerifyManuscript = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/evidence/verify-manuscript", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonBody({ manuscript_text: manuscriptText }),
      });
      if (res.ok) {
        const data = await res.json();
        setAuditResult(data);
      }
    } catch (err) {
      console.error("Verification error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchEvidence = async () => {
    setSearching(true);
    try {
      const res = await fetch("http://localhost:8000/api/evidence/search-evidence", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonBody({ query: searchQuery, top_k: 4 }),
      });
      if (res.ok) {
        const data = await res.json();
        setSearchResults(data.results || []);
      }
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setSearching(false);
    }
  };

  function jsonBody(obj: any) {
    return JSON.stringify(obj);
  }

  useEffect(() => {
    handleVerifyManuscript();
    handleSearchEvidence();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Supported":
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"><CheckCircle2 className="w-3 h-3" /> Supported</span>;
      case "Partially Supported":
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30"><AlertTriangle className="w-3 h-3" /> Partial</span>;
      case "Contradicted":
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/20 text-purple-400 border border-purple-500/30"><XCircle className="w-3 h-3" /> Contradicted</span>;
      case "Unsupported":
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30"><XCircle className="w-3 h-3" /> Unsupported</span>;
      default:
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-500/20 text-slate-400 border border-slate-500/30"><HelpCircle className="w-3 h-3" /> Unverified</span>;
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-600 text-white shadow-lg shadow-teal-500/20">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight">Evidence Verification Agent</h1>
              <p className="text-sm text-slate-400">pgvector semantic cross-referencing & citation grounded audit</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleVerifyManuscript}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-colors shadow-lg shadow-emerald-600/30 disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            Run Verification
          </button>
        </div>
      </div>

      {/* Audit Stats Banner */}
      {auditResult && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Verification Score</span>
            <div className="text-3xl font-extrabold text-emerald-400 mt-1">{auditResult.evidence_verification_score}%</div>
            <span className="text-xs text-slate-500 mt-1 block">Weighted citation confidence</span>
          </div>
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Supported Claims</span>
            <div className="text-3xl font-extrabold text-emerald-400 mt-1">{auditResult.status_summary?.Supported || 0}</div>
            <span className="text-xs text-slate-500 mt-1 block">Full DOI alignment</span>
          </div>
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Partial Evidence</span>
            <div className="text-3xl font-extrabold text-amber-400 mt-1">{auditResult.status_summary?.["Partially Supported"] || 0}</div>
            <span className="text-xs text-slate-500 mt-1 block">Related conceptual match</span>
          </div>
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Flagged / Unverified</span>
            <div className="text-3xl font-extrabold text-rose-400 mt-1">
              {(auditResult.status_summary?.Unsupported || 0) + (auditResult.status_summary?.Contradicted || 0)}
            </div>
            <span className="text-xs text-slate-500 mt-1 block">Requires manual citation</span>
          </div>
          <div className="bg-slate-900/60 border border-white/10 rounded-xl p-4">
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Submission Status</span>
            <div className="mt-2">
              {auditResult.is_submission_ready ? (
                <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">READY</span>
              ) : (
                <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">NEEDS REVISION</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Input manuscript text */}
      <div className="bg-slate-900/70 border border-white/10 rounded-xl p-5 space-y-3">
        <label className="text-sm font-semibold text-slate-300 flex items-center gap-2">
          <FileText className="w-4 h-4 text-emerald-400" />
          Manuscript Passage to Verify
        </label>
        <textarea
          value={manuscriptText}
          onChange={(e) => setManuscriptText(e.target.value)}
          rows={4}
          className="w-full bg-slate-950/80 border border-white/10 rounded-lg p-3 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 font-mono"
          placeholder="Paste manuscript claims with citation keys like [1] or [Smith et al., 2023]..."
        />
      </div>

      {/* Extracted & Verified Claims */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          Claim-by-Claim Verification Analysis
          {auditResult && <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">({auditResult.total_claims_extracted} extracted)</span>}
        </h2>

        {auditResult?.verified_claims?.length > 0 ? (
          <div className="space-y-3">
            {auditResult.verified_claims.map((claim: any, idx: number) => (
              <div key={idx} className="bg-slate-900/50 border border-white/10 rounded-xl p-4 space-y-2">
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-slate-400">{claim.claim_id}</span>
                      {getStatusBadge(claim.status)}
                      <span className="text-xs text-slate-400">Confidence: {(claim.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <p className="text-sm font-medium text-slate-200 mt-1">"{claim.claim_text}"</p>
                  </div>
                </div>

                {claim.matched_doi && (
                  <div className="text-xs text-slate-400 bg-slate-950/50 p-2.5 rounded-lg border border-white/5 space-y-1">
                    <div className="flex items-center gap-2 text-emerald-400 font-medium">
                      <span>Source: {claim.matched_source}</span>
                      <span className="text-slate-500">|</span>
                      <span>DOI: {claim.matched_doi}</span>
                    </div>
                    {claim.evidence_excerpt && (
                      <p className="text-slate-300 italic">"{claim.evidence_excerpt}"</p>
                    )}
                  </div>
                )}

                <div className="text-xs text-amber-300/80 bg-amber-500/10 px-3 py-1.5 rounded border border-amber-500/20">
                  <span className="font-semibold text-amber-400">Remediation:</span> {claim.correction_suggestion}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-slate-900/30 border border-white/5 rounded-xl p-8 text-center text-slate-400">
            {loading ? "Analyzing claims..." : "No claims extracted. Enter text above to run verification."}
          </div>
        )}
      </div>

      {/* Semantic Literature Search */}
      <div className="bg-slate-900/60 border border-white/10 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Search className="w-4 h-4 text-cyan-400" />
              pgvector Semantic Evidence Explorer
            </h3>
            <p className="text-xs text-slate-400">Retrieve dense 384-d semantic chunks indexed from OpenAlex, Crossref, and Docling</p>
          </div>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1 bg-slate-950 border border-white/10 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            placeholder="Search verified academic evidence passages..."
          />
          <button
            onClick={handleSearchEvidence}
            disabled={searching}
            className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-sm rounded-lg transition-colors disabled:opacity-50"
          >
            {searching ? "Searching..." : "Retrieve"}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
          {searchResults.map((item, idx) => (
            <div key={idx} className="bg-slate-950/70 border border-white/10 rounded-lg p-3.5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-cyan-400">{item.title}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono">
                  Sim: {(item.similarity_score * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{item.content}</p>
              <div className="text-[10px] text-slate-500 font-mono">DOI: {item.doi}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
