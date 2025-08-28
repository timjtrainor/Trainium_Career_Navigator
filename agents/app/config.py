import os
from pydantic import BaseModel

class Settings(BaseModel):
    environment: str = os.getenv("ENVIRONMENT", "local")

    # DBs
    pg_host: str = os.getenv("POSTGRES_HOST", "postgres")
    pg_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    pg_db: str   = os.getenv("POSTGRES_DB", "trainium")
    pg_user: str = os.getenv("POSTGRES_USER", "trainium")
    pg_pass: str = os.getenv("POSTGRES_PASSWORD", "devpassword")

    mongo_host: str = os.getenv("MONGO_HOST", "mongo")
    mongo_port: int = int(os.getenv("MONGO_PORT", "27017"))
    mongo_db:   str = os.getenv("MONGO_DB", "trainium")

    # LLM keys
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")

settings = Settings()