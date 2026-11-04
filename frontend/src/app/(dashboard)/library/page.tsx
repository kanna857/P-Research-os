"use client";

import React, { useState, useRef, useCallback } from "react";
import Link from "next/link";
import {
  BookOpen,
  Download,
  Upload,
  FileText,
  CheckCircle2,
  Lock,
  ExternalLink,
  TableProperties,
  ArrowRight,
  Loader2,
  X,
  File,
  AlertCircle,
  RefreshCw,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { toast } from "sonner";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface LibraryPaper {
  id: number;
  title: string;
  authors: string | string[];
  year: number | null;
  venue: string;
  doi: string | null;
  status: string;
  isOA: boolean;
  hasPdf: boolean;
  pdf_path?: string;
}

export default function ResearchLibraryPage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const inlineFileRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadTarget, setUploadTarget] = useState<number | null>(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploadDoi, setUploadDoi] = useState("");

  const [papers, setPapers] = useState<LibraryPaper[]>([
    {
      id: 1,
      title: "A Deep Convolutional Coupling Network for Change Detection in Multitemporal SAR Images",
      authors: "G. Gong et al.",
      year: 2023,
      venue: "IEEE TGRS",
      doi: "10.1109/TGRS.2023.3245671",
      status: "Extracted (Docling)",
      isOA: true,
      hasPdf: true,
    },
    {
      id: 2,
      title: "Siamese-Based Multiscale Attention Networks for High-Resolution Remote Sensing Change Detection",
      authors: "C. Zhang et al.",
      year: 2024,
      venue: "IEEE J-STARS",
      doi: "10.1109/JSTARS.2024.3359012",
      status: "Extracted (Docling)",
      isOA: true,
      hasPdf: true,
    },
    {
      id: 3,
      title: "Deep Learning in Remote Sensing: A Review and Global Benchmark",
      authors: "X. Zhu et al.",
      year: 2022,
      venue: "IEEE MGRS",
      doi: "10.1109/MGRS.2022.3168750",
      status: "Extracted (Docling)",
      isOA: true,
      hasPdf: true,
    },
    {
      id: 4,
      title: "Self-Supervised Feature Representation for Multitemporal SAR Coherence",
      authors: "E. Rostova et al.",
      year: 2023,
      venue: "ISPRS Journal",
      doi: "10.1016/j.isprsjprs.2023.08.015",
      status: "Requires PDF Upload",
      isOA: false,
      hasPdf: false,
    },
  ]);

  const handleUploadPdf = useCallback(
    async (file: File, paperId?: number) => {
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        toast.error("Only PDF files are accepted");
        return;
      }

      if (file.size > 100 * 1024 * 1024) {
        toast.error("File too large. Maximum 100MB.");
        return;
      }

      setUploading(true);
      setUploadTarget(paperId ?? null);

      try {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("project_id", "1");
        if (uploadTitle) formData.append("title", uploadTitle);
        if (uploadDoi) formData.append("doi", uploadDoi);

        const resp = await fetch(`${API}/api/papers/upload?project_id=1`, {
          method: "POST",
          body: formData,
        });

        if (!resp.ok) {
          const errData = await resp.json().catch(() => ({}));
          throw new Error(errData.detail || `Upload failed (${resp.status})`);
        }

        const result = await resp.json();

        // Add or update paper in local state
        if (paperId) {
          setPapers((prev) =>
            prev.map((p) =>
              p.id === paperId
                ? {
                    ...p,
                    hasPdf: true,
                    status: "Extracted (Docling)",
                    pdf_path: result.pdf_path,
                  }
                : p
            )
          );
        } else {
          const newPaper: LibraryPaper = {
            id: result.id || Date.now(),
            title: result.title || file.name.replace(".pdf", ""),
            authors: Array.isArray(result.authors) ? result.authors.join(", ") : (result.authors || "Uploaded"),
            year: result.year || new Date().getFullYear(),
            venue: "User Upload",
            doi: result.doi || uploadDoi || null,
            status: "Extracted (Docling)",
            isOA: true,
            hasPdf: true,
            pdf_path: result.pdf_path,
          };
          setPapers((prev) => [newPaper, ...prev]);
        }

        toast.success(`✅ "${file.name}" uploaded and parsed successfully!`);
        setShowUploadModal(false);
        setUploadTitle("");
        setUploadDoi("");
      } catch (err: any) {
        toast.error(`Upload failed: ${err.message}`);
      } finally {
        setUploading(false);
        setUploadTarget(null);
      }
    },
    [uploadTitle, uploadDoi]
  );

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>, paperId?: number) => {
    const file = e.target.files?.[0];
    if (file) handleUploadPdf(file, paperId);
    e.target.value = "";
  };

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file) handleUploadPdf(file);
    },
    [handleUploadPdf]
  );

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  return (
    <div className="space-y-6">
      {/* Hidden file inputs */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,application/pdf"
        className="hidden"
        onChange={(e) => handleFileSelect(e)}
      />
      <input
        ref={inlineFileRef}
        type="file"
        accept=".pdf,application/pdf"
        className="hidden"
        onChange={(e) => handleFileSelect(e, uploadTarget ?? undefined)}
      />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-violet-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Research Library
            </h2>
            <Badge className="bg-violet-500/10 text-violet-400 border-violet-500/20 text-xs">
              Docling + GROBID
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Manage your project literature, upload PDFs, and extract structured content with Docling.
          </p>
        </div>
        <div className="flex gap-2">
          <Link href="/literature-review">
            <Button variant="outline" className="gap-2 text-xs">
              <TableProperties className="h-4 w-4" /> Comparison Matrix
            </Button>
          </Link>
          <Button
            className="bg-gradient-to-r from-violet-600 to-blue-600 hover:from-violet-500 hover:to-blue-500 text-white gap-2 text-xs"
            onClick={() => setShowUploadModal(true)}
            disabled={uploading}
          >
            {uploading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Upload className="h-4 w-4" />
            )}
            Upload PDF
          </Button>
        </div>
      </div>

      {/* Upload Modal / Drop Zone */}
      {showUploadModal && (
        <Card className="border-2 border-dashed border-violet-500/40 bg-gradient-to-r from-violet-950/20 to-blue-950/20">
          <CardContent className="pt-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold flex items-center gap-2">
                <Upload className="h-4 w-4 text-violet-400" /> Upload Research Paper PDF
              </h3>
              <Button variant="ghost" size="sm" onClick={() => setShowUploadModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>

            {/* Optional metadata */}
            <div className="grid grid-cols-2 gap-3">
              <Input
                placeholder="Paper title (optional, extracted from PDF)"
                value={uploadTitle}
                onChange={(e) => setUploadTitle(e.target.value)}
                className="h-8 text-xs"
              />
              <Input
                placeholder="DOI (optional, e.g. 10.1109/TGRS.2023...)"
                value={uploadDoi}
                onChange={(e) => setUploadDoi(e.target.value)}
                className="h-8 text-xs"
              />
            </div>

            {/* Drop Zone */}
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              className="flex flex-col items-center justify-center p-8 rounded-lg border-2 border-dashed border-border/60 hover:border-violet-500/60 transition-colors cursor-pointer bg-muted/10"
              onClick={() => fileInputRef.current?.click()}
            >
              {uploading ? (
                <div className="flex flex-col items-center gap-3">
                  <Loader2 className="h-10 w-10 animate-spin text-violet-400" />
                  <p className="text-sm text-muted-foreground">Uploading and extracting content...</p>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-3">
                  <div className="h-14 w-14 rounded-full bg-violet-500/10 flex items-center justify-center">
                    <File className="h-7 w-7 text-violet-400" />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-medium">
                      Drop PDF here or <span className="text-violet-400 underline">click to browse</span>
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Supports .pdf files up to 100MB. Content will be parsed by Docling / PyPDF.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Papers Table */}
      <Card className="border-border/80">
        <CardHeader>
          <CardTitle className="text-base font-semibold">
            Indexed Project Literature ({papers.length} Works)
          </CardTitle>
          <CardDescription className="text-xs">
            Documents parsed into structured sections and vector passage indexes for grounded synthesis.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Paper Title & Authors</TableHead>
                <TableHead>Venue / Year</TableHead>
                <TableHead>Access Status</TableHead>
                <TableHead>Docling / GROBID</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {papers.map((p) => (
                <TableRow key={p.id} className="hover:bg-muted/30">
                  <TableCell className="max-w-md">
                    <div className="font-semibold text-foreground text-xs">{p.title}</div>
                    <div className="text-[11px] text-muted-foreground">
                      {Array.isArray(p.authors) ? p.authors.join(", ") : p.authors}
                    </div>
                  </TableCell>
                  <TableCell className="text-xs">
                    <span className="font-medium text-blue-400">{p.venue}</span>
                    {p.year && <span className="text-muted-foreground ml-1">({p.year})</span>}
                  </TableCell>
                  <TableCell>
                    {p.isOA ? (
                      <Badge className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20 text-[10px]">
                        Open Access
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="text-[10px] text-amber-500 gap-1">
                        <Lock className="h-2.5 w-2.5" /> Restricted
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant="outline"
                      className={`text-[10px] gap-1 ${
                        p.hasPdf ? "" : "text-amber-500 border-amber-500/30"
                      }`}
                    >
                      {p.hasPdf ? (
                        <CheckCircle2 className="h-3 w-3 text-emerald-500" />
                      ) : (
                        <AlertCircle className="h-3 w-3" />
                      )}
                      {p.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Link href="/papers/reader">
                        <Button size="sm" variant="outline" className="h-7 text-xs gap-1">
                          <FileText className="h-3 w-3" /> Read
                        </Button>
                      </Link>
                      {p.hasPdf ? (
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-7 text-xs gap-1"
                          onClick={() => toast.success("Opening PDF reader...")}
                        >
                          <Download className="h-3 w-3" />
                        </Button>
                      ) : (
                        <Button
                          size="sm"
                          variant="secondary"
                          className="h-7 text-xs gap-1 text-violet-400 hover:text-violet-300"
                          disabled={uploading && uploadTarget === p.id}
                          onClick={() => {
                            setUploadTarget(p.id);
                            inlineFileRef.current?.click();
                          }}
                        >
                          {uploading && uploadTarget === p.id ? (
                            <Loader2 className="h-3 w-3 animate-spin" />
                          ) : (
                            <Upload className="h-3 w-3" />
                          )}
                          Upload PDF
                        </Button>
                      )}
                    </div>
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
