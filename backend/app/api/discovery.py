"""
Free-First Autonomous Research Paper & Dataset Discovery API Routes.
Enables unified multi-source discovery, legal PDF resolution, paper-to-dataset linking,
and polite resumable downloading without paid API subscriptions.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.integrations.discovery.autonomous_discovery import autonomous_discovery_engine
from app.integrations.discovery.papers_federated import papers_federated_discovery
from app.integrations.discovery.datasets_federated import datasets_federated_discovery
from app.integrations.discovery.paper_dataset_linker import paper_dataset_linker
from app.integrations.discovery.free_api_manager import free_api_manager
from app.integrations.discovery.download_manager import download_manager

router = APIRouter()


@router.post("/start")
async def start_autonomous_discovery(data: Dict[str, Any]):
    """
    Start Autonomous Topic-to-Research Discovery:
    User inputs research topic -> Expands technical keywords ->
    Searches 10 free academic repositories -> Resolves open-access PDFs ->
    Searches 10 free dataset hubs -> Links papers to datasets ->
    Evaluates training suitability -> Hands off to downstream agents.
    """
    topic = data.get("topic", "")
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Research topic cannot be empty")

    project_id = int(data.get("project_id", 1))
    max_papers = int(data.get("max_papers_per_source", 4))
    max_datasets = int(data.get("max_datasets_per_source", 4))
    open_access_only = bool(data.get("open_access_only", False))

    return await autonomous_discovery_engine.execute_autonomous_discovery(
        topic=topic.strip(),
        project_id=project_id,
        max_papers_per_source=max_papers,
        max_datasets_per_source=max_datasets,
        open_access_only=open_access_only,
    )


@router.post("/papers")
async def federated_papers_search(data: Dict[str, Any]):
    """Search across 10 free academic paper repositories."""
    query = data.get("query", "")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    year_from = data.get("year_from")
    year_to = data.get("year_to")
    limit = int(data.get("limit_per_source", 5))
    oa_only = bool(data.get("open_access_only", False))

    return await papers_federated_discovery.search_all_repositories(
        query=query.strip(),
        year_from=year_from,
        year_to=year_to,
        limit_per_source=limit,
        open_access_only=oa_only,
    )


@router.post("/datasets")
async def federated_datasets_search(data: Dict[str, Any]):
    """Search across 10 free scientific dataset repositories."""
    query = data.get("query", "")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    limit = int(data.get("limit_per_source", 5))
    dataset_type = data.get("dataset_type")  # e.g. "labeled_only"

    return await datasets_federated_discovery.search_all_repositories(
        query=query.strip(),
        limit_per_source=limit,
        dataset_type=dataset_type,
    )


@router.post("/link-paper-datasets")
async def link_papers_to_datasets(data: Dict[str, Any]):
    """Run Paper-to-Dataset Linking Agent on a provided list of papers and datasets."""
    papers = data.get("papers", [])
    datasets = data.get("datasets", [])
    return await paper_dataset_linker.link_papers_and_datasets(
        papers=papers,
        available_datasets=datasets,
    )


@router.get("/apis")
async def list_free_api_providers(category: Optional[str] = Query(default=None)):
    """List all configured free API providers, authentication requirements, and statuses."""
    providers = free_api_manager.list_providers(category=category)
    policy = free_api_manager.get_policy_summary()
    return {"policy": policy, "providers": providers}


@router.post("/apis/{provider_id}/test")
async def test_provider_connection(provider_id: str):
    """Test connection and measure latency to a specific free academic provider."""
    return await free_api_manager.test_provider(provider_id)


@router.post("/download")
async def download_asset(data: Dict[str, Any]):
    """Politely download permitted paper PDF or open dataset archive with SHA-256 verification."""
    url = data.get("url", "")
    title = data.get("title", "Research Asset")
    asset_type = data.get("asset_type", "paper_pdf")
    project_id = int(data.get("project_id", 1))
    doi = data.get("doi")
    license_info = data.get("license")

    if not url.strip():
        raise HTTPException(status_code=400, detail="Download URL cannot be empty")

    return await download_manager.download_file(
        url=url.strip(),
        title=title,
        asset_type=asset_type,
        project_id=project_id,
        doi=doi,
        license=license_info,
    )


@router.get("/downloads")
async def list_downloads(project_id: Optional[int] = Query(default=None)):
    """Retrieve history and active queue of downloaded files with checksums."""
    return download_manager.list_downloads(project_id=project_id)


@router.get("/stats")
async def get_discovery_stats():
    """Retrieve discovery engine statistics and historical topics."""
    history = autonomous_discovery_engine.get_discovery_history(limit=5)
    policy = free_api_manager.get_policy_summary()
    downloads = download_manager.list_downloads()
    completed_downloads = len([d for d in downloads if d.get("status") == "completed"])

    return {
        "policy": policy,
        "total_downloads": len(downloads),
        "completed_downloads": completed_downloads,
        "recent_discovery_runs": history,
    }

