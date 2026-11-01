"use client";

import React, { useState } from "react";
import {
  Workflow,
  Plus,
  Play,
  Save,
  Code2,
  Sparkles,
  Layers,
  ArrowRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function ModelArchitectureEditorPage() {
  const [selectedNode, setSelectedNode] = useState("Difference Module |T1 - T2|");

  const nodes = [
    { id: "1", name: "Temporal Input T1 (SAR VV/VH)", type: "Input", color: "border-blue-500 bg-blue-500/10 text-blue-400" },
    { id: "2", name: "Temporal Input T2 (SAR VV/VH)", type: "Input", color: "border-blue-500 bg-blue-500/10 text-blue-400" },
    { id: "3", name: "Encoder Stream 1 (Shared Weights)", type: "Conv + ResBlock", color: "border-purple-500 bg-purple-500/10 text-purple-400" },
    { id: "4", name: "Encoder Stream 2 (Shared Weights)", type: "Conv + ResBlock", color: "border-purple-500 bg-purple-500/10 text-purple-400" },
    { id: "5", name: "Difference Module |T1 - T2|", type: "Differential Fusion", color: "border-amber-500 bg-amber-500/10 text-amber-400" },
    { id: "6", name: "Multiscale Decoder with Skips", type: "Transposed Conv", color: "border-emerald-500 bg-emerald-500/10 text-emerald-400" },
    { id: "7", name: "Binary Change Classifier Head", type: "Output Mask", color: "border-rose-500 bg-rose-500/10 text-rose-400" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Model Architecture Editor</h2>
            <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
              React Flow (@xyflow)
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Visual topological editor for neural network components, skip pathways, and temporal difference operations.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-1.5 text-xs"
            onClick={() => toast.success("Generated PyTorch nn.Module source code synced to Code Editor!")}
          >
            <Code2 className="h-4 w-4" /> Generate PyTorch Code
          </Button>
          <Button
            size="sm"
            className="bg-blue-600 hover:bg-blue-500 text-white gap-1.5 text-xs"
            onClick={() => toast.success("Saved Architecture: Siamese U-Net v2.1")}
          >
            <Save className="h-4 w-4" /> Save Architecture
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Visual Graph Canvas */}
        <Card className="lg:col-span-3 border-border/80 h-[620px] flex flex-col overflow-hidden bg-slate-950/70">
          <CardHeader className="py-3 px-4 border-b border-border/60 bg-muted/20">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-foreground flex items-center gap-1.5">
                <Workflow className="h-4 w-4 text-purple-400" /> Siamese U-Net Graph Flow
              </span>
              <Badge variant="outline" className="text-[10px] font-mono">
                7 Nodes • 6 Skip Edges
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="flex-1 p-6 relative flex flex-col justify-center items-center gap-6 overflow-y-auto">
            {/* Interactive Graph Node Representation */}
            <div className="grid grid-cols-2 gap-8 w-full max-w-lg">
              <div
                onClick={() => setSelectedNode(nodes[0].name)}
                className={`p-3 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-sm ${nodes[0].color}`}
              >
                <span className="text-[10px] block opacity-75 font-mono">{nodes[0].type}</span>
                <span className="text-xs font-bold block mt-0.5">{nodes[0].name}</span>
              </div>
              <div
                onClick={() => setSelectedNode(nodes[1].name)}
                className={`p-3 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-sm ${nodes[1].color}`}
              >
                <span className="text-[10px] block opacity-75 font-mono">{nodes[1].type}</span>
                <span className="text-xs font-bold block mt-0.5">{nodes[1].name}</span>
              </div>
            </div>

            <div className="text-muted-foreground text-xs font-mono">↓ Twin Weight-Sharing Conv Streams ↓</div>

            <div className="grid grid-cols-2 gap-8 w-full max-w-lg">
              <div
                onClick={() => setSelectedNode(nodes[2].name)}
                className={`p-3 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-sm ${nodes[2].color}`}
              >
                <span className="text-[10px] block opacity-75 font-mono">{nodes[2].type}</span>
                <span className="text-xs font-bold block mt-0.5">{nodes[2].name}</span>
              </div>
              <div
                onClick={() => setSelectedNode(nodes[3].name)}
                className={`p-3 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-sm ${nodes[3].color}`}
              >
                <span className="text-[10px] block opacity-75 font-mono">{nodes[3].type}</span>
                <span className="text-xs font-bold block mt-0.5">{nodes[3].name}</span>
              </div>
            </div>

            <div className="text-muted-foreground text-xs font-mono">↓ Differential Subtraction |F1 - F2| ↓</div>

            <div
              onClick={() => setSelectedNode(nodes[4].name)}
              className={`p-4 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-md w-full max-w-sm ${nodes[4].color}`}
            >
              <span className="text-[10px] block opacity-75 font-mono">{nodes[4].type}</span>
              <span className="text-xs font-bold block mt-0.5">{nodes[4].name}</span>
            </div>

            <div className="text-muted-foreground text-xs font-mono">↓ Transposed Convolutions + Skip Fusion ↓</div>

            <div
              onClick={() => setSelectedNode(nodes[5].name)}
              className={`p-3 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-sm w-full max-w-sm ${nodes[5].color}`}
            >
              <span className="text-[10px] block opacity-75 font-mono">{nodes[5].type}</span>
              <span className="text-xs font-bold block mt-0.5">{nodes[5].name}</span>
            </div>

            <div
              onClick={() => setSelectedNode(nodes[6].name)}
              className={`p-3 rounded-xl border text-center cursor-pointer transition-all hover:scale-105 shadow-sm w-full max-w-sm ${nodes[6].color}`}
            >
              <span className="text-[10px] block opacity-75 font-mono">{nodes[6].type}</span>
              <span className="text-xs font-bold block mt-0.5">{nodes[6].name}</span>
            </div>
          </CardContent>
        </Card>

        {/* Node Properties Panel */}
        <Card className="border-border/80 h-[620px] flex flex-col justify-between">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-semibold">Layer Properties</CardTitle>
            <CardDescription className="text-xs">Selected: {selectedNode}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-xs flex-1">
            <div className="p-3 rounded-xl bg-muted/40 border border-border/60 space-y-2">
              <span className="text-muted-foreground block text-[11px]">Layer Type</span>
              <span className="font-semibold text-foreground">Cross-Temporal Differential Fusion</span>
            </div>

            <div className="space-y-1.5">
              <span className="text-muted-foreground block text-[11px]">Operation Formula</span>
              <code className="p-2 rounded bg-background border border-border block font-mono text-[11px]">
                delta_F = torch.abs(F1 - F2)
              </code>
            </div>

            <div className="space-y-1.5">
              <span className="text-muted-foreground block text-[11px]">Output Channels</span>
              <input
                type="number"
                defaultValue={128}
                className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs"
              />
            </div>

            <div className="space-y-1.5">
              <span className="text-muted-foreground block text-[11px]">Dropout Rate</span>
              <input
                type="number"
                step="0.05"
                defaultValue={0.2}
                className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs"
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

