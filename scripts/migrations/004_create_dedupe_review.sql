CREATE TABLE IF NOT EXISTS dedupe_review (
    id SERIAL PRIMARY KEY,
    job_id_1 INT NOT NULL REFERENCES jobs_normalized(id) ON DELETE CASCADE,
    job_id_2 INT NOT NULL REFERENCES jobs_normalized(id) ON DELETE CASCADE,
    similarity DOUBLE PRECISION NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ,
    CONSTRAINT dedupe_review_job_pair_unique UNIQUE (job_id_1, job_id_2)
);
