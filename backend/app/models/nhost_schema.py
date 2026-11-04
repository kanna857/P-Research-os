"""
Nhost + PostgreSQL Schema Models for ResearchOS.
Enriches the research platform with normalized tables for multi-user isolation,
audit logging, research jobs, agent execution, training metrics, paper embeddings,
manuscript versions, and API provider tracking.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import json

from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    func,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator

from app.database import Base

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False


class FlexibleVector(TypeDecorator):
    """
    PostgreSQL pgvector Vector type when on Postgres,
    with JSON/Text fallback when running on SQLite for unit tests.
    """
    impl = Text
    cache_ok = True

    def __init__(self, dim: int = 384, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dim = dim

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql" and HAS_PGVECTOR:
            return dialect.type_descriptor(Vector(self.dim))
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, (list, tuple)):
            if dialect.name == "postgresql" and HAS_PGVECTOR:
                return value
            return json.dumps(list(value))
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return value
        return value


# ── 1. User Profiles & Research Metadata ──────────────────────────────────────
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    institution: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    orcid: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    research_interests: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    h_index: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False)  # user, admin, researcher
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


# ── 2. Research Topics ─────────────────────────────────────────────────────────
class ResearchTopic(Base):
    __tablename__ = "research_topics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    topic_title: Mapped[str] = mapped_column(String(500), nullable=False)
    domain_tags: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    expanded_queries: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


# ── 3. Paper Authors & Citation Graph ─────────────────────────────────────────
class PaperAuthor(Base):
    __tablename__ = "paper_authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    affiliation: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    orcid: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    author_order: Mapped[int] = mapped_column(Integer, default=1)


class Citation(Base):
    __tablename__ = "citations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    citation_text: Mapped[str] = mapped_column(Text, nullable=False)
    doi: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    context_snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


# ── 4. Dataset Versions & Paper-to-Dataset Links ──────────────────────────────
class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    version_tag: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "v1.0-80-20-split"
    sample_count: Mapped[int] = mapped_column(Integer, default=0)
    train_count: Mapped[int] = mapped_column(Integer, default=0)
    test_count: Mapped[int] = mapped_column(Integer, default=0)
    split_strategy: Mapped[str] = mapped_column(String(100), default="80_20_stratified_non_leaking")
    storage_uri: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    sha256_manifest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class PaperDatasetLink(Base):
    """Bipartite connection linking paper to experimental dataset."""
    __tablename__ = "paper_dataset_links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    paper_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("papers.id", ondelete="SET NULL"), nullable=True)
    dataset_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True)
    paper_title: Mapped[str] = mapped_column(String(500), nullable=False)
    dataset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dataset_source: Mapped[Optional[str]] = mapped_column(String(100), default="scientific_repository")
    official_source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    is_labeled_benchmark: Mapped[bool] = mapped_column(Boolean, default=True)
    training_suitability: Mapped[str] = mapped_column(
        String(50), default="HIGH_TRAINING_READY"
    )  # HIGH_TRAINING_READY, RAW_OBSERVATIONS_ONLY, MODERATE_REQUIRES_ANNOTATION
    suitability_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.95)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


# ── 5. Autonomous Research Jobs & Agent Logs ──────────────────────────────────
class ResearchJob(Base):
    """Tracks asynchronous research tasks, background discovery, and model training."""
    __tablename__ = "research_jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # uuid or task_id
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    job_type: Mapped[str] = mapped_column(String(100), nullable=False)  # paper_discovery, dataset_download, training, etc.
    status: Mapped[str] = mapped_column(String(50), default="queued", index=True)  # queued, running, completed, failed, cancelled
    progress_pct: Mapped[float] = mapped_column(Float, default=0.0)
    current_step: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    retries_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result_payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class ResearchAgent(Base):
    """Tracks LangGraph multi-agent execution states."""
    __tablename__ = "research_agents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)  # literature_reviewer, gap_analyzer, etc.
    status: Mapped[str] = mapped_column(String(50), default="idle")
    current_perspective: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    memory_state: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class AgentExecutionLog(Base):
    """Step-by-step summarized logs from autonomous agents."""
    __tablename__ = "agent_execution_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job_id: Mapped[str] = mapped_column(String(64), ForeignKey("research_jobs.id", ondelete="CASCADE"), index=True)
    agent_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    step_name: Mapped[str] = mapped_column(String(255), nullable=False)
    log_level: Mapped[str] = mapped_column(String(20), default="INFO")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


# ── 6. Scientific Experiment Metrics & Checkpoints ─────────────────────────────
class ExperimentMetric(Base):
    """Time-series or epoch-by-epoch training metrics."""
    __tablename__ = "experiment_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    experiment_id: Mapped[int] = mapped_column(Integer, ForeignKey("experiments.id", ondelete="CASCADE"), index=True)
    epoch: Mapped[int] = mapped_column(Integer, nullable=False)
    step: Mapped[int] = mapped_column(Integer, default=0)
    train_loss: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    val_loss: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    accuracy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    precision: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    recall: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    f1_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    iou: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dice: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class TrainingCheckpoint(Base):
    """Saved PyTorch Lightning model weights."""
    __tablename__ = "training_checkpoints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    experiment_id: Mapped[int] = mapped_column(Integer, ForeignKey("experiments.id", ondelete="CASCADE"), index=True)
    epoch: Mapped[int] = mapped_column(Integer, nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    val_loss: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    val_f1: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sha256_checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


# ── 7. Scientific Figures & Manuscripts ───────────────────────────────────────
class GeneratedFigure(Base):
    """Saved scientific diagrams, ROC curves, confusion matrices, and React Flow visualizers."""
    __tablename__ = "generated_figures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    experiment_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("experiments.id", ondelete="SET NULL"), nullable=True)
    figure_type: Mapped[str] = mapped_column(String(100), nullable=False)  # confusion_matrix, roc_curve, architecture, flow_graph
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    nhost_file_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    format: Mapped[str] = mapped_column(String(20), default="png")  # png, svg, pdf
    sha256_checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class ManuscriptVersion(Base):
    """Versioned IEEE manuscript documents."""
    __tablename__ = "manuscript_versions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manuscript_id: Mapped[int] = mapped_column(Integer, ForeignKey("manuscripts.id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    latex_content: Mapped[Text] = mapped_column(Text, nullable=False)
    compiled_pdf_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    changelog: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


# ── 8. Research Artifacts, Notifications & Audit Logs ──────────────────────────
class ResearchArtifact(Base):
    """Persistent structured artifacts created during autonomous discovery and writing."""
    __tablename__ = "research_artifacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    artifact_name: Mapped[str] = mapped_column(String(255), nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(100), nullable=False)  # report, matrix, diff, experiment_log
    summary: Mapped[Text] = mapped_column(Text, nullable=False)
    file_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    user_facing: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class Notification(Base):
    """User notifications for background job completion, downloads, and training alerts."""
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(50), default="info")  # info, success, warning, error
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[Text] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class AuditLog(Base):
    """Security and compliance audit log for user actions and project modifications."""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)  # project_create, model_train, paper_download, etc.
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)  # project, paper, dataset, experiment
    entity_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class ApiProviderUsage(Base):
    """Monitors free-tier rate limits and connection statuses for all 20 external providers."""
    __tablename__ = "api_provider_usage"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # openalex, arxiv, kaggle, etc.
    provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # papers, datasets, crawlers
    is_free_tier: Mapped[bool] = mapped_column(Boolean, default=True)
    request_count: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    last_status: Mapped[str] = mapped_column(String(50), default="healthy")
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    quota_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


# ── 9. pgvector Semantic Paper Embeddings ──────────────────────────────────────
class PaperEmbedding(Base):
    """Vector embeddings of research paper abstracts and extracted methodology chunks."""
    __tablename__ = "paper_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    chunk_type: Mapped[str] = mapped_column(String(50), default="abstract")  # abstract, methodology, limitations, findings
    content_text: Mapped[Text] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[list]] = mapped_column(FlexibleVector(384), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_paper_embeddings_paper_chunk", "paper_id", "chunk_index"),
    )

