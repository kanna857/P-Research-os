"""
API endpoints for Research Integrity, Plagiarism, Attribution, and Data Leakage Audits.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.integrations.originality.research_integrity_checker import ResearchIntegrityChecker

router = APIRouter()
integrity_checker = ResearchIntegrityChecker()


class IntegrityAuditRequest(BaseModel):
    manuscript_text: str = Field(..., description="Manuscript text to inspect")
    metrics: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Experimental metrics reported")
    split_metadata: Optional[Dict[str, Any]] = None
    tables_data: Optional[List[Dict[str, Any]]] = None


@router.post("/audit")
async def audit_integrity_endpoint(req: IntegrityAuditRequest):
    """
    Run full multi-factor research integrity audit:
    - Missing attribution
    - Unsupported novelty claims
    - Suspicious metric patterns (e.g. perfect scores)
    - Data leakage (spatial/temporal contamination)
    - Numerical consistency
    """
    default_metrics = req.metrics or {
        "accuracy": 0.945,
        "f1_score": 0.884,
        "iou": 0.795,
        "precision": 0.892,
        "recall": 0.876
    }
    return integrity_checker.full_integrity_audit(
        manuscript_text=req.manuscript_text,
        metrics=default_metrics,
        split_metadata=req.split_metadata,
        tables_data=req.tables_data
    )


@router.get("/rules")
async def get_integrity_rules():
    """List all research integrity rules and red-flag patterns checked."""
    return {
        "integrity_standards": [
            "Mandatory attribution for domain assertions and prior works",
            "Elimination of unhedged novelty absolutes ('first ever', 'unprecedented')",
            "Detection of implausible metrics (100% accuracy, zero test error)",
            "Spatial/temporal cross-validation enforcement (no random pixel split in geospatial datasets)",
            "Cross-section numerical consistency (Abstract vs Tables vs Conclusion)"
        ]
    }
