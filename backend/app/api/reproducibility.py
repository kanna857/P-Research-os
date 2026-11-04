"""
API endpoints for Scientific Reproducibility, Manifest Generation, and One-Click Experiment Reproduction.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import tempfile
import os

from app.integrations.research.reproducibility_engine import ScientificReproducibilityEngine

router = APIRouter()
repro_engine = ScientificReproducibilityEngine()


class ManifestGenerateRequest(BaseModel):
    experiment_id: str = Field(..., description="Unique experiment ID")
    project_name: str = Field(..., description="Project name")
    hyperparameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    dataset_name: Optional[str] = "Sentinel-1 SAR Change Detection Benchmark"
    random_seed: Optional[int] = 42
    model_name: Optional[str] = "ResNet-Siamese-DualPol"


class ReproduceRequest(BaseModel):
    manifest: Dict[str, Any]


@router.post("/manifest")
async def generate_manifest_endpoint(req: ManifestGenerateRequest):
    """Generate a complete scientific reproducibility manifest."""
    hparams = req.hyperparameters or {
        "learning_rate": 0.0003,
        "batch_size": 16,
        "epochs": 50,
        "optimizer": "AdamW",
        "loss": "Focal-Dice Composite (gamma=2.0)"
    }
    metrics = req.metrics or {
        "f1_score": 0.884,
        "iou": 0.795,
        "accuracy": 0.945,
        "precision": 0.892,
        "recall": 0.876
    }
    manifest = repro_engine.generate_manifest(
        experiment_id=req.experiment_id,
        project_name=req.project_name,
        hyperparameters=hparams,
        metrics=metrics,
        dataset_name=req.dataset_name or "Sentinel-1 SAR Change Detection Benchmark",
        random_seed=req.random_seed or 42,
        model_name=req.model_name or "ResNet-Siamese-DualPol"
    )
    return manifest


@router.post("/package")
async def export_package_endpoint(req: ManifestGenerateRequest):
    """Build and return downloadable reproducibility package ZIP."""
    manifest = await generate_manifest_endpoint(req)
    temp_zip = os.path.join(tempfile.gettempdir(), f"reproducibility_{req.experiment_id}.zip")
    pkg_path = repro_engine.create_reproducibility_package(manifest, temp_zip)

    if not os.path.exists(pkg_path):
        raise HTTPException(status_code=500, detail="Failed to create reproducibility package")

    return FileResponse(
        pkg_path,
        media_type="application/zip",
        filename=f"reproducibility_package_{req.experiment_id}.zip"
    )


@router.post("/reproduce")
async def reproduce_endpoint(req: ReproduceRequest):
    """
    Rerun experiment pipeline with identical parameters and verify metric parity.
    """
    return repro_engine.reproduce_experiment(req.manifest)
