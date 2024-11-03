"""Application settings."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings,SettingsConfigDict

from app.utils import get_env_file_path


class ApplicationSettings(BaseModel):
    """Application settings."""

    version: str = "dev"
    port: int = 8000


class AuthSettings(BaseModel):
    """Authentication settings."""

    jwt_secret: str = ""
    jwt_expiration_delta_hours: int = 3600


class PostgresqlSettings(BaseModel):
    """Database settings."""

    url: str = ""


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=get_env_file_path(),
        env_nested_delimiter='__'
    )

    app: ApplicationSettings = ApplicationSettings()
    auth: AuthSettings = AuthSettings()
    database: PostgresqlSettings = PostgresqlSettings()
