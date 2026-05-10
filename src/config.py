from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

if TYPE_CHECKING:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


class LLMConfig(BaseModel): ...


class DatabaseConfig(BaseModel):
    driver: PostgresDsn = "postgresql+asyncpg"
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


class Settings(BaseSettings):
    db: DatabaseConfig
    # llm: LLMConfig

    model_config = SettingsConfigDict(
        env_file=[BASE_DIR / ".env.example", BASE_DIR / ".env"],
        case_sensitive=False,
        env_prefix="MY_APP__",
        env_nested_delimiter="__",
    )


settings = Settings()
