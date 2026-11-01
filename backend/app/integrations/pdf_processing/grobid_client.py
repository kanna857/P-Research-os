"""
GROBID Integration (kermitt2/grobid).
Parses scientific PDF headers, authors, affiliations, citations, and TEI-XML representations.
"""

from typing import Dict, Any, Optional
import httpx
from app.config import get_settings

settings = get_settings()


class GrobidClient:
    """Client for GROBID TEI-XML extraction service."""

    def __init__(self):
        self.grobid_url = settings.GROBID_URL.rstrip("/")

    async def is_healthy(self) -> bool:
        """Check if GROBID service is running."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.grobid_url}/api/isalive")
                return resp.status_code == 200
        except Exception:
            return False

    async def process_header(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Extract bibliographic header metadata via GROBID."""
        if not await self.is_healthy():
            return {"status": "grobid_unavailable", "message": "GROBID service not detected"}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"input": ("paper.pdf", pdf_bytes, "application/pdf")}
                resp = await client.post(f"{self.grobid_url}/api/processHeaderDocument", files=files)
                if resp.status_code == 200:
                    return {
                        "status": "success",
                        "tei_xml": resp.text,
                    }
                return {"status": "error", "code": resp.status_code, "text": resp.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def process_references(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Extract structured reference list from PDF."""
        if not await self.is_healthy():
            return {"status": "grobid_unavailable"}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"input": ("paper.pdf", pdf_bytes, "application/pdf")}
                resp = await client.post(f"{self.grobid_url}/api/processReferences", files=files)
                if resp.status_code == 200:
                    return {"status": "success", "tei_xml": resp.text}
                return {"status": "error", "code": resp.status_code}
        except Exception as e:
            return {"status": "error", "message": str(e)}


grobid_client = GrobidClient()
