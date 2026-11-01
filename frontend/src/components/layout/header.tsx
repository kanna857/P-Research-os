"use client";

import React from "react";
import { useTheme } from "next-themes";
import { Search, Sun, Moon, Bell, ShieldCheck, GitBranch } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Header({ title }: { title?: string }) {
  const { theme, setTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex h-16 w-full items-center justify-between border-b border-border bg-background/80 px-6 backdrop-blur-md">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold tracking-tight text-foreground">
          {title || "ResearchOS"}
        </h1>
        <Badge variant="outline" className="hidden sm:inline-flex items-center gap-1.5 border-blue-500/30 text-blue-500 bg-blue-500/5 text-xs py-0.5">
          <span className="h-1.5 w-1.5 rounded-full bg-blue-500 animate-pulse" />
          Primary Benchmark: Sentinel-1 SAR
        </Badge>
      </div>

      <div className="flex items-center gap-3">
        {/* Quick Search */}
        <div className="relative hidden md:block w-64">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search papers, models, data..."
            className="w-full rounded-md border border-input bg-muted/40 pl-9 pr-4 py-1.5 text-xs ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>

        {/* Theme Toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="rounded-full h-8 w-8 text-muted-foreground hover:text-foreground"
          title="Toggle dark/light mode"
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        </Button>

        {/* Notifications / Live telemetry badge */}
        <div className="flex items-center gap-2 pl-2 border-l border-border">
          <Badge variant="secondary" className="text-[11px] font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10">
            WS: Connected
          </Badge>
        </div>
      </div>
    </header>
  );
}

