"""
API endpoints for System Monitoring, Node Health Diagnostics, and Prometheus Metrics.
"""

from fastapi import APIRouter, Response
from app.integrations.infrastructure.monitoring_service import SystemMonitoringService

router = APIRouter()
monitor = SystemMonitoringService()


@router.get("/health")
async def health_endpoint():
    """
    Comprehensive health check across FastAPI, PostgreSQL, Redis, Celery, Ollama,
    and system hardware resources (CPU, RAM, Disk, GPU).
    """
    return await monitor.check_full_health()


@router.get("/jobs")
async def jobs_metrics_endpoint():
    """Returns active, completed, failed research jobs and Celery queue depths."""
    return monitor.get_job_metrics()


@router.get("/metrics")
async def prometheus_metrics_endpoint():
    """
    Prometheus-compatible plain text metrics exposition.
    """
    health = await monitor.check_full_health()
    jobs = monitor.get_job_metrics()
    metrics_text = monitor.generate_prometheus_metrics(health, jobs)
    return Response(content=metrics_text, media_type="text/plain; version=0.0.4; charset=utf-8")
