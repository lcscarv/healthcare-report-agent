from functools import lru_cache

from sqlalchemy.engine import create_engine, Engine
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    srag_data_path: str
    database_url: str
    model_name: str = "gpt-4.o-mini"
    openai_api_key: str
    serp_api_key: str
    table_name: str
    web_search_headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (compatible; SRAGNewsBot/1.0)"
    }
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def engine(self) -> Engine:
        if not hasattr(self, "_engine"):
            self._engine = create_engine(self.database_url)
        return self._engine


@lru_cache()
def load_settings() -> Settings:
    return Settings()
