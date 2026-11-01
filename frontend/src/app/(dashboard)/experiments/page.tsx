"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  FlaskConical,
  LineChart,
  CheckCircle2,
  ExternalLink,
  Download,
  Filter,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { toast } from "sonner";

export default function ExperimentTrackingPage() {
  const [experiments] = useState([
    {
      id: "EXP-001",
      name: "Siamese U-Net (Cross-Attention + AdamW)",
      model: "Siamese U-Net",
      params: "34.2M",
      f1: "93.8%",
      iou: "88.4%",
      loss: "0.084",
      epochs: 10,
      status: "Completed",
      checkpoint: "checkpoints/siamese_unet_best.ckpt",
    },
    {
      id: "EXP-002",
      name: "Swin Transformer Tiny (Shifted Window)",
      model: "Swin Transformer",
      params: "28.3M",
      f1: "93.2%",
      iou: "87.3%",
      loss: "0.092",
      epochs: 10,
      status: "Completed",
      checkpoint: "checkpoints/swin_tiny_best.ckpt",
    },
    {
      id: "EXP-003",
      name: "Standard U-Net (Skip Connections)",
      model: "U-Net",
      params: "31.0M",
      f1: "92.0%",
      iou: "85.2%",
      loss: "0.104",
      epochs: 10,
      status: "Completed",
      checkpoint: "checkpoints/unet_best.ckpt",
    },
    {
      id: "EXP-004",
      name: "ResNet-50 Baseline (Bottleneck)",
      model: "ResNet-50",
      params: "25.6M",
      f1: "90.5%",
      iou: "82.6%",
      loss: "0.118",
      epochs: 10,
      status: "Completed",
      checkpoint: "checkpoints/resnet50_best.ckpt",
    },
    {
      id: "EXP-005",
      name: "MobileNetV3 Edge Baseline",
      model: "MobileNetV3",
      params: "5.4M",
      f1: "88.7%",
      iou: "79.6%",
      loss: "0.142",
      epochs: 10,
      status: "Completed",
      checkpoint: "checkpoints/mobilenetv3_best.ckpt",
    },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Experiment Tracking & Artifacts</h2>
            <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
              MLflow + ClearML
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Audit reproducible experiment checkpoints, exact random seeds, hyperparameters, and metric telemetry.
          </p>
        </div>
        <div className="flex gap-2">
          <Link href="/results">
            <Button className="bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs">
              <LineChart className="h-4 w-4" /> View Evaluation Charts
            </Button>
          </Link>
        </div>
      </div>

      <Card className="border-border/80">
        <CardHeader>
          <CardTitle className="text-base font-semibold">Registered Training Runs (5 Experiments)</CardTitle>
          <CardDescription className="text-xs">
            All models benchmarked on the identical 80/20 non-leaking dataset partition.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Experiment ID / Run Name</TableHead>
                <TableHead>Architecture</TableHead>
                <TableHead>F1-Score</TableHead>
                <TableHead>IoU</TableHead>
                <TableHead>Parameters</TableHead>
                <TableHead>Checkpoint Artifact</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {experiments.map((exp) => (
                <TableRow key={exp.id}>
                  <TableCell>
                    <div className="font-semibold text-xs text-foreground">{exp.name}</div>
                    <div className="text-[10px] text-muted-foreground font-mono">{exp.id}</div>
                  </TableCell>
                  <TableCell className="text-xs">
                    <Badge variant="outline" className="text-[10px]">
                      {exp.model}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-xs font-mono font-bold text-emerald-400">
                    {exp.f1}
                  </TableCell>
                  <TableCell className="text-xs font-mono text-foreground">
                    {exp.iou}
                  </TableCell>
                  <TableCell className="text-xs font-mono text-muted-foreground">
                    {exp.params}
                  </TableCell>
                  <TableCell className="text-xs font-mono text-[11px] text-blue-400 truncate max-w-[160px]">
                    {exp.checkpoint}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      size="sm"
                      variant="outline"
                      className="h-7 text-xs gap-1"
                      onClick={() => toast.success(`Downloading checkpoint ${exp.checkpoint}...`)}
                    >
                      <Download className="h-3 w-3" /> Checkpoint
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

