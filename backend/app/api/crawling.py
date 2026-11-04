"""
Autonomous Web Scraping & Research Crawling API Routes.
Integrates:
- Scrapy (scrapy/scrapy) — Large-scale academic crawling & link following
- Crawl4AI (unclecode/crawl4ai) — AI-ready Markdown & structured semantic extraction
- Trafilatura (adbar/trafilatura) — Main article text and metadata extraction
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, status

from app.integrations.web_crawling.crawl_manager import crawl_manager
from app.integrations.web_crawling.trafilatura_adapter import trafilatura_adapter
from app.integrations.web_crawling.crawl4ai_adapter import crawl4ai_adapter
from app.integrations.web_crawling.scrapy_adapter import scrapy_adapter
from app.integrations.web_crawling.source_provenance import provenance_tracker
from app.integrations.web_crawling.deduplication import deduplication_engine

router = APIRouter()


@router.post("/autonomous-agent")
async def run_autonomous_crawling_agent(data: Dict[str, Any]):
    """
    Run Autonomous Research Crawling Agent:
    Takes a research topic -> Discovers scholarly URLs via APIs ->
    Politely crawls with robots.txt compliance & rate limiting ->
    Extracts text with Trafilatura and structured Markdown with Crawl4AI ->
    Deduplicates and stores verified evidence with source provenance.
    """
    topic = data.get("topic", "")
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Research topic cannot be empty")

    project_id = int(data.get("project_id", 1))
    max_pages = int(data.get("max_pages", 8))
    tool = data.get("tool", "auto")

    result = await crawl_manager.run_autonomous_agent(
        topic=topic.strip(),
        project_id=project_id,
        max_pages=max_pages,
        preferred_tool=tool,
    )
    return result


@router.post("/crawl")
async def crawl_url_endpoint(data: Dict[str, Any]):
    """
    Crawl and extract a single academic URL or paper landing page.
    Automatically verifies robots.txt, respects rate limits, and extracts evidence.
    """
    url = data.get("url", "")
    if not url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    tool = data.get("tool", "auto")
    project_id = int(data.get("project_id", 1))

    return await crawl_manager.crawl_and_extract(
        url=url.strip(),
        project_id=project_id,
        tool=tool,
    )


@router.post("/extract")
async def extract_content_endpoint(data: Dict[str, Any]):
    """
    Extract article text using Trafilatura or Crawl4AI from raw HTML or direct URL.
    """
    html = data.get("html", "")
    url = data.get("url", "https://academic.example.org/article")
    tool = data.get("tool", "trafilatura")
    project_id = int(data.get("project_id", 1))

    if html:
        if tool == "crawl4ai":
            return await crawl4ai_adapter.crawl_and_structure(html, url, project_id=project_id)
        else:
            return await trafilatura_adapter.extract_from_html(html, url, project_id=project_id)
    elif url:
        return await crawl_manager.crawl_and_extract(url, project_id=project_id, tool=tool)
    else:
        raise HTTPException(status_code=400, detail="Either 'html' or 'url' must be provided")


@router.get("/jobs")
async def list_crawl_jobs(limit: int = Query(default=30, ge=1, le=100)):
    """List recent and active crawl jobs."""
    return crawl_manager.list_jobs(limit=limit)


@router.get("/jobs/{job_id}")
async def get_crawl_job(job_id: str):
    """Get status and details of a specific crawl job."""
    job = crawl_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/evidence")
async def get_crawled_evidence(
    project_id: Optional[int] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """Retrieve collected scholarly evidence with provenance metadata."""
    return crawl_manager.get_evidence_database(project_id=project_id, limit=limit)


@router.get("/provenance/{evidence_id}")
async def get_provenance_record(evidence_id: str):
    """Retrieve immutable source provenance badge and verification details."""
    badge = provenance_tracker.get_provenance_badge(evidence_id)
    if not badge.get("verified"):
        raise HTTPException(status_code=404, detail="Evidence provenance record not found")
    record = provenance_tracker.get_by_id(evidence_id)
    return {"badge": badge, "record": record}


@router.get("/stats")
async def get_crawler_statistics():
    """Retrieve real-time crawling metrics, robots.txt compliance, and cache status."""
    return crawl_manager.get_crawler_stats()
