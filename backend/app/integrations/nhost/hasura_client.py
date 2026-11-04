"""
Nhost Hasura GraphQL Client & PostgreSQL Integration.
Provides high-performance GraphQL operations, permissions enforcement,
realtime subscriptions helper, and database event logging.
"""

from typing import Dict, Any, List, Optional
import httpx
import logging
import json
from datetime import datetime, timezone

from app.config import get_settings

logger = logging.getLogger(__name__)


class HasuraGraphQLClient:
    """
    Client for interacting with Hasura GraphQL Engine and Nhost backend.
    Supports role-based user token authentication and administrative operations.
    """

    def __init__(self):
        settings = get_settings()
        self.endpoint = getattr(settings, "HASURA_GRAPHQL_ENDPOINT", "http://localhost:8080/v1/graphql")
        self.admin_secret = getattr(settings, "HASURA_GRAPHQL_ADMIN_SECRET", "nhost-admin-secret")
        self.nhost_subdomain = getattr(settings, "NHOST_SUBDOMAIN", "local")
        self.nhost_region = getattr(settings, "NHOST_REGION", "local")

    async def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        user_token: Optional[str] = None,
        role: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute GraphQL query/mutation against Hasura.
        If user_token is provided, uses user's JWT claims for row-level security.
        Otherwise uses admin secret for backend service-to-service calls.
        """
        headers = {
            "Content-Type": "application/json",
        }

        if user_token:
            headers["Authorization"] = f"Bearer {user_token}"
            if role:
                headers["x-hasura-role"] = role
        elif self.admin_secret:
            headers["x-hasura-admin-secret"] = self.admin_secret

        payload = {
            "query": query,
            "variables": variables or {},
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(self.endpoint, json=payload, headers=headers)
                if resp.status_code >= 400:
                    logger.warning(f"Hasura HTTP error {resp.status_code}: {resp.text}")
                    return {"errors": [{"message": f"HTTP {resp.status_code}: {resp.text}"}]}
                return resp.json()
        except Exception as e:
            logger.debug(f"Hasura connection error (fallback mode): {e}")
            return {"errors": [{"message": str(e)}], "fallback": True}

    # ── Convenient Research Operations ────────────────────────────────────────

    async def log_job_progress(
        self,
        job_id: str,
        project_id: int,
        job_type: str,
        progress_pct: float,
        step_message: str,
        status: str = "running",
        result_payload: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Persist or update research job progress in PostgreSQL for Hasura GraphQL subscriptions.
        Frontend subscribers receive instantaneous progress events.
        """
        mutation = """
        mutation UpsertResearchJob(
            $id: String!,
            $project_id: Int!,
            $job_type: String!,
            $status: String!,
            $progress_pct: Float!,
            $current_step: String!,
            $result_payload: jsonb
        ) {
            insert_research_jobs_one(
                object: {
                    id: $id,
                    project_id: $project_id,
                    job_type: $job_type,
                    status: $status,
                    progress_pct: $progress_pct,
                    current_step: $current_step,
                    result_payload: $result_payload
                },
                on_conflict: {
                    constraint: research_jobs_pkey,
                    update_columns: [status, progress_pct, current_step, result_payload, updated_at]
                }
            ) {
                id
                status
                progress_pct
            }
        }
        """
        variables = {
            "id": job_id,
            "project_id": project_id,
            "job_type": job_type,
            "status": status,
            "progress_pct": float(progress_pct),
            "current_step": step_message,
            "result_payload": result_payload or {},
        }
        res = await self.execute(mutation, variables)
        return "errors" not in res

    async def record_paper_dataset_link(
        self,
        project_id: int,
        paper_title: str,
        dataset_name: str,
        dataset_source: str,
        official_source_url: str,
        is_labeled_benchmark: bool,
        training_suitability: str,
        suitability_rationale: str,
        confidence_score: float = 0.95,
        paper_id: Optional[int] = None,
    ) -> bool:
        """Record a bipartite relationship between a discovered paper and a benchmark dataset."""
        mutation = """
        mutation InsertPaperDatasetLink(
            $project_id: Int!,
            $paper_id: Int,
            $paper_title: String!,
            $dataset_name: String!,
            $dataset_source: String!,
            $official_source_url: String,
            $is_labeled_benchmark: Boolean!,
            $training_suitability: String!,
            $suitability_rationale: String,
            $confidence_score: Float!
        ) {
            insert_paper_dataset_links_one(
                object: {
                    project_id: $project_id,
                    paper_id: $paper_id,
                    paper_title: $paper_title,
                    dataset_name: $dataset_name,
                    dataset_source: $dataset_source,
                    official_source_url: $official_source_url,
                    is_labeled_benchmark: $is_labeled_benchmark,
                    training_suitability: $training_suitability,
                    suitability_rationale: $suitability_rationale,
                    confidence_score: $confidence_score
                }
            ) {
                id
            }
        }
        """
        variables = {
            "project_id": project_id,
            "paper_id": paper_id,
            "paper_title": paper_title,
            "dataset_name": dataset_name,
            "dataset_source": dataset_source,
            "official_source_url": official_source_url,
            "is_labeled_benchmark": is_labeled_benchmark,
            "training_suitability": training_suitability,
            "suitability_rationale": suitability_rationale,
            "confidence_score": confidence_score,
        }
        res = await self.execute(mutation, variables)
        return "errors" not in res

    async def record_experiment_metric(
        self,
        experiment_id: int,
        epoch: int,
        train_loss: float,
        val_loss: float,
        accuracy: float,
        precision: float,
        recall: float,
        f1_score: float,
        iou: Optional[float] = None,
        dice: Optional[float] = None,
    ) -> bool:
        """Record epoch training metrics in PostgreSQL."""
        mutation = """
        mutation InsertMetric(
            $experiment_id: Int!,
            $epoch: Int!,
            $train_loss: Float,
            $val_loss: Float,
            $accuracy: Float,
            $precision: Float,
            $recall: Float,
            $f1_score: Float,
            $iou: Float,
            $dice: Float
        ) {
            insert_experiment_metrics_one(
                object: {
                    experiment_id: $experiment_id,
                    epoch: $epoch,
                    train_loss: $train_loss,
                    val_loss: $val_loss,
                    accuracy: $accuracy,
                    precision: $precision,
                    recall: $recall,
                    f1_score: $f1_score,
                    iou: $iou,
                    dice: $dice
                }
            ) {
                id
            }
        }
        """
        variables = {
            "experiment_id": experiment_id,
            "epoch": epoch,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "iou": iou,
            "dice": dice,
        }
        res = await self.execute(mutation, variables)
        return "errors" not in res


hasura_client = HasuraGraphQLClient()
