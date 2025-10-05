from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Base response structure for API responses."""

    success: bool
    data: T | None = None
    error_message: str | None = None
    timestamp: datetime = datetime.now()
