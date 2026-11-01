"""Celery application configuration for ResearchOS background task processing."""

from celery import Celery

try:
    from app.config import settings

    BROKER_URL = settings.REDIS_URL
    RESULT_BACKEND = settings.REDIS_URL
except (ImportError, Exception):
    # Fallback for standalone execution or when settings are unavailable
    BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"

celery_app = Celery(
    "researchos",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=3600,
)

# Autodiscover tasks from app.workers package
celery_app.autodiscover_tasks(["app.workers"])
