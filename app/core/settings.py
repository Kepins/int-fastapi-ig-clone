from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    engine_url: str = "sqlite+pysqlite:///:memory:"
