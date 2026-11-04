"""
Trafilatura Integration Adapter (adbar/trafilatura).
Extracts main article text, removes navigation and advertisement clutter,
extracts author and publication dates, and preserves provenance.
"""

from typing import Dict, Any, Optional
import logging
import re
from urllib.parse import urlparse

from app.integrations.web_crawling.deduplication import deduplication_engine
from app.integrations.web_crawling.source_provenance import provenance_tracker

logger = logging.getLogger(__name__)


class TrafilaturaAdapter:
    """Adapter for Trafilatura article content extraction engine."""

    def __init__(self):
        self._trafilatura_available = None

    def _check_library(self) -> bool:
        if self._trafilatura_available is None:
            try:
                import trafilatura
                self._trafilatura_available = True
            except ImportError:
                self._trafilatura_available = False
        return self._trafilatura_available

    async def extract_from_html(
        self,
        html_content: str,
        url: str,
        project_id: int = 1,
        status_code: int = 200,
        robots_compliant: bool = True,
    ) -> Dict[str, Any]:
        """
        Extract clean article body text and metadata from HTML content using Trafilatura.
        """
        canonical_url = deduplication_engine.normalize_url(url)

        if not html_content or not html_content.strip():
            return {
                "url": url,
                "canonical_url": canonical_url,
                "tool": "Trafilatura",
                "status": "error",
                "error": "Empty HTML content",
                "text": "",
                "metadata": {},
            }

        text = ""
        meta_dict = {}

        if self._check_library():
            try:
                import trafilatura

                # Extract main text
                extracted_text = trafilatura.extract(
                    html_content,
                    url=canonical_url,
                    include_links=True,
                    include_images=False,
                    include_tables=True,
                    include_comments=False,
                    output_format="txt",
                    with_metadata=True,
                )
                text = extracted_text or ""

                # Extract rich metadata
                metadata = trafilatura.extract_metadata(html_content, default_url=canonical_url)
                if metadata:
                    meta_dict = {
                        "title": metadata.title,
                        "author": metadata.author,
                        "date": metadata.date,
                        "sitename": metadata.sitename,
                        "description": metadata.description,
                        "categories": metadata.categories,
                        "tags": metadata.tags,
                        "license": metadata.license,
                    }
            except Exception as e:
                logger.warning(f"Trafilatura native extraction failed, falling back: {e}")
                text = self._heuristic_fallback_extract(html_content)
        else:
            text = self._heuristic_fallback_extract(html_content)

        # Fallback title if not in metadata
        if not meta_dict.get("title"):
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
            if title_match:
                meta_dict["title"] = re.sub(r"\s+", " ", title_match.group(1)).strip()

        # Deduplication check
        is_dup, prev_url = deduplication_engine.is_content_seen(text)
        content_hash = deduplication_engine.compute_content_hash(text)
        deduplication_engine.record_crawl(canonical_url, text)

        # Paywall indicator check
        is_paywalled = self._detect_paywall(html_content, text)

        # Register provenance
        prov_record = provenance_tracker.register(
            url=url,
            canonical_url=canonical_url,
            crawler_tool="Trafilatura",
            status_code=status_code,
            robots_compliant=robots_compliant,
            content_hash=content_hash,
            title=meta_dict.get("title"),
            author=meta_dict.get("author"),
            publication_date=meta_dict.get("date"),
            is_paywalled=is_paywalled,
            license_info=meta_dict.get("license"),
            project_id=project_id,
            evidence_type="article_full_text",
        )

        return {
            "url": url,
            "canonical_url": canonical_url,
            "tool": "Trafilatura (adbar/trafilatura)",
            "status": "success",
            "is_duplicate": is_dup,
            "duplicate_source": prev_url,
            "is_paywalled": is_paywalled,
            "evidence_id": prov_record.evidence_id,
            "title": meta_dict.get("title") or "Untitled Document",
            "author": meta_dict.get("author"),
            "date": meta_dict.get("date"),
            "sitename": meta_dict.get("sitename") or urlparse(canonical_url).netloc,
            "text": text,
            "word_count": len(text.split()),
            "character_count": len(text),
            "content_hash": content_hash,
            "metadata": meta_dict,
        }

    async def fetch_and_extract(
        self,
        url: str,
        project_id: int = 1,
        timeout: float = 20.0,
        user_agent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch URL over HTTP and extract clean text with Trafilatura."""
        import httpx

        headers = {
            "User-Agent": user_agent or "ResearchOS-Academic-Crawler/1.0 (+https://github.com/kanna857/P-Research-os; polite academic indexer)"
        }

        try:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                return await self.extract_from_html(
                    html_content=resp.text,
                    url=str(resp.url),
                    project_id=project_id,
                    status_code=resp.status_code,
                    robots_compliant=True,
                )
        except Exception as e:
            return {
                "url": url,
                "canonical_url": deduplication_engine.normalize_url(url),
                "tool": "Trafilatura",
                "status": "error",
                "error": str(e),
                "text": "",
                "metadata": {},
            }

    def _heuristic_fallback_extract(self, html: str) -> str:
        """Lightweight DOM parsing fallback when trafilatura binary not loaded."""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Remove scripts, styles, nav, headers, footers
            for elem in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "svg"]):
                elem.extract()
            # Prefer article, main, or body
            main_elem = soup.find("article") or soup.find("main") or soup.find("div", {"id": re.compile(r"content|main|article", re.I)}) or soup.body
            if main_elem:
                return re.sub(r"\n\s*\n", "\n\n", main_elem.get_text(separator="\n")).strip()
            return re.sub(r"\n\s*\n", "\n\n", soup.get_text(separator="\n")).strip()
        except Exception:
            clean = re.sub(r"<[^>]+>", " ", html)
            return re.sub(r"\s+", " ", clean).strip()

    def _detect_paywall(self, html: str, text: str) -> bool:
        """Detect paywall, login gates, and subscription restrictions without attempting bypass."""
        keywords = [
            "access through your institution",
            "purchase access",
            "subscribe to view",
            "institutional login",
            "rent or buy article",
            "buy this article",
            "full text is available to subscribers",
            "view subscription options",
            "sign in to download",
        ]
        sample = (html[:3000] + " " + text[:2000]).lower()
        return any(k in sample for k in keywords)


trafilatura_adapter = TrafilaturaAdapter()
