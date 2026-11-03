"""
Main API router: groups all functional sub-routers under /api prefix.
"""

from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.papers import router as papers_router
from app.api.datasets import router as datasets_router
from app.api.models import router as models_router
from app.api.evaluation import router as evaluation_router
from app.api.manuscripts import router as manuscripts_router
from app.api.references import router as references_router
from app.api.diagrams import router as diagrams_router
from app.api.originality import router as originality_router
from app.api.exports import router as exports_router
from app.api.writing_pipeline import router as writing_pipeline_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
api_router.include_router(papers_router, prefix="/papers", tags=["Research Papers"])
api_router.include_router(datasets_router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(models_router, prefix="/models", tags=["Models & Training"])
api_router.include_router(evaluation_router, prefix="/evaluation", tags=["Scientific Evaluation"])
api_router.include_router(manuscripts_router, prefix="/manuscripts", tags=["Manuscripts & Writing"])
api_router.include_router(references_router, prefix="/references", tags=["References & Citations"])
api_router.include_router(diagrams_router, prefix="/diagrams", tags=["Scientific Diagrams"])
api_router.include_router(originality_router, prefix="/originality", tags=["Originality & Similarity"])
api_router.include_router(writing_pipeline_router, prefix="/writing-pipeline", tags=["Academic Writing & Originality Pipeline"])
api_router.include_router(exports_router, prefix="/exports", tags=["Project Export"])
