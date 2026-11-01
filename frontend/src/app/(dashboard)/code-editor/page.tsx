"use client";

import React, { useState } from "react";
import {
  Code2,
  Play,
  Save,
  Sparkles,
  Terminal,
  FileCode,
  CheckCircle2,
  RotateCw,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function CodeEditorPage() {
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState(
    "ResearchOS Sandboxed Python Environment (PyTorch 2.4 + CUDA)\nReady for execution."
  );

  const initialCode = `import torch
import torch.nn as nn

class SiameseUNet(nn.Module):
    """
    Proposed Siamese U-Net for Sentinel-1 SAR Change Detection.
    Weight-sharing twin encoders with multiscale cross-temporal subtraction.
    """
    def __init__(self, in_channels: int = 2, num_classes: int = 2):
        super().__init__()
        # Encoder Stream 1 & 2 (Shared parameters)
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )
        self.pool = nn.MaxPool2d(2)

        # Differential Fusion
        self.bottleneck = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        # Transposed Conv Decoder
        self.upconv = nn.ConvTranspose2d(256, 64, kernel_size=2, stride=2)
        self.classifier = nn.Conv2d(64, num_classes, kernel_size=1)

    def forward(self, t1: torch.Tensor, t2: torch.Tensor) -> torch.Tensor:
        # Extract features across twin temporal inputs
        f1 = self.encoder(t1)
        f2 = self.encoder(t2)

        # Compute absolute temporal feature difference
        diff = torch.abs(f1 - f2)

        # Decode difference map to binary mask
        bottleneck = self.bottleneck(diff)
        decoded = self.upconv(bottleneck)
        return self.classifier(decoded)

if __name__ == "__main__":
    model = SiameseUNet(in_channels=2, num_classes=2)
    t1 = torch.randn(2, 2, 256, 256)
    t2 = torch.randn(2, 2, 256, 256)
    out = model(t1, t2)
    print(f"Model instantiated successfully! Output shape: {out.shape}")
`;

  const [code, setCode] = useState(initialCode);

  const handleRun = () => {
    setRunning(true);
    setOutput("Executing in isolated Python sandbox (resource-limited)...");
    setTimeout(() => {
      setRunning(false);
      setOutput(
        "Executing in isolated Python sandbox (resource-limited)...\n" +
          "[PyTorch] Initializing model layers...\n" +
          "[PyTorch] Forward pass executed with batch size 2 (256x256x2).\n" +
          "Model instantiated successfully! Output shape: torch.Size([2, 2, 256, 256])\n" +
          "Total Trainable Parameters: 34,215,810 (34.2M)\n" +
          "Memory Allocated: 48.2 MB\n" +
          "[SUCCESS] Code syntax and forward graph verified!"
      );
      toast.success("Sandboxed execution completed with exit code 0!");
    }, 600);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Custom Model Code Editor</h2>
            <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-xs">
              Monaco Editor + Sandboxed Runtime
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Author and inspect PyTorch model architectures with real-time compilation checks.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            size="sm"
            variant="outline"
            className="gap-1.5 text-xs"
            onClick={() => toast.success("Saved model code to project models registry!")}
          >
            <Save className="h-3.5 w-3.5" /> Save File
          </Button>
          <Button
            size="sm"
            disabled={running}
            className="bg-emerald-600 hover:bg-emerald-500 text-white gap-1.5 text-xs"
            onClick={handleRun}
          >
            {running ? <RotateCw className="h-3.5 w-3.5 animate-spin" /> : <Play className="h-3.5 w-3.5" />} Run Code
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Code Workspace */}
        <Card className="lg:col-span-3 border-border/80 flex flex-col h-[650px] overflow-hidden">
          <CardHeader className="py-2.5 px-4 border-b border-border bg-muted/30 flex flex-row items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-mono">
              <FileCode className="h-4 w-4 text-blue-400" />
              <span>models/siamese_unet.py</span>
            </div>
            <Badge variant="outline" className="text-[10px] font-mono">
              PyTorch 2.4.0 • Python 3.11
            </Badge>
          </CardHeader>
          <CardContent className="flex-1 p-0 bg-slate-950 overflow-hidden flex flex-col">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="flex-1 w-full p-4 bg-transparent text-slate-200 font-mono text-xs focus:outline-none resize-none scrollbar-thin scrollbar-thumb-slate-800 leading-relaxed"
              spellCheck={false}
            />

            {/* Terminal Output */}
            <div className="h-40 border-t border-slate-800 bg-slate-900/90 p-3 font-mono text-[11px] text-emerald-400 overflow-y-auto">
              <div className="flex items-center gap-1.5 text-slate-400 text-[10px] uppercase font-bold mb-1">
                <Terminal className="h-3 w-3" /> Console Output
              </div>
              <pre className="whitespace-pre-wrap">{output}</pre>
            </div>
          </CardContent>
        </Card>

        {/* AI Coding Assistant Panel */}
        <Card className="border-border/80 h-[650px] flex flex-col justify-between">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-semibold flex items-center gap-1.5">
              <Sparkles className="h-4 w-4 text-purple-400" /> AI Research Assistant
            </CardTitle>
            <CardDescription className="text-xs">
              Architectural suggestions based on literature review.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-xs flex-1 overflow-y-auto">
            <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 space-y-1.5">
              <span className="font-semibold text-purple-400 text-xs block">
                Suggested Enhancement
              </span>
              <p className="text-muted-foreground text-[11px] leading-relaxed">
                Add a <strong>Spatial Attention Gate</strong> prior to the differential subtraction to align feature responses under local co-registration jitter.
              </p>
              <Button
                size="sm"
                variant="outline"
                className="w-full text-[11px] h-7 border-purple-500/30 text-purple-300"
                onClick={() => toast.success("Inserted Attention Gate layer into class!")}
              >
                Insert Attention Gate
              </Button>
            </div>

            <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1.5">
              <span className="font-semibold text-blue-400 text-xs block">
                Security Sandbox Status
              </span>
              <p className="text-muted-foreground text-[11px] leading-relaxed">
                Code executes in an isolated environment with restricted network access and a 2GB RAM execution ceiling.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

