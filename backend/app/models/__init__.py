"""ResearchOS SQLAlchemy models package.

All models are imported here so they are registered with Base.metadata
when this package is imported.
"""

from app.models.user import User
from app.models.project import Project
from app.models.paper import Paper
from app.models.dataset import Dataset, ProcessedDataset
from app.models.model import MLModel, TrainingJob, Experiment
from app.models.manuscript import Manuscript, Reference
from app.models.diagram import Diagram

__all__ = [
    "User",
    "Project",
    "Paper",
    "Dataset",
    "ProcessedDataset",
    "MLModel",
    "TrainingJob",
    "Experiment",
    "Manuscript",
    "Reference",
    "Diagram",
]
