"""
Comprehensive test suite for the 10 Essential Technologies and 5 Advanced Research Capabilities:
1. Redis Coordinator & Caching
2. Celery Multi-Queue Worker Architecture
3. Ollama Local LLM & Evidence Grounding
4. Evidence Verification Agent
5. Scientific Reproducibility Engine
6. Research Integrity Checker
7. Journal-Ready Manuscript Export Engine
8. FiftyOne Remote Sensing Visualizer
9. System Monitoring & Prometheus Telemetry
"""

import pytest
import os
import tempfile
import json
from pathlib import Path

from app.integrations.infrastructure.redis_coordinator import RedisCoordinator
from app.integrations.llm.ollama_client import OllamaClient
from app.integrations.research.evidence_verification_agent import EvidenceVerificationAgent
from app.integrations.research.reproducibility_engine import ScientificReproducibilityEngine
from app.integrations.originality.research_integrity_checker import ResearchIntegrityChecker
from app.integrations.writing.journal_export_engine import JournalExportEngine
from app.integrations.datasets.fiftyone_adapter import FiftyOneSARVisualizer
from app.integrations.infrastructure.monitoring_service import SystemMonitoringService
from app.workers.celery_app import celery_app


# ── 1. Redis Coordinator Tests ───────────────────────────────────────────────
def test_redis_coordinator_caching():
    coord = RedisCoordinator()
    coord.set("test_key", {"foo": "bar"}, ttl_seconds=60)
    val = coord.get("test_key")
    assert val == {"foo": "bar"}

    coord.delete("test_key")
    assert coord.get("test_key") is None


def test_redis_coordinator_cancellation_and_rate_limit():
    coord = RedisCoordinator()
    job_id = "job-test-999"
    coord.cancel_job(job_id)
    assert coord.is_job_cancelled(job_id) is True

    # Rate limiting
    rl = coord.check_rate_limit("user-1:openalex", max_requests=3, window_seconds=60)
    assert rl["allowed"] is True
    assert rl["current"] >= 1

    health = coord.get_health()
    assert "connected" in health
    assert "mode" in health


# ── 2. Celery Multi-Queue Routing ────────────────────────────────────────────
def test_celery_queues_and_configuration():
    assert celery_app.conf.task_routes is not None
    routes = celery_app.conf.task_routes
    assert "app.workers.tasks.search_papers_async" in routes
    assert routes["app.workers.tasks.search_papers_async"]["queue"] == "discovery_queue"
    assert routes["app.workers.tasks.train_model_async"]["queue"] == "training_queue"
    assert routes["app.workers.tasks.verify_evidence_async"]["queue"] == "verification_queue"
    assert routes["app.workers.tasks.compile_manuscript_async"]["queue"] == "manuscript_queue"


# ── 3. Ollama Local LLM & Grounding ──────────────────────────────────────────
@pytest.mark.asyncio
async def test_ollama_client_grounding():
    client = OllamaClient()
    health = await client.check_health()
    assert "status" in health
    assert health["status"] in ("ONLINE", "OFFLINE")

    # Test grounded generation
    evidence = [
        {"title": "SAR Speckle Mitigation", "content": "Log-ratio dual-pol filtering preserves edges in flood mapping."}
    ]
    resp = await client.generate_evidence_grounded(
        prompt="Explain SAR despeckling",
        evidence_chunks=evidence
    )
    assert "generated_text" in resp
    assert "citations_included" in resp
    assert "grounding_score" in resp


# ── 4. Evidence Verification Agent ───────────────────────────────────────────
def test_evidence_verification_claims():
    agent = EvidenceVerificationAgent()
    sample_text = (
        "Recent Siamese convolutional networks achieve F1-scores over 0.88 when trained on dual-polarized Sentinel-1 GRD imagery [1]. "
        "Our approach outperforms standard baselines by 12%."
    )
    claims = agent.extract_claims(sample_text)
    assert len(claims) >= 1

    audit = agent.verify_manuscript(sample_text)
    assert "evidence_verification_score" in audit
    assert "is_submission_ready" in audit
    assert "verified_claims" in audit
    assert len(audit["verified_claims"]) >= 1


# ── 5. Scientific Reproducibility Engine ──────────────────────────────────────
def test_scientific_reproducibility_engine():
    engine = ScientificReproducibilityEngine()
    commit = engine.get_git_commit()
    assert commit is not None

    dvc_hash = engine.compute_dvc_checksum()
    assert dvc_hash.startswith("dvc-")

    manifest = engine.generate_manifest(
        experiment_id="exp-test-01",
        project_name="Test Sentinel-1 Project",
        hyperparameters={"lr": 0.001, "batch_size": 32},
        metrics={"f1_score": 0.884, "iou": 0.795}
    )
    assert manifest["experiment_id"] == "exp-test-01"
    assert "provenance" in manifest
    assert "evaluation_protocol" in manifest

    # Test package creation
    with tempfile.TemporaryDirectory() as tmpdir:
        out_zip = os.path.join(tmpdir, "test_pkg.zip")
        pkg_path = engine.create_reproducibility_package(manifest, out_zip)
        assert os.path.exists(pkg_path)
        assert os.path.getsize(pkg_path) > 500

    # Test rerun reproduction
    repro = engine.reproduce_experiment(manifest)
    assert repro["status"] == "Verified Reproducible"
    assert repro["reproducibility_grade"] == "A+ (Full Determinism Verified)"


# ── 6. Research Integrity Checker ────────────────────────────────────────────
def test_research_integrity_checker():
    checker = ResearchIntegrityChecker()

    # Flawed text with overclaiming and missing attribution
    flawed_text = (
        "We introduce the first ever flawless framework for SAR. "
        "Recent advances in convnets show great promise for multitemporal remote sensing imagery."
    )
    metrics = {"accuracy": 1.00, "f1_score": 0.884}  # Suspicious 1.00 accuracy

    audit = checker.full_integrity_audit(flawed_text, metrics)
    assert audit["findings_count"] > 0
    assert audit["overall_integrity_score"] < 100
    # Overclaiming and 100% accuracy should be flagged
    categories = [f["category"] for f in audit["findings"]]
    assert "Unsupported Novelty Claim" in categories or "Suspicious Metric" in categories


# ── 7. Journal-Ready Manuscript Export Engine ────────────────────────────────
def test_journal_export_engine():
    engine = JournalExportEngine()

    readiness = engine.audit_publication_readiness(
        title="Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection",
        abstract="Synthetic Aperture Radar change detection is critical. " * 15,
        sections={
            "introduction": "Intro content...",
            "methodology": "Methods content...",
            "results": "Results content...",
            "conclusion": "Conclusion content..."
        },
        references=[{"title": f"Ref {i}", "year": 2024} for i in range(16)]
    )
    assert "is_ready_for_export" in readiness
    assert readiness["readiness_score"] >= 80

    with tempfile.TemporaryDirectory() as tmpdir:
        out_zip = os.path.join(tmpdir, "test_manuscript.zip")
        res = engine.export_submission_package(
            title="Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection",
            authors=["A. Vance", "E. Rostova"],
            abstract="Synthetic Aperture Radar multitemporal change detection...",
            keywords=["SAR", "Sentinel-1", "Change Detection"],
            sections={"introduction": "Intro text...", "methodology": "Methods...", "results": "Results...", "conclusion": "Conclusion..."},
            references=[{"authors": "A. Author", "title": "SAR Analysis", "year": 2024, "doi": "10.1109/TGRS.2023.3241567"}],
            hyperparameters={"lr": 0.0003},
            metrics={"f1_score": 0.884, "iou": 0.795},
            output_zip_path=out_zip
        )
        assert res["status"] == "SUCCESS"
        assert os.path.exists(res["package_path"])


# ── 8. FiftyOne SAR Visualizer ───────────────────────────────────────────────
def test_fiftyone_sar_visualizer():
    vis = FiftyOneSARVisualizer()
    summary = vis.get_dataset_inspection_summary("Sentinel-1 SAR Benchmark")
    assert summary["total_samples"] == 12
    assert "agreement_summary" in summary
    assert "quality_audit" in summary

    session_info = vis.launch_or_connect_session(port=5151)
    assert "status" in session_info
    assert "url" in session_info


# ── 9. System Monitoring & Prometheus Telemetry ──────────────────────────────
@pytest.mark.asyncio
async def test_system_monitoring_service():
    monitor = SystemMonitoringService()
    health = await monitor.check_full_health()
    assert health["status"] in ("HEALTHY", "DEGRADED")
    assert "components" in health
    assert "fastapi" in health["components"]
    assert "database" in health["components"]
    assert "redis" in health["components"]

    jobs = monitor.get_job_metrics()
    assert jobs["jobs_completed"] >= 0

    prom_text = monitor.generate_prometheus_metrics(health, jobs)
    assert "researchos_uptime_seconds" in prom_text
    assert "researchos_jobs_completed_total" in prom_text
    assert "researchos_celery_queue_depth" in prom_text
