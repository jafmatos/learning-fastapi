from pydantic_settings import SettingsConfigDict
from pydantic import Field
from pathlib import Path
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    API_TITLE: str = Field(..., description="Título da API")
    API_VERSION: str = Field(..., description="Versão da API")
    API_DESCRIPTION: str = Field(..., description="Descrição da API")
    API_SECRET_KEY: str = Field(..., description="Chave de API da aplicação")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

API_VERSION=settings.API_VERSION
API_TITLE=settings.API_TITLE
API_DESCRIPTION=settings.API_DESCRIPTION
API_SECRET_KEY=settings.API_SECRET_KEY