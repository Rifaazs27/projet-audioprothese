"""Configuration de l'application, chargée depuis l'environnement.

Aucun secret n'est codé en dur : tout provient des variables
d'environnement (injectées par docker-compose ou par un Secret Kubernetes).
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Paramètres applicatifs."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Audioprothese API"
    environment: str = Field(default="development")

    # Base de données — surchargée par DATABASE_URL en production.
    database_url: str = Field(
        default="postgresql+psycopg://audio:audio@localhost:5432/audioprothese",
        alias="DATABASE_URL",
    )

    # CORS — origines autorisées pour le frontend.
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
