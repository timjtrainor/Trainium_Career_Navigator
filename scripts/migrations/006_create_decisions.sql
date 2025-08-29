CREATE TABLE IF NOT EXISTS decisions (
    id SERIAL PRIMARY KEY,
    job_unique_id TEXT NOT NULL UNIQUE,
    final_decision_bool BOOLEAN NOT NULL,
    confidence REAL NOT NULL,
    method TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
