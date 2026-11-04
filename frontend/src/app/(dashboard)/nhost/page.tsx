"use client";

import React, { useState, useEffect } from "react";
import {
  Database,
  Server,
  Key,
  FolderLock,
  Search,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  Code2,
  Activity,
  Layers,
  ArrowRight,
  Upload,
  RefreshCw,
  Cpu,
  Hash,
  Copy,
  Terminal,
  ExternalLink,
  Lock,
  UserCheck,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { toast } from "sonner";
import nhost from "@/lib/nhost";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function NhostIntegrationPage() {
  const [statusData, setStatusData] = useState<any>(null);
  const [loadingStatus, setLoadingStatus] = useState(false);
  const [activeTab, setActiveTab] = useState("semantic-search");

  // Semantic search state
  const [searchQuery, setSearchQuery] = useState("Sentinel-1 SAR speckle reduction deep learning");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);

  // GraphQL query state
  const [graphqlQuery, setGraphqlQuery] = useState(`query GetResearchOverview {
  projects(limit: 5) {
    id
    name
    research_topic
    status
    created_at
  }
}`);
  const [graphqlResult, setGraphqlResult] = useState<string>("");
  const [executingGql, setExecutingGql] = useState(false);

  // Auth / Hasura token state
  const [userEmail, setUserEmail] = useState("researcher@researchos.local");
  const [selectedRole, setSelectedRole] = useState("user");
  const [activeJwt, setActiveJwt] = useState<string>("");
  const [decodedClaims, setDecodedClaims] = useState<any>(null);

  // Storage state
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([]);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    setLoadingStatus(true);
    try {
      const data = await nhost.getStatus();
      setStatusData(data);
    } catch {
      // offline fallback
    } finally {
      setLoadingStatus(false);
    }
  };

  const handleSemanticSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      const res = await nhost.semanticSearch(searchQuery.trim(), 5);
      setSearchResults(res.matches || []);
      toast.success(`Found ${res.results_count || 0} semantic matches via pgvector!`);
    } catch (err: any) {
      toast.error(`Semantic search error: ${err.message}`);
    } finally {
      setSearching(false);
    }
  };

  const handleExecuteGql = async () => {
    setExecutingGql(true);
    try {
      const res = await nhost.graphql(graphqlQuery);
      setGraphqlResult(JSON.stringify(res, null, 2));
      if (res.errors) {
        toast.warning("GraphQL query returned errors (see output)");
      } else {
        toast.success("GraphQL execution successful!");
      }
    } catch (err: any) {
      setGraphqlResult(JSON.stringify({ error: err.message }, null, 2));
      toast.error(`GraphQL error: ${err.message}`);
    } finally {
      setExecutingGql(false);
    }
  };

  const handleGenerateJwt = async () => {
    try {
      const token = await nhost.getHasuraToken(userEmail, 1, selectedRole);
      setActiveJwt(token);
      setDecodedClaims({
        "x-hasura-default-role": selectedRole,
        "x-hasura-allowed-roles": ["user", selectedRole],
        "x-hasura-user-id": "1",
        "email": userEmail,
      });
      toast.success(`Generated Hasura JWT with role: ${selectedRole}`);
    } catch (err: any) {
      toast.error(`Failed generating token: ${err.message}`);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const res = await nhost.uploadFile(file);
      setUploadedFiles((prev) => [res, ...prev]);
      toast.success(`Uploaded: ${file.name} (SHA-256: ${res.sha256?.slice(0, 10)}...)`);
    } catch (err: any) {
      toast.error(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Hero Header */}
      <div className="relative overflow-hidden rounded-2xl border border-indigo-500/20 bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950/40 p-8 shadow-2xl backdrop-blur-xl">
        <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-indigo-500/10 blur-3xl" />
        <div className="absolute -left-20 -bottom-20 h-64 w-64 rounded-full bg-sky-500/10 blur-3xl" />

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="inline-flex items-center gap-2 rounded-full border border-indigo-400/30 bg-indigo-500/10 px-4 py-1.5 text-xs font-semibold text-indigo-300">
              <Database className="h-4 w-4 text-indigo-400" />
              <span>Nhost Backend Architecture • PostgreSQL + Hasura GraphQL + pgvector</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
              <span>Role-Based Access Control • 100% Free & Self-Hostable</span>
            </div>
          </div>

          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl bg-gradient-to-r from-white via-slate-100 to-indigo-300 bg-clip-text text-transparent">
              Nhost + PostgreSQL Application Backend
            </h1>
            <p className="mt-2 text-sm text-slate-300 max-w-3xl">
              Unified enterprise backend powering ResearchOS: Hasura GraphQL engine with realtime subscriptions,
              PostgreSQL database with pgvector semantic similarity, Nhost Auth RBAC, and polite file storage.
            </p>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            <div className="p-3 rounded-xl border border-slate-800 bg-slate-900/80">
              <div className="text-xs text-slate-400">PostgreSQL Schema</div>
              <div className="text-lg font-bold text-white mt-1">25 Tables</div>
              <div className="text-[11px] text-emerald-400">Normalized & Indexed</div>
            </div>
            <div className="p-3 rounded-xl border border-slate-800 bg-slate-900/80">
              <div className="text-xs text-slate-400">Semantic Search</div>
              <div className="text-lg font-bold text-white mt-1">pgvector</div>
              <div className="text-[11px] text-indigo-400">384-d Cosine Distance</div>
            </div>
            <div className="p-3 rounded-xl border border-slate-800 bg-slate-900/80">
              <div className="text-xs text-slate-400">GraphQL Engine</div>
              <div className="text-lg font-bold text-white mt-1">Hasura v2.44</div>
              <div className="text-[11px] text-sky-400">Realtime Subscriptions</div>
            </div>
            <div className="p-3 rounded-xl border border-slate-800 bg-slate-900/80">
              <div className="text-xs text-slate-400">Storage & Integrity</div>
              <div className="text-lg font-bold text-white mt-1">SHA-256</div>
              <div className="text-[11px] text-amber-400">Nhost + Local Volumes</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="bg-slate-900/80 border border-slate-800 p-1 rounded-xl">
          <TabsTrigger value="semantic-search" className="data-[state=active]:bg-indigo-600 data-[state=active]:text-white gap-2">
            <Search className="h-4 w-4" />
            <span>pgvector Semantic Search</span>
          </TabsTrigger>
          <TabsTrigger value="graphql" className="data-[state=active]:bg-sky-600 data-[state=active]:text-white gap-2">
            <Code2 className="h-4 w-4" />
            <span>Hasura GraphQL Explorer</span>
          </TabsTrigger>
          <TabsTrigger value="auth" className="data-[state=active]:bg-emerald-600 data-[state=active]:text-white gap-2">
            <Lock className="h-4 w-4" />
            <span>Nhost Auth & RBAC</span>
          </TabsTrigger>
          <TabsTrigger value="storage" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white gap-2">
            <FolderLock className="h-4 w-4" />
            <span>Storage & Checksums</span>
          </TabsTrigger>
          <TabsTrigger value="architecture" className="data-[state=active]:bg-slate-800 data-[state=active]:text-white gap-2">
            <Server className="h-4 w-4" />
            <span>System Architecture</span>
          </TabsTrigger>
        </TabsList>

        {/* TAB 1: PGVECTOR SEMANTIC SEARCH */}
        <TabsContent value="semantic-search" className="space-y-4">
          <Card className="border-slate-800 bg-slate-900/60">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-indigo-400" />
                pgvector Hybrid Semantic Retrieval
              </CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Combines 384-dimensional dense vector embeddings with PostgreSQL lexical ranking to search
                across research paper abstracts, methodologies, limitations, and benchmark descriptions.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-400" />
                  <Input
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && !searching && handleSemanticSearch()}
                    placeholder="Search scientific methodology, limitations, or datasets..."
                    className="pl-10 h-11 bg-slate-950 border-slate-700 text-white placeholder:text-slate-500 rounded-xl"
                  />
                </div>
                <Button
                  onClick={handleSemanticSearch}
                  disabled={searching}
                  className="h-11 px-6 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium"
                >
                  {searching ? "Searching..." : "Vector Search"}
                </Button>
              </div>

              {/* Preset search queries */}
              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
                <span>Presets:</span>
                {[
                  "Sentinel-1 SAR speckle reduction deep learning",
                  "Siamese network change detection SpaceNet benchmark",
                  "Dual-temporal cross-attention multitemporal satellite imagery",
                ].map((q) => (
                  <button
                    key={q}
                    onClick={() => setSearchQuery(q)}
                    className="rounded-lg border border-slate-800 bg-slate-950 px-2.5 py-1 text-slate-300 hover:border-indigo-500/40 hover:text-indigo-300"
                  >
                    {q}
                  </button>
                ))}
              </div>

              {/* Results */}
              <div className="space-y-3 pt-2">
                {searchResults.length === 0 && !searching && (
                  <div className="text-center py-8 text-slate-400 text-sm">
                    Enter a research query above to test pgvector hybrid retrieval.
                  </div>
                )}

                {searchResults.map((match, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl border border-slate-800 bg-slate-950 flex flex-col gap-2 hover:border-slate-700 transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="font-mono text-xs uppercase border-indigo-500/40 text-indigo-300">
                          {match.chunk_type}
                        </Badge>
                        <span className="text-xs text-slate-400">
                          Paper ID: #{match.paper_id}
                        </span>
                      </div>
                      <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-500/40 text-xs">
                        Match Score: {(match.hybrid_score * 100).toFixed(1)}%
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed font-mono">
                      &quot;{match.content_snippet}&quot;
                    </p>
                    <div className="text-[11px] text-slate-500 flex items-center gap-4">
                      <span>Cosine Similarity: {match.semantic_similarity}</span>
                      <span>384-d Dense Embedding Vector</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* TAB 2: GRAPHQL EXPLORER */}
        <TabsContent value="graphql" className="space-y-4">
          <Card className="border-slate-800 bg-slate-900/60">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Code2 className="h-5 w-5 text-sky-400" />
                Hasura GraphQL Query & Mutation Console
              </CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Execute authorized GraphQL operations with Hasura row-level permissions.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-medium">GraphQL Query</span>
                    <button
                      onClick={() => setGraphqlQuery(`query GetResearchJobs {
  research_jobs(order_by: {created_at: desc}, limit: 5) {
    id
    job_type
    status
    progress_pct
    current_step
    created_at
  }
}`)}
                      className="text-sky-400 hover:underline"
                    >
                      Load Jobs Query
                    </button>
                  </div>
                  <textarea
                    value={graphqlQuery}
                    onChange={(e) => setGraphqlQuery(e.target.value)}
                    rows={12}
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 p-3 font-mono text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-sky-500"
                  />
                  <Button
                    onClick={handleExecuteGql}
                    disabled={executingGql}
                    className="w-full bg-sky-600 hover:bg-sky-500 text-white text-xs h-9"
                  >
                    {executingGql ? "Executing..." : "Run GraphQL Query"}
                  </Button>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-medium">Execution Output (JSON)</span>
                    {graphqlResult && (
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(graphqlResult);
                          toast.success("Copied to clipboard");
                        }}
                        className="text-xs text-slate-400 hover:text-white inline-flex items-center gap-1"
                      >
                        <Copy className="h-3 w-3" /> Copy
                      </button>
                    )}
                  </div>
                  <pre className="h-[285px] overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-3 font-mono text-xs text-emerald-400">
                    {graphqlResult || "// Click 'Run GraphQL Query' to inspect response payload."}
                  </pre>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* TAB 3: AUTH & RBAC */}
        <TabsContent value="auth" className="space-y-4">
          <Card className="border-slate-800 bg-slate-900/60">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Lock className="h-5 w-5 text-emerald-400" />
                Nhost Authentication & Hasura JWT Claims
              </CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Inspect Hasura row-level security claims (`https://hasura.io/jwt/claims`) and test role-based project isolation.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div>
                  <label className="text-xs text-slate-400 block mb-1">Researcher Email</label>
                  <Input
                    value={userEmail}
                    onChange={(e) => setUserEmail(e.target.value)}
                    className="bg-slate-950 border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-400 block mb-1">Assigned Role</label>
                  <select
                    value={selectedRole}
                    onChange={(e) => setSelectedRole(e.target.value)}
                    className="w-full h-9 rounded-md border border-slate-800 bg-slate-950 px-3 text-xs text-white"
                  >
                    <option value="user">User (Standard Researcher)</option>
                    <option value="admin">Administrator (Global Access)</option>
                    <option value="reviewer">Peer Reviewer (Read-Only)</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <Button
                    onClick={handleGenerateJwt}
                    className="w-full h-9 bg-emerald-600 hover:bg-emerald-500 text-white text-xs"
                  >
                    Generate Hasura JWT
                  </Button>
                </div>
              </div>

              {decodedClaims && (
                <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 space-y-2">
                  <div className="text-xs font-semibold text-emerald-300 flex items-center gap-2">
                    <UserCheck className="h-4 w-4" /> Hasura JWT Claims Token Active
                  </div>
                  <pre className="font-mono text-xs text-slate-300 bg-slate-900/80 p-3 rounded-lg overflow-x-auto">
                    {JSON.stringify(decodedClaims, null, 2)}
                  </pre>
                  <div className="text-[11px] text-slate-500">
                    Row-Level Security: Only projects matching <code>user_id == {decodedClaims["x-hasura-user-id"]}</code> are accessible.
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* TAB 4: STORAGE & CHECKSUMS */}
        <TabsContent value="storage" className="space-y-4">
          <Card className="border-slate-800 bg-slate-900/60">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <FolderLock className="h-5 w-5 text-amber-400" />
                Nhost File Storage & Checksum Verification
              </CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Upload research assets with automatic SHA-256 integrity hashing and local storage volume fallback.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-6 rounded-xl border border-dashed border-slate-700 bg-slate-950 text-center space-y-3">
                <Upload className="h-8 w-8 text-amber-400 mx-auto" />
                <div className="text-xs text-slate-300">
                  Select a research paper (PDF), dataset sample, or figure to upload
                </div>
                <input
                  type="file"
                  onChange={handleFileUpload}
                  disabled={uploading}
                  className="text-xs text-slate-400 file:mr-4 file:py-1.5 file:px-4 file:rounded-lg file:border-0 file:text-xs file:bg-amber-600 file:text-white hover:file:bg-amber-500 cursor-pointer"
                />
              </div>

              {uploadedFiles.length > 0 && (
                <div className="space-y-2">
                  <div className="text-xs font-medium text-slate-300">Recently Uploaded Files</div>
                  {uploadedFiles.map((file, i) => (
                    <div
                      key={i}
                      className="p-3 rounded-xl border border-slate-800 bg-slate-950 flex items-center justify-between gap-4 text-xs"
                    >
                      <div>
                        <div className="font-semibold text-white">{file.filename}</div>
                        <div className="font-mono text-[11px] text-slate-400">
                          SHA-256: {file.sha256}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-[11px] uppercase">
                          {file.storage_provider}
                        </Badge>
                        <Badge className="bg-emerald-500/20 text-emerald-300 text-[11px]">
                          {(file.file_size / (1024 * 1024)).toFixed(2)} MB
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* TAB 5: ARCHITECTURE */}
        <TabsContent value="architecture" className="space-y-4">
          <Card className="border-slate-800 bg-slate-900/60">
            <CardHeader>
              <CardTitle className="text-lg text-white">Full Stack Architecture Blueprint</CardTitle>
              <CardDescription className="text-xs text-slate-400">
                End-to-end integration topology between Nhost, PostgreSQL, Hasura, and FastAPI Python AI workers.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-xs text-slate-300 leading-relaxed font-mono">
              <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 space-y-2">
                <div className="text-sky-300 font-semibold">// 1. Nhost Core Services</div>
                <div>• PostgreSQL 16 + pgvector: Primary relational data store & 384-d semantic index</div>
                <div>• Hasura GraphQL Engine v2.44: Exposes authorized GraphQL API & WebSocket subscriptions</div>
                <div>• Nhost Auth (Hasura Auth): Issues JWT with `https://hasura.io/jwt/claims` for row-level security</div>
                <div>• Nhost Storage: S3-compatible file storage with signed URLs and SHA-256 checksums</div>
              </div>
              <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 space-y-2">
                <div className="text-emerald-300 font-semibold">// 2. FastAPI Scientific Backend</div>
                <div>• Autonomous Paper Discovery across 10 academic APIs with Unpaywall open PDF resolution</div>
                <div>• Free-first Dataset Discovery across 10 data repositories (Kaggle, Zenodo, Copernicus, etc.)</div>
                <div>• Paper-to-Dataset Linking Agent: Categorizes labeled benchmarks vs raw sensor feeds</div>
                <div>• PyTorch Lightning 80/20 non-leaking training studio and scientific evaluation engine</div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

