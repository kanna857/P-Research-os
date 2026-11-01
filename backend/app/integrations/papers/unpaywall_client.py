"""
Unpaywall Integration (ourresearch/unpaywall).
Discovers legal, open-access full-text PDFs and author accepted manuscripts.
Never bypasses paywalls or authentication; uses official Unpaywall REST API.
"""

from typing import Optional, Dict, Any
import httpx
from app.config import get_settings

settings = get_settings()


class UnpaywallClient:
    """Client for Unpaywall REST API."""

    BASE_URL = "https://api.unpaywall.org/v2"

    def __init__(self):
        self.email = settings.UNPAYWALL_EMAIL or "researchos@local.dev"

    async def get_oa_status(self, doi: str) -> Dict[str, Any]:
        """Query Unpaywall for open-access PDF availability."""
        # Clean DOI
        clean_doi = doi.strip()
        if clean_doi.startswith("https://doi.org/"):
            clean_doi = clean_doi[len("https://doi.org/") :]
        elif clean_doi.startswith("http://doi.org/"):
            clean_doi = clean_doi[len("http://doi.org/") :]

        url = f"{self.BASE_URL}/{clean_doi}"
        params = {"email": self.email}

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    best_oa = data.get("best_oa_location") or {}
                    return {
                        "is_oa": data.get("is_oa", False),
                        "oa_status": data.get("oa_status"),
                        "pdf_url": best_oa.get("url_for_pdf") or best_oa.get("url"),
                        "landing_page_url": best_oa.get("url_for_landing_page"),
                        "host_type": best_oa.get("host_type"),
                        "license": best_oa.get("license"),
                        "version": best_oa.get("version"),
                        "journal_is_oa": data.get("journal_is_oa", False),
                    }
                else:
                    return {
                        "is_oa": False,
                        "oa_status": "closed",
                        "pdf_url": None,
                        "landing_page_url": f"https://doi.org/{clean_doi}",
                    }
            except Exception:
                return {
                    "is_oa": False,
                    "oa_status": "lookup_failed",
                    "pdf_url": None,
                    "landing_page_url": f"https://doi.org/{clean_doi}",
                }


unpaywall_client = UnpaywallClient()
