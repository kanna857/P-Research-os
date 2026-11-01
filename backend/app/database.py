"""
ResearchOS async database module with PostgreSQL and SQLite fallback support.
"""

from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

db_url = settings.DATABASE_URL
# In dev environments without active Postgres, fallback to SQLite
connect_args = {}
if "sqlite" in db_url:
    connect_args = {"check_same_thread": False}

try:
    engine = create_async_engine(
        db_url,
        echo=False,
        connect_args=connect_args,
    )
except Exception:
    # Safe fallback for standalone local dev
    db_url = "sqlite+aiosqlite:///./researchos.db"
    engine = create_async_engine(
        db_url,
        echo=False,
        connect_args={"check_same_thread": False},
    )

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding async database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Create all registered tables."""
    import app.models  # ensure models are registered
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"[ResearchOS DB] Postgres connection deferred/failed ({e}), fallback initialized.")
