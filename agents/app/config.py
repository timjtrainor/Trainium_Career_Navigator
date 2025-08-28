import os
from pydantic import BaseModel

class Settings(BaseModel):
    environment: str = os.getenv("ENVIRONMENT", "local")

    # DBs
    pg_host: str = os.getenv("POSTGRES_HOST")
    pg_port: int = int(os.getenv("POSTGRES_PORT"))
    pg_db: str   = os.getenv("POSTGRES_DB")
    pg_user: str = os.getenv("POSTGRES_USER")
    pg_pass: str = os.getenv("POSTGRES_PASSWORD")

    mongo_host: str = os.getenv("MONGO_HOST")
    mongo_port: int = int(os.getenv("MONGO_PORT"))
    mongo_db:   str = os.getenv("MONGO_DB")

    # LLM keys
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")

settings = Settings()
