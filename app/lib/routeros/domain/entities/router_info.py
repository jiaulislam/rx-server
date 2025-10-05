from datetime import datetime

from pydantic import BaseModel


class RouterInfo(BaseModel):
    """Domain entity representing router information."""

    host: str
    board_name: str
    platform: str
    version: str
    uptime: str
    last_updated: datetime | None = None
