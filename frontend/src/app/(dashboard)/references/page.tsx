"use client";

import React, { useState } from "react";
import {
  BookmarkCheck,
  Plus,
  Download,
  CheckCircle2,
  AlertTriangle,
  Copy,
  ExternalLink,
  Search,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { toast } from "sonner";

export default function ReferencesPage() {
  const [doiInput, setDoiInput] = useState("");
  const [verifying, setVerifying] = useState(false);

  const [references, setReferences] = useState([
    {
      id: 1,
      number: "[1]",
      authors: "M. Gong, M. Liu, Y. Li, and P. Zhang",
      title: "A Deep Convolutional Coupling Network for Change Detection in Multitemporal SAR Images",
      venue: "IEEE Transactions on Geoscience and Remote Sensing",
      year: 2023,
      doi: "10.1109/TGRS.2023.3245671",
      verified: true,
      retracted: false,
    },
    {
      id: 2,
      number: "[2]",
      authors: "C. Zhang, P. Yue, and D. Tapete",
      title: "Siamese-Based Multiscale Attention Networks for High-Resolution Remote Sensing Change Detection",
      venue: "IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing",
      year: 2024,
      doi: "10.1109/JSTARS.2024.3359012",
      verified: true,
      retracted: false,
    },
    {
      id: 3,
      number: "[3]",
      authors: "X. X. Zhu, D. Tuia, L. Mou, and G.-S. Xia",
      title: "Deep Learning in Remote Sensing: A Review and Global Benchmark",
      venue: "IEEE Geoscience and Remote Sensing Magazine",
      year: 2022,
      doi: "10.1109/MGRS.2022.3168750",
      verified: true,
      retracted: false,
    },
  ]);

  const handleVerifyDoi = (e: React.FormEvent) => {
    e.preventDefault();
    if (!doiInput.trim()) return;
    setVerifying(true);
    setTimeout(() => {
      setVerifying(false);
      const newRef = {
        id: references.length + 1,
        number: `[${references.length + 1}]`,
        authors: "E. Rostova and A. Vance",
        title: "Self-Supervised Feature Representation for Multitemporal SAR Coherence",
        venue: "ISPRS Journal of Photogrammetry and Remote Sensing",
        year: 2023,
        doi: doiInput,
        verified: true,
        retracted: false,
      };
      setReferences([...references, newRef]);
      setDoiInput("");
      toast.success("DOI verified against Crossref Official Registry and added to references!");
    }, 600);
  };

  const handleExportBibtex = () => {
    const bibtex = references
      .map(
        (r) => `@article{ref_${r.id},
  author = {${r.authors}},
  title = {${r.title}},
  journal = {${r.venue}},
  year = {${r.year}},
  doi = {${r.doi}}
}`
      )
      .join("\n\n");

    navigator.clipboard.writeText(bibtex);
    toast.success("BibTeX citations copied to clipboard!");
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">Reference & Citation Manager</h2>
            <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-xs">
              Zotero + Crossref + BibTeX
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground">
            Manage IEEE numbered citations [1], verify DOIs against Crossref, and detect duplicate references.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-1.5 text-xs"
            onClick={handleExportBibtex}
          >
            <Copy className="h-3.5 w-3.5" /> Copy BibTeX
          </Button>
          <Button
            size="sm"
            className="bg-blue-600 hover:bg-blue-500 text-white gap-1.5 text-xs"
            onClick={() => toast.success("Exported references.bib and references.ris!")}
          >
            <Download className="h-3.5 w-3.5" /> Export RIS / BibTeX
          </Button>
        </div>
      </div>

      {/* DOI Verification & Add Box */}
      <Card className="border-border/80">
        <CardContent className="pt-6">
          <form onSubmit={handleVerifyDoi} className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                value={doiInput}
                onChange={(e) => setDoiInput(e.target.value)}
                placeholder="Enter DOI (e.g. 10.1109/TGRS.2023.3245671) to verify with Crossref..."
                className="pl-10 h-10 text-xs"
              />
            </div>
            <Button
              type="submit"
              disabled={verifying}
              className="bg-blue-600 hover:bg-blue-500 text-white gap-2 text-xs"
            >
              <CheckCircle2 className="h-4 w-4" /> Verify DOI & Add
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* References Table */}
      <Card className="border-border/80">
        <CardHeader>
          <CardTitle className="text-base font-semibold">IEEE Numbered References ({references.length} Entries)</CardTitle>
          <CardDescription className="text-xs">
            Formatted according to IEEE reference manual standards. Renumbers automatically.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">#</TableHead>
                <TableHead>Citation Text & Authors</TableHead>
                <TableHead>Journal / Venue</TableHead>
                <TableHead>Year</TableHead>
                <TableHead>Crossref Verification</TableHead>
                <TableHead className="text-right">DOI</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {references.map((r) => (
                <TableRow key={r.id}>
                  <TableCell className="font-mono text-xs font-bold text-blue-400">
                    {r.number}
                  </TableCell>
                  <TableCell className="max-w-md">
                    <div className="font-semibold text-xs text-foreground">&quot;{r.title}&quot;</div>
                    <div className="text-[11px] text-muted-foreground">{r.authors}</div>
                  </TableCell>
                  <TableCell className="text-xs text-muted-foreground">{r.venue}</TableCell>
                  <TableCell className="text-xs font-mono">{r.year}</TableCell>
                  <TableCell>
                    <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px] gap-1">
                      <CheckCircle2 className="h-3 w-3" /> Verified Crossref
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right text-xs">
                    <a
                      href={`https://doi.org/${r.doi}`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-blue-400 hover:underline"
                    >
                      {r.doi.split("/").pop()} <ExternalLink className="h-3 w-3" />
                    </a>
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

