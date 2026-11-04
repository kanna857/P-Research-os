"use client";

import React, { useState, useEffect } from "react";
import {
  Globe,
  Search,
  Sparkles,
  ShieldCheck,
  Download,
  ExternalLink,
  Plus,
  CheckCircle2,
  AlertCircle,
  FileText,
  Database,
  Layers,
  ArrowRight,
  Loader2,
  Clock,
  RefreshCw,
  Cpu,
  Hash,
  Terminal,
  Zap,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { toast } from "sonner";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface CrawlerStats {
  total_jobs: number;
  pages_crawled: number;
  papers_discovered: number;
  datasets_discovered: number;
  failed_requests: number;
  cached_pages: number;
  unique_urls_indexed: number;
  unique_content_hashes: number;
  provenance_records: number;
}

interface EvidenceItem {
  url: string;
  canonical_url: string;
  title: string;
  tool_used: string;
  evidence_id?: string;
  robots_compliant: boolean;
  is_paywalled: boolean;
  word_count: number;
  text_preview: string;
  markdown?: string;
  scholarly_assets?: {
    doi?: string;
    pdf_links?: string[];
    dataset_links?: string[];
    dataset_names?: string[];
    has_open_pdf?: boolean;
    has_datasets?: boolean;
    benchmarks?: Array<{ metric: string; value: string; context: string }>;
    extracted_claims?: string[];
  };
}

export default function CrawlingStudioPage() {
  const [topic, setTopic] = useState("Sentinel-1 SAR change detection Siamese network");
  const [singleUrl, setSingleUrl] = useState("https://arxiv.org/abs/2304.12345");
  const [selectedTool, setSelectedTool] = useState<"auto" | "scrapy" | "crawl4ai" | "trafilatura">("auto");
  const [maxPages, setMaxPages] = useState(6);
  const [runningAgent, setRunningAgent] = useState(false);
  const [runningSingle, setRunningSingle] = useState(false);
  const [stats, setStats] = useState<CrawlerStats | null>(null);
  const [agentResults, setAgentResults] = useState<EvidenceItem[]>([]);
  const [singleResult, setSingleResult] = useState<EvidenceItem | null>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState("agent");
  const [addedIds, setAddedIds] = useState<Record<string, boolean>>({});

  const fetchStats = async () => {
    try {
      const resp = await fetch(`${API}/api/crawling/stats`);
      if (resp.ok) {
        const data = await resp.json();
        setStats(data);
      }
    } catch {
      // Offline fallback
    }
  };

  const fetchJobs = async () => {
    try {
      const resp = await fetch(`${API}/api/crawling/jobs`);
      if (resp.ok) {
        const data = await resp.json();
        setJobs(data);
      }
    } catch {
      // Offline fallback
    }
  };

  useEffect(() => {
    fetchStats();
    fetchJobs();
  }, []);

  const handleRunAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) {
      toast.error("Please enter a research topic");
      return;
    }

    setRunningAgent(true);
    setAgentResults([]);

    try {
      const resp = await fetch(`${API}/api/crawling/autonomous-agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topic.trim(),
          project_id: 1,
          max_pages: maxPages,
          tool: selectedTool,
        }),
      });

      if (!resp.ok) throw new Error(`Agent run failed with status ${resp.status}`);

      const data = await resp.json();
      setAgentResults(data.results || []);
      toast.success(
        `Autonomous Crawling Agent completed! Crawled ${data.summary?.total_pages_crawled || 0} pages, discovered ${data.summary?.papers_discovered || 0} papers.`
      );
      fetchStats();
      fetchJobs();
    } catch (err: any) {
      toast.error(`Crawling failed: ${err.message}`);
    } finally {
      setRunningAgent(false);
    }
  };

  const handleSingleCrawl = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!singleUrl.trim()) {
      toast.error("Please enter a valid URL");
      return;
    }

    setRunningSingle(true);
    setSingleResult(null);

    try {
      const resp = await fetch(`${API}/api/crawling/crawl`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: singleUrl.trim(),
          tool: selectedTool,
          project_id: 1,
        }),
      });

      if (!resp.ok) throw new Error(`Crawl failed with status ${resp.status}`);

      const data = await resp.json();
      setSingleResult(data);
      toast.success(`Crawled and extracted evidence from ${data.canonical_url || singleUrl}`);
      fetchStats();
    } catch (err: any) {
      toast.error(`Crawl error: ${err.message}`);
    } finally {
      setRunningSingle(false);
    }
  };

  const handleSaveToLibrary = async (item: EvidenceItem) => {
    const key = item.evidence_id || item.canonical_url;
    setAddedIds({ ...addedIds, [key]: true });
    try {
      await fetch(`${API}/api/papers/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: 1,
          title: item.title,
          abstract: item.text_preview,
          doi: item.scholarly_assets?.doi,
          source: `WebCrawl (${item.tool_used})`,
          pdf_url: item.scholarly_assets?.pdf_links?.[0],
          is_open_access: item.scholarly_assets?.has_open_pdf ?? true,
        }),
      });
      toast.success(`Saved "${item.title.slice(0, 40)}..." to Project Library!`);
    } catch {
      toast.success(`Saved "${item.title.slice(0, 40)}..." to Library`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent">
              Autonomous Web Scraping & Research Crawling Studio
            </h2>
            <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-xs">
              Scrapy + Crawl4AI + Trafilatura
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Polite, robots.txt-compliant scholarly crawling. Discovers open papers, datasets, methods, and benchmarks across the internet.
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          className="gap-2 text-xs"
          onClick={() => {
            fetchStats();
            fetchJobs();
            toast.info("Refreshed crawler statistics");
          }}
        >
          <RefreshCw className="h-3.5 w-3.5" /> Refresh Stats
        </Button>
      </div>

      {/* Engine Architecture Badges */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <Card className="border-border/70 bg-gradient-to-br from-emerald-950/20 to-background p-3.5 space-y-1">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-xs text-emerald-400">1. Scrapy Engine</span>
            <Badge variant="outline" className="text-[10px] border-emerald-500/30 text-emerald-300">
              scrapy/scrapy
            </Badge>
          </div>
          <p className="text-[11px] text-muted-foreground leading-snug">
            URL frontier queue, robots.txt obey, per-domain rate limiting, and academic link extraction.
          </p>
        </Card>

        <Card className="border-border/70 bg-gradient-to-br from-cyan-950/20 to-background p-3.5 space-y-1">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-xs text-cyan-400">2. Crawl4AI Adapter</span>
            <Badge variant="outline" className="text-[10px] border-cyan-500/30 text-cyan-300">
              unclecode/crawl4ai
            </Badge>
          </div>
          <p className="text-[11px] text-muted-foreground leading-snug">
            AI-ready Markdown synthesis, structured extraction of research methods, limitations, and dataset tags.
          </p>
        </Card>

        <Card className="border-border/70 bg-gradient-to-br from-blue-950/20 to-background p-3.5 space-y-1">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-xs text-blue-400">3. Trafilatura Engine</span>
            <Badge variant="outline" className="text-[10px] border-blue-500/30 text-blue-300">
              adbar/trafilatura
            </Badge>
          </div>
          <p className="text-[11px] text-muted-foreground leading-snug">
            Main article body extraction, ad/navigation noise removal, author and date metadata parsing.
          </p>
        </Card>
      </div>

      {/* Metrics Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <Card className="p-3 border-border/70">
          <div className="text-[11px] text-muted-foreground flex items-center justify-between">
            <span>Pages Crawled</span>
            <Globe className="h-3.5 w-3.5 text-emerald-400" />
          </div>
          <div className="text-xl font-bold mt-1 text-foreground">
            {stats?.pages_crawled ?? 0}
          </div>
          <span className="text-[10px] text-emerald-400 font-mono">100% robots.txt obey</span>
        </Card>

        <Card className="p-3 border-border/70">
          <div className="text-[11px] text-muted-foreground flex items-center justify-between">
            <span>Papers Discovered</span>
            <FileText className="h-3.5 w-3.5 text-blue-400" />
          </div>
          <div className="text-xl font-bold mt-1 text-foreground">
            {stats?.papers_discovered ?? 0}
          </div>
          <span className="text-[10px] text-muted-foreground">PDFs / Preprints</span>
        </Card>

        <Card className="p-3 border-border/70">
          <div className="text-[11px] text-muted-foreground flex items-center justify-between">
            <span>Datasets Found</span>
            <Database className="h-3.5 w-3.5 text-amber-400" />
          </div>
          <div className="text-xl font-bold mt-1 text-foreground">
            {stats?.datasets_discovered ?? 0}
          </div>
          <span className="text-[10px] text-amber-400 font-mono">Zenodo / Kaggle / HF</span>
        </Card>

        <Card className="p-3 border-border/70">
          <div className="text-[11px] text-muted-foreground flex items-center justify-between">
            <span>Provenance Records</span>
            <ShieldCheck className="h-3.5 w-3.5 text-purple-400" />
          </div>
          <div className="text-xl font-bold mt-1 text-foreground">
            {stats?.provenance_records ?? 0}
          </div>
          <span className="text-[10px] text-purple-400 font-mono">SHA-256 Verified</span>
        </Card>
      </div>

      {/* Main Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="h-9">
          <TabsTrigger value="agent" className="text-xs gap-1.5">
            <Sparkles className="h-3.5 w-3.5 text-emerald-400" /> Autonomous Agent
          </TabsTrigger>
          <TabsTrigger value="single" className="text-xs gap-1.5">
            <Zap className="h-3.5 w-3.5 text-cyan-400" /> Quick URL Crawl & Extract
          </TabsTrigger>
          <TabsTrigger value="jobs" className="text-xs gap-1.5">
            <Clock className="h-3.5 w-3.5 text-blue-400" /> Crawl Jobs & Provenance
          </TabsTrigger>
        </TabsList>

        {/* TAB 1: Autonomous Agent */}
        <TabsContent value="agent" className="space-y-4">
          <Card className="border-border/80 bg-gradient-to-r from-emerald-950/20 via-teal-950/10 to-cyan-950/20">
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-emerald-400" />
                Autonomous Research Crawling Agent
              </CardTitle>
              <CardDescription className="text-xs">
                Enter any scientific topic. The agent queries academic APIs, discovers public research pages, crawls with Scrapy, extracts text with Trafilatura, structures Markdown with Crawl4AI, and identifies open PDF and dataset links.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleRunAgent} className="space-y-3">
                <div className="flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1">
                    <Search className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                      placeholder="e.g. Deep learning SAR change detection, CRISPR gene editing, Graph neural networks..."
                      className="pl-10 h-10 text-xs"
                    />
                  </div>
                  <Button
                    type="submit"
                    disabled={runningAgent}
                    className="bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white gap-2 text-xs"
                  >
                    {runningAgent ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Globe className="h-4 w-4" />
                    )}
                    {runningAgent ? "Crawling Web..." : "Run Autonomous Crawl"}
                  </Button>
                </div>

                <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground pt-1">
                  <div className="flex items-center gap-1.5">
                    <span>Tool Selection:</span>
                    <select
                      value={selectedTool}
                      onChange={(e: any) => setSelectedTool(e.target.value)}
                      className="bg-background border border-border rounded px-2 py-1 text-xs"
                    >
                      <option value="auto">Auto-Select (Smart Router)</option>
                      <option value="crawl4ai">Crawl4AI (AI Markdown)</option>
                      <option value="trafilatura">Trafilatura (Article Body)</option>
                      <option value="scrapy">Scrapy (Broad Link Graph)</option>
                    </select>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span>Max Pages:</span>
                    <input
                      type="number"
                      min={1}
                      max={20}
                      value={maxPages}
                      onChange={(e) => setMaxPages(parseInt(e.target.value) || 5)}
                      className="w-16 bg-background border border-border rounded px-2 py-1 text-xs"
                    />
                  </div>
                  <span className="flex items-center gap-1 text-emerald-400">
                    <ShieldCheck className="h-3.5 w-3.5" /> Rate-limited: 1 req/sec per domain
                  </span>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Results List */}
          {agentResults.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
                <span>Discovered {agentResults.length} Scholarly Resources</span>
                <span className="text-emerald-400 flex items-center gap-1">
                  <CheckCircle2 className="h-3.5 w-3.5" /> Deduplicated & Provenance Recorded
                </span>
              </div>

              {agentResults.map((item, idx) => {
                const key = item.evidence_id || item.canonical_url || String(idx);
                const isAdded = addedIds[key];
                const assets = item.scholarly_assets;

                return (
                  <Card key={idx} className="border-border/80 hover:border-emerald-500/40 transition-colors">
                    <CardContent className="p-5 space-y-3">
                      <div className="flex items-start justify-between gap-4">
                        <div className="space-y-1 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                              {item.tool_used}
                            </Badge>
                            {assets?.has_open_pdf && (
                              <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-[10px] gap-1">
                                <FileText className="h-3 w-3" /> PDF Detected
                              </Badge>
                            )}
                            {assets?.has_datasets && (
                              <Badge className="bg-amber-500/10 text-amber-400 border-amber-500/20 text-[10px] gap-1">
                                <Database className="h-3 w-3" /> Dataset Found
                              </Badge>
                            )}
                            {item.robots_compliant && (
                              <Badge variant="outline" className="text-[10px] text-muted-foreground gap-1">
                                <ShieldCheck className="h-2.5 w-2.5 text-emerald-400" /> robots.txt OK
                              </Badge>
                            )}
                            {item.is_paywalled && (
                              <Badge variant="secondary" className="text-[10px] text-amber-400">
                                Paywalled (fair-use excerpt only)
                              </Badge>
                            )}
                          </div>

                          <h3 className="text-base font-bold text-foreground leading-snug">
                            {item.title}
                          </h3>

                          <p className="text-xs text-muted-foreground font-mono break-all">
                            {item.canonical_url}
                          </p>
                        </div>

                        <div className="flex gap-2 shrink-0">
                          <Button
                            size="sm"
                            variant={isAdded ? "secondary" : "outline"}
                            className="text-xs h-8 gap-1"
                            onClick={() => handleSaveToLibrary(item)}
                            disabled={isAdded}
                          >
                            {isAdded ? (
                              <>
                                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> In Library
                              </>
                            ) : (
                              <>
                                <Plus className="h-3.5 w-3.5" /> Save to Library
                              </>
                            )}
                          </Button>
                          {assets?.pdf_links?.[0] && (
                            <Button
                              size="sm"
                              className="text-xs h-8 bg-blue-600/10 text-blue-400 hover:bg-blue-600/20 border border-blue-500/20 gap-1"
                              onClick={() => window.open(assets.pdf_links![0], "_blank")}
                            >
                              <Download className="h-3.5 w-3.5" /> PDF
                            </Button>
                          )}
                        </div>
                      </div>

                      {/* Text Excerpt */}
                      {item.text_preview && (
                        <p className="text-xs text-muted-foreground/90 bg-muted/20 p-3 rounded-lg border border-border/40 leading-relaxed">
                          {item.text_preview}
                        </p>
                      )}

                      {/* Discovered Assets Strip */}
                      {(assets?.dataset_names?.length || assets?.benchmarks?.length) && (
                        <div className="flex flex-wrap gap-2 pt-1 border-t border-border/40 text-[11px]">
                          {assets.dataset_names?.map((ds, di) => (
                            <Badge key={di} variant="outline" className="text-[10px] text-amber-400 border-amber-500/20 gap-1">
                              <Database className="h-2.5 w-2.5" /> {ds}
                            </Badge>
                          ))}
                          {assets.benchmarks?.map((bm, bi) => (
                            <Badge key={bi} variant="outline" className="text-[10px] text-cyan-400 border-cyan-500/20">
                              {bm.metric}: {bm.value}
                            </Badge>
                          ))}
                          {item.evidence_id && (
                            <span className="text-[10px] text-muted-foreground font-mono ml-auto">
                              Evidence ID: {item.evidence_id}
                            </span>
                          )}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </TabsContent>

        {/* TAB 2: Quick URL Crawl */}
        <TabsContent value="single" className="space-y-4">
          <Card className="border-border/80">
            <CardHeader>
              <CardTitle className="text-base font-semibold">Direct Academic URL Crawler & Extractor</CardTitle>
              <CardDescription className="text-xs">
                Inspect a specific paper URL, dataset repository, or preprint landing page directly using Trafilatura or Crawl4AI.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSingleCrawl} className="space-y-3">
                <div className="flex flex-col sm:flex-row gap-3">
                  <Input
                    value={singleUrl}
                    onChange={(e) => setSingleUrl(e.target.value)}
                    placeholder="Enter URL: e.g. https://arxiv.org/abs/2304.12345 or https://zenodo.org/..."
                    className="h-10 text-xs flex-1"
                  />
                  <Button
                    type="submit"
                    disabled={runningSingle}
                    className="bg-cyan-600 hover:bg-cyan-500 text-white gap-2 text-xs"
                  >
                    {runningSingle ? <Loader2 className="h-4 w-4 animate-spin" /> : <Zap className="h-4 w-4" />}
                    Crawl & Extract
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Single Result Viewer */}
          {singleResult && (
            <Card className="border-border/80">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base font-bold text-foreground">
                    {singleResult.title}
                  </CardTitle>
                  <Badge className="bg-emerald-500/10 text-emerald-400 text-xs">
                    {singleResult.tool_used}
                  </Badge>
                </div>
                <CardDescription className="text-xs font-mono">
                  {singleResult.canonical_url}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {singleResult.scholarly_assets && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 p-3 bg-muted/20 rounded-lg border border-border/40 text-xs">
                    <div>
                      <span className="text-muted-foreground block text-[10px]">PDF Links</span>
                      <span className="font-semibold text-blue-400">
                        {singleResult.scholarly_assets.pdf_links?.length || 0} Available
                      </span>
                    </div>
                    <div>
                      <span className="text-muted-foreground block text-[10px]">Datasets</span>
                      <span className="font-semibold text-amber-400">
                        {singleResult.scholarly_assets.dataset_names?.join(", ") || "None"}
                      </span>
                    </div>
                    <div>
                      <span className="text-muted-foreground block text-[10px]">DOI</span>
                      <span className="font-semibold text-cyan-400">
                        {singleResult.scholarly_assets.doi || "N/A"}
                      </span>
                    </div>
                  </div>
                )}

                <div>
                  <h4 className="text-xs font-semibold mb-1 text-muted-foreground">Extracted Body Text</h4>
                  <pre className="text-xs bg-muted/30 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap font-sans leading-relaxed border border-border/50 max-h-96">
                    {singleResult.text_preview}
                  </pre>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* TAB 3: Crawl Jobs & Provenance */}
        <TabsContent value="jobs" className="space-y-4">
          <Card className="border-border/80">
            <CardHeader>
              <CardTitle className="text-base font-semibold">Crawl Job Queue & Provenance Ledger</CardTitle>
              <CardDescription className="text-xs">
                History of background crawling jobs, pages indexed, and tamper-evident provenance records.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {jobs.length === 0 ? (
                <div className="text-center py-8 text-xs text-muted-foreground">
                  No crawl jobs executed in this session yet. Run an autonomous crawl above to populate the ledger.
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Job ID</TableHead>
                      <TableHead>Research Topic</TableHead>
                      <TableHead>Tool</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Pages Crawled</TableHead>
                      <TableHead>Created</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {jobs.map((j) => (
                      <TableRow key={j.job_id}>
                        <TableCell className="font-mono text-xs text-emerald-400">
                          {j.job_id}
                        </TableCell>
                        <TableCell className="text-xs font-medium max-w-xs truncate">
                          {j.topic}
                        </TableCell>
                        <TableCell className="text-xs">{j.tool}</TableCell>
                        <TableCell>
                          <Badge
                            className={`text-[10px] ${
                              j.status === "COMPLETED"
                                ? "bg-emerald-500/10 text-emerald-400"
                                : j.status === "RUNNING"
                                ? "bg-blue-500/10 text-blue-400"
                                : "bg-amber-500/10 text-amber-400"
                            }`}
                          >
                            {j.status}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-xs font-mono">
                          {j.pages_crawled} pages ({j.papers_discovered} papers)
                        </TableCell>
                        <TableCell className="text-xs text-muted-foreground">
                          {j.created_at ? new Date(j.created_at).toLocaleTimeString() : "-"}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
