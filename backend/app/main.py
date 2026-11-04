"""
ResearchOS API – FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
import app.models  # Register all ORM models
from app.api import api_router
from app.utils.websocket_manager import ws_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: initialize database and background services."""
    await init_db()
    yield


app = FastAPI(
    title="ResearchOS API",
    version="1.0.0",
    description="Autonomous AI Research Operating System backend service.",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include Main API Router ────────────────────────────────────────────────────
app.include_router(api_router)


# ── WebSockets for Live Progress ──────────────────────────────────────────────
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str = "global"):
    """WebSocket connection for real-time telemetry, logs, and training updates."""
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or process client command if needed
            await websocket.send_text(f'{{"received": true, "channel": "{channel}"}}')
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, channel)
    except Exception:
        await ws_manager.disconnect(websocket, channel)


# ── Root & Health ─────────────────────────────────────────────────────────────
@app.get("/", tags=["status"])
async def root() -> dict:
    return {
        "name": "ResearchOS API",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs",
    }


@app.get("/health", tags=["status"])
async def health_check() -> dict:
    return {"status": "healthy", "service": "ResearchOS Backend"}


@app.get("/metrics", tags=["monitoring"])
async def root_prometheus_metrics():
    """Prometheus-compatible metrics exposition endpoint."""
    from fastapi import Response
    from app.integrations.infrastructure.monitoring_service import SystemMonitoringService
    monitor = SystemMonitoringService()
    health = await monitor.check_full_health()
    jobs = monitor.get_job_metrics()
    metrics_text = monitor.generate_prometheus_metrics(health, jobs)
    return Response(content=metrics_text, media_type="text/plain; version=0.0.4; charset=utf-8")
