"use client";

import React, { useState } from "react";
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
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { toast } from "sonner";

export default function ResearchLibraryPage() {
  const [papers] = useState([
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

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Research Library</h2>
          <p className="text-xs text-muted-foreground">
            Manage your project literature collection, legal PDF downloads, and Docling document extractions.
          </p>
        </div>
        <div className="flex gap-2">
          <Link href="/literature-review">
            <Button variant="outline" className="gap-2 text-xs">
              <TableProperties className="h-4 w-4" /> Comparison Matrix
            </Button>
          </Link>
          <Button
            className="bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs"
            onClick={() => toast.info("Select PDF file to upload...")}
          >
            <Upload className="h-4 w-4" /> Upload Legal PDF
          </Button>
        </div>
      </div>

      <Card className="border-border/80">
        <CardHeader>
          <CardTitle className="text-base font-semibold">Indexed Project Literature ({papers.length} Works)</CardTitle>
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
                <TableRow key={p.id}>
                  <TableCell className="max-w-md">
                    <div className="font-semibold text-foreground text-xs">{p.title}</div>
                    <div className="text-[11px] text-muted-foreground">{p.authors}</div>
                  </TableCell>
                  <TableCell className="text-xs">
                    <span className="font-medium text-blue-400">{p.venue}</span>
                    <span className="text-muted-foreground ml-1">({p.year})</span>
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
                    <Badge variant="outline" className="text-[10px] gap-1">
                      <CheckCircle2 className="h-3 w-3 text-emerald-500" /> {p.status}
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
                          className="h-7 text-xs gap-1"
                          onClick={() => toast.info("Please upload legally obtained PDF")}
                        >
                          <Upload className="h-3 w-3" /> Upload
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

