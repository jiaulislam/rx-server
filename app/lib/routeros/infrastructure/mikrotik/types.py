from dataclasses import dataclass


@dataclass
class MikrotikConnectionConfig:
    host: str
    username: str
    password: str
    port: int = 8728
    use_ssl: bool = False
    ssl_verify: bool = False
    timeout: int = 5
