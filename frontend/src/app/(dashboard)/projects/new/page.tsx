"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { FolderPlus, Sparkles, Check, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

export default function NewProjectPage() {
  const router = useRouter();
  const [name, setName] = useState("Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery");
  const [topic, setTopic] = useState("Multitemporal Synthetic Aperture Radar (SAR) Change Detection");
  const [journal, setJournal] = useState("IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing (J-STARS)");
  const [keywords, setKeywords] = useState("Sentinel-1, SAR, Change Detection, Siamese Networks, Cross-Attention");
  const [questions, setQuestions] = useState(
    "1. How can dual-stream Siamese architectures mitigate speckle noise in multitemporal SAR imagery?\n2. What is the impact of strict non-leaking 80/20 spatial partitioning compared to random pixel sampling?"
  );

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    toast.success("Research Project Initialized with LangGraph Orchestrator!");
    router.push("/papers/discover");
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="space-y-1">
        <h2 className="text-2xl font-bold tracking-tight">Create New Research Project</h2>
        <p className="text-xs text-muted-foreground">
          Initialize your autonomous research workspace, target journal, and hypothesis search space.
        </p>
      </div>

      <form onSubmit={handleCreate}>
        <Card className="border-border/80 shadow-xs">
          <CardHeader>
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <FolderPlus className="h-4 w-4 text-blue-500" /> Project Metadata & Hypothesis Scope
            </CardTitle>
            <CardDescription className="text-xs">
              Configures the multi-agent literature explorer (LangGraph / Stanford STORM).
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="name">Project Title</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery"
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label htmlFor="topic">Research Topic</Label>
                <Input
                  id="topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g. Multitemporal SAR Change Detection"
                  required
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="journal">Target Journal / Conference</Label>
                <Input
                  id="journal"
                  value={journal}
                  onChange={(e) => setJournal(e.target.value)}
                  placeholder="e.g. IEEE J-STARS"
                  required
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="keywords">Keywords (Comma Separated)</Label>
              <Input
                id="keywords"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="Sentinel-1, SAR, Change Detection, Siamese Networks"
              />
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="questions">Research Questions & Hypotheses Scope</Label>
              <Textarea
                id="questions"
                rows={4}
                value={questions}
                onChange={(e) => setQuestions(e.target.value)}
                placeholder="Enter initial research questions..."
              />
            </div>

            <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 text-xs space-y-1">
              <span className="font-semibold text-blue-400 flex items-center gap-1.5">
                <Sparkles className="h-3.5 w-3.5" /> Automated Scientific Rigor Guarantee
              </span>
              <p className="text-muted-foreground">
                ResearchOS enforces a default 80% training / 20% held-out test partitioning protocol across all dataset processing and model evaluations.
              </p>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <Button type="button" variant="outline" onClick={() => router.back()}>
                Cancel
              </Button>
              <Button type="submit" className="bg-blue-600 hover:bg-blue-500 text-white gap-2">
                Initialize Project & Discover Papers <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}

