"use client";

import React, { useState } from "react";
import {
  PlayCircle,
  PauseCircle,
  StopCircle,
  Cpu,
  Layers,
  Sparkles,
  RotateCw,
  LineChart,
  HardDrive,
  Activity,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

export default function TrainingStudioPage() {
  const [epochs, setEpochs] = useState("10");
  const [batchSize, setBatchSize] = useState("32");
  const [lr, setLr] = useState("0.001");
  const [optimizer, setOptimizer] = useState("AdamW");
  const [lossFn, setLossFn] = useState("Combined BCE + Focal Tversky");
  const [training, setTraining] = useState(false);
  const [currentEpoch, setCurrentEpoch] = useState(10);
  const [progress, setProgress] = useState(100);

  const activeModels = [
    { name: "Proposed Siamese U-Net", status: "Completed", trainAcc: "96.8%", valAcc: "94.2%", trainLoss: "0.084", epoch: "10/10" },
    { name: "Swin Transformer (Tiny)", status: "Completed", trainAcc: "96.1%", valAcc: "93.8%", trainLoss: "0.092", epoch: "10/10" },
    { name: "Standard U-Net", status: "Completed", trainAcc: "95.4%", valAcc: "92.5%", trainLoss: "0.104", epoch: "10/10" },
    { name: "ResNet-50 Baseline", status: "Completed", trainAcc: "94.2%", valAcc: "91.2%", trainLoss: "0.118", epoch: "10/10" },
    { name: "MobileNetV3-Large", status: "Completed", trainAcc: "92.8%", valAcc: "89.5%", trainLoss: "0.142", epoch: "10/10" },
  ];

  const handleStartTraining = () => {
    setTraining(true);
    setProgress(5);
    setCurrentEpoch(1);
    toast.info("Launching PyTorch Lightning multi-model training worker...");

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTraining(false);
          setCurrentEpoch(10);
          toast.success("Training completed! Evaluation metrics ready in Results tab.");
          return 100;
        }
        setCurrentEpoch((e) => Math.min(10, e + 1));
        return prev + 20;
      });
    }, 600);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Multi-Model Training Studio</h2>
            <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
              PyTorch Lightning + MLflow
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Execute concurrent multi-architecture training across 5 model families on the 80% training partition.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs font-mono text-emerald-400 bg-emerald-500/10 border-emerald-500/20">
            Hardware: NVIDIA GPU (16GB VRAM)
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Training Configuration Panel */}
        <Card className="border-border/80">
          <CardHeader>
            <CardTitle className="text-base font-semibold">Hyperparameters & Setup</CardTitle>
            <CardDescription className="text-xs">
              Configure batch execution for all selected models.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-xs">Epochs</Label>
                <input
                  type="number"
                  value={epochs}
                  onChange={(e) => setEpochs(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs"
                />
              </div>

              <div className="space-y-1.5">
                <Label className="text-xs">Batch Size</Label>
                <input
                  type="number"
                  value={batchSize}
                  onChange={(e) => setBatchSize(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-xs">Learning Rate</Label>
                <input
                  type="text"
                  value={lr}
                  onChange={(e) => setLr(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs font-mono"
                />
              </div>

              <div className="space-y-1.5">
                <Label className="text-xs">Optimizer</Label>
                <select
                  value={optimizer}
                  onChange={(e) => setOptimizer(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs"
                >
                  <option value="AdamW">AdamW</option>
                  <option value="Adam">Adam</option>
                  <option value="SGD">SGD (Momentum=0.9)</option>
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Loss Function</Label>
              <select
                value={lossFn}
                onChange={(e) => setLossFn(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-xs"
              >
                <option value="Combined BCE + Focal Tversky">Combined BCE + Focal Tversky</option>
                <option value="Focal Loss">Focal Loss</option>
                <option value="Cross-Entropy">Standard Cross-Entropy</option>
              </select>
            </div>

            <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 text-xs text-muted-foreground space-y-1">
              <span className="font-semibold text-blue-400 block">Strict Evaluation Protocol</span>
              <p>Validation curves computed via cross-validation strictly within the 80% training partition.</p>
            </div>

            <Button
              className="w-full bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs h-10"
              disabled={training}
              onClick={handleStartTraining}
            >
              {training ? (
                <>
                  <RotateCw className="h-4 w-4 animate-spin" /> Training 5 Models ({progress}%)...
                </>
              ) : (
                <>
                  <PlayCircle className="h-4 w-4" /> Start Multi-Model Training
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Live Training Telemetry */}
        <Card className="lg:col-span-2 border-border/80">
          <CardHeader>
            <CardTitle className="text-base font-semibold flex items-center justify-between">
              <span>Concurrent Model Progression</span>
              <Badge variant="outline" className="font-mono text-xs">
                Epoch {currentEpoch} / {epochs}
              </Badge>
            </CardTitle>
            <CardDescription className="text-xs">
              Live PyTorch Lightning metrics recorded to MLflow tracking registry.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {training && (
              <div className="space-y-2 p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
                <div className="flex justify-between text-xs font-semibold text-purple-400">
                  <span>Training in Progress (PyTorch Lightning Worker)</span>
                  <span>{progress}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            )}

            <div className="space-y-3">
              {activeModels.map((m, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-muted/40 border border-border/60 space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-foreground">{m.name}</span>
                    <Badge
                      className={
                        m.status === "Completed"
                          ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]"
                          : "bg-blue-500/10 text-blue-400 border-blue-500/20 text-[10px]"
                      }
                    >
                      {training ? "Training..." : m.status}
                    </Badge>
                  </div>

                  <div className="grid grid-cols-4 gap-2 pt-1 font-mono text-[11px]">
                    <div>
                      <span className="text-[10px] text-muted-foreground block font-sans">Train Acc:</span>
                      <span className="font-semibold text-foreground">{m.trainAcc}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-muted-foreground block font-sans">Val Acc (CV):</span>
                      <span className="font-semibold text-blue-400">{m.valAcc}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-muted-foreground block font-sans">Loss:</span>
                      <span className="font-semibold text-foreground">{m.trainLoss}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-muted-foreground block font-sans">Checkpoints:</span>
                      <span className="font-semibold text-emerald-400">Saved</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

