CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    job_unique_id TEXT NOT NULL,
    persona TEXT NOT NULL,
    provider TEXT NOT NULL,
    vote_bool BOOLEAN,
    rationale_text TEXT,
    latency_ms INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS evaluations_job_idx ON evaluations(job_unique_id);
