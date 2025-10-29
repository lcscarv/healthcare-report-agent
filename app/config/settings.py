from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    srag_data_path: str
    database_url: str
    model_name: str = "gpt-4.o-mini"
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


def load_settings() -> Settings:
    return Settings()
