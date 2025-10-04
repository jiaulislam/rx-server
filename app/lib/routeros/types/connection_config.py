from typing import Protocol


class ConnectionConfig(Protocol):
    host: str
    username: str
    password: str
    port: int
