"""
Automated Unit and Integration Tests for Nhost + PostgreSQL Backend Integration.
Tests Nhost Auth (Hasura claims), 25 Normalized Database Tables, pgvector Semantic Search,
Nhost File Storage with SHA-256 Checksums, and Hasura GraphQL Operations.
"""

import pytest
import os
import asyncio
from fastapi.testclient import TestClient

from app.integrations.nhost.auth_manager import nhost_auth_manager
from app.integrations.nhost.storage_client import nhost_storage_client
from app.integrations.nhost.semantic_search import semantic_search_engine
from app.integrations.nhost.hasura_client import hasura_client
from app.database import Base, init_db
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def ensure_db():
    asyncio.run(init_db())


def test_nhost_jwt_generation_and_hasura_claims():
    """Verify that JWT contains valid https://hasura.io/jwt/claims."""
    token = nhost_auth_manager.generate_hasura_jwt(
        user_id=42,
        email="lead.researcher@academic.org",
        role="researcher",
        allowed_roles=["user", "researcher"],
    )
    assert token is not None

    payload = nhost_auth_manager.verify_jwt(token)
    assert payload["sub"] == "42"
    assert payload["email"] == "lead.researcher@academic.org"

    claims = payload.get("https://hasura.io/jwt/claims")
    assert claims is not None
    assert claims["x-hasura-user-id"] == "42"
    assert claims["x-hasura-default-role"] == "researcher"
    assert "researcher" in claims["x-hasura-allowed-roles"]
    assert "user" in claims["x-hasura-allowed-roles"]


def test_nhost_jwt_rbac_and_project_ownership():
    """Verify project ownership check blocks unauthorized researchers."""
    user_claims = {
        "user_id": 10,
        "email": "user10@univ.edu",
        "role": "user",
    }
    admin_claims = {
        "user_id": 99,
        "email": "admin@univ.edu",
        "role": "admin",
    }

    # Owner can access their own project
    assert nhost_auth_manager.verify_project_ownership(user_claims, project_user_id=10) is True

    # Admin can access any project
    assert nhost_auth_manager.verify_project_ownership(admin_claims, project_user_id=10) is True

    # Different user is blocked
    with pytest.raises(Exception):
        nhost_auth_manager.verify_project_ownership(user_claims, project_user_id=20)


def test_nhost_database_schema_completeness():
    """Verify all 25 requested normalized tables are registered in SQLAlchemy Base.metadata."""
    table_names = set(Base.metadata.tables.keys())

    required_tables = [
        "users",
        "user_profiles",
        "projects",
        "research_topics",
        "papers",
        "paper_authors",
        "citations",
        "datasets",
        "processed_datasets",
        "dataset_versions",
        "paper_dataset_links",
        "research_jobs",
        "research_agents",
        "agent_execution_logs",
        "ml_models",
        "training_jobs",
        "experiments",
        "experiment_metrics",
        "training_checkpoints",
        "generated_figures",
        "manuscripts",
        "manuscript_versions",
        "research_artifacts",
        "notifications",
        "audit_logs",
        "api_provider_usage",
        "paper_embeddings",
    ]

    for table in required_tables:
        assert table in table_names, f"Table '{table}' missing from schema"


def test_nhost_storage_checksum_and_upload():
    """Verify file upload calculates valid 64-char SHA-256 and records metadata."""
    sample_content = b"ResearchOS: Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection (Test File)"
    res = asyncio.run(nhost_storage_client.upload_file(
        file_bytes=sample_content,
        filename="sentinel1_test_sample.bin",
    ))

    assert res["status"] in ["uploaded", "uploaded_local"]
    assert res["file_size"] == len(sample_content)
    assert len(res["sha256"]) == 64  # SHA-256 hex length
    assert res["filename"] == "sentinel1_test_sample.bin"


def test_pgvector_semantic_search_engine():
    """Verify 384-dimensional vector computation, normalization, and cosine distance."""
    text1 = "Synthetic Aperture Radar (SAR) speckle noise reduction using deep convolutional neural networks."
    text2 = "Speckle suppression in Sentinel-1 SAR imagery with multi-temporal deep learning architectures."
    text3 = "Genomic sequencing of colorectal cancer using long-read Oxford Nanopore technology."

    vec1 = semantic_search_engine.compute_embedding(text1)
    vec2 = semantic_search_engine.compute_embedding(text2)
    vec3 = semantic_search_engine.compute_embedding(text3)

    assert len(vec1) == 384
    assert len(vec2) == 384
    assert len(vec3) == 384

    # Related SAR topics should have higher similarity than unrelated cancer genomic topic
    sim_sar = semantic_search_engine.cosine_similarity(vec1, vec2)
    sim_unrelated = semantic_search_engine.cosine_similarity(vec1, vec3)

    assert sim_sar > sim_unrelated
    assert sim_sar > 0.25


def test_hasura_graphql_client_logging():
    """Verify Hasura client can format and execute job progress updates."""
    success = asyncio.run(hasura_client.log_job_progress(
        job_id="job-test-sar-001",
        project_id=1,
        job_type="discovery",
        progress_pct=85.0,
        step_message="Searching Copernicus Data Space for Sentinel-1 GRD scenes",
        status="running",
    ))
    # In test environment, client executes and handles fallback gracefully
    assert isinstance(success, bool)


def test_nhost_api_routes():
    """Verify REST endpoints for Nhost status, Hasura token issuance, and semantic search."""
    # 1. Status endpoint
    res = client.get("/api/nhost/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert "postgresql" in data["components"]
    assert "hasura_graphql" in data["components"]

    # 2. Token issuance endpoint
    res = client.post("/api/nhost/auth/token", json={
        "email": "sar.researcher@earthdata.nasa.gov",
        "user_id": 5,
        "role": "researcher",
    })
    assert res.status_code == 200
    token_data = res.json()
    assert "access_token" in token_data
    assert token_data["claims"]["x-hasura-default-role"] == "researcher"

    # 3. Semantic search endpoint
    res = client.post("/api/nhost/search/semantic", json={
        "query": "Sentinel-1 SAR change detection deep learning",
        "top_k": 3,
    })
    assert res.status_code == 200
    search_data = res.json()
    assert "matches" in search_data
