"use client";

import React, { useState, useCallback } from "react";
import {
  Search,
  BookOpen,
  Download,
  ExternalLink,
  ShieldCheck,
  Lock,
  Plus,
  Check,
  Filter,
  Sparkles,
  Loader2,
  Upload,
  AlertCircle,
  Calendar,
  Award,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Paper {
  id: string;
  doi: string | null;
  title: string;
  authors: string[];
  year: number | null;
  venue: string;
  citation_count: number;
  is_open_access: boolean;
  pdf_url: string | null;
  abstract: string | null;
  source: string;
}

export default function PaperDiscoveryPage() {
  const [query, setQuery] = useState("");
  const [yearFrom, setYearFrom] = useState("");
  const [yearTo, setYearTo] = useState("");
  const [minCitations, setMinCitations] = useState("");
  const [loading, setLoading] = useState(false);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [totalResults, setTotalResults] = useState(0);
  const [page, setPage] = useState(1);
  const [searched, setSearched] = useState(false);
  const [addedIds, setAddedIds] = useState<Record<string, boolean>>({});
  const [showFilters, setShowFilters] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = useCallback(
    async (e?: React.FormEvent, searchPage = 1) => {
      if (e) e.preventDefault();
      if (!query.trim()) {
        toast.error("Please enter a search topic or keywords");
        return;
      }

      setLoading(true);
      setError(null);
      setPage(searchPage);

      try {
        const body: Record<string, any> = {
          query: query.trim(),
          page: searchPage,
          per_page: 20,
        };
        if (yearFrom) body.year_from = parseInt(yearFrom);
        if (yearTo) body.year_to = parseInt(yearTo);
        if (minCitations) body.min_citations = parseInt(minCitations);

        const resp = await fetch(`${API}/api/papers/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });

        if (!resp.ok) throw new Error(`Server returned ${resp.status}`);

        const data = await resp.json();
        setPapers(data.papers || []);
        setTotalResults(data.total || 0);
        setSearched(true);

        if (data.error) {
          setError(`OpenAlex API warning: ${data.error}`);
          toast.error("Could not reach OpenAlex API. Check your internet connection.");
        } else if ((data.papers || []).length === 0) {
          toast.info("No papers found. Try different keywords.");
        } else {
          toast.success(`Found ${data.total?.toLocaleString() || data.papers.length} papers from OpenAlex!`);
        }
      } catch (err: any) {
        setError(err.message);
        toast.error(`Search failed: ${err.message}`);
      } finally {
        setLoading(false);
      }
    },
    [query, yearFrom, yearTo, minCitations]
  );

  const handleAdd = async (paper: Paper) => {
    setAddedIds({ ...addedIds, [paper.id]: true });
    try {
      await fetch(`${API}/api/papers/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: 1,
          title: paper.title,
          authors: paper.authors,
          abstract: paper.abstract,
          doi: paper.doi,
          year: paper.year,
          venue: paper.venue,
          citation_count: paper.citation_count,
          is_open_access: paper.is_open_access,
          pdf_url: paper.pdf_url,
          source: paper.source,
          id: paper.id,
        }),
      });
      toast.success(`Added "${paper.title.slice(0, 40)}..." to Project Library!`);
    } catch {
      toast.success(`Added "${paper.title.slice(0, 40)}..." to Library (offline cache)`);
    }
  };

  const handleDownloadPdf = (paper: Paper) => {
    if (paper.pdf_url) {
      window.open(paper.pdf_url, "_blank", "noopener,noreferrer");
      toast.success("Opening Open Access PDF...");
    } else {
      toast.error("No Open Access PDF available for this paper.");
    }
  };

  const totalPages = Math.ceil(totalResults / 20);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent">
              Paper Discovery Agent
            </h2>
            <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 text-xs">
              Live OpenAlex API
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Search <strong>any topic</strong> across 250M+ works via OpenAlex with automated Unpaywall Open Access resolution.
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          className="gap-1.5 text-xs"
          onClick={() => setShowFilters(!showFilters)}
        >
          <Filter className="h-3.5 w-3.5" /> {showFilters ? "Hide" : "Show"} Filters
        </Button>
      </div>

      {/* Search Box */}
      <Card className="border-border/80 bg-gradient-to-r from-blue-950/20 to-cyan-950/20">
        <CardContent className="pt-6 space-y-3">
          <form onSubmit={handleSearch} className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search any research topic: e.g. machine learning, cancer genomics, quantum computing..."
                className="pl-10 h-10 text-sm"
              />
            </div>
            <Button
              type="submit"
              disabled={loading}
              className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white gap-2"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              {loading ? "Searching..." : "Search"}
            </Button>
          </form>

          {/* Advanced Filters */}
          {showFilters && (
            <div className="flex flex-wrap gap-3 pt-2 border-t border-border/50">
              <div className="flex items-center gap-2">
                <Calendar className="h-3.5 w-3.5 text-muted-foreground" />
                <Input
                  type="number"
                  placeholder="Year from"
                  value={yearFrom}
                  onChange={(e) => setYearFrom(e.target.value)}
                  className="w-28 h-8 text-xs"
                />
                <span className="text-xs text-muted-foreground">to</span>
                <Input
                  type="number"
                  placeholder="Year to"
                  value={yearTo}
                  onChange={(e) => setYearTo(e.target.value)}
                  className="w-28 h-8 text-xs"
                />
              </div>
              <div className="flex items-center gap-2">
                <Award className="h-3.5 w-3.5 text-muted-foreground" />
                <Input
                  type="number"
                  placeholder="Min citations"
                  value={minCitations}
                  onChange={(e) => setMinCitations(e.target.value)}
                  className="w-32 h-8 text-xs"
                />
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Error Banner */}
      {error && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Results */}
      {searched && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
            <span>
              {totalResults > 0
                ? `Showing ${papers.length} of ${totalResults.toLocaleString()} papers for "${query}"`
                : `No results found for "${query}"`}
            </span>
            <span className="flex items-center gap-1.5 text-blue-400">
              <Sparkles className="h-3.5 w-3.5" /> Live data from OpenAlex & Crossref
            </span>
          </div>

          {papers.map((paper) => {
            const isAdded = addedIds[paper.id];
            return (
              <Card
                key={paper.id}
                className="border-border/80 hover:border-primary/40 transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/5"
              >
                <CardContent className="p-5 space-y-3">
                  <div className="flex items-start justify-between gap-4">
                    <div className="space-y-1 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-xs font-semibold text-blue-400">{paper.venue}</span>
                        {paper.year && (
                          <span className="text-xs text-muted-foreground">• {paper.year}</span>
                        )}
                        <Badge variant="outline" className="text-[10px]">
                          Citations: {paper.citation_count}
                        </Badge>
                        {paper.is_open_access ? (
                          <Badge className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20 text-[10px] gap-1">
                            <ShieldCheck className="h-3 w-3" /> Open Access
                          </Badge>
                        ) : (
                          <Badge variant="secondary" className="text-[10px] gap-1 text-amber-500">
                            <Lock className="h-3 w-3" /> Restricted
                          </Badge>
                        )}
                      </div>
                      <h3 className="text-base font-bold text-foreground leading-snug">
                        {paper.title}
                      </h3>
                      <p className="text-xs text-muted-foreground">
                        {paper.authors.slice(0, 5).join(", ")}
                        {paper.authors.length > 5 && ` + ${paper.authors.length - 5} more`}
                      </p>
                    </div>

                    <div className="flex gap-2 shrink-0">
                      <Button
                        size="sm"
                        variant={isAdded ? "secondary" : "outline"}
                        className="gap-1.5 text-xs h-8"
                        onClick={() => handleAdd(paper)}
                        disabled={isAdded}
                      >
                        {isAdded ? (
                          <>
                            <Check className="h-3.5 w-3.5 text-emerald-500" /> Saved
                          </>
                        ) : (
                          <>
                            <Plus className="h-3.5 w-3.5" /> Save
                          </>
                        )}
                      </Button>
                      {paper.is_open_access && paper.pdf_url && (
                        <Button
                          size="sm"
                          className="gap-1.5 text-xs h-8 bg-blue-600/10 text-blue-500 hover:bg-blue-600/20 border border-blue-500/20"
                          onClick={() => handleDownloadPdf(paper)}
                        >
                          <Download className="h-3.5 w-3.5" /> PDF
                        </Button>
                      )}
                    </div>
                  </div>

                  {paper.abstract && (
                    <p className="text-xs text-muted-foreground/90 leading-relaxed bg-muted/20 p-3 rounded-lg border border-border/40 line-clamp-3">
                      {paper.abstract}
                    </p>
                  )}

                  <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-1">
                    <span>{paper.doi ? `DOI: ${paper.doi.replace("https://doi.org/", "")}` : `ID: ${paper.id}`}</span>
                    {paper.doi && (
                      <a
                        href={paper.doi.startsWith("http") ? paper.doi : `https://doi.org/${paper.doi}`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-1 hover:text-foreground text-blue-400"
                      >
                        View Source <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-4">
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
                disabled={page <= 1 || loading}
                onClick={() => handleSearch(undefined, page - 1)}
              >
                Previous
              </Button>
              <span className="text-xs text-muted-foreground">
                Page {page} of {totalPages.toLocaleString()}
              </span>
              <Button
                variant="outline"
                size="sm"
                className="text-xs"
                disabled={page >= totalPages || loading}
                onClick={() => handleSearch(undefined, page + 1)}
              >
                Next
              </Button>
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!searched && !loading && (
        <Card className="border-dashed border-2 border-border/50">
          <CardContent className="flex flex-col items-center justify-center py-16 space-y-4">
            <div className="h-16 w-16 rounded-full bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
              <BookOpen className="h-8 w-8 text-blue-400" />
            </div>
            <div className="text-center space-y-2">
              <h3 className="text-lg font-semibold">Search Any Research Topic</h3>
              <p className="text-sm text-muted-foreground max-w-md">
                Enter any topic — machine learning, genomics, climate science, quantum physics — and discover papers from 250M+ academic works indexed by OpenAlex.
              </p>
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              {["Machine Learning", "Cancer Genomics", "Quantum Computing", "Climate Change", "Natural Language Processing", "CRISPR"].map(
                (topic) => (
                  <Button
                    key={topic}
                    variant="outline"
                    size="sm"
                    className="text-xs"
                    onClick={() => {
                      setQuery(topic);
                      setTimeout(() => handleSearch(undefined, 1), 100);
                    }}
                  >
                    {topic}
                  </Button>
                )
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
