-- Add salary and job type fields to support enhanced job postings
ALTER TABLE jobs_normalized ADD COLUMN IF NOT EXISTS salary_min INTEGER;
ALTER TABLE jobs_normalized ADD COLUMN IF NOT EXISTS salary_max INTEGER;
ALTER TABLE jobs_normalized ADD COLUMN IF NOT EXISTS job_type TEXT;