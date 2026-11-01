"""
Unit and integration tests for ResearchOS API endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ResearchOS Backend"}


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "ResearchOS API" in response.json()["name"]


@pytest.mark.asyncio
async def test_model_library(client):
    response = await client.get("/api/models/library")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    model_names = [m["name"] for m in data]
    assert any("Siamese U-Net" in name for name in model_names)
    assert any("ResNet" in name for name in model_names)


@pytest.mark.asyncio
async def test_diagram_templates(client):
    response = await client.get("/api/diagrams/templates")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) >= 2


@pytest.mark.asyncio
async def test_scientific_evaluation(client):
    response = await client.get("/api/evaluation/model/Siamese U-Net")
    assert response.status_code == 200
    eval_data = response.json()
    assert "metrics" in eval_data
    assert "confusion_matrix" in eval_data
    assert "roc_curve" in eval_data
    assert eval_data["metrics"]["test_accuracy"] >= 0.90


@pytest.mark.asyncio
async def test_academic_rewrite(client):
    response = await client.post(
        "/api/manuscripts/rewrite",
        json={"text": "It can be observed from the experimental findings that the model works well.", "tone": "concise"},
    )
    assert response.status_code == 200
    res = response.json()
    assert "rewritten_text" in res
    assert res["selected_tone"] == "concise"

