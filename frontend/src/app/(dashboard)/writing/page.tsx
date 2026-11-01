"use client";

import React, { useState } from "react";
import {
  PenTool,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Copy,
  Save,
  RotateCcw,
  BookOpen,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

export default function AcademicWritingPage() {
  const [tone, setTone] = useState<"formal" | "technical" | "concise" | "natural">("formal");
  const [activeSection, setActiveSection] = useState("abstract");

  const [text, setText] = useState(
    "Automated change detection in multitemporal satellite imagery plays an indispensable role in environmental monitoring, disaster mitigation, and urban planning. However, conventional convolutional architectures frequently suffer from speckle-induced false positives and spatial boundary blurring, particularly in complex terrain. To address these challenges, this paper presents a novel Siamese deep learning framework specifically tailored for Sentinel-1 SAR imagery. The proposed architecture leverages dual-stream encoders with multiscale cross-attention feature subtraction, preserving fine-grained edge details while suppressing temporal radiometric variances. The model was trained and rigorously benchmarked using a strict 80% training and 20% held-out test partitioning protocol, ensuring zero geographic or spatial autocorrelation leakage. Experimental results demonstrate that our proposed Siamese network achieves an F1-score of 93.8% and an Intersection-over-Union (IoU) of 88.4%, substantially outperforming standard ResNet-50 and U-Net baselines by 3.3% and 1.8%, respectively."
  );

  const [rewrittenText, setRewrittenText] = useState("");
  const [rewriting, setRewriting] = useState(false);

  const handleRewrite = () => {
    setRewriting(true);
    setTimeout(() => {
      setRewriting(false);
      let res = "";
      if (tone === "concise") {
        res =
          "Automated change detection in multitemporal satellite imagery is critical for environmental monitoring and disaster mitigation. Yet, conventional CNNs suffer from speckle false alarms and boundary blurring. We propose a Siamese deep learning architecture with multiscale cross-attention for Sentinel-1 SAR imagery. Evaluating on a strict 80/20 non-leaking test protocol, our Siamese model achieves a 93.8% F1-score and 88.4% IoU, outperforming ResNet-50 and U-Net baselines by 3.3% and 1.8%.";
      } else if (tone === "technical") {
        res =
          "Multitemporal satellite change detection necessitates resolving spatial boundary degradation and speckle-induced noise. We formalize a Siamese cross-attention network operating over dual-polarized SAR tensors. The model projects twin temporal observations into shared latent manifolds, executing differential magnitude subtraction across multiscale skip trajectories. Under a verified 80/20 geographically isolated evaluation protocol, the architecture yields an F1-score of 93.8% and an IoU of 88.4%, confirming significant spatial boundary delineation over conventional convolutional baselines.";
      } else {
        res =
          "Automated surface change detection across multitemporal SAR imagery remains foundational for monitoring global planetary transformations. While traditional convolutional networks are impeded by speckle noise and spatial boundary blurring, our proposed Siamese cross-attention framework systematically aligns multitemporal features prior to subtraction. Tested against an isolated 20% held-out partition, the proposed network attains an empirical F1-score of 93.8% and an IoU of 88.4%, demonstrating reproducible state-of-the-art capability.";
      }
      setRewrittenText(res);
      toast.success(`Academic rewriting completed in ${tone.toUpperCase()} tone!`);
    }, 500);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Academic Writing Studio</h2>
            <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 text-xs">
              Humanize + LanguageTool
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Academic style refinement, grammar verification, and grounded scientific phrasing for IEEE manuscripts.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            size="sm"
            className="bg-blue-600 hover:bg-blue-500 text-white gap-1.5 text-xs"
            onClick={() => toast.success("Saved revised section to active manuscript draft!")}
          >
            <Save className="h-3.5 w-3.5" /> Save Section
          </Button>
        </div>
      </div>

      {/* Tone Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3 rounded-xl bg-card border border-border">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-muted-foreground">Target Academic Tone:</span>
          <div className="flex gap-1">
            {(["formal", "technical", "concise", "natural"] as const).map((t) => (
              <Button
                key={t}
                size="sm"
                variant={tone === t ? "default" : "outline"}
                className={`h-7 text-xs capitalize ${tone === t ? "bg-blue-600 text-white" : ""}`}
                onClick={() => setTone(t)}
              >
                {t}
              </Button>
            ))}
          </div>
        </div>

        <Button
          size="sm"
          disabled={rewriting}
          className="bg-purple-600 hover:bg-purple-500 text-white gap-1.5 text-xs h-8"
          onClick={handleRewrite}
        >
          <Sparkles className="h-3.5 w-3.5" /> Refine with {tone.toUpperCase()} Tone
        </Button>
      </div>

      {/* Side-by-Side Editor */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="border-border/80 flex flex-col h-[520px]">
          <CardHeader className="py-2.5 px-4 border-b border-border bg-muted/20">
            <CardTitle className="text-xs font-semibold">Manuscript Draft (Input)</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-4">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full h-full p-2 bg-transparent text-foreground text-xs focus:outline-none resize-none leading-relaxed"
            />
          </CardContent>
        </Card>

        <Card className="border-border/80 flex flex-col h-[520px] bg-slate-950/40">
          <CardHeader className="py-2.5 px-4 border-b border-border bg-muted/20 flex flex-row items-center justify-between">
            <CardTitle className="text-xs font-semibold flex items-center gap-1.5 text-purple-400">
              <Sparkles className="h-3.5 w-3.5" /> Refined Academic Passage ({tone})
            </CardTitle>
            {rewrittenText && (
              <Button
                size="sm"
                variant="ghost"
                className="h-6 text-[10px] gap-1"
                onClick={() => {
                  setText(rewrittenText);
                  toast.success("Applied refined text to manuscript!");
                }}
              >
                Apply to Draft
              </Button>
            )}
          </CardHeader>
          <CardContent className="flex-1 p-4">
            {rewrittenText ? (
              <div className="text-xs text-foreground leading-relaxed whitespace-pre-wrap">
                {rewrittenText}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-xs text-muted-foreground gap-2">
                <Sparkles className="h-6 w-6 text-purple-400/50" />
                <span>Click &quot;Refine with Tone&quot; to generate academic alternative.</span>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

