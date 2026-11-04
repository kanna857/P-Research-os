"""
Unified Research Crawling Pipeline & Autonomous Crawling Agent Manager.
Orchestrates Scrapy, Crawl4AI, and Trafilatura with academic discovery APIs
(OpenAlex, Crossref, Unpaywall, arXiv).
"""

from typing import Dict, Any, List, Optional
import asyncio
import uuid
from datetime import datetime, timezone
import logging

from app.integrations.web_crawling.scrapy_adapter import scrapy_adapter
from app.integrations.web_crawling.crawl4ai_adapter import crawl4ai_adapter
from app.integrations.web_crawling.trafilatura_adapter import trafilatura_adapter
from app.integrations.web_crawling.content_extractor import content_extractor
from app.integrations.web_crawling.deduplication import deduplication_engine
from app.integrations.web_crawling.source_provenance import provenance_tracker
from app.integrations.research.openalex_client import openalex_client

logger = logging.getLogger(__name__)


class CrawlJob:
    """Represents an active or historical crawling job."""

    def __init__(self, job_id: str, topic: str, tool: str, seed_urls: List[str], project_id: int = 1):
        self.job_id = job_id
        self.topic = topic
        self.tool = tool
        self.seed_urls = seed_urls
        self.project_id = project_id
        self.status = "QUEUED"  # QUEUED, RUNNING, COMPLETED, FAILED
        self.pages_crawled = 0
        self.papers_discovered = 0
        self.datasets_discovered = 0
        self.failed_requests = 0
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.completed_at: Optional[str] = None
        self.results: List[Dict[str, Any]] = []
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "topic": self.topic,
            "tool": self.tool,
            "seed_urls": self.seed_urls,
            "project_id": self.project_id,
            "status": self.status,
            "pages_crawled": self.pages_crawled,
            "papers_discovered": self.papers_discovered,
            "datasets_discovered": self.datasets_discovered,
            "failed_requests": self.failed_requests,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "results_count": len(self.results),
        }


class CrawlManager:
    """Unified Orchestrator for academic web crawling and evidence synthesis."""

    def __init__(self):
        self._jobs: Dict[str, CrawlJob] = {}
        self._evidence_database: List[Dict[str, Any]] = []
        self._page_cache: Dict[str, Dict[str, Any]] = {}  # canonical_url -> cached_result

    # ──────────────────────── Job Management ────────────────────────
    def create_job(self, topic: str, tool: str = "auto", seed_urls: Optional[List[str]] = None, project_id: int = 1) -> CrawlJob:
        job_id = f"job_{uuid.uuid4().hex[:10]}"
        job = CrawlJob(
            job_id=job_id,
            topic=topic,
            tool=tool,
            seed_urls=seed_urls or [],
            project_id=project_id,
        )
        self._jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        job = self._jobs.get(job_id)
        if not job:
            return None
        res = job.to_dict()
        res["results"] = job.results[:20]  # include preview of recent results
        return res

    def list_jobs(self, limit: int = 30) -> List[Dict[str, Any]]:
        jobs = sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)
        return [j.to_dict() for j in jobs[:limit]]

    # ──────────────────────── Autonomous Crawling Agent ────────────────────────
    async def run_autonomous_agent(
        self,
        topic: str,
        project_id: int = 1,
        max_pages: int = 10,
        preferred_tool: str = "auto",
    ) -> Dict[str, Any]:
        """
        Autonomous Research Crawling Agent:
        1. Generates targeted scholarly search queries from research topic
        2. Discovers relevant public academic pages & open-access repositories via OpenAlex
        3. Dynamically selects optimal crawling tool (Scrapy, Crawl4AI, Trafilatura)
        4. Extracts clean structured content, research methods, and benchmark metrics
        5. Identifies PDF download links and open dataset repositories
        6. Deduplicates across canonical URLs and content hashes
        7. Saves immutable source provenance records
        8. Feeds verified evidence to the ResearchOS evidence database
        """
        job = self.create_job(topic=topic, tool=preferred_tool, project_id=project_id)
        job.status = "RUNNING"

        try:
            # Step 1: Discover seed URLs from academic discovery API
            discovery_res = await openalex_client.search_works(query=topic, per_page=min(max_pages, 10))
            discovered_papers = discovery_res.get("papers", [])

            seed_urls: List[str] = []
            for p in discovered_papers:
                if p.get("pdf_url"):
                    seed_urls.append(p["pdf_url"])
                elif p.get("doi"):
                    seed_urls.append(p["doi"] if p["doi"].startswith("http") else f"https://doi.org/{p['doi']}")

            # Add general scholarly search URLs for preprint/dataset portals
            clean_topic = topic.replace(" ", "+")
            seed_urls.append(f"https://arxiv.org/search/?query={clean_topic}&searchtype=all")
            seed_urls.append(f"https://zenodo.org/search?q={clean_topic}")

            job.seed_urls = seed_urls[:max_pages]

            # Step 2: Crawl and extract from each seed URL
            for url in seed_urls[:max_pages]:
                try:
                    result = await self.crawl_and_extract(
                        url=url,
                        project_id=project_id,
                        tool=preferred_tool,
                    )
                    job.results.append(result)

                    if result.get("status") == "success":
                        job.pages_crawled += 1
                        assets = result.get("scholarly_assets", {})
                        if assets.get("has_open_pdf"):
                            job.papers_discovered += 1
                        if assets.get("has_datasets"):
                            job.datasets_discovered += 1

                        # Store in global evidence database
                        self._evidence_database.append(result)
                    else:
                        job.failed_requests += 1
                except Exception as e:
                    job.failed_requests += 1
                    logger.warning(f"Error crawling {url}: {e}")

            job.status = "COMPLETED"
            job.completed_at = datetime.now(timezone.utc).isoformat()

            return {
                "job": job.to_dict(),
                "topic": topic,
                "summary": {
                    "total_pages_crawled": job.pages_crawled,
                    "papers_discovered": job.papers_discovered,
                    "datasets_discovered": job.datasets_discovered,
                    "failed_requests": job.failed_requests,
                    "evidence_items_stored": len(job.results),
                },
                "results": job.results,
            }
        except Exception as e:
            job.status = "FAILED"
            job.error = str(e)
            job.completed_at = datetime.now(timezone.utc).isoformat()
            return {"job": job.to_dict(), "error": str(e)}

    # ──────────────────────── Single URL Crawl & Extract ────────────────────────
    async def crawl_and_extract(
        self,
        url: str,
        project_id: int = 1,
        tool: str = "auto",
    ) -> Dict[str, Any]:
        """
        Orchestrates responsible crawl, deduplication, tool execution, and asset extraction.
        """
        canonical_url = deduplication_engine.normalize_url(url)

        # Check in-memory page cache first to avoid repeat requests
        if canonical_url in self._page_cache:
            cached = self._page_cache[canonical_url]
            return {**cached, "cached": True}

        # Step A: Perform polite fetch via Scrapy adapter (enforces robots.txt and domain rate limits)
        crawl_resp = await scrapy_adapter.crawl_url(canonical_url, project_id=project_id)

        if crawl_resp.get("status") != "success":
            return {
                "url": url,
                "canonical_url": canonical_url,
                "status": crawl_resp.get("status", "failed"),
                "error": crawl_resp.get("error", "Failed to retrieve page"),
                "tool_used": "ScrapyCrawler",
                "robots_compliant": crawl_resp.get("robots_compliant", False),
            }

        html = crawl_resp.get("html", "")

        # Step B: Select tool or execute multi-tool extraction
        # Determine optimal tool if 'auto'
        chosen_tool = tool
        if tool == "auto":
            # If preprint or article landing page -> Trafilatura
            # If complex modern site or rich methods -> Crawl4AI
            if any(k in canonical_url for k in ["arxiv.org", "doi.org", "nature.com", "sciencedirect.com"]):
                chosen_tool = "trafilatura"
            else:
                chosen_tool = "crawl4ai"

        extraction_result = {}
        if chosen_tool in ("trafilatura", "all"):
            extraction_result["trafilatura"] = await trafilatura_adapter.extract_from_html(
                html_content=html,
                url=canonical_url,
                project_id=project_id,
                status_code=crawl_resp.get("status_code", 200),
                robots_compliant=True,
            )

        if chosen_tool in ("crawl4ai", "all") or not extraction_result.get("trafilatura", {}).get("text"):
            extraction_result["crawl4ai"] = await crawl4ai_adapter.crawl_and_structure(
                html_content=html,
                url=canonical_url,
                project_id=project_id,
                status_code=crawl_resp.get("status_code", 200),
                robots_compliant=True,
            )

        # Step C: Content Extractor for scholarly assets (PDFs, datasets, benchmarks, claims)
        clean_text = ""
        if "trafilatura" in extraction_result:
            clean_text = extraction_result["trafilatura"].get("text", "")
        elif "crawl4ai" in extraction_result:
            clean_text = extraction_result["crawl4ai"].get("markdown", "")

        assets = content_extractor.extract_scholarly_assets(
            html=html,
            text=clean_text,
            url=canonical_url,
        )

        title = (
            extraction_result.get("trafilatura", {}).get("title")
            or extraction_result.get("crawl4ai", {}).get("title")
            or assets.get("doi")
            or url
        )

        evidence_entry = {
            "url": url,
            "canonical_url": canonical_url,
            "final_url": crawl_resp.get("final_url", canonical_url),
            "status": "success",
            "title": title,
            "tool_used": chosen_tool,
            "evidence_id": crawl_resp.get("evidence_id"),
            "robots_compliant": True,
            "is_paywalled": crawl_resp.get("is_paywalled", False),
            "is_duplicate": crawl_resp.get("is_duplicate", False),
            "scholarly_assets": assets,
            "text_preview": clean_text[:600] + ("..." if len(clean_text) > 600 else ""),
            "markdown": extraction_result.get("crawl4ai", {}).get("markdown"),
            "word_count": len(clean_text.split()),
            "discovered_links_count": len(crawl_resp.get("discovered_links", [])),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
        }

        # Cache in memory
        self._page_cache[canonical_url] = evidence_entry
        return evidence_entry

    def get_evidence_database(self, project_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Return collected evidence items with provenance."""
        evidence = self._evidence_database
        if project_id is not None:
            evidence = [e for e in evidence if e.get("project_id", 1) == project_id]
        return evidence[-limit:]

    def get_crawler_stats(self) -> Dict[str, Any]:
        """Overview statistics across all jobs and cache."""
        total_pages = sum(j.pages_crawled for j in self._jobs.values())
        total_papers = sum(j.papers_discovered for j in self._jobs.values())
        total_datasets = sum(j.datasets_discovered for j in self._jobs.values())
        total_failed = sum(j.failed_requests for j in self._jobs.values())
        dedup_stats = deduplication_engine.get_stats()

        return {
            "total_jobs": len(self._jobs),
            "pages_crawled": total_pages,
            "papers_discovered": total_papers,
            "datasets_discovered": total_datasets,
            "failed_requests": total_failed,
            "cached_pages": len(self._page_cache),
            "unique_urls_indexed": dedup_stats["unique_urls_indexed"],
            "unique_content_hashes": dedup_stats["unique_content_hashes"],
            "provenance_records": len(provenance_tracker.list_records(limit=1000)),
        }


crawl_manager = CrawlManager()
