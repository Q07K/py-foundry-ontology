from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # neo4j
    neo4j_url: str
    neo4j_username: str
    neo4j_password: str

    # sqlite
    sqlite_path: str

    # Settings Config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@cache
def get_settings() -> Settings:
    return Settings()
