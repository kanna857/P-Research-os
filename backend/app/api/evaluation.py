"""
Scientific evaluation, confusion matrices, ROC/PR curves, and multi-model benchmarking API routes.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.integrations.evaluation.scientific_evaluator import scientific_evaluator

router = APIRouter()


@router.get("/model/{model_name}")
async def get_model_evaluation(model_name: str, task: str = Query("classification")):
    """Compute complete scientific evaluation suite on held-out 20% test set."""
    report = scientific_evaluator.evaluate_model(model_name=model_name, task_type=task)
    return report


@router.post("/compare")
async def compare_models(data: Dict[str, Any]):
    """
    Generate unified multi-model comparison leaderboard and comparative charts.
    """
    models = data.get("models") or [
        "Proposed Siamese U-Net",
        "ResNet-50 Baseline",
        "Standard U-Net",
        "Swin Transformer (Tiny)",
        "MobileNetV3-Large",
    ]
    comparison = scientific_evaluator.generate_multi_model_comparison(models)
    return comparison


@router.get("/metrics/{job_id}")
async def get_job_metrics(job_id: int):
    """Retrieve detailed numerical metrics for an executed training job."""
    return scientific_evaluator.evaluate_model(model_name="Siamese U-Net")

