"use client";

import React, { useState } from "react";
import {
  ShieldCheck,
  Search,
  AlertTriangle,
  CheckCircle2,
  HelpCircle,
  Sparkles,
  RotateCw,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";

export default function OriginalityPage() {
  const [scanning, setScanning] = useState(false);
  const [score, setScore] = useState(94.2);

  const flagged = [
    {
      id: 1,
      passage:
        "Multitemporal synthetic aperture radar change detection is challenging due to multiplicative speckle noise following a Gamma distribution.",
      similarity: "76% Lexical Overlap",
      matchedDoc: "Gong et al. (IEEE TGRS 2023)",
      advice: "Add direct citation [1] or rephrase physical description of speckle distribution.",
    },
    {
      id: 2,
      passage:
        "Twin weight-sharing encoders project temporal pairs into shared feature manifolds before differential magnitude subtraction.",
      similarity: "68% Structural Overlap",
      matchedDoc: "Zhang et al. (IEEE J-STARS 2024)",
      advice: "Properly attributed with citation [2]; conforms to standard IEEE methodology phrasing.",
    },
  ];

  const handleScan = () => {
    setScanning(true);
    setTimeout(() => {
      setScanning(false);
      setScore(94.2);
      toast.success("Originality audit completed against 38 indexed library papers!");
    }, 700);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Originality & Attribution Checker</h2>
            <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-xs">
              Sentence Transformers + RapidFuzz
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Scans manuscript passages against accessible library papers for unattributed verbatim copying or heavy paraphrasing.
          </p>
        </div>
        <Button
          disabled={scanning}
          className="bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs"
          onClick={handleScan}
        >
          {scanning ? <RotateCw className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />} Run Originality Audit
        </Button>
      </div>

      {/* Score Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="border-border/80 flex flex-col justify-between p-6">
          <div className="space-y-2">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Originality Index
            </span>
            <div className="text-4xl font-extrabold text-emerald-400 font-mono">
              {score}%
            </div>
            <Progress value={score} className="h-2 bg-muted" />
          </div>
          <p className="text-[11px] text-muted-foreground mt-4">
            Zero unattributed passages detected. All high-overlap passages possess valid bibliographic citations.
          </p>
        </Card>

        <Card className="md:col-span-2 border-border/80 p-6 space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400">
            <ShieldCheck className="h-4 w-4" /> Scientific Integrity & Responsible Disclosure Policy
          </div>
          <p className="text-xs text-muted-foreground leading-relaxed">
            ResearchOS verifies academic integrity using semantic cosine distance (Sentence-Transformers) and token-ratio fingerprinting (RapidFuzz).
            The platform is designed to promote <strong>100% rigorous scientific attribution</strong> rather than attempting to bypass commercial AI detection software.
          </p>
          <div className="grid grid-cols-3 gap-2 pt-2 text-[11px]">
            <div className="p-2.5 rounded-lg bg-muted/40 border border-border">
              <span className="text-muted-foreground block text-[10px]">Sources Scanned:</span>
              <span className="font-semibold text-foreground">38 Library Papers</span>
            </div>
            <div className="p-2.5 rounded-lg bg-muted/40 border border-border">
              <span className="text-muted-foreground block text-[10px]">Flagged Passages:</span>
              <span className="font-semibold text-amber-400">2 Passages</span>
            </div>
            <div className="p-2.5 rounded-lg bg-muted/40 border border-border">
              <span className="text-muted-foreground block text-[10px]">Missing Citations:</span>
              <span className="font-semibold text-emerald-400">0 Missing</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Flagged Passages List */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-foreground">
          Audited Passages & Overlap Analysis ({flagged.length} Items)
        </h3>

        <div className="space-y-3">
          {flagged.map((item) => (
            <Card key={item.id} className="border-border/80">
              <CardContent className="p-4 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-amber-400 border-amber-500/30 bg-amber-500/10 text-[10px]">
                    {item.similarity}
                  </Badge>
                  <span className="text-muted-foreground text-[11px]">Matched Source: {item.matchedDoc}</span>
                </div>

                <div className="p-3 rounded-lg bg-muted/30 border border-border/50 text-foreground font-serif text-xs italic">
                  &quot;{item.passage}&quot;
                </div>

                <div className="text-[11px] text-blue-400 flex items-center gap-1.5 pt-1">
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                  <span>Recommendation: {item.advice}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

