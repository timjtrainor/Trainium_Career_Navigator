CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    response_time_ms DOUBLE PRECISION NOT NULL,
    error_category VARCHAR(10)
);
