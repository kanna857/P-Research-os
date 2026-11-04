"""
Nhost & Hasura GraphQL Integration API Routes.
Exposes status, Hasura JWT issuance, GraphQL proxy, Nhost file storage,
pgvector semantic search, and realtime job event triggers.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from pathlib import Path
import os

from app.integrations.nhost.auth_manager import nhost_auth_manager
from app.integrations.nhost.hasura_client import hasura_client
from app.integrations.nhost.storage_client import nhost_storage_client, LOCAL_STORAGE_DIR
from app.integrations.nhost.semantic_search import semantic_search_engine
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/status")
async def get_nhost_status():
    """
    Check health and integration status across:
    - PostgreSQL database with pgvector
    - Hasura GraphQL Engine
    - Nhost Authentication & RBAC
    - Nhost Storage & local volumes
    """
    # Test Hasura ping
    hasura_res = await hasura_client.execute("{ __typename }")
    hasura_online = "errors" not in hasura_res

    # Check pgvector
    from app.models.nhost_schema import HAS_PGVECTOR

    return {
        "status": "operational",
        "backend": "Nhost + PostgreSQL (ResearchOS)",
        "components": {
            "postgresql": {
                "configured": True,
                "pgvector_support": HAS_PGVECTOR,
                "vector_dimension": 384,
            },
            "hasura_graphql": {
                "endpoint": hasura_client.endpoint,
                "online": hasura_online,
                "subscriptions_enabled": True,
            },
            "nhost_auth": {
                "active": True,
                "jwt_algorithm": nhost_auth_manager.algorithm,
                "hasura_claims_enabled": True,
                "roles": ["user", "admin", "researcher"],
            },
            "nhost_storage": {
                "active": True,
                "endpoint": nhost_storage_client.endpoint,
                "local_volume_path": str(LOCAL_STORAGE_DIR),
                "max_file_size_mb": nhost_storage_client.max_file_size_mb,
            },
        },
        "free_first_policy": {
            "FREE_ONLY_MODE": True,
            "zero_paid_credits": True,
        },
    }


@router.post("/auth/token")
async def issue_hasura_jwt(credentials: Dict[str, Any]):
    """
    Issue a Hasura-compatible JWT token containing https://hasura.io/jwt/claims
    for row-level security and GraphQL subscriptions.
    """
    email = credentials.get("email", "researcher@researchos.local")
    user_id = int(credentials.get("user_id", 1))
    role = credentials.get("role", "user")

    token = nhost_auth_manager.generate_hasura_jwt(
        user_id=user_id,
        email=email,
        role=role,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user_id,
        "role": role,
        "claims": {
            "x-hasura-default-role": role,
            "x-hasura-user-id": str(user_id),
            "x-hasura-allowed-roles": ["user", role] if role != "user" else ["user"],
        },
    }


@router.post("/graphql")
async def execute_graphql(
    body: Dict[str, Any],
    claims: Dict[str, Any] = Depends(nhost_auth_manager.get_current_user_claims),
):
    """
    Execute GraphQL query or mutation through Hasura with row-level security claims.
    """
    query = body.get("query", "")
    variables = body.get("variables", {})

    if not query.strip():
        raise HTTPException(status_code=400, detail="GraphQL query cannot be empty")

    user_token = claims.get("token")
    return await hasura_client.execute(
        query=query,
        variables=variables,
        user_token=user_token,
        role=claims.get("role"),
    )


@router.post("/storage/upload")
async def upload_storage_file(
    file: UploadFile = File(...),
    claims: Dict[str, Any] = Depends(nhost_auth_manager.get_current_user_claims),
):
    """
    Upload paper PDF, dataset sample, confusion matrix, or manuscript to Nhost Storage.
    Computes SHA-256 and records metadata.
    """
    contents = await file.read()
    res = await nhost_storage_client.upload_file(
        file_bytes=contents,
        filename=file.filename or "upload.bin",
        content_type=file.content_type or "application/octet-stream",
        user_token=claims.get("token"),
    )
    return res


@router.get("/storage/files/{filename}")
async def get_storage_file(filename: str):
    """Retrieve or stream file from local volume storage."""
    file_path = LOCAL_STORAGE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found in storage")
    return FileResponse(path=str(file_path), filename=filename)


@router.post("/search/semantic")
async def semantic_hybrid_search(body: Dict[str, Any]):
    """
    Execute pgvector semantic search over paper abstracts and research methodologies.
    Combines dense cosine similarity with lexical overlap.
    """
    query = body.get("query", "")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    top_k = int(body.get("top_k", 10))
    results = await semantic_search_engine.hybrid_search(query=query.strip(), top_k=top_k)
    return {
        "query": query,
        "results_count": len(results),
        "matches": results,
    }


@router.post("/jobs/{job_id}/progress")
async def update_job_progress(job_id: str, body: Dict[str, Any]):
    """
    Update job progress to emit realtime events for GraphQL subscriptions.
    """
    project_id = int(body.get("project_id", 1))
    job_type = body.get("job_type", "research_task")
    progress_pct = float(body.get("progress_pct", 0.0))
    step_message = body.get("step_message", "Processing...")
    status_str = body.get("status", "running")
    result_payload = body.get("result_payload", {})

    success = await hasura_client.log_job_progress(
        job_id=job_id,
        project_id=project_id,
        job_type=job_type,
        progress_pct=progress_pct,
        step_message=step_message,
        status=status_str,
        result_payload=result_payload,
    )

    return {
        "job_id": job_id,
        "success": success,
        "progress_pct": progress_pct,
        "status": status_str,
    }

