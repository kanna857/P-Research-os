"""
Celery Asynchronous Background Tasks for ResearchOS.
Provides durable queued execution across discovery, PDF extraction, dataset partitioning,
model training, scientific evaluation, evidence verification, and manuscript compilation.
Includes cancellation checks, retries with backoff, and PostgreSQL progress synchronization.
"""

from typing import Dict, Any, Optional
import asyncio
import logging

from app.workers.celery_app import celery_app
from app.integrations.infrastructure.redis_coordinator import redis_coordinator
from app.integrations.nhost.hasura_client import hasura_client

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Safely run async coroutine in sync Celery task worker."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


@celery_app.task(
    name="app.workers.tasks.search_papers_async",
    bind=True,
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
)
def search_papers_async(self, topic: str, project_id: int = 1, job_id: Optional[str] = None):
    """Run federated paper discovery across 10 academic repositories."""
    if job_id and redis_coordinator.is_job_cancelled(job_id):
        logger.info(f"Job {job_id} cancelled before execution.")
        return {"status": "cancelled", "job_id": job_id}

    from app.integrations.discovery.papers_federated import papers_federated_discovery
    logger.info(f"Starting Celery paper search task for topic: '{topic}'")

    if job_id:
        _run_async(hasura_client.log_job_progress(
            job_id=job_id,
            project_id=project_id,
            job_type="paper_discovery",
            progress_pct=25.0,
            step_message=f"Querying 10 academic paper repositories for '{topic}'...",
        ))

    results = _run_async(papers_federated_discovery.search_all_repositories(query=topic, limit_per_source=4))

    if job_id:
        _run_async(hasura_client.log_job_progress(
            job_id=job_id,
            project_id=project_id,
            job_type="paper_discovery",
            progress_pct=100.0,
            step_message=f"Discovered {results.get('total_found', 0)} papers.",
            status="completed",
            result_payload={"total_found": results.get("total_found", 0)},
        ))

    return results


@celery_app.task(
    name="app.workers.tasks.discover_datasets_async",
    bind=True,
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=True,
)
def discover_datasets_async(self, topic: str, project_id: int = 1, job_id: Optional[str] = None):
    """Run federated dataset discovery across Kaggle, Zenodo, Copernicus, Hugging Face, etc."""
    if job_id and redis_coordinator.is_job_cancelled(job_id):
        return {"status": "cancelled", "job_id": job_id}

    from app.integrations.discovery.datasets_federated import datasets_federated_discovery
    logger.info(f"Starting Celery dataset discovery for topic: '{topic}'")

    results = _run_async(datasets_federated_discovery.search_all_repositories(query=topic, limit_per_source=4))
    return results


@celery_app.task(
    name="app.workers.tasks.extract_pdf_async",
    bind=True,
    autoretry_for=(Exception,),
    max_retries=2,
)
def extract_pdf_async(self, pdf_path: str, paper_id: int = 1, job_id: Optional[str] = None):
    """Hierarchical scientific PDF extraction using Docling / GROBID with pgvector indexing."""
    from app.integrations.pdf_processing.docling_extractor import docling_extractor
    from app.integrations.nhost.semantic_search import semantic_search_engine

    extracted = _run_async(docling_extractor.extract_pdf(pdf_path))
    if "sections" in extracted:
        # Index extracted sections into pgvector
        _run_async(semantic_search_engine.index_paper(
            paper_id=paper_id,
            title=extracted.get("metadata", {}).get("title", "Research Paper"),
            abstract=extracted.get("sections", {}).get("abstract"),
            methodology=extracted.get("sections", {}).get("methodology"),
            limitations=extracted.get("sections", {}).get("limitations"),
        ))

    return extracted


@celery_app.task(name="app.workers.tasks.process_dataset_async")
def process_dataset_async(raw_path: str, output_dir: str, config: dict):
    """Execute reproducible 80/20 non-leaking dataset partitioning."""
    from app.integrations.preprocessing.split_manager import preprocessing_split_manager
    return preprocessing_split_manager.process_dataset(
        raw_dataset_path=raw_path,
        output_dir=output_dir,
        train_ratio=0.80,
    )


@celery_app.task(
    name="app.workers.tasks.train_model_async",
    bind=True,
)
def train_model_async(self, job_id: int, model_name: str, epochs: int):
    """Execute PyTorch Lightning model training with checkpointing and metrics."""
    from app.integrations.training.lightning_trainer import lightning_engine
    return _run_async(lightning_engine.run_training(job_id=job_id, model_name=model_name, epochs=epochs))


@celery_app.task(name="app.workers.tasks.verify_evidence_async")
def verify_evidence_async(manuscript_text: str, project_id: int = 1):
    """Run Evidence Verification Agent on manuscript claims against indexed research literature."""
    from app.integrations.research.evidence_verification_agent import evidence_verification_agent
    return _run_async(evidence_verification_agent.verify_manuscript_claims(manuscript_text=manuscript_text, project_id=project_id))


@celery_app.task(name="app.workers.tasks.compile_manuscript_async")
def compile_manuscript_async(manuscript_id: int, format: str = "latex"):
    """Compile IEEE journal manuscript with citations and figure references."""
    from app.integrations.writing.journal_export_engine import journal_export_engine
    return journal_export_engine.export_ieee_manuscript(manuscript_id=manuscript_id, export_format=format)
