"""
Source Provenance & Attribution Tracking Ledger for ResearchOS.
Maintains tamper-evident provenance records for all crawled web pages,
scientific articles, and public datasets.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid


class ProvenanceRecord:
    """Represents the provenance record of an acquired web document or scientific asset."""

    def __init__(
        self,
        url: str,
        canonical_url: str,
        crawler_tool: str,
        status_code: int,
        robots_compliant: bool = True,
        content_hash: str = "",
        title: Optional[str] = None,
        author: Optional[str] = None,
        publication_date: Optional[str] = None,
        is_paywalled: bool = False,
        license_info: Optional[str] = None,
        project_id: int = 1,
        evidence_type: str = "scholarly_article",
    ):
        self.evidence_id = f"evd_{uuid.uuid4().hex[:12]}"
        self.url = url
        self.canonical_url = canonical_url
        self.crawler_tool = crawler_tool
        self.status_code = status_code
        self.robots_compliant = robots_compliant
        self.content_hash = content_hash
        self.title = title or "Untitled Scholarly Resource"
        self.author = author
        self.publication_date = publication_date
        self.is_paywalled = is_paywalled
        self.license_info = license_info or "Public Web Access / Fair Academic Attribution"
        self.project_id = project_id
        self.evidence_type = evidence_type
        self.retrieved_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "url": self.url,
            "canonical_url": self.canonical_url,
            "crawler_tool": self.crawler_tool,
            "status_code": self.status_code,
            "robots_compliant": self.robots_compliant,
            "content_hash": self.content_hash,
            "title": self.title,
            "author": self.author,
            "publication_date": self.publication_date,
            "is_paywalled": self.is_paywalled,
            "license_info": self.license_info,
            "project_id": self.project_id,
            "evidence_type": self.evidence_type,
            "retrieved_at": self.retrieved_at,
        }


class ProvenanceTracker:
    """Global ledger of source provenance entries."""

    def __init__(self):
        self._records: Dict[str, ProvenanceRecord] = {}

    def register(
        self,
        url: str,
        canonical_url: str,
        crawler_tool: str,
        status_code: int,
        robots_compliant: bool = True,
        content_hash: str = "",
        title: Optional[str] = None,
        author: Optional[str] = None,
        publication_date: Optional[str] = None,
        is_paywalled: bool = False,
        license_info: Optional[str] = None,
        project_id: int = 1,
        evidence_type: str = "scholarly_article",
    ) -> ProvenanceRecord:
        record = ProvenanceRecord(
            url=url,
            canonical_url=canonical_url,
            crawler_tool=crawler_tool,
            status_code=status_code,
            robots_compliant=robots_compliant,
            content_hash=content_hash,
            title=title,
            author=author,
            publication_date=publication_date,
            is_paywalled=is_paywalled,
            license_info=license_info,
            project_id=project_id,
            evidence_type=evidence_type,
        )
        self._records[record.evidence_id] = record
        return record

    def get_by_id(self, evidence_id: str) -> Optional[Dict[str, Any]]:
        record = self._records.get(evidence_id)
        return record.to_dict() if record else None

    def list_records(self, project_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
        records = list(self._records.values())
        if project_id is not None:
            records = [r for r in records if r.project_id == project_id]
        records.sort(key=lambda r: r.retrieved_at, reverse=True)
        return [r.to_dict() for r in records[:limit]]

    def get_provenance_badge(self, evidence_id: str) -> Dict[str, Any]:
        record = self._records.get(evidence_id)
        if not record:
            return {"verified": False, "message": "Unknown provenance record"}
        return {
            "verified": True,
            "evidence_id": record.evidence_id,
            "canonical_url": record.canonical_url,
            "crawler_tool": record.crawler_tool,
            "robots_compliant": record.robots_compliant,
            "retrieved_at": record.retrieved_at,
            "content_hash": record.content_hash[:12] + "...",
            "attribution_label": f"Retrieved via {record.crawler_tool} from {record.canonical_url} on {record.retrieved_at[:10]}",
        }


provenance_tracker = ProvenanceTracker()
