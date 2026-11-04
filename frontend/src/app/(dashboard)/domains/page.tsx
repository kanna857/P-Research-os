"use client";

import React, { useState, useEffect } from "react";
import { Compass, Search, BookOpen, Cpu, ShieldAlert, Database, ArrowRight } from "lucide-react";

export default function DomainExplorerPage() {
  const [taxonomies, setTaxonomies] = useState<any>(null);
  const [selectedDomain, setSelectedDomain] = useState<string>("Artificial Intelligence and Machine Learning");
  const [searchFilter, setSearchFilter] = useState("");
  const [domainDetail, setDomainDetail] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/universal/taxonomies")
      .then((res) => res.json())
      .then((data) => setTaxonomies(data))
      .catch((err) => console.error("Taxonomy fetch error:", err));
  }, []);

  useEffect(() => {
    if (!selectedDomain) return;
    setLoading(true);
    fetch("http://localhost:8000/api/universal/route-domain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: selectedDomain, user_override_domain: selectedDomain }),
    })
      .then((res) => res.json())
      .then((data) => setDomainDetail(data))
      .catch((err) => console.error("Domain route error:", err))
      .finally(() => setLoading(false));
  }, [selectedDomain]);

  const filteredDomains = taxonomies?.domains?.filter((d: string) =>
    d.toLowerCase().includes(searchFilter.toLowerCase())
  ) || [];

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
            <Compass className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Universal Domain Explorer</h1>
            <p className="text-sm text-slate-400">36 academic disciplines across physical, biological, social, and formal sciences</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Domain List */}
        <div className="bg-slate-900/60 border border-white/10 rounded-2xl p-5 space-y-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Search 36 academic disciplines..."
              className="w-full bg-slate-950 border border-white/10 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>

          <div className="space-y-1.5 max-h-[560px] overflow-y-auto pr-1">
            {filteredDomains.map((d: string) => (
              <button
                key={d}
                onClick={() => setSelectedDomain(d)}
                className={`w-full text-left px-3 py-2.5 rounded-lg text-xs font-medium transition-all flex items-center justify-between ${
                  selectedDomain === d
                    ? "bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 border border-cyan-500/40 text-cyan-300 font-bold"
                    : "hover:bg-slate-800/60 text-slate-300"
                }`}
              >
                <span className="truncate">{d}</span>
                {selectedDomain === d && <ArrowRight className="w-3.5 h-3.5 text-cyan-400 shrink-0" />}
              </button>
            ))}
          </div>
        </div>

        {/* Right: Domain Details */}
        <div className="lg:col-span-2 space-y-4">
          {domainDetail && (
            <div className="bg-slate-900/60 border border-white/10 rounded-2xl p-6 space-y-5">
              <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <div>
                  <span className="text-xs font-mono text-cyan-400 uppercase tracking-widest">{domainDetail.category}</span>
                  <h2 className="text-xl font-bold text-white mt-0.5">{domainDetail.primary_domain}</h2>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30">
                  Method: {domainDetail.default_methodology}
                </span>
              </div>

              {/* Grid properties */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                {/* Evidence Requirements */}
                <div className="bg-slate-950/80 p-4 rounded-xl border border-white/5 space-y-2">
                  <span className="font-bold text-cyan-400 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4" /> Required Evidence Types
                  </span>
                  <ul className="list-disc pl-4 space-y-1 text-slate-300">
                    {domainDetail.evidence_requirements?.map((e: string, idx: number) => (
                      <li key={idx}>{e}</li>
                    ))}
                  </ul>
                </div>

                {/* Dataset Requirements */}
                <div className="bg-slate-950/80 p-4 rounded-xl border border-white/5 space-y-2">
                  <span className="font-bold text-amber-400 flex items-center gap-1.5">
                    <Database className="w-4 h-4" /> Dataset Specifications
                  </span>
                  <ul className="list-disc pl-4 space-y-1 text-slate-300">
                    {domainDetail.dataset_requirements?.map((d: string, idx: number) => (
                      <li key={idx}>{d}</li>
                    ))}
                  </ul>
                </div>

                {/* Computational Needs */}
                <div className="bg-slate-950/80 p-4 rounded-xl border border-white/5 space-y-2">
                  <span className="font-bold text-purple-400 flex items-center gap-1.5">
                    <Cpu className="w-4 h-4" /> Computational Architecture
                  </span>
                  <p className="text-slate-300 leading-relaxed">{domainDetail.computational_needs}</p>
                </div>

                {/* Ethics */}
                <div className="bg-slate-950/80 p-4 rounded-xl border border-white/5 space-y-2">
                  <span className="font-bold text-rose-400 flex items-center gap-1.5">
                    <ShieldAlert className="w-4 h-4" /> Ethical & Regulatory Safeguards
                  </span>
                  <ul className="list-disc pl-4 space-y-1 text-slate-300">
                    {domainDetail.ethical_and_regulatory_considerations?.map((eth: string, idx: number) => (
                      <li key={idx}>{eth}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
