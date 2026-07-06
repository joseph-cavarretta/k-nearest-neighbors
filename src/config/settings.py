from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    max_points_per_list: int = Field(
        default=50_000,
        description="Reject requests with more points than this per list",
    )
    balltree_leaf_size: int = Field(
        default=40,
        description="BallTree leaf size (sklearn default)",
    )
    log_level: str = Field(default="INFO", description="Application log level")


def get_settings() -> Settings:
    """Return a Settings instance loaded from environment and .env file."""
    return Settings()
