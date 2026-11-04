"""
Universal Multidisciplinary Research API Endpoints for P-Research-OS Ω.
Provides REST APIs for:
- Domain Routing across 36 academic disciplines
- Universal Methodology Planning across 9 study designs
- Interactive Research Knowledge Graph
- Statistical Analysis, Simulations, Systematic Reviews & Qualitative Coding
- Research Ethics & Regulatory Compliance
- Universal Manuscript Generation
- Unified End-to-End Autopilot
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.integrations.universal.domain_router import universal_domain_router, RESEARCH_DOMAINS
from app.integrations.universal.methodology_planner import universal_methodology_planner, METHODOLOGIES
from app.integrations.universal.knowledge_graph import research_knowledge_graph
from app.integrations.engines.statistical_engine import universal_statistical_engine
from app.integrations.engines.simulation_engine import scientific_simulation_engine
from app.integrations.engines.systematic_review_engine import systematic_review_engine
from app.integrations.engines.qualitative_engine import qualitative_research_engine
from app.integrations.engines.ethics_engine import research_ethics_engine
from app.integrations.writing.universal_manuscript_engine import universal_manuscript_engine
from app.integrations.universal.research_autopilot import universal_research_autopilot

router = APIRouter()


# ── Pydantic Request Models ──────────────────────────────────────────────────
class DomainRouteRequest(BaseModel):
    topic: str = Field(..., description="Research topic to classify")
    abstract_context: Optional[str] = None
    user_override_domain: Optional[str] = None


class MethodologyPlanRequest(BaseModel):
    topic: str
    primary_domain: Optional[str] = None
    user_methodology_override: Optional[str] = None


class KnowledgeGraphRequest(BaseModel):
    topic: str
    domain: Optional[str] = "Computer Science"
    methodology: Optional[str] = "computational"
    research_questions: Optional[List[str]] = None


class StatisticalAnalysisRequest(BaseModel):
    group_a: List[float]
    group_b: List[float]
    group_names: Optional[List[str]] = None
    paired: Optional[bool] = False


class SimulationRequest(BaseModel):
    length_meters: Optional[float] = 0.10
    thermal_diffusivity_alpha: Optional[float] = 1.2e-4
    initial_temp_celsius: Optional[float] = 25.0
    boundary_temp_left: Optional[float] = 180.0
    boundary_temp_right: Optional[float] = 25.0
    simulation_time_seconds: Optional[float] = 30.0


class QualitativeRequest(BaseModel):
    transcript_text: str
    domain: Optional[str] = "Social Sciences"


class SystematicReviewRequest(BaseModel):
    topic: str
    records_identified: Optional[int] = 1420


class EthicsScreeningRequest(BaseModel):
    topic: str
    methodology: Optional[str] = "computational"
    data_sources: Optional[List[str]] = None


class AutopilotStartRequest(BaseModel):
    topic: str = Field(..., description="Single topic entered by user")
    user_domain_override: Optional[str] = None
    user_methodology_override: Optional[str] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────
@router.post("/route-domain")
async def route_domain_endpoint(req: DomainRouteRequest):
    """Classifies topic into primary and secondary domains across 36 disciplines."""
    return universal_domain_router.classify_topic(
        topic=req.topic,
        abstract_context=req.abstract_context,
        user_override_domain=req.user_override_domain
    )


@router.post("/plan-methodology")
async def plan_methodology_endpoint(req: MethodologyPlanRequest):
    """Plans 10-point scientific methodology without assuming deep learning is required."""
    domain_routing = universal_domain_router.classify_topic(req.topic, user_override_domain=req.primary_domain)
    return universal_methodology_planner.plan_methodology(
        topic=req.topic,
        domain_routing=domain_routing,
        user_methodology_override=req.user_methodology_override
    )


@router.post("/knowledge-graph")
async def build_knowledge_graph_endpoint(req: KnowledgeGraphRequest):
    """Builds node-link research knowledge graph."""
    rqs = req.research_questions or [f"RQ: How does {req.topic} behave under empirical evaluation?"]
    return research_knowledge_graph.build_project_knowledge_graph(
        topic=req.topic,
        domain=req.domain or "Interdisciplinary Research",
        methodology=req.methodology or "computational",
        research_questions=rqs
    )


@router.post("/statistical-analysis")
async def statistical_analysis_endpoint(req: StatisticalAnalysisRequest):
    """Runs hypothesis-driven two-sample comparison with assumption validation and effect sizes."""
    names = (req.group_names[0], req.group_names[1]) if req.group_names and len(req.group_names) >= 2 else ("Control", "Treatment")
    return universal_statistical_engine.run_two_sample_comparison(
        group_a=req.group_a,
        group_b=req.group_b,
        group_names=names,
        paired=req.paired or False
    )


@router.post("/run-simulation")
async def run_simulation_endpoint(req: SimulationRequest):
    """Executes 1D transient heat conduction numerical simulation."""
    return scientific_simulation_engine.simulate_heat_transfer_1d(
        length_meters=req.length_meters or 0.10,
        thermal_diffusivity_alpha=req.thermal_diffusivity_alpha or 1.2e-4,
        initial_temp_celsius=req.initial_temp_celsius or 25.0,
        boundary_temp_left=req.boundary_temp_left or 180.0,
        boundary_temp_right=req.boundary_temp_right or 25.0,
        simulation_time_seconds=req.simulation_time_seconds or 30.0
    )


@router.post("/qualitative-coding")
async def qualitative_coding_endpoint(req: QualitativeRequest):
    """Performs transcript segmentation and thematic coding."""
    segments = qualitative_research_engine.segment_transcript(req.transcript_text)
    codebook = qualitative_research_engine.create_codebook(req.domain or "Social Sciences")
    return qualitative_research_engine.apply_thematic_coding(segments, codebook)


@router.post("/systematic-review")
async def systematic_review_endpoint(req: SystematicReviewRequest):
    """Generates PRISMA 2020 screening flow counts and meta-analytic pooling."""
    prisma = systematic_review_engine.generate_prisma_flow(topic=req.topic, records_identified=req.records_identified or 1420)
    meta = systematic_review_engine.run_meta_analysis_pooling()
    return {"prisma": prisma, "meta_analysis": meta}


@router.post("/ethics-screening")
async def ethics_screening_endpoint(req: EthicsScreeningRequest):
    """Screens research for IRB, HIPAA, IACUC, and sensitive triggers."""
    return research_ethics_engine.screen_project_ethics(
        topic=req.topic,
        methodology=req.methodology or "computational",
        data_sources=req.data_sources
    )


@router.post("/autopilot/start")
async def autopilot_start_endpoint(req: AutopilotStartRequest):
    """
    Core universal autopilot:
    Enter Topic -> Full Multidisciplinary Research Lifecycle Executed.
    """
    return universal_research_autopilot.run_autopilot_pipeline(
        topic=req.topic,
        user_domain_override=req.user_domain_override,
        user_methodology_override=req.user_methodology_override
    )


@router.get("/taxonomies")
async def get_taxonomies_endpoint():
    """Lists all 36 academic domains and 9 supported scientific methodologies."""
    return {
        "domains_count": len(RESEARCH_DOMAINS),
        "domains": list(RESEARCH_DOMAINS.keys()),
        "categories": list(set(d["category"] for d in RESEARCH_DOMAINS.values())),
        "methodologies_count": len(METHODOLOGIES),
        "methodologies": METHODOLOGIES
    }
