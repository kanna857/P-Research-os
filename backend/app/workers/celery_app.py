"""Celery application configuration for ResearchOS background task processing."""

try:
    from celery import Celery
except ImportError:
    class DummyConf(dict):
        def update(self, *args, **kwargs):
            if args and isinstance(args[0], dict):
                super().update(args[0])
            super().update(kwargs)

        def __getattr__(self, name):
            return self.get(name)

    class Celery:
        def __init__(self, name, broker=None, backend=None):
            self.name = name
            self.broker = broker
            self.backend = backend
            self.conf = DummyConf()

        def autodiscover_tasks(self, packages):
            pass

        def task(self, *args, **kwargs):
            def decorator(f):
                f.delay = f
                f.apply_async = lambda *a, **kw: None
                return f
            return decorator

try:
    from app.config import settings

    BROKER_URL = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")
    RESULT_BACKEND = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")
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
    task_time_limit=1800,       # 30 minutes hard limit
    task_soft_time_limit=1500,  # 25 minutes soft limit
    task_routes={
        "app.workers.tasks.search_papers_async": {"queue": "discovery_queue"},
        "app.workers.tasks.discover_datasets_async": {"queue": "discovery_queue"},
        "app.workers.tasks.extract_pdf_async": {"queue": "pdf_queue"},
        "app.workers.tasks.process_dataset_async": {"queue": "datasets_queue"},
        "app.workers.tasks.train_model_async": {"queue": "training_queue"},
        "app.workers.tasks.evaluate_experiment_async": {"queue": "evaluation_queue"},
        "app.workers.tasks.verify_evidence_async": {"queue": "verification_queue"},
        "app.workers.tasks.compile_manuscript_async": {"queue": "manuscript_queue"},
    },
)

# Autodiscover tasks from app.workers package
celery_app.autodiscover_tasks(["app.workers"])
