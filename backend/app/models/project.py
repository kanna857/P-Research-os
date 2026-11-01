from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_topic: Mapped[str | None] = mapped_column(String(500), nullable=True)
    keywords: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    target_journal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="projects", lazy="selectin")
    papers: Mapped[list["Paper"]] = relationship(back_populates="project", lazy="selectin")
    datasets: Mapped[list["Dataset"]] = relationship(back_populates="project", lazy="selectin")
    models: Mapped[list["MLModel"]] = relationship(back_populates="project", lazy="selectin")
    manuscripts: Mapped[list["Manuscript"]] = relationship(back_populates="project", lazy="selectin")
    diagrams: Mapped[list["Diagram"]] = relationship(back_populates="project", lazy="selectin")
    references: Mapped[list["Reference"]] = relationship(back_populates="project", lazy="selectin")
