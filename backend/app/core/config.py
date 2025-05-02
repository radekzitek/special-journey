import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "./data/aiphb.db")


settings = Settings()
