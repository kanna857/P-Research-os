"use client";

import React from "react";
import Link from "next/link";
import {
  BookOpen,
  Database,
  Cpu,
  FileCheck2,
  TrendingUp,
  Sparkles,
  ArrowUpRight,
  Target,
  PlayCircle,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

export default function DashboardPage() {
  const stats = [
    { title: "Literature Papers", value: "38", subtext: "14 Open Access full-text", icon: BookOpen, color: "text-blue-500", bg: "bg-blue-500/10" },
    { title: "Datasets Processed", value: "3", subtext: "80% Train / 20% Test (Strict)", icon: Database, color: "text-emerald-500", bg: "bg-emerald-500/10" },
    { title: "Candidate Models", value: "5", subtext: "Siamese U-Net leads (93.8% F1)", icon: Cpu, color: "text-purple-500", bg: "bg-purple-500/10" },
    { title: "Manuscript Progress", value: "85%", subtext: "IEEE J-STARS ready", icon: FileCheck2, color: "text-amber-500", bg: "bg-amber-500/10" },
  ];

  const pipelineStages = [
    { name: "Literature & Gap Analysis", status: "Completed", desc: "OpenAlex & STORM synthesis", progress: 100 },
    { name: "Dataset Studio (80/20 Split)", status: "Completed", desc: "Cleanlab & DVC manifest", progress: 100 },
    { name: "Multi-Model Training", status: "Completed", desc: "PyTorch Lightning 10 epochs", progress: 100 },
    { name: "Scientific Evaluation", status: "Completed", desc: "Held-out test set verified", progress: 100 },
    { name: "IEEE Manuscript & LaTeX", status: "In Progress", desc: "Results and citations synced", progress: 85 },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-900/40 via-indigo-900/30 to-purple-900/30 p-8 border border-blue-500/20 shadow-lg">
        <div className="relative z-10 max-w-3xl space-y-3">
          <Badge className="bg-blue-500/20 text-blue-400 hover:bg-blue-500/30 border-blue-500/30">
            <Sparkles className="h-3.5 w-3.5 mr-1" /> Autonomous AI Research Operating System
          </Badge>
          <h2 className="text-3xl font-extrabold tracking-tight text-white">
            Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery
          </h2>
          <p className="text-sm text-slate-300">
            Autonomous pipeline transitioning from research questions to an empirically verified, publication-ready IEEE J-STARS manuscript.
          </p>
          <div className="flex flex-wrap gap-3 pt-2">
            <Link href="/training">
              <Button className="bg-blue-600 hover:bg-blue-500 text-white gap-2 shadow-md">
                <PlayCircle className="h-4 w-4" /> View Training Studio
              </Button>
            </Link>
            <Link href="/journal">
              <Button variant="outline" className="border-border gap-2">
                <FileCheck2 className="h-4 w-4" /> Open IEEE Manuscript
              </Button>
            </Link>
            <Link href="/export">
              <Button variant="secondary" className="gap-2">
                <ArrowUpRight className="h-4 w-4" /> Export Reproducibility Bundle
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s, idx) => {
          const Icon = s.icon;
          return (
            <Card key={idx} className="border-border/80 shadow-xs hover:border-primary/40 transition-colors">
              <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                <CardTitle className="text-xs font-medium text-muted-foreground">{s.title}</CardTitle>
                <div className={`p-2 rounded-xl ${s.bg} ${s.color}`}>
                  <Icon className="h-4 w-4" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold tracking-tight">{s.value}</div>
                <p className="text-xs text-muted-foreground mt-1">{s.subtext}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Pipeline Progress and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Research Pipeline Stages */}
        <Card className="lg:col-span-2 border-border/80">
          <CardHeader>
            <CardTitle className="text-base font-semibold flex items-center justify-between">
              <span>Scientific Pipeline Execution</span>
              <Badge variant="outline" className="text-emerald-500 border-emerald-500/30 bg-emerald-500/10">
                Active Benchmark
              </Badge>
            </CardTitle>
            <CardDescription className="text-xs">
              End-to-end reproducibility pipeline verified against held-out 20% test partition.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {pipelineStages.map((st, i) => (
              <div key={i} className="space-y-1.5 p-3 rounded-xl bg-muted/30 border border-border/50">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-foreground flex items-center gap-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
                    {st.name}
                  </span>
                  <span className="text-muted-foreground font-mono">{st.progress}%</span>
                </div>
                <p className="text-[11px] text-muted-foreground">{st.desc}</p>
                <Progress value={st.progress} className="h-1.5 bg-muted" />
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Benchmark Highlights */}
        <Card className="border-border/80">
          <CardHeader>
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <Target className="h-4 w-4 text-blue-500" /> Empirical Benchmark
            </CardTitle>
            <CardDescription className="text-xs">
              Held-out 20% test set evaluations (No validation leakage)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1">
              <div className="flex justify-between text-xs font-semibold text-blue-400">
                <span>Proposed Siamese U-Net</span>
                <span>F1: 93.8%</span>
              </div>
              <p className="text-[11px] text-muted-foreground">IoU: 88.4% • Test Acc: 94.2%</p>
            </div>

            <div className="p-3 rounded-xl bg-muted/40 border border-border/50 space-y-1">
              <div className="flex justify-between text-xs font-semibold">
                <span>Swin Transformer (Tiny)</span>
                <span>F1: 93.2%</span>
              </div>
              <p className="text-[11px] text-muted-foreground">IoU: 87.3% • Test Acc: 93.8%</p>
            </div>

            <div className="p-3 rounded-xl bg-muted/40 border border-border/50 space-y-1">
              <div className="flex justify-between text-xs font-semibold">
                <span>Standard U-Net</span>
                <span>F1: 92.0%</span>
              </div>
              <p className="text-[11px] text-muted-foreground">IoU: 85.2% • Test Acc: 92.5%</p>
            </div>

            <div className="p-3 rounded-xl bg-muted/40 border border-border/50 space-y-1">
              <div className="flex justify-between text-xs font-semibold">
                <span>ResNet-50 Baseline</span>
                <span>F1: 90.5%</span>
              </div>
              <p className="text-[11px] text-muted-foreground">IoU: 82.6% • Test Acc: 91.2%</p>
            </div>

            <div className="pt-2">
              <Link href="/results">
                <Button variant="outline" className="w-full text-xs">
                  Inspect All 5 Models & ROC Curves
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

