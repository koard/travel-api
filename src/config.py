from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLDB_URL: str = "sqlite+aiosqlite:///database.db"

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
