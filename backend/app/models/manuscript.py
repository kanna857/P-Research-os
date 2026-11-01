from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Manuscript(Base):
    __tablename__ = "manuscripts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sections: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    template: Mapped[str | None] = mapped_column(String(100), default="ieee", nullable=True)
    references: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="manuscripts", lazy="selectin")


class Reference(Base):
    __tablename__ = "references"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    authors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    doi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    venue: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bibtex: Mapped[str | None] = mapped_column(Text, nullable=True)
    ris: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_paper_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("papers.id", use_alter=True), nullable=True
    )
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="references", lazy="selectin")
    source_paper: Mapped["Paper | None"] = relationship(back_populates="references", lazy="selectin")
