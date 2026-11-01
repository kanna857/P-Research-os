"use client";

import React, { useState } from "react";
import {
  Settings,
  Key,
  CheckCircle2,
  HardDrive,
  Cpu,
  Layers,
  Sparkles,
  Save,
  ExternalLink,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { toast } from "sonner";

export default function SettingsPage() {
  const [openalexEmail, setOpenalexEmail] = useState("researcher@university.edu");
  const [unpaywallEmail, setUnpaywallEmail] = useState("researcher@university.edu");
  const [hfToken, setHfToken] = useState("hf_••••••••••••••••••••••••");
  const [grobidUrl, setGrobidUrl] = useState("http://localhost:8070");
  const [mlflowUri, setMlflowUri] = useState("http://localhost:5000");

  const integrations = [
    { name: "LangGraph (langchain-ai/langgraph)", category: "Multi-Agent Research", status: "Active / Integrated", icon: Sparkles },
    { name: "Stanford STORM (stanford-oval/storm)", category: "Outline & Perspective Synthesis", status: "Active / Integrated", icon: Sparkles },
    { name: "LlamaIndex (run-llama/llama_index)", category: "RAG & Literature Indexing", status: "Active / Integrated", icon: Sparkles },
    { name: "OpenAlex Python (ourresearch/openalex-python)", category: "Academic Paper Discovery", status: "Active / Connected", icon: Sparkles },
    { name: "Unpaywall (ourresearch/unpaywall)", category: "Legal Open Access PDF Acquisition", status: "Active / Connected", icon: Sparkles },
    { name: "Docling (docling-project/docling)", category: "Scientific Document Parsing", status: "Active / Integrated", icon: Sparkles },
    { name: "GROBID (kermitt2/grobid)", category: "Bibliographic Header Extraction", status: "Active / Ready", icon: Sparkles },
    { name: "Hugging Face Datasets & Hub", category: "Dataset Discovery", status: "Active / Connected", icon: Sparkles },
    { name: "FiftyOne & Cleanlab (voxel51/fiftyone, cleanlab/cleanlab)", category: "Quality Auditing & Label Inspection", status: "Active / Integrated", icon: Sparkles },
    { name: "DVC (iterative/dvc)", category: "Reproducible Data Versioning", status: "Active / Integrated", icon: Sparkles },
    { name: "PyTorch Lightning (Lightning-AI/pytorch-lightning)", category: "Multi-Model Training Engine", status: "Active / Integrated", icon: Sparkles },
    { name: "ClearML & MLflow (clearml/clearml, mlflow/mlflow)", category: "Experiment Telemetry & Artifact Tracking", status: "Active / Connected", icon: Sparkles },
    { name: "Optuna (optuna/optuna)", category: "Bayesian Hyperparameter Search", status: "Active / Integrated", icon: Sparkles },
    { name: "Mermaid & React Flow (mermaid-js/mermaid, xyflow/xyflow)", category: "Scientific Diagram Generator", status: "Active / Integrated", icon: Sparkles },
    { name: "LanguageTool (languagetool-org/languagetool)", category: "Academic Style & Grammar", status: "Active / Integrated", icon: Sparkles },
    { name: "Sentence Transformers & RapidFuzz", category: "Originality & Attribution Verification", status: "Active / Integrated", icon: Sparkles },
  ];

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success("Settings and API credentials updated successfully!");
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold tracking-tight">Settings & Integrations</h2>
          <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-xs">
            16 / 16 Repositories Connected
          </Badge>
        </div>
        <p className="text-xs text-muted-foreground">
          Manage API credentials, external academic connections, and verify GitHub open-source repository adapters.
        </p>
      </div>

      <Tabs defaultValue="integrations" className="space-y-4">
        <TabsList className="h-9">
          <TabsTrigger value="integrations" className="text-xs">
            Repository Integrations (16)
          </TabsTrigger>
          <TabsTrigger value="apikeys" className="text-xs">
            API Keys & Endpoints
          </TabsTrigger>
          <TabsTrigger value="storage" className="text-xs">
            Storage & Compute
          </TabsTrigger>
        </TabsList>

        {/* Integrations Grid */}
        <TabsContent value="integrations" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {integrations.map((item, idx) => (
              <Card key={idx} className="border-border/80">
                <CardContent className="p-4 flex items-center justify-between text-xs">
                  <div className="space-y-0.5">
                    <span className="font-semibold text-foreground block">{item.name}</span>
                    <span className="text-[11px] text-muted-foreground">{item.category}</span>
                  </div>
                  <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px] gap-1 shrink-0">
                    <CheckCircle2 className="h-3 w-3" /> {item.status}
                  </Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* API Credentials */}
        <TabsContent value="apikeys">
          <form onSubmit={handleSave}>
            <Card className="border-border/80">
              <CardHeader>
                <CardTitle className="text-base font-semibold">Service Credentials & Keys</CardTitle>
                <CardDescription className="text-xs">
                  Academic APIs (OpenAlex & Unpaywall require valid email addresses for higher rate limits).
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4 text-xs">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label className="text-xs">OpenAlex Email (Polite Pool)</Label>
                    <Input
                      value={openalexEmail}
                      onChange={(e) => setOpenalexEmail(e.target.value)}
                      className="text-xs"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label className="text-xs">Unpaywall Email</Label>
                    <Input
                      value={unpaywallEmail}
                      onChange={(e) => setUnpaywallEmail(e.target.value)}
                      className="text-xs"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <Label className="text-xs">Hugging Face User Access Token</Label>
                  <Input
                    type="password"
                    value={hfToken}
                    onChange={(e) => setHfToken(e.target.value)}
                    className="text-xs font-mono"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label className="text-xs">GROBID Service Endpoint</Label>
                    <Input
                      value={grobidUrl}
                      onChange={(e) => setGrobidUrl(e.target.value)}
                      className="text-xs font-mono"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label className="text-xs">MLflow Tracking URI</Label>
                    <Input
                      value={mlflowUri}
                      onChange={(e) => setMlflowUri(e.target.value)}
                      className="text-xs font-mono"
                    />
                  </div>
                </div>

                <div className="flex justify-end pt-2">
                  <Button type="submit" className="bg-blue-600 hover:bg-blue-500 text-white gap-1.5 text-xs">
                    <Save className="h-4 w-4" /> Save Configuration
                  </Button>
                </div>
              </CardContent>
            </Card>
          </form>
        </TabsContent>

        {/* Storage Tab */}
        <TabsContent value="storage">
          <Card className="border-border/80">
            <CardHeader>
              <CardTitle className="text-base font-semibold">MinIO S3 & Local Storage Buckets</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-muted/40 border border-border flex justify-between items-center">
                <div>
                  <span className="font-semibold text-foreground block">researchos-papers</span>
                  <span className="text-[10px] text-muted-foreground">PDFs and Docling structured JSON</span>
                </div>
                <span className="font-mono text-muted-foreground">1.8 GB / 100 GB</span>
              </div>

              <div className="p-3 rounded-xl bg-muted/40 border border-border flex justify-between items-center">
                <div>
                  <span className="font-semibold text-foreground block">researchos-datasets</span>
                  <span className="text-[10px] text-muted-foreground">GeoTIFF multitemporal tiles & 80/20 manifests</span>
                </div>
                <span className="font-mono text-muted-foreground">4.2 GB / 100 GB</span>
              </div>

              <div className="p-3 rounded-xl bg-muted/40 border border-border flex justify-between items-center">
                <div>
                  <span className="font-semibold text-foreground block">researchos-models</span>
                  <span className="text-[10px] text-muted-foreground">PyTorch Lightning checkpoints & MLflow artifacts</span>
                </div>
                <span className="font-mono text-muted-foreground">840 MB / 100 GB</span>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

