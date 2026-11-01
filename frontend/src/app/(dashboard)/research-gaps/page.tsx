"use client";

import React, { useState } from "react";
import {
  Target,
  Sparkles,
  ShieldAlert,
  CheckCircle2,
  HelpCircle,
  Lightbulb,
  ArrowRight,
  TrendingUp,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function ResearchGapsPage() {
  const gaps = [
    {
      id: "gap-1",
      title: "Severe Class Imbalance in Sparse Change Targets",
      severity: "High",
      category: "Empirical Limitation",
      description:
        "Existing SAR literature frequently relies on standard cross-entropy or generic focal loss. When changed pixels occupy less than 3% of spatial coverage, models degenerate towards predicting 'no change', yielding high nominal accuracy but catastrophic recall.",
      recommended_direction:
        "Formulate a combined Focal-Tversky loss function with asymmetric spatial weighting tailored for multitemporal radar backscatter.",
    },
    {
      id: "gap-2",
      title: "High False Alarm Rates Under Speckle & Soil Moisture Fluctuations",
      severity: "Critical",
      category: "Theoretical & Physical Limitation",
      description:
        "Single-branch differencing networks fail to decouple genuine structural changes (e.g. building construction, flooding) from environmental speckle noise and seasonal soil moisture variations.",
      recommended_direction:
        "Deploy a dual-branch Siamese U-Net with cross-temporal attention gates to align feature manifolds before spatial subtraction.",
    },
    {
      id: "gap-3",
      title: "Data Leakage from Random Pixel Partitioning",
      severity: "High",
      category: "Methodological Defect in Prior Literature",
      description:
        "Numerous published studies partition datasets by randomly splitting pixel patches. Due to spatial autocorrelation, training patches share identical neighborhoods with test samples, artificially inflating reported F1-scores by 6% to 11%.",
      recommended_direction:
        "Enforce strict geographically isolated 80% train / 20% test partitioning with zero spatial overlap.",
    },
  ];

  const hypotheses = [
    {
      id: "H1",
      statement:
        "A Siamese U-Net featuring multiscale cross-attention feature subtraction will achieve an F1-score >= 93.0% on Sentinel-1 SAR benchmarks, surpassing standard ResNet-50 baselines by at least 3.0%.",
      confidence: "88% Estimated Confidence",
      tag: "AI-Generated Hypothesis (Requires Empirical Validation)",
      isVerified: false,
    },
    {
      id: "H2",
      statement:
        "Enforcing strict 80/20 non-leaking geographic block partitioning will eliminate artificial spatial autocorrelation inflation and produce scientifically defensible test results.",
      confidence: "98% Methodological Standard",
      tag: "Methodologically Verified Requirement",
      isVerified: true,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold tracking-tight">Research Gap & Novelty Agent</h2>
          <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
            LangGraph Multi-Agent
          </Badge>
        </div>
        <p className="text-xs text-muted-foreground">
          Autonomous identification of theoretical and empirical limitations, baseline models, and formulated research hypotheses.
        </p>
      </div>

      {/* Identified Gaps */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider text-[11px] text-muted-foreground">
          Critical Gaps Identified Across Literature Collection
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {gaps.map((g) => (
            <Card key={g.id} className="border-border/80 hover:border-primary/40 transition-colors">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-amber-400 border-amber-500/30 bg-amber-500/10 text-xs">
                      {g.category}
                    </Badge>
                    <Badge variant={g.severity === "Critical" ? "destructive" : "secondary"} className="text-xs">
                      {g.severity} Priority
                    </Badge>
                  </div>
                  <span className="text-[10px] text-muted-foreground font-mono">{g.id}</span>
                </div>

                <h4 className="text-base font-bold text-foreground">{g.title}</h4>
                <p className="text-xs text-muted-foreground leading-relaxed">{g.description}</p>

                <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1">
                  <span className="text-xs font-semibold text-blue-400 flex items-center gap-1.5">
                    <Lightbulb className="h-3.5 w-3.5" /> Recommended Research Direction:
                  </span>
                  <p className="text-xs text-muted-foreground">{g.recommended_direction}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Novelty Hypotheses */}
      <div className="space-y-4 pt-2">
        <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider text-[11px] text-muted-foreground">
          Formulated Research Hypotheses & Evidence Classification
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {hypotheses.map((h) => (
            <Card key={h.id} className="border-border/80">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="font-mono text-xs">
                    Hypothesis {h.id}
                  </Badge>
                  <Badge
                    className={
                      h.isVerified
                        ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]"
                        : "bg-blue-500/10 text-blue-400 border-blue-500/20 text-[10px]"
                    }
                  >
                    {h.tag}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-xs text-foreground leading-relaxed font-medium">
                  &quot;{h.statement}&quot;
                </p>
                <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-2 border-t border-border/50">
                  <span>Confidence: {h.confidence}</span>
                  <span className="text-blue-400">Tested in Section V</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

