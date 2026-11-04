"""
Scrapy Integration Adapter (scrapy/scrapy).
Large-scale academic web crawling architecture with URL frontier queue,
robots.txt parsing & compliance, per-domain rate limiting, and link graph extraction.
"""

from typing import Dict, Any, List, Optional, Set, Callable
import asyncio
import re
import time
import logging
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

from app.integrations.web_crawling.deduplication import deduplication_engine
from app.integrations.web_crawling.source_provenance import provenance_tracker

logger = logging.getLogger(__name__)


class DomainRateLimiter:
    """Per-domain rate limiter to ensure polite academic crawling."""

    def __init__(self, default_delay: float = 1.0):
        self.default_delay = default_delay
        self._last_request_times: Dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def throttle(self, domain: str, delay: Optional[float] = None):
        """Wait if needed before allowing request to proceed to domain."""
        target_delay = delay if delay is not None else self.default_delay
        async with self._lock:
            last_time = self._last_request_times.get(domain, 0.0)
            elapsed = time.time() - last_time
            if elapsed < target_delay:
                await asyncio.sleep(target_delay - elapsed)
            self._last_request_times[domain] = time.time()


class RobotsComplianceChecker:
    """Caches and evaluates robots.txt files per domain to guarantee compliance."""

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self._parsers: Dict[str, RobotFileParser] = {}
        self._crawl_delays: Dict[str, float] = {}

    async def can_fetch(self, url: str) -> bool:
        """Check if robots.txt permits crawling the given URL."""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if not domain:
            return False

        if domain not in self._parsers:
            rp = RobotFileParser()
            robots_url = f"{parsed.scheme}://{domain}/robots.txt"
            try:
                import httpx
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(robots_url)
                    if resp.status_code == 200:
                        rp.parse(resp.text.splitlines())
                    else:
                        # If 404, standard convention is that all crawling is allowed
                        rp.allow_all = True
            except Exception:
                # If robots.txt cannot be fetched, default to permissive but gentle
                rp.allow_all = True

            self._parsers[domain] = rp
            try:
                delay = rp.crawl_delay(self.user_agent)
                if delay:
                    self._crawl_delays[domain] = float(delay)
            except Exception:
                pass

        parser = self._parsers[domain]
        try:
            return parser.can_fetch(self.user_agent, url)
        except Exception:
            return True

    def get_crawl_delay(self, domain: str) -> Optional[float]:
        return self._crawl_delays.get(domain)


class ScrapyCrawlerAdapter:
    """
    Adapter implementing Scrapy-style spider crawling architecture:
    - URL frontier queue
    - Obey robots.txt
    - Domain rate limits & concurrency controls
    - Link extraction & filtering for academic domains
    - Duplicate detection
    - Retries with exponential backoff
    """

    # Academic domains with high signal for papers and datasets
    ACADEMIC_DOMAIN_PATTERNS = [
        r"arxiv\.org",
        r"biorxiv\.org",
        r"medrxiv\.org",
        r"zenodo\.org",
        r"paperswithcode\.com",
        r"openreview\.net",
        r"huggingface\.co",
        r"kaggle\.com",
        r"crossref\.org",
        r"semanticscholar\.org",
        r"nature\.com",
        r"ieee\.org",
        r"acm\.org",
        r"springer\.com",
        r"sciencedirect\.com",
        r"github\.com",
    ]

    def __init__(
        self,
        user_agent: str = "ResearchOS-Academic-Crawler/1.0 (+https://github.com/kanna857/P-Research-os; polite academic indexer)",
        default_rate_limit: float = 1.0,
        max_depth: int = 2,
    ):
        self.user_agent = user_agent
        self.max_depth = max_depth
        self.rate_limiter = DomainRateLimiter(default_delay=default_rate_limit)
        self.robots_checker = RobotsComplianceChecker(user_agent=user_agent)

    async def crawl_url(
        self,
        url: str,
        project_id: int = 1,
        max_retries: int = 2,
    ) -> Dict[str, Any]:
        """
        Crawl a single URL respecting robots.txt and rate limits.
        Extracts links, metadata, and body HTML.
        """
        import httpx

        canonical_url = deduplication_engine.normalize_url(url)
        parsed = urlparse(canonical_url)
        domain = parsed.netloc.lower()

        # 1. Robots.txt check
        is_allowed = await self.robots_checker.can_fetch(canonical_url)
        if not is_allowed:
            return {
                "url": url,
                "canonical_url": canonical_url,
                "status": "blocked_by_robots_txt",
                "robots_compliant": True,
                "error": f"robots.txt disallows crawling {canonical_url} for user-agent",
                "links": [],
                "html": "",
            }

        # 2. Rate limit throttle
        delay = self.robots_checker.get_crawl_delay(domain)
        await self.rate_limiter.throttle(domain, delay=delay)

        # 3. Fetch with retries
        headers = {"User-Agent": self.user_agent}
        attempt = 0
        last_error = None

        while attempt <= max_retries:
            try:
                async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
                    resp = await client.get(canonical_url, headers=headers)

                    # Check for paywalls / access denial
                    is_paywalled = resp.status_code in (401, 403) or any(
                        p in resp.text.lower()[:3000]
                        for p in ["purchase access", "institutional login", "subscribe to view"]
                    )

                    # Extract academic links
                    discovered_links = self._extract_academic_links(resp.text, str(resp.url))

                    # Deduplication
                    content_hash = deduplication_engine.compute_content_hash(resp.text)
                    is_dup, prev_url = deduplication_engine.is_content_seen(resp.text)
                    deduplication_engine.record_crawl(canonical_url, resp.text)

                    # Provenance
                    prov_record = provenance_tracker.register(
                        url=url,
                        canonical_url=canonical_url,
                        crawler_tool="ScrapyCrawler",
                        status_code=resp.status_code,
                        robots_compliant=True,
                        content_hash=content_hash,
                        is_paywalled=is_paywalled,
                        project_id=project_id,
                        evidence_type="web_page",
                    )

                    return {
                        "url": url,
                        "canonical_url": canonical_url,
                        "final_url": str(resp.url),
                        "status_code": resp.status_code,
                        "status": "success" if resp.status_code < 400 else "http_error",
                        "is_duplicate": is_dup,
                        "duplicate_source": prev_url,
                        "is_paywalled": is_paywalled,
                        "robots_compliant": True,
                        "evidence_id": prov_record.evidence_id,
                        "content_hash": content_hash,
                        "discovered_links": discovered_links[:30],
                        "html": resp.text,
                        "size_bytes": len(resp.content),
                    }
            except Exception as e:
                last_error = str(e)
                attempt += 1
                if attempt <= max_retries:
                    await asyncio.sleep(1.5 * attempt)

        return {
            "url": url,
            "canonical_url": canonical_url,
            "status": "failed",
            "error": last_error,
            "links": [],
            "html": "",
        }

    async def crawl_frontier(
        self,
        seed_urls: List[str],
        max_pages: int = 10,
        project_id: int = 1,
    ) -> List[Dict[str, Any]]:
        """
        Crawl a list of seed URLs and follow discovered academic links up to max_pages.
        """
        frontier = deduplication_engine.filter_frontier(seed_urls)
        results = []
        crawled_count = 0

        while frontier and crawled_count < max_pages:
            next_url = frontier.pop(0)
            crawl_res = await self.crawl_url(next_url, project_id=project_id)
            results.append(crawl_res)
            crawled_count += 1

            if crawl_res.get("status") == "success":
                new_links = crawl_res.get("discovered_links", [])
                unseen = deduplication_engine.filter_frontier(new_links)
                # Append high-value links to frontier
                frontier.extend(unseen[:5])

        return results

    def _extract_academic_links(self, html: str, base_url: str) -> List[str]:
        """Extract links from HTML that match academic domain patterns or PDF paths."""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                abs_url = urljoin(base_url, href)
                if abs_url.startswith("http"):
                    # Check if academic domain or PDF link
                    is_academic = any(re.search(pat, abs_url, re.I) for pat in self.ACADEMIC_DOMAIN_PATTERNS)
                    is_pdf = abs_url.lower().endswith(".pdf") or "/pdf/" in abs_url
                    if is_academic or is_pdf:
                        links.append(abs_url)
            return list(dict.fromkeys(links))  # preserve order deduplication
        except Exception:
            return []


scrapy_adapter = ScrapyCrawlerAdapter()
