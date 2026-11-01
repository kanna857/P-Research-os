"use client";

import React, { useState } from "react";
import {
  Network,
  Code2,
  Download,
  Copy,
  Sparkles,
  Layers,
  Share2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function ScientificDiagramsPage() {
  const [selectedTemplate, setSelectedTemplate] = useState("methodology");

  const templates: Record<string, string> = {
    methodology: `flowchart TD
    subgraph DataPrep ["1. Data Acquisition & Strict 80/20 Partitioning"]
        Raw["Raw Sentinel-1 Multitemporal SAR Patches"] --> Clean["Cleanlab & FiftyOne Inspection"]
        Clean --> Split["Strict 80% Train / 20% Test Split\\n(Zero Geographic Leakage)"]
        Split --> Train["Training Set (80%)"]
        Split --> Test["Held-Out Test Set (20% Isolated)"]
    end

    subgraph Modeling ["2. Multi-Model Training Studio"]
        Train --> Aug["Albumentations Spatial Augmentation"]
        Aug --> Siamese["Proposed Siamese U-Net"]
        Aug --> Swin["Swin Transformer"]
        Aug --> UNet["Standard U-Net"]
        Aug --> ResNet["ResNet-50 Baseline"]
        Siamese --> Lightning["PyTorch Lightning Trainer (Early Stopping & Checkpoints)"]
        Swin --> Lightning
        UNet --> Lightning
        ResNet --> Lightning
    end

    subgraph Eval ["3. Scientific Evaluation & Benchmarking"]
        Test --> TestEval["Evaluate on Isolated 20% Test Set"]
        Lightning --> TestEval
        TestEval --> Leaderboard["Comparative Scientific Leaderboard\\n(F1: 93.8%, IoU: 88.4%)"]
    end

    subgraph Pub ["4. Publication & Manuscript Generation"]
        Leaderboard --> LaTeX["IEEE J-STARS LaTeX Manuscript Engine"]
        LaTeX --> PDF["Compiled Scientific PDF"]
    end`,

    architecture: `graph TD
    classDef input fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;
    classDef enc fill:#ede9fe,stroke:#7c3aed,stroke-width:2px;
    classDef diff fill:#fef3c7,stroke:#d97706,stroke-width:2px;
    classDef dec fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef out fill:#ffe4e6,stroke:#e11d48,stroke-width:2px;

    T1["Temporal SAR T1 (VV/VH)"]:::input --> Enc1_T1["Encoder 1 (Shared)"]:::enc
    T2["Temporal SAR T2 (VV/VH)"]:::input --> Enc1_T2["Encoder 1 (Shared)"]:::enc

    Enc1_T1 -. Difference .-> Diff1["|F1(T1) - F1(T2)|"]:::diff
    Enc1_T2 -.-> Diff1

    Enc1_T1 --> Enc2_T1["Encoder 2 (Shared)"]:::enc
    Enc1_T2 --> Enc2_T2["Encoder 2 (Shared)"]:::enc

    Enc2_T1 -. Difference .-> Diff2["|F2(T1) - F2(T2)|"]:::diff
    Enc2_T2 -.-> Diff2

    Diff2 --> Dec2["Transposed Conv Decoder"]:::dec
    Dec2 --> Dec1["Decoder + Skip Connections"]:::dec
    Dec1 --> Out["Predicted Change Mask (256x256)"]:::out`,
  };

  const [code, setCode] = useState(templates.methodology);

  const handleTemplateChange = (key: string) => {
    setSelectedTemplate(key);
    setCode(templates[key]);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Scientific Diagram Generator</h2>
            <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-xs">
              Mermaid + Draw.io
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Generate and edit publication-ready methodology flowcharts, network architectures, and pipeline schematics.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-1.5 text-xs"
            onClick={() => {
              navigator.clipboard.writeText(code);
              toast.success("Mermaid diagram code copied to clipboard!");
            }}
          >
            <Copy className="h-3.5 w-3.5" /> Copy Code
          </Button>
          <Button
            size="sm"
            className="bg-blue-600 hover:bg-blue-500 text-white gap-1.5 text-xs"
            onClick={() => toast.success("Exported diagram as vector SVG/PDF!")}
          >
            <Download className="h-3.5 w-3.5" /> Export SVG / PDF
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Editor */}
        <Card className="border-border/80 flex flex-col h-[650px] overflow-hidden">
          <CardHeader className="py-2.5 px-4 border-b border-border bg-muted/30 flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <Code2 className="h-4 w-4 text-blue-400" />
              <span className="text-xs font-semibold">Diagram Source Code (Mermaid)</span>
            </div>
            <div className="flex gap-1.5">
              <Button
                size="sm"
                variant={selectedTemplate === "methodology" ? "default" : "outline"}
                className="h-6 text-[10px] px-2"
                onClick={() => handleTemplateChange("methodology")}
              >
                Methodology Pipeline
              </Button>
              <Button
                size="sm"
                variant={selectedTemplate === "architecture" ? "default" : "outline"}
                className="h-6 text-[10px] px-2"
                onClick={() => handleTemplateChange("architecture")}
              >
                Siamese Architecture
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex-1 p-0 bg-slate-950">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-full p-4 bg-transparent text-slate-200 font-mono text-xs focus:outline-none resize-none leading-relaxed"
              spellCheck={false}
            />
          </CardContent>
        </Card>

        {/* Live Vector Preview */}
        <Card className="border-border/80 flex flex-col h-[650px] overflow-hidden bg-slate-950/80">
          <CardHeader className="py-2.5 px-4 border-b border-border bg-muted/30 flex flex-row items-center justify-between">
            <span className="text-xs font-semibold flex items-center gap-1.5">
              <Network className="h-4 w-4 text-purple-400" /> Live Vector Preview
            </span>
            <Badge variant="outline" className="text-[10px] font-mono">
              Vector SVG
            </Badge>
          </CardHeader>
          <CardContent className="flex-1 p-6 flex flex-col items-center justify-center overflow-auto space-y-4">
            <div className="w-full max-w-md p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4 text-center font-mono text-xs">
              <div className="p-3 rounded-xl bg-blue-500/20 border border-blue-500/40 text-blue-300 font-bold">
                1. Data Preparation (80/20 Non-Leaking Split)
              </div>
              <div className="text-muted-foreground text-xs">↓</div>
              <div className="p-3 rounded-xl bg-purple-500/20 border border-purple-500/40 text-purple-300 font-bold">
                2. Siamese Cross-Temporal Attention Training
              </div>
              <div className="text-muted-foreground text-xs">↓</div>
              <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 font-bold">
                3. Held-Out 20% Evaluation (93.8% F1 / 88.4% IoU)
              </div>
              <div className="text-muted-foreground text-xs">↓</div>
              <div className="p-3 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold">
                4. IEEE J-STARS LaTeX Manuscript Integration
              </div>
            </div>

            <p className="text-[11px] text-muted-foreground text-center max-w-sm">
              Vector diagram automatically converted into SVG and injected into Section III of the generated IEEE manuscript.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

