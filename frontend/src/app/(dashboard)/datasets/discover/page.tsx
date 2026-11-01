"use client";

import React, { useState } from "react";
import {
  Database,
  Search,
  Download,
  Upload,
  ExternalLink,
  Layers,
  HardDrive,
  FileCheck,
  CheckCircle2,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function DatasetDiscoveryPage() {
  const [query, setQuery] = useState("Sentinel-1 SAR change detection");
  const [imported, setImported] = useState<Record<string, boolean>>({ "sentinel1-sar": true });

  const datasets = [
    {
      id: "sentinel1-sar",
      name: "Sentinel-1 SAR Multitemporal Change Detection Benchmark",
      source: "Copernicus / Zenodo",
      license: "CC-BY-4.0",
      samples: "12,450 Image Pairs",
      classes: ["Unchanged", "Changed"],
      dimensions: "256x256",
      channels: "2 (VV / VH SAR Polarizations)",
      format: "GeoTIFF / PNG",
      size: "2.4 GB",
      suitability: "Primary benchmark for SAR deep learning experiments",
      description:
        "Dual-polarized multitemporal Sentinel-1 SAR imagery acquired over urban, agricultural, and coastal flood zones with co-registered ground truth masks.",
    },
    {
      id: "spacenet-7",
      name: "SpaceNet 7 Multi-Temporal Urban Development Challenge",
      source: "Hugging Face Hub / AWS",
      license: "CC-BY-SA-4.0",
      samples: "40,100 Tiled Patches",
      classes: ["Background", "Building Footprint"],
      dimensions: "1024x1024",
      channels: "3 (RGB Optical)",
      format: "GeoTIFF",
      size: "18.5 GB",
      suitability: "Benchmark for long-baseline multi-year development tracking",
      description:
        "Global planet satellite imagery tracking monthly rapid urbanization across 24 distinct geographic sites.",
    },
    {
      id: "oscd-onera",
      name: "OSCD: Onera Satellite Change Detection Dataset",
      source: "IEEE Dataport",
      license: "Open Data",
      samples: "2,400 Multispectral Pairs",
      classes: ["No Change", "Change"],
      dimensions: "224x224 (Tiled)",
      channels: "13 (Multispectral)",
      format: "GeoTIFF / NumPy",
      size: "850 MB",
      suitability: "Widely cited in IEEE J-STARS literature for multispectral baselines",
      description:
        "Sentinel-2 registered multispectral image pairs across 24 global cities with manually verified change masks.",
    },
  ];

  const handleImport = (id: string, name: string) => {
    setImported({ ...imported, [id]: true });
    toast.success(`Imported "${name.slice(0, 30)}..." into Dataset Studio!`);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Dataset Discovery Agent</h2>
            <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-xs">
              Hugging Face Hub + Zenodo
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Search, discover, and import scientific datasets for remote sensing and computer vision benchmarks.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-2 text-xs"
            onClick={() => toast.info("Drag and drop custom dataset folder or ZIP archive...")}
          >
            <Upload className="h-4 w-4" /> Upload Custom Dataset
          </Button>
        </div>
      </div>

      <Card className="border-border/80">
        <CardContent className="pt-6">
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search datasets by modality (SAR, Optical, LiDAR), task, or sensor..."
                className="pl-10 h-10"
              />
            </div>
            <Button className="bg-blue-600 hover:bg-blue-500 text-white gap-2">
              <Search className="h-4 w-4" /> Search Hugging Face & Zenodo
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
          <span>Found 3 scientific datasets matching query</span>
          <span className="text-blue-400 flex items-center gap-1">
            <Sparkles className="h-3.5 w-3.5" /> DVC-ready manifests
          </span>
        </div>

        {datasets.map((d) => {
          const isImp = imported[d.id];
          return (
            <Card key={d.id} className="border-border/80 hover:border-primary/40 transition-colors">
              <CardContent className="p-5 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge variant="outline" className="text-xs text-blue-400">
                        {d.source}
                      </Badge>
                      <Badge variant="secondary" className="text-[10px]">
                        License: {d.license}
                      </Badge>
                      <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                        {d.suitability}
                      </Badge>
                    </div>
                    <h3 className="text-base font-bold text-foreground">{d.name}</h3>
                    <p className="text-xs text-muted-foreground leading-relaxed">{d.description}</p>
                  </div>

                  <div className="shrink-0">
                    <Button
                      size="sm"
                      variant={isImp ? "secondary" : "default"}
                      className={`gap-1.5 text-xs h-8 ${!isImp ? "bg-blue-600 hover:bg-blue-500 text-white" : ""}`}
                      onClick={() => handleImport(d.id, d.name)}
                    >
                      {isImp ? (
                        <>
                          <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> Imported in Studio
                        </>
                      ) : (
                        <>
                          <Download className="h-3.5 w-3.5" /> Import to Studio
                        </>
                      )}
                    </Button>
                  </div>
                </div>

                {/* Dataset Specifications Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-xs">
                  <div className="p-2.5 rounded-lg bg-muted/40 border border-border/50">
                    <span className="text-[10px] text-muted-foreground block">Total Records:</span>
                    <span className="font-semibold text-foreground">{d.samples}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-muted/40 border border-border/50">
                    <span className="text-[10px] text-muted-foreground block">Dimensions:</span>
                    <span className="font-semibold text-foreground">{d.dimensions}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-muted/40 border border-border/50">
                    <span className="text-[10px] text-muted-foreground block">Channels:</span>
                    <span className="font-semibold text-foreground">{d.channels}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-muted/40 border border-border/50">
                    <span className="text-[10px] text-muted-foreground block">Download Size:</span>
                    <span className="font-semibold text-foreground">{d.size}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

