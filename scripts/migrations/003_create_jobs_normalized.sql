CREATE TABLE IF NOT EXISTS jobs_normalized (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    company TEXT,
    description TEXT,
    location TEXT,
    url TEXT,
    is_remote BOOLEAN,
    job_id_ext TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source, job_id_ext)
);
