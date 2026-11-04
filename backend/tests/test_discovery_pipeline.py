"""
Automated Tests for Free-First Autonomous Research Paper & Dataset Discovery Engine.
Verifies Query Expander, Federated Search, Free-First API Manager, Paper-to-Dataset Linker,
Download Manager, and Orchestrator.
"""

import pytest
import os
import asyncio
from fastapi.testclient import TestClient

from app.integrations.discovery.query_expander import query_expander
from app.integrations.discovery.free_api_manager import free_api_manager
from app.integrations.discovery.paper_dataset_linker import paper_dataset_linker
from app.integrations.discovery.download_manager import download_manager
from app.integrations.discovery.autonomous_discovery import autonomous_discovery_engine
from app.main import app

client = TestClient(app)


def test_query_expander_sar_domain():
    """Verify topic understanding, keyword expansion, and candidate benchmark detection."""
    topic = "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection"
    plan = query_expander.expand_topic(topic)

    assert plan["cleaned_topic"] is not None
    assert len(plan["paper_queries"]) >= 2
    # Domain expansions
    queries_joined = " ".join(plan["paper_queries"]).lower()
    assert "sentinel-1" in queries_joined or "sar" in queries_joined or "change detection" in queries_joined
    # Candidate benchmark datasets detected
    benchmarks = plan["candidate_benchmarks"]
    assert any("spacenet" in b.lower() or "oscd" in b.lower() or "sentinel-1" in b.lower() for b in benchmarks)


def test_free_api_manager_policy_and_profiles():
    """Verify free-first policy guarantees: no billable APIs, exactly 20 open providers."""
    providers = free_api_manager.list_providers()
    assert len(providers) >= 20

    # Ensure all are free-first
    for p in providers:
        assert p.get("is_free") is True

    # Free quota guarantees
    policy = free_api_manager.get_policy_summary()
    assert policy["FREE_ONLY_MODE"] is True
    assert policy["ENABLE_PAID_APIS"] is False
    assert policy["AUTO_PURCHASE_CREDITS"] is False
    assert policy["billable_requests_blocked"] is True


def test_free_api_live_ping():
    """Test ping capability on a public zero-auth provider (OpenAlex, arXiv, or Zenodo)."""
    res = asyncio.run(free_api_manager.test_provider("zenodo"))
    assert res["provider_id"] == "zenodo"
    assert res["status"] in ["connected", "healthy"] or "http" in res["status"]


def test_paper_dataset_linker_benchmark_classification():
    """
    Verify paper-to-dataset linker extracts benchmarks from paper abstracts
    and correctly categorizes labeled benchmarks vs raw sensor imagery.
    """
    papers = [
        {
            "id": "openalex:W123456",
            "title": "Dual-Temporal Siamese Transformers for Multitemporal SAR Change Detection",
            "abstract": "We evaluate our framework on the OSCD dataset and SpaceNet 6 benchmark, comparing with raw Sentinel-1 GRD imagery baselines.",
            "url": "https://doi.org/10.1109/TGRS.2023.12345",
            "doi": "10.1109/TGRS.2023.12345",
            "year": 2023,
            "is_open_access": True,
        }
    ]

    res = asyncio.run(paper_dataset_linker.link_papers_and_datasets(papers))
    assert res["total_connections"] >= 1

    connections = res["connections"]
    dataset_names = [c["dataset_name"] for c in connections]
    assert any("OSCD" in name or "SpaceNet" in name or "Sentinel-1 GRD" in name for name in dataset_names)

    # OSCD or SpaceNet should be labeled benchmark
    labeled = [c for c in connections if "OSCD" in c["dataset_name"] or "SpaceNet" in c["dataset_name"]]
    if labeled:
        assert labeled[0]["is_labeled_benchmark"] is True


def test_download_manager_storage_and_checksum(tmp_path):
    """Verify download manager computes SHA-256 and records metadata."""
    sample_url = "https://raw.githubusercontent.com/kanna857/P-Research-os/main/README.md"
    record = asyncio.run(download_manager.download_file(
        url=sample_url,
        title="Test README",
        asset_type="paper_pdf",
        project_id=1,
    ))

    assert record["asset_id"] is not None
    assert record["title"] == "Test README"
    assert record["sha256_checksum"] is not None
    assert len(record["sha256_checksum"]) == 64


def test_autonomous_discovery_orchestrator():
    """Verify 12-step autonomous discovery execution for Sentinel-1 SAR change detection."""
    topic = "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection"
    result = asyncio.run(autonomous_discovery_engine.execute_autonomous_discovery(
        topic=topic,
        project_id=1,
        max_papers_per_source=2,
        max_datasets_per_source=2,
        open_access_only=False,
    ))

    assert result["topic"] == topic
    assert "summary" in result
    assert result["summary"]["total_papers_found"] >= 1
    assert result["summary"]["total_datasets_found"] >= 1
    assert "query_expansion" in result
    assert "downstream_ready" in result
    assert result["free_policy"]["FREE_ONLY_MODE"] is True


def test_discovery_api_routes():
    """Verify REST endpoints for discovery management."""
    # List APIs
    res = client.get("/api/discovery/apis")
    assert res.status_code == 200
    data = res.json()
    assert "providers" in data
    assert len(data["providers"]) >= 20

    # Get Discovery Stats
    res = client.get("/api/discovery/stats")
    assert res.status_code == 200
    stats = res.json()
    assert "policy" in stats
    assert stats["policy"]["FREE_ONLY_MODE"] is True

    # Test single API endpoint
    res = client.post("/api/discovery/apis/zenodo/test")
    assert res.status_code == 200
    ping_data = res.json()
    assert ping_data["provider_id"] == "zenodo"
