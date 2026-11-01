"""
Model library, training execution, and experiment tracking API routes.
"""

from typing import List, Dict, Any, Optional
import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.model import MLModel, TrainingJob, Experiment
from app.schemas.model import ModelCreate, ModelResponse, TrainingConfig, TrainingJobResponse
from app.integrations.training.model_registry import get_available_model_families
from app.integrations.training.lightning_trainer import lightning_engine
from app.integrations.training.experiment_tracker import experiment_tracker
from app.integrations.training.optuna_tuner import optuna_tuner
from app.utils.websocket_manager import ws_manager

router = APIRouter()


@router.get("/library")
async def list_model_library():
    """Return all supported neural network families and architectures."""
    return get_available_model_families()


@router.get("/project/{project_id}")
async def get_project_models(project_id: int, db: AsyncSession = Depends(get_db)):
    """List models registered or configured in this project."""
    result = await db.execute(select(MLModel).where(MLModel.project_id == project_id))
    return result.scalars().all()


@router.post("/register")
async def register_model(data: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """Register selected model family or custom architecture in project."""
    model = MLModel(
        project_id=data.get("project_id", 1),
        name=data.get("name", "Siamese U-Net"),
        family=data.get("family", "Siamese U-Net"),
        architecture=data.get("architecture", "Dual-stream encoder with cross-temporal subtraction"),
        config=data.get("config", {}),
        code_path=data.get("code_path"),
        pretrained=data.get("pretrained", True),
        status="configured",
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


@router.post("/train")
async def start_training_job(
    config: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Launch PyTorch Lightning training job with live WebSocket progress.
    """
    project_id = config.get("project_id", 1)
    model_name = config.get("model_name", "Siamese U-Net")
    epochs = int(config.get("epochs", 10))
    batch_size = int(config.get("batch_size", 32))
    lr = float(config.get("learning_rate", 0.001))
    optimizer = config.get("optimizer", "AdamW")

    job = TrainingJob(
        project_id=project_id,
        model_id=config.get("model_id", 1),
        dataset_id=config.get("dataset_id", 1),
        config=config,
        status="running",
        current_epoch=1,
        total_epochs=epochs,
        metrics={},
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # Define training background runner
    async def run_training_background(job_id: int):
        async def on_progress(update: Dict[str, Any]):
            # Broadcast to real-time WebSockets
            await ws_manager.broadcast({
                "type": "TRAINING_PROGRESS",
                "data": update,
            }, channel=f"project-{project_id}")

        train_result = await lightning_engine.run_training(
            job_id=job_id,
            model_name=model_name,
            epochs=epochs,
            batch_size=batch_size,
            lr=lr,
            optimizer_name=optimizer,
            progress_callback=on_progress,
        )

        # Log to MLflow and ClearML
        experiment_tracker.log_experiment(
            experiment_name=f"{model_name}-Run",
            params=config,
            metrics=train_result["final_metrics"],
        )

        await ws_manager.broadcast({
            "type": "TRAINING_COMPLETED",
            "job_id": job_id,
            "metrics": train_result["final_metrics"],
        }, channel=f"project-{project_id}")

    # Launch non-blocking background task
    asyncio.create_task(run_training_background(job.id))

    return {
        "job_id": job.id,
        "status": "running",
        "model_name": model_name,
        "epochs": epochs,
        "message": "PyTorch Lightning training worker initiated in background.",
    }


@router.get("/train/{job_id}")
async def get_training_status(job_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve current training job telemetry and checkpoint info."""
    result = await db.execute(select(TrainingJob).where(TrainingJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Training job not found")
    return job


@router.post("/optimize-hyperparameters")
async def optimize_hyperparameters(config: Dict[str, Any]):
    """Execute Optuna Bayesian hyperparameter search study."""
    model_name = config.get("model_name", "Siamese U-Net")
    n_trials = int(config.get("trials", 5))
    result = optuna_tuner.run_study(model_name=model_name, n_trials=n_trials)
    return result

