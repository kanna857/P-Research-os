"use client";

import React, { useState } from "react";
import {
  FileText,
  Download,
  Share2,
  Bookmark,
  Sparkles,
  ChevronRight,
  BookOpen,
  CheckCircle2,
  ExternalLink,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { toast } from "sonner";

export default function PDFReaderPage() {
  const [selectedSection, setSelectedSection] = useState("methodology");

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">PDF Reader & Literature Intelligence</h2>
            <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
              Docling + GROBID
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Structured scientific document analysis, claim extraction, and section navigation.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="gap-1.5 text-xs">
            <Bookmark className="h-3.5 w-3.5" /> Save Annotation
          </Button>
          <Button
            size="sm"
            className="bg-blue-600 hover:bg-blue-500 text-white gap-1.5 text-xs"
            onClick={() => toast.success("Citation copied to clipboard (IEEE format)!")}
          >
            <Share2 className="h-3.5 w-3.5" /> Copy IEEE Citation
          </Button>
        </div>
      </div>

      {/* Split Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[720px]">
        {/* Left: PDF Document Rendering */}
        <Card className="flex flex-col border-border/80 overflow-hidden">
          <CardHeader className="py-3 px-4 border-b border-border bg-muted/30">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold truncate max-w-sm">
                Gong_2023_Deep_Convolutional_Coupling_SAR.pdf
              </span>
              <Badge variant="outline" className="text-[10px]">
                Page 4 of 14
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="flex-1 p-6 bg-slate-950/80 overflow-y-auto font-mono text-xs text-slate-300 space-y-4">
            <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
              <div className="text-center font-bold text-sm text-white">
                A Deep Convolutional Coupling Network for Change Detection in Multitemporal SAR Images
              </div>
              <div className="text-center text-[10px] text-slate-400">
                Maoguo Gong, Senior Member, IEEE, Mingyang Liu, Yuan Li, and Puzhao Zhang
              </div>
            </div>

            <div className="space-y-2 text-slate-300 leading-relaxed text-[11px]">
              <p className="font-bold text-slate-100 uppercase tracking-wider text-[10px]">
                III. Proposed Methodology
              </p>
              <p>
                Let X1, X2 in R^(H x W) represent two co-registered multitemporal synthetic aperture radar (SAR) images acquired over the same geographical region at distinct dates T1 and T2. Due to environmental variations and coherent interference, pixels exhibit multiplicative speckle noise following a Gamma distribution.
              </p>
              <p>
                To overcome pixel-level degradation, our coupling convolutional stream extracts joint temporal invariant manifolds. Skip connections transfer fine-grained spatial boundaries directly from low-level feature decoders to the final binary classification layer, preserving linear structural features while minimizing spurious detections.
              </p>
              <div className="p-3 my-2 rounded bg-slate-900 border border-slate-800 text-center font-sans text-xs text-amber-400">
                [Equation 4] L_coupling = || Phi(X1) - Phi(X2) ||_2^2 + lambda * L_focal
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Right: Docling Structured Sections & Claims */}
        <Card className="flex flex-col border-border/80 overflow-hidden">
          <CardHeader className="py-3 px-4 border-b border-border bg-muted/30">
            <CardTitle className="text-xs font-semibold flex items-center justify-between">
              <span>Docling Hierarchical Extraction</span>
              <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3" /> 100% Parsed
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-4 overflow-y-auto space-y-4">
            <Tabs defaultValue="methods" className="w-full">
              <TabsList className="grid grid-cols-4 w-full h-8 text-xs">
                <TabsTrigger value="abstract" className="text-xs">Abstract</TabsTrigger>
                <TabsTrigger value="methods" className="text-xs">Methods</TabsTrigger>
                <TabsTrigger value="results" className="text-xs">Results</TabsTrigger>
                <TabsTrigger value="claims" className="text-xs">Claims</TabsTrigger>
              </TabsList>

              <TabsContent value="abstract" className="space-y-3 pt-3 text-xs leading-relaxed">
                <div className="p-3 rounded-xl bg-muted/40 border border-border/60">
                  <h4 className="font-semibold text-foreground mb-1 text-xs">Extracted Abstract</h4>
                  <p className="text-muted-foreground">
                    Multitemporal SAR change detection is severely hampered by speckle noise and lack of ground truth labels. This work proposes a deep convolutional coupling framework that bridges feature distributions across multitemporal acquisitions, achieving state-of-the-art accuracy on benchmark datasets.
                  </p>
                </div>
              </TabsContent>

              <TabsContent value="methods" className="space-y-3 pt-3 text-xs leading-relaxed">
                <div className="p-3 rounded-xl bg-muted/40 border border-border/60 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-foreground">Core Architecture</span>
                    <Badge variant="outline" className="text-[10px]">Convolutional Coupling</Badge>
                  </div>
                  <p className="text-muted-foreground">
                    Dual-stream encoder with parameter coupling layers. Applies difference feature maps followed by residual refinement blocks.
                  </p>
                  <div className="grid grid-cols-2 gap-2 pt-2 text-[11px]">
                    <div className="p-2 rounded bg-background border border-border">
                      <span className="text-muted-foreground block">Loss Function:</span>
                      <span className="font-medium text-foreground">Combined L2 + Focal Loss</span>
                    </div>
                    <div className="p-2 rounded bg-background border border-border">
                      <span className="text-muted-foreground block">Input Channels:</span>
                      <span className="font-medium text-foreground">2 (SAR VV/VH Polarizations)</span>
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="results" className="space-y-3 pt-3 text-xs leading-relaxed">
                <div className="p-3 rounded-xl bg-muted/40 border border-border/60 space-y-2">
                  <span className="font-semibold text-foreground">Reported Metrics in Paper</span>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="p-2 rounded bg-background border border-border">
                      <span className="text-muted-foreground text-[10px]">Reported F1:</span>
                      <span className="font-bold text-foreground block">89.4%</span>
                    </div>
                    <div className="p-2 rounded bg-background border border-border">
                      <span className="text-muted-foreground text-[10px]">Reported IoU:</span>
                      <span className="font-bold text-foreground block">80.8%</span>
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="claims" className="space-y-3 pt-3 text-xs leading-relaxed">
                <div className="space-y-2">
                  <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 space-y-1">
                    <div className="flex items-center justify-between text-blue-400 font-semibold">
                      <span>Scientific Claim #1</span>
                      <Badge variant="outline" className="text-[10px]">Page 6, Para 2</Badge>
                    </div>
                    <p className="text-muted-foreground text-[11px]">
                      &quot;Feature coupling reduces false alarm rates in agricultural flood zones by 14.2% compared to principal component analysis differencing.&quot;
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-1">
                    <div className="flex items-center justify-between text-amber-400 font-semibold">
                      <span>Identified Limitation</span>
                      <Badge variant="outline" className="text-[10px]">Page 11, Section V</Badge>
                    </div>
                    <p className="text-muted-foreground text-[11px]">
                      Authors note that the model does not include cross-attention mechanisms and struggles under severe baseline temporal decorrelation.
                    </p>
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

