# Missed Opportunities Design

Missed Opportunities capture jobs a user applies to that Trainium did not surface.
This helps identify gaps in scraping, ranking, or filtering.

## Data Capture
- Record jobs the user applied to outside Trainium with job URL and metadata.
- Compare against surfaced jobs to detect gaps.
- Store all scraped jobs, including those rejected by the AI, for review.

## Future Workflow
1. User reports an external application.
2. System checks if the job was scraped but filtered out.
3. Analysts review AI-rejected listings to improve recall.
