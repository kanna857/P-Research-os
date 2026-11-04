"""
Redis Cache & Job Coordination Service for ResearchOS.
Handles caching, task coordination, rate-limit tracking, worker heartbeats,
and job cancellation signals with robust fallback when Redis is offline.
"""

from typing import Dict, Any, Optional, List, Union
import json
import time
import logging
from datetime import datetime, timezone

from app.config import get_settings

logger = logging.getLogger(__name__)


class RedisCoordinator:
    """
    Manages caching, job signals, rate-limit enforcement, and worker communication.
    Employs an in-memory fallback cache when Redis server is unreachable.
    """

    def __init__(self):
        settings = get_settings()
        self.redis_url = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")
        self._client = None
        self._is_connected = False
        self._in_memory_cache: Dict[str, Dict[str, Any]] = {}
        self._cancellation_tokens: set = set()

    def _get_client(self):
        """Lazy-initialize Redis connection."""
        if self._client is None and not self._is_connected:
            try:
                import redis
                self._client = redis.Redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2.0,
                    socket_timeout=2.0,
                )
                self._client.ping()
                self._is_connected = True
                logger.info(f"Connected to Redis at {self.redis_url}")
            except Exception as e:
                self._client = None
                self._is_connected = False
                logger.debug(f"Redis unavailable, operating in in-memory fallback mode: {e}")
        return self._client

    # ── 1. Cache Operations ───────────────────────────────────────────────────

    def get(self, key: str) -> Optional[Any]:
        """Retrieve cached value with expiration check."""
        client = self._get_client()
        if client and self._is_connected:
            try:
                val = client.get(key)
                return json.loads(val) if val else None
            except Exception:
                pass

        # In-memory fallback
        item = self._in_memory_cache.get(key)
        if item:
            if item["expires_at"] is None or item["expires_at"] > time.time():
                return item["value"]
            else:
                del self._in_memory_cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Store key-value with TTL."""
        client = self._get_client()
        val_str = json.dumps(value)
        if client and self._is_connected:
            try:
                client.setex(key, ttl_seconds, val_str)
                return True
            except Exception:
                pass

        # In-memory fallback
        self._in_memory_cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds if ttl_seconds > 0 else None,
        }
        return True

    def delete(self, key: str) -> bool:
        """Remove key from cache."""
        client = self._get_client()
        if client and self._is_connected:
            try:
                client.delete(key)
            except Exception:
                pass
        self._in_memory_cache.pop(key, None)
        return True

    # ── 2. Job Cancellation & Signals ─────────────────────────────────────────

    def set_job_cancellation(self, job_id: str) -> bool:
        """Signal background worker to cancel active job."""
        self._cancellation_tokens.add(job_id)
        client = self._get_client()
        if client and self._is_connected:
            try:
                client.setex(f"cancel_job:{job_id}", 86400, "1")
                return True
            except Exception:
                pass
        return True

    def cancel_job(self, job_id: str) -> bool:
        """Alias for set_job_cancellation()."""
        return self.set_job_cancellation(job_id)

    def is_job_cancelled(self, job_id: str) -> bool:
        """Check if job has received a cancellation signal."""
        if job_id in self._cancellation_tokens:
            return True
        client = self._get_client()
        if client and self._is_connected:
            try:
                return bool(client.exists(f"cancel_job:{job_id}"))
            except Exception:
                pass
        return False

    def clear_job_cancellation(self, job_id: str):
        self._cancellation_tokens.discard(job_id)
        self.delete(f"cancel_job:{job_id}")

    # ── 3. Rate-Limit Sliding Window ──────────────────────────────────────────

    def check_rate_limit(self, identifier: str, max_requests: int = 60, window_seconds: int = 60) -> Dict[str, Any]:
        """
        Check and increment rate-limit counter using fixed/sliding window.
        """
        key = f"ratelimit:{identifier}"
        now = time.time()
        client = self._get_client()

        if client and self._is_connected:
            try:
                current = client.incr(key)
                if current == 1:
                    client.expire(key, window_seconds)
                ttl = client.ttl(key)
                allowed = current <= max_requests
                return {
                    "allowed": allowed,
                    "current": current,
                    "max_requests": max_requests,
                    "remaining": max(0, max_requests - current),
                    "reset_seconds": ttl,
                }
            except Exception:
                pass

        # In-memory fallback
        item = self._in_memory_cache.get(key)
        if not item or item["expires_at"] <= now:
            self._in_memory_cache[key] = {
                "value": 1,
                "expires_at": now + window_seconds,
            }
            return {"allowed": True, "current": 1, "max_requests": max_requests, "remaining": max_requests - 1, "reset_seconds": window_seconds}

        item["value"] += 1
        allowed = item["value"] <= max_requests
        return {
            "allowed": allowed,
            "current": item["value"],
            "max_requests": max_requests,
            "remaining": max(0, max_requests - item["value"]),
            "reset_seconds": int(item["expires_at"] - now),
        }

    # ── 4. Health Check ───────────────────────────────────────────────────────

    def get_health(self) -> Dict[str, Any]:
        """Return connectivity status and metrics."""
        client = self._get_client()
        connected = False
        memory_used = 0
        if client and self._is_connected:
            try:
                client.ping()
                info = client.info("memory")
                memory_used = info.get("used_memory_human", "N/A")
                connected = True
            except Exception:
                connected = False

        return {
            "connected": connected,
            "mode": "redis_cluster" if connected else "in_memory_fallback",
            "redis_url": self.redis_url if connected else "in_memory://internal",
            "cached_keys_count": len(self._in_memory_cache) if not connected else "managed_by_redis",
            "memory_used": memory_used if connected else f"{len(self._in_memory_cache)} items",
        }

    def health_check(self) -> Dict[str, Any]:
        """Alias for get_health()."""
        return self.get_health()


redis_coordinator = RedisCoordinator()
