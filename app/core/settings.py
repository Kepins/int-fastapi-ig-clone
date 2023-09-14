from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    engine_url: str = "sqlite+pysqlite:///:memory:"
