from pydantic import AliasChoices, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings"]


class RouterOSConfig(BaseModel):
    host: str
    username: str
    password: str
    port: int
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

    routeros: RouterOSConfig

    model_config = SettingsConfigDict(env_nested_delimiter="__")
