from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Diagram(Base):
    __tablename__ = "diagrams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    diagram_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    format: Mapped[str | None] = mapped_column(String(50), default="mermaid", nullable=True)
    svg_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    png_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    pdf_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="diagrams", lazy="selectin")
