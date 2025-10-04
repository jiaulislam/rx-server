from dataclasses import dataclass
from datetime import datetime


@dataclass
class RouterInfo:
    """Domain entity representing router information."""

    host: str
    board_name: str
    platform: str
    version: str
    uptime: str
    last_updated: datetime | None = None
