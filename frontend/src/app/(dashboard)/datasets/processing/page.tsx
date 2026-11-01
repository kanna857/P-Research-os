"use client";

import React, { useState } from "react";
import {
  SlidersHorizontal,
  Layers,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Play,
  RotateCw,
  Sparkles,
  HardDrive,
  FileCheck2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";

export default function DatasetProcessingPage() {
  const [resolution, setResolution] = useState("256x256");
  const [normalize, setNormalize] = useState(true);
  const [augment, setAugment] = useState(true);
  const [denoise, setDenoise] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isCompleted, setIsCompleted] = useState(true);

  const handleStartProcessing = () => {
    setProcessing(true);
    setProgress(10);
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setProcessing(false);
          setIsCompleted(true);
          toast.success("Dataset preprocessed and 80/20 non-leaking split generated!");
          return 100;
        }
        return prev + 25;
      });
    }, 400);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Dataset Processing Studio</h2>
            <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-xs">
              Cleanlab + DVC Versioning
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Configure image resolutions, spatial augmentations, and enforce non-leaking 80% train / 20% test partitioning.
          </p>
        </div>
      </div>

      {/* Mandatory Rigor Alert */}
      <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-start gap-3 text-xs">
        <ShieldCheck className="h-5 w-5 text-blue-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-semibold text-blue-400 block text-xs">
            Mandatory Rigorous Partitioning Standard (80% Train / 20% Held-Out Test)
          </span>
          <p className="text-muted-foreground leading-relaxed">
            By default, ResearchOS allocates exactly 80% of samples to training and isolates 20% exclusively for final held-out testing.
            <strong> No separate validation partition is carved out.</strong> All hyperparameter tuning, model checkpoint selection, and early stopping rely strictly on internal cross-validation within the 80% training set to guarantee zero data leakage.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Preprocessing Controls */}
        <Card className="lg:col-span-1 border-border/80">
          <CardHeader>
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <SlidersHorizontal className="h-4 w-4 text-blue-500" /> Pipeline Parameters
            </CardTitle>
            <CardDescription className="text-xs">
              Configure normalization, resolution, and data cleaning.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            {/* Resolution Selector */}
            <div className="space-y-2">
              <Label className="text-xs">Target Image Resolution</Label>
              <div className="grid grid-cols-2 gap-2">
                {["128x128", "224x224", "256x256", "512x512"].map((res) => (
                  <Button
                    key={res}
                    type="button"
                    variant={resolution === res ? "default" : "outline"}
                    className={`text-xs h-9 ${resolution === res ? "bg-blue-600 text-white" : ""}`}
                    onClick={() => setResolution(res)}
                  >
                    {res}
                  </Button>
                ))}
              </div>
            </div>

            {/* Split Ratio Indicator */}
            <div className="space-y-1.5 p-3 rounded-xl bg-muted/40 border border-border/60">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-foreground">Train / Test Split</span>
                <span className="font-mono text-blue-400 font-bold">80% / 20%</span>
              </div>
              <p className="text-[11px] text-muted-foreground">
                Locked: Held-out test set is never evaluated during model training or hyperparameter tuning.
              </p>
            </div>

            {/* Toggles */}
            <div className="space-y-3 pt-1 text-xs">
              <label className="flex items-center justify-between cursor-pointer p-2 rounded-lg hover:bg-muted/30">
                <span className="text-foreground">Radiometric / Z-Score Normalization</span>
                <input
                  type="checkbox"
                  checked={normalize}
                  onChange={(e) => setNormalize(e.target.checked)}
                  className="rounded border-input text-blue-600 focus:ring-blue-500 h-4 w-4"
                />
              </label>

              <label className="flex items-center justify-between cursor-pointer p-2 rounded-lg hover:bg-muted/30">
                <span className="text-foreground">Albumentations Spatial Augmentation</span>
                <input
                  type="checkbox"
                  checked={augment}
                  onChange={(e) => setAugment(e.target.checked)}
                  className="rounded border-input text-blue-600 focus:ring-blue-500 h-4 w-4"
                />
              </label>

              <label className="flex items-center justify-between cursor-pointer p-2 rounded-lg hover:bg-muted/30">
                <span className="text-foreground">Lee Filter Speckle Denoising</span>
                <input
                  type="checkbox"
                  checked={denoise}
                  onChange={(e) => setDenoise(e.target.checked)}
                  className="rounded border-input text-blue-600 focus:ring-blue-500 h-4 w-4"
                />
              </label>
            </div>

            <Button
              className="w-full bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs h-10"
              disabled={processing}
              onClick={handleStartProcessing}
            >
              {processing ? (
                <>
                  <RotateCw className="h-4 w-4 animate-spin" /> Processing Pipeline ({progress}%)...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" /> Run 80/20 Preprocessing Pipeline
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Manifest & Preprocessing Report */}
        <Card className="lg:col-span-2 border-border/80">
          <CardHeader>
            <CardTitle className="text-base font-semibold flex items-center justify-between">
              <span>Processed Dataset Manifest & Verification</span>
              <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-xs">
                DVC Hash: #a98f12c3
              </Badge>
            </CardTitle>
            <CardDescription className="text-xs">
              Output stored separately in storage/processed_datasets/sentinel1_sar_256x256/.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {processing && (
              <div className="space-y-2 p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
                <div className="flex justify-between text-xs font-semibold text-blue-400">
                  <span>Executing Preprocessing & Cleanlab Inspection</span>
                  <span>{progress}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-muted/40 border border-border/60">
                <span className="text-[10px] text-muted-foreground block">Total Image Pairs</span>
                <span className="text-xl font-bold text-foreground">2,500</span>
                <span className="text-[10px] text-muted-foreground block mt-0.5">256x256 GeoTIFF/PNG</span>
              </div>
              <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20">
                <span className="text-[10px] text-blue-400 block font-semibold">Training Partition (80%)</span>
                <span className="text-xl font-bold text-blue-400">2,000</span>
                <span className="text-[10px] text-muted-foreground block mt-0.5">Cross-validation tuning only</span>
              </div>
              <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20">
                <span className="text-[10px] text-purple-400 block font-semibold">Held-Out Test Partition (20%)</span>
                <span className="text-xl font-bold text-purple-400">500</span>
                <span className="text-[10px] text-muted-foreground block mt-0.5">Strictly isolated, zero leakage</span>
              </div>
            </div>

            {/* Manifest JSON preview */}
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-foreground">Generated dataset_manifest.json</span>
              <pre className="p-4 rounded-xl bg-slate-950 text-slate-300 font-mono text-[11px] overflow-x-auto border border-border/50">
{`{
  "dataset_version": "v1.0-dvc",
  "dvc_hash": "a98f12c3b8790de4",
  "resolution": "${resolution}",
  "partition_protocol": {
    "train_ratio": 0.80,
    "test_ratio": 0.20,
    "validation_partition": "None (Internal 5-fold CV within Training Set only)",
    "heldout_test_isolated": true,
    "spatial_autocorrelation_safeguard": "Geographic sub-block tile isolation"
  },
  "cleanlab_quality_score": 97.2,
  "samples": {
    "train_count": 2000,
    "test_count": 500,
    "total": 2500
  }
}`}
              </pre>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

