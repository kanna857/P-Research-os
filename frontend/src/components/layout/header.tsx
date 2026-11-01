"use client";

import React from "react";
import { useTheme } from "next-themes";
import { Search, Sun, Moon, Sparkles, Activity, ShieldCheck, Flame } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Header({ title }: { title?: string }) {
  const { theme, setTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex h-16 w-full items-center justify-between border-b border-border/80 bg-background/80 px-6 backdrop-blur-xl transition-colors">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-sky-400 via-indigo-500 to-purple-500 bg-clip-text text-transparent">
          {title || "ResearchOS"}
        </h1>
        <Badge className="hidden sm:inline-flex items-center gap-1.5 border-cyan-500/40 text-cyan-400 bg-cyan-500/10 text-xs py-0.5 shadow-sm shadow-cyan-500/10 hover:bg-cyan-500/20">
          <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
          Primary Benchmark: Sentinel-1 SAR (IEEE J-STARS)
        </Badge>
        <span className="hidden lg:inline-flex text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-gradient-to-r from-emerald-500/15 to-teal-500/15 border border-emerald-500/30 text-emerald-400">
          Strict 80% Train / 20% Test Verified
        </span>
      </div>

      <div className="flex items-center gap-3">
        {/* Quick Search */}
        <div className="relative hidden md:block w-72">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-cyan-400" />
          <input
            type="text"
            placeholder="Search papers, models, data, citations..."
            className="w-full rounded-xl border border-border/80 bg-muted/40 pl-9 pr-4 py-1.5 text-xs ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 focus-visible:border-cyan-500 transition-all shadow-inner"
          />
        </div>

        {/* Theme Toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="rounded-xl h-9 w-9 text-muted-foreground hover:text-foreground hover:bg-accent/80 border border-border/60 transition-colors"
          title="Toggle dark/light mode"
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0 text-amber-500" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 text-sky-400" />
        </Button>

        {/* Live telemetry & WebSocket status */}
        <div className="flex items-center gap-2 pl-2 border-l border-border">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-gradient-to-r from-emerald-500/20 to-teal-500/20 border border-emerald-500/40 text-emerald-400 text-xs font-bold shadow-sm shadow-emerald-500/10">
            <Activity className="h-3.5 w-3.5 animate-pulse text-emerald-400" />
            <span className="font-mono text-[11px]">TELEMETRY: ONLINE</span>
          </div>
        </div>
      </div>
    </header>
  );
}
