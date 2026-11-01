"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FolderPlus,
  Search,
  BookOpen,
  FileText,
  TableProperties,
  Target,
  Database,
  SlidersHorizontal,
  Layers,
  Cpu,
  Workflow,
  Code2,
  PlayCircle,
  FlaskConical,
  LineChart,
  Network,
  PenTool,
  BookmarkCheck,
  ShieldCheck,
  Send,
  Download,
  Settings,
  ChevronLeft,
  ChevronRight,
  Sparkles,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_GROUPS = [
  {
    label: "WORKSPACE",
    items: [
      { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { name: "New Research Project", href: "/projects/new", icon: FolderPlus },
    ],
  },
  {
    label: "RESEARCH INTELLIGENCE",
    items: [
      { name: "Paper Discovery", href: "/papers/discover", icon: Search },
      { name: "Research Library", href: "/library", icon: BookOpen },
      { name: "PDF Reader", href: "/papers/reader", icon: FileText },
      { name: "Literature Review", href: "/literature-review", icon: TableProperties },
      { name: "Gap Analysis", href: "/research-gaps", icon: Target },
    ],
  },
  {
    label: "DATASET STUDIO",
    items: [
      { name: "Dataset Discovery", href: "/datasets/discover", icon: Database },
      { name: "Processing Studio (80/20)", href: "/datasets/processing", icon: SlidersHorizontal },
      { name: "Dataset Explorer", href: "/datasets/explorer", icon: Layers },
    ],
  },
  {
    label: "MODEL & TRAINING",
    items: [
      { name: "Model Library", href: "/models/library", icon: Cpu },
      { name: "Architecture Editor", href: "/models/editor", icon: Workflow },
      { name: "Code Editor", href: "/code-editor", icon: Code2 },
      { name: "Training Studio", href: "/training", icon: PlayCircle },
      { name: "Experiment Tracking", href: "/experiments", icon: FlaskConical },
    ],
  },
  {
    label: "SCIENTIFIC RESULTS",
    items: [
      { name: "Results & Viz", href: "/results", icon: LineChart },
      { name: "Diagram Generator", href: "/diagrams", icon: Network },
    ],
  },
  {
    label: "PUBLICATION STUDIO",
    items: [
      { name: "Academic Writing", href: "/writing", icon: PenTool },
      { name: "Reference Manager", href: "/references", icon: BookmarkCheck },
      { name: "Originality Check", href: "/originality", icon: ShieldCheck },
      { name: "Journal Submission", href: "/journal", icon: Send },
      { name: "Project Export", href: "/export", icon: Download },
    ],
  },
  {
    label: "SYSTEM",
    items: [
      { name: "Settings & Integrations", href: "/settings", icon: Settings },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "relative flex flex-col border-r border-border bg-card/60 backdrop-blur-xl transition-all duration-300 z-30 select-none h-screen",
        collapsed ? "w-18" : "w-64"
      )}
    >
      {/* Brand Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border/80">
        {!collapsed && (
          <Link href="/dashboard" className="flex items-center gap-2.5 font-bold tracking-tight">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 text-white shadow-md shadow-blue-500/20">
              <Sparkles className="h-5 w-5" />
            </div>
            <div className="flex flex-col">
              <span className="text-base font-extrabold bg-gradient-to-r from-foreground via-foreground/90 to-muted-foreground bg-clip-text text-transparent">
                ResearchOS
              </span>
              <span className="text-[10px] font-medium text-blue-500 tracking-wider">
                AUTONOMOUS SYSTEM
              </span>
            </div>
          </Link>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      {/* Nav List */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6 scrollbar-thin scrollbar-thumb-muted">
        {NAV_GROUPS.map((group) => (
          <div key={group.label} className="space-y-1">
            {!collapsed && (
              <h4 className="px-3 text-[11px] font-semibold text-muted-foreground tracking-wider uppercase">
                {group.label}
              </h4>
            )}
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const Icon = item.icon;
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2 text-xs font-medium transition-colors",
                      active
                        ? "bg-primary text-primary-foreground shadow-sm"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                      collapsed && "justify-center px-2"
                    )}
                    title={collapsed ? item.name : undefined}
                  >
                    <Icon className={cn("h-4 w-4 shrink-0", active && "text-primary-foreground")} />
                    {!collapsed && <span className="truncate">{item.name}</span>}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Primary Project Badge at bottom */}
      {!collapsed && (
        <div className="p-3 border-t border-border/80 bg-muted/30">
          <div className="rounded-lg p-2.5 bg-background/80 border border-border shadow-xs text-xs space-y-1">
            <div className="flex items-center justify-between text-[11px] text-muted-foreground">
              <span>ACTIVE PROJECT</span>
              <span className="inline-block h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            </div>
            <p className="font-semibold text-foreground truncate" title="Sentinel-1 SAR Change Detection">
              Sentinel-1 SAR Change Detection
            </p>
            <p className="text-[10px] text-muted-foreground">IEEE J-STARS • 80/20 Split</p>
          </div>
        </div>
      )}
    </aside>
  );
}

