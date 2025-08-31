"""Backend configuration with environment variable loading."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def get_database_url() -> str:
    """Get database URL from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Construct from individual environment variables
    pg_host = os.getenv("POSTGRES_HOST", "postgres")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    pg_user = os.getenv("POSTGRES_USER", "trainium")
    pg_password = os.getenv("POSTGRES_PASSWORD", "changeme")
    pg_db = os.getenv("POSTGRES_DB", "trainium")
    
    return f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"