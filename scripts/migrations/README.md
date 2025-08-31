# Database Migrations

This directory contains database migration scripts for the Trainium Career Navigator application.

## Alembic Integration

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database schema migrations.

### Configuration

- `alembic.ini` (in repository root): Main Alembic configuration
- `env.py`: Migration environment configuration  
- `versions/`: Directory for versioned migration files
- `*.sql`: Legacy SQL migration files

### Environment Variables

Alembic reads database connection settings from environment variables:

- `DATABASE_URL`: Complete database URL (optional)
- `POSTGRES_HOST`: Database host (default: postgres)
- `POSTGRES_PORT`: Database port (default: 5432)  
- `POSTGRES_USER`: Database user (default: trainium)
- `POSTGRES_PASSWORD`: Database password (default: changeme)
- `POSTGRES_DB`: Database name (default: trainium)

### Usage

```bash
# Apply all pending migrations
alembic upgrade head

# Show current migration version
alembic current

# Show migration history
alembic history

# Create a new migration
alembic revision -m "description of changes"

# Downgrade to previous version
alembic downgrade -1
```

### Legacy SQL Files

The existing `*.sql` files in this directory contain the schema definitions:

- `001_create_feedback.sql`: User feedback table
- `002_create_metrics.sql`: Metrics tracking table
- `003_create_jobs_normalized.sql`: Normalized job listings table
- `004_create_dedupe_review.sql`: Deduplication review table  
- `005_create_evaluations.sql`: Job evaluation results table
- `006_create_decisions.sql`: Final hiring decisions table

These can be manually applied or used as reference when creating Alembic migrations.