# Variáveis de ambiente: DB_URL, REDIS_URL, JWT_SECRET etc.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Polis"

    DATABASE_URL: str = "sqlite:///./polis.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()