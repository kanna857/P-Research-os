"""
OpenAlex Integration (ourresearch/openalex-python).
Performs academic paper discovery, citation graph exploration, and author/venue metadata resolution.
"""

from typing import List, Dict, Any, Optional
import asyncio
import httpx
from app.config import get_settings

settings = get_settings()


class OpenAlexClient:
    """Client for OpenAlex API with pyalex fallback/direct REST integration."""

    BASE_URL = "https://api.openalex.org"

    def __init__(self):
        self.email = settings.OPENALEX_EMAIL
        self.headers = {"User-Agent": f"ResearchOS ({self.email or 'researchos@local.dev'})"}

    async def search_works(
        self,
        query: str,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        min_citations: int = 0,
        page: int = 1,
        per_page: int = 25,
    ) -> Dict[str, Any]:
        """Search works using OpenAlex API with filtering and pagination."""
        params: Dict[str, Any] = {
            "search": query,
            "page": page,
            "per_page": per_page,
            "sort": "relevance_score:desc",
        }

        filter_parts = []
        if year_from and year_to:
            filter_parts.append(f"publication_year:{year_from}-{year_to}")
        elif year_from:
            filter_parts.append(f"from_publication_date:{year_from}-01-01")
        elif year_to:
            filter_parts.append(f"to_publication_date:{year_to}-12-31")

        if min_citations > 0:
            filter_parts.append(f"cited_by_count:>{min_citations}")

        if filter_parts:
            params["filter"] = ",".join(filter_parts)

        if self.email:
            params["mailto"] = self.email

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.get(f"{self.BASE_URL}/works", params=params, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()

                results = []
                for item in data.get("results", []):
                    authors = []
                    for auth in item.get("authorships", []):
                        author_info = auth.get("author", {})
                        if author_info.get("display_name"):
                            authors.append(author_info.get("display_name"))

                    open_access = item.get("open_access", {})
                    primary_loc = item.get("primary_location") or {}
                    source = primary_loc.get("source") or {}

                    results.append({
                        "id": item.get("id"),
                        "doi": item.get("doi"),
                        "title": item.get("title") or "Untitled",
                        "authors": authors,
                        "year": item.get("publication_year"),
                        "venue": source.get("display_name") or "Academic Venue",
                        "citation_count": item.get("cited_by_count", 0),
                        "abstract": item.get("abstract") or self._reconstruct_abstract(item.get("abstract_inverted_index")),
                        "is_open_access": open_access.get("is_oa", False),
                        "pdf_url": open_access.get("oa_url") or primary_loc.get("pdf_url"),
                        "source": "OpenAlex",
                        "cited_by_count": item.get("cited_by_count", 0),
                        "referenced_works_count": len(item.get("referenced_works", [])),
                        "referenced_works": item.get("referenced_works", [])[:10],
                    })

                return {
                    "total": data.get("meta", {}).get("count", 0),
                    "page": page,
                    "per_page": per_page,
                    "papers": results,
                }
            except Exception as e:
                # Return empty or graceful response if API fails/offline
                return {
                    "total": 0,
                    "page": page,
                    "per_page": per_page,
                    "papers": [],
                    "error": str(e),
                }

    def _reconstruct_abstract(self, inverted_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
        if not inverted_index:
            return None
        try:
            words = []
            for word, positions in inverted_index.items():
                for pos in positions:
                    words.append((pos, word))
            words.sort(key=lambda x: x[0])
            return " ".join(w[1] for w in words)
        except Exception:
            return None


openalex_client = OpenAlexClient()
