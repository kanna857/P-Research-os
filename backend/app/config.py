"""
ResearchOS configuration module.

Loads all environment variables from .env using Pydantic Settings.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/researchos"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "researchos"

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── JWT / Auth ────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Nhost & Hasura GraphQL Configuration ──────────────────────────────────
    HASURA_GRAPHQL_ENDPOINT: str = "http://localhost:8080/v1/graphql"
    HASURA_GRAPHQL_ADMIN_SECRET: str = "nhost-admin-secret"
    NHOST_SUBDOMAIN: str = "local"
    NHOST_REGION: str = "local"
    NHOST_AUTH_URL: str = "http://localhost:8080/v1/auth"
    NHOST_STORAGE_ENDPOINT: str = "http://localhost:8080/v1/storage"
    NHOST_JWT_SECRET: str = "change-me-in-production-nhost-jwt-secret-key-32chars"

    # ── LLM API Keys ─────────────────────────────────────────────────────────
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    # ── Academic API Keys ─────────────────────────────────────────────────────
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = None
    OPENALEX_EMAIL: Optional[str] = None
    UNPAYWALL_EMAIL: Optional[str] = None

    # ── Datasets & Repositories (Kaggle & HuggingFace) ────────────────────────
    HUGGINGFACE_TOKEN: Optional[str] = None
    KAGGLE_USERNAME: Optional[str] = None
    KAGGLE_KEY: Optional[str] = None

    # ── Web Crawling & Scraping ───────────────────────────────────────────────
    CRAWLER_USER_AGENT: str = "ResearchOS-Academic-Crawler/1.0 (+https://github.com/kanna857/P-Research-os; polite academic indexer)"
    CRAWLER_RATE_LIMIT_SECONDS: float = 1.0
    CRAWLER_MAX_DEPTH: int = 2
    CRAWLER_CONCURRENCY_PER_DOMAIN: int = 2
    CRAWLER_CACHE_ENABLED: bool = True

    # ── Experiment Tracking ───────────────────────────────────────────────────
    CLEARML_API_KEY: Optional[str] = None
    CLEARML_API_SECRET: Optional[str] = None
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"

    # ── Object Storage (MinIO / S3) ───────────────────────────────────────────
    MINIO_ROOT_USER: str = "minioadmin"
    MINIO_ROOT_PASSWORD: str = "minioadmin"
    MINIO_ENDPOINT: str = "localhost:9000"

    S3_BUCKET_PAPERS: str = "researchos-papers"
    S3_BUCKET_DATASETS: str = "researchos-datasets"
    S3_BUCKET_MODELS: str = "researchos-models"
    S3_BUCKET_EXPORTS: str = "researchos-exports"

    # ── Free-First Policy & Academic Quota Controls ───────────────────────────
    FREE_ONLY_MODE: bool = True
    ENABLE_PAID_APIS: bool = False
    AUTO_PURCHASE_CREDITS: bool = False
    CORE_API_KEY: Optional[str] = None
    NASA_EARTHDATA_TOKEN: Optional[str] = None
    COPERNICUS_CLIENT_ID: Optional[str] = None
    COPERNICUS_CLIENT_SECRET: Optional[str] = None

    # ── GROBID ────────────────────────────────────────────────────────────────
    GROBID_URL: str = "http://localhost:8070"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance (created once per process)."""
    return Settings()
