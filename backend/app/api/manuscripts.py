"""
Academic writing studio, LanguageTool grammar verification, and IEEE LaTeX manuscript generation API routes.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.manuscript import Manuscript, Reference
from app.integrations.writing.academic_writer import academic_writer
from app.integrations.writing.ieee_latex_generator import ieee_latex_generator
from app.integrations.citations.citation_engine import citation_engine

router = APIRouter()


@router.get("/project/{project_id}")
async def get_project_manuscript(project_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve or initialize manuscript for project."""
    result = await db.execute(select(Manuscript).where(Manuscript.project_id == project_id))
    manuscript = result.scalar_one_or_none()
    if not manuscript:
        # Create default initial manuscript
        manuscript = Manuscript(
            project_id=project_id,
            title="Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery: A Siamese Cross-Attention Approach",
            abstract=academic_writer.generate_manuscript_section("abstract", "Sentinel-1 SAR Change Detection"),
            keywords=["Sentinel-1 SAR", "Change Detection", "Siamese Network", "Attention Mechanism", "Remote Sensing"],
            sections={
                "introduction": academic_writer.generate_manuscript_section("introduction", "Sentinel-1 SAR Change Detection"),
                "methodology": academic_writer.generate_manuscript_section("methodology", "Sentinel-1 SAR Change Detection"),
                "results": academic_writer.generate_manuscript_section("results", "Sentinel-1 SAR Change Detection"),
                "conclusion": "In this paper, we introduced a novel Siamese deep learning architecture for multitemporal SAR change detection...",
            },
            template="IEEE J-STARS",
            references=[],
            status="draft",
            version=1,
        )
        db.add(manuscript)
        await db.commit()
        await db.refresh(manuscript)
    return manuscript


@router.put("/{manuscript_id}")
async def update_manuscript(
    manuscript_id: int,
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """Save manuscript text, sections, abstract, or template."""
    result = await db.execute(select(Manuscript).where(Manuscript.id == manuscript_id))
    manuscript = result.scalar_one_or_none()
    if not manuscript:
        raise HTTPException(status_code=404, detail="Manuscript not found")

    for k in ["title", "abstract", "keywords", "sections", "template", "status"]:
        if k in data:
            setattr(manuscript, k, data[k])

    manuscript.version += 1
    await db.commit()
    await db.refresh(manuscript)
    return manuscript


@router.post("/rewrite")
async def rewrite_academic_passage(data: Dict[str, Any]):
    """Rewrite text with academic tone adjustment (formal, technical, concise, natural)."""
    text = data.get("text", "")
    tone = data.get("tone", "formal")
    return academic_writer.rewrite_text(text=text, tone=tone)


@router.post("/check-grammar")
async def check_grammar_and_style(data: Dict[str, Any]):
    """Run LanguageTool grammar and style checks."""
    text = data.get("text", "")
    return academic_writer.check_grammar(text=text)


@router.post("/generate-section")
async def generate_section(data: Dict[str, Any]):
    """Generate structured section grounded in scientific evidence."""
    section_name = data.get("section_name", "abstract")
    topic = data.get("topic", "Sentinel-1 SAR Change Detection")
    content = academic_writer.generate_manuscript_section(section_name=section_name, topic=topic)
    return {"section_name": section_name, "content": content}


@router.post("/{manuscript_id}/compile-latex")
async def compile_manuscript_latex(manuscript_id: int, db: AsyncSession = Depends(get_db)):
    """Generate full IEEE J-STARS LaTeX document source."""
    result = await db.execute(select(Manuscript).where(Manuscript.id == manuscript_id))
    manuscript = result.scalar_one_or_none()
    if not manuscript:
        raise HTTPException(status_code=404, detail="Manuscript not found")

    latex_code = ieee_latex_generator.generate_full_manuscript_latex(
        title=manuscript.title,
        authors=["Alex Vance", "Elena Rostova", "Marcus Chen"],
        abstract=manuscript.abstract or "",
        keywords=manuscript.keywords or [],
        sections=manuscript.sections or {},
        references=manuscript.references or [],
        template=manuscript.template or "IEEE J-STARS",
    )

    return {
        "manuscript_id": manuscript_id,
        "template": manuscript.template,
        "latex_source": latex_code,
        "status": "ready_for_pdflatex_compilation",
    }

