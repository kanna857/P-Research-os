"""Dataset-related Pydantic v2 schemas for dataset search, inspection, and processing."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatasetSearch(BaseModel):
    """Schema for searching datasets from external repositories."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Search query for datasets",
        examples=["brain tumor MRI classification"],
    )
    source: str | None = Field(
        default="huggingface",
        description="Dataset repository to search",
        examples=["huggingface", "kaggle", "roboflow"],
    )
    task_type: str | None = Field(
        default=None,
        description="Filter by ML task type",
        examples=["image-classification", "object-detection", "text-classification"],
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results to return",
    )


class DatasetCreate(BaseModel):
    """Schema for adding a dataset to a project."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Dataset name",
        examples=["Brain Tumor MRI Dataset"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Dataset description",
    )
    source: str = Field(
        ...,
        description="Source repository",
        examples=["huggingface", "kaggle", "local"],
    )
    source_url: str | None = Field(
        default=None,
        description="URL to the dataset on its source platform",
        examples=["https://huggingface.co/datasets/brain-tumor-mri"],
    )
    project_id: int = Field(..., description="Associated project ID")


class DatasetResponse(BaseModel):
    """Schema for dataset data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique dataset identifier")
    project_id: int = Field(..., description="Associated project ID")
    name: str = Field(..., description="Dataset name")
    description: str | None = Field(default=None, description="Dataset description")
    source: str = Field(..., description="Source repository")
    source_url: str | None = Field(default=None, description="Source URL")
    license: str | None = Field(default=None, description="Dataset license")
    total_samples: int | None = Field(
        default=None, description="Total number of samples"
    )
    classes: list[str] | None = Field(default=None, description="Class label names")
    image_width: int | None = Field(default=None, description="Image width in pixels")
    image_height: int | None = Field(
        default=None, description="Image height in pixels"
    )
    channels: int | None = Field(
        default=None, description="Number of image channels (e.g. 3 for RGB)"
    )
    file_format: str | None = Field(
        default=None,
        description="Primary file format",
        examples=["png", "jpg", "parquet"],
    )
    download_size: str | None = Field(
        default=None, description="Human-readable download size"
    )
    local_path: str | None = Field(
        default=None, description="Local filesystem path after download"
    )
    status: str = Field(
        default="pending",
        description="Download / processing status",
        examples=["pending", "downloading", "ready", "failed"],
    )
    metadata_: dict | None = Field(
        default=None,
        alias="metadata_",
        description="Additional metadata from the source",
    )
    created_at: datetime = Field(..., description="Record creation timestamp")


class DatasetInspectionResponse(BaseModel):
    """Schema for dataset quality inspection results."""

    dataset_id: int = Field(..., description="Inspected dataset ID")
    total_samples: int = Field(..., ge=0, description="Total sample count")
    class_distribution: dict | None = Field(
        default=None,
        description="Distribution of samples across classes",
        examples=[{"glioma": 826, "meningioma": 822, "pituitary": 827, "no_tumor": 395}],
    )
    duplicate_count: int | None = Field(
        default=None, ge=0, description="Number of duplicate samples detected"
    )
    quality_issues: list[dict] | None = Field(
        default=None,
        description="List of quality issues found during inspection",
    )
    statistics: dict | None = Field(
        default=None,
        description="Summary statistics (mean, std, min/max dimensions, etc.)",
    )


class ProcessingConfig(BaseModel):
    """Schema for dataset preprocessing configuration."""

    resolution: list[int] | None = Field(
        default=[224, 224],
        min_length=2,
        max_length=2,
        description="Target image resolution [height, width]",
        examples=[[224, 224]],
    )
    normalization: dict | None = Field(
        default={"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]},
        description="Normalization parameters (ImageNet defaults)",
    )
    augmentation: dict | None = Field(
        default=None,
        description="Data augmentation configuration",
        examples=[{"horizontal_flip": True, "rotation": 15, "color_jitter": 0.2}],
    )
    split_ratio: float = Field(
        default=0.8,
        ge=0.5,
        le=0.95,
        description="Train split ratio (remainder goes to test/val)",
    )
    seed: int = Field(
        default=42,
        description="Random seed for reproducibility",
    )


class ProcessedDatasetResponse(BaseModel):
    """Schema for processed dataset data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique processed dataset identifier")
    dataset_id: int = Field(..., description="Source dataset ID")
    project_id: int = Field(..., description="Associated project ID")
    name: str = Field(..., description="Processed dataset name")
    config: dict | None = Field(
        default=None, description="Processing configuration used"
    )
    train_count: int | None = Field(
        default=None, description="Number of training samples"
    )
    test_count: int | None = Field(
        default=None, description="Number of test samples"
    )
    output_path: str | None = Field(
        default=None, description="Path to the processed dataset"
    )
    version: str | None = Field(
        default=None,
        description="Processing version identifier",
        examples=["v1.0"],
    )
    status: str = Field(
        default="pending",
        description="Processing status",
        examples=["pending", "processing", "completed", "failed"],
    )
    created_at: datetime = Field(..., description="Record creation timestamp")
