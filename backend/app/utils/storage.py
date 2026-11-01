"""
Object storage utilities with automatic MinIO/S3 support and local filesystem fallback.
"""

import os
from pathlib import Path
from typing import Optional, BinaryIO
import asyncio

try:
    import aiofiles
except ImportError:
    aiofiles = None

from app.config import get_settings

settings = get_settings()

STORAGE_ROOT = Path("storage")
STORAGE_ROOT.mkdir(parents=True, exist_ok=True)


class StorageManager:
    def __init__(self):
        self.settings = settings
        self._s3_client = None

    def _get_s3_client(self):
        if self._s3_client is None:
            try:
                import boto3
                from botocore.client import Config
                self._s3_client = boto3.client(
                    "s3",
                    endpoint_url=f"http://{self.settings.MINIO_ENDPOINT}",
                    aws_access_key_id=self.settings.MINIO_ROOT_USER,
                    aws_secret_access_key=self.settings.MINIO_ROOT_PASSWORD,
                    config=Config(signature_version="s3v4"),
                    region_name="us-east-1",
                )
                # Ensure buckets exist
                buckets = [
                    self.settings.S3_BUCKET_PAPERS,
                    self.settings.S3_BUCKET_DATASETS,
                    self.settings.S3_BUCKET_MODELS,
                    self.settings.S3_BUCKET_EXPORTS,
                ]
                existing = [b["Name"] for b in self._s3_client.list_buckets().get("Buckets", [])]
                for b in buckets:
                    if b not in existing:
                        self._s3_client.create_bucket(Bucket=b)
            except Exception:
                self._s3_client = False
        return self._s3_client if self._s3_client is not False else None

    async def save_file(self, bucket: str, path: str, content: bytes) -> str:
        """Save file to storage and return relative path or URI."""
        s3 = self._get_s3_client()
        if s3:
            try:
                s3.put_object(Bucket=bucket, Key=path, Body=content)
                return f"s3://{bucket}/{path}"
            except Exception:
                pass

        # Fallback to local filesystem
        dest = STORAGE_ROOT / bucket / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        if aiofiles:
            async with aiofiles.open(dest, "wb") as f:
                await f.write(content)
        else:
            with open(dest, "wb") as f:
                f.write(content)
        return str(dest.as_posix())

    async def read_file(self, bucket: str, path: str) -> Optional[bytes]:
        """Read file from storage."""
        s3 = self._get_s3_client()
        if s3:
            try:
                resp = s3.get_object(Bucket=bucket, Key=path)
                return resp["Body"].read()
            except Exception:
                pass

        dest = STORAGE_ROOT / bucket / path
        if dest.exists():
            if aiofiles:
                async with aiofiles.open(dest, "rb") as f:
                    return await f.read()
            else:
                with open(dest, "rb") as f:
                    return f.read()
        return None

    def get_local_path(self, bucket: str, path: str) -> Path:
        """Return or prepare local path for file operations."""
        dest = STORAGE_ROOT / bucket / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        return dest


storage_manager = StorageManager()
