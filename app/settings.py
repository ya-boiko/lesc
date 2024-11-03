"""Application settings."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings,SettingsConfigDict

from app.utils import get_env_file_path


class ApplicationSettings(BaseSettings):
    pass


class Settings(BaseModel):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=get_env_file_path(),
        env_nested_delimiter='__'
    )

    app: ApplicationSettings = ApplicationSettings()
