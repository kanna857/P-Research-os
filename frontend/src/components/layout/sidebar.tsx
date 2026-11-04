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
  Info,
  Globe,
  Compass,
  ShieldAlert,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_GROUPS = [
  {
    label: "WORKSPACE",
    color: "text-sky-400",
    items: [
      { name: "Universal Autopilot Ω", href: "/autopilot", icon: Sparkles, iconColor: "text-amber-400", activeBg: "bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600" },
      { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard, iconColor: "text-sky-400", activeBg: "bg-gradient-to-r from-sky-500 to-blue-600" },
      { name: "New Research Project", href: "/projects/new", icon: FolderPlus, iconColor: "text-emerald-400", activeBg: "bg-gradient-to-r from-emerald-500 to-teal-600" },
    ],
  },
  {
    label: "RESEARCH INTELLIGENCE",
    color: "text-violet-400",
    items: [
      { name: "Domain Explorer (36)", href: "/domains", icon: Compass, iconColor: "text-cyan-400", activeBg: "bg-gradient-to-r from-cyan-500 to-blue-600" },
      { name: "Autonomous Discovery", href: "/discovery", icon: Compass, iconColor: "text-amber-400", activeBg: "bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600" },
      { name: "Paper Discovery", href: "/papers/discover", icon: Search, iconColor: "text-blue-400", activeBg: "bg-gradient-to-r from-blue-500 to-indigo-600" },
      { name: "Web Crawling Studio", href: "/crawling", icon: Globe, iconColor: "text-emerald-400", activeBg: "bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-600" },
      { name: "Research Library", href: "/library", icon: BookOpen, iconColor: "text-violet-400", activeBg: "bg-gradient-to-r from-violet-500 to-purple-600" },
      { name: "PDF Reader", href: "/papers/reader", icon: FileText, iconColor: "text-pink-400", activeBg: "bg-gradient-to-r from-pink-500 to-rose-600" },
      { name: "Literature Review", href: "/literature-review", icon: TableProperties, iconColor: "text-purple-400", activeBg: "bg-gradient-to-r from-purple-500 to-indigo-600" },
      { name: "Gap Analysis", href: "/research-gaps", icon: Target, iconColor: "text-rose-400", activeBg: "bg-gradient-to-r from-rose-500 to-red-600" },
      { name: "Evidence Verification", href: "/evidence", icon: ShieldCheck, iconColor: "text-emerald-400", activeBg: "bg-gradient-to-r from-emerald-500 to-teal-600" },
    ],
  },
  {
    label: "DATASET STUDIO",
    color: "text-amber-400",
    items: [
      { name: "Dataset Discovery", href: "/datasets/discover", icon: Database, iconColor: "text-amber-400", activeBg: "bg-gradient-to-r from-amber-500 to-orange-600" },
      { name: "Processing Studio (80/20)", href: "/datasets/processing", icon: SlidersHorizontal, iconColor: "text-orange-400", activeBg: "bg-gradient-to-r from-orange-500 to-amber-600" },
      { name: "Dataset Explorer", href: "/datasets/explorer", icon: Layers, iconColor: "text-lime-400", activeBg: "bg-gradient-to-r from-lime-500 to-emerald-600" },
    ],
  },
  {
    label: "MODEL & TRAINING",
    color: "text-cyan-400",
    items: [
      { name: "Model Library", href: "/models/library", icon: Cpu, iconColor: "text-cyan-400", activeBg: "bg-gradient-to-r from-cyan-500 to-blue-600" },
      { name: "Architecture Editor", href: "/models/editor", icon: Workflow, iconColor: "text-indigo-400", activeBg: "bg-gradient-to-r from-indigo-500 to-purple-600" },
      { name: "Code Editor", href: "/code-editor", icon: Code2, iconColor: "text-teal-400", activeBg: "bg-gradient-to-r from-teal-500 to-cyan-600" },
      { name: "Training Studio", href: "/training", icon: PlayCircle, iconColor: "text-red-400", activeBg: "bg-gradient-to-r from-red-500 to-rose-600" },
      { name: "Experiment Tracking", href: "/experiments", icon: FlaskConical, iconColor: "text-yellow-400", activeBg: "bg-gradient-to-r from-yellow-500 to-amber-600" },
    ],
  },
  {
    label: "SCIENTIFIC RESULTS",
    color: "text-emerald-400",
    items: [
      { name: "Statistical Studio", href: "/statistics", icon: LineChart, iconColor: "text-emerald-400", activeBg: "bg-gradient-to-r from-emerald-500 to-teal-600" },
      { name: "Simulation Studio", href: "/simulation", icon: Cpu, iconColor: "text-cyan-400", activeBg: "bg-gradient-to-r from-cyan-500 to-indigo-600" },
      { name: "Results & Viz", href: "/results", icon: LineChart, iconColor: "text-emerald-400", activeBg: "bg-gradient-to-r from-emerald-500 to-green-600" },
      { name: "Diagram Generator", href: "/diagrams", icon: Network, iconColor: "text-fuchsia-400", activeBg: "bg-gradient-to-r from-fuchsia-500 to-pink-600" },
    ],
  },
  {
    label: "PUBLICATION STUDIO",
    color: "text-fuchsia-400",
    items: [
      { name: "Ethics & Compliance", href: "/ethics", icon: ShieldAlert, iconColor: "text-rose-400", activeBg: "bg-gradient-to-r from-rose-500 to-red-600" },
      { name: "Originality Studio", href: "/writing/originality-studio", icon: Sparkles, iconColor: "text-amber-400", activeBg: "bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600" },
      { name: "Academic Writing", href: "/writing", icon: PenTool, iconColor: "text-violet-400", activeBg: "bg-gradient-to-r from-violet-500 to-purple-600" },
      { name: "Reference Manager", href: "/references", icon: BookmarkCheck, iconColor: "text-blue-400", activeBg: "bg-gradient-to-r from-blue-500 to-sky-600" },
      { name: "Research Integrity", href: "/integrity", icon: ShieldCheck, iconColor: "text-rose-400", activeBg: "bg-gradient-to-r from-rose-500 to-red-600" },
      { name: "Reproducibility Engine", href: "/reproducibility", icon: Layers, iconColor: "text-cyan-400", activeBg: "bg-gradient-to-r from-cyan-500 to-blue-600" },
      { name: "Originality Check", href: "/originality", icon: ShieldCheck, iconColor: "text-green-400", activeBg: "bg-gradient-to-r from-green-500 to-emerald-600" },
      { name: "Journal Submission", href: "/journal", icon: Send, iconColor: "text-indigo-400", activeBg: "bg-gradient-to-r from-indigo-500 to-blue-600" },
      { name: "Project Export", href: "/export", icon: Download, iconColor: "text-orange-400", activeBg: "bg-gradient-to-r from-orange-500 to-red-600" },
    ],
  },
  {
    label: "SYSTEM",
    color: "text-slate-400",
    items: [
      { name: "System Monitoring", href: "/monitoring", icon: LineChart, iconColor: "text-teal-400", activeBg: "bg-gradient-to-r from-teal-500 to-emerald-600" },
      { name: "Nhost & PostgreSQL", href: "/nhost", icon: Database, iconColor: "text-indigo-400", activeBg: "bg-gradient-to-r from-indigo-500 to-purple-600" },
      { name: "Settings & Integrations", href: "/settings", icon: Settings, iconColor: "text-slate-300", activeBg: "bg-gradient-to-r from-slate-600 to-gray-700" },
      { name: "About ResearchOS", href: "/about", icon: Info, iconColor: "text-cyan-400", activeBg: "bg-gradient-to-r from-cyan-500 to-blue-600" },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "relative flex flex-col border-r border-border/80 bg-slate-950/80 backdrop-blur-2xl transition-all duration-300 z-30 select-none h-screen shadow-2xl",
        collapsed ? "w-18" : "w-64"
      )}
    >
      {/* Brand Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-white/10 bg-gradient-to-r from-blue-950/50 via-indigo-950/40 to-purple-950/50">
        {!collapsed && (
          <Link href="/dashboard" className="flex items-center gap-2.5 font-bold tracking-tight group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform duration-200">
              <Sparkles className="h-5 w-5 animate-pulse" />
            </div>
            <div className="flex flex-col">
              <span className="text-base font-black bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                ResearchOS
              </span>
              <span className="text-[10px] font-bold tracking-widest bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                AUTONOMOUS SYSTEM
              </span>
            </div>
          </Link>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg text-slate-400 hover:bg-white/10 hover:text-white transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      {/* Nav List */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6 scrollbar-thin scrollbar-thumb-white/10">
        {NAV_GROUPS.map((group) => (
          <div key={group.label} className="space-y-1">
            {!collapsed && (
              <h4 className={cn("px-3 text-[10px] font-extrabold tracking-wider uppercase opacity-80", group.color)}>
                {group.label}
              </h4>
            )}
            <div className="space-y-1">
              {group.items.map((item) => {
                const Icon = item.icon;
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2 text-xs font-semibold transition-all duration-150 group",
                      active
                        ? cn(item.activeBg, "text-white shadow-md shadow-indigo-500/25 font-bold scale-[1.01]")
                        : "text-slate-300 hover:bg-white/5 hover:text-white",
                      collapsed && "justify-center px-2"
                    )}
                    title={collapsed ? item.name : undefined}
                  >
                    <Icon className={cn("h-4 w-4 shrink-0 transition-transform group-hover:scale-110", active ? "text-white" : item.iconColor)} />
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
        <div className="p-3 border-t border-white/10 bg-gradient-to-b from-transparent to-blue-950/40">
          <div className="rounded-xl p-3 bg-gradient-to-r from-blue-900/40 via-indigo-900/40 to-purple-900/40 border border-blue-500/30 shadow-lg text-xs space-y-1.5">
            <div className="flex items-center justify-between text-[10px] font-bold tracking-wider text-cyan-400">
              <span>ACTIVE RESEARCH BENCHMARK</span>
              <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400 animate-pulse" />
            </div>
            <p className="font-bold text-white truncate" title="Sentinel-1 SAR Change Detection">
              Sentinel-1 SAR Change Detection
            </p>
            <div className="flex items-center gap-2 text-[10px]">
              <span className="px-1.5 py-0.5 rounded-md bg-blue-500/20 text-blue-300 font-medium border border-blue-500/30">IEEE J-STARS</span>
              <span className="px-1.5 py-0.5 rounded-md bg-emerald-500/20 text-emerald-300 font-medium border border-emerald-500/30">80/20 Split</span>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
