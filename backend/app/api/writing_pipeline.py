"""
Unified Academic Writing and Originality Engine API Routes.
Integrates:
- LanguageTool (languagetool-org/languagetool)
- TextHumanize (ksanyok/TextHumanize)
- Parrot Paraphraser (PrithivirajDamodaran/Parrot_Paraphraser)
- Noplag Engine (NoplagLabs/noplag-engine)
"""

from typing import List, Dict, Any, Optional
import io
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import StreamingResponse

from app.integrations.writing.languagetool_adapter import languagetool_adapter
from app.integrations.writing.text_humanize_adapter import text_humanize_adapter
from app.integrations.writing.parrot_paraphraser_adapter import parrot_adapter
from app.integrations.originality.noplag_adapter import noplag_adapter
from app.integrations.writing.unified_pipeline import unified_pipeline
from app.integrations.writing.ieee_latex_generator import ieee_latex_generator

logger = logging.getLogger(__name__)


async def _load_reference_library(project_id: int, inline_refs: Optional[List[Dict]] = None) -> List[Dict]:
    """Load reference library from DB if available, else fall back to inline refs or empty list."""
    if inline_refs:
        return inline_refs
    try:
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import select
        from app.database import get_db, async_session_factory
        from app.models.paper import Paper
        async with async_session_factory() as db:
            result = await db.execute(select(Paper).where(Paper.project_id == project_id))
            papers = result.scalars().all()
            return [
                {"title": p.title, "abstract": p.abstract or "", "doi": p.doi, "authors": p.authors}
                for p in papers
            ]
    except Exception as e:
        logger.warning(f"Database unavailable for reference library (project_id={project_id}): {e}")
        return []

router = APIRouter()


@router.post("/grammar-check")
async def grammar_check(data: Dict[str, Any]):
    """LanguageTool grammar, spelling, punctuation, and academic clarity check."""
    text = data.get("text", "")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return languagetool_adapter.check(text)


@router.post("/humanize-style")
async def humanize_style(data: Dict[str, Any]):
    """TextHumanize academic style refinement (formal, technical, concise, natural)."""
    text = data.get("text", "")
    style = data.get("style", "formal")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return text_humanize_adapter.refine_style(text=text, style=style)


@router.post("/paraphrase")
async def paraphrase_sentence(data: Dict[str, Any]):
    """Parrot Paraphraser controlled academic rewriting with metric & citation preservation."""
    sentence = data.get("sentence", "")
    max_cand = int(data.get("max_candidates", 3))
    if not sentence.strip():
        raise HTTPException(status_code=400, detail="Sentence cannot be empty")
    return parrot_adapter.paraphrase(sentence=sentence, max_candidates=max_cand)


@router.post("/noplag-similarity")
async def noplag_similarity(data: Dict[str, Any]):
    """Noplag Engine similarity and originality analysis against project library."""
    text = data.get("text", "")
    project_id = int(data.get("project_id", 1))
    threshold = float(data.get("threshold", 0.45))
    api_key = data.get("commercial_api_key")
    inline_refs = data.get("reference_library")

    library = await _load_reference_library(project_id, inline_refs)

    return noplag_adapter.analyze_similarity(
        manuscript_text=text,
        reference_library=library,
        similarity_threshold=threshold,
        commercial_api_key=api_key,
    )


@router.post("/verify-citations")
async def verify_citations(data: Dict[str, Any]):
    """Verify in-text citation markers [1] against project reference database and experimental claims."""
    text = data.get("text", "")
    project_id = int(data.get("project_id", 1))
    inline_refs = data.get("reference_library")

    library = await _load_reference_library(project_id, inline_refs)
    library_slim = [{"title": r.get("title", ""), "doi": r.get("doi", "")} for r in library]

    benchmark = data.get("experimental_benchmark", {
        "f1_score": "93.8%",
        "miou": "0.841",
        "accuracy": "96.4%",
    })

    return unified_pipeline._verify_citations_and_claims(
        manuscript_text=text,
        reference_library=library_slim,
        experimental_benchmark=benchmark,
    )


@router.post("/autonomous-review")
async def autonomous_manuscript_review(data: Dict[str, Any]):
    """
    Execute the complete 7-step autonomous review pipeline:
    LanguageTool -> TextHumanize -> Parrot -> Noplag -> Citation Verification -> Quality Scorecard.
    """
    text = data.get("text", "")
    project_title = data.get("project_title", "Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery")
    project_id = int(data.get("project_id", 1))
    target_style = data.get("style", "formal")
    inline_refs = data.get("reference_library")

    library = await _load_reference_library(project_id, inline_refs)

    benchmark = data.get("experimental_benchmark", {
        "f1_score": "93.8%",
        "miou": "0.841",
        "accuracy": "96.4%",
    })

    return unified_pipeline.run_autonomous_review(
        manuscript_text=text,
        project_title=project_title,
        reference_library=library,
        experimental_benchmark=benchmark,
        target_style=target_style,
    )


@router.post("/export-docx")
async def export_manuscript_docx(data: Dict[str, Any]):
    """Export camera-ready manuscript as a formatted Microsoft Word DOCX file."""
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH

        title = data.get("title", "Manuscript Title")
        abstract = data.get("abstract", "")
        keywords = data.get("keywords", ["Remote Sensing", "Deep Learning", "Sentinel-1"])
        sections = data.get("sections", {})

        doc = Document()

        # Title
        p_title = doc.add_paragraph()
        run_title = p_title.add_run(title)
        run_title.font.size = Pt(20)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(15, 23, 42)
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Subtitle / Authors
        p_auth = doc.add_paragraph()
        run_auth = p_auth.add_run("ResearchOS Autonomous Research System • IEEE J-STARS Format")
        run_auth.font.size = Pt(10)
        run_auth.font.italic = True
        p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Abstract
        if abstract:
            doc.add_heading("Abstract", level=1)
            p_abs = doc.add_paragraph()
            p_abs.add_run(abstract).font.size = Pt(10.5)

        # Keywords
        if keywords:
            p_kw = doc.add_paragraph()
            r_kw_bold = p_kw.add_run("Keywords—")
            r_kw_bold.bold = True
            p_kw.add_run(", ".join(keywords))

        # Sections
        for sec_name, sec_content in sections.items():
            doc.add_heading(sec_name.replace("_", " ").title(), level=1)
            for paragraph in str(sec_content).split("\n\n"):
                if paragraph.strip():
                    doc.add_paragraph(paragraph.strip())

        # Save to buffer
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        filename = f"Manuscript_{title[:25].replace(' ', '_')}.docx"
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate DOCX: {str(e)}")


@router.post("/export-latex")
async def export_manuscript_latex(data: Dict[str, Any]):
    """Export manuscript as IEEE J-STARS two-column LaTeX file (.tex)."""
    title = data.get("title", "Deep Learning-Based Change Detection Using Sentinel-1 SAR Imagery")
    abstract = data.get("abstract", "")
    keywords = data.get("keywords", ["Sentinel-1", "SAR", "Change Detection", "Siamese Network"])
    sections = data.get("sections", {})
    references = data.get("references", [])

    latex_code = ieee_latex_generator.generate_latex(
        title=title,
        authors=[{"name": "ResearchOS Principal Investigator", "affiliation": "Scientific AI Systems Laboratory"}],
        abstract=abstract,
        keywords=keywords,
        sections=sections,
        references=references,
    )

    filename = "IEEE_JSTARS_Manuscript.tex"
    return Response(
        content=latex_code,
        media_type="text/x-tex",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post("/export-report")
async def export_originality_report(data: Dict[str, Any]):
    """Export downloadable Noplag & Academic Quality Audit report."""
    audit_data = data.get("audit_data", {})
    project_title = data.get("project_title", "Research Project")
    report = noplag_adapter.generate_report_export(audit_data, project_title)

    filename = "Noplag_Originality_Audit_Report.json"
    import json
    return Response(
        content=json.dumps(report, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

