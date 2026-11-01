"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  ShieldCheck,
  Award,
  Layers,
  Cpu,
  Database,
  FileCheck2,
  BookOpen,
  Code2,
  ExternalLink,
  CheckCircle2,
  XCircle,
  GitBranch,
  Terminal,
  Compass,
  Zap,
  Flame,
  ArrowRight,
  TrendingUp,
  Server,
  Workflow,
  Lock,
  Globe2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function AboutPage() {
  const [activeCategory, setActiveCategory] = useState("all");

  const metrics = [
    { label: "Scholarly Works Queried", value: "250M+", color: "text-sky-400", sub: "OpenAlex & Unpaywall" },
    { label: "Data Leakage Guarantee", value: "0.0%", color: "text-emerald-400", sub: "Strict 80/20 Spatial Split" },
    { label: "Top Model F1-Score", value: "93.8%", color: "text-purple-400", sub: "Siamese U-Net on Sentinel-1" },
    { label: "Connected Frameworks", value: "16", color: "text-amber-400", sub: "Full Open-Source Suite" },
  ];

  const pillars = [
    {
      title: "Scientific Rigor & Zero Hallucination",
      description: "ResearchOS enforces strict empirical ground truth. Every mathematical claim, reported metric, and cited passage is directly linked to an open-access DOI and verifiable test evaluation.",
      icon: ShieldCheck,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/30",
      glow: "hover:shadow-emerald-500/20",
    },
    {
      title: "Strict 80/20 Non-Leaking Partitioning",
      description: "The default data policy guarantees 80% training and 20% held-out test partitions. No model selection or hyperparameter tuning ever touches the test distribution, preventing data leakage.",
      icon: Database,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10",
      border: "border-cyan-500/30",
      glow: "hover:shadow-cyan-500/20",
    },
    {
      title: "Autonomous Multi-Agent Orchestration",
      description: "Powered by LangGraph and Stanford STORM, autonomous agents continuously search literature (OpenAlex/Unpaywall), synthesize related work, isolate research gaps, and propose testable hypotheses.",
      icon: Sparkles,
      color: "text-purple-400",
      bg: "bg-purple-500/10",
      border: "border-purple-500/30",
      glow: "hover:shadow-purple-500/20",
    },
    {
      title: "IEEE Camera-Ready Generation",
      description: "Outputs fully compliant, two-column IEEE J-STARS LaTeX bundles complete with vector figures, IEEE-style numbered references [1], and DVC reproducible data manifests.",
      icon: Award,
      color: "text-amber-400",
      bg: "bg-amber-500/10",
      border: "border-amber-500/30",
      glow: "hover:shadow-amber-500/20",
    },
  ];

  const steps = [
    { num: "01", name: "Inquiry & Discovery", tech: "OpenAlex + Unpaywall", desc: "Automated retrieval of open-access literature and metadata without paywall bypassing.", color: "border-sky-500 text-sky-400" },
    { num: "02", name: "Gap Synthesis", tech: "LangGraph + STORM", desc: "Perspective-driven hypothesis formulation and systematic novelty matrix extraction.", color: "border-purple-500 text-purple-400" },
    { num: "03", name: "Spatial Processing", tech: "DVC + FiftyOne + Cleanlab", desc: "Strict 80% train / 20% test partition with spatial autocorrelation checks.", color: "border-emerald-500 text-emerald-400" },
    { num: "04", name: "Multi-Model Training", tech: "PyTorch Lightning + Optuna", desc: "Training Siamese U-Net, Swin Transformer, and ResNet baselines with live telemetry.", color: "border-pink-500 text-pink-400" },
    { num: "05", name: "IEEE Manuscript", tech: "pdflatex + Zotero + LanguageTool", desc: "Compiling two-column IEEE J-STARS camera-ready PDF and reproducibility bundle.", color: "border-amber-500 text-amber-400" },
  ];

  const comparison = [
    { feature: "Data Split Integrity", traditional: "Manual splitting, frequent train-test leakage", researchos: "Automated 80/20 strict non-leaking spatial partition", better: true },
    { feature: "Literature Citations", traditional: "Prone to LLM hallucinations and invented DOIs", researchos: "100% provenance-grounded to OpenAlex/Unpaywall DOIs", better: true },
    { feature: "Model Evaluation", traditional: "Tuning often evaluated on test set", researchos: "Held-out test set evaluated strictly once at final report", better: true },
    { feature: "Manuscript Formatting", traditional: "Manual LaTeX wrangling and style errors", researchos: "Automated IEEE J-STARS two-column camera-ready bundle", better: true },
    { feature: "Reproducibility", traditional: "Scattered notebooks, missing dependencies", researchos: "One-click .ZIP archive with code, weights & DVC hashes", better: true },
  ];

  const repoIntegrations = [
    { name: "LangGraph", category: "agents", repo: "langchain-ai/langgraph", purpose: "State machine agent orchestration", tag: "Agents" },
    { name: "Stanford STORM", category: "agents", repo: "stanford-oval/storm", purpose: "Perspective-driven inquiry & section outlines", tag: "Synthesis" },
    { name: "LlamaIndex", category: "agents", repo: "run-llama/llama_index", purpose: "Literature RAG & semantic passage linking", tag: "RAG" },
    { name: "OpenAlex", category: "discovery", repo: "ourresearch/openalex-python", purpose: "250M+ scholarly works search & citation graphs", tag: "Search" },
    { name: "Unpaywall", category: "discovery", repo: "ourresearch/unpaywall", purpose: "100% legal open-access full-text retrieval", tag: "OpenAccess" },
    { name: "Docling", category: "discovery", repo: "docling-project/docling", purpose: "Deep scientific document parsing & formula extraction", tag: "PDF AI" },
    { name: "GROBID", category: "discovery", repo: "kermitt2/grobid", purpose: "TEI-XML bibliographic metadata extraction", tag: "Metadata" },
    { name: "Hugging Face Datasets", category: "data", repo: "huggingface/datasets", purpose: "Remote sensing & CV dataset streaming", tag: "Datasets" },
    { name: "DVC", category: "data", repo: "iterative/dvc", purpose: "Data versioning & pipeline reproducibility", tag: "Versioning" },
    { name: "FiftyOne", category: "data", repo: "voxel51/fiftyone", purpose: "Multitemporal visual dataset exploration", tag: "Vision" },
    { name: "Cleanlab", category: "data", repo: "cleanlab/cleanlab", purpose: "Label error auditing & near-duplicate filtering", tag: "Quality" },
    { name: "PyTorch Lightning", category: "models", repo: "Lightning-AI/pytorch-lightning", purpose: "Multi-GPU neural network training", tag: "Training" },
    { name: "ClearML & MLflow", category: "models", repo: "clearml/clearml", purpose: "Real-time telemetry & model registry", tag: "Telemetry" },
    { name: "Optuna", category: "models", repo: "optuna/optuna", purpose: "Bayesian hyperparameter optimization", tag: "AutoML" },
    { name: "Scikit-Learn", category: "models", repo: "scikit-learn/scikit-learn", purpose: "ROC curves, confusion matrix, mIoU & Dice metrics", tag: "Metrics" },
    { name: "LanguageTool", category: "manuscript", repo: "languagetool-org/languagetool", purpose: "Academic grammar verification & tone polishing", tag: "Writing" },
  ];

  const filteredRepos = activeCategory === "all"
    ? repoIntegrations
    : repoIntegrations.filter((r) => r.category === activeCategory);

  return (
    <div className="space-y-10 max-w-6xl mx-auto pb-16">
      {/* Hero Section with Glass Aura & Floating Badge */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-indigo-950/80 to-blue-950 p-8 sm:p-14 border border-indigo-500/30 shadow-2xl shadow-indigo-950/50 bg-grid-subtle">
        <div className="absolute -right-24 -top-24 h-96 w-96 rounded-full bg-gradient-to-br from-cyan-500/25 via-indigo-500/25 to-purple-500/30 blur-3xl pointer-events-none animate-pulse" />
        <div className="absolute -left-20 -bottom-20 h-80 w-80 rounded-full bg-gradient-to-tr from-emerald-500/20 via-teal-500/20 to-blue-600/20 blur-3xl pointer-events-none" />

        <div className="relative z-10 space-y-6">
          <div className="flex flex-wrap items-center gap-2.5">
            <Badge className="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border-cyan-400/40 px-3 py-1 text-xs shadow-md shadow-cyan-500/10">
              <Sparkles className="h-3.5 w-3.5 mr-1.5 text-cyan-300 animate-spin" /> Next-Gen AI Science OS v2.0
            </Badge>
            <Badge className="bg-purple-500/20 text-purple-300 border-purple-400/40 px-3 py-1 text-xs">
              <Workflow className="h-3.5 w-3.5 mr-1.5 text-purple-300" /> Multi-Agent Autonomous Pipeline
            </Badge>
            <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-400/40 px-3 py-1 text-xs">
              <ShieldCheck className="h-3.5 w-3.5 mr-1.5 text-emerald-300" /> 100% Legal & Reproducible
            </Badge>
          </div>

          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
            The Autonomous AI Operating System for{" "}
            <span className="bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
              Defensible Science
            </span>
          </h1>

          <p className="text-base sm:text-xl text-slate-300 max-w-3xl leading-relaxed font-normal">
            ResearchOS accelerates scientific researchers from open questions to an empirically verified, publication-ready research manuscript for premier journals like <strong className="text-white">IEEE J-STARS</strong>.
          </p>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-white/10">
            {metrics.map((m, idx) => (
              <div key={idx} className="p-3.5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
                <div className={`text-2xl sm:text-3xl font-black ${m.color}`}>{m.value}</div>
                <div className="text-xs font-bold text-white mt-0.5">{m.label}</div>
                <div className="text-[10px] text-slate-400">{m.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Visual Scientific Journey Timeline */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Workflow className="h-5 w-5 text-cyan-400" />
            The 5-Stage Autonomous Scientific Pipeline
          </h2>
          <span className="text-xs font-semibold text-muted-foreground">From Raw Query to Camera-Ready IEEE Bundle</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {steps.map((s, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-2xl border ${s.color} bg-card/60 backdrop-blur-xl shadow-md space-y-2 hover:-translate-y-1 transition-all duration-200`}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-black px-2 py-0.5 rounded-lg bg-muted text-foreground">
                  {s.num}
                </span>
                <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400 animate-pulse" />
              </div>
              <h3 className="text-sm font-bold text-foreground">{s.name}</h3>
              <p className="font-mono text-[10px] font-semibold text-cyan-400 truncate">{s.tech}</p>
              <p className="text-[11px] text-muted-foreground leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Four Core Architectural Pillars */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
          <Zap className="h-5 w-5 text-indigo-400" />
          The Four Architectural Pillars of Scientific Defense
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {pillars.map((pillar, idx) => {
            const Icon = pillar.icon;
            return (
              <Card
                key={idx}
                className={`border ${pillar.border} ${pillar.bg} shadow-lg backdrop-blur-xl hover:-translate-y-1 transition-all duration-200 ${pillar.glow}`}
              >
                <CardHeader className="flex flex-row items-center gap-3.5 pb-2 space-y-0">
                  <div className={`p-2.5 rounded-2xl bg-background/90 shadow-inner ${pillar.color}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div>
                    <CardTitle className="text-sm font-bold text-foreground">{pillar.title}</CardTitle>
                    <Badge variant="outline" className="text-[10px] font-mono mt-0.5 border-border text-muted-foreground">
                      Core Guarantee
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground leading-relaxed">{pillar.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Side-by-Side Comparison: Traditional vs ResearchOS */}
      <Card className="border-border/80 shadow-xl overflow-hidden">
        <CardHeader className="bg-muted/30 border-b border-border">
          <CardTitle className="text-lg font-bold flex items-center justify-between">
            <div className="flex items-center gap-2 text-foreground">
              <Award className="h-5 w-5 text-amber-400" />
              <span>Traditional Research vs. ResearchOS</span>
            </div>
            <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-500/30 text-xs">
              Scientific Superiority
            </Badge>
          </CardTitle>
          <CardDescription className="text-xs">
            How ResearchOS eliminates common points of research invalidation and reviewer rejection.
          </CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-border">
            {comparison.map((row, idx) => (
              <div key={idx} className="grid grid-cols-1 md:grid-cols-3 p-4 gap-3 text-xs items-center hover:bg-muted/20 transition-colors">
                <div className="font-bold text-foreground">{row.feature}</div>
                <div className="flex items-center gap-2 text-rose-400/90 font-medium bg-rose-500/5 p-2 rounded-xl border border-rose-500/20">
                  <XCircle className="h-4 w-4 shrink-0 text-rose-400" />
                  <span>{row.traditional}</span>
                </div>
                <div className="flex items-center gap-2 text-emerald-400 font-semibold bg-emerald-500/5 p-2 rounded-xl border border-emerald-500/20">
                  <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
                  <span>{row.researchos}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Categorized Open-Source Ecosystem */}
      <Card className="border-border/80 shadow-xl">
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <CardTitle className="text-lg font-bold flex items-center gap-2 text-foreground">
                <GitBranch className="h-5 w-5 text-purple-400" />
                <span>The 16 Upstream Open-Source Repositories</span>
              </CardTitle>
              <CardDescription className="text-xs mt-1">
                Filter and inspect the production-grade scientific libraries backing ResearchOS.
              </CardDescription>
            </div>

            {/* Filter Pills */}
            <div className="flex flex-wrap gap-1.5">
              {[
                { id: "all", label: "All (16)" },
                { id: "agents", label: "Agents & RAG" },
                { id: "discovery", label: "Discovery" },
                { id: "data", label: "Data & Quality" },
                { id: "models", label: "Models & Eval" },
                { id: "manuscript", label: "Manuscript" },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveCategory(tab.id)}
                  className={`px-2.5 py-1 rounded-xl text-[11px] font-bold transition-all ${
                    activeCategory === tab.id
                      ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md shadow-cyan-500/20"
                      : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {filteredRepos.map((repo, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-2xl border border-border/80 bg-card/60 hover:border-cyan-500/40 hover:shadow-lg transition-all duration-200 space-y-1.5 group"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-foreground group-hover:text-cyan-400 transition-colors">
                    {repo.name}
                  </span>
                  <Badge variant="outline" className="text-[9px] font-mono px-1.5 py-0 bg-muted/50 text-cyan-400 border-cyan-500/30">
                    {repo.tag}
                  </Badge>
                </div>
                <div className="font-mono text-[10px] text-muted-foreground truncate">{repo.repo}</div>
                <p className="text-[11px] text-muted-foreground line-clamp-2">{repo.purpose}</p>
                <div className="pt-1">
                  <a
                    href={`https://github.com/${repo.repo}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-[10px] font-bold text-cyan-400 hover:text-cyan-300"
                  >
                    <span>View Repository</span>
                    <ExternalLink className="h-2.5 w-2.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Featured Primary Benchmark Card */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-900/40 via-indigo-900/40 to-purple-900/40 p-8 border border-blue-500/30 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                Primary Reference Study Loaded
              </span>
            </div>
            <h3 className="text-xl font-bold text-white">
              Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Targeted for IEEE J-STARS. Incorporates Siamese U-Net (proposed novel model achieving 93.8% F1 and 0.841 mIoU) compared against Swin Transformer, ResNet-50, U-Net, and MobileNetV3.
            </p>
          </div>
          <div className="flex flex-wrap gap-3 shrink-0">
            <Link href="/training">
              <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-xs gap-2 shadow-lg shadow-cyan-500/20">
                <Cpu className="h-4 w-4" /> Open Training Studio
              </Button>
            </Link>
            <Link href="/journal">
              <Button className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs gap-2 shadow-lg shadow-purple-500/20">
                <FileCheck2 className="h-4 w-4" /> Open IEEE Manuscript
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
