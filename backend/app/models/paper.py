from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), index=True, nullable=False)
    authors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    doi: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    venue: Mapped[str | None] = mapped_column(String(500), nullable=True)
    citation_count: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pdf_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    pdf_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_open_access: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    download_status: Mapped[str | None] = mapped_column(String(50), default="pending", nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="papers", lazy="selectin")
    references: Mapped[list["Reference"]] = relationship(back_populates="source_paper", lazy="selectin")
