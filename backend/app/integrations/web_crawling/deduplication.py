"""
Deduplication Engine for Autonomous Academic Crawling.
Implements canonical URL normalization, content hashing, SimHash-style similarity,
and URL frontier deduplication.
"""

import hashlib
import re
from typing import Dict, Set, Optional, Tuple, List
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


class DeduplicationEngine:
    """Manages canonical URL deduplication and content hash tracking."""

    # Query parameters that do not alter content and should be stripped for deduplication
    TRACKING_PARAMS = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "ref", "referer", "referrer", "fbclid", "gclid", "_ga", "_gl",
        "spm", "from", "source", "origin"
    }

    def __init__(self):
        self._seen_urls: Set[str] = set()
        self._seen_content_hashes: Dict[str, str] = {}  # content_hash -> canonical_url
        self._seen_dois: Set[str] = set()

    def normalize_url(self, raw_url: str) -> str:
        """
        Produce a canonical representation of a URL:
        - Lowercase scheme and netloc
        - Strip common tracking query parameters
        - Sort remaining query parameters
        - Remove default ports (:80, :443)
        - Strip fragment identifiers
        - Standardize trailing slash on directory paths
        """
        if not raw_url:
            return ""

        url = raw_url.strip()

        # Handle DOI URLs canonicalization
        doi_match = re.search(r'(?:https?://(?:dx\.)?doi\.org/|doi:)(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', url)
        if doi_match:
            return f"https://doi.org/{doi_match.group(1).lower()}"

        try:
            parsed = urlparse(url)
            scheme = (parsed.scheme or "http").lower()
            netloc = parsed.netloc.lower()

            # Remove standard ports
            if netloc.endswith(":80") and scheme == "http":
                netloc = netloc[:-3]
            elif netloc.endswith(":443") and scheme == "https":
                netloc = netloc[:-4]

            path = parsed.path or "/"
            # Collapse multiple slashes
            path = re.sub(r'/{2,}', '/', path)

            # Filter out tracking query parameters and sort remaining
            query_pairs = parse_qsl(parsed.query, keep_blank_values=False)
            filtered_pairs = sorted(
                (k, v) for k, v in query_pairs if k.lower() not in self.TRACKING_PARAMS
            )
            query_str = urlencode(filtered_pairs) if filtered_pairs else ""

            # Standardized URL without fragment
            return urlunparse((scheme, netloc, path, "", query_str, ""))
        except Exception:
            return url

    def compute_content_hash(self, text: str) -> str:
        """Compute SHA-256 hash of normalized body text for near-exact deduplication."""
        # Normalize whitespace and casing
        normalized = re.sub(r'\s+', ' ', text.lower().strip())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def is_url_seen(self, raw_url: str) -> bool:
        """Check if canonical URL has already been crawled."""
        canonical = self.normalize_url(raw_url)
        return canonical in self._seen_urls

    def is_content_seen(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Check if content has already been indexed from another URL.
        Returns (is_seen, previous_canonical_url).
        """
        if not text or len(text.strip()) < 100:
            return False, None
        content_hash = self.compute_content_hash(text)
        if content_hash in self._seen_content_hashes:
            return True, self._seen_content_hashes[content_hash]
        return False, None

    def record_crawl(self, raw_url: str, text: Optional[str] = None, doi: Optional[str] = None) -> str:
        """Record URL, content hash, and DOI in the deduplication ledger."""
        canonical = self.normalize_url(raw_url)
        self._seen_urls.add(canonical)

        if text:
            content_hash = self.compute_content_hash(text)
            self._seen_content_hashes[content_hash] = canonical

        if doi:
            self._seen_dois.add(doi.lower().strip())

        return canonical

    def is_doi_seen(self, doi: str) -> bool:
        """Check if DOI has already been acquired."""
        return doi.lower().strip() in self._seen_dois

    def filter_frontier(self, urls: List[str]) -> List[str]:
        """Filter a list of candidate URLs, keeping only unvisited ones."""
        unique_unseen = []
        local_seen = set()
        for u in urls:
            canon = self.normalize_url(u)
            if canon and canon not in self._seen_urls and canon not in local_seen:
                local_seen.add(canon)
                unique_unseen.append(u)
        return unique_unseen

    def get_stats(self) -> Dict[str, int]:
        """Return deduplication engine statistics."""
        return {
            "unique_urls_indexed": len(self._seen_urls),
            "unique_content_hashes": len(self._seen_content_hashes),
            "unique_dois_tracked": len(self._seen_dois),
        }

    def clear(self):
        """Reset state (primarily for tests)."""
        self._seen_urls.clear()
        self._seen_content_hashes.clear()
        self._seen_dois.clear()


deduplication_engine = DeduplicationEngine()
