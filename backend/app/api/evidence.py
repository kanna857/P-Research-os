"""
API endpoints for Evidence Verification and Grounded Scientific Retrieval.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.integrations.research.evidence_verification_agent import EvidenceVerificationAgent
from app.integrations.nhost.semantic_search import SemanticSearchEngine

router = APIRouter()
verification_agent = EvidenceVerificationAgent()
search_engine = SemanticSearchEngine()


class ClaimVerificationRequest(BaseModel):
    claim_text: str = Field(..., description="The factual or experimental statement to verify")
    citations: Optional[List[str]] = Field(default_factory=list, description="Associated citation markers e.g. ['1']")
    evidence_passages: Optional[List[Dict[str, Any]]] = None


class ManuscriptVerificationRequest(BaseModel):
    project_id: Optional[str] = None
    manuscript_text: str = Field(..., description="Full text or section to verify")
    evidence_passages: Optional[List[Dict[str, Any]]] = None


class SemanticQueryRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/verify-claim")
async def verify_claim_endpoint(req: ClaimVerificationRequest):
    """Verify a single claim against evidence passages."""
    claim = {
        "claim_id": "req-claim-001",
        "text": req.claim_text,
        "citations": req.citations or []
    }
    passages = req.evidence_passages or verification_agent._get_default_evidence_pool()
    result = verification_agent.verify_claim(claim, passages)
    return result


@router.post("/verify-manuscript")
async def verify_manuscript_endpoint(req: ManuscriptVerificationRequest):
    """
    Extract all claims from manuscript, query pgvector / evidence chunks,
    and return verification status for every claim with an overall confidence score.
    """
    return verification_agent.verify_manuscript(
        manuscript_text=req.manuscript_text,
        project_id=req.project_id,
        evidence_passages=req.evidence_passages
    )


@router.post("/search-evidence")
async def search_evidence_endpoint(req: SemanticQueryRequest):
    """Retrieve top-K semantically relevant evidence passages using pgvector embeddings."""
    q_vec = search_engine.compute_embedding(req.query)
    pool = verification_agent._get_default_evidence_pool()
    results = []

    for item in pool:
        p_vec = search_engine.compute_embedding(item["content"])
        sim = search_engine.cosine_similarity(q_vec, p_vec)
        results.append({
            **item,
            "similarity_score": round(sim, 4)
        })

    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return {"query": req.query, "results": results[:req.top_k]}


@router.get("/benchmark-evidence")
async def get_benchmark_evidence():
    """Returns baseline literature chunks for Sentinel-1 SAR change detection."""
    return {
        "benchmark_topic": "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection",
        "passages": verification_agent._get_default_evidence_pool()
    }
