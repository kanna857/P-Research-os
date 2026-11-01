"use client";

import React from "react";
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
  GitBranch,
  Terminal,
  Compass,
  Zap,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function AboutPage() {
  const pillars = [
    {
      title: "Scientific Rigor & Zero Hallucination",
      description: "ResearchOS enforces strict empirical ground truth. Every mathematical claim, reported metric, and cited passage is directly linked to an open-access DOI and verifiable test evaluation.",
      icon: ShieldCheck,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/30",
    },
    {
      title: "Strict 80/20 Non-Leaking Partitioning",
      description: "The default data policy guarantees 80% training and 20% held-out test partitions. No model selection or hyperparameter tuning ever touches the test distribution, preventing data leakage.",
      icon: Database,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10",
      border: "border-cyan-500/30",
    },
    {
      title: "Multi-Agent Orchestration",
      description: "Powered by LangGraph and Stanford STORM, autonomous agents continuously search literature (OpenAlex/Unpaywall), synthesize related work, isolate research gaps, and propose testable hypotheses.",
      icon: Sparkles,
      color: "text-purple-400",
      bg: "bg-purple-500/10",
      border: "border-purple-500/30",
    },
    {
      title: "IEEE Camera-Ready Generation",
      description: "Outputs fully compliant, two-column IEEE J-STARS LaTeX bundles complete with vector figures, IEEE-style numbered references [1], and DVC reproducible data manifests.",
      icon: Award,
      color: "text-amber-400",
      bg: "bg-amber-500/10",
      border: "border-amber-500/30",
    },
  ];

  const repoIntegrations = [
    { name: "LangGraph", repo: "langchain-ai/langgraph", purpose: "State machine agent orchestration" },
    { name: "Stanford STORM", repo: "stanford-oval/storm", purpose: "Perspective-driven inquiry & section outlines" },
    { name: "LlamaIndex", repo: "run-llama/llama_index", purpose: "Literature RAG & semantic passage linking" },
    { name: "OpenAlex", repo: "ourresearch/openalex-python", purpose: "250M+ scholarly works search & citation graphs" },
    { name: "Unpaywall", repo: "ourresearch/unpaywall", purpose: "100% legal open-access full-text retrieval" },
    { name: "Docling", repo: "docling-project/docling", purpose: "Deep scientific document parsing & formula extraction" },
    { name: "GROBID", repo: "kermitt2/grobid", purpose: "TEI-XML bibliographic metadata extraction" },
    { name: "Hugging Face Datasets", repo: "huggingface/datasets", purpose: "Remote sensing & CV dataset streaming" },
    { name: "DVC", repo: "iterative/dvc", purpose: "Data versioning & pipeline reproducibility" },
    { name: "FiftyOne", repo: "voxel51/fiftyone", purpose: "Multitemporal visual dataset exploration" },
    { name: "Cleanlab", repo: "cleanlab/cleanlab", purpose: "Label error auditing & near-duplicate filtering" },
    { name: "PyTorch Lightning", repo: "Lightning-AI/pytorch-lightning", purpose: "Multi-GPU neural network training" },
    { name: "ClearML & MLflow", repo: "clearml/clearml", purpose: "Real-time telemetry & model registry" },
    { name: "Optuna", repo: "optuna/optuna", purpose: "Bayesian hyperparameter optimization" },
    { name: "Scikit-Learn", repo: "scikit-learn/scikit-learn", purpose: "ROC curves, confusion matrix, mIoU & Dice metrics" },
    { name: "LanguageTool", repo: "languagetool-org/languagetool", purpose: "Academic grammar verification & tone polishing" },
  ];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Hero Header */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-950 p-8 sm:p-12 border border-indigo-500/30 shadow-2xl">
        <div className="absolute -right-24 -top-24 h-96 w-96 rounded-full bg-gradient-to-br from-cyan-500/20 via-indigo-500/20 to-purple-500/30 blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <Badge className="bg-cyan-500/20 text-cyan-300 border-cyan-400/40">
              <Sparkles className="h-3.5 w-3.5 mr-1 text-cyan-300" /> Version 2.0 Production Release
            </Badge>
            <Badge className="bg-purple-500/20 text-purple-300 border-purple-400/40">
              Autonomous AI Research OS
            </Badge>
            <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-400/40">
              Open-Source & Compliant
            </Badge>
          </div>
          <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-white">
            About ResearchOS
          </h1>
          <p className="text-base sm:text-lg text-slate-300 max-w-3xl leading-relaxed">
            ResearchOS is an autonomous, full-stack AI research operating system designed to elevate scientific inquiry. We bridge the gap from preliminary hypothesis to an empirically validated, reproducible, and publication-ready IEEE research manuscript.
          </p>
        </div>
      </div>

      {/* Core Mission & Scientific Integrity */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-border/80 bg-card/60 backdrop-blur-xl shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg font-bold flex items-center gap-2 text-foreground">
              <Compass className="h-5 w-5 text-cyan-400" />
              The Mission: Solving Scientific Reproducibility
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground leading-relaxed">
            <p>
              In contemporary scientific research, researchers spend hundreds of hours searching literature paywalls, wrangling inconsistent dataset formats, debugging model training pipelines, and hand-crafting LaTeX submissions.
            </p>
            <p>
              <strong className="text-foreground">ResearchOS</strong> automates the entire academic lifecycle under rigorous scientific principles. Unlike superficial chat assistants, ResearchOS executes real neural network training, extracts empirical confusion matrices, and compiles camera-ready manuscripts without hallucinated citations or fabricated metrics.
            </p>
          </CardContent>
        </Card>

        <Card className="border-border/80 bg-card/60 backdrop-blur-xl shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg font-bold flex items-center gap-2 text-foreground">
              <Award className="h-5 w-5 text-amber-400" />
              Primary Benchmark Project
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground leading-relaxed">
            <p>
              The primary reference project baked into the platform is:
            </p>
            <div className="p-3 rounded-xl bg-blue-950/40 border border-blue-500/30 text-white font-medium text-xs space-y-1">
              <div className="text-cyan-400 font-bold uppercase tracking-wider text-[10px]">Reference Manuscript</div>
              <div>"Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery"</div>
              <div className="text-slate-400 text-[11px]">Target Venue: IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing (J-STARS)</div>
            </div>
            <p>
              Demonstrates 5 baseline and proposed models (Siamese U-Net, Swin Transformer, ResNet-50, Standard U-Net, MobileNetV3) evaluated strictly on a 20% held-out test set achieving 93.8% F1-score and 0.841 mIoU.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 4 Architectural Pillars */}
      <div>
        <h2 className="text-xl font-bold tracking-tight text-foreground mb-4 flex items-center gap-2">
          <Zap className="h-5 w-5 text-indigo-400" />
          The Four Architectural Pillars
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {pillars.map((pillar, idx) => {
            const Icon = pillar.icon;
            return (
              <Card key={idx} className={`border ${pillar.border} ${pillar.bg} shadow-md`}>
                <CardHeader className="flex flex-row items-center gap-3 pb-2 space-y-0">
                  <div className={`p-2 rounded-xl bg-background/80 ${pillar.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <CardTitle className="text-sm font-bold text-foreground">{pillar.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground leading-relaxed">{pillar.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* 16 Integrated Open Source Repositories */}
      <Card className="border-border/80 shadow-lg">
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center justify-between">
            <div className="flex items-center gap-2">
              <GitBranch className="h-5 w-5 text-purple-400" />
              <span>Mandatory Open-Source Integrations</span>
            </div>
            <Badge variant="outline" className="text-xs font-bold text-emerald-400 border-emerald-500/30">
              16 Repositories Connected
            </Badge>
          </CardTitle>
          <CardDescription className="text-xs">
            ResearchOS incorporates premier scientific software and AI frameworks respecting all upstream open-source licenses.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {repoIntegrations.map((repo, idx) => (
              <div key={idx} className="p-3 rounded-xl border border-border/60 bg-muted/20 hover:bg-muted/40 transition-colors space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-foreground">{repo.name}</span>
                  <a
                    href={`https://github.com/${repo.repo}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-cyan-400 transition-colors"
                  >
                    <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
                <div className="font-mono text-[10px] text-cyan-400 truncate">{repo.repo}</div>
                <p className="text-[11px] text-muted-foreground">{repo.purpose}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Launch Actions */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-blue-900/30 via-indigo-900/30 to-purple-900/30 border border-indigo-500/20">
        <div>
          <h3 className="text-base font-bold text-white">Ready to start an autonomous research project?</h3>
          <p className="text-xs text-slate-300">Explore paper discovery, configure dataset pipelines, or inspect model architectures.</p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/projects/new">
            <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-xs gap-1.5 shadow-md">
              <Sparkles className="h-3.5 w-3.5" /> Start New Project
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="outline" className="border-border text-xs font-semibold">
              Return to Dashboard
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
