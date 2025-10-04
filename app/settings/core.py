from os import environ

from pydantic import AliasChoices, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings"]


class RouterOSConfig(BaseModel):
    host: str = environ.get("ROUTEROS_HOST", "")
    username: str = environ.get("ROUTEROS_USERNAME", "")
    password: str = environ.get("ROUTEROS_PASSWORD", "")
    port: int = int(environ.get("ROUTEROS_PORT", "8728"))
    use_ssl: bool = False
    ssl_verify: bool = False
    timeout: int = 5


class Settings(BaseSettings):
    app_name: str = "MikroTik Router Monitoring System"
    admin_email: str = "admin@example.com"
    db_url: str = "sqlite:///./test.db"
    secret_key: str = ""
    debug: bool = Field(
        default=False, validation_alias=AliasChoices("DEBUG", "debug", "DEBUG_MODE")
    )

    allowed_hosts: list[str] = Field(default_factory=list)

    routeros: RouterOSConfig = RouterOSConfig()

    model_config = SettingsConfigDict(env_file=".env")
