"""
Celery asynchronous background tasks.
"""

from app.workers.celery_app import celery_app
from app.integrations.research.openalex_client import openalex_client
from app.integrations.pdf_processing.docling_extractor import docling_extractor
from app.integrations.preprocessing.split_manager import preprocessing_split_manager
from app.integrations.training.lightning_trainer import lightning_engine
import asyncio


@celery_app.task(name="app.workers.tasks.search_papers_async")
def search_papers_async(query: str, year_from: int = None, year_to: int = None):
    """Run paper discovery in durable Celery queue."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        openalex_client.search_works(query=query, year_from=year_from, year_to=year_to)
    )


@celery_app.task(name="app.workers.tasks.process_dataset_async")
def process_dataset_async(raw_path: str, output_dir: str, config: dict):
    """Run 80/20 dataset partitioning in durable Celery queue."""
    return preprocessing_split_manager.process_dataset(
        raw_dataset_path=raw_path,
        output_dir=output_dir,
        train_ratio=0.80,
    )


@celery_app.task(name="app.workers.tasks.train_model_async")
def train_model_async(job_id: int, model_name: str, epochs: int):
    """Execute model training in durable Celery worker."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        lightning_engine.run_training(job_id=job_id, model_name=model_name, epochs=epochs)
    )

