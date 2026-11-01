"""
Dataset discovery, inspection, preprocessing, and 80/20 partitioning API routes.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.dataset import Dataset, ProcessedDataset
from app.schemas.dataset import DatasetCreate, DatasetResponse, ProcessingConfig, ProcessedDatasetResponse
from app.integrations.datasets.hf_datasets_client import hf_datasets_client
from app.integrations.datasets.fiftyone_inspector import fiftyone_inspector
from app.integrations.preprocessing.split_manager import preprocessing_split_manager
from app.integrations.preprocessing.dvc_tracker import dvc_tracker
from app.utils.storage import storage_manager

router = APIRouter()


@router.post("/search")
async def search_datasets(query: str = Form(""), limit: int = Form(20)):
    """Search scientific datasets across Hugging Face Hub, Zenodo, and remote sensing archives."""
    results = await hf_datasets_client.search_datasets(query=query, limit=limit)
    return results


@router.get("/project/{project_id}")
async def get_project_datasets(project_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve datasets linked to project."""
    result = await db.execute(select(Dataset).where(Dataset.project_id == project_id).order_by(Dataset.created_at.desc()))
    return result.scalars().all()


@router.post("/register")
async def register_dataset(data: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """Register an imported dataset with project workspace."""
    dataset = Dataset(
        project_id=data.get("project_id", 1),
        name=data.get("name", "Sentinel-1 SAR Benchmark"),
        description=data.get("description", "Multitemporal SAR change detection dataset"),
        source=data.get("source", "Copernicus / Zenodo"),
        source_url=data.get("source_url"),
        license=data.get("license", "CC-BY-4.0"),
        total_samples=data.get("total_samples", 2500),
        classes=data.get("classes", ["Unchanged", "Changed"]),
        image_width=256,
        image_height=256,
        channels=data.get("channels", 2),
        file_format=data.get("file_format", "GeoTIFF / PNG"),
        download_size=data.get("download_size", "2.4 GB"),
        status="registered",
        dataset_metadata=data,
    )
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    return dataset


@router.post("/{dataset_id}/inspect")
async def inspect_dataset(dataset_id: int, db: AsyncSession = Depends(get_db)):
    """Run FiftyOne, Cleanlab, and CleanVision quality inspection on dataset."""
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    inspection = fiftyone_inspector.inspect_dataset_directory(
        dataset.local_path or f"storage/datasets/{dataset.name}"
    )

    dataset.dataset_metadata = {**(dataset.dataset_metadata or {}), "cleanlab_inspection": inspection}
    await db.commit()
    return inspection


@router.post("/{dataset_id}/process")
async def process_dataset(
    dataset_id: int,
    config: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """
    Execute preprocessing pipeline:
    - Target resolution (128x128, 224x224, 256x256, 512x512)
    - Normalization and data augmentations
    - MANDATORY 80% Train / 20% Test partition
    - Validation is strictly restricted to training folds
    - DVC manifest tracking
    """
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    res_str = config.get("resolution", "256x256")
    try:
        w, h = map(int, res_str.split("x"))
    except Exception:
        w, h = 256, 256

    output_dir = f"storage/processed_datasets/{dataset.id}_{w}x{h}"
    manifest = preprocessing_split_manager.process_dataset(
        raw_dataset_path=dataset.local_path or f"storage/datasets/{dataset.id}",
        output_dir=output_dir,
        target_resolution=(w, h),
        normalize=config.get("normalize", True),
        apply_augmentation=config.get("apply_augmentation", True),
        train_ratio=0.80,  # Enforce 80/20 default split
    )

    dvc_info = dvc_tracker.create_dvc_manifest(output_dir, version=f"v{dataset.id}.0")

    processed = ProcessedDataset(
        dataset_id=dataset.id,
        project_id=dataset.project_id,
        name=f"{dataset.name} (Processed {w}x{h} - 80/20)",
        config=config,
        train_count=manifest["statistics"]["train_samples"],
        test_count=manifest["statistics"]["test_samples"],
        output_path=output_dir,
        version="v1.0-dvc",
        status="completed",
    )
    db.add(processed)
    await db.commit()
    await db.refresh(processed)

    return {
        "processed_dataset": processed,
        "manifest": manifest,
        "dvc_manifest": dvc_info,
    }


@router.get("/{dataset_id}/processed")
async def list_processed_datasets(dataset_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all processed versions and manifests for dataset."""
    result = await db.execute(select(ProcessedDataset).where(ProcessedDataset.dataset_id == dataset_id))
    return result.scalars().all()

