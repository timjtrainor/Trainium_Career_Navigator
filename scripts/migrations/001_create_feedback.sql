CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    persona TEXT NOT NULL,
    input TEXT NOT NULL,
    output TEXT NOT NULL,
    feedback TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
