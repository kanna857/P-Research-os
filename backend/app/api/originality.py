"""
Originality and similarity verification API routes (Sentence Transformers, RapidFuzz, Datasketch).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.paper import Paper
from app.integrations.originality.originality_engine import originality_engine

router = APIRouter()


@router.post("/check")
async def check_manuscript_originality(data: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """
    Compare manuscript text against accessible research library using:
    - Sentence Transformers embeddings
    - RapidFuzz token set ratio
    - Datasketch MinHash Jaccard similarity
    """
    project_id = data.get("project_id", 1)
    text = data.get("text", "")
    threshold = float(data.get("threshold", 0.60))

    result = await db.execute(select(Paper).where(Paper.project_id == project_id))
    papers = result.scalars().all()

    library = [
        {"title": p.title, "abstract": p.abstract or "", "doi": p.doi}
        for p in papers
    ]

    report = originality_engine.check_originality(
        manuscript_text=text,
        reference_library=library,
        similarity_threshold=threshold,
    )
    return report

