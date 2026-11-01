from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    license: Mapped[str | None] = mapped_column(String(255), nullable=True)
    total_samples: Mapped[int | None] = mapped_column(Integer, nullable=True)
    classes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    image_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    channels: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_format: Mapped[str | None] = mapped_column(String(50), nullable=True)
    download_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    local_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="registered", nullable=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="datasets", lazy="selectin")
    processed_datasets: Mapped[list["ProcessedDataset"]] = relationship(
        back_populates="dataset", lazy="selectin"
    )


class ProcessedDataset(Base):
    __tablename__ = "processed_datasets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(Integer, ForeignKey("datasets.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    train_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    test_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    dataset: Mapped["Dataset"] = relationship(back_populates="processed_datasets", lazy="selectin")
    project: Mapped["Project"] = relationship(lazy="selectin")
