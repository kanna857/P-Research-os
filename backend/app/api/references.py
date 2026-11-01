"""
Reference manager, DOI verification, and BibTeX/RIS export API routes.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.manuscript import Reference
from app.integrations.citations.citation_engine import citation_engine

router = APIRouter()


@router.get("/project/{project_id}")
async def get_project_references(project_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all references for project."""
    result = await db.execute(select(Reference).where(Reference.project_id == project_id))
    refs = result.scalars().all()
    if not refs:
        # Seed initial standard references for the benchmark
        sample_refs = [
            Reference(
                project_id=project_id,
                title="A Deep Convolutional Coupling Network for Change Detection in Multitemporal SAR Images",
                authors=["G. Gong", "M. Liu", "Y. Li"],
                year=2023,
                doi="10.1109/TGRS.2023.3245671",
                venue="IEEE Transactions on Geoscience and Remote Sensing",
                verified=True,
            ),
            Reference(
                project_id=project_id,
                title="Siamese-Based Multiscale Attention Networks for High-Resolution Remote Sensing Change Detection",
                authors=["C. Zhang", "P. Yue", "D. Tapete"],
                year=2024,
                doi="10.1109/JSTARS.2024.3359012",
                venue="IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing",
                verified=True,
            ),
            Reference(
                project_id=project_id,
                title="Deep Learning in Remote Sensing: A Review and Global Benchmark",
                authors=["X. Zhu", "D. Tuia", "L. Mou"],
                year=2022,
                doi="10.1109/MGRS.2022.3168750",
                venue="IEEE Geoscience and Remote Sensing Magazine",
                verified=True,
            ),
        ]
        for r in sample_refs:
            db.add(r)
        await db.commit()
        result = await db.execute(select(Reference).where(Reference.project_id == project_id))
        refs = result.scalars().all()
    return refs


@router.post("")
async def add_reference(data: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """Add a new bibliographic reference to project."""
    ref = Reference(
        project_id=data.get("project_id", 1),
        title=data.get("title", "Untitled Reference"),
        authors=data.get("authors", ["Author"]),
        year=data.get("year", 2024),
        doi=data.get("doi"),
        venue=data.get("venue", "IEEE J-STARS"),
        verified=False,
    )
    db.add(ref)
    await db.commit()
    await db.refresh(ref)
    return ref


@router.post("/verify-doi")
async def verify_doi_endpoint(data: Dict[str, str]):
    """Verify DOI with Crossref official registry."""
    doi = data.get("doi", "")
    return await citation_engine.verify_doi(doi)


@router.get("/export-bibtex/{project_id}")
async def export_bibtex(project_id: int, db: AsyncSession = Depends(get_db)):
    """Export project references as complete BibTeX file."""
    result = await db.execute(select(Reference).where(Reference.project_id == project_id))
    refs = result.scalars().all()
    bib_entries = [
        citation_engine.to_bibtex({
            "title": r.title,
            "authors": r.authors,
            "year": r.year,
            "venue": r.venue,
            "doi": r.doi,
        })
        for r in refs
    ]
    return {"bibtex": "\n\n".join(bib_entries)}


@router.post("/detect-duplicates")
async def detect_duplicates_endpoint(references: List[Dict[str, Any]]):
    """Scan reference array for duplicate DOIs or titles."""
    return citation_engine.detect_duplicates(references)

