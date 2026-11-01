from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MLModel(Base):
    __tablename__ = "ml_models"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    family: Mapped[str | None] = mapped_column(String(100), nullable=True)
    architecture: Mapped[str | None] = mapped_column(String(255), nullable=True)
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    code_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    pretrained: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="registered", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="models", lazy="selectin")
    training_jobs: Mapped[list["TrainingJob"]] = relationship(back_populates="model", lazy="selectin")


class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("ml_models.id"), nullable=False)
    dataset_id: Mapped[int] = mapped_column(Integer, ForeignKey("processed_datasets.id"), nullable=False)
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="queued", nullable=False)
    current_epoch: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    total_epochs: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    checkpoint_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    logs_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(lazy="selectin")
    model: Mapped["MLModel"] = relationship(back_populates="training_jobs", lazy="selectin")
    dataset: Mapped["ProcessedDataset"] = relationship(lazy="selectin")
    experiments: Mapped[list["Experiment"]] = relationship(back_populates="training_job", lazy="selectin")


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    training_job_id: Mapped[int] = mapped_column(Integer, ForeignKey("training_jobs.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    artifacts: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    comparison_group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(lazy="selectin")
    training_job: Mapped["TrainingJob"] = relationship(back_populates="experiments", lazy="selectin")
