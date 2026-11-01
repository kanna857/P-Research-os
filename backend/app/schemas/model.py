"""Model-related Pydantic v2 schemas for model management, training, and experiments."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ModelFamily(BaseModel):
    """Schema describing a model family and its available architectures."""

    name: str = Field(
        ...,
        description="Model family name",
        examples=["resnet", "efficientnet", "vit"],
    )
    architectures: list[str] = Field(
        ...,
        description="Available architecture variants",
        examples=[["resnet18", "resnet34", "resnet50", "resnet101"]],
    )
    description: str | None = Field(
        default=None,
        description="Description of the model family",
        examples=["Residual Networks for image classification"],
    )
    supports_pretrained: bool = Field(
        default=True,
        description="Whether pretrained weights are available",
    )


class ModelCreate(BaseModel):
    """Schema for adding a model to a project."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Model display name",
        examples=["ResNet50 Brain Tumor Classifier"],
    )
    family: str = Field(
        ...,
        description="Model family",
        examples=["resnet", "efficientnet", "vit"],
    )
    architecture: str | None = Field(
        default=None,
        description="Specific architecture variant",
        examples=["resnet50"],
    )
    config: dict | None = Field(
        default=None,
        description="Custom model configuration overrides",
        examples=[{"num_classes": 4, "dropout": 0.3}],
    )
    pretrained: bool = Field(
        default=True,
        description="Use pretrained weights (e.g. ImageNet)",
    )
    project_id: int = Field(..., description="Associated project ID")


class ModelResponse(BaseModel):
    """Schema for model data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique model identifier")
    project_id: int = Field(..., description="Associated project ID")
    name: str = Field(..., description="Model display name")
    family: str = Field(..., description="Model family")
    architecture: str | None = Field(default=None, description="Architecture variant")
    config: dict | None = Field(default=None, description="Model configuration")
    code_path: str | None = Field(
        default=None, description="Path to generated model code"
    )
    pretrained: bool = Field(default=True, description="Using pretrained weights")
    status: str = Field(
        default="created",
        description="Model status",
        examples=["created", "ready", "training", "trained", "failed"],
    )
    created_at: datetime = Field(..., description="Record creation timestamp")


class TrainingConfig(BaseModel):
    """Schema for configuring a training job."""

    model_id: int = Field(..., description="Model to train")
    dataset_id: int = Field(..., description="Dataset to train on")
    project_id: int = Field(..., description="Associated project ID")
    epochs: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Number of training epochs",
    )
    batch_size: int = Field(
        default=32,
        ge=1,
        le=512,
        description="Training batch size",
    )
    learning_rate: float = Field(
        default=0.001,
        gt=0,
        le=1.0,
        alias="lr",
        description="Initial learning rate",
    )
    optimizer: str = Field(
        default="adam",
        description="Optimizer algorithm",
        examples=["adam", "sgd", "adamw", "rmsprop"],
    )
    scheduler: str | None = Field(
        default=None,
        description="Learning rate scheduler",
        examples=["cosine", "step", "reduce_on_plateau"],
    )
    loss: str = Field(
        default="cross_entropy",
        description="Loss function",
        examples=["cross_entropy", "focal_loss", "bce"],
    )
    resolution: list[int] | None = Field(
        default=[224, 224],
        min_length=2,
        max_length=2,
        description="Input image resolution [height, width]",
    )
    seed: int = Field(default=42, description="Random seed for reproducibility")
    use_optuna: bool = Field(
        default=False,
        description="Enable Optuna hyperparameter optimization",
    )
    optuna_trials: int = Field(
        default=20,
        ge=1,
        le=500,
        description="Number of Optuna trials to run",
    )

    model_config = ConfigDict(populate_by_name=True)


class TrainingJobResponse(BaseModel):
    """Schema for training job data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique training job identifier")
    project_id: int = Field(..., description="Associated project ID")
    model_id: int = Field(..., description="Model being trained")
    dataset_id: int = Field(..., description="Dataset used for training")
    config: dict | None = Field(default=None, description="Training configuration")
    status: str = Field(
        default="queued",
        description="Job status",
        examples=["queued", "running", "completed", "failed", "cancelled"],
    )
    current_epoch: int | None = Field(
        default=None, description="Current epoch in progress"
    )
    total_epochs: int | None = Field(default=None, description="Total epochs planned")
    metrics: dict | None = Field(
        default=None,
        description="Latest training metrics",
        examples=[{"accuracy": 0.95, "loss": 0.12, "f1": 0.94}],
    )
    checkpoint_path: str | None = Field(
        default=None, description="Path to best model checkpoint"
    )
    logs_path: str | None = Field(
        default=None, description="Path to training logs directory"
    )
    started_at: datetime | None = Field(
        default=None, description="Training start timestamp"
    )
    finished_at: datetime | None = Field(
        default=None, description="Training completion timestamp"
    )
    created_at: datetime = Field(..., description="Record creation timestamp")


class ExperimentResponse(BaseModel):
    """Schema for experiment tracking data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique experiment identifier")
    project_id: int = Field(..., description="Associated project ID")
    training_job_id: int = Field(..., description="Linked training job ID")
    name: str = Field(..., description="Experiment name")
    metrics: dict | None = Field(
        default=None,
        description="Final experiment metrics",
        examples=[{"accuracy": 0.96, "precision": 0.95, "recall": 0.94, "f1": 0.945}],
    )
    artifacts: dict | None = Field(
        default=None,
        description="Paths to experiment artifacts (confusion matrix, plots, etc.)",
    )
    comparison_group: str | None = Field(
        default=None,
        description="Group label for comparing related experiments",
        examples=["baseline_comparison"],
    )
    created_at: datetime = Field(..., description="Record creation timestamp")


class ModelCompareRequest(BaseModel):
    """Schema for requesting a comparison between experiments."""

    experiment_ids: list[int] = Field(
        ...,
        min_length=2,
        description="IDs of experiments to compare",
    )
    metrics: list[str] | None = Field(
        default=None,
        description="Specific metrics to compare",
        examples=[["accuracy", "f1", "loss"]],
    )


class ModelCompareResponse(BaseModel):
    """Schema for experiment comparison results."""

    experiments: list[dict] = Field(
        ..., description="Summary of each experiment in the comparison"
    )
    comparison: dict = Field(
        ...,
        description="Aggregated comparison data (rankings, deltas, best model)",
    )
