"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Cpu,
  Check,
  Plus,
  PlayCircle,
  Sparkles,
  Layers,
  ArrowRight,
  Code2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function ModelLibraryPage() {
  const [selectedModels, setSelectedModels] = useState<Record<string, boolean>>({
    "siamese-unet": true,
    "resnet-50": true,
    "unet-standard": true,
    "swin-transformer-tiny": true,
    "mobilenet-v3": true,
  });

  const models = [
    {
      id: "siamese-unet",
      name: "Proposed Siamese U-Net",
      family: "Siamese U-Net",
      params: "34.2M",
      category: "Change Detection",
      isPrimary: true,
      description:
        "Dual-branch weight-sharing encoders with multiscale cross-temporal differential feature subtraction and transposed convolution decoder.",
    },
    {
      id: "swin-transformer-tiny",
      name: "Swin Transformer (Tiny)",
      family: "Swin Transformer",
      params: "28.3M",
      category: "Hierarchical Vision Transformer",
      isPrimary: false,
      description:
        "Shifted window self-attention network providing linear computational complexity for dense geospatial change mapping.",
    },
    {
      id: "unet-standard",
      name: "Standard U-Net",
      family: "U-Net",
      params: "31.0M",
      category: "Segmentation Baseline",
      isPrimary: false,
      description:
        "Symmetric encoder-decoder topology with skip connections directly concatenating early spatial features to decoder stages.",
    },
    {
      id: "resnet-50",
      name: "ResNet-50 Baseline",
      family: "ResNet",
      params: "25.6M",
      category: "Convolutional Baseline",
      isPrimary: false,
      description:
        "Deep residual learning framework with bottleneck blocks, serving as standard comparative baseline for remote sensing tasks.",
    },
    {
      id: "mobilenet-v3",
      name: "MobileNetV3-Large",
      family: "MobileNet",
      params: "5.4M",
      category: "Lightweight Baseline",
      isPrimary: false,
      description:
        "Hardware-efficient inverted bottleneck architecture with squeeze-and-excitation attention for low-latency satellite edge inference.",
    },
    {
      id: "densenet-121",
      name: "DenseNet-121",
      family: "DenseNet",
      params: "8.0M",
      category: "Densely Connected",
      isPrimary: false,
      description:
        "Direct connections from every layer to all subsequent layers, maximizing feature propagation and gradient flow.",
    },
  ];

  const toggleSelect = (id: string) => {
    setSelectedModels((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const selectedCount = Object.values(selectedModels).filter(Boolean).length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Model Library & Architectures</h2>
            <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-xs">
              PyTorch Lightning + Torchvision
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Select candidate model families for comparative benchmarking or build custom architectures.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" className="text-xs px-3 py-1 font-mono">
            {selectedCount} Models Selected for Training
          </Badge>
          <Link href="/training">
            <Button className="bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs">
              <PlayCircle className="h-4 w-4" /> Open Training Studio
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {models.map((m) => {
          const selected = !!selectedModels[m.id];
          return (
            <Card
              key={m.id}
              className={`border transition-all flex flex-col justify-between ${
                selected
                  ? "border-blue-500/60 bg-blue-500/5 shadow-md shadow-blue-500/5"
                  : "border-border/80 hover:border-border"
              }`}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-[10px] text-muted-foreground">
                        {m.category}
                      </Badge>
                      {m.isPrimary && (
                        <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30 text-[10px] gap-1">
                          <Sparkles className="h-2.5 w-2.5" /> Proposed
                        </Badge>
                      )}
                    </div>
                    <CardTitle className="text-base font-bold text-foreground">{m.name}</CardTitle>
                  </div>
                  <Badge variant="secondary" className="font-mono text-xs">
                    {m.params}
                  </Badge>
                </div>
              </CardHeader>

              <CardContent className="space-y-4 flex-1 flex flex-col justify-between">
                <p className="text-xs text-muted-foreground leading-relaxed">{m.description}</p>

                <div className="flex items-center justify-between pt-2 border-t border-border/50">
                  <Link href={`/models/editor?model=${m.id}`} className="text-xs text-blue-400 hover:underline flex items-center gap-1">
                    <Code2 className="h-3.5 w-3.5" /> Edit Layers
                  </Link>

                  <Button
                    size="sm"
                    variant={selected ? "default" : "outline"}
                    className={`h-8 text-xs gap-1.5 ${selected ? "bg-blue-600 hover:bg-blue-500 text-white" : ""}`}
                    onClick={() => toggleSelect(m.id)}
                  >
                    {selected ? (
                      <>
                        <Check className="h-3.5 w-3.5" /> Selected for Studio
                      </>
                    ) : (
                      <>
                        <Plus className="h-3.5 w-3.5" /> Select Model
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

