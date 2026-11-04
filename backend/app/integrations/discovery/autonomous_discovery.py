"""
Autonomous Topic-to-Research Discovery Orchestrator.
Coordinates the entire free-first discovery lifecycle:
Topic Understanding -> Query Expansion -> Federated Paper Search ->
Legal PDF Resolution -> Federated Dataset Search -> Paper-to-Dataset Linking ->
Relevance Ranking -> Downstream Hand-off to Literature & Experimentation Agents.
"""

from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime, timezone
import logging

from app.integrations.discovery.query_expander import query_expander
from app.integrations.discovery.papers_federated import papers_federated_discovery
from app.integrations.discovery.datasets_federated import datasets_federated_discovery
from app.integrations.discovery.paper_dataset_linker import paper_dataset_linker
from app.integrations.discovery.free_api_manager import free_api_manager
from app.integrations.research.storm_planner import storm_planner
from app.integrations.research.langgraph_agent import langgraph_orchestrator

logger = logging.getLogger(__name__)


class AutonomousDiscoveryEngine:
    """End-to-end autonomous research discovery engine operating with free-first guarantees."""

    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    async def execute_autonomous_discovery(
        self,
        topic: str,
        project_id: int = 1,
        max_papers_per_source: int = 4,
        max_datasets_per_source: int = 4,
        open_access_only: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute full autonomous topic discovery workflow:
        Input: Research Topic
        Output: Verified papers with PDFs, candidate datasets, paper-dataset linkages,
                research gap synthesis, and downstream handoff packet.
        """
        start_time = datetime.now(timezone.utc)

        # ── Step 1: Query Expansion & Technical Term Decomposition ──
        expansion = query_expander.expand_topic(topic)
        primary_query = expansion["cleaned_topic"]

        # ── Step 2 & 3: Concurrent Federated Search (Papers & Datasets) ──
        papers_task = papers_federated_discovery.search_all_repositories(
            query=primary_query,
            limit_per_source=max_papers_per_source,
            open_access_only=open_access_only,
        )
        datasets_task = datasets_federated_discovery.search_all_repositories(
            query=primary_query,
            limit_per_source=max_datasets_per_source,
        )

        papers_res, datasets_res = await asyncio.gather(papers_task, datasets_task)

        papers = papers_res.get("papers", [])
        datasets = datasets_res.get("datasets", [])

        # ── Step 4: Paper-to-Dataset Linking Agent ──
        linkage_res = await paper_dataset_linker.link_papers_and_datasets(
            papers=papers,
            available_datasets=datasets,
        )

        # ── Step 5: Research Gap & Perspective Synthesis ──
        storm_perspectives = storm_planner.generate_perspectives(primary_query)

        # ── Step 6: Assemble Downstream Hand-off Packet ──
        # Identifies top verified labeled benchmark vs raw observation collection
        labeled_benchmarks = [d for d in datasets if d.get("is_labeled_benchmark")]
        raw_collections = [d for d in datasets if not d.get("is_labeled_benchmark")]

        recommended_training_dataset = (
            labeled_benchmarks[0] if labeled_benchmarks
            else (datasets[0] if datasets else None)
        )

        summary_metrics = {
            "total_papers_found": len(papers),
            "open_access_pdfs_available": len([p for p in papers if p.get("is_open_access") and p.get("pdf_url")]),
            "total_datasets_found": len(datasets),
            "labeled_benchmarks_count": len(labeled_benchmarks),
            "raw_imagery_collections_count": len(raw_collections),
            "paper_dataset_connections": linkage_res.get("total_connections", 0),
            "free_apis_utilized": len(papers_res.get("sources_searched", [])) + len(datasets_res.get("sources_searched", [])),
            "execution_duration_sec": round((datetime.now(timezone.utc) - start_time).total_seconds(), 2),
        }

        result = {
            "topic": topic,
            "project_id": project_id,
            "query_expansion": expansion,
            "summary": summary_metrics,
            "free_policy": free_api_manager.get_policy_summary(),
            "papers": papers[:20],
            "datasets": datasets[:20],
            "paper_dataset_connections": linkage_res.get("connections", []),
            "recommended_training_dataset": recommended_training_dataset,
            "storm_perspectives": storm_perspectives,
            "downstream_ready": {
                "literature_review_ready": len(papers) >= 3,
                "gap_analysis_ready": True,
                "training_pipeline_ready": bool(recommended_training_dataset),
                "manuscript_studio_ready": len(papers) >= 3,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self._history.append({
            "topic": topic,
            "timestamp": result["timestamp"],
            "summary": summary_metrics,
        })

        return result

    def get_discovery_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._history[-limit:]


autonomous_discovery_engine = AutonomousDiscoveryEngine()
