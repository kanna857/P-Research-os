"use client";

import React, { useState } from "react";
import {
  Layers,
  Filter,
  CheckCircle2,
  AlertCircle,
  Eye,
  BarChart3,
  HardDrive,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function DatasetExplorerPage() {
  const [filterSplit, setFilterSplit] = useState<"all" | "train" | "test">("all");

  const samples = [
    { id: "SAR_Pair_001", split: "train", class: "Changed", location: "Danube Basin", quality: "Clean (98.4%)", size: "256x256" },
    { id: "SAR_Pair_002", split: "train", class: "Unchanged", location: "Bavaria Urban", quality: "Clean (99.1%)", size: "256x256" },
    { id: "SAR_Pair_003", split: "train", class: "Changed", location: "Rhine Agricultural", quality: "Clean (97.8%)", size: "256x256" },
    { id: "SAR_Pair_004", split: "test", class: "Unchanged", location: "Vienna Outskirts", quality: "Clean (98.9%)", size: "256x256" },
    { id: "SAR_Pair_005", split: "test", class: "Changed", location: "Po Valley Flood", quality: "Clean (96.5%)", size: "256x256" },
    { id: "SAR_Pair_006", split: "train", class: "Unchanged", location: "Berlin Industrial", quality: "Clean (99.0%)", size: "256x256" },
  ];

  const filtered = filterSplit === "all" ? samples : samples.filter((s) => s.split === filterSplit);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Dataset Explorer</h2>
            <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
              FiftyOne + CleanVision
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Visual inspection of image pairs, Cleanlab quality flags, and class distribution across partitions.
          </p>
        </div>

        {/* Filter buttons */}
        <div className="flex gap-1.5 p-1 rounded-lg bg-muted/60 border border-border">
          <Button
            size="sm"
            variant={filterSplit === "all" ? "default" : "ghost"}
            className="h-7 text-xs"
            onClick={() => setFilterSplit("all")}
          >
            All Samples (2,500)
          </Button>
          <Button
            size="sm"
            variant={filterSplit === "train" ? "default" : "ghost"}
            className="h-7 text-xs"
            onClick={() => setFilterSplit("train")}
          >
            Train 80% (2,000)
          </Button>
          <Button
            size="sm"
            variant={filterSplit === "test" ? "default" : "ghost"}
            className="h-7 text-xs"
            onClick={() => setFilterSplit("test")}
          >
            Held-Out Test 20% (500)
          </Button>
        </div>
      </div>

      {/* Quality Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="border-border/80">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs text-muted-foreground">Cleanlab Health Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-400">97.2 / 100</div>
            <p className="text-[11px] text-muted-foreground mt-0.5">High radiometric fidelity</p>
          </CardContent>
        </Card>

        <Card className="border-border/80">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs text-muted-foreground">Class Balance (Changed / Unchanged)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">16% / 84%</div>
            <p className="text-[11px] text-amber-400 mt-0.5">Moderate natural imbalance</p>
          </CardContent>
        </Card>

        <Card className="border-border/80">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs text-muted-foreground">Corrupted Images Detected</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-400">0</div>
            <p className="text-[11px] text-muted-foreground mt-0.5">100% GeoTIFF header integrity</p>
          </CardContent>
        </Card>

        <Card className="border-border/80">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs text-muted-foreground">Duplicate Filter</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">12 Purged</div>
            <p className="text-[11px] text-muted-foreground mt-0.5">Perceptual hashing filtered</p>
          </CardContent>
        </Card>
      </div>

      {/* Multitemporal Image Pairs Grid */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-foreground">
          Multitemporal Image Pairs ({filtered.length} Displayed)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((s) => (
            <Card key={s.id} className="border-border/80 overflow-hidden hover:border-primary/40 transition-colors">
              <div className="grid grid-cols-3 bg-slate-950 p-2 gap-1 border-b border-border/60">
                <div className="aspect-square bg-slate-800 rounded flex flex-col items-center justify-center p-1 border border-slate-700/50">
                  <span className="text-[9px] text-slate-400 uppercase font-mono">T1 (Pre)</span>
                  <div className="w-8 h-8 rounded bg-slate-700/60 my-auto flex items-center justify-center text-[10px] text-slate-300 font-mono">
                    SAR
                  </div>
                </div>
                <div className="aspect-square bg-slate-800 rounded flex flex-col items-center justify-center p-1 border border-slate-700/50">
                  <span className="text-[9px] text-slate-400 uppercase font-mono">T2 (Post)</span>
                  <div className="w-8 h-8 rounded bg-slate-700/60 my-auto flex items-center justify-center text-[10px] text-slate-300 font-mono">
                    SAR
                  </div>
                </div>
                <div className="aspect-square bg-slate-900 rounded flex flex-col items-center justify-center p-1 border border-blue-500/30">
                  <span className="text-[9px] text-blue-400 uppercase font-mono">Ground Truth</span>
                  <div className="w-8 h-8 rounded bg-blue-500/20 my-auto flex items-center justify-center text-[10px] text-blue-400 font-mono">
                    Mask
                  </div>
                </div>
              </div>

              <CardContent className="p-3 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-foreground font-mono">{s.id}</span>
                  <Badge
                    variant="outline"
                    className={
                      s.split === "train"
                        ? "text-blue-400 border-blue-500/30 bg-blue-500/10 text-[10px]"
                        : "text-purple-400 border-purple-500/30 bg-purple-500/10 text-[10px]"
                    }
                  >
                    {s.split.toUpperCase()} (80/20)
                  </Badge>
                </div>
                <div className="flex items-center justify-between text-[11px] text-muted-foreground">
                  <span>Location: {s.location}</span>
                  <Badge variant="secondary" className="text-[10px]">
                    {s.class}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

