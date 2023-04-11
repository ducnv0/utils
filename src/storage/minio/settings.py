from typing import Optional

from pydantic import BaseSettings


class MinioSettings(BaseSettings):
    """
    Get Minio configuration from environment variables
    """
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_ENDPOINT: str
    MINIO_SECURE: bool = True
    MINIO_DEFAULT_BUCKET: Optional[str]
