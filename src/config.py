from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).resolve().parent.parent


class DatabaseConfig(BaseModel):
    driver: str = "postgresql+asyncpg"
    user: str
    password: SecretStr
    host: str = "localhost"
    port: int = 5432
    name: str

    pool_size: int = 20
    max_overflow: int = 5
    echo: bool = False

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class AIConfig(BaseModel):
    class LLMConfig(BaseModel):
        class OllamaConfig(BaseModel):
            model: str
            base_url: str

        ollama: OllamaConfig

    class EmbeddingModelConfig(BaseModel):
        class HuggingFaceConfig(BaseModel):
            model: str = "sentence-transformers/all-MiniLM-L6-v2"
            device: Literal["cuda", "cpu"] = "cpu"

        hf: HuggingFaceConfig

    llm: LLMConfig
    embedding: EmbeddingModelConfig


class Settings(BaseSettings):
    db: DatabaseConfig
    ai: AIConfig

    model_config = SettingsConfigDict(
        env_file=[BASE_DIR / ".env.example", BASE_DIR / ".env"],
        case_sensitive=False,
        env_prefix="MY_APP__",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
